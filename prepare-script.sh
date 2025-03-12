#!/bin/bash
# This script prepares your codebase (both backend and frontend) for sharing with AI assistants
# by stripping docstrings, comments, and whitespace and generating UML diagrams

# Exit on any error
set -e

# Default values
PROJECT_DIR="."
OUTPUT_DIR="stripped_code"
DIAGRAM_FORMAT="png"
GENERATE_UML=true
GENERATE_MERMAID=true
STRIP_BACKEND=true
STRIP_FRONTEND=true
BACKEND_DIR=""
FRONTEND_DIR=""

# Display help
function show_help {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  -p, --project-dir DIR    Project directory (default: current directory)"
    echo "  -o, --output-dir DIR     Output directory (default: stripped_code)"
    echo "  -f, --format FORMAT      Diagram format: png, svg, pdf (default: png)"
    echo "  -b, --backend-dir DIR    Backend directory (relative to project dir)"
    echo "  -fe, --frontend-dir DIR  Frontend directory (relative to project dir)"
    echo "  --no-uml                 Don't generate standard UML diagrams"
    echo "  --no-mermaid             Don't generate Mermaid diagrams"
    echo "  --backend-only           Only process backend code"
    echo "  --frontend-only          Only process frontend code"
    echo "  -h, --help               Show this help message"
    exit 0
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -p|--project-dir)
            PROJECT_DIR="$2"
            shift 2
            ;;
        -o|--output-dir)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -f|--format)
            DIAGRAM_FORMAT="$2"
            shift 2
            ;;
        -b|--backend-dir)
            BACKEND_DIR="$2"
            shift 2
            ;;
        -fe|--frontend-dir)
            FRONTEND_DIR="$2"
            shift 2
            ;;
        --no-uml)
            GENERATE_UML=false
            shift
            ;;
        --no-mermaid)
            GENERATE_MERMAID=false
            shift
            ;;
        --backend-only)
            STRIP_FRONTEND=false
            shift
            ;;
        --frontend-only)
            STRIP_BACKEND=false
            shift
            ;;
        -h|--help)
            show_help
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            ;;
    esac
done

# Ensure project directory exists
if [ ! -d "$PROJECT_DIR" ]; then
    echo "Error: Project directory '$PROJECT_DIR' does not exist"
    exit 1
fi

# Determine backend and frontend directories if not specified
if [ -z "$BACKEND_DIR" ]; then
    # Try to find backend directory
    if [ -d "$PROJECT_DIR/backend" ]; then
        BACKEND_DIR="backend"
    else
        # Look for Python files in the project root
        if [ -n "$(find "$PROJECT_DIR" -maxdepth 1 -name "*.py" -print -quit)" ]; then
            BACKEND_DIR="."
        else
            echo "Warning: Could not determine backend directory. Use --backend-dir to specify."
            STRIP_BACKEND=false
        fi
    fi
fi

if [ -z "$FRONTEND_DIR" ]; then
    # Try to find frontend directory
    if [ -d "$PROJECT_DIR/frontend" ]; then
        FRONTEND_DIR="frontend"
    else
        # Check for Vue/React files in the project root
        if [ -n "$(find "$PROJECT_DIR" -maxdepth 1 -name "*.vue" -o -name "*.tsx" -o -name "package.json" -print -quit)" ]; then
            FRONTEND_DIR="."
        else
            echo "Warning: Could not determine frontend directory. Use --frontend-dir to specify."
            STRIP_FRONTEND=false
        fi
    fi
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Get the absolute path of the project and output directories
PROJECT_DIR=$(realpath "$PROJECT_DIR")
OUTPUT_DIR=$(realpath "$OUTPUT_DIR")

echo "=== Preparing code from $PROJECT_DIR ==="
echo "Output will be saved to $OUTPUT_DIR"

# Create directories
BACKEND_OUTPUT_DIR="$OUTPUT_DIR/backend"
FRONTEND_OUTPUT_DIR="$OUTPUT_DIR/frontend"
DIAGRAMS_DIR="$OUTPUT_DIR/diagrams"
mkdir -p "$DIAGRAMS_DIR"

# Check if required scripts exist
if [ "$STRIP_BACKEND" = true ] && [ ! -f "backend-stripper.py" ]; then
    echo "Error: backend-stripper.py not found in current directory"
    exit 1
fi

if [ "$STRIP_FRONTEND" = true ] && [ ! -f "frontend-stripper.py" ]; then
    echo "Error: frontend-stripper.py not found in current directory"
    exit 1
fi

