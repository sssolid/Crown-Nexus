# tools/crown_nexus_pylint/audit_checker.py
"""Pylint plugin to check for proper audit system usage."""

import astroid
from pylint.checkers import BaseChecker
from pylint.lint import PyLinter


class AuditChecker(BaseChecker):
    """Checks that audit logging is used in critical operations."""

    name = "audit-checker"
    priority = -1
    msgs = {
        "C9001": (
            "Function '%s' should include audit logging (required for %s)",
            "missing-audit-logging",
            "Add audit logging calls to important operations",
        ),
    }
    options = ()

    # Make sure you're implementing the required interfaces
    def __init__(self, linter=None):
        super().__init__(linter)

    def visit_functiondef(self, node):
        """Check if function requires audit logging."""
        self._check_for_audit(node)

    def visit_asyncfunctiondef(self, node):
        """Check if async function requires audit logging."""
        self._check_for_audit(node)

    def _check_for_audit(self, node):
        """Check if a function should have audit logging."""
        # Skip if this is a test, private method, or property
        if (node.name.startswith("test_") or
                node.name.startswith("_")):
            return

        # Check if this function matches patterns for requiring audit
        audit_patterns = {
            "create_": "creation operations",
            "update_": "update operations",
            "delete_": "deletion operations",
            "share_": "sharing operations",
            "export_": "export operations",
            "import_": "import operations",
            "upload_": "file upload operations",
            "download_": "file download operations",
            "change_": "modification operations",
            "approve_": "approval operations",
            "reject_": "rejection operations",
            "authenticate": "authentication operations",
            "deactivate_": "deactivation operations",
        }

        required_for = None
        for pattern, reason in audit_patterns.items():
            if node.name.startswith(pattern):
                required_for = reason
                break

        if required_for is None:
            return

        # Look for audit calls within the function
        if not self._has_audit_call(node):
            self.add_message("C9001", node=node, args=(node.name, "required_for"))

    def _has_audit_call(self, node):
        """Check if function has audit logging calls."""
        for child_node in node.nodes_of_class(astroid.Call):
            if hasattr(child_node, "func") and isinstance(child_node.func, astroid.Attribute):
                if child_node.func.attrname == "log_event":
                    # Check if it's calling audit_service.log_event() or similar
                    if (
                        # direct audit_service.log_event()
                        (isinstance(child_node.func.expr, astroid.Name) and
                         child_node.func.expr.name == "audit_service")
                        or
                        # self.audit_service.log_event()
                        (isinstance(child_node.func.expr, astroid.Attribute) and
                         isinstance(child_node.func.expr.expr, astroid.Name) and
                         child_node.func.expr.expr.name == "self" and
                         child_node.func.expr.attrname == "audit_service")
                        or
                        # get_audit_service().log_event()
                        (isinstance(child_node.func.expr, astroid.Call) and
                         isinstance(child_node.func.expr.func, astroid.Name) and
                         child_node.func.expr.func.name == "get_audit_service")
                    ):
                        return True
        return False


def register(linter):
    """Required method to auto-register this checker."""
    linter.register_checker(AuditChecker(linter))
