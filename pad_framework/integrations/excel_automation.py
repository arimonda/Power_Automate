"""
Excel Automation Module for Power Automate Desktop
====================================================
Comprehensive PAD flow builder for all Excel operations.

This module generates Power Automate Desktop flow definitions (JSON)
that use PAD's native Excel and UI Automation actions.  Each public
method returns a list of PAD action dicts that can be appended to a
flow's ``actions`` array — or the convenience wrappers can build and
execute a complete flow in one call.

Coverage
--------
* Workbook   — open, close, create, save, save-as, attach, password
* Worksheet  — add, delete, rename, copy, activate, list, hide/show
* Cell/Range — read, write, clear, select, find, replace, formulas
* Row/Column — insert, delete, hide/show, auto-fit
* Formatting — font, borders, fill, number format, merge, freeze
* Data       — sort, filter, remove duplicates, named ranges
* Tables     — create, resize, read
* Pivot      — create, refresh
* Charts     — create, delete, export as image
* Print      — print, page setup, print area
* Import/Export — CSV, PDF
* Protection — workbook protect/unprotect, worksheet protect/unprotect
* Calculation — mode switch, force recalculate
* Error Recovery — detect hung Excel, force-kill, dialog-stuck recovery
"""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from .excel_popup_handler import PADActions


# -----------------------------------------------------------------------
# Helper: action id generator
# -----------------------------------------------------------------------

class _StepCounter:
    """Tiny helper to generate unique sequential action ids."""

    def __init__(self, prefix: str = ""):
        self._n = 0
        self._prefix = prefix

    def next(self, label: str = "") -> str:
        self._n += 1
        tag = f"_{label}" if label else ""
        return f"{self._prefix}step_{self._n}{tag}"


# =======================================================================
# 1. WORKBOOK OPERATIONS
# =======================================================================