if [ "$GENERATE_UML" = true ] || [ "$GENERATE_MERMAID" = true ]; then
    if [ ! -f "uml-generator.py" ]; then
        echo "Error: uml-generator.py not found in current directory"
        exit 1
    fi
fi

# Calculate original sizes if 'du' is available
if command -v du &> /dev/null; then
    if [ "$STRIP_BACKEND" = true ] && [ -n "$BACKEND_DIR" ]; then
        BACKEND_ORIGINAL_SIZE=$(du -sh "$PROJECT_DIR/$BACKEND_DIR" 2>/dev/null | cut -f1 || echo "unknown")
    fi

    if [ "$STRIP_FRONTEND" = true ] && [ -n "$FRONTEND_DIR" ]; then
        FRONTEND_ORIGINAL_SIZE=$(du -sh "$PROJECT_DIR/$FRONTEND_DIR" 2>/dev/null | cut -f1 || echo "unknown")
    fi
fi

# Run the code strippers
if [ "$STRIP_BACKEND" = true ] && [ -n "$BACKEND_DIR" ]; then
    echo "=== Stripping Python docstrings and comments ==="
    mkdir -p "$BACKEND_OUTPUT_DIR"
    python backend-stripper.py "$PROJECT_DIR/$BACKEND_DIR" --output "$BACKEND_OUTPUT_DIR" --extensions .py
fi

if [ "$STRIP_FRONTEND" = true ] && [ -n "$FRONTEND_DIR" ]; then
    echo "=== Stripping frontend code comments and whitespace ==="
    mkdir -p "$FRONTEND_OUTPUT_DIR"
    python frontend-stripper.py "$PROJECT_DIR/$FRONTEND_DIR" --output "$FRONTEND_OUTPUT_DIR"
fi

# Generate UML diagrams for backend code if requested
if [ "$GENERATE_UML" = true ] && [ "$STRIP_BACKEND" = true ] && [ -n "$BACKEND_DIR" ]; then
    echo "=== Generating standard UML class diagrams for backend ==="
    python uml-generator.py "$PROJECT_DIR/$BACKEND_DIR" --output-dir "$DIAGRAMS_DIR" --format "$DIAGRAM_FORMAT" --project-name "$(basename "$PROJECT_DIR")_backend"
fi

# Generate Mermaid diagrams for backend code if requested
if [ "$GENERATE_MERMAID" = true ] && [ "$STRIP_BACKEND" = true ] && [ -n "$BACKEND_DIR" ]; then
    echo "=== Generating Mermaid class diagrams for backend ==="
    python uml-generator.py "$PROJECT_DIR/$BACKEND_DIR" --output-dir "$DIAGRAMS_DIR" --mermaid --project-name "$(basename "$PROJECT_DIR")_backend"
fi

# Calculate sizes of stripped code
if command -v du &> /dev/null; then
    if [ "$STRIP_BACKEND" = true ] && [ -n "$BACKEND_DIR" ]; then
        BACKEND_STRIPPED_SIZE=$(du -sh "$BACKEND_OUTPUT_DIR" 2>/dev/null | cut -f1 || echo "unknown")
    fi

    if [ "$STRIP_FRONTEND" = true ] && [ -n "$FRONTEND_DIR" ]; then
        FRONTEND_STRIPPED_SIZE=$(du -sh "$FRONTEND_OUTPUT_DIR" 2>/dev/null | cut -f1 || echo "unknown")
    fi
fi

# Calculate line count statistics
if [ "$STRIP_BACKEND" = true ] && [ -n "$BACKEND_DIR" ]; then
    BACKEND_ORIGINAL_LINES=$(find "$PROJECT_DIR/$BACKEND_DIR" -name "*.py" -exec cat {} \; | wc -l)
    BACKEND_STRIPPED_LINES=$(find "$BACKEND_OUTPUT_DIR" -name "*.py" -exec cat {} \; | wc -l)
    BACKEND_REDUCTION=$(( 100 - (BACKEND_STRIPPED_LINES * 100 / BACKEND_ORIGINAL_LINES) ))
fi

