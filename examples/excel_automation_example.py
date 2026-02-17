"""
Excel Automation Examples — Full Coverage
==========================================
Demonstrates every category of Excel operations available in the
PAD Framework:  workbook, worksheet, cell, row/column, formatting,
data, tables, pivots, charts, print, import/export, protection,
macros, popup handling, and error recovery.

Each example builds a PAD flow definition using the ExcelFlowBuilder
and the action classes.  The flows can be saved to disk or executed
directly through the framework.
"""

from pad_framework import (
    PADFramework,
    ExcelFlowBuilder,
    ExcelWorkbookActions,
    ExcelWorksheetActions,
    ExcelCellActions,
    ExcelRowColumnActions,
    ExcelFormatActions,
    ExcelDataActions,
    ExcelTableActions,
    ExcelPivotActions,
    ExcelChartActions,
    ExcelPrintActions,
    ExcelImportExportActions,
    ExcelProtectionActions,
    ExcelMacroActions,
    ExcelErrorRecovery,
    ExcelPopupTemplates,
    PopupDescriptor,
    PopupField,
)


# ---------------------------------------------------------------
# 1. Workbook operations
# ---------------------------------------------------------------

def example_workbook_ops():
    """Open, save-as, and close a workbook."""
    print("=" * 60)
    print("1. Workbook Operations")
    print("=" * 60)

    b = ExcelFlowBuilder("WorkbookOps", "Open, save-as, close")
    b.add(ExcelWorkbookActions.launch())
    b.add(ExcelWorkbookActions.open_workbook(r"C:\Data\sales.xlsx"))
    b.add_wait(1)
    b.add(ExcelWorkbookActions.save_as(r"C:\Data\sales_backup.xlsx"))
    b.add(ExcelWorkbookActions.close(save=False))

    flow = b.build()
    print(f"  Flow: {flow['name']}  Actions: {len(flow['actions'])}")
    print()


# ---------------------------------------------------------------
# 2. Worksheet operations
# ---------------------------------------------------------------

def example_worksheet_ops():
    """Add, rename, copy, delete worksheets."""
    print("=" * 60)
    print("2. Worksheet Operations")
    print("=" * 60)

    b = ExcelFlowBuilder("WorksheetOps")
    b.add(ExcelWorkbookActions.launch())
    b.add(ExcelWorkbookActions.open_workbook(r"C:\Data\report.xlsx"))
    b.add(ExcelWorksheetActions.list_all())
    b.add(ExcelWorksheetActions.add("Summary"))
    b.add(ExcelWorksheetActions.rename("Sheet1", "RawData"))
    b.add(ExcelWorksheetActions.copy("RawData", "RawData_Backup"))
    b.add(ExcelWorksheetActions.activate("Summary"))
    b.add(ExcelWorksheetActions.delete("RawData_Backup"))
    b.add(ExcelWorkbookActions.save())
    b.add(ExcelWorkbookActions.close())

    flow = b.build()
    print(f"  Flow: {flow['name']}  Actions: {len(flow['actions'])}")
    print()


# ---------------------------------------------------------------
# 3. Cell / range read & write
# ---------------------------------------------------------------

def example_cell_ops():
    """Read, write, find, replace, formulas."""
    print("=" * 60)
    print("3. Cell / Range Operations")
    print("=" * 60)

    b = ExcelFlowBuilder("CellOps")
    b.add(ExcelWorkbookActions.launch())
    b.add(ExcelWorkbookActions.open_workbook(r"C:\Data\inventory.xlsx"))

    b.add(ExcelCellActions.read("A1:D100"))
    b.add(ExcelCellActions.write("E1", "Total"))
    b.add(ExcelCellActions.write_formula("E2", "=SUM(B2:D2)"))
    b.add(ExcelCellActions.write_range("G1", [
        ["Region", "Q1", "Q2"],
        ["North", 1200, 1350],
        ["South", 980, 1100],
    ]))
    b.add(ExcelCellActions.find("Discontinued"))
    b.add(ExcelCellActions.find_and_replace("N/A", "0"))
    b.add(ExcelCellActions.clear("F1:F100", clear_type="contents"))
    b.add(ExcelCellActions.get_first_free_row("A"))
    b.add(ExcelCellActions.get_first_free_column(1))

    b.add(ExcelWorkbookActions.save())
    b.add(ExcelWorkbookActions.close())

    flow = b.build()
    print(f"  Flow: {flow['name']}  Actions: {len(flow['actions'])}")
    print()


