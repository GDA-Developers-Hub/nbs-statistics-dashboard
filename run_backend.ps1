# Somalia National Bureau of Statistics Dashboard
# Backend Services Startup Script

# Configuration
$BASE_DIR = Split-Path -Parent $MyInvocation.MyCommand.Definition
$BACKEND_DIR = Join-Path -Path $BASE_DIR -ChildPath "backend"
$ENV_FILE = Join-Path -Path $BACKEND_DIR -ChildPath ".env"
$LOG_DIR = Join-Path -Path $BASE_DIR -ChildPath "logs"

# Service Ports
$API_PORT = 8000
$AUTH_PORT = 8001
$SCRAPER_PORT = 8002

# Celery Configuration
$USE_CELERY = $true  # Set to $false to disable Celery workers

# Create logs directory if it doesn't exist
if (-not (Test-Path -Path $LOG_DIR)) {
    New-Item -ItemType Directory -Path $LOG_DIR | Out-Null
    Write-Host "Created logs directory at $LOG_DIR" -ForegroundColor Green
}

# Log files
$API_LOG = Join-Path -Path $LOG_DIR -ChildPath "api_service.log"
$AUTH_LOG = Join-Path -Path $LOG_DIR -ChildPath "auth_service.log"
$SCRAPER_LOG = Join-Path -Path $LOG_DIR -ChildPath "scraper_service.log"
$API_CELERY_LOG = Join-Path -Path $LOG_DIR -ChildPath "api_celery.log"
$SCRAPER_CELERY_LOG = Join-Path -Path $LOG_DIR -ChildPath "scraper_celery.log"
$CELERY_BEAT_LOG = Join-Path -Path $LOG_DIR -ChildPath "celery_beat.log"

# Create or update .env file with required environment variables
function Create-EnvFile {
    $envContent = @"
DEBUG=True
SECRET_KEY=your_secret_key_change_in_production
DATABASE_URL=postgresql://postgres:AhBiNDPahjXEJqOLxIcQQKHMpBltSyKK@switchback.proxy.rlwy.net:46640/railway
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173
JWT_SECRET_KEY=your_jwt_secret_change_in_production
API_VERSION=v1
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USER=snbsuser
RABBITMQ_PASSWORD=snbspassword
RABBITMQ_VHOST=snbs
SNBS_BASE_URL=https://nbs.gov.so/

# Celery settings
CELERY_BROKER_URL=amqp://snbsuser:snbspassword@localhost:5672/snbs
CELERY_RESULT_BACKEND=redis://localhost:6379/0
"@
    Set-Content -Path $ENV_FILE -Value $envContent -Force
    Write-Host "Created/Updated .env file at $ENV_FILE" -ForegroundColor Green
}

# Check prerequisites
function Check-Prerequisites {
    Write-Host "Checking prerequisites..." -ForegroundColor Yellow

    # Check Python
    try {
        $pythonVersion = python --version 2>&1
        if ($pythonVersion -match "Python 3") {
            Write-Host "✅ Python installed: $pythonVersion" -ForegroundColor Green
        } else {
            Write-Host "❌ Python 3.x required but found: $pythonVersion" -ForegroundColor Red
            return $false
        }
    } catch {
        Write-Host "❌ Python not found. Please install Python 3.9+ and add it to PATH" -ForegroundColor Red
        return $false
    }

    # Check pip
    try {
        $pipVersion = pip --version 2>&1
        Write-Host "✅ Pip installed: $pipVersion" -ForegroundColor Green
    } catch {
        Write-Host "❌ Pip not found. Please ensure pip is installed with Python" -ForegroundColor Red
        return $false
    }

    # Check PostgreSQL (simplified check - just looks for psql command)
    try {
        $pgVersion = psql --version 2>&1
        Write-Host "✅ PostgreSQL installed: $pgVersion" -ForegroundColor Green
    } catch {
        Write-Host "⚠️ PostgreSQL not found or not in PATH. Please ensure PostgreSQL is installed and running on port 5432" -ForegroundColor Yellow
        Write-Host "  Database should have user 'snbsuser' with password 'snbspassword' and database 'snbsdb'" -ForegroundColor Yellow
    }

    # Check RabbitMQ (simplified check - just looks for rabbitmqctl command)
    try {
        $rabbitVersion = rabbitmqctl status 2>&1
        Write-Host "✅ RabbitMQ is running" -ForegroundColor Green
    } catch {
        Write-Host "⚠️ RabbitMQ not found or not running. Please ensure RabbitMQ is installed and running on port 5672" -ForegroundColor Yellow
        Write-Host "  RabbitMQ should have vhost 'snbs', user 'snbsuser' with password 'snbspassword'" -ForegroundColor Yellow
    }

    return $true
}

