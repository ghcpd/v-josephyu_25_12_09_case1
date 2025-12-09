# PowerShell runner for pytest
.\.venv\Scripts\Activate.ps1
.venv\Scripts\pytest -q
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }