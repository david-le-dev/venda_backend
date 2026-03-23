$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Join-Path $root ".venv\\Scripts\\python.exe"

if (-not (Test-Path $python)) {
    throw "Virtual environment not found. Run .\\setup_local.ps1 first."
}

Set-Location (Join-Path $root "backend")
& $python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
