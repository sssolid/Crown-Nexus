# Crown Nexus Pylint Plugins

This package contains custom Pylint plugins for the Crown Nexus project.

## Audit Checker

The Audit Checker plugin identifies functions that should include audit logging based on
their names and operations. It checks for the presence of proper audit calls in these functions.

### Installation

```bash
# Install from the project directory
pip install -e tools/crown_nexus_pylint

# Or install directly from the package
pip install crown-nexus-pylint
```

### Usage

```bash
# Run pylint with only the audit checker
pylint --load-plugins=crown_nexus_pylint.audit_checker --disable=all --enable=missing-audit-logging your_package/

# Or use the provided .pylintrc-audit file
pylint --rcfile=.pylintrc-audit your_package/
```

### What It Checks

The plugin looks for functions with names that match these patterns:
- `create_*` - Creation operations
- `update_*` - Update operations
- `delete_*` - Deletion operations
- `share_*` - Sharing operations
- And many more critical operations

It then checks if these functions contain proper audit logging calls using:
- `audit_service.log_event()`
- `self.audit_service.log_event()`
- `get_audit_service().log_event()`

### Integration with Tox

Add to your tox.ini:

```ini
[testenv:audit]
deps =
    crown-nexus-pylint
    pylint>=3.0.0
commands =
    pylint --rcfile={toxinidir}/.pylintrc-audit your_package/
```
