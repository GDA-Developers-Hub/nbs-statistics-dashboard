# Somalia Statistics Dashboard - Direct Web Scraper
# This script directly scrapes the SNBS website without requiring backend services

# Configuration
$BASE_URL = "https://nbs.gov.so/"
$OUTPUT_DIR = Join-Path -Path $PSScriptRoot -ChildPath "scraped_data"
$STATS_OUTPUT_DIR = Join-Path -Path $OUTPUT_DIR -ChildPath "statistics"
$PUBS_OUTPUT_DIR = Join-Path -Path $OUTPUT_DIR -ChildPath "publications"

# Create output directories if they don't exist
if (-not (Test-Path -Path $OUTPUT_DIR)) {
    New-Item -ItemType Directory -Path $OUTPUT_DIR | Out-Null
    Write-Host "Created output directory at $OUTPUT_DIR" -ForegroundColor Green
}
if (-not (Test-Path -Path $STATS_OUTPUT_DIR)) {
    New-Item -ItemType Directory -Path $STATS_OUTPUT_DIR | Out-Null
}
if (-not (Test-Path -Path $PUBS_OUTPUT_DIR)) {
    New-Item -ItemType Directory -Path $PUBS_OUTPUT_DIR | Out-Null
}

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

function Scrape-Statistics {
    Write-Log "Starting statistics scraper..."
    
    try {
        # Main statistics page
        $statsPath = "statistics"
        $statsUrl = "$BASE_URL$statsPath"
        
        Write-Log "Fetching statistics page: $statsUrl"
        $response = Invoke-WebRequest -Uri $statsUrl -UseBasicParsing
        
        # Extract table data using regular expressions
        $tables = @()
        $links = @()
        
        # Look for links to statistics pages
        if ($response.Links) {
            foreach ($link in $response.Links) {
                if ($link.href -like "*/statistics/*" -or $link.href -like "*/data/*") {
                    $absoluteUrl = $null
                    
                    if ($link.href -match "^https?://") {
                        # Absolute URL
                        $absoluteUrl = $link.href
                    } else {
                        # Relative URL
                        $absoluteUrl = "$BASE_URL$($link.href.TrimStart('/'))"
                    }
                    
                    if ($absoluteUrl -and $links -notcontains $absoluteUrl) {
                        $links += $absoluteUrl
                        Write-Log "Found link: $absoluteUrl"
                    }
                }
            }
        }
        
        # Process each linked page to extract tables
        $tableCount = 0
        foreach ($link in $links) {
            try {
                Write-Log "Processing page: $link"
                $pageResponse = Invoke-WebRequest -Uri $link -UseBasicParsing
                
                # Extract tables from the page
                $htmlTables = $pageResponse.ParsedHtml.getElementsByTagName("table")
                
                if ($htmlTables -and $htmlTables.Length -gt 0) {
                    for ($i = 0; $i -lt $htmlTables.Length; $i++) {
                        $tableCount++
                        $htmlTable = $htmlTables[$i]
                        
                        # Extract table title (if available)
                        $tableTitle = "Table $tableCount"
                        $titleElements = $htmlTable.parentNode.getElementsByTagName("h1") + 
                                        $htmlTable.parentNode.getElementsByTagName("h2") +
                                        $htmlTable.parentNode.getElementsByTagName("h3") +
                                        $htmlTable.parentNode.getElementsByTagName("h4")
                        
                        if ($titleElements -and $titleElements.Length -gt 0) {
                            $tableTitle = $titleElements[0].innerText.Trim()
                        }
                        
                        # Convert table to CSV
                        $csv = ConvertFrom-Html -Table $htmlTable
                        
                        # Save to file
                        $fileName = "table_$($tableCount)_$(Get-Date -Format 'yyyyMMddHHmmss').csv"
                        $filePath = Join-Path -Path $STATS_OUTPUT_DIR -ChildPath $fileName
                        $csv | Out-File -FilePath $filePath -Encoding utf8
                        
                        Write-Log "Saved table '$tableTitle' to $fileName"
                        
                        # Store metadata
                        $metadata = @{
                            "title" = $tableTitle
                            "source_url" = $link
                            "extracted_date" = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
                            "file_path" = $filePath
                        }
                        
                        $metadataPath = Join-Path -Path $STATS_OUTPUT_DIR -ChildPath "$([IO.Path]::GetFileNameWithoutExtension($fileName)).json"
                        $metadata | ConvertTo-Json | Out-File -FilePath $metadataPath -Encoding utf8
                    }
                }
            }
            catch {
                Write-Log "Error processing page $link`: $_" -Level "ERROR"
            }
        }
        
        Write-Log "Statistics scraping completed. Extracted $tableCount tables"
        return $tableCount -gt 0
    }
    catch {
        Write-Log "Error in statistics scraper: $_" -Level "ERROR"
        return $false
    }
}