# ---------------------------------------------------------------
# 4. Row / column manipulation
# ---------------------------------------------------------------

def example_row_column_ops():
    """Insert, delete, autofit, resize rows and columns."""
    print("=" * 60)
    print("4. Row / Column Operations")
    print("=" * 60)

    b = ExcelFlowBuilder("RowColOps")
    b.add(ExcelWorkbookActions.launch())
    b.add(ExcelWorkbookActions.open_workbook(r"C:\Data\employees.xlsx"))

    b.add(ExcelRowColumnActions.insert_row(1))
    b.add(ExcelRowColumnActions.insert_column("A"))
    b.add(ExcelRowColumnActions.set_column_width("B", 25.0))
    b.add(ExcelRowColumnActions.set_row_height(1, 30.0))
    b.add(ExcelRowColumnActions.autofit_columns("A1:F100"))
    b.add(ExcelRowColumnActions.autofit_rows("A1:F100"))
    b.add(ExcelRowColumnActions.delete_row(50))
    b.add(ExcelRowColumnActions.delete_column("G"))

    b.add(ExcelWorkbookActions.save())
    b.add(ExcelWorkbookActions.close())

    flow = b.build()
    print(f"  Flow: {flow['name']}  Actions: {len(flow['actions'])}")
    print()


# ---------------------------------------------------------------
# 5. Formatting
# ---------------------------------------------------------------

def example_formatting():
    """Apply fonts, colors, borders, merging, freeze panes."""
    print("=" * 60)
    print("5. Formatting Operations")
    print("=" * 60)

    b = ExcelFlowBuilder("FormattingOps")
    b.add(ExcelWorkbookActions.launch())
    b.add(ExcelWorkbookActions.open_workbook(r"C:\Data\report.xlsx"))

    b.add(ExcelFormatActions.format_cells(
        "A1:F1",
        bold=True, font_size=14, font_color="#FFFFFF",
        fill_color="#4472C4", horizontal_align="center",
        border_style="thin", border_color="#000000",
    ))
    b.add(ExcelFormatActions.format_cells(
        "B2:B100", number_format="$#,##0.00",
    ))
    b.add(ExcelFormatActions.format_cells(
        "C2:C100", number_format="yyyy-mm-dd",
    ))
    b.add(ExcelFormatActions.merge("A1:F1"))
    b.add(ExcelFormatActions.freeze_panes("A2"))

    b.add(ExcelWorkbookActions.save())
    b.add(ExcelWorkbookActions.close())

    flow = b.build()
    print(f"  Flow: {flow['name']}  Actions: {len(flow['actions'])}")
    print()


# ---------------------------------------------------------------
# 6. Data: sort, filter, duplicates, named ranges
# ---------------------------------------------------------------

def example_data_ops():
    """Sort, filter, remove duplicates, named ranges."""
    print("=" * 60)
    print("6. Data Operations")
    print("=" * 60)

    b = ExcelFlowBuilder("DataOps")
    b.add(ExcelWorkbookActions.launch())
    b.add(ExcelWorkbookActions.open_workbook(r"C:\Data\transactions.xlsx"))

    b.add(ExcelDataActions.sort("A1:E500", "D", ascending=False))
    b.add(ExcelDataActions.auto_filter("A1:E500", "B", ">1000"))
    b.add(ExcelDataActions.remove_duplicates("A1:E500", columns=["A", "C"]))
    b.add(ExcelDataActions.add_named_range("SalesData", "A1:E500"))
    b.add(ExcelDataActions.get_named_range("SalesData"))
    b.add(ExcelDataActions.remove_filter())

    b.add(ExcelWorkbookActions.save())
    b.add(ExcelWorkbookActions.close())

    flow = b.build()
    print(f"  Flow: {flow['name']}  Actions: {len(flow['actions'])}")
    print()


# ---------------------------------------------------------------
# 7. Tables
# ---------------------------------------------------------------