if [ "$STRIP_FRONTEND" = true ] && [ -n "$FRONTEND_DIR" ]; then
    # Calculate frontend lines using multiple extensions
    FRONTEND_EXTS="-name *.vue -o -name *.ts -o -name *.js -o -name *.tsx -o -name *.jsx -o -name *.css -o -name *.scss -o -name *.html"

    # Use eval to handle the complex find command
    FRONTEND_ORIGINAL_LINES=$(eval "find \"$PROJECT_DIR/$FRONTEND_DIR\" \( $FRONTEND_EXTS \) -type f -not -path \"*/node_modules/*\" -not -path \"*/dist/*\" -exec cat {} \; | wc -l")
    FRONTEND_STRIPPED_LINES=$(eval "find \"$FRONTEND_OUTPUT_DIR\" \( $FRONTEND_EXTS \) -type f -exec cat {} \; | wc -l")

    if [ "$FRONTEND_ORIGINAL_LINES" -gt 0 ]; then
        FRONTEND_REDUCTION=$(( 100 - (FRONTEND_STRIPPED_LINES * 100 / FRONTEND_ORIGINAL_LINES) ))
    else
        FRONTEND_REDUCTION=0
    fi
fi

# Create a summary section
echo "=== Summary ==="

if [ "$STRIP_BACKEND" = true ] && [ -n "$BACKEND_DIR" ]; then
    echo "Backend code:"
    echo "  Original: $BACKEND_ORIGINAL_LINES lines ($BACKEND_ORIGINAL_SIZE)"
    echo "  Stripped: $BACKEND_STRIPPED_LINES lines ($BACKEND_STRIPPED_SIZE)"
    echo "  Line reduction: approximately $BACKEND_REDUCTION%"
    echo ""
fi

if [ "$STRIP_FRONTEND" = true ] && [ -n "$FRONTEND_DIR" ]; then
    echo "Frontend code:"
    echo "  Original: $FRONTEND_ORIGINAL_LINES lines ($FRONTEND_ORIGINAL_SIZE)"
    echo "  Stripped: $FRONTEND_STRIPPED_LINES lines ($FRONTEND_STRIPPED_SIZE)"
    echo "  Line reduction: approximately $FRONTEND_REDUCTION%"
    echo ""
fi

echo "Diagrams saved to: $DIAGRAMS_DIR"
echo ""

# Create a readme file with usage instructions
README_FILE="$OUTPUT_DIR/README.md"
cat > "$README_FILE" << EOF
# Code Prepared for AI Assistants

This directory contains a stripped-down version of the codebase with comments, docstrings,
and unnecessary whitespace removed to reduce size when sharing with AI assistants.

## Contents

EOF

# Add appropriate sections to README based on what was processed
if [ "$STRIP_BACKEND" = true ] && [ -n "$BACKEND_DIR" ]; then
    cat >> "$README_FILE" << EOF
- \`backend/\`: The stripped backend code files
EOF
fi

if [ "$STRIP_FRONTEND" = true ] && [ -n "$FRONTEND_DIR" ]; then
    cat >> "$README_FILE" << EOF
- \`frontend/\`: The stripped frontend code files
EOF
fi

cat >> "$README_FILE" << EOF
- \`diagrams/\`: UML and Mermaid diagrams of the code structure

## How to Use

When working with AI assistants like Claude:

1. **Share the stripped code files** instead of the original files.
   These maintain all functionality but are much smaller.

2. **Share the diagrams** to provide architectural context:
   - For Mermaid diagrams: Share the \`.mmd\` file contents in a code block with the "mermaid" language tag
   - For standard UML diagrams: Upload the PNG/SVG file directly

3. **Reference the original documentation** when needed for specific implementation details.

## Size Comparison

EOF

if [ "$STRIP_BACKEND" = true ] && [ -n "$BACKEND_DIR" ]; then
    cat >> "$README_FILE" << EOF
- Original backend code: $BACKEND_ORIGINAL_LINES lines ($BACKEND_ORIGINAL_SIZE)
- Stripped backend code: $BACKEND_STRIPPED_LINES lines ($BACKEND_STRIPPED_SIZE)
- Backend reduction: approximately $BACKEND_REDUCTION%
EOF
fi

if [ "$STRIP_FRONTEND" = true ] && [ -n "$FRONTEND_DIR" ]; then
    cat >> "$README_FILE" << EOF
- Original frontend code: $FRONTEND_ORIGINAL_LINES lines ($FRONTEND_ORIGINAL_SIZE)
- Stripped frontend code: $FRONTEND_STRIPPED_LINES lines ($FRONTEND_STRIPPED_SIZE)
- Frontend reduction: approximately $FRONTEND_REDUCTION%
EOF
fi

cat >> "$README_FILE" << EOF

## Generated on: $(date)
EOF

echo "=== Documentation ==="
echo "A README file with usage instructions has been created at $README_FILE"
echo ""
echo "Done! Your code is now ready for sharing with AI assistants."