function Scrape-Publications {
    Write-Log "Starting publications scraper..."
    
    try {
        # Main publications page
        $pubsPath = "publications"
        $pubsUrl = "$BASE_URL$pubsPath"
        
        Write-Log "Fetching publications page: $pubsUrl"
        $response = Invoke-WebRequest -Uri $pubsUrl -UseBasicParsing
        
        # Extract PDF links
        $pdfLinks = @()
        
        if ($response.Links) {
            foreach ($link in $response.Links) {
                if ($link.href -like "*.pdf") {
                    $absoluteUrl = $null
                    
                    if ($link.href -match "^https?://") {
                        # Absolute URL
                        $absoluteUrl = $link.href
                    } else {
                        # Relative URL
                        $absoluteUrl = "$BASE_URL$($link.href.TrimStart('/'))"
                    }
                    
                    if ($absoluteUrl -and $pdfLinks -notcontains $absoluteUrl) {
                        $pdfLinks += $absoluteUrl
                        Write-Log "Found PDF: $absoluteUrl"
                    }
                }
            }
        }
        
        # Download PDFs
        $pdfCount = 0
        foreach ($pdfLink in $pdfLinks) {
            try {
                $pdfName = [System.IO.Path]::GetFileName($pdfLink)
                $pdfPath = Join-Path -Path $PUBS_OUTPUT_DIR -ChildPath $pdfName
                
                Write-Log "Downloading PDF: $pdfName"
                Invoke-WebRequest -Uri $pdfLink -OutFile $pdfPath
                
                $pdfCount++
                
                # Store metadata
                $metadata = @{
                    "title" = $pdfName
                    "source_url" = $pdfLink
                    "extracted_date" = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
                    "file_path" = $pdfPath
                }
                
                $metadataPath = Join-Path -Path $PUBS_OUTPUT_DIR -ChildPath "$([IO.Path]::GetFileNameWithoutExtension($pdfName)).json"
                $metadata | ConvertTo-Json | Out-File -FilePath $metadataPath -Encoding utf8
            }
            catch {
                Write-Log "Error downloading PDF $pdfLink`: $_" -Level "ERROR"
            }
        }
        
        Write-Log "Publications scraping completed. Downloaded $pdfCount PDFs"
        return $pdfCount -gt 0
    }
    catch {
        Write-Log "Error in publications scraper: $_" -Level "ERROR"
        return $false
    }
}

# Helper function to convert HTML tables to CSV
function ConvertFrom-Html {
    param (
        [Parameter(Mandatory=$true)]
        $Table
    )
    
    $rows = @()
    
    # Process header row
    $headerRow = $Table.getElementsByTagName("th")
    if ($headerRow -and $headerRow.Length -gt 0) {
        $headers = @()
        foreach ($cell in $headerRow) {
            $headers += $cell.innerText.Trim()
        }
        $rows += $headers -join ","
    }
    
    # Process data rows
    $dataRows = $Table.getElementsByTagName("tr")
    foreach ($row in $dataRows) {
        $cells = $row.getElementsByTagName("td")
        if ($cells -and $cells.Length -gt 0) {
            $rowData = @()
            foreach ($cell in $cells) {
                # Replace commas with semicolons to avoid CSV issues
                $cellText = $cell.innerText.Trim().Replace(",", ";")
                $rowData += $cellText
            }
            $rows += $rowData -join ","
        }
    }
    
    return $rows -join "`n"
}

# Main execution
Write-Log "Starting Somalia Statistics Dashboard direct scraper"

# Scrape statistics
$statsSuccess = Scrape-Statistics
if ($statsSuccess) {
    Write-Log "Statistics scraping completed successfully"
}
else {
    Write-Log "Statistics scraping failed or found no data" -Level "ERROR"
}

# Scrape publications
$pubsSuccess = Scrape-Publications
if ($pubsSuccess) {
    Write-Log "Publications scraping completed successfully"
}
else {
    Write-Log "Publications scraping failed or found no data" -Level "ERROR"
}

Write-Log "Scraping completed. Check the following directories for results:"
Write-Log "Statistics data: $STATS_OUTPUT_DIR"
Write-Log "Publications data: $PUBS_OUTPUT_DIR"
