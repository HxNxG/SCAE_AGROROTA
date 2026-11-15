$ErrorActionPreference = 'Stop'
$repo = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$python = Join-Path $repo '.venv-smap/Scripts/python.exe'
$script = Join-Path $PSScriptRoot 'recopilar_humedad.py'
$folder = Join-Path $PSScriptRoot 'datos/historico'
New-Item -ItemType Directory -Path $folder -Force | Out-Null
$running = @(Get-CimInstance Win32_Process | Where-Object {
    $_.Name -eq 'python.exe' -and $_.CommandLine -like '*recopilar_humedad.py*' -and $_.CommandLine -like '*--name historico*'
})
if ($running.Count -gt 0) {
    Write-Output 'Ya existe una recopilacion del historico activa. No se iniciara otra.'
    $running | Select-Object ProcessId,ParentProcessId
    exit 0
}
if (-not (Test-Path -LiteralPath $python)) { throw 'Falta el entorno Python SMAP.' }
$arguments = '-u "' + $script + '" --start 2015-03-31 --end 2026-11-11 --name historico --workers 4'
$process = Start-Process -FilePath $python -ArgumentList $arguments -WorkingDirectory $repo -WindowStyle Hidden -RedirectStandardOutput (Join-Path $folder 'recopilacion.log') -RedirectStandardError (Join-Path $folder 'recopilacion.err.log') -PassThru
$info = [ordered]@{ launcher_pid=$process.Id; started_at_utc=[datetime]::UtcNow.ToString('o'); status_file='datos/historico/estado.json'; note='El equipo debe permanecer encendido y con Internet. Un estado running guardado no garantiza que el proceso siga vivo.' }
$utf8 = New-Object System.Text.UTF8Encoding($false)
[IO.File]::WriteAllText((Join-Path $folder 'proceso.json'), ($info | ConvertTo-Json), $utf8)
$info | ConvertTo-Json
