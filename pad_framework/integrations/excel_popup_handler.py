"""
Excel Popup Handler for Power Automate Desktop
================================================
Generates and manages PAD flows that open Excel/XLS files containing
VBA macros, detect macro-triggered popups, fill field values, and
submit them automatically.

Supported scenarios
-------------------
1. Open workbook -> enable macros -> handle security prompt
2. Run a VBA macro that spawns a UserForm popup -> fill fields -> submit
3. Open workbook that auto-launches a popup on Workbook_Open -> fill -> submit
4. Handle multiple sequential popups from a single macro
5. Handle standard Excel dialogs (Save As, Read-Only, etc.)

All heavy lifting is done by PAD's native actions; this module only
builds the JSON flow definitions and delegates execution to the
framework's FlowExecutor.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# PAD Action type constants — mirror Power Automate Desktop action names
# ---------------------------------------------------------------------------

class PADActions:
    """Power Automate Desktop native action identifiers."""

    # ---- Excel: Instance & workbook lifecycle ----
    EXCEL_LAUNCH = "Excel.LaunchExcel"
    EXCEL_OPEN = "Excel.OpenDocument"
    EXCEL_CLOSE = "Excel.CloseExcel"
    EXCEL_SAVE = "Excel.SaveDocument"
    EXCEL_SAVE_AS = "Excel.SaveDocumentAs"
    EXCEL_ATTACH = "Excel.AttachToRunningExcel"

    # ---- Excel: Macro ----
    EXCEL_RUN_MACRO = "Excel.RunMacro"

    # ---- Excel: Worksheet ----
    EXCEL_GET_ACTIVE_WORKSHEET = "Excel.GetActiveWorksheet"
    EXCEL_SET_ACTIVE_WORKSHEET = "Excel.SetActiveWorksheet"
    EXCEL_ADD_WORKSHEET = "Excel.AddWorksheet"
    EXCEL_DELETE_WORKSHEET = "Excel.DeleteWorksheet"
    EXCEL_RENAME_WORKSHEET = "Excel.RenameWorksheet"
    EXCEL_GET_WORKSHEETS = "Excel.GetAllWorksheets"
    EXCEL_COPY_WORKSHEET = "Excel.CopyWorksheet"

    # ---- Excel: Cell / range read & write ----
    EXCEL_READ_CELLS = "Excel.ReadFromCells"
    EXCEL_WRITE_CELLS = "Excel.WriteToCells"
    EXCEL_CLEAR_CELLS = "Excel.ClearCells"
    EXCEL_GET_FIRST_FREE_ROW = "Excel.GetFirstFreeRowOnColumn"
    EXCEL_GET_FIRST_FREE_COL = "Excel.GetFirstFreeColumn"
    EXCEL_ACTIVATE_CELL = "Excel.ActivateCellInWorksheet"
    EXCEL_GET_SELECTED_RANGE = "Excel.GetSelectedCellRange"
    EXCEL_SELECT_RANGE = "Excel.SelectCellsInWorksheet"

    # ---- Excel: Row / column manipulation ----
    EXCEL_INSERT_ROW = "Excel.InsertRow"
    EXCEL_INSERT_COLUMN = "Excel.InsertColumn"
    EXCEL_DELETE_ROW = "Excel.DeleteRow"
    EXCEL_DELETE_COLUMN = "Excel.DeleteColumn"

    # ---- Excel: Find & replace ----
    EXCEL_FIND = "Excel.FindCells"
    EXCEL_FIND_REPLACE = "Excel.FindAndReplace"

    # ---- Excel: Formatting ----
    EXCEL_SET_CELL_FORMAT = "Excel.FormatCells"
    EXCEL_SET_COLUMN_WIDTH = "Excel.SetColumnWidth"
    EXCEL_SET_ROW_HEIGHT = "Excel.SetRowHeight"
    EXCEL_AUTOFIT_COLUMNS = "Excel.AutoFitColumns"
    EXCEL_AUTOFIT_ROWS = "Excel.AutoFitRows"
    EXCEL_MERGE_CELLS = "Excel.MergeCells"
    EXCEL_UNMERGE_CELLS = "Excel.UnmergeCells"
    EXCEL_FREEZE_PANES = "Excel.FreezePanes"
    EXCEL_UNFREEZE_PANES = "Excel.UnfreezePanes"

    # ---- Excel: Sort / filter / data ----
    EXCEL_SORT = "Excel.SortCells"
    EXCEL_AUTO_FILTER = "Excel.SetAutoFilter"
    EXCEL_REMOVE_FILTER = "Excel.RemoveAutoFilter"
    EXCEL_REMOVE_DUPLICATES = "Excel.RemoveDuplicateRows"

    # ---- Excel: Named ranges ----
    EXCEL_ADD_NAMED_RANGE = "Excel.AddNamedRange"
    EXCEL_DELETE_NAMED_RANGE = "Excel.DeleteNamedRange"
    EXCEL_GET_NAMED_RANGE = "Excel.GetNamedRange"

    # ---- Excel: Table / ListObject ----
    EXCEL_CREATE_TABLE = "Excel.CreateTable"
    EXCEL_RESIZE_TABLE = "Excel.ResizeTable"
    EXCEL_GET_TABLE_DATA = "Excel.GetTableData"

    # ---- Excel: Pivot table ----
    EXCEL_CREATE_PIVOT = "Excel.CreatePivotTable"
    EXCEL_REFRESH_PIVOT = "Excel.RefreshPivotTable"

    # ---- Excel: Chart ----
    EXCEL_CREATE_CHART = "Excel.CreateChart"
    EXCEL_DELETE_CHART = "Excel.DeleteChart"
    EXCEL_EXPORT_CHART = "Excel.ExportChartAsImage"

    # ---- Excel: Print ----
    EXCEL_PRINT = "Excel.PrintWorksheet"
    EXCEL_SET_PRINT_AREA = "Excel.SetPrintArea"
    EXCEL_SET_PAGE_SETUP = "Excel.SetPageSetup"

    # ---- Excel: Import / Export ----
    EXCEL_EXPORT_PDF = "Excel.ExportToPDF"
    EXCEL_EXPORT_CSV = "Excel.ExportToCSV"
    EXCEL_IMPORT_CSV = "Excel.ImportCSV"

    # ---- Excel: Protection ----
    EXCEL_PROTECT_WORKBOOK = "Excel.ProtectWorkbook"
    EXCEL_UNPROTECT_WORKBOOK = "Excel.UnprotectWorkbook"
    EXCEL_PROTECT_WORKSHEET = "Excel.ProtectWorksheet"
    EXCEL_UNPROTECT_WORKSHEET = "Excel.UnprotectWorksheet"

    # ---- Excel: Calculation ----
    EXCEL_SET_CALCULATION = "Excel.SetCalculationMode"
    EXCEL_CALCULATE = "Excel.CalculateWorkbook"

    # ---- UI Automation actions ----
    UI_WAIT_WINDOW = "UIAutomation.WaitForWindow"
    UI_GET_WINDOW = "UIAutomation.GetWindow"
    UI_FOCUS_WINDOW = "UIAutomation.FocusWindow"
    UI_POPULATE_TEXT = "UIAutomation.PopulateTextField"
    UI_SET_DROPDOWN = "UIAutomation.SetDropdownValue"
    UI_SET_CHECKBOX = "UIAutomation.SetCheckboxState"
    UI_CLICK = "UIAutomation.Click"
    UI_CLOSE_WINDOW = "UIAutomation.CloseWindow"
    UI_GET_ELEMENT = "UIAutomation.GetElement"
    UI_GET_ELEMENT_ATTRIBUTE = "UIAutomation.GetElementAttribute"
    UI_EXTRACT_DATA = "UIAutomation.ExtractData"
    UI_SEND_KEYS = "UIAutomation.SendKeys"
    UI_PRESS_BUTTON = "UIAutomation.PressButton"
    UI_IF_WINDOW_EXISTS = "UIAutomation.IfWindowExists"

    # ---- Conditionals / control ----
    IF = "Conditionals.If"
    ELSE = "Conditionals.Else"
    ELSE_IF = "Conditionals.ElseIf"
    END_IF = "Conditionals.EndIf"
    LOOP = "Loops.Loop"
    END_LOOP = "Loops.EndLoop"
    FOR_EACH = "Loops.ForEach"
    END_FOR_EACH = "Loops.EndForEach"
    WAIT = "Flow.Wait"
    SET_VARIABLE = "Variables.SetVariable"
    INCREASE_VARIABLE = "Variables.IncreaseVariable"
    LOG_MESSAGE = "Display.LogMessage"

    # ---- Error handling ----
    ON_ERROR = "ErrorHandling.BeginExceptionBlock"
    END_ERROR = "ErrorHandling.EndExceptionBlock"

    # ---- Process management ----
    PROCESS_IF_RUNNING = "System.IfProcessIsRunning"
    PROCESS_TERMINATE = "System.TerminateProcess"
    PROCESS_GET = "System.GetRunningProcesses"


# ---------------------------------------------------------------------------
# Field descriptor — describes a single field inside a popup
# ---------------------------------------------------------------------------

class PopupField:
    """Describes one input field inside an Excel VBA popup / UserForm."""

    FIELD_TEXT = "text"
    FIELD_DROPDOWN = "dropdown"
    FIELD_CHECKBOX = "checkbox"

    def __init__(
        self,
        name: str,
        value: Any,
        field_type: str = "text",
        selector: Optional[str] = None,
        element_name: Optional[str] = None,
        tab_index: Optional[int] = None,
    ):
        """
        Parameters
        ----------
        name : str
            Human-readable label (used for logging and action IDs).
        value : Any
            The value to fill — string for text, str for dropdown, bool for checkbox.
        field_type : str
            One of ``text``, ``dropdown``, ``checkbox``.
        selector : str, optional
            CSS-like or UI-tree selector for the element inside the popup.
            When *None*, PAD will match by ``element_name``.
        element_name : str, optional
            The ``Name`` property of the UI element (visible in PAD recorder).
        tab_index : int, optional
            If set, the handler presses Tab this many times to reach the field
            instead of using a selector.
        """
        self.name = name
        self.value = value
        self.field_type = field_type
        self.selector = selector
        self.element_name = element_name or name
        self.tab_index = tab_index

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "value": self.value,
            "field_type": self.field_type,
            "selector": self.selector,
            "element_name": self.element_name,
            "tab_index": self.tab_index,
        }


# ---------------------------------------------------------------------------
# Popup descriptor — full description of one popup
# ---------------------------------------------------------------------------

class PopupDescriptor:
    """Describes an expected popup window triggered by an Excel macro."""

    def __init__(
        self,
        window_title: str,
        fields: Optional[List[PopupField]] = None,
        submit_button: str = "OK",
        submit_selector: Optional[str] = None,
        cancel_button: str = "Cancel",
        timeout: int = 30,
        window_class: Optional[str] = None,
        window_process: str = "EXCEL.EXE",
    ):
        """
        Parameters
        ----------
        window_title : str
            Title (or substring) of the popup window that PAD should wait for.
        fields : list[PopupField], optional
            Fields to fill before submitting.
        submit_button : str
            Display text of the submit/OK button.
        submit_selector : str, optional
            Explicit UI selector for the submit button.
        cancel_button : str
            Display text of the cancel button (for error-recovery flows).
        timeout : int
            Seconds to wait for the popup before timing out.
        window_class : str, optional
            Win32 window class name (e.g. ``ThunderDFrame`` for VBA UserForms).
        window_process : str
            Process that owns the popup.
        """
        self.window_title = window_title
        self.fields = fields or []
        self.submit_button = submit_button
        self.submit_selector = submit_selector
        self.cancel_button = cancel_button
        self.timeout = timeout
        self.window_class = window_class
        self.window_process = window_process

    def to_dict(self) -> Dict[str, Any]:
        return {
            "window_title": self.window_title,
            "fields": [f.to_dict() for f in self.fields],
            "submit_button": self.submit_button,
            "submit_selector": self.submit_selector,
            "cancel_button": self.cancel_button,
            "timeout": self.timeout,
            "window_class": self.window_class,
            "window_process": self.window_process,
        }


# ---------------------------------------------------------------------------
# ExcelPopupHandler — builds and executes PAD flows
# ---------------------------------------------------------------------------

class ExcelPopupHandler:
    """
    High-level handler that builds PAD flow definitions for opening Excel
    workbooks, running macros, detecting popups, filling values, and
    submitting them.

    Usage
    -----
    >>> handler = ExcelPopupHandler(pad_framework)
    >>> popup = PopupDescriptor(
    ...     window_title="Enter Credentials",
    ...     fields=[
    ...         PopupField("Username", "admin"),
    ...         PopupField("Password", "s3cret"),
    ...     ],
    ...     submit_button="Login",
    ... )
    >>> result = handler.open_and_handle_popup(
    ...     file_path=r"C:\\Reports\\secured_report.xlsm",
    ...     macro_name="ShowLoginForm",
    ...     popups=[popup],
    ... )
    """

    def __init__(self, framework):
        """
        Parameters
        ----------
        framework : PADFramework
            Initialized PADFramework instance.
        """
        self.framework = framework
        self.config = framework.config
        self.logger = framework.logger
        self.flow_manager = framework.flow_manager

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def open_and_handle_popup(
        self,
        file_path: str,
        macro_name: Optional[str] = None,
        popups: Optional[List[PopupDescriptor]] = None,
        enable_macros: bool = True,
        save_after: bool = False,
        close_after: bool = True,
        timeout: int = 300,
        retry_count: int = 1,
    ) -> Any:
        """
        Build and execute a PAD flow that opens *file_path*, optionally
        runs *macro_name*, then for each popup in *popups*: waits for the
        window, fills every field, and clicks submit.

        Parameters
        ----------
        file_path : str
            Full path to the ``.xls``, ``.xlsx``, or ``.xlsm`` file.
        macro_name : str, optional
            VBA macro to run (e.g. ``Sheet1.MyMacro``).  If *None*, the
            handler only opens the workbook and waits for any auto-launch
            popup (``Workbook_Open``).
        popups : list[PopupDescriptor]
            Popups expected after macro execution, in order.
        enable_macros : bool
            If *True*, adds actions to dismiss the macro security bar.
        save_after : bool
            Save the workbook after all popups are handled.
        close_after : bool
            Close Excel after completion.
        timeout : int
            Overall flow timeout in seconds.
        retry_count : int
            Number of retries on failure.

        Returns
        -------
        FlowExecutionResult
        """
        popups = popups or []
        flow_name = self._generate_flow_name(file_path)

        flow_def = self._build_flow(
            flow_name=flow_name,
            file_path=file_path,
            macro_name=macro_name,
            popups=popups,
            enable_macros=enable_macros,
            save_after=save_after,
            close_after=close_after,
            timeout=timeout,
        )

        self._save_flow(flow_name, flow_def)
        self.logger.info(
            f"Executing Excel popup flow: {flow_name} "
            f"(file={file_path}, macro={macro_name}, popups={len(popups)})"
        )

        result = self.framework.execute_flow(
            flow_name=flow_name,
            input_variables={
                "file_path": file_path,
                "macro_name": macro_name or "",
            },
            timeout=timeout,
            retry_count=retry_count,
        )

        return result

    def handle_macro_popup(
        self,
        file_path: str,
        macro_name: str,
        popup: PopupDescriptor,
        **kwargs,
    ) -> Any:
        """Convenience shortcut for a single-macro, single-popup scenario."""
        return self.open_and_handle_popup(
            file_path=file_path,
            macro_name=macro_name,
            popups=[popup],
            **kwargs,
        )

    def handle_auto_popup(
        self,
        file_path: str,
        popup: PopupDescriptor,
        **kwargs,
    ) -> Any:
        """Convenience shortcut for files that auto-launch a popup on open."""
        return self.open_and_handle_popup(
            file_path=file_path,
            macro_name=None,
            popups=[popup],
            **kwargs,
        )

    def build_flow_only(
        self,
        file_path: str,
        macro_name: Optional[str] = None,
        popups: Optional[List[PopupDescriptor]] = None,
        enable_macros: bool = True,
        save_after: bool = False,
        close_after: bool = True,
        timeout: int = 300,
    ) -> Dict[str, Any]:
        """
        Build and save the flow definition without executing it.
        Returns the flow JSON dict so it can be inspected or edited.
        """
        popups = popups or []
        flow_name = self._generate_flow_name(file_path)

        flow_def = self._build_flow(
            flow_name=flow_name,
            file_path=file_path,
            macro_name=macro_name,
            popups=popups,
            enable_macros=enable_macros,
            save_after=save_after,
            close_after=close_after,
            timeout=timeout,
        )

        self._save_flow(flow_name, flow_def)
        self.logger.info(f"Flow saved (not executed): {flow_name}")
        return flow_def

    # ------------------------------------------------------------------
    # Flow builder — assembles the PAD action list
    # ------------------------------------------------------------------

    def _build_flow(
        self,
        flow_name: str,
        file_path: str,
        macro_name: Optional[str],
        popups: List[PopupDescriptor],
        enable_macros: bool,
        save_after: bool,
        close_after: bool,
        timeout: int,
    ) -> Dict[str, Any]:
        """Assemble a complete PAD flow definition."""

        actions: List[Dict[str, Any]] = []
        step = 0

        def _next_id(label: str = "") -> str:
            nonlocal step
            step += 1
            tag = f"_{label}" if label else ""
            return f"step_{step}{tag}"

        # --- 1. Launch Excel -----------------------------------------
        actions.append({
            "id": _next_id("launch_excel"),
            "type": PADActions.EXCEL_LAUNCH,
            "parameters": {
                "instance_name": "%ExcelInstance%",
                "visible": True,
                "display_alerts": False,
            },
        })

        # --- 2. Open the workbook ------------------------------------
        actions.append({
            "id": _next_id("open_workbook"),
            "type": PADActions.EXCEL_OPEN,
            "parameters": {
                "instance": "%ExcelInstance%",
                "file_path": file_path,
                "open_as_readonly": False,
            },
        })

        # --- 3. Handle macro security bar ----------------------------
        if enable_macros:
            actions.extend(self._build_enable_macros_actions(_next_id))

        # Brief pause for workbook to fully initialize
        actions.append({
            "id": _next_id("wait_init"),
            "type": PADActions.WAIT,
            "parameters": {"duration": 2},
        })

        # --- 4. Run VBA macro (if specified) -------------------------
        if macro_name:
            actions.append({
                "id": _next_id("run_macro"),
                "type": PADActions.EXCEL_RUN_MACRO,
                "parameters": {
                    "instance": "%ExcelInstance%",
                    "macro_name": macro_name,
                },
            })
            actions.append({
                "id": _next_id("wait_macro"),
                "type": PADActions.WAIT,
                "parameters": {"duration": 1},
            })

        # --- 5. Handle each popup in sequence ------------------------
        for idx, popup in enumerate(popups):
            popup_actions = self._build_popup_actions(popup, idx, _next_id)
            actions.extend(popup_actions)

        # --- 6. Save workbook (optional) -----------------------------
        if save_after:
            actions.append({
                "id": _next_id("save_workbook"),
                "type": PADActions.EXCEL_SAVE,
                "parameters": {"instance": "%ExcelInstance%"},
            })

        # --- 7. Close Excel (optional) -------------------------------
        if close_after:
            actions.append({
                "id": _next_id("close_excel"),
                "type": PADActions.EXCEL_CLOSE,
                "parameters": {
                    "instance": "%ExcelInstance%",
                    "save_before_close": save_after,
                },
            })

        # --- 8. Final status -----------------------------------------
        actions.append({
            "id": _next_id("set_status"),
            "type": PADActions.SET_VARIABLE,
            "parameters": {
                "variable": "status",
                "value": "success",
            },
        })

        # --- Assemble full flow definition ---------------------------
        flow_def = {
            "name": flow_name,
            "description": (
                f"Auto-generated: open '{Path(file_path).name}'"
                + (f", run macro '{macro_name}'" if macro_name else "")
                + f", handle {len(popups)} popup(s)"
            ),
            "version": "1.0",
            "enabled": True,
            "variables": {
                "input": {
                    "file_path": {
                        "type": "string",
                        "default": file_path,
                        "description": "Path to the Excel file",
                    },
                    "macro_name": {
                        "type": "string",
                        "default": macro_name or "",
                        "description": "VBA macro to execute",
                    },
                },
                "output": {
                    "status": {
                        "type": "string",
                        "description": "success or failed",
                    },
                    "popups_handled": {
                        "type": "number",
                        "description": "Count of popups handled",
                    },
                },
            },
            "actions": actions,
            "error_handling": {
                "on_error": "stop",
                "retry_count": 1,
                "retry_delay": 3,
                "cleanup_actions": [
                    {
                        "id": "cleanup_close_excel",
                        "type": PADActions.EXCEL_CLOSE,
                        "parameters": {
                            "instance": "%ExcelInstance%",
                            "save_before_close": False,
                        },
                    }
                ],
            },
            "settings": {
                "timeout": timeout,
                "priority": 5,
                "run_mode": "attended",
            },
            "metadata": {
                "created_by": "ExcelPopupHandler",
                "created_at": datetime.now().isoformat(),
                "source_file": file_path,
                "macro_name": macro_name,
                "popup_count": len(popups),
                "tags": ["excel", "popup", "macro", "auto-generated"],
            },
        }

        return flow_def

    # ------------------------------------------------------------------
    # Action builders for specific concerns
    # ------------------------------------------------------------------

    def _build_enable_macros_actions(self, next_id) -> List[Dict[str, Any]]:
        """
        Actions to dismiss the Excel macro security bar.

        When a macro-enabled workbook opens, Excel shows a yellow
        "Security Warning — Macros have been disabled" bar with an
        "Enable Content" button.  These actions detect that bar and
        click the button.
        """
        return [
            {
                "id": next_id("wait_security_bar"),
                "type": PADActions.UI_WAIT_WINDOW,
                "parameters": {
                    "window_title": "Microsoft Excel",
                    "process_name": "EXCEL.EXE",
                    "timeout": 10,
                    "on_timeout": "continue",
                },
            },
            {
                "id": next_id("check_security_bar"),
                "type": PADActions.UI_GET_ELEMENT,
                "parameters": {
                    "window": "%ExcelWindow%",
                    "element_name": "Enable Content",
                    "element_type": "Button",
                    "on_not_found": "continue",
                    "output_variable": "%EnableContentBtn%",
                },
            },
            {
                "id": next_id("if_security_bar"),
                "type": PADActions.IF,
                "parameters": {
                    "condition": "%EnableContentBtn% IS NOT EMPTY",
                },
            },
            {
                "id": next_id("click_enable_content"),
                "type": PADActions.UI_CLICK,
                "parameters": {
                    "element": "%EnableContentBtn%",
                    "click_type": "left_click",
                },
            },
            {
                "id": next_id("log_macros_enabled"),
                "type": PADActions.LOG_MESSAGE,
                "parameters": {
                    "message": "Macro security bar dismissed — content enabled",
                },
            },
            {
                "id": next_id("end_if_security"),
                "type": PADActions.END_IF,
                "parameters": {},
            },
            {
                "id": next_id("wait_after_enable"),
                "type": PADActions.WAIT,
                "parameters": {"duration": 1},
            },
        ]

    def _build_popup_actions(
        self,
        popup: PopupDescriptor,
        popup_index: int,
        next_id,
    ) -> List[Dict[str, Any]]:
        """
        Build actions that wait for a popup, fill every field, and submit.
        """
        prefix = f"popup{popup_index}"
        actions: List[Dict[str, Any]] = []

        # 5a. Wait for the popup window to appear
        wait_params = {
            "window_title": popup.window_title,
            "process_name": popup.window_process,
            "timeout": popup.timeout,
            "output_variable": f"%PopupWindow_{popup_index}%",
        }
        if popup.window_class:
            wait_params["window_class"] = popup.window_class

        actions.append({
            "id": next_id(f"{prefix}_wait"),
            "type": PADActions.UI_WAIT_WINDOW,
            "parameters": wait_params,
        })

        # 5b. Focus the popup window
        actions.append({
            "id": next_id(f"{prefix}_focus"),
            "type": PADActions.UI_FOCUS_WINDOW,
            "parameters": {
                "window": f"%PopupWindow_{popup_index}%",
            },
        })

        actions.append({
            "id": next_id(f"{prefix}_pause"),
            "type": PADActions.WAIT,
            "parameters": {"duration": 0.5},
        })

        # 5c. Fill each field
        for field_idx, field in enumerate(popup.fields):
            field_actions = self._build_field_actions(
                field, popup_index, field_idx, next_id
            )
            actions.extend(field_actions)

        # Small pause before clicking submit
        actions.append({
            "id": next_id(f"{prefix}_pre_submit"),
            "type": PADActions.WAIT,
            "parameters": {"duration": 0.5},
        })

        # 5d. Click the submit / OK button
        submit_params: Dict[str, Any] = {
            "window": f"%PopupWindow_{popup_index}%",
            "click_type": "left_click",
        }
        if popup.submit_selector:
            submit_params["element_selector"] = popup.submit_selector
        else:
            submit_params["element_name"] = popup.submit_button
            submit_params["element_type"] = "Button"

        actions.append({
            "id": next_id(f"{prefix}_submit"),
            "type": PADActions.UI_CLICK,
            "parameters": submit_params,
        })

        # Log
        actions.append({
            "id": next_id(f"{prefix}_log"),
            "type": PADActions.LOG_MESSAGE,
            "parameters": {
                "message": (
                    f"Popup '{popup.window_title}' handled — "
                    f"{len(popup.fields)} field(s) filled, "
                    f"clicked '{popup.submit_button}'"
                ),
            },
        })

        # Wait for popup to close
        actions.append({
            "id": next_id(f"{prefix}_wait_close"),
            "type": PADActions.WAIT,
            "parameters": {"duration": 1},
        })

        return actions

    def _build_field_actions(
        self,
        field: PopupField,
        popup_index: int,
        field_index: int,
        next_id,
    ) -> List[Dict[str, Any]]:
        """Build fill actions for a single field inside a popup."""

        tag = f"popup{popup_index}_field{field_index}"
        actions: List[Dict[str, Any]] = []

        # Resolve how to target the element
        target = {}
        if field.selector:
            target["element_selector"] = field.selector
        else:
            target["element_name"] = field.element_name

        target["window"] = f"%PopupWindow_{popup_index}%"

        if field.field_type == PopupField.FIELD_TEXT:
            actions.append({
                "id": next_id(f"{tag}_fill"),
                "type": PADActions.UI_POPULATE_TEXT,
                "parameters": {
                    **target,
                    "text": str(field.value),
                    "clear_before": True,
                    "send_keys_mode": "hardware",
                },
            })

        elif field.field_type == PopupField.FIELD_DROPDOWN:
            actions.append({
                "id": next_id(f"{tag}_select"),
                "type": PADActions.UI_SET_DROPDOWN,
                "parameters": {
                    **target,
                    "value": str(field.value),
                },
            })

        elif field.field_type == PopupField.FIELD_CHECKBOX:
            desired = "checked" if field.value else "unchecked"
            actions.append({
                "id": next_id(f"{tag}_check"),
                "type": PADActions.UI_SET_CHECKBOX,
                "parameters": {
                    **target,
                    "state": desired,
                },
            })

        return actions

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _generate_flow_name(self, file_path: str) -> str:
        """Generate a unique flow name based on the file and timestamp."""
        stem = Path(file_path).stem
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = "".join(c if c.isalnum() or c == "_" else "_" for c in stem)
        return f"ExcelPopup_{safe_name}_{ts}"

    def _save_flow(self, flow_name: str, flow_def: Dict[str, Any]) -> None:
        """Persist the flow definition to the flows directory."""
        flows_path = self.config.get_path("flows")
        flows_path.mkdir(parents=True, exist_ok=True)

        target = flows_path / f"{flow_name}.json"
        with open(target, "w", encoding="utf-8") as fh:
            json.dump(flow_def, fh, indent=2, default=str)

        self.logger.info(f"Flow definition saved: {target}")


# ---------------------------------------------------------------------------
# Pre-built popup templates for common scenarios
# ---------------------------------------------------------------------------

class ExcelPopupTemplates:
    """
    Ready-made PopupDescriptor objects for common Excel / VBA popup
    patterns.  Use these directly or as starting points.
    """

    @staticmethod
    def login_form(
        username: str,
        password: str,
        window_title: str = "Login",
        submit_button: str = "Login",
    ) -> PopupDescriptor:
        """Standard username / password login UserForm."""
        return PopupDescriptor(
            window_title=window_title,
            fields=[
                PopupField("Username", username, element_name="txtUsername"),
                PopupField("Password", password, element_name="txtPassword"),
            ],
            submit_button=submit_button,
        )

    @staticmethod
    def single_input(
        value: str,
        window_title: str = "Input",
        field_name: str = "Value",
        submit_button: str = "OK",
    ) -> PopupDescriptor:
        """Simple single-input dialog (e.g. VBA InputBox style)."""
        return PopupDescriptor(
            window_title=window_title,
            fields=[
                PopupField(field_name, value, element_name="txtInput"),
            ],
            submit_button=submit_button,
        )

    @staticmethod
    def confirmation_dialog(
        window_title: str = "Confirm",
        submit_button: str = "Yes",
    ) -> PopupDescriptor:
        """Popup with no fields — just click a confirmation button."""
        return PopupDescriptor(
            window_title=window_title,
            fields=[],
            submit_button=submit_button,
        )

    @staticmethod
    def data_entry_form(
        fields: Dict[str, Any],
        window_title: str = "Data Entry",
        submit_button: str = "Submit",
    ) -> PopupDescriptor:
        """
        Multi-field data entry form.

        Parameters
        ----------
        fields : dict
            Mapping of element_name -> value.  All fields are treated
            as text inputs.
        """
        popup_fields = [
            PopupField(name=k, value=v, element_name=k)
            for k, v in fields.items()
        ]
        return PopupDescriptor(
            window_title=window_title,
            fields=popup_fields,
            submit_button=submit_button,
        )

    @staticmethod
    def dropdown_selection(
        dropdown_name: str,
        selected_value: str,
        window_title: str = "Select Option",
        submit_button: str = "OK",
    ) -> PopupDescriptor:
        """Popup with a single dropdown selection."""
        return PopupDescriptor(
            window_title=window_title,
            fields=[
                PopupField(
                    dropdown_name,
                    selected_value,
                    field_type=PopupField.FIELD_DROPDOWN,
                    element_name=dropdown_name,
                ),
            ],
            submit_button=submit_button,
        )

    @staticmethod
    def macro_security_prompt(
        submit_button: str = "Enable Macros",
    ) -> PopupDescriptor:
        """Standard Excel macro security warning dialog."""
        return PopupDescriptor(
            window_title="Microsoft Excel Security Notice",
            fields=[],
            submit_button=submit_button,
            window_process="EXCEL.EXE",
            timeout=15,
        )

    @staticmethod
    def save_as_dialog(
        file_path: str,
        window_title: str = "Save As",
        submit_button: str = "Save",
    ) -> PopupDescriptor:
        """Handle a Save As dialog — type path and click Save."""
        return PopupDescriptor(
            window_title=window_title,
            fields=[
                PopupField(
                    "File name",
                    file_path,
                    element_name="FileNameControlHost",
                ),
            ],
            submit_button=submit_button,
            window_process="EXCEL.EXE",
        )

    @staticmethod
    def read_only_prompt(
        submit_button: str = "No",
    ) -> PopupDescriptor:
        """
        Handle the 'Open as Read-Only?' prompt.
        Click 'No' to open with write access.
        """
        return PopupDescriptor(
            window_title="Microsoft Excel",
            fields=[],
            submit_button=submit_button,
            window_process="EXCEL.EXE",
            timeout=10,
        )

    # ------------------------------------------------------------------
    # VBA InputBox
    # ------------------------------------------------------------------

    @staticmethod
    def vba_inputbox(
        value: str,
        window_title: str = "Microsoft Excel",
        submit_button: str = "OK",
    ) -> PopupDescriptor:
        """
        Handle a VBA ``InputBox`` / ``Application.InputBox`` prompt.
        These have a single text field and OK / Cancel buttons.
        """
        return PopupDescriptor(
            window_title=window_title,
            fields=[
                PopupField("Input", value, element_name="Edit1"),
            ],
            submit_button=submit_button,
            window_process="EXCEL.EXE",
            timeout=20,
        )

    # ------------------------------------------------------------------
    # VBA MsgBox variants
    # ------------------------------------------------------------------

    @staticmethod
    def msgbox_ok(
        window_title: str = "Microsoft Excel",
    ) -> PopupDescriptor:
        """Dismiss a VBA ``MsgBox`` with only an OK button."""
        return PopupDescriptor(
            window_title=window_title,
            fields=[],
            submit_button="OK",
            window_process="EXCEL.EXE",
            timeout=15,
        )

    @staticmethod
    def msgbox_yes_no(
        click_yes: bool = True,
        window_title: str = "Microsoft Excel",
    ) -> PopupDescriptor:
        """Handle a VBA ``MsgBox vbYesNo``."""
        return PopupDescriptor(
            window_title=window_title,
            fields=[],
            submit_button="Yes" if click_yes else "No",
            window_process="EXCEL.EXE",
            timeout=15,
        )

    @staticmethod
    def msgbox_yes_no_cancel(
        button: str = "Yes",
        window_title: str = "Microsoft Excel",
    ) -> PopupDescriptor:
        """Handle a VBA ``MsgBox vbYesNoCancel``."""
        return PopupDescriptor(
            window_title=window_title,
            fields=[],
            submit_button=button,
            window_process="EXCEL.EXE",
            timeout=15,
        )

    @staticmethod
    def msgbox_retry_cancel(
        click_retry: bool = True,
        window_title: str = "Microsoft Excel",
    ) -> PopupDescriptor:
        """Handle a VBA ``MsgBox vbRetryCancel``."""
        return PopupDescriptor(
            window_title=window_title,
            fields=[],
            submit_button="Retry" if click_retry else "Cancel",
            window_process="EXCEL.EXE",
            timeout=15,
        )

    @staticmethod
    def msgbox_abort_retry_ignore(
        button: str = "Retry",
        window_title: str = "Microsoft Excel",
    ) -> PopupDescriptor:
        """Handle a VBA ``MsgBox vbAbortRetryIgnore``."""
        return PopupDescriptor(
            window_title=window_title,
            fields=[],
            submit_button=button,
            window_process="EXCEL.EXE",
            timeout=15,
        )

    # ------------------------------------------------------------------
    # File dialogs
    # ------------------------------------------------------------------

    @staticmethod
    def file_open_dialog(
        file_path: str,
        window_title: str = "Open",
        submit_button: str = "Open",
    ) -> PopupDescriptor:
        """Handle a File Open dialog — type path and click Open."""
        return PopupDescriptor(
            window_title=window_title,
            fields=[
                PopupField(
                    "File name", file_path,
                    element_name="FileNameControlHost",
                ),
            ],
            submit_button=submit_button,
            window_process="EXCEL.EXE",
        )

    @staticmethod
    def folder_browse_dialog(
        folder_path: str,
        window_title: str = "Browse For Folder",
        submit_button: str = "OK",
    ) -> PopupDescriptor:
        """Handle a folder-picker dialog."""
        return PopupDescriptor(
            window_title=window_title,
            fields=[
                PopupField(
                    "Folder", folder_path,
                    element_name="FolderPath",
                ),
            ],
            submit_button=submit_button,
            window_process="EXCEL.EXE",
        )

    # ------------------------------------------------------------------
    # Password prompts
    # ------------------------------------------------------------------

    @staticmethod
    def password_prompt(
        password: str,
        window_title: str = "Password",
        submit_button: str = "OK",
    ) -> PopupDescriptor:
        """Handle an Excel password-protected file prompt."""
        return PopupDescriptor(
            window_title=window_title,
            fields=[
                PopupField("Password", password, element_name="Edit1"),
            ],
            submit_button=submit_button,
            window_process="EXCEL.EXE",
            timeout=15,
        )

    @staticmethod
    def write_password_prompt(
        password: str,
        window_title: str = "Password",
        submit_button: str = "OK",
    ) -> PopupDescriptor:
        """Handle an Excel write-reservation password prompt."""
        return PopupDescriptor(
            window_title=window_title,
            fields=[
                PopupField("Password", password, element_name="Edit2"),
            ],
            submit_button=submit_button,
            window_process="EXCEL.EXE",
            timeout=15,
        )

    # ------------------------------------------------------------------
    # Protected View
    # ------------------------------------------------------------------

    @staticmethod
    def protected_view_bar(
        submit_button: str = "Enable Editing",
    ) -> PopupDescriptor:
        """
        Handle the Protected View bar that appears when opening files
        from the internet or untrusted locations.
        """
        return PopupDescriptor(
            window_title="Microsoft Excel",
            fields=[],
            submit_button=submit_button,
            window_process="EXCEL.EXE",
            timeout=15,
        )

    # ------------------------------------------------------------------
    # Compatibility mode / format prompts
    # ------------------------------------------------------------------

    @staticmethod
    def compatibility_mode_prompt(
        submit_button: str = "Yes",
    ) -> PopupDescriptor:
        """
        Handle the prompt when saving a .xlsx file as .xls (or vice
        versa) asking about compatibility mode.
        """
        return PopupDescriptor(
            window_title="Microsoft Excel - Compatibility Checker",
            fields=[],
            submit_button=submit_button,
            window_process="EXCEL.EXE",
            timeout=15,
        )

    @staticmethod
    def format_change_prompt(
        submit_button: str = "Yes",
    ) -> PopupDescriptor:
        """
        Handle the 'Do you want to keep the workbook in this format?'
        prompt that appears when saving to a different file type.
        """
        return PopupDescriptor(
            window_title="Microsoft Excel",
            fields=[],
            submit_button=submit_button,
            window_process="EXCEL.EXE",
            timeout=15,
        )

    # ------------------------------------------------------------------
    # Print dialog
    # ------------------------------------------------------------------

    @staticmethod
    def print_dialog(
        submit_button: str = "Print",
    ) -> PopupDescriptor:
        """Handle the print dialog (click Print or Cancel)."""
        return PopupDescriptor(
            window_title="Print",
            fields=[],
            submit_button=submit_button,
            window_process="EXCEL.EXE",
            timeout=20,
        )

    # ------------------------------------------------------------------
    # Dynamic / unknown popup catcher
    # ------------------------------------------------------------------

    @staticmethod
    def any_excel_dialog(
        submit_button: str = "OK",
        timeout: int = 10,
    ) -> PopupDescriptor:
        """
        Catch-all for any unexpected Excel dialog.  Uses a broad
        window title match on 'Microsoft Excel' and clicks the
        specified button.
        """
        return PopupDescriptor(
            window_title="Microsoft Excel",
            fields=[],
            submit_button=submit_button,
            window_process="EXCEL.EXE",
            timeout=timeout,
        )

    # ------------------------------------------------------------------
    # Multi-page UserForm
    # ------------------------------------------------------------------

    @staticmethod
    def multi_page_form(
        pages: List[Dict[str, Any]],
        window_title: str = "Data Entry",
        final_submit: str = "Submit",
    ) -> List[PopupDescriptor]:
        """
        Build descriptors for a multi-page VBA UserForm.

        Each entry in *pages* is a dict::

            {
                "fields": [PopupField(...)],
                "next_button": "Next"       # button to advance
            }

        The last page uses *final_submit* instead.

        Returns a list of PopupDescriptor objects (one per page).
        """
        descriptors: List[PopupDescriptor] = []
        for idx, page in enumerate(pages):
            is_last = idx == len(pages) - 1
            button = final_submit if is_last else page.get("next_button", "Next")
            descriptors.append(
                PopupDescriptor(
                    window_title=window_title,
                    fields=page.get("fields", []),
                    submit_button=button,
                    window_process="EXCEL.EXE",
                )
            )
        return descriptors
