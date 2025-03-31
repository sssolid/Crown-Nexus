"""Verify that the plugin can be loaded."""

import sys
import importlib
import pylint

print("Python version:", sys.version)
print("Pylint version:", pylint.__version__)
print("\nChecking for plugin...")

try:
    import crown_nexus_pylint

    print("Found crown_nexus_pylint at:", crown_nexus_pylint.__file__)

    import crown_nexus_pylint.audit_checker

    print("Found audit_checker at:", crown_nexus_pylint.audit_checker.__file__)

    print("\nPlugin is properly installed!")
except ImportError as e:
    print(f"IMPORT ERROR: {e}")
    print("\nPython path:")
    for p in sys.path:
        print(f"  {p}")
