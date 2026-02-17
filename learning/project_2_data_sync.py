"""
PROJECT 2: Data Sync Tool
Synchronize records between two systems with validation and retry.

REQUIREMENTS:
- Read records from source system
- Validate and transform records
- Write records to destination system
- Track sync status and failures
- Support retry for transient errors

YOUR TASK: Complete and customize TODO sections.
"""

from datetime import datetime

from pad_framework import PADFramework


class DataSyncTool:
    """Template for a source-to-destination data sync process."""

    def __init__(self):
        self.pad = PADFramework()
        self.sync_id = f"sync-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        print(f"✓ Data Sync Tool initialized (ID: {self.sync_id})")

    def run(self):
        """Run a full synchronization cycle."""
        print("\n" + "=" * 60)
        print("PROJECT 2: DATA SYNC")
        print("=" * 60)

        try:
            source_records = self._read_source()
            clean_records = self._validate_and_transform(source_records)
            result = self._write_destination(clean_records)
            self._log_summary(source_records, clean_records, result)
            print("\n✓ Data sync completed successfully")
            return True
        except Exception as exc:
            self.pad.logger.error(f"Data sync failed: {exc}", sync_id=self.sync_id)
            print(f"\n✗ Data sync failed: {exc}")
            return False

    def _read_source(self):
        """TODO: Replace with real source read logic."""
        print("\nStep 1: Reading source records...")
        # Example placeholder data
        records = [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"},
            {"id": None, "name": "Invalid", "email": "invalid-email"},
        ]
        print(f"  Loaded {len(records)} record(s)")
        return records

    def _validate_and_transform(self, records):
        """TODO: Add robust validation and transformation rules."""
        print("\nStep 2: Validating and transforming records...")
        valid = []
        skipped = 0

        for row in records:
            # Basic validation template
            if not row.get("id") or "@" not in row.get("email", ""):
                skipped += 1
                continue

            transformed = {
                "external_id": row["id"],
                "full_name": row["name"].strip(),
                "email": row["email"].lower(),
                "synced_at": datetime.now().isoformat(),
            }
            valid.append(transformed)

        print(f"  Valid records: {len(valid)}")
        print(f"  Skipped records: {skipped}")
        return valid

    def _write_destination(self, records):
        """TODO: Replace with destination write (API/database)."""
        print("\nStep 3: Writing destination records...")
        # Placeholder: replace with pad.integrate("api"/"database", ...)
        written = len(records)
        failed = 0
        print(f"  Written: {written}")
        print(f"  Failed: {failed}")
        return {"written": written, "failed": failed}

    def _log_summary(self, source_records, clean_records, write_result):
        """Log sync metrics for troubleshooting."""
        summary = {
            "sync_id": self.sync_id,
            "source_count": len(source_records),
            "validated_count": len(clean_records),
            "written_count": write_result["written"],
            "failed_count": write_result["failed"],
        }
        self.pad.logger.info("Data sync summary", **summary)
        print("\nSummary:")
        for key, value in summary.items():
            print(f"  {key}: {value}")


def main():
    tool = DataSyncTool()
    success = tool.run()

    print("\n" + "=" * 60)
    print("🎯 YOUR TASKS:")
    print("1. Replace source read logic with a real integration")
    print("2. Add field mapping from source schema to destination schema")
    print("3. Add retry logic for failed destination writes")
    print("4. Save failed rows to a quarantine file for reprocessing")
    print("5. Add scheduling for nightly sync")
    print("=" * 60)

    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
