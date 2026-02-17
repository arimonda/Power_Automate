"""
Excel Popup Handling Examples for Power Automate Desktop
=========================================================
Demonstrates how to use the ExcelPopupHandler to:
  1. Open an Excel file with macros
  2. Detect VBA-triggered popups
  3. Fill field values
  4. Submit / dismiss the popup

All examples build PAD flow definitions that are executed via the
framework's FlowExecutor (which drives PAD.Console.Host.exe).
"""

from pad_framework import (
    PADFramework,
    ExcelPopupHandler,
    ExcelPopupTemplates,
    PopupDescriptor,
    PopupField,
)


def example_1_single_macro_popup():
    """
    SCENARIO: An Excel macro (ShowLoginForm) opens a login UserForm
    with Username and Password fields plus a Login button.
    """
    print("=" * 60)
    print("Example 1: Single Macro Popup — Login Form")
    print("=" * 60)

    pad = PADFramework()
    handler = ExcelPopupHandler(pad)

    popup = PopupDescriptor(
        window_title="Login",
        fields=[
            PopupField("Username", "admin", element_name="txtUsername"),
            PopupField("Password", "s3cret", element_name="txtPassword"),
        ],
        submit_button="Login",
    )

    result = handler.handle_macro_popup(
        file_path=r"C:\Reports\secured_report.xlsm",
        macro_name="ShowLoginForm",
        popup=popup,
        timeout=120,
        retry_count=1,
    )

    print(f"  Status: {result.status}")
    print(f"  Duration: {result.duration:.2f}s")
    print()


def example_2_auto_popup_on_open():
    """
    SCENARIO: Opening the workbook triggers Workbook_Open which
    shows an InputBox asking for a report date.
    """
    print("=" * 60)
    print("Example 2: Auto-Launch Popup on Workbook_Open")
    print("=" * 60)

    pad = PADFramework()
    handler = ExcelPopupHandler(pad)

    popup = PopupDescriptor(
        window_title="Enter Report Date",
        fields=[
            PopupField("Date", "2026-02-17", element_name="txtInput"),
        ],
        submit_button="OK",
    )

    result = handler.handle_auto_popup(
        file_path=r"C:\Reports\daily_report.xlsm",
        popup=popup,
    )

    print(f"  Status: {result.status}")
    print()


def example_3_multiple_sequential_popups():
    """
    SCENARIO: Running RunDataPipeline macro triggers three popups
    in sequence — a config form, a confirmation dialog, and a
    results summary.
    """
    print("=" * 60)
    print("Example 3: Multiple Sequential Popups")
    print("=" * 60)

    pad = PADFramework()
    handler = ExcelPopupHandler(pad)

    popup_config = PopupDescriptor(
        window_title="Pipeline Configuration",
        fields=[
            PopupField("Source", "Production", field_type="dropdown",
                        element_name="cmbSource"),
            PopupField("Date Range", "Last 30 days",
                        element_name="txtDateRange"),
            PopupField("Include Archived", True, field_type="checkbox",
                        element_name="chkArchived"),
        ],
        submit_button="Next",
    )

    popup_confirm = ExcelPopupTemplates.confirmation_dialog(
        window_title="Confirm Pipeline Run",
        submit_button="Yes",
    )

    popup_done = ExcelPopupTemplates.confirmation_dialog(
        window_title="Pipeline Complete",
        submit_button="OK",
    )

    result = handler.open_and_handle_popup(
        file_path=r"C:\ETL\data_pipeline.xlsm",
        macro_name="RunDataPipeline",
        popups=[popup_config, popup_confirm, popup_done],
        save_after=True,
        close_after=True,
    )

    print(f"  Status: {result.status}")
    print(f"  Duration: {result.duration:.2f}s")
    print()


