# Somalia Statistics Dashboard - Web Scraper Trigger Script
# This script triggers the web scraping processes via API endpoints

# API endpoints
$SCRAPER_SERVICE_URL = "http://localhost:8002/api/v1"
$API_SERVICE_URL = "http://localhost:8000/api/v1"
$AUTH_SERVICE_URL = "http://localhost:8001/api/auth"

function Write-Log {
    param (
        [string]$Message,
        [string]$Level = "INFO"
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $formattedMessage = "$timestamp - $Level - $Message"
    
    switch ($Level) {
        "INFO" { Write-Host $formattedMessage -ForegroundColor Green }
        "WARNING" { Write-Host $formattedMessage -ForegroundColor Yellow }
        "ERROR" { Write-Host $formattedMessage -ForegroundColor Red }
        default { Write-Host $formattedMessage }
    }
}

function Check-ETLStatus {
    try {
        Write-Log "Checking ETL consumer status..."
        $response = Invoke-RestMethod -Uri "$SCRAPER_SERVICE_URL/etl/status/" -Method Get -ErrorAction Stop
        
        Write-Log "ETL consumer status: $($response.status)"
        return $response.status -eq "running"
    }
    catch {
        Write-Log "Error checking ETL status: $_" -Level "ERROR"
        return $false
    }
}

function Trigger-StatisticsScraper {
    try {
        Write-Log "Triggering statistics scraper..."
        $body = @{
            publish = $true
        } | ConvertTo-Json
        
        $response = Invoke-RestMethod -Uri "$SCRAPER_SERVICE_URL/scraper/jobs/statistics/" -Method Post -Body $body -ContentType "application/json" -ErrorAction Stop
        
        $jobId = $response.id
        if (-not $jobId) {
            Write-Log "No job ID returned from the API" -Level "ERROR"
            return $false
        }
        
        Write-Log "Scraper job started with ID: $jobId"
        
        # Monitor the job status
        $maxAttempts = 60  # Wait for up to 5 minutes (60 * 5 seconds)
        for ($attempt = 0; $attempt -lt $maxAttempts; $attempt++) {
            # Check job status
            try {
                $statusResponse = Invoke-RestMethod -Uri "$SCRAPER_SERVICE_URL/scraper/jobs/$jobId/" -Method Get -ErrorAction Stop
                
                $jobStatus = $statusResponse.status
                $itemsFound = $statusResponse.items_found
                $itemsProcessed = $statusResponse.items_processed
                $itemsFailed = $statusResponse.items_failed
                
                Write-Log "Job status: $jobStatus - Found: $itemsFound, Processed: $itemsProcessed, Failed: $itemsFailed"
                
                if ($jobStatus -eq "completed") {
                    Write-Log "Scraper job completed successfully!"
                    return $true
                }
                elseif ($jobStatus -eq "failed") {
                    Write-Log "Scraper job failed: $($statusResponse.error_message)" -Level "ERROR"
                    return $false
                }
            }
            catch {
                Write-Log "Failed to get job status: $_" -Level "ERROR"
            }
            
            # Wait before checking again
            Start-Sleep -Seconds 5
        }
        
        Write-Log "Maximum monitoring time reached, job may still be running" -Level "WARNING"
        return $false
    }
    catch {
        Write-Log "Error triggering statistics scraper: $_" -Level "ERROR"
        return $false
    }
}

function Trigger-PublicationsScraper {
    try {
        Write-Log "Triggering publications scraper..."
        $body = @{
            publish = $true
        } | ConvertTo-Json
        
        $response = Invoke-RestMethod -Uri "$SCRAPER_SERVICE_URL/scraper/jobs/publications/" -Method Post -Body $body -ContentType "application/json" -ErrorAction Stop
        
        $jobId = $response.id
        if (-not $jobId) {
            Write-Log "No job ID returned from the API" -Level "ERROR"
            return $false
        }
        
        Write-Log "Scraper job started with ID: $jobId"
        
        # Monitor the job status
        $maxAttempts = 120  # Wait for up to 10 minutes (120 * 5 seconds)
        for ($attempt = 0; $attempt -lt $maxAttempts; $attempt++) {
            # Check job status
            try {
                $statusResponse = Invoke-RestMethod -Uri "$SCRAPER_SERVICE_URL/scraper/jobs/$jobId/" -Method Get -ErrorAction Stop
                
                $jobStatus = $statusResponse.status
                $itemsFound = $statusResponse.items_found
                $itemsProcessed = $statusResponse.items_processed
                $itemsFailed = $statusResponse.items_failed
                
                Write-Log "Job status: $jobStatus - Found: $itemsFound, Processed: $itemsProcessed, Failed: $itemsFailed"
                
                if ($jobStatus -eq "completed") {
                    Write-Log "Scraper job completed successfully!"
                    return $true
                }
                elseif ($jobStatus -eq "failed") {
                    Write-Log "Scraper job failed: $($statusResponse.error_message)" -Level "ERROR"
                    return $false
                }
            }
            catch {
                Write-Log "Failed to get job status: $_" -Level "ERROR"
            }
            
            # Wait before checking again
            Start-Sleep -Seconds 5
        }
        
        Write-Log "Maximum monitoring time reached, job may still be running" -Level "WARNING"
        return $false
    }
    catch {
        Write-Log "Error triggering publications scraper: $_" -Level "ERROR"
        return $false
    }
}

# Main execution
Write-Log "Starting Somalia Statistics Dashboard scraper"

# First check if the ETL consumer is running
$etlRunning = Check-ETLStatus
if (-not $etlRunning) {
    Write-Log "ETL consumer does not appear to be running, data may not be processed" -Level "WARNING"
}

# Trigger statistics scraper
Write-Log "Starting statistics scraper..."
$statisticsSuccess = Trigger-StatisticsScraper
if ($statisticsSuccess) {
    Write-Log "Statistics scraper completed successfully"
}
else {
    Write-Log "Statistics scraper failed or timed out" -Level "ERROR"
}

# Trigger publications scraper
Write-Log "Starting publications scraper..."
$publicationsSuccess = Trigger-PublicationsScraper
if ($publicationsSuccess) {
    Write-Log "Publications scraper completed successfully"
}
else {
    Write-Log "Publications scraper failed or timed out" -Level "ERROR"
}

Write-Log "All scraping jobs completed"