def example_table_ops():
    """Create an Excel table and read its data."""
    print("=" * 60)
    print("7. Table Operations")
    print("=" * 60)

    b = ExcelFlowBuilder("TableOps")
    b.add(ExcelWorkbookActions.launch())
    b.add(ExcelWorkbookActions.open_workbook(r"C:\Data\products.xlsx"))

    b.add(ExcelTableActions.create("A1:D50", "ProductTable"))
    b.add(ExcelTableActions.get_data("ProductTable"))
    b.add(ExcelTableActions.resize("ProductTable", "A1:E60"))

    b.add(ExcelWorkbookActions.save())
    b.add(ExcelWorkbookActions.close())

    flow = b.build()
    print(f"  Flow: {flow['name']}  Actions: {len(flow['actions'])}")
    print()


# ---------------------------------------------------------------
# 8. Pivot tables
# ---------------------------------------------------------------

def example_pivot_ops():
    """Create and refresh a pivot table."""
    print("=" * 60)
    print("8. Pivot Table Operations")
    print("=" * 60)

    b = ExcelFlowBuilder("PivotOps")
    b.add(ExcelWorkbookActions.launch())
    b.add(ExcelWorkbookActions.open_workbook(r"C:\Data\sales.xlsx"))

    b.add(ExcelPivotActions.create(
        source_range="Sheet1!A1:E500",
        dest_cell="PivotSheet!A1",
        row_fields=["Region"],
        column_fields=["Quarter"],
        value_fields=["Revenue"],
    ))
    b.add(ExcelPivotActions.refresh())

    b.add(ExcelWorkbookActions.save())
    b.add(ExcelWorkbookActions.close())

    flow = b.build()
    print(f"  Flow: {flow['name']}  Actions: {len(flow['actions'])}")
    print()


# ---------------------------------------------------------------
# 9. Charts
# ---------------------------------------------------------------

def example_chart_ops():
    """Create a chart and export it as an image."""
    print("=" * 60)
    print("9. Chart Operations")
    print("=" * 60)

    b = ExcelFlowBuilder("ChartOps")
    b.add(ExcelWorkbookActions.launch())
    b.add(ExcelWorkbookActions.open_workbook(r"C:\Data\metrics.xlsx"))

    b.add(ExcelChartActions.create(
        source_range="A1:C12",
        chart_type="Line",
        chart_title="Monthly Metrics",
    ))
    b.add(ExcelChartActions.export_image(
        chart_name="Chart 1",
        output_path=r"C:\Output\metrics_chart.png",
    ))
    b.add(ExcelChartActions.delete("Chart 1"))

    b.add(ExcelWorkbookActions.close())

    flow = b.build()
    print(f"  Flow: {flow['name']}  Actions: {len(flow['actions'])}")
    print()


# ---------------------------------------------------------------
# 10. Print
# ---------------------------------------------------------------

def example_print_ops():
    """Set up page and print a worksheet."""
    print("=" * 60)
    print("10. Print Operations")
    print("=" * 60)

    b = ExcelFlowBuilder("PrintOps")
    b.add(ExcelWorkbookActions.launch())
    b.add(ExcelWorkbookActions.open_workbook(r"C:\Data\invoice.xlsx"))

    b.add(ExcelPrintActions.page_setup(
        orientation="landscape", paper_size="A4",
        margins={"top": 1.0, "bottom": 1.0, "left": 0.75, "right": 0.75},
    ))
    b.add(ExcelPrintActions.set_print_area("A1:G50"))
    b.add(ExcelPrintActions.print_worksheet(copies=2))

    b.add(ExcelWorkbookActions.close())

    flow = b.build()
    print(f"  Flow: {flow['name']}  Actions: {len(flow['actions'])}")
    print()


# ---------------------------------------------------------------
# 11. Import / Export
# ---------------------------------------------------------------

