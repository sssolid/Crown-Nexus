#!/bin/bash
# Crown Nexus Deployment System - Test Runner
# Run deployment tests in Docker containers

# Function to display help
show_help() {
    echo "Crown Nexus Deployment System - Test Runner"
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  -h, --help          Show this help message"
    echo "  -g, --generate-only Generate scripts without running deployment"
    echo "  -d, --debug         Enable debug mode for verbose output"
    echo "  -c, --clean         Clean existing containers before running"
    echo "  -f, --full          Enable full deployment testing with all services"
    echo ""
    echo "Examples:"
    echo "  $0                  Run standard tests with deployment"
    echo "  $0 -f               Run full deployment with all services"
    echo "  $0 -g               Generate scripts only"
    echo "  $0 -c -f            Clean up and run full deployment tests"
    echo ""
}

# Parse command line options
GENERATE_ONLY=false
DEBUG=false
CLEAN=false
FULL_DEPLOYMENT=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help)
            show_help
            exit 0
            ;;
        -g|--generate-only)
            GENERATE_ONLY=true
            shift
            ;;
        -d|--debug)
            DEBUG=true
            shift
            ;;
        -c|--clean)
            CLEAN=true
            shift
            ;;
        -f|--full)
            FULL_DEPLOYMENT=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Clean up if requested
if $CLEAN; then
    echo "=== Cleaning up existing containers ==="
    docker compose down -v
fi

# Create output directory
mkdir -p test-output

# Set environment variables
ENV_VARS="-e SERVER_COUNT=3"

if $GENERATE_ONLY; then
    ENV_VARS="$ENV_VARS -e GENERATE_ONLY=true"
    echo "=== Running in GENERATE_ONLY mode ==="
fi

if $DEBUG; then
    ENV_VARS="$ENV_VARS -e DEBUG=true"
    echo "=== Debug mode enabled ==="
fi

if $FULL_DEPLOYMENT; then
    ENV_VARS="$ENV_VARS -e FULL_DEPLOYMENT=true"
    echo "=== Running with FULL DEPLOYMENT testing ==="

    # Create minimal directory structure for mounting
    mkdir -p backend frontend

    if [ ! -f "backend/main.py" ]; then
        echo "Creating minimal backend structure..."
        mkdir -p backend
        # Create empty files that will be populated in the container
        touch backend/main.py
        touch backend/requirements.txt
    fi

    if [ ! -f "frontend/package.json" ]; then
        echo "Creating minimal frontend structure..."
        mkdir -p frontend
        # Create empty files that will be populated in the container
        touch frontend/package.json
        touch frontend/index.html
    fi
fi

# Build the server base image first
echo "=== Building server base image ==="
docker compose build server-base

# Then build and run other containers
echo "=== Building remaining containers ==="
docker compose build

echo "=== Running tests ==="
docker compose run $ENV_VARS test-runner

# Check result
RESULT=$?
if [ $RESULT -eq 0 ]; then
    echo "=== Tests completed successfully ==="
    echo "Deployment scripts available in ./test-output/"
else
    echo "=== Tests failed with code $RESULT ==="
    echo "Check logs for details"
fi

# Show output files
if [ -d "test-output" ] && [ "$(ls -A test-output)" ]; then
    echo "=== Generated files ==="
    find test-output -type f -name "*.sh" | sort

    if [ -f "test-output/deployment-report.md" ]; then
        echo ""
        echo "=== Deployment Report ==="
        cat test-output/deployment-report.md
    fi
fi

exit $RESULT
