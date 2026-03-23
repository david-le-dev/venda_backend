$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$venv = Join-Path $root ".venv"

if (-not (Test-Path $venv)) {
    python -m venv $venv
}

$python = Join-Path $venv "Scripts\\python.exe"
$pip = Join-Path $venv "Scripts\\pip.exe"

& $python -m pip install --upgrade pip
& $pip install -r (Join-Path $root "backend\\requirements.txt")
& $pip install -r (Join-Path $root "frontend_streamlit\\requirements.txt")

if (-not (Test-Path (Join-Path $root ".env"))) {
    Copy-Item (Join-Path $root ".env.example") (Join-Path $root ".env")
}

Write-Host "Local setup complete."
Write-Host "Activate with: .\\.venv\\Scripts\\Activate.ps1"
