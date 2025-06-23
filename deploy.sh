#!/bin/bash

# AI-Backed Community Legal Aid Assistant - Deployment Script
# This script helps deploy the application to various environments

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if required tools are installed
check_requirements() {
    print_status "Checking requirements..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    print_success "All requirements satisfied."
}

# Function to create environment file
create_env_file() {
    if [ ! -f .env ]; then
        print_status "Creating environment file..."
        cp backend/.env.example .env
        print_warning "Please edit .env file with your configuration before deployment."
        print_warning "Especially set your OPENAI_API_KEY and SECRET_KEY."
    else
        print_status "Environment file already exists."
    fi
}

# Function to build images
build_images() {
    print_status "Building Docker images..."
    docker-compose build --no-cache
    print_success "Images built successfully."
}

# Function to deploy for development
deploy_development() {
    print_status "Deploying for development..."
    
    # Stop any running containers
    docker-compose down
    
    # Build and start services
    docker-compose up -d
    
    print_success "Development deployment completed."
    print_status "Frontend available at: http://localhost:3000"
    print_status "Backend API available at: http://localhost:8000"
    print_status "API Documentation available at: http://localhost:8000/api/docs"
}

# Function to deploy for production
deploy_production() {
    print_status "Deploying for production..."
    
    # Check if .env file exists
    if [ ! -f .env ]; then
        print_error "Environment file (.env) not found. Please create it first."
        exit 1
    fi
    
    # Stop any running containers
    docker-compose -f docker-compose.prod.yml down
    
    # Build and start services
    docker-compose -f docker-compose.prod.yml up -d
    
    print_success "Production deployment completed."
    print_status "Application available at: http://localhost"
    print_status "Backend API available at: http://localhost:8000"
}

# Function to stop services
stop_services() {
    print_status "Stopping services..."
    docker-compose down
    docker-compose -f docker-compose.prod.yml down 2>/dev/null || true
    print_success "Services stopped."
}

# Function to view logs
view_logs() {
    local service=${1:-}
    if [ -z "$service" ]; then
        docker-compose logs -f
    else
        docker-compose logs -f "$service"
    fi
}

# Function to run health checks
health_check() {
    print_status "Running health checks..."
    
    # Check backend health
    if curl -f http://localhost:8000/api/health &> /dev/null; then
        print_success "Backend is healthy."
    else
        print_error "Backend health check failed."
    fi
    
    # Check frontend health
    if curl -f http://localhost:3000/health &> /dev/null || curl -f http://localhost/health &> /dev/null; then
        print_success "Frontend is healthy."
    else
        print_error "Frontend health check failed."
    fi
}

# Function to initialize database
init_database() {
    print_status "Initializing database..."
    docker-compose exec backend python init_db.py
    print_success "Database initialized."
}

# Function to backup data
backup_data() {
    local backup_dir="backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"
    
    print_status "Creating backup in $backup_dir..."
    
    # Backup database
    docker-compose exec backend cp legal_aid.db /tmp/
    docker cp $(docker-compose ps -q backend):/tmp/legal_aid.db "$backup_dir/"
    
    # Backup generated documents
    docker cp $(docker-compose ps -q backend):/app/generated_documents "$backup_dir/"
    
    print_success "Backup created in $backup_dir"
}

# Function to show usage
show_usage() {
    echo "AI-Backed Community Legal Aid Assistant - Deployment Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  dev         Deploy for development"
    echo "  prod        Deploy for production"
    echo "  build       Build Docker images"
    echo "  stop        Stop all services"
    echo "  logs        View logs (optional: specify service name)"
    echo "  health      Run health checks"
    echo "  init-db     Initialize database"
    echo "  backup      Backup application data"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 dev                 # Deploy for development"
    echo "  $0 prod                # Deploy for production"
    echo "  $0 logs backend        # View backend logs"
    echo "  $0 health              # Check application health"
}

# Main script logic
main() {
    local command=${1:-help}
    
    case $command in
        "dev"|"development")
            check_requirements
            create_env_file
            deploy_development
            ;;
        "prod"|"production")
            check_requirements
            create_env_file
            deploy_production
            ;;
        "build")
            check_requirements
            build_images
            ;;
        "stop")
            stop_services
            ;;
        "logs")
            view_logs $2
            ;;
        "health")
            health_check
            ;;
        "init-db")
            init_database
            ;;
        "backup")
            backup_data
            ;;
        "help"|*)
            show_usage
            ;;
    esac
}

# Run main function with all arguments
main "$@"

