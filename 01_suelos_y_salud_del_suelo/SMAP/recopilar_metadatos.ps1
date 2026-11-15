param([string]$Cutoff = '2026-11-14T23:59:59Z')
$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$utf8 = New-Object System.Text.UTF8Encoding($false)
$root = $PSScriptRoot
$geo = Join-Path $root 'geografia'
$meta = Join-Path $root 'metadatos'
New-Item -ItemType Directory -Force -Path $geo,$meta | Out-Null
function Save-Json($Path, $Value) {
    [IO.File]::WriteAllText($Path, ($Value | ConvertTo-Json -Depth 100 -Compress), $utf8)
}
function Get-Json($Url) {
    $value = Invoke-RestMethod -Uri $Url -TimeoutSec 90
    if ($value.error) { throw ($value.error | ConvertTo-Json -Compress) }
    return $value
}
$service = 'https://geoportal.eeq.com.ec/arcgis/rest/services/WEBGIS/Visor_cartografia/MapServer'
$provinceWhere = "DPA_PROVIN IN ('07','08','09','12','13','23','24')"
$provinceUrl = $service + '/31/query?where=' + [uri]::EscapeDataString($provinceWhere) + '&outFields=DPA_ANIO,DPA_PROVIN,DPA_DESPRO&outSR=4326&returnGeometry=true&f=geojson'
$provinces = Get-Json $provinceUrl
if (@($provinces.features).Count -ne 7) { throw 'No se recibieron exactamente siete provincias.' }
if (@($provinces.features | Where-Object { $_.properties.DPA_PROVIN -eq '12' }).Count -ne 1) { throw 'Falta Los Rios o esta duplicado.' }
if ($provinces.exceededTransferLimit) { throw 'Respuesta provincial truncada.' }
Save-Json (Join-Path $geo 'costa_provincias_referencia_2019.geojson') $provinces
$cantonUrl = $service + '/30/query?where=' + [uri]::EscapeDataString("DPA_PROVIN = '12'") + '&outFields=DPA_ANIO,DPA_PROVIN,DPA_DESPRO,DPA_CANTON,DPA_DESCAN&outSR=4326&returnGeometry=true&f=geojson'
$cantons = Get-Json $cantonUrl
if (@($cantons.features).Count -ne 13 -or $cantons.exceededTransferLimit) { throw 'La respuesta no contiene los 13 cantones de Los Rios sin truncamiento.' }
Save-Json (Join-Path $geo 'los_rios_cantones_referencia_2019.geojson') $cantons
$cantons.features.properties | Select-Object DPA_PROVIN,DPA_DESPRO,DPA_CANTON,DPA_DESCAN,DPA_ANIO | Export-Csv -LiteralPath (Join-Path $geo 'los_rios_cantones.csv') -NoTypeInformation -Encoding UTF8
$bounds = foreach ($feature in $provinces.features) {
    $where = "DPA_PROVIN = '" + $feature.properties.DPA_PROVIN + "'"
    $extentUrl = $service + '/31/query?where=' + [uri]::EscapeDataString($where) + '&returnExtentOnly=true&outSR=4326&f=json'
    $extent = (Get-Json $extentUrl).extent
    if ($null -eq $extent.xmin) { throw 'No se recibio la extension provincial.' }
    [pscustomobject]@{ provincia_id=$feature.properties.DPA_PROVIN; provincia=$feature.properties.DPA_DESPRO; anio_referencia=$feature.properties.DPA_ANIO; west=$extent.xmin; south=$extent.ymin; east=$extent.xmax; north=$extent.ymax }
}
$bounds | Export-Csv -LiteralPath (Join-Path $geo 'limites_por_provincia.csv') -NoTypeInformation -Encoding UTF8
$bbox = @(
    ($bounds | Measure-Object west -Minimum).Minimum,
    ($bounds | Measure-Object south -Minimum).Minimum,
    ($bounds | Measure-Object east -Maximum).Maximum,
    ($bounds | Measure-Object north -Maximum).Maximum
)
$bboxText = ($bbox | ForEach-Object { $_.ToString('R', [cultureinfo]::InvariantCulture) }) -join ','
$collection = Get-Json 'https://cmr.earthdata.nasa.gov/search/collections.json?short_name=SPL4SMGP&version=008&page_size=10'
Save-Json (Join-Path $meta 'coleccion_cmr.json') $collection
$entries = @($collection.feed.entry)
if ($entries.Count -ne 1) { throw 'La coleccion requiere revision: resultado ambiguo.' }
$cid = $entries[0].id
$base = 'https://cmr.earthdata.nasa.gov/search/granules.json?collection_concept_id=' + $cid + '&page_size=1&bounding_box=' + $bboxText
$temporal = '&temporal=' + [uri]::EscapeDataString('2010-01-01T00:00:00Z,' + $Cutoff)
$latestResponse = Invoke-WebRequest -UseBasicParsing -Uri ($base + $temporal + '&sort_key=-start_date') -TimeoutSec 90
$latest = $latestResponse.Content | ConvertFrom-Json
$first = Get-Json ($base + $temporal + '&sort_key=start_date')
Save-Json (Join-Path $meta 'primer_granulo.json') $first
Save-Json (Join-Path $meta 'ultimo_granulo.json') $latest
$annual = foreach ($year in 2010..([datetime]$Cutoff).Year) {
    $begin = '{0}-01-01T00:00:00Z' -f $year
    $end = '{0}-12-31T23:59:59Z' -f $year
    if ([datetime]$end -gt [datetime]$Cutoff) { $end = $Cutoff }
    $url = $base + '&temporal=' + [uri]::EscapeDataString($begin + ',' + $end)
    $response = Invoke-WebRequest -UseBasicParsing -Uri $url -TimeoutSec 90
    $hits = [long]$response.Headers['CMR-Hits']
    [pscustomobject]@{ year=$year; granules_found=$hits; requested_start_utc=$begin; requested_end_utc=$end; state=if($hits -eq 0){'sin_granulos'}else{'catalogados_no_descargados'} }
}
$annual | Export-Csv -LiteralPath (Join-Path $meta 'disponibilidad_anual.csv') -NoTypeInformation -Encoding UTF8
$lastEntry = @($latest.feed.entry)[0]
$manifest = [ordered]@{
    retrieved_at_utc=[datetime]::UtcNow.ToString('o'); requested_start='2010-01-01T00:00:00Z'; requested_cutoff=$Cutoff
    product='SPL4SMGP'; version='008'; collection_concept_id=$cid
    actual_first_start=$first.feed.entry[0].time_start; actual_last_start=$lastEntry.time_start; actual_last_end=$lastEntry.time_end
    catalog_hits=[long]$latestResponse.Headers['CMR-Hits']; bounding_box_wgs84=$bbox
    provinces_count=7; los_rios_cantons_count=13; geographic_reference_year='2019'
    province_query=$provinceUrl; canton_query=$cantonUrl; cmr_query=($base+$temporal+'&sort_key=-start_date')
    status='metadatos_y_geometrias_recopilados; humedad_no_descargada; acceso_Earthdata_pendiente'
    geography_limitation='Referencia DPA 2019 servida por EEQ; no equivale a limites legales vigentes ni a validacion de cobertura SMAP.'
    data_limitation='Los granulos son globales: los hits de la caja no prueban valores validos en Costa. No descargar granulos globales completos.'
}
Save-Json (Join-Path $meta 'manifiesto_recopilacion.json') $manifest
Get-ChildItem $geo,$meta -File | ForEach-Object {
    [pscustomobject]@{ file=$_.Name; bytes=$_.Length; sha256=(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash }
} | Export-Csv -LiteralPath (Join-Path $root 'archivos_recopilados.csv') -NoTypeInformation -Encoding UTF8
$manifest | ConvertTo-Json -Depth 5
