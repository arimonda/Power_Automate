"""
Integration Manager
Manages external service integrations
"""

from typing import Any, Dict, List, Optional


class IntegrationManager:
    """Manages external integrations"""
    
    def __init__(self, config, logger):
        """
        Initialize Integration Manager
        
        Args:
            config: Configuration object
            logger: Logger object
        """
        self.config = config
        self.logger = logger
        self.integrations = {}
        self._excel_popup_handler = None
        
    def integrate(self, service: str, **kwargs) -> Any:
        """
        Integrate with external service
        
        Args:
            service: Service name
            **kwargs: Service-specific parameters
            
        Returns:
            Integration result
        """
        self.logger.info(f"Integrating with service: {service}")
        
        handlers = {
            "email": self._integrate_email,
            "database": self._integrate_database,
            "api": self._integrate_api,
            "web": self._integrate_web,
            "file": self._integrate_file,
            "notification": self._integrate_notification,
            "excel": self._integrate_excel
        }
        
        handler = handlers.get(service.lower())
        
        if not handler:
            self.logger.warning(f"Unknown integration service: {service}")
            return None
        
        return handler(**kwargs)

    def list_integrations(self) -> List[str]:
        """Return names of all available integration services."""
        return [
            "email", "database", "api", "web",
            "file", "notification", "excel"
        ]

    def get_excel_popup_handler(self):
        """
        Get or create the ExcelPopupHandler singleton.
        Requires the framework reference to be set via set_framework().
        """
        if self._excel_popup_handler is None:
            from .excel_popup_handler import ExcelPopupHandler
            self._excel_popup_handler = ExcelPopupHandler(self._framework)
        return self._excel_popup_handler

    def set_framework(self, framework) -> None:
        """Store a back-reference to PADFramework (called during init)."""
        self._framework = framework
    
    def _integrate_email(self, **kwargs) -> Dict[str, Any]:
        """Email integration"""
        self.logger.info("Email integration initialized")
        return {
            "service": "email",
            "status": "connected",
            "smtp_server": self.config.get("email.smtp_server"),
            "capabilities": ["send", "receive", "attachments"]
        }
    
    def _integrate_database(self, **kwargs) -> Dict[str, Any]:
        """Database integration"""
        self.logger.info("Database integration initialized")
        return {
            "service": "database",
            "status": "connected",
            "type": self.config.get("database.type"),
            "capabilities": ["query", "insert", "update", "delete"]
        }
    
    def _integrate_api(self, **kwargs) -> Dict[str, Any]:
        """API integration"""
        endpoint = kwargs.get("endpoint", "")
        self.logger.info(f"API integration initialized: {endpoint}")
        return {
            "service": "api",
            "status": "ready",
            "endpoint": endpoint,
            "capabilities": ["get", "post", "put", "delete"]
        }
    
    def _integrate_web(self, **kwargs) -> Dict[str, Any]:
        """Web automation integration"""
        self.logger.info("Web automation integration initialized")
        return {
            "service": "web",
            "status": "ready",
            "browser": self.config.get("integrations.web_automation.browser"),
            "capabilities": ["navigate", "click", "input", "scrape"]
        }
    
    def _integrate_file(self, **kwargs) -> Dict[str, Any]:
        """File operations integration"""
        self.logger.info("File operations integration initialized")
        return {
            "service": "file",
            "status": "ready",
            "capabilities": ["read", "write", "copy", "move", "delete", "archive"]
        }
    
    def _integrate_notification(self, **kwargs) -> Dict[str, Any]:
        """Notification integration"""
        self.logger.info("Notification integration initialized")
        return {
            "service": "notification",
            "status": "ready",
            "capabilities": ["email", "slack", "teams", "webhook"]
        }

    def _integrate_excel(self, **kwargs) -> Any:
        """
        Excel integration — popups, workbook, worksheet, cell, data,
        formatting, macros, charts, pivot, print, import/export,
        protection, error recovery.

        Supported operations (pass as ``operation`` kwarg):

        Popup / dialog handling:
          - ``open_and_handle`` : Open file, run macro, handle popups
          - ``handle_macro``    : Single-macro single-popup shortcut
          - ``handle_auto``     : Auto-launch popup on open
          - ``build_flow``      : Build & save flow without executing

        Flow building (returns action lists — use with ExcelFlowBuilder):
          - ``workbook``   : Workbook lifecycle actions
          - ``worksheet``  : Worksheet CRUD actions
          - ``cell``       : Cell/range read/write/find actions
          - ``row_column`` : Insert/delete/autofit row/column
          - ``format``     : Formatting actions
          - ``data``       : Sort/filter/duplicates/named ranges
          - ``table``      : Table create/resize/read
          - ``pivot``      : Pivot table create/refresh
          - ``chart``      : Chart create/delete/export
          - ``print``      : Print/page setup
          - ``import_export`` : CSV/PDF import & export
          - ``protection`` : Protect/unprotect/calculation mode
          - ``macro``      : Run macro with args / capture return
          - ``recovery``   : Error recovery actions

          - ``info``       : Return full capabilities dict
        """
        operation = kwargs.pop("operation", "info")

        if operation == "info":
            self.logger.info("Excel integration ready")
            return {
                "service": "excel",
                "status": "ready",
                "capabilities": {
                    "popup": [
                        "open_and_handle", "handle_macro",
                        "handle_auto", "build_flow",
                    ],
                    "workbook": [
                        "launch", "open", "create", "save",
                        "save_as", "close", "attach_running",
                    ],
                    "worksheet": [
                        "get_active", "activate", "add", "delete",
                        "rename", "list_all", "copy",
                        "protect", "unprotect",
                    ],
                    "cell": [
                        "read", "write", "write_formula", "write_range",
                        "clear", "select", "activate_cell",
                        "get_first_free_row", "get_first_free_column",
                        "find", "find_and_replace",
                    ],
                    "row_column": [
                        "insert_row", "insert_column",
                        "delete_row", "delete_column",
                        "autofit_columns", "autofit_rows",
                        "set_column_width", "set_row_height",
                    ],
                    "format": [
                        "format_cells", "merge", "unmerge",
                        "freeze_panes", "unfreeze_panes",
                    ],
                    "data": [
                        "sort", "auto_filter", "remove_filter",
                        "remove_duplicates", "add_named_range",
                        "delete_named_range", "get_named_range",
                    ],
                    "table": ["create", "resize", "get_data"],
                    "pivot": ["create", "refresh"],
                    "chart": ["create", "delete", "export_image"],
                    "print": [
                        "print_worksheet", "set_print_area", "page_setup",
                    ],
                    "import_export": [
                        "export_pdf", "export_csv", "import_csv",
                    ],
                    "protection": [
                        "protect_workbook", "unprotect_workbook",
                        "set_calculation_mode", "recalculate",
                    ],
                    "macro": [
                        "run", "run_with_args", "run_and_capture",
                    ],
                    "recovery": [
                        "detect_hung_excel", "force_kill_excel",
                        "dismiss_unexpected_dialog",
                        "safe_close_with_retry",
                    ],
                },
                "templates": [
                    "excel_macro_popup",
                    "excel_auto_popup",
                    "excel_multi_popup",
                ],
            }

        # --- Popup operations (delegate to ExcelPopupHandler) ---
        handler = self.get_excel_popup_handler()

        popup_ops = {
            "open_and_handle": handler.open_and_handle_popup,
            "handle_macro": handler.handle_macro_popup,
            "handle_auto": handler.handle_auto_popup,
            "build_flow": handler.build_flow_only,
        }
        if operation in popup_ops:
            return popup_ops[operation](**kwargs)

        # --- Excel automation actions (return action lists) ---
        from .excel_automation import (
            ExcelWorkbookActions, ExcelWorksheetActions,
            ExcelCellActions, ExcelRowColumnActions,
            ExcelFormatActions, ExcelDataActions,
            ExcelTableActions, ExcelPivotActions,
            ExcelChartActions, ExcelPrintActions,
            ExcelImportExportActions, ExcelProtectionActions,
            ExcelMacroActions, ExcelErrorRecovery,
        )

        action_map = {
            "workbook": ExcelWorkbookActions,
            "worksheet": ExcelWorksheetActions,
            "cell": ExcelCellActions,
            "row_column": ExcelRowColumnActions,
            "format": ExcelFormatActions,
            "data": ExcelDataActions,
            "table": ExcelTableActions,
            "pivot": ExcelPivotActions,
            "chart": ExcelChartActions,
            "print": ExcelPrintActions,
            "import_export": ExcelImportExportActions,
            "protection": ExcelProtectionActions,
            "macro": ExcelMacroActions,
            "recovery": ExcelErrorRecovery,
        }

        if operation in action_map:
            method_name = kwargs.pop("method", None)
            cls = action_map[operation]
            if method_name and hasattr(cls, method_name):
                return getattr(cls, method_name)(**kwargs)
            self.logger.warning(
                f"Excel '{operation}' requires a 'method' kwarg. "
                f"Available: {[m for m in dir(cls) if not m.startswith('_')]}"
            )
            return None

        self.logger.warning(f"Unknown excel operation: {operation}")
        return None
