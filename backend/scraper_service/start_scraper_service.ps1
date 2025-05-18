# PowerShell script to start the Somalia scraper scheduler as a background process
# This script will run the continuous scheduler and log its output

# Get the current directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path

# Set up log file path
$logFile = Join-Path $scriptPath "scraper_scheduler_service.log"

# Log start message
$startTime = Get-Date
"[$startTime] Starting Somalia scraper scheduler service" | Out-File -FilePath $logFile -Append

try {
    # Navigate to the scraper service directory
    Set-Location $scriptPath
    
    # Start the scraper scheduler in continuous mode
    # Use a job to run it in the background
    Start-Process -FilePath "python" -ArgumentList "manage.py run_scraper_scheduler --continuous --interval 60" -NoNewWindow -RedirectStandardOutput (Join-Path $scriptPath "scraper_output.log") -RedirectStandardError (Join-Path $scriptPath "scraper_error.log")
    
    "[$startTime] Scraper scheduler service started successfully in the background" | Out-File -FilePath $logFile -Append
    
    # Output a success message to the console
    Write-Host "Somalia scraper scheduler service started successfully."
    Write-Host "Logs are being written to: $logFile"
    Write-Host "Output is being written to: $(Join-Path $scriptPath "scraper_output.log")"
    Write-Host "Errors are being written to: $(Join-Path $scriptPath "scraper_error.log")"
    
} catch {
    # Log any errors
    $errorTime = Get-Date
    "[$errorTime] Error starting scheduler: $_" | Out-File -FilePath $logFile -Append
    $_.Exception.Message | Out-File -FilePath $logFile -Append
    
    # Output error to the console
    Write-Error "Failed to start Somalia scraper scheduler service: $_"
    exit 1
} 