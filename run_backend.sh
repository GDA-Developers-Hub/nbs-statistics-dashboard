#!/bin/bash

# Somalia Statistics Dashboard Backend Manager for WSL
# This script manages the backend services for the Somalia Statistics Dashboard

# Base directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend"
LOG_DIR="$SCRIPT_DIR/logs"
ENV_FILE="$BACKEND_DIR/.env"

# Service Ports
API_PORT=8000
AUTH_PORT=8001
SCRAPER_PORT=8002

# Celery Configuration
USE_CELERY=true  # Set to false to disable Celery workers

# Create logs directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Log files
API_LOG="$LOG_DIR/api_service.log"
AUTH_LOG="$LOG_DIR/auth_service.log"
SCRAPER_LOG="$LOG_DIR/scraper_service.log"
API_CELERY_LOG="$LOG_DIR/api_celery.log"
SCRAPER_CELERY_LOG="$LOG_DIR/scraper_celery.log"
CELERY_BEAT_LOG="$LOG_DIR/celery_beat.log"

# Create or update .env file with required environment variables
create_env_file() {
    cat > "$ENV_FILE" << EOL
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
EOL
    echo -e "\e[32mCreated/Updated .env file at $ENV_FILE\e[0m"
}

# Check for Python and pip
check_prerequisites() {
    echo -e "\e[33mChecking prerequisites...\e[0m"
    
    # Check for Python
    if ! command -v python3 &> /dev/null; then
        echo -e "\e[31m❌ Python3 is not installed or not in PATH\e[0m"
        echo -e "\e[33mPlease install Python 3.8+ using: sudo apt update && sudo apt install python3 python3-pip python3-venv\e[0m"
        exit 1
    else
        PYTHON_VERSION=$(python3 --version | awk '{print $2}')
        echo -e "\e[32m✅ Python $PYTHON_VERSION is installed\e[0m"
    fi
    
    # Check for pip
    if ! command -v pip3 &> /dev/null; then
        echo -e "\e[31m❌ pip3 is not installed or not in PATH\e[0m"
        echo -e "\e[33mPlease install pip3 using: sudo apt install python3-pip\e[0m"
        exit 1
    else
        PIP_VERSION=$(pip3 --version | awk '{print $2}')
        echo -e "\e[32m✅ pip $PIP_VERSION is installed\e[0m"
    fi
    
    # Check for virtualenv
    if ! command -v virtualenv &> /dev/null; then
        echo -e "\e[33mInstalling virtualenv...\e[0m"
        pip3 install virtualenv
    else
        VENV_VERSION=$(virtualenv --version)
        echo -e "\e[32m✅ virtualenv $VENV_VERSION is installed\e[0m"
    fi
    
    echo -e "\e[32m✅ All prerequisites are installed\e[0m"
}

# Create and activate virtual environment if it doesn't exist
setup_virtual_env() {
    if [ ! -d "$BACKEND_DIR/venv" ]; then
        echo -e "\e[33mCreating virtual environment...\e[0m"
        cd "$BACKEND_DIR" && virtualenv venv
        echo -e "\e[32m✅ Virtual environment created\e[0m"
    else
        echo -e "\e[32m✅ Virtual environment already exists\e[0m"
    fi
    
    # Activate virtual environment
    source "$BACKEND_DIR/venv/bin/activate"
    echo -e "\e[32m✅ Virtual environment activated\e[0m"
}

# Install dependencies
install_dependencies() {
    check_prerequisites
    setup_virtual_env
    create_env_file
    
    echo -e "\e[33mInstalling dependencies...\e[0m"
    pip3 install -r "$BACKEND_DIR/requirements.txt"
    echo -e "\e[32m✅ Dependencies installed\e[0m"
    
    echo -e "\n\e[32m🚀 Backend environment setup complete!\e[0m"
    echo -e "\e[32m💡 Next steps:\e[0m"
    echo -e "   1. Run migrations: \e[33m./run_backend.sh migrate\e[0m"
    echo -e "   2. Create a superuser: \e[33m./run_backend.sh superuser\e[0m"
    echo -e "   3. Start services: \e[33m./run_backend.sh start\e[0m"
}

# Run migrations for all services
run_migrations() {
    setup_virtual_env
    
    echo -e "\e[33mRunning database migrations for API service...\e[0m"
    cd "$BACKEND_DIR/api_service" && python3 manage.py migrate
    echo -e "\e[32m✅ API Service migrations applied\e[0m"
    
    echo -e "\e[33mRunning database migrations for Auth service...\e[0m"
    cd "$BACKEND_DIR/auth_service" && python3 manage.py migrate
    echo -e "\e[32m✅ Auth Service migrations applied\e[0m"
    
    echo -e "\e[33mRunning database migrations for Scraper service...\e[0m"
    cd "$BACKEND_DIR/scraper_service" && python3 manage.py migrate
    echo -e "\e[32m✅ Scraper Service migrations applied\e[0m"
    
    echo -e "\n\e[32m✅ All migrations completed successfully\e[0m"
}

