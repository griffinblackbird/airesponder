import pandas as pd
import os
from datetime import datetime
from main import similaritySearchAgent
from codeDoctor import fix_bug
from devOps import githubAgent
import uuid
import sys
from io import StringIO
import contextlib

class BugReportEntry:
    def __init__(self, csv_file="bug_reports.csv"):
        self.csv_file = csv_file
        self.initialize_csv()

    def initialize_csv(self):
        # Create the CSV file if it doesn't exist yet
        if not os.path.exists(self.csv_file):
            df = pd.DataFrame(columns=[
                'service_number',
                'timestamp',
                'customer_name',
                'customer_email',
                'bug_description',
                'device_info',
                'priority'
            ])
            df.to_csv(self.csv_file, index=False)
            print(f"Created new bug reports database: {self.csv_file}")
        else:
            # Make sure the priority column exists in existing files
            df = pd.read_csv(self.csv_file)
            if 'priority' not in df.columns:
                df['priority'] = ''
                df.to_csv(self.csv_file, index=False)
                print("Added priority column to existing bug_reports.csv")

    def generate_service_number(self):
        # Create a unique service number with date and random ID
        date_str = datetime.now().strftime("%Y%m%d")
        unique_id = str(uuid.uuid4())[:8].upper()
        return f"SR-{date_str}-{unique_id}"

    def file_new_bug(self):
        print("\n=== File New Bug Report ===")

        # Get a unique service number for this bug
        service_number = self.generate_service_number()
        print(f"Service Number: {service_number}")

        # Collect bug information from the user
        bug_data = {
            'service_number': service_number,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'customer_name': input("Customer Name: ").strip(),
            'customer_email': input("Customer Email: ").strip(),
            'bug_description': input("Bug Description: ").strip(),
            'device_info': input("Device/OS: ").strip(),
            'priority': ''  # We'll fill this after AI analysis
        }

        # Add the bug report to our database
        df = pd.read_csv(self.csv_file)
        new_row = pd.DataFrame([bug_data])
        df = pd.concat([df, new_row], ignore_index=True)

        print(f"\nBug report filed successfully!")
        print(f"Service Number: {service_number}")

        # Let the AI analyze the bug to find similar issues
        print("\nRunning AI similarity analysis...")
        search_query = f"Bug: {bug_data['bug_description']} on {bug_data['device_info']}"
        similarity_result = similaritySearchAgent(search_query)

        print("\nAI Analysis Results:")
        for key, value in similarity_result.items():
            print(f"{key}: {value}")

        # Parse the AI response to get priority and similarity info
        priority = ''
        similarity_status = ''

        # Convert AI response to text for parsing
        ai_response_text = str(similarity_result)

        # Look for priority information in the response
        if 'priority:' in ai_response_text.lower():
            parts = ai_response_text.lower().split('priority:')
            if len(parts) > 1:
                priority_part = parts[1].split(',')[0].strip()
                # Clean up any extra characters
                priority = priority_part.rstrip("',} ").strip()
                # Just take the first word (high/medium/low)
                priority = priority.split()[0] if priority else ''

        # Look for similarity status
        if 'similarity_status:' in ai_response_text.lower():
            parts = ai_response_text.lower().split('similarity_status:')
            if len(parts) > 1:
                similarity_part = parts[1].split(',')[0].strip()
                similarity_status = similarity_part

        # Update the priority in our database
        if priority:
            df.loc[df['service_number'] == service_number, 'priority'] = priority
            print(f"\nPriority '{priority}' extracted and assigned to bug report.")

        # Show similarity status if we found it
        if similarity_status:
            print(f"Similarity Status: {similarity_status}")

        # Save everything to the CSV file
        df.to_csv(self.csv_file, index=False)
        print(f"\nBug report with priority saved to CSV.")

        # Now handle the bug based on its priority
        if priority:
            priority_lower = priority.lower()
            if priority_lower == 'high':
                print("\nHIGH PRIORITY DETECTED: This bug has been staged for human review.")
                print("A developer will be assigned to review this issue manually.")

                # Ask if they still want to run Code Doctor even though it's high priority
                run_code_doctor = input("WARNING: High priority bugs may require careful manual review. Do you still want to run Code Doctor? (y/n): ").strip().lower()

                if run_code_doctor == 'y':
                    print(f"\nRunning Code Doctor for HIGH PRIORITY bug: {bug_data['bug_description']}")
                    print("=" * 50)
                    print("⚠️  WARNING: Automated fixes for high priority bugs should be carefully reviewed!")
                    try:
                        # Capture all output from Code Doctor
                        f = StringIO()
                        with contextlib.redirect_stdout(f):
                            fix_bug(bug_data['bug_description'])
                        code_doctor_output = f.getvalue()
                        print("CODE DOCTOR OUTPUT:", code_doctor_output)
                        print("=" * 50)
                        print("Code Doctor analysis completed for HIGH PRIORITY bug.")

                        # Send the fix to GitHub
                        print("\nPushing code changes to GitHub...")
                        print("=" * 50)
                        githubAgent(code_doctor_output)
                        print("=" * 50)
                        print("Code changes pushed to GitHub successfully!")
                        print("⚠️  IMPORTANT: Please manually review the automated changes pushed to GitHub!")

                    except Exception as e:
                        print(f"Error during automated fix or GitHub push: {str(e)}")
                else:
                    print("High priority bug will be handled by human review only.")
            elif priority_lower in ['medium', 'low']:
                print(f"\n{priority_lower.upper()} PRIORITY DETECTED")
                # Ask if they want to use Code Doctor for this bug
                run_code_doctor = input(f"Do you want to run Code Doctor to attempt fixing this {priority_lower} priority bug? (y/n): ").strip().lower()

                if run_code_doctor == 'y':
                    print(f"\nRunning Code Doctor for bug: {bug_data['bug_description']}")
                    print("=" * 50)
                    try:
                        # Capture Code Doctor output
                        f = StringIO()
                        with contextlib.redirect_stdout(f):
                            fix_bug(bug_data['bug_description'])
                        code_doctor_output = f.getvalue()
                        print("=" * 50)
                        print(f"Code Doctor analysis completed for {priority_lower} priority bug.")

                        # Send the fix to GitHub
                        print("\nPushing code changes to GitHub...")
                        print("=" * 50)
                        githubAgent(code_doctor_output)
                        print("=" * 50)
                        print("Code changes pushed to GitHub successfully!")

                    except Exception as e:
                        print(f"Error during automated fix or GitHub push: {str(e)}")
                else:
                    print("Code Doctor skipped. Bug will be handled manually if needed.")

        return service_number

def main():
    print("AI Responder - Customer Service Portal")

    portal = BugReportEntry()
    portal.file_new_bug()

    print("\nDone!")

if __name__ == "__main__":
    main()