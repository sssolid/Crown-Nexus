# File: run-enhanced-tests.ps1

# Create test output directory
$testOutputDir = Join-Path (Get-Location) "test-output"
if (-not (Test-Path $testOutputDir)) {
    New-Item -Path $testOutputDir -ItemType Directory -Force
}

# Stop any existing containers
docker-compose -f docker-compose.enhanced.yml down

# Build and start enhanced containers
docker-compose -f docker-compose.enhanced.yml build
docker-compose -f docker-compose.enhanced.yml up test-runner

# Display result
if ($LASTEXITCODE -eq 0) {
    Write-Host "======================================"
    Write-Host "   Deployment Testing Succeeded!     "
    Write-Host "======================================"
    Write-Host "Scripts have been extracted to:"
    Write-Host "$testOutputDir"

    # Open file explorer to the scripts location
    explorer $testOutputDir
} else {
    Write-Host "======================================"
    Write-Host "     Deployment Testing Failed       "
    Write-Host "======================================"
    Write-Host "Check the logs for error details"
}