# Install dependencies
function Install-Dependencies {
    Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
    Push-Location $BACKEND_DIR
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
        Pop-Location
        return $false
    }
    Pop-Location
    Write-Host "✅ Dependencies installed successfully" -ForegroundColor Green
    return $true
}

# Run database migrations
function Run-Migrations {
    Write-Host "Running database migrations..." -ForegroundColor Yellow
    
    # API Service
    Write-Host "Migrating API Service database..." -ForegroundColor Yellow
    Push-Location (Join-Path -Path $BACKEND_DIR -ChildPath "api_service")
    python manage.py migrate
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to migrate API Service database" -ForegroundColor Red
        Pop-Location
        return $false
    }
    Pop-Location
    
    # Auth Service
    Write-Host "Migrating Auth Service database..." -ForegroundColor Yellow
    Push-Location (Join-Path -Path $BACKEND_DIR -ChildPath "auth_service")
    python manage.py migrate
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to migrate Auth Service database" -ForegroundColor Red
        Pop-Location
        return $false
    }
    Pop-Location
    
    # Scraper Service
    Write-Host "Migrating Scraper Service database..." -ForegroundColor Yellow
    Push-Location (Join-Path -Path $BACKEND_DIR -ChildPath "scraper_service")
    python manage.py migrate
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to migrate Scraper Service database" -ForegroundColor Red
        Pop-Location
        return $false
    }
    Pop-Location
    
    Write-Host "✅ Database migrations completed successfully" -ForegroundColor Green
    return $true
}

# Start backend services
function Start-Services {
    Write-Host "Starting backend services..." -ForegroundColor Yellow
    
    # Start API Service
    Start-Process -FilePath "cmd.exe" -ArgumentList "/c python manage.py runserver 0.0.0.0:$API_PORT > $API_LOG 2>&1" -WorkingDirectory (Join-Path -Path $BACKEND_DIR -ChildPath "api_service") -WindowStyle Minimized
    Write-Host "✅ API Service started on http://localhost:$API_PORT - Logs at $API_LOG" -ForegroundColor Green
    
    # Start Auth Service
    Start-Process -FilePath "cmd.exe" -ArgumentList "/c python manage.py runserver 0.0.0.0:$AUTH_PORT > $AUTH_LOG 2>&1" -WorkingDirectory (Join-Path -Path $BACKEND_DIR -ChildPath "auth_service") -WindowStyle Minimized
    Write-Host "✅ Auth Service started on http://localhost:$AUTH_PORT - Logs at $AUTH_LOG" -ForegroundColor Green
    
    # Start Scraper Service
    Start-Process -FilePath "cmd.exe" -ArgumentList "/c python manage.py runserver 0.0.0.0:$SCRAPER_PORT > $SCRAPER_LOG 2>&1" -WorkingDirectory (Join-Path -Path $BACKEND_DIR -ChildPath "scraper_service") -WindowStyle Minimized
    Write-Host "✅ Scraper Service started on http://localhost:$SCRAPER_PORT - Logs at $SCRAPER_LOG" -ForegroundColor Green
    
    # Start Celery Workers if enabled
    if ($USE_CELERY) {
        Write-Host "Starting Celery workers..." -ForegroundColor Yellow
        
        # API Service Celery Worker
        Start-Process -FilePath "cmd.exe" -ArgumentList "/c celery -A api_service worker --loglevel=info > $API_CELERY_LOG 2>&1" -WorkingDirectory (Join-Path -Path $BACKEND_DIR -ChildPath "api_service") -WindowStyle Minimized
        Write-Host "✅ API Service Celery worker started - Logs at $API_CELERY_LOG" -ForegroundColor Green
        
        # Scraper Service Celery Worker
        Start-Process -FilePath "cmd.exe" -ArgumentList "/c celery -A scraper_service worker --loglevel=info > $SCRAPER_CELERY_LOG 2>&1" -WorkingDirectory (Join-Path -Path $BACKEND_DIR -ChildPath "scraper_service") -WindowStyle Minimized
        Write-Host "✅ Scraper Service Celery worker started - Logs at $SCRAPER_CELERY_LOG" -ForegroundColor Green
        
        # Celery Beat for Scheduled Tasks (using Scraper Service)
        Start-Process -FilePath "cmd.exe" -ArgumentList "/c celery -A scraper_service beat --loglevel=info > $CELERY_BEAT_LOG 2>&1" -WorkingDirectory (Join-Path -Path $BACKEND_DIR -ChildPath "scraper_service") -WindowStyle Minimized
        Write-Host "✅ Celery Beat scheduler started - Logs at $CELERY_BEAT_LOG" -ForegroundColor Green
    }
}

