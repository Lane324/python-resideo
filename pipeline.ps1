Write-Host "Running formatter..." -f green
uv run ruff format
Write-Host "Running linter..." -f green
uv run ruff check
Write-Host "Running tests..." -f green
uv run pytest