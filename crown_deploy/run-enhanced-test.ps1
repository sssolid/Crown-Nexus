# File: run-enhanced-test.ps1

# Create test output directory
$testOutputDir = Join-Path (Get-Location) "test-output"
if (-not (Test-Path $testOutputDir)) {
    New-Item -Path $testOutputDir -ItemType Directory -Force
}

# Stop any existing containers
docker-compose -f docker-compose.enhanced.yml down

# Build and start enhanced containers
docker-compose -f docker-compose.enhanced.yml build
$result = docker-compose -f docker-compose.enhanced.yml up test-runner
$exitCode = $LASTEXITCODE

# Properly check the result
$success = $false
if ($exitCode -eq 0) {
    # Further verify by checking if README.md contains SUCCESS
    if (Test-Path "$testOutputDir/README.md") {
        $content = Get-Content "$testOutputDir/README.md" -Raw
        $success = $content -match "Test Result: SUCCESS"
    }
}

# Display results based on accurate success check
if ($success) {
    Write-Host "======================================"
    Write-Host "   Deployment Testing Succeeded!     " -ForegroundColor Green
    Write-Host "======================================"
    Write-Host "Scripts have been extracted to:"
    Write-Host "$testOutputDir"

    # Open file explorer to the scripts location
    explorer $testOutputDir
} else {
    Write-Host "======================================"
    Write-Host "     Deployment Testing Failed       " -ForegroundColor Red
    Write-Host "======================================"
    Write-Host "Exit code: $exitCode"
    Write-Host "Check logs for details"
    Write-Host "Log output from test runner:"

    # Show the last few lines with potential errors
    $result | Select-Object -Last 20
}
