import pandas as pd
import os
from datetime import datetime
from main import similaritySearch, ensureSeverityColumn, updateSeverityScore
import uuid

class BugReportEntry:
    def __init__(self, csv_file="bug_reports.csv"):
        self.csv_file = csv_file
        self.initialize_csv()

    def initialize_csv(self):
        if not os.path.exists(self.csv_file):
            df = pd.DataFrame(columns=[
                'service_number',
                'timestamp',
                'customer_name',
                'customer_email',
                'bug_description',
                'os_info',
                'similarity_check_result',
                'severity_score'
            ])
            df.to_csv(self.csv_file, index=False)
            print(f"Created new bug reports database: {self.csv_file}")
        else:
            # Ensure severity_score column exists in existing CSV
            ensureSeverityColumn()
            # Replace 'nan' strings with actual NaN values for consistency
            df = pd.read_csv(self.csv_file, na_values=['nan'])
            df.to_csv(self.csv_file, index=False)

    def generate_service_number(self):
        date_str = datetime.now().strftime("%Y%m%d")
        unique_id = str(uuid.uuid4())[:8].upper()
        return f"SR-{date_str}-{unique_id}"

    def file_new_bug(self):
        print("\n=== File New Bug Report ===")

        service_number = self.generate_service_number()
        print(f"Service Number: {service_number}")

        bug_data = {
            'service_number': service_number,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'customer_name': input("Customer Name: ").strip(),
            'customer_email': input("Customer Email: ").strip(),
            'bug_description': input("Bug Description (in natural language): ").strip(),
            'os_info': input("OS/Environment (e.g., Windows 11, macOS Sonoma): ").strip(),
            'similarity_check_result': 'Pending',
            'severity_score': None  # Use None instead of empty string
        }

        df = pd.read_csv(self.csv_file)
        new_row = pd.DataFrame([bug_data])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(self.csv_file, index=False)

        print(f"\nBug report filed successfully!")
        print(f"Service Number: {service_number}")

        return service_number

    def run_similarity_search(self, service_number):
        try:
            # Read CSV once
            df = pd.read_csv(self.csv_file, na_values=['nan', 'NaN', ''])
            print(f"📊 Loaded CSV with {len(df)} rows")

            bug_row = df[df['service_number'] == service_number]
            if bug_row.empty:
                print(f"❌ Bug report {service_number} not found!")
                return

            bug_row = bug_row.iloc[0]
            print(f"\nRunning similarity search for Service Number: {service_number}")

            # Check current values before search
            current_severity = df.loc[df['service_number'] == service_number, 'severity_score'].iloc[0]
            current_status = df.loc[df['service_number'] == service_number, 'similarity_check_result'].iloc[0]
            print(f"📊 Current severity_score: '{current_severity}' (type: {type(current_severity)})")
            print(f"📊 Current similarity_check_result: '{current_status}'")

            search_query = f"Bug: {bug_row['bug_description']} on {bug_row['os_info']}"
            print(f"🔍 Search query: {search_query}")

            print("\nAI Similarity Search Results:")
            priority = similaritySearch(search_query)
            print(f"🎯 AI returned priority: {priority}")

            # Update both columns in a single operation
            df.loc[df['service_number'] == service_number, ['severity_score', 'similarity_check_result']] = [priority, 'Completed']
            df.to_csv(self.csv_file, index=False)
            print("✅ Both columns updated successfully")

            # Verify the updates
            df_final = pd.read_csv(self.csv_file, na_values=['nan', 'NaN', ''])
            final_severity = df_final.loc[df_final['service_number'] == service_number, 'severity_score'].iloc[0]
            final_status = df_final.loc[df_final['service_number'] == service_number, 'similarity_check_result'].iloc[0]
            print(f"📋 Final severity_score: '{final_severity}'")
            print(f"📋 Final similarity_check_result: '{final_status}'")

            if pd.isna(current_severity) and not pd.isna(final_severity) and final_severity != '':
                print("✅ SUCCESS: Severity score was updated from empty to:", final_severity)
            elif not pd.isna(final_severity):
                print("✅ Severity score is present:", final_severity)
            else:
                print("⚠️ WARNING: Severity score is still empty or NaN")

            if current_status == 'Pending' and final_status == 'Completed':
                print("✅ SUCCESS: Similarity check was updated from Pending to Completed")
            else:
                print("✅ Similarity check is:", final_status)

        except Exception as e:
            print(f"❌ Error running similarity search: {str(e)}")
            import traceback
            traceback.print_exc()

def main():
    print("AI Responder 360 - Customer Service Portal")

    portal = BugReportEntry()

    service_number = portal.file_new_bug()

    search_now = input("\nRun similarity search now? (y/n): ").strip().lower()
    if search_now == 'y':
        portal.run_similarity_search(service_number)

    print("\nDone!")

if __name__ == "__main__":
    main()