# Stop backend services (finds and kills Python processes running on specific ports)
function Stop-Services {
    Write-Host "Stopping backend services..." -ForegroundColor Yellow
    
    # Find all Python processes running on our ports
    $pythonProcesses = Get-NetTCPConnection -LocalPort $API_PORT,$AUTH_PORT,$SCRAPER_PORT -ErrorAction SilentlyContinue | 
                      Select-Object -ExpandProperty OwningProcess | 
                      ForEach-Object { Get-Process -Id $_ | Where-Object { $_.Name -eq "python" } }
    
    if ($pythonProcesses) {
        foreach ($process in $pythonProcesses) {
            Stop-Process -Id $process.Id -Force
            Write-Host "Stopped process on port $(($process | Get-NetTCPConnection).LocalPort)" -ForegroundColor Green
        }
    } else {
        Write-Host "No backend services found running on ports $API_PORT, $AUTH_PORT, $SCRAPER_PORT" -ForegroundColor Yellow
    }
    
    # Stop Celery workers if they're running
    if ($USE_CELERY) {
        Write-Host "Stopping Celery workers..." -ForegroundColor Yellow
        $celeryProcesses = Get-Process | Where-Object { $_.Name -eq "celery" -or $_.CommandLine -like "*celery*" } -ErrorAction SilentlyContinue
        
        if ($celeryProcesses) {
            foreach ($process in $celeryProcesses) {
                Stop-Process -Id $process.Id -Force
                Write-Host "Stopped Celery process with ID $($process.Id)" -ForegroundColor Green
            }
        } else {
            Write-Host "No Celery processes found running" -ForegroundColor Yellow
        }
    }
}

# Create superuser for Auth service interactively
function Create-Superuser {
    Write-Host "Creating superuser for Auth service..." -ForegroundColor Yellow
    Start-Process -FilePath "cmd.exe" -ArgumentList "/c python manage.py createsuperuser" -WorkingDirectory (Join-Path -Path $BACKEND_DIR -ChildPath "auth_service") -NoNewWindow -Wait
    Write-Host "✅ Superuser created successfully" -ForegroundColor Green
}

# Run statistics scraper
function Run-StatisticsScraper {
    param(
        [switch]$Publish
    )
    
    Write-Host "Running statistics scraper..." -ForegroundColor Yellow
    $publishArg = ""
    if ($Publish) {
        $publishArg = "--publish"
    }
    
    $statsScrapeLog = Join-Path -Path $LOG_DIR -ChildPath "stats_scraper.log"
    Start-Process -FilePath "cmd.exe" -ArgumentList "/c python manage.py run_statistics_scraper $publishArg > $statsScrapeLog 2>&1" -WorkingDirectory (Join-Path -Path $BACKEND_DIR -ChildPath "scraper_service") -NoNewWindow -Wait
    
    if (Test-Path $statsScrapeLog) {
        Get-Content -Path $statsScrapeLog | ForEach-Object { Write-Host $_ }
    }
    
    Write-Host "✅ Statistics scraper completed" -ForegroundColor Green
}