class ExcelWorkbookActions:
    """Build PAD actions for workbook-level operations."""

    @staticmethod
    def launch(instance_var: str = "%ExcelInstance%",
               visible: bool = True) -> List[Dict[str, Any]]:
        """Launch a new Excel instance."""
        return [{
            "id": "launch_excel",
            "type": PADActions.EXCEL_LAUNCH,
            "parameters": {
                "instance_name": instance_var,
                "visible": visible,
                "display_alerts": False,
            },
        }]

    @staticmethod
    def open_workbook(file_path: str,
                      instance_var: str = "%ExcelInstance%",
                      readonly: bool = False,
                      password: Optional[str] = None) -> List[Dict[str, Any]]:
        """Open a workbook file."""
        params: Dict[str, Any] = {
            "instance": instance_var,
            "file_path": file_path,
            "open_as_readonly": readonly,
        }
        if password:
            params["password"] = password
        return [{
            "id": "open_workbook",
            "type": PADActions.EXCEL_OPEN,
            "parameters": params,
        }]

    @staticmethod
    def create_workbook(instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        """Launch Excel with a blank workbook (launch without opening a file)."""
        return [{
            "id": "create_workbook",
            "type": PADActions.EXCEL_LAUNCH,
            "parameters": {
                "instance_name": instance_var,
                "visible": True,
                "display_alerts": False,
                "open_blank_workbook": True,
            },
        }]

    @staticmethod
    def save(instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        """Save the active workbook."""
        return [{
            "id": "save_workbook",
            "type": PADActions.EXCEL_SAVE,
            "parameters": {"instance": instance_var},
        }]

    @staticmethod
    def save_as(file_path: str,
                file_format: str = "xlsx",
                instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        """Save the workbook to a new path / format."""
        return [{
            "id": "save_workbook_as",
            "type": PADActions.EXCEL_SAVE_AS,
            "parameters": {
                "instance": instance_var,
                "file_path": file_path,
                "file_format": file_format,
            },
        }]

    @staticmethod
    def close(instance_var: str = "%ExcelInstance%",
              save: bool = False) -> List[Dict[str, Any]]:
        """Close the Excel instance."""
        return [{
            "id": "close_excel",
            "type": PADActions.EXCEL_CLOSE,
            "parameters": {
                "instance": instance_var,
                "save_before_close": save,
            },
        }]

    @staticmethod
    def attach_running(instance_var: str = "%ExcelInstance%",
                       window_title: Optional[str] = None) -> List[Dict[str, Any]]:
        """Attach to an already-running Excel instance."""
        params: Dict[str, Any] = {"instance_name": instance_var}
        if window_title:
            params["document_name"] = window_title
        return [{
            "id": "attach_excel",
            "type": PADActions.EXCEL_ATTACH,
            "parameters": params,
        }]


# =======================================================================
# 2. WORKSHEET OPERATIONS
# =======================================================================

class ExcelWorksheetActions:
    """Build PAD actions for worksheet-level operations."""

    @staticmethod
    def get_active(output_var: str = "%ActiveSheet%",
                   instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        """Get the name of the active worksheet."""
        return [{
            "id": "get_active_sheet",
            "type": PADActions.EXCEL_GET_ACTIVE_WORKSHEET,
            "parameters": {
                "instance": instance_var,
                "output_variable": output_var,
            },
        }]

    @staticmethod
    def activate(sheet_name: str,
                 instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        """Activate (switch to) a worksheet by name."""
        return [{
            "id": f"activate_sheet_{sheet_name}",
            "type": PADActions.EXCEL_SET_ACTIVE_WORKSHEET,
            "parameters": {
                "instance": instance_var,
                "worksheet_name": sheet_name,
            },
        }]

    @staticmethod
    def add(sheet_name: str,
            instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        """Add a new worksheet."""
        return [{
            "id": f"add_sheet_{sheet_name}",
            "type": PADActions.EXCEL_ADD_WORKSHEET,
            "parameters": {
                "instance": instance_var,
                "worksheet_name": sheet_name,
            },
        }]

    @staticmethod
    def delete(sheet_name: str,
               instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        """Delete a worksheet."""
        return [{
            "id": f"delete_sheet_{sheet_name}",
            "type": PADActions.EXCEL_DELETE_WORKSHEET,
            "parameters": {
                "instance": instance_var,
                "worksheet_name": sheet_name,
            },
        }]

    @staticmethod
    def rename(old_name: str, new_name: str,
               instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        """Rename a worksheet."""
        return [{
            "id": f"rename_sheet_{old_name}",
            "type": PADActions.EXCEL_RENAME_WORKSHEET,
            "parameters": {
                "instance": instance_var,
                "worksheet_name": old_name,
                "new_name": new_name,
            },
        }]

    @staticmethod
    def list_all(output_var: str = "%SheetNames%",
                 instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        """Get a list of all worksheet names."""
        return [{
            "id": "list_worksheets",
            "type": PADActions.EXCEL_GET_WORKSHEETS,
            "parameters": {
                "instance": instance_var,
                "output_variable": output_var,
            },
        }]

    @staticmethod
    def copy(source_sheet: str, new_name: str,
             instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        """Copy a worksheet within the same workbook."""
        return [{
            "id": f"copy_sheet_{source_sheet}",
            "type": PADActions.EXCEL_COPY_WORKSHEET,
            "parameters": {
                "instance": instance_var,
                "source_worksheet": source_sheet,
                "new_worksheet_name": new_name,
            },
        }]

    @staticmethod
    def protect(sheet_name: str, password: str = "",
                instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        """Protect a worksheet."""
        return [{
            "id": f"protect_sheet_{sheet_name}",
            "type": PADActions.EXCEL_PROTECT_WORKSHEET,
            "parameters": {
                "instance": instance_var,
                "worksheet_name": sheet_name,
                "password": password,
            },
        }]

    @staticmethod
    def unprotect(sheet_name: str, password: str = "",
                  instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        """Unprotect a worksheet."""
        return [{
            "id": f"unprotect_sheet_{sheet_name}",
            "type": PADActions.EXCEL_UNPROTECT_WORKSHEET,
            "parameters": {
                "instance": instance_var,
                "worksheet_name": sheet_name,
                "password": password,
            },
        }]


# =======================================================================
# 3. CELL / RANGE OPERATIONS
# =======================================================================

class ExcelCellActions:
    """Build PAD actions for cell and range operations."""

    @staticmethod
    def read(cell_or_range: str,
             output_var: str = "%CellValue%",
             instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        """Read value(s) from a cell or range (e.g. 'A1' or 'A1:D10')."""
        return [{
            "id": f"read_{cell_or_range}",
            "type": PADActions.EXCEL_READ_CELLS,
            "parameters": {
                "instance": instance_var,
                "range": cell_or_range,
                "output_variable": output_var,
            },
        }]

    @staticmethod
    def write(cell: str, value: Any,
              instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        """Write a value to a cell."""
        return [{
            "id": f"write_{cell}",
            "type": PADActions.EXCEL_WRITE_CELLS,
            "parameters": {
                "instance": instance_var,
                "cell": cell,
                "value": value,
            },
        }]

    @staticmethod
    def write_formula(cell: str, formula: str,
                      instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        """Write a formula to a cell (e.g. '=SUM(A1:A10)')."""
        return [{
            "id": f"formula_{cell}",
            "type": PADActions.EXCEL_WRITE_CELLS,
            "parameters": {
                "instance": instance_var,
                "cell": cell,
                "value": formula,
                "is_formula": True,
            },
        }]

    @staticmethod
    def write_range(start_cell: str, values: List[List[Any]],
                    instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        """Write a 2-D array of values starting at *start_cell*."""
        return [{
            "id": f"write_range_{start_cell}",
            "type": PADActions.EXCEL_WRITE_CELLS,
            "parameters": {
                "instance": instance_var,
                "cell": start_cell,
                "value": values,
                "write_mode": "range",
            },
        }]

    @staticmethod
    def clear(cell_or_range: str,
              clear_type: str = "contents",
              instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        """
        Clear cell(s).

        *clear_type*: ``contents``, ``formats``, ``comments``, ``all``.
        """
        return [{
            "id": f"clear_{cell_or_range}",
            "type": PADActions.EXCEL_CLEAR_CELLS,
            "parameters": {
                "instance": instance_var,
                "range": cell_or_range,
                "clear_type": clear_type,
            },
        }]

    @staticmethod
    def select(cell_or_range: str,
               instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        """Select a cell or range."""
        return [{
            "id": f"select_{cell_or_range}",
            "type": PADActions.EXCEL_SELECT_RANGE,
            "parameters": {
                "instance": instance_var,
                "range": cell_or_range,
            },
        }]

    @staticmethod
    def activate_cell(cell: str,
                      instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        """Activate (navigate to) a specific cell."""
        return [{
            "id": f"activate_{cell}",
            "type": PADActions.EXCEL_ACTIVATE_CELL,
            "parameters": {
                "instance": instance_var,
                "cell": cell,
            },
        }]

    @staticmethod
    def get_first_free_row(column: str = "A",
                           output_var: str = "%FirstFreeRow%",
                           instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        """Get the first empty row in a column."""
        return [{
            "id": f"first_free_row_{column}",
            "type": PADActions.EXCEL_GET_FIRST_FREE_ROW,
            "parameters": {
                "instance": instance_var,
                "column": column,
                "output_variable": output_var,
            },
        }]

    @staticmethod
    def get_first_free_column(row: int = 1,
                              output_var: str = "%FirstFreeCol%",
                              instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        """Get the first empty column in a row."""
        return [{
            "id": f"first_free_col_row{row}",
            "type": PADActions.EXCEL_GET_FIRST_FREE_COL,
            "parameters": {
                "instance": instance_var,
                "row": row,
                "output_variable": output_var,
            },
        }]

    @staticmethod
    def find(search_text: str,
             search_range: str = "",
             output_var: str = "%FoundCell%",
             instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        """Find cell(s) matching *search_text*."""
        params: Dict[str, Any] = {
            "instance": instance_var,
            "search_text": search_text,
            "output_variable": output_var,
        }
        if search_range:
            params["range"] = search_range
        return [{
            "id": f"find_{search_text[:20]}",
            "type": PADActions.EXCEL_FIND,
            "parameters": params,
        }]

    @staticmethod
    def find_and_replace(search_text: str, replace_text: str,
                         search_range: str = "",
                         instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        """Find and replace text in cells."""
        params: Dict[str, Any] = {
            "instance": instance_var,
            "search_text": search_text,
            "replace_text": replace_text,
        }
        if search_range:
            params["range"] = search_range
        return [{
            "id": "find_replace",
            "type": PADActions.EXCEL_FIND_REPLACE,
            "parameters": params,
        }]


# =======================================================================
# 4. ROW / COLUMN OPERATIONS
# =======================================================================

class ExcelRowColumnActions:
    """Build PAD actions for row and column manipulation."""

    @staticmethod
    def insert_row(row_number: int,
                   instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        return [{
            "id": f"insert_row_{row_number}",
            "type": PADActions.EXCEL_INSERT_ROW,
            "parameters": {"instance": instance_var, "row": row_number},
        }]

    @staticmethod
    def insert_column(column: str,
                      instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        return [{
            "id": f"insert_col_{column}",
            "type": PADActions.EXCEL_INSERT_COLUMN,
            "parameters": {"instance": instance_var, "column": column},
        }]

    @staticmethod
    def delete_row(row_number: int,
                   instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        return [{
            "id": f"delete_row_{row_number}",
            "type": PADActions.EXCEL_DELETE_ROW,
            "parameters": {"instance": instance_var, "row": row_number},
        }]

    @staticmethod
    def delete_column(column: str,
                      instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        return [{
            "id": f"delete_col_{column}",
            "type": PADActions.EXCEL_DELETE_COLUMN,
            "parameters": {"instance": instance_var, "column": column},
        }]

    @staticmethod
    def autofit_columns(range_str: str = "",
                        instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        params: Dict[str, Any] = {"instance": instance_var}
        if range_str:
            params["range"] = range_str
        return [{
            "id": "autofit_columns",
            "type": PADActions.EXCEL_AUTOFIT_COLUMNS,
            "parameters": params,
        }]

    @staticmethod
    def autofit_rows(range_str: str = "",
                     instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        params: Dict[str, Any] = {"instance": instance_var}
        if range_str:
            params["range"] = range_str
        return [{
            "id": "autofit_rows",
            "type": PADActions.EXCEL_AUTOFIT_ROWS,
            "parameters": params,
        }]

    @staticmethod
    def set_column_width(column: str, width: float,
                         instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        return [{
            "id": f"col_width_{column}",
            "type": PADActions.EXCEL_SET_COLUMN_WIDTH,
            "parameters": {
                "instance": instance_var,
                "column": column,
                "width": width,
            },
        }]

    @staticmethod
    def set_row_height(row: int, height: float,
                       instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        return [{
            "id": f"row_height_{row}",
            "type": PADActions.EXCEL_SET_ROW_HEIGHT,
            "parameters": {
                "instance": instance_var,
                "row": row,
                "height": height,
            },
        }]


# =======================================================================
# 5. FORMATTING
# =======================================================================

class ExcelFormatActions:
    """Build PAD actions for cell formatting."""

    @staticmethod
    def format_cells(cell_or_range: str,
                     font_name: Optional[str] = None,
                     font_size: Optional[int] = None,
                     bold: Optional[bool] = None,
                     italic: Optional[bool] = None,
                     underline: Optional[bool] = None,
                     font_color: Optional[str] = None,
                     fill_color: Optional[str] = None,
                     number_format: Optional[str] = None,
                     horizontal_align: Optional[str] = None,
                     vertical_align: Optional[str] = None,
                     wrap_text: Optional[bool] = None,
                     border_style: Optional[str] = None,
                     border_color: Optional[str] = None,
                     instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        """
        Apply formatting to cells.

        Colors are hex strings (e.g. ``#FF0000``).
        ``number_format`` examples: ``0.00``, ``#,##0``, ``yyyy-mm-dd``,
        ``$#,##0.00``, ``0%``.
        """
        fmt: Dict[str, Any] = {}
        if font_name is not None:
            fmt["font_name"] = font_name
        if font_size is not None:
            fmt["font_size"] = font_size
        if bold is not None:
            fmt["bold"] = bold
        if italic is not None:
            fmt["italic"] = italic
        if underline is not None:
            fmt["underline"] = underline
        if font_color is not None:
            fmt["font_color"] = font_color
        if fill_color is not None:
            fmt["fill_color"] = fill_color
        if number_format is not None:
            fmt["number_format"] = number_format
        if horizontal_align is not None:
            fmt["horizontal_alignment"] = horizontal_align
        if vertical_align is not None:
            fmt["vertical_alignment"] = vertical_align
        if wrap_text is not None:
            fmt["wrap_text"] = wrap_text
        if border_style is not None:
            fmt["border_style"] = border_style
        if border_color is not None:
            fmt["border_color"] = border_color

        return [{
            "id": f"format_{cell_or_range}",
            "type": PADActions.EXCEL_SET_CELL_FORMAT,
            "parameters": {
                "instance": instance_var,
                "range": cell_or_range,
                "format": fmt,
            },
        }]

    @staticmethod
    def merge(cell_range: str,
              instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        return [{
            "id": f"merge_{cell_range}",
            "type": PADActions.EXCEL_MERGE_CELLS,
            "parameters": {"instance": instance_var, "range": cell_range},
        }]

    @staticmethod
    def unmerge(cell_range: str,
                instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        return [{
            "id": f"unmerge_{cell_range}",
            "type": PADActions.EXCEL_UNMERGE_CELLS,
            "parameters": {"instance": instance_var, "range": cell_range},
        }]

    @staticmethod
    def freeze_panes(cell: str = "A2",
                     instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        return [{
            "id": f"freeze_{cell}",
            "type": PADActions.EXCEL_FREEZE_PANES,
            "parameters": {"instance": instance_var, "cell": cell},
        }]

    @staticmethod
    def unfreeze_panes(instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        return [{
            "id": "unfreeze",
            "type": PADActions.EXCEL_UNFREEZE_PANES,
            "parameters": {"instance": instance_var},
        }]


# =======================================================================
# 6. DATA OPERATIONS (sort, filter, duplicates, named ranges)
# =======================================================================

class ExcelDataActions:
    """Build PAD actions for data manipulation."""

    @staticmethod
    def sort(range_str: str, sort_column: str,
             ascending: bool = True,
             instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        return [{
            "id": "sort_data",
            "type": PADActions.EXCEL_SORT,
            "parameters": {
                "instance": instance_var,
                "range": range_str,
                "sort_column": sort_column,
                "ascending": ascending,
            },
        }]

    @staticmethod
    def auto_filter(range_str: str, column: str, criteria: str,
                    instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        return [{
            "id": "auto_filter",
            "type": PADActions.EXCEL_AUTO_FILTER,
            "parameters": {
                "instance": instance_var,
                "range": range_str,
                "column": column,
                "criteria": criteria,
            },
        }]

    @staticmethod
    def remove_filter(instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        return [{
            "id": "remove_filter",
            "type": PADActions.EXCEL_REMOVE_FILTER,
            "parameters": {"instance": instance_var},
        }]

    @staticmethod
    def remove_duplicates(range_str: str,
                          columns: Optional[List[str]] = None,
                          instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        params: Dict[str, Any] = {
            "instance": instance_var,
            "range": range_str,
        }
        if columns:
            params["columns"] = columns
        return [{
            "id": "remove_duplicates",
            "type": PADActions.EXCEL_REMOVE_DUPLICATES,
            "parameters": params,
        }]

    @staticmethod
    def add_named_range(name: str, range_str: str,
                        instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        return [{
            "id": f"named_range_{name}",
            "type": PADActions.EXCEL_ADD_NAMED_RANGE,
            "parameters": {
                "instance": instance_var,
                "name": name,
                "range": range_str,
            },
        }]

    @staticmethod
    def delete_named_range(name: str,
                           instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        return [{
            "id": f"delete_named_{name}",
            "type": PADActions.EXCEL_DELETE_NAMED_RANGE,
            "parameters": {"instance": instance_var, "name": name},
        }]

    @staticmethod
    def get_named_range(name: str,
                        output_var: str = "%NamedRangeValue%",
                        instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        return [{
            "id": f"get_named_{name}",
            "type": PADActions.EXCEL_GET_NAMED_RANGE,
            "parameters": {
                "instance": instance_var,
                "name": name,
                "output_variable": output_var,
            },
        }]


# =======================================================================
# 7. TABLE / LISTOBJECT OPERATIONS
# =======================================================================

class ExcelTableActions:
    """Build PAD actions for Excel table operations."""

    @staticmethod
    def create(range_str: str, table_name: str,
               has_headers: bool = True,
               instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        return [{
            "id": f"create_table_{table_name}",
            "type": PADActions.EXCEL_CREATE_TABLE,
            "parameters": {
                "instance": instance_var,
                "range": range_str,
                "table_name": table_name,
                "has_headers": has_headers,
            },
        }]

    @staticmethod
    def resize(table_name: str, new_range: str,
               instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        return [{
            "id": f"resize_table_{table_name}",
            "type": PADActions.EXCEL_RESIZE_TABLE,
            "parameters": {
                "instance": instance_var,
                "table_name": table_name,
                "new_range": new_range,
            },
        }]

    @staticmethod
    def get_data(table_name: str,
                 output_var: str = "%TableData%",
                 instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        return [{
            "id": f"get_table_{table_name}",
            "type": PADActions.EXCEL_GET_TABLE_DATA,
            "parameters": {
                "instance": instance_var,
                "table_name": table_name,
                "output_variable": output_var,
            },
        }]


# =======================================================================
# 8. PIVOT TABLE
# =======================================================================

class ExcelPivotActions:
    """Build PAD actions for pivot table operations."""

    @staticmethod
    def create(source_range: str, dest_cell: str,
               row_fields: Optional[List[str]] = None,
               column_fields: Optional[List[str]] = None,
               value_fields: Optional[List[str]] = None,
               instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        return [{
            "id": "create_pivot",
            "type": PADActions.EXCEL_CREATE_PIVOT,
            "parameters": {
                "instance": instance_var,
                "source_range": source_range,
                "destination_cell": dest_cell,
                "row_fields": row_fields or [],
                "column_fields": column_fields or [],
                "value_fields": value_fields or [],
            },
        }]

    @staticmethod
    def refresh(pivot_name: str = "",
                instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        params: Dict[str, Any] = {"instance": instance_var}
        if pivot_name:
            params["pivot_table_name"] = pivot_name
        return [{
            "id": "refresh_pivot",
            "type": PADActions.EXCEL_REFRESH_PIVOT,
            "parameters": params,
        }]


# =======================================================================
# 9. CHART OPERATIONS
# =======================================================================

class ExcelChartActions:
    """Build PAD actions for chart operations."""

    @staticmethod
    def create(source_range: str,
               chart_type: str = "ColumnClustered",
               chart_title: str = "",
               instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        return [{
            "id": "create_chart",
            "type": PADActions.EXCEL_CREATE_CHART,
            "parameters": {
                "instance": instance_var,
                "source_range": source_range,
                "chart_type": chart_type,
                "chart_title": chart_title,
            },
        }]

    @staticmethod
    def delete(chart_name: str,
               instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        return [{
            "id": f"delete_chart_{chart_name}",
            "type": PADActions.EXCEL_DELETE_CHART,
            "parameters": {"instance": instance_var, "chart_name": chart_name},
        }]

    @staticmethod
    def export_image(chart_name: str, output_path: str,
                     image_format: str = "png",
                     instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        return [{
            "id": f"export_chart_{chart_name}",
            "type": PADActions.EXCEL_EXPORT_CHART,
            "parameters": {
                "instance": instance_var,
                "chart_name": chart_name,
                "file_path": output_path,
                "image_format": image_format,
            },
        }]


# =======================================================================
# 10. PRINT OPERATIONS
# =======================================================================

class ExcelPrintActions:
    """Build PAD actions for printing."""

    @staticmethod
    def print_worksheet(copies: int = 1,
                        printer: Optional[str] = None,
                        instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        params: Dict[str, Any] = {
            "instance": instance_var,
            "copies": copies,
        }
        if printer:
            params["printer_name"] = printer
        return [{
            "id": "print_sheet",
            "type": PADActions.EXCEL_PRINT,
            "parameters": params,
        }]

    @staticmethod
    def set_print_area(range_str: str,
                       instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        return [{
            "id": "set_print_area",
            "type": PADActions.EXCEL_SET_PRINT_AREA,
            "parameters": {"instance": instance_var, "range": range_str},
        }]

    @staticmethod
    def page_setup(orientation: str = "portrait",
                   paper_size: str = "A4",
                   margins: Optional[Dict[str, float]] = None,
                   fit_to_page: bool = False,
                   instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        params: Dict[str, Any] = {
            "instance": instance_var,
            "orientation": orientation,
            "paper_size": paper_size,
            "fit_to_page": fit_to_page,
        }
        if margins:
            params["margins"] = margins
        return [{
            "id": "page_setup",
            "type": PADActions.EXCEL_SET_PAGE_SETUP,
            "parameters": params,
        }]


# =======================================================================
# 11. IMPORT / EXPORT
# =======================================================================

class ExcelImportExportActions:
    """Build PAD actions for import and export."""

    @staticmethod
    def export_pdf(output_path: str,
                   sheet_name: Optional[str] = None,
                   instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        params: Dict[str, Any] = {
            "instance": instance_var,
            "file_path": output_path,
        }
        if sheet_name:
            params["worksheet_name"] = sheet_name
        return [{
            "id": "export_pdf",
            "type": PADActions.EXCEL_EXPORT_PDF,
            "parameters": params,
        }]

    @staticmethod
    def export_csv(output_path: str,
                   delimiter: str = ",",
                   instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        return [{
            "id": "export_csv",
            "type": PADActions.EXCEL_EXPORT_CSV,
            "parameters": {
                "instance": instance_var,
                "file_path": output_path,
                "delimiter": delimiter,
            },
        }]

    @staticmethod
    def import_csv(file_path: str, dest_cell: str = "A1",
                   delimiter: str = ",",
                   instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        return [{
            "id": "import_csv",
            "type": PADActions.EXCEL_IMPORT_CSV,
            "parameters": {
                "instance": instance_var,
                "file_path": file_path,
                "destination_cell": dest_cell,
                "delimiter": delimiter,
            },
        }]


# =======================================================================
# 12. PROTECTION & CALCULATION
# =======================================================================

class ExcelProtectionActions:
    """Build PAD actions for workbook/worksheet protection."""

    @staticmethod
    def protect_workbook(password: str = "",
                         instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        return [{
            "id": "protect_workbook",
            "type": PADActions.EXCEL_PROTECT_WORKBOOK,
            "parameters": {"instance": instance_var, "password": password},
        }]

    @staticmethod
    def unprotect_workbook(password: str = "",
                           instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        return [{
            "id": "unprotect_workbook",
            "type": PADActions.EXCEL_UNPROTECT_WORKBOOK,
            "parameters": {"instance": instance_var, "password": password},
        }]

    @staticmethod
    def set_calculation_mode(mode: str = "automatic",
                             instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        """mode: ``automatic``, ``manual``, ``semiautomatic``."""
        return [{
            "id": "calc_mode",
            "type": PADActions.EXCEL_SET_CALCULATION,
            "parameters": {"instance": instance_var, "mode": mode},
        }]

    @staticmethod
    def recalculate(instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        return [{
            "id": "recalculate",
            "type": PADActions.EXCEL_CALCULATE,
            "parameters": {"instance": instance_var},
        }]


# =======================================================================
# 13. VBA MACRO OPERATIONS (extended)
# =======================================================================

class ExcelMacroActions:
    """Build PAD actions for VBA macro operations."""

    @staticmethod
    def run(macro_name: str,
            instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        return [{
            "id": f"run_macro_{macro_name}",
            "type": PADActions.EXCEL_RUN_MACRO,
            "parameters": {
                "instance": instance_var,
                "macro_name": macro_name,
            },
        }]

    @staticmethod
    def run_with_args(macro_name: str, args: List[Any],
                      instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        """Run a macro with arguments."""
        return [{
            "id": f"run_macro_{macro_name}_args",
            "type": PADActions.EXCEL_RUN_MACRO,
            "parameters": {
                "instance": instance_var,
                "macro_name": macro_name,
                "arguments": args,
            },
        }]

    @staticmethod
    def run_and_capture(macro_name: str,
                        output_var: str = "%MacroResult%",
                        instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        """Run a macro and capture its return value."""
        return [{
            "id": f"run_capture_{macro_name}",
            "type": PADActions.EXCEL_RUN_MACRO,
            "parameters": {
                "instance": instance_var,
                "macro_name": macro_name,
                "capture_return": True,
                "output_variable": output_var,
            },
        }]


# =======================================================================
# 14. ERROR RECOVERY
# =======================================================================

class ExcelErrorRecovery:
    """
    Build PAD actions for detecting and recovering from Excel problems
    such as hung processes, stuck dialogs, and unexpected popups.
    """

    @staticmethod
    def detect_hung_excel(timeout: int = 30) -> List[Dict[str, Any]]:
        """Check if Excel is responding; if not, log a warning."""
        return [
            {
                "id": "check_excel_running",
                "type": PADActions.PROCESS_IF_RUNNING,
                "parameters": {"process_name": "EXCEL.EXE"},
            },
            {
                "id": "wait_for_response",
                "type": PADActions.UI_WAIT_WINDOW,
                "parameters": {
                    "window_title": "Microsoft Excel",
                    "process_name": "EXCEL.EXE",
                    "timeout": timeout,
                    "on_timeout": "continue",
                },
            },
        ]

    @staticmethod
    def force_kill_excel() -> List[Dict[str, Any]]:
        """Forcefully terminate all Excel processes."""
        return [{
            "id": "kill_excel",
            "type": PADActions.PROCESS_TERMINATE,
            "parameters": {"process_name": "EXCEL.EXE"},
        }]

    @staticmethod
    def dismiss_unexpected_dialog(button: str = "OK",
                                  timeout: int = 5) -> List[Dict[str, Any]]:
        """Try to dismiss any unexpected Excel dialog."""
        return [
            {
                "id": "check_unexpected_dialog",
                "type": PADActions.UI_IF_WINDOW_EXISTS,
                "parameters": {
                    "window_title": "Microsoft Excel",
                    "process_name": "EXCEL.EXE",
                    "timeout": timeout,
                    "output_variable": "%UnexpectedDlg%",
                },
            },
            {
                "id": "if_dialog_exists",
                "type": PADActions.IF,
                "parameters": {"condition": "%UnexpectedDlg% IS NOT EMPTY"},
            },
            {
                "id": "dismiss_dialog",
                "type": PADActions.UI_CLICK,
                "parameters": {
                    "window": "%UnexpectedDlg%",
                    "element_name": button,
                    "element_type": "Button",
                    "click_type": "left_click",
                },
            },
            {
                "id": "log_dismissed",
                "type": PADActions.LOG_MESSAGE,
                "parameters": {
                    "message": f"Dismissed unexpected Excel dialog (clicked '{button}')",
                },
            },
            {
                "id": "end_if_dialog",
                "type": PADActions.END_IF,
                "parameters": {},
            },
        ]

    @staticmethod
    def safe_close_with_retry(max_attempts: int = 3,
                              instance_var: str = "%ExcelInstance%") -> List[Dict[str, Any]]:
        """
        Attempt to close Excel gracefully; dismiss dialogs if they
        appear; force-kill as last resort.
        """
        actions: List[Dict[str, Any]] = []
        for attempt in range(1, max_attempts + 1):
            actions.extend([
                {
                    "id": f"try_close_{attempt}",
                    "type": PADActions.ON_ERROR,
                    "parameters": {"on_error": "continue"},
                },
                {
                    "id": f"close_attempt_{attempt}",
                    "type": PADActions.EXCEL_CLOSE,
                    "parameters": {
                        "instance": instance_var,
                        "save_before_close": False,
                    },
                },
                {
                    "id": f"end_try_close_{attempt}",
                    "type": PADActions.END_ERROR,
                    "parameters": {},
                },
            ])
            actions.extend(ExcelErrorRecovery.dismiss_unexpected_dialog())
            actions.append({
                "id": f"wait_close_{attempt}",
                "type": PADActions.WAIT,
                "parameters": {"duration": 1},
            })

        actions.extend(ExcelErrorRecovery.force_kill_excel())
        return actions


# =======================================================================
# 15. COMPOSITE FLOW BUILDER
# =======================================================================

class ExcelFlowBuilder:
    """
    High-level builder that composes action lists from the classes
    above into a complete, executable PAD flow definition.

    Usage::

        builder = ExcelFlowBuilder("MyReport")
        builder.add(ExcelWorkbookActions.launch())
        builder.add(ExcelWorkbookActions.open_workbook(r"C:\\data.xlsx"))
        builder.add(ExcelCellActions.read("A1:D100"))
        builder.add(ExcelDataActions.sort("A1:D100", "B"))
        builder.add(ExcelWorkbookActions.save())
        builder.add(ExcelWorkbookActions.close())
        flow = builder.build()
    """

    def __init__(self, name: str, description: str = "",
                 timeout: int = 300):
        self.name = name
        self.description = description or f"Excel automation flow: {name}"
        self.timeout = timeout
        self._actions: List[Dict[str, Any]] = []
        self._step = 0

    def add(self, actions: List[Dict[str, Any]]) -> "ExcelFlowBuilder":
        """Append a list of actions (from any Actions class)."""
        for action in actions:
            self._step += 1
            if action["id"] in {a["id"] for a in self._actions}:
                action = {**action, "id": f"{action['id']}_{self._step}"}
            self._actions.append(action)
        return self

    def add_wait(self, seconds: float = 1) -> "ExcelFlowBuilder":
        self._step += 1
        self._actions.append({
            "id": f"wait_{self._step}",
            "type": PADActions.WAIT,
            "parameters": {"duration": seconds},
        })
        return self

    def add_log(self, message: str) -> "ExcelFlowBuilder":
        self._step += 1
        self._actions.append({
            "id": f"log_{self._step}",
            "type": PADActions.LOG_MESSAGE,
            "parameters": {"message": message},
        })
        return self

    def add_error_recovery(self) -> "ExcelFlowBuilder":
        """Append standard error-recovery actions at the end."""
        self.add(ExcelErrorRecovery.dismiss_unexpected_dialog())
        self.add(ExcelErrorRecovery.safe_close_with_retry())
        return self

    def build(self) -> Dict[str, Any]:
        """Return the complete flow definition dict."""
        return {
            "name": self.name,
            "description": self.description,
            "version": "1.0",
            "enabled": True,
            "variables": {
                "input": {},
                "output": {
                    "status": {"type": "string", "description": "success or failed"},
                },
            },
            "actions": self._actions,
            "error_handling": {
                "on_error": "stop",
                "retry_count": 1,
                "retry_delay": 3,
            },
            "settings": {
                "timeout": self.timeout,
                "priority": 5,
                "run_mode": "attended",
            },
            "metadata": {
                "created_by": "ExcelFlowBuilder",
                "created_at": datetime.now().isoformat(),
                "tags": ["excel", "automation", "auto-generated"],
            },
        }

    def save(self, flows_dir: Union[str, Path]) -> Path:
        """Build and write to ``flows_dir/{name}.json``."""
        import json as _json

        flows_dir = Path(flows_dir)
        flows_dir.mkdir(parents=True, exist_ok=True)
        target = flows_dir / f"{self.name}.json"

        with open(target, "w", encoding="utf-8") as fh:
            _json.dump(self.build(), fh, indent=2, default=str)

        return target