# Start backend services
start_services() {
    setup_virtual_env
    
    echo -e "\e[33mStarting backend services...\e[0m"
    
    # Start API Service
    cd "$BACKEND_DIR/api_service" && python3 manage.py runserver 0.0.0.0:$API_PORT > "$API_LOG" 2>&1 &
    echo -e "\e[32m✅ API Service started on http://localhost:$API_PORT - Logs at $API_LOG\e[0m"
    
    # Start Auth Service
    cd "$BACKEND_DIR/auth_service" && python3 manage.py runserver 0.0.0.0:$AUTH_PORT > "$AUTH_LOG" 2>&1 &
    echo -e "\e[32m✅ Auth Service started on http://localhost:$AUTH_PORT - Logs at $AUTH_LOG\e[0m"
    
    # Start Scraper Service
    cd "$BACKEND_DIR/scraper_service" && python3 manage.py runserver 0.0.0.0:$SCRAPER_PORT > "$SCRAPER_LOG" 2>&1 &
    echo -e "\e[32m✅ Scraper Service started on http://localhost:$SCRAPER_PORT - Logs at $SCRAPER_LOG\e[0m"
    
    # Start Celery Workers if enabled
    if [ "$USE_CELERY" = true ]; then
        echo -e "\e[33mStarting Celery workers...\e[0m"
        
        # API Service Celery Worker
        cd "$BACKEND_DIR/api_service" && celery -A api_service worker --loglevel=info > "$API_CELERY_LOG" 2>&1 &
        echo -e "\e[32m✅ API Service Celery worker started - Logs at $API_CELERY_LOG\e[0m"
        
        # Scraper Service Celery Worker
        cd "$BACKEND_DIR/scraper_service" && celery -A scraper_service worker --loglevel=info > "$SCRAPER_CELERY_LOG" 2>&1 &
        echo -e "\e[32m✅ Scraper Service Celery worker started - Logs at $SCRAPER_CELERY_LOG\e[0m"
        
        # Celery Beat for Scheduled Tasks (using Scraper Service)
        cd "$BACKEND_DIR/scraper_service" && celery -A scraper_service beat --loglevel=info > "$CELERY_BEAT_LOG" 2>&1 &
        echo -e "\e[32m✅ Celery Beat scheduler started - Logs at $CELERY_BEAT_LOG\e[0m"
    fi
}

# Stop backend services
stop_services() {
    echo -e "\e[33mStopping backend services...\e[0m"
    
    # Find and kill Django development servers
    pkill -f "python3 manage.py runserver" || echo -e "\e[33mNo Django servers were running\e[0m"
    echo -e "\e[32m✅ Stopped Django services\e[0m"
    
    # Stop Celery workers if enabled
    if [ "$USE_CELERY" = true ]; then
        echo -e "\e[33mStopping Celery workers...\e[0m"
        pkill -f "celery" || echo -e "\e[33mNo Celery workers were running\e[0m"
        echo -e "\e[32m✅ Stopped Celery workers\e[0m"
    fi
}

# Create superuser for Auth service interactively
create_superuser() {
    setup_virtual_env
    create_env_file
    
    echo -e "\e[33mCreating superuser for Auth service...\e[0m"
    cd "$BACKEND_DIR/auth_service" && python3 manage.py createsuperuser
    echo -e "\e[32m✅ Superuser created successfully\e[0m"
}

# Display script usage
show_usage() {
    echo -e "\e[36mSomalia National Bureau of Statistics Dashboard - Backend Manager\e[0m"
    echo -e "\e[36m===================================================================\e[0m\n"
    echo -e "\e[33mUsage: ./run_backend.sh [command]\e[0m"
    echo -e "\n\e[33mAvailable commands:\e[0m"
    echo -e "  \e[37minstall   - Check prerequisites and install dependencies\e[0m"
    echo -e "  \e[37mmigrate   - Run database migrations for all services\e[0m"
    echo -e "  \e[37msuperuser - Create superuser for Auth service\e[0m"
    echo -e "  \e[37mstart     - Start all backend services\e[0m"
    echo -e "  \e[37mstop      - Stop all backend services\e[0m"
    echo -e "  \e[37mrestart   - Restart all backend services\e[0m"
    echo -e "\n\e[33mExample: ./run_backend.sh start\e[0m"
}

# Main command handler
case "$1" in
    "install")
        install_dependencies
        ;;
    "migrate")
        run_migrations
        ;;
    "superuser")
        create_superuser
        ;;
    "start")
        create_env_file
        start_services
        
        echo -e "\n\e[36m🚀 Somalia Statistics Dashboard Backend is running\e[0m"
        echo -e "\e[36m📊 API Service: http://localhost:$API_PORT\e[0m"
        echo -e "\e[36m🔐 Auth Service: http://localhost:$AUTH_PORT\e[0m"
        echo -e "\e[36m🤖 Scraper Service: http://localhost:$SCRAPER_PORT\e[0m"
        
        if [ "$USE_CELERY" = true ]; then
            echo -e "\e[36m🔄 Celery workers are running in the background\e[0m"
            echo -e "\e[36m⏱️ Scheduled tasks are managed by Celery Beat\e[0m"
        fi
        echo -e "\n\e[36mTo stop the services, run: ./run_backend.sh stop\e[0m"
        ;;
    "stop")
        stop_services
        echo -e "\n\e[36m🛑 Somalia Statistics Dashboard Backend stopped\e[0m"
        ;;
    "restart")
        stop_services
        start_services
        echo -e "\n\e[36m🔄 Somalia Statistics Dashboard Backend restarted\e[0m"
        ;;
    *)
        show_usage
        ;;
esac
