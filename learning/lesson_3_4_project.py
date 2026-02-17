"""
Lesson 3.4: Complete Solution - Data Processing Pipeline
Build a real-world data processing pipeline
"""

from pad_framework import PADFramework
import time
from datetime import datetime

class DataPipeline:
    """Complete data processing pipeline example"""
    
    def __init__(self):
        self.pad = PADFramework()
        self.results = []
        self.start_time = None
        self.end_time = None
    
    def run_pipeline(self, data_file):
        """Run complete data processing pipeline"""
        
        self.start_time = datetime.now()
        
        print("="*60)
        print("DATA PROCESSING PIPELINE")
        print("="*60)
        print(f"Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        try:
            # Step 1: Validate
            if not self._validate_flows():
                return False
            
            # Step 2: Extract
            if not self._extract_data(data_file):
                return False
            
            # Step 3: Transform
            if not self._transform_data():
                return False
            
            # Step 4: Load
            if not self._load_data():
                return False
            
            # Step 5: Report
            self._generate_report()
            
            self.end_time = datetime.now()
            duration = (self.end_time - self.start_time).total_seconds()
            
            print("="*60)
            print("✓ PIPELINE COMPLETED SUCCESSFULLY!")
            print(f"Total Duration: {duration:.2f} seconds")
            print("="*60)
            
            return True
            
        except Exception as e:
            print(f"\n✗ Pipeline failed: {str(e)}")
            return False
    
    def _validate_flows(self):
        """Step 1: Validate all required flows"""
        print("Step 1: Validating flows...")
        print("-"*40)
        
        flows = ["ExampleFlow"]  # Add your required flows
        
        for flow in flows:
            print(f"  Validating {flow}...", end=" ")
            validation = self.pad.validate_flow(flow)
            
            if validation["valid"]:
                print("✓")
            else:
                print("✗")
                print(f"    Errors: {validation['errors']}")
                return False
        
        print("✓ All flows validated\n")
        return True
    
    def _extract_data(self, data_file):
        """Step 2: Extract data from source"""
        print("Step 2: Extracting data...")
        print("-"*40)
        print(f"  Source: {data_file}")
        
        # Simulate data extraction
        time.sleep(0.5)
        
        extracted_data = {
            "records": 150,
            "columns": ["ID", "Name", "Value"],
            "status": "extracted"
        }
        
        self.results.append(("extract", extracted_data))
        
        print(f"  ✓ Extracted {extracted_data['records']} records")
        print(f"  Columns: {', '.join(extracted_data['columns'])}\n")
        
        return True
    
    def _transform_data(self):
        """Step 3: Transform extracted data"""
        print("Step 3: Transforming data...")
        print("-"*40)
        
        extract_result = self.results[-1][1]
        print(f"  Processing {extract_result['records']} records...")
        
        # Simulate data transformation
        time.sleep(0.5)
        
        transformed_data = {
            "records": extract_result['records'],
            "status": "transformed",
            "transformations": ["cleaned", "validated", "enriched"]
        }
        
        self.results.append(("transform", transformed_data))
        
        print(f"  ✓ Applied {len(transformed_data['transformations'])} transformations")
        print(f"    - {', '.join(transformed_data['transformations'])}\n")
        
        return True
    
    def _load_data(self):
        """Step 4: Load data to destination"""
        print("Step 4: Loading data...")
        print("-"*40)
        
        transform_result = self.results[-1][1]
        print(f"  Loading {transform_result['records']} records...")
        
        # Simulate data loading
        time.sleep(0.5)
        
        loaded_data = {
            "records": transform_result['records'],
            "destination": "database",
            "status": "loaded"
        }
        
        self.results.append(("load", loaded_data))
        
        print(f"  ✓ Loaded to {loaded_data['destination']}")
        print(f"  Records: {loaded_data['records']}\n")
        
        return True
    
    def _generate_report(self):
        """Step 5: Generate execution report"""
        print("Step 5: Generating report...")
        print("-"*40)
        
        print("\n  PIPELINE EXECUTION REPORT")
        print("  " + "-"*38)
        
        for step_name, step_data in self.results:
            print(f"  {step_name.upper():12} : {step_data['status'].upper()}")
        
        print(f"\n  Total Steps   : {len(self.results)}")
        print(f"  Records       : {self.results[-1][1]['records']}")
        
        # Performance stats
        stats = self.pad.get_performance_stats()
        if stats:
            print(f"  Flows Used    : {len(stats)}")
        
        print()


def main():
    """Main execution function"""
    
    print("\n" + "="*60)
    print("LESSON 3.4: Building a Complete Solution")
    print("="*60)
    print()
    
    # Create and run pipeline
    pipeline = DataPipeline()
    success = pipeline.run_pipeline("data/input.xlsx")
    
    if success:
        print("\n✓ Project completed successfully!")
        print("\n💡 You've built a complete data processing pipeline!")
    else:
        print("\n✗ Project failed!")
        print("Review the errors above and try again.")
    
    print()
    print("="*60)
    print("\n💡 WHAT YOU LEARNED:")
    print("  ✓ Building multi-step workflows")
    print("  ✓ Error handling in pipelines")
    print("  ✓ Data processing patterns")
    print("  ✓ Result tracking")
    print("  ✓ Report generation")
    print()
    
    print("🎯 NEXT STEPS:")
    print("  1. Add real flow executions")
    print("  2. Add error recovery")
    print("  3. Add email notifications")
    print("  4. Add scheduling")
    print()


if __name__ == "__main__":
    main()