def example_import_export():
    """Export to PDF and CSV; import a CSV."""
    print("=" * 60)
    print("11. Import / Export Operations")
    print("=" * 60)

    b = ExcelFlowBuilder("ImportExportOps")
    b.add(ExcelWorkbookActions.launch())
    b.add(ExcelWorkbookActions.open_workbook(r"C:\Data\financials.xlsx"))

    b.add(ExcelImportExportActions.export_pdf(r"C:\Output\financials.pdf"))
    b.add(ExcelImportExportActions.export_csv(r"C:\Output\financials.csv"))
    b.add(ExcelWorksheetActions.add("Imported"))
    b.add(ExcelWorksheetActions.activate("Imported"))
    b.add(ExcelImportExportActions.import_csv(
        r"C:\Input\external_data.csv", dest_cell="A1",
    ))

    b.add(ExcelWorkbookActions.save())
    b.add(ExcelWorkbookActions.close())

    flow = b.build()
    print(f"  Flow: {flow['name']}  Actions: {len(flow['actions'])}")
    print()


# ---------------------------------------------------------------
# 12. Protection & calculation
# ---------------------------------------------------------------

def example_protection():
    """Protect workbook/sheets and manage calculation mode."""
    print("=" * 60)
    print("12. Protection & Calculation")
    print("=" * 60)

    b = ExcelFlowBuilder("ProtectionOps")
    b.add(ExcelWorkbookActions.launch())
    b.add(ExcelWorkbookActions.open_workbook(r"C:\Data\budget.xlsx"))

    b.add(ExcelProtectionActions.set_calculation_mode("manual"))
    b.add(ExcelCellActions.write("A1", "Updated Budget"))
    b.add(ExcelProtectionActions.recalculate())
    b.add(ExcelProtectionActions.set_calculation_mode("automatic"))
    b.add(ExcelWorksheetActions.protect("Summary", password="s3cret"))
    b.add(ExcelProtectionActions.protect_workbook(password="wb_pass"))

    b.add(ExcelWorkbookActions.save())
    b.add(ExcelWorkbookActions.close())

    flow = b.build()
    print(f"  Flow: {flow['name']}  Actions: {len(flow['actions'])}")
    print()


# ---------------------------------------------------------------
# 13. VBA macro operations
# ---------------------------------------------------------------

def example_macro_ops():
    """Run macros: basic, with args, capture return value."""
    print("=" * 60)
    print("13. VBA Macro Operations")
    print("=" * 60)

    b = ExcelFlowBuilder("MacroOps")
    b.add(ExcelWorkbookActions.launch())
    b.add(ExcelWorkbookActions.open_workbook(
        r"C:\Macros\reporting.xlsm",
    ))

    b.add(ExcelMacroActions.run("PrepareData"))
    b.add(ExcelMacroActions.run_with_args(
        "GenerateReport", args=["2026-Q1", "North"],
    ))
    b.add(ExcelMacroActions.run_and_capture("GetSummary"))

    b.add(ExcelWorkbookActions.save())
    b.add(ExcelWorkbookActions.close())

    flow = b.build()
    print(f"  Flow: {flow['name']}  Actions: {len(flow['actions'])}")
    print()


# ---------------------------------------------------------------
# 14. Popup / dialog handling (expanded)
# ---------------------------------------------------------------

def example_popup_handling():
    """Handle every type of Excel popup and VBA dialog."""
    print("=" * 60)
    print("14. Popup / Dialog Handling (All Types)")
    print("=" * 60)

    from pad_framework import ExcelPopupHandler
    pad = PADFramework()
    handler = ExcelPopupHandler(pad)

    popups = [
        ExcelPopupTemplates.password_prompt("filepass123"),
        ExcelPopupTemplates.protected_view_bar(),
        ExcelPopupTemplates.macro_security_prompt(),
        ExcelPopupTemplates.vba_inputbox("2026-02-17", window_title="Enter Date"),
        ExcelPopupTemplates.msgbox_yes_no(click_yes=True),
        ExcelPopupTemplates.login_form("admin", "p@ss"),
        ExcelPopupTemplates.data_entry_form({
            "txtName": "Test",
            "txtAmount": "500",
        }),
        ExcelPopupTemplates.compatibility_mode_prompt(),
        ExcelPopupTemplates.save_as_dialog(r"C:\Out\result.xlsx"),
    ]

    flow_def = handler.build_flow_only(
        file_path=r"C:\Legacy\old_system.xlsm",
        macro_name="ProcessAll",
        popups=popups,
    )

    print(f"  Flow: {flow_def['name']}")
    print(f"  Actions: {len(flow_def['actions'])}")
    print(f"  Popups handled: {len(popups)}")
    print()


