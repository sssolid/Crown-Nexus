# Code Stripper and Structure Mapper Tools

A collection of tools to prepare codebases for AI analysis by either:
1. Stripping unnecessary elements (comments, docstrings, whitespace) to reduce size
2. Generating detailed structural maps of the codebase

These tools help you efficiently share your code with AI assistants when the full codebase is too large or when you need to provide detailed structural information without sharing all implementation details.

## Tools Overview

- **`backend-stripper.py`**: Strips docstrings, comments, and extra whitespace from Python code
- **`frontend-stripper.py`**: Aggressively minifies frontend code (Vue, TypeScript, JavaScript, CSS, HTML)
- **`code-structure-mapper.py`**: Creates detailed structural maps of Python projects
- **`frontend-structure-mapper.py`**: Creates detailed structural maps of Vue/TypeScript frontend projects

## Installation

These tools have minimal dependencies and can be used with a standard Python 3.7+ installation.

```bash
# Clone the repository
git clone https://github.com/yourusername/code-stripper-tools.git
cd code-stripper-tools

# Install dependencies
pip install -r requirements.txt
```

### Dependencies

- For backend-stripper.py: Standard Python library (no external dependencies)
- For frontend-stripper.py: Standard Python library (no external dependencies)
- For code-structure-mapper.py: Standard Python library (no external dependencies)
- For frontend-structure-mapper.py: Standard Python library (no external dependencies)

## Usage Instructions

### Backend Code Stripper

Strips docstrings, comments, and extra whitespace from Python code while maintaining functionality.

```bash
python backend-stripper.py /path/to/python/code [options]
```

#### Options

- `--output`: Output file or directory (defaults to inputname_stripped)
- `--keep-blank-lines`: Keep blank lines in the output
- `--extensions`: Comma-separated list of file extensions to process (default: .py)

#### Examples

```bash
# Strip a single Python file
python backend-stripper.py app.py

# Strip a directory of Python files
python backend-stripper.py my_project/ --output my_project_stripped/

# Strip with custom extensions and keeping blank lines
python backend-stripper.py my_project/ --extensions .py,.pyw --keep-blank-lines
```

### Frontend Code Stripper

Aggressively minifies frontend code to reduce size while maintaining functionality.

```bash
python frontend-stripper.py /path/to/frontend/code [options]
```

#### Options

- `--output`: Output file or directory (defaults to inputname_minified)
- `--extensions`: Comma-separated list of file extensions to process (default: .vue,.ts,.js,.css,.scss,.html,.json,.tsx,.jsx)
- `--exclude-dirs`: Comma-separated list of directories to exclude (default: node_modules,dist,.git,.github,.vscode,.idea,coverage,build)

#### Examples

```bash
# Minify a single Vue file
python frontend-stripper.py Component.vue

# Minify a directory of frontend files
python frontend-stripper.py src/ --output src_minified/

# Minify with custom extensions and exclusions
python frontend-stripper.py src/ --extensions .vue,.ts --exclude-dirs node_modules,dist,tests
```

### Code Structure Mapper

Generates detailed structural maps of Python projects for AI analysis.

```bash
python code-structure-mapper.py /path/to/python/project [options]
```

#### Options

- `--output`: Output file (default: standard output)
- `--format`: Output format: json, markdown, mermaid, or text (default: markdown)
- `--project-name`: Project name (default: directory name)
- `--include-docstrings`: Include docstrings in the output
- `--include-source`: Include source code in the output
- `--max-docstring-length`: Maximum length for docstrings (default: 100)
- `--include-private`: Include private members in the output
- `--ignore`: Comma-separated list of patterns to ignore
- `--verbose`: Enable verbose output

#### Examples

```bash
# Generate markdown structure map of a Python project
python code-structure-mapper.py my_project/ --output my_project_structure.md

# Generate JSON structure with docstrings
python code-structure-mapper.py my_project/ --format json --output structure.json --include-docstrings

# Generate mermaid diagram ignoring test files
python code-structure-mapper.py my_project/ --format mermaid --output diagram.mmd --ignore "tests/,*_test.py"
```

### Frontend Structure Mapper

Generates detailed structural maps of Vue/TypeScript frontend projects for AI analysis.

```bash
python frontend-structure-mapper.py /path/to/frontend/project [options]
```

