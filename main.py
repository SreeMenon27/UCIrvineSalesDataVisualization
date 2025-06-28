from abstract_base import BaseAnalysis
from logic.data_processor import DataProcessor
from logic.report_generator import ReportGenerator
import pandas as pd
import sys
import os

class Analysis(BaseAnalysis): 

    def __init__(self):
        # logic for dataset load into dataframe
        filename = './online_retail_II.xlsx'
        try:                
            df_1 = pd.read_excel(filename,sheet_name="Year 2009-2010")
            df_2 = pd.read_excel(filename,sheet_name="Year 2010-2011")
            df = pd.concat([df_1,df_2], ignore_index=True)

            df.columns = df.columns.str.strip()
            # initial count of records
            self.initial_count = df['Invoice'].count()

            # Remove null values from customer id
            df = df.dropna(subset=['Customer ID'])
            
            # Remove cancelled entries from the dataframe
            df = df[~df['Invoice'].astype(str).str.startswith('C')]
            # Remove Quantity and Price with 0
            df = df[df['Quantity'] > 0]
            df = df[df['Price']>0]
            self.final_count = df['Invoice'].count() 
            self.df = df

             # Ensure assets folder exists
            os.makedirs("assets", exist_ok=True)

        except FileNotFoundError:
            print("❌ Error: Data file not found. Please check the filename and path.")
            sys.exit(1)
        except ValueError as ve:
            print(f"❌ Error: {ve}. Please verify sheet names or file content.")
            sys.exit(1)

        
         
    def _get_user_choice(self):
        print("--------------------------------")
        dp = DataProcessor(self.df)
        flag = True

        # Print the menu only once at the start
        print("\nSelect option from the list:")
        print("1. Level 1 analysis")
        print("2. Level 2 analysis")
        print("3. Level 3 analysis")
        print("Use 4, 'q' or 'exit' to quit")
        print("--------------------------------")

        while flag:
            option = input("Select option - 1, 2, 3 or 4: \n").strip().lower()
            print("--------------------------------")

            match option:
                case "1":
                    # Level 1 report generation
                    report_data = dp._handle_level_1(self.final_count) 
                    rg = ReportGenerator()
                    rg.generate_level_1_report(report_data, "assets/Level1_Report.pdf") 
                    print("✅ Level 1 PDF report generated successfully: Level1_Report.pdf\n")   
                    print("-----------------------------------------------------------------")                 
                case "2":
                    rg = ReportGenerator()
                    report_data_l1 = dp._handle_level_1(self.final_count)
                    report_data_l2 = dp._handle_level_2()
                    rg.generate_level_2_report(report_data_l1, report_data_l2, "assets/Level2_Report.pdf")
                    print("✅ Level 2 Report generated at assets/Level2_Report.pdf\n")
                case "3":
                    rg = ReportGenerator()
                    report_data_l1 = dp._handle_level_1(self.final_count)
                    report_data_l2 = dp._handle_level_2()
                    report_data_l3 = dp._handle_level_3()
                    rg.generate_level_3_report(report_data_l1, report_data_l2, report_data_l3, "assets/Level3_Report.pdf")

                    print("✅ Level 3 Report generated at assets/Level3_Report.pdf\n")
                case "4" | "q" | "exit":
                    print("Thank you for using Report Generator. Goodbye!")
                    print("---------------------------------------------")
                    flag = False
                case _:
                    print("❌ Invalid choice. Please select an option: 1, 2, 3 or 4\n")


    def run_analysis(self):
        print("💰 Welcome to Report Generator 💰", end="\n")
        self._get_user_choice()

if __name__ == "__main__":
        analysis = Analysis()
        analysis.run_analysis()
        


            
        