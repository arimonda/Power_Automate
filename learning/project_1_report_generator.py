"""
PROJECT 1: Automated Report Generator
Build a system that generates and sends reports automatically

REQUIREMENTS:
- Schedule daily execution
- Extract data from database
- Generate Excel report
- Send email with report attached
- Log all operations

YOUR TASK: Complete the TODOs below
"""

from pad_framework import PADFramework
from datetime import datetime

class ReportGenerator:
    """Automated report generation system"""
    
    def __init__(self):
        self.pad = PADFramework()
        print("✓ Report Generator initialized")
    
    def generate_daily_report(self, report_date=None):
        """Generate daily report"""
        
        if not report_date:
            report_date = datetime.now().strftime("%Y-%m-%d")
        
        print(f"\n{'='*60}")
        print(f"GENERATING REPORT FOR {report_date}")
        print(f"{'='*60}\n")
        
        try:
            # TODO 1: Extract data from database
            print("Step 1: Extracting data...")
            data = self._extract_data(report_date)
            print(f"✓ Extracted {data['records']} records\n")
            
            # TODO 2: Generate Excel report
            print("Step 2: Generating Excel report...")
            report_file = self._generate_excel(data, report_date)
            print(f"✓ Report saved: {report_file}\n")
            
            # TODO 3: Send email with attachment
            print("Step 3: Sending email...")
            self._send_email(report_file, report_date)
            print(f"✓ Email sent\n")
            
            # TODO 4: Log success
            self.pad.logger.info(f"Report generated successfully: {report_date}")
            
            print(f"{'='*60}")
            print("✓ REPORT GENERATION COMPLETED")
            print(f"{'='*60}\n")
            
            return True
            
        except Exception as e:
            self.pad.logger.error(f"Report generation failed: {str(e)}")
            print(f"✗ Error: {str(e)}")
            return False
    
    def _extract_data(self, report_date):
        """TODO: Implement data extraction"""
        # Hint: Use pad.integrate("database")
        
        # PLACEHOLDER: Replace with real database query
        return {
            "date": report_date,
            "records": 250,
            "data": []  # Your data here
        }
    
    def _generate_excel(self, data, report_date):
        """TODO: Implement Excel generation"""
        # Hint: Use openpyxl or pandas
        
        # PLACEHOLDER: Replace with real Excel generation
        report_file = f"reports/daily_report_{report_date}.xlsx"
        print(f"  Creating {report_file}...")
        return report_file
    
    def _send_email(self, report_file, report_date):
        """TODO: Implement email sending"""
        # Hint: Use pad.integrate("email")
        
        # PLACEHOLDER: Replace with real email sending
        email_info = {
            "to": "manager@company.com",
            "subject": f"Daily Report - {report_date}",
            "body": f"Please find attached the daily report for {report_date}",
            "attachment": report_file
        }
        print(f"  Email configured: {email_info['to']}")
        return True
    
    def schedule_reports(self, schedule="0 8 * * *"):
        """Schedule daily report generation"""
        
        print(f"\n{'='*60}")
        print("SCHEDULING DAILY REPORTS")
        print(f"{'='*60}\n")
        
        # TODO 5: Implement scheduling
        print(f"Schedule: {schedule} (Daily at 8 AM)")
        
        schedule_id = self.pad.schedule_flow(
            flow_name="DailyReportGenerator",
            schedule=schedule,
            input_variables={"auto_generated": True}
        )
        
        print(f"✓ Report generation scheduled")
        print(f"  Schedule ID: {schedule_id}")
        print(f"  Next run: Tomorrow at 8:00 AM\n")
        
        return schedule_id


def main():
    """Main execution"""
    
    print("\n" + "="*60)
    print("PROJECT 1: Automated Report Generator")
    print("="*60)
    print()
    print("This project demonstrates:")
    print("  • Data extraction")
    print("  • Report generation")
    print("  • Email automation")
    print("  • Scheduling")
    print()
    
    # Create generator
    generator = ReportGenerator()
    
    # Generate today's report
    success = generator.generate_daily_report()
    
    if success:
        # Schedule for daily execution
        schedule_id = generator.schedule_reports()
        print(f"✓ Project setup completed!")
        print(f"\nSchedule ID: {schedule_id}")
        print("Reports will be generated automatically!")
    else:
        print("✗ Setup failed!")
    
    print()
    print("="*60)
    print("\n🎯 YOUR TASKS:")
    print("  1. Implement _extract_data() with real database")
    print("  2. Implement _generate_excel() to create Excel file")
    print("  3. Implement _send_email() with email integration")
    print("  4. Add error handling and retry logic")
    print("  5. Add report validation before sending")
    print()
    print("💡 HINTS:")
    print("  • Use pad.integrate('database') for data")
    print("  • Use openpyxl or pandas for Excel")
    print("  • Use pad.integrate('email') for sending")
    print("  • Check logs/ folder for execution logs")
    print()


if __name__ == "__main__":
    main()