#### Options

- `--output`: Output file (default: standard output)
- `--format`: Output format: json, markdown, mermaid, or text (default: markdown)
- `--project-name`: Project name (default: directory name)
- `--include-templates`: Include Vue templates in the output
- `--ignore`: Comma-separated list of patterns to ignore
- `--verbose`: Enable verbose output

#### Examples

```bash
# Generate markdown structure map of a Vue project
python frontend-structure-mapper.py my_vue_project/ --output frontend_structure.md

# Generate JSON structure with templates
python frontend-structure-mapper.py my_vue_project/ --format json --output frontend.json --include-templates

# Generate text structure ignoring certain directories
python frontend-structure-mapper.py my_vue_project/ --format text --ignore "node_modules,dist,tests"
```

## Combined Usage Examples

### Windows: Process a Full-Stack Project

```batch
:: Create a directory for the processed output
mkdir processed_project

:: Strip and map the backend code
python backend-stripper.py backend_dir\ --output processed_project\backend_stripped\
python code-structure-mapper.py backend_dir\ --output processed_project\backend_structure.md --include-docstrings

:: Strip and map the frontend code
python frontend-stripper.py frontend_dir\ --output processed_project\frontend_stripped\
python frontend-structure-mapper.py frontend_dir\ --output processed_project\frontend_structure.md

:: Combine the structure files (optional)
type processed_project\backend_structure.md processed_project\frontend_structure.md > processed_project\full_structure.md
```

### Linux/macOS: Process a Full-Stack Project

```bash
# Create a directory for the processed output
mkdir -p processed_project

# Strip and map the backend code
python backend-stripper.py backend_dir/ --output processed_project/backend_stripped/
python code-structure-mapper.py backend_dir/ --output processed_project/backend_structure.md --include-docstrings

# Strip and map the frontend code
python frontend-stripper.py frontend_dir/ --output processed_project/frontend_stripped/
python frontend-structure-mapper.py frontend_dir/ --output processed_project/frontend_structure.md

# Combine the structure files (optional)
cat processed_project/backend_structure.md processed_project/frontend_structure.md > processed_project/full_structure.md
```

### One-liner for Linux/macOS

```bash
# Process everything and create a combined structure file
mkdir -p processed_project && \
python backend-stripper.py backend_dir/ --output processed_project/backend_stripped/ && \
python frontend-stripper.py frontend_dir/ --output processed_project/frontend_stripped/ && \
python code-structure-mapper.py backend_dir/ --output processed_project/backend_structure.md --include-docstrings && \
python frontend-structure-mapper.py frontend_dir/ --output processed_project/frontend_structure.md && \
cat processed_project/backend_structure.md processed_project/frontend_structure.md > processed_project/full_structure.md
```

### One-liner for Windows

```batch
mkdir processed_project && python backend-stripper.py backend_dir\ --output processed_project\backend_stripped\ && python frontend-stripper.py frontend_dir\ --output processed_project\frontend_stripped\ && python code-structure-mapper.py backend_dir\ --output processed_project\backend_structure.md --include-docstrings && python frontend-structure-mapper.py frontend_dir\ --output processed_project\frontend_structure.md && type processed_project\backend_structure.md processed_project\frontend_structure.md > processed_project\full_structure.md
```

## Best Practices for AI Assistance

1. **Structure Maps for Context**: Share structure maps first to give the AI a comprehensive overview of your project
   
2. **Stripped Code for Specific Issues**: Share relevant stripped code files when asking about specific implementation issues

3. **Combined Approach**: For complex issues, provide both the structure map and the relevant stripped code files

4. **Use Markdown Format**: When sharing structure maps with AI, the markdown format provides the best readability

5. **Focus on Relevant Directories**: Only process the directories relevant to your current task to reduce noise

6. **Include Important Docstrings**: When using the structure mapper, include docstrings for critical components to preserve important context

7. **Exclude Test and Build Artifacts**: Always exclude test directories, build artifacts, and dependencies to focus on your actual code

## Troubleshooting

- If you encounter encoding issues, try adding `--encoding utf-8` when running the scripts
- For large codebases, consider processing directories in smaller chunks
- For very complex TypeScript types, the frontend structure mapper might not capture all details perfectly

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

These tools are released under the MIT License.