# Run publications scraper
function Run-PublicationsScraper {
    param(
        [switch]$Publish
    )
    
    Write-Host "Running publications scraper..." -ForegroundColor Yellow
    $publishArg = ""
    if ($Publish) {
        $publishArg = "--publish"
    }
    
    $pubsScrapeLog = Join-Path -Path $LOG_DIR -ChildPath "pubs_scraper.log"
    Start-Process -FilePath "cmd.exe" -ArgumentList "/c python manage.py run_publications_scraper $publishArg > $pubsScrapeLog 2>&1" -WorkingDirectory (Join-Path -Path $BACKEND_DIR -ChildPath "scraper_service") -NoNewWindow -Wait
    
    if (Test-Path $pubsScrapeLog) {
        Get-Content -Path $pubsScrapeLog | ForEach-Object { Write-Host $_ }
    }
    
    Write-Host "✅ Publications scraper completed" -ForegroundColor Green
}

# Main execution flow with command line parameter support
$command = $args[0]

# Create .env file if it doesn't exist
if (-not (Test-Path -Path $ENV_FILE)) {
    Create-EnvFile
}

switch ($command) {
    "install" {
        if (Check-Prerequisites) {
            Install-Dependencies
        }
    }
    "migrate" {
        Run-Migrations
    }
    "superuser" {
        Create-Superuser
    }
    "start" {
        Start-Services
        Write-Host "`n🚀 Somalia Statistics Dashboard Backend is running" -ForegroundColor Cyan
        Write-Host "📊 API Service: http://localhost:$API_PORT" -ForegroundColor Cyan
        Write-Host "🔐 Auth Service: http://localhost:$AUTH_PORT" -ForegroundColor Cyan
        Write-Host "🤖 Scraper Service: http://localhost:$SCRAPER_PORT" -ForegroundColor Cyan
        
        if ($USE_CELERY) {
            Write-Host "🔄 Celery workers are running in the background" -ForegroundColor Cyan
            Write-Host "⏱️ Scheduled tasks are managed by Celery Beat" -ForegroundColor Cyan
        }
        Write-Host "`nTo stop the services, run: .\run_backend.ps1 stop" -ForegroundColor Cyan
    }
    "stop" {
        Stop-Services
        Write-Host "✅ Backend services stopped" -ForegroundColor Green
    }
    "restart" {
        Stop-Services
        Start-Services
        Write-Host "`n🔄 Somalia Statistics Dashboard Backend restarted" -ForegroundColor Cyan
    }
    "scrape" {
        if ($args.Count -lt 2) {
            Write-Host "Please specify what to scrape: stats or pubs" -ForegroundColor Yellow
            Write-Host "Usage: .\run_backend.ps1 scrape stats|pubs [--publish]" -ForegroundColor Yellow
        } else {
            $scrapeType = $args[1].ToLower()
            $publish = $args -contains "--publish"
            
            if ($scrapeType -eq "stats") {
                Run-StatisticsScraper -Publish:$publish
            } elseif ($scrapeType -eq "pubs") {
                Run-PublicationsScraper -Publish:$publish
            } else {
                Write-Host "Invalid scrape type. Use 'stats' or 'pubs'" -ForegroundColor Red
            }
        }
    }
    default {
        Write-Host "Somalia National Bureau of Statistics Dashboard - Backend Manager" -ForegroundColor Cyan
        Write-Host "===================================================================`n" -ForegroundColor Cyan
        Write-Host "Usage: .\run_backend.ps1 [command]" -ForegroundColor Yellow
        Write-Host "`nAvailable commands:" -ForegroundColor Yellow
        Write-Host "  install   - Check prerequisites and install dependencies" -ForegroundColor White
        Write-Host "  migrate   - Run database migrations for all services" -ForegroundColor White
        Write-Host "  superuser - Create superuser for Auth service" -ForegroundColor White
        Write-Host "  start     - Start all backend services" -ForegroundColor White
        Write-Host "  stop      - Stop all backend services" -ForegroundColor White
        Write-Host "  restart   - Restart all backend services" -ForegroundColor White
        Write-Host "  scrape    - Run scrapers (use: scrape stats|pubs [--publish])" -ForegroundColor White
        Write-Host "`nExample: .\run_backend.ps1 start" -ForegroundColor Yellow
    }
}