def example_4_using_templates():
    """
    SCENARIO: Use the built-in ExcelPopupTemplates for common
    popup patterns instead of building PopupDescriptors manually.
    """
    print("=" * 60)
    print("Example 4: Using Built-in Templates")
    print("=" * 60)

    pad = PADFramework()
    handler = ExcelPopupHandler(pad)

    login = ExcelPopupTemplates.login_form("jdoe", "P@ssw0rd")

    data_entry = ExcelPopupTemplates.data_entry_form(
        fields={
            "txtName": "John Doe",
            "txtDepartment": "Engineering",
            "txtAmount": "15000",
        },
        window_title="Expense Entry",
        submit_button="Submit",
    )

    dropdown = ExcelPopupTemplates.dropdown_selection(
        dropdown_name="cmbRegion",
        selected_value="North America",
        window_title="Select Region",
    )

    result = handler.open_and_handle_popup(
        file_path=r"C:\Finance\expense_tracker.xlsm",
        macro_name="OpenEntryForm",
        popups=[login, data_entry, dropdown],
    )

    print(f"  Status: {result.status}")
    print()


def example_5_build_flow_only():
    """
    SCENARIO: Build and save the PAD flow definition without
    executing it — useful for review, export, or manual tweaking.
    """
    print("=" * 60)
    print("Example 5: Build Flow Only (No Execution)")
    print("=" * 60)

    pad = PADFramework()
    handler = ExcelPopupHandler(pad)

    popup = PopupDescriptor(
        window_title="Approval Required",
        fields=[
            PopupField("Approver", "manager@company.com",
                        element_name="txtApprover"),
            PopupField("Comments", "Auto-approved by RPA",
                        element_name="txtComments"),
        ],
        submit_button="Approve",
    )

    flow_def = handler.build_flow_only(
        file_path=r"C:\HR\leave_requests.xlsm",
        macro_name="ShowApprovalForm",
        popups=[popup],
    )

    print(f"  Flow name: {flow_def['name']}")
    print(f"  Actions: {len(flow_def['actions'])}")
    print(f"  Description: {flow_def['description']}")
    print()


def example_6_via_integration_manager():
    """
    SCENARIO: Use the integration manager interface instead of
    directly instantiating ExcelPopupHandler.
    """
    print("=" * 60)
    print("Example 6: Via Integration Manager")
    print("=" * 60)

    pad = PADFramework()

    info = pad.integrate("excel")
    print(f"  Capabilities: {info['capabilities']}")
    print(f"  Templates: {info['templates']}")
    print()

    popup = PopupDescriptor(
        window_title="Enter Password",
        fields=[PopupField("Password", "secret123", element_name="txtPwd")],
        submit_button="OK",
    )

    result = pad.integrate(
        "excel",
        operation="open_and_handle",
        file_path=r"C:\Secure\protected_workbook.xlsm",
        macro_name="RequestPassword",
        popups=[popup],
    )

    print(f"  Status: {result.status}")
    print()


def example_7_handle_standard_dialogs():
    """
    SCENARIO: Handle standard Excel dialogs — macro security
    warning, read-only prompt, Save As dialog.
    """
    print("=" * 60)
    print("Example 7: Standard Excel Dialogs")
    print("=" * 60)

    pad = PADFramework()
    handler = ExcelPopupHandler(pad)

    security = ExcelPopupTemplates.macro_security_prompt()
    read_only = ExcelPopupTemplates.read_only_prompt(submit_button="No")
    save_as = ExcelPopupTemplates.save_as_dialog(
        file_path=r"C:\Output\report_final.xlsx"
    )

    result = handler.open_and_handle_popup(
        file_path=r"C:\Templates\quarterly_report.xlsm",
        macro_name="GenerateReport",
        popups=[security, read_only, save_as],
        enable_macros=True,
        save_after=False,
        close_after=True,
    )

    print(f"  Status: {result.status}")
    print()


def main():
    """Run all examples."""
    print()
    print("*" * 60)
    print("  Excel Popup Handling — PAD Framework Examples")
    print("*" * 60)
    print()

    examples = [
        example_1_single_macro_popup,
        example_2_auto_popup_on_open,
        example_3_multiple_sequential_popups,
        example_4_using_templates,
        example_5_build_flow_only,
        example_6_via_integration_manager,
        example_7_handle_standard_dialogs,
    ]

    for fn in examples:
        try:
            fn()
        except Exception as exc:
            print(f"  [Example failed — expected without PAD runtime] {exc}")
            print()

    print("=" * 60)
    print("All examples completed.")
    print("=" * 60)


if __name__ == "__main__":
    main()