# ---------------------------------------------------------------
# 15. Error recovery
# ---------------------------------------------------------------

def example_error_recovery():
    """Detect hung Excel, dismiss dialogs, force close."""
    print("=" * 60)
    print("15. Error Recovery")
    print("=" * 60)

    b = ExcelFlowBuilder("ErrorRecovery")
    b.add(ExcelErrorRecovery.detect_hung_excel(timeout=15))
    b.add(ExcelErrorRecovery.dismiss_unexpected_dialog("OK"))
    b.add(ExcelErrorRecovery.safe_close_with_retry(max_attempts=3))
    b.add_log("Excel cleanup completed")

    flow = b.build()
    print(f"  Flow: {flow['name']}  Actions: {len(flow['actions'])}")
    print()


# ---------------------------------------------------------------
# 16. End-to-end: complete reporting pipeline
# ---------------------------------------------------------------

def example_full_pipeline():
    """
    Full pipeline: open file, read data, add sheet, write formulas,
    format, create chart, export PDF, handle popups, close.
    """
    print("=" * 60)
    print("16. End-to-End Reporting Pipeline")
    print("=" * 60)

    b = ExcelFlowBuilder("FullReportPipeline", timeout=600)

    b.add(ExcelWorkbookActions.launch())
    b.add(ExcelWorkbookActions.open_workbook(r"C:\Data\quarterly.xlsx"))
    b.add_wait(2)

    b.add(ExcelCellActions.read("Data!A1:F500"))
    b.add(ExcelWorksheetActions.add("Analysis"))
    b.add(ExcelWorksheetActions.activate("Analysis"))

    b.add(ExcelCellActions.write("A1", "Region"))
    b.add(ExcelCellActions.write("B1", "Total Revenue"))
    b.add(ExcelCellActions.write_formula("B2", "=SUMIFS(Data!F:F,Data!A:A,A2)"))

    b.add(ExcelFormatActions.format_cells(
        "A1:B1", bold=True, fill_color="#4472C4", font_color="#FFFFFF",
    ))
    b.add(ExcelFormatActions.format_cells("B2:B100", number_format="$#,##0"))
    b.add(ExcelRowColumnActions.autofit_columns("A1:B100"))

    b.add(ExcelDataActions.sort("A1:B100", "B", ascending=False))
    b.add(ExcelTableActions.create("A1:B50", "RevenueTable"))

    b.add(ExcelChartActions.create(
        "A1:B10", chart_type="ColumnClustered", chart_title="Top Regions",
    ))

    b.add(ExcelPrintActions.page_setup(orientation="landscape"))
    b.add(ExcelImportExportActions.export_pdf(r"C:\Output\quarterly_report.pdf"))

    b.add(ExcelWorkbookActions.save_as(r"C:\Output\quarterly_analysis.xlsx"))

    b.add_error_recovery()

    flow = b.build()
    print(f"  Flow: {flow['name']}  Actions: {len(flow['actions'])}")
    print(f"  Timeout: {flow['settings']['timeout']}s")
    print()


# ---------------------------------------------------------------
# Main
# ---------------------------------------------------------------

def main():
    print()
    print("*" * 60)
    print("  Excel Automation — Complete Example Suite")
    print("*" * 60)
    print()

    examples = [
        example_workbook_ops,
        example_worksheet_ops,
        example_cell_ops,
        example_row_column_ops,
        example_formatting,
        example_data_ops,
        example_table_ops,
        example_pivot_ops,
        example_chart_ops,
        example_print_ops,
        example_import_export,
        example_protection,
        example_macro_ops,
        example_popup_handling,
        example_error_recovery,
        example_full_pipeline,
    ]

    for fn in examples:
        try:
            fn()
        except Exception as exc:
            print(f"  [Expected without PAD runtime] {exc}")
            print()

    print("=" * 60)
    print("All 16 examples completed.")
    print("=" * 60)


if __name__ == "__main__":
    main()
