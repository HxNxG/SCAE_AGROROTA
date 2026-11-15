$ErrorActionPreference = 'Stop'
$repo = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$python = Join-Path $repo '.venv-smap/Scripts/python.exe'
if (-not (Test-Path -LiteralPath $python)) { throw 'El entorno SMAP todavia no esta instalado.' }
& $python (Join-Path $PSScriptRoot 'autenticar_earthdata.py')
if ($LASTEXITCODE -ne 0) { throw 'Autenticacion no completada.' }
