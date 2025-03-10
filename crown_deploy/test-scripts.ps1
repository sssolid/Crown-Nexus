# File: crown_deploy/test-scripts.ps1
# Simple test script for Crown Deploy

# Check for GenerateOnly parameter
$GenerateOnly = $false
foreach ($arg in $args) {
    if ($arg -eq "-GenerateOnly") {
        $GenerateOnly = $true
        break
    }
}

# Create test output directory
$testOutputDir = Join-Path (Get-Location) "test-output"
if (-not (Test-Path $testOutputDir)) {
    New-Item -Path $testOutputDir -ItemType Directory -Force | Out-Null
}

# Build command
$cmd = "docker-compose -f docker-compose.test.yml run -e TEST_MODE=true"
if ($GenerateOnly) {
    $cmd += " -e GENERATE_ONLY=true"
    Write-Host "Running in GENERATE_ONLY mode - scripts will be generated but not executed" -ForegroundColor Yellow
} else {
    Write-Host "Running with full test - scripts will be generated and tested" -ForegroundColor Cyan
}
$cmd += " test-runner"

# Execute command
Write-Host "Executing: $cmd"
Invoke-Expression $cmd

# Check result
if ($LASTEXITCODE -eq 0) {
    Write-Host "======================================"
    Write-Host "   Test Completed Successfully!      " -ForegroundColor Green
    Write-Host "======================================"
    Write-Host "Generated scripts are available in: $testOutputDir"
    explorer $testOutputDir
} else {
    Write-Host "======================================"
    Write-Host "   Test Failed                       " -ForegroundColor Red
    Write-Host "======================================"
    Write-Host "Check logs for details"
}
