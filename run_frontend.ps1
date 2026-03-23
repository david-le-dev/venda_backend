$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Join-Path $root ".venv\\Scripts\\python.exe"

if (-not (Test-Path $python)) {
    throw "Virtual environment not found. Run .\\setup_local.ps1 first."
}

Set-Location (Join-Path $root "frontend_streamlit")
& $python -m streamlit run app.py
