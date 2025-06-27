from abstract_base import BaseAnalysis
from DataVisualization.logic.data_processor import DataProcessor
from DataVisualization.logic.report_generator import ReportGenerator
import pandas as pd

class Analysis(BaseAnalysis): 

    def __init__(self):
        # logic for dataset load into dataframe
        filename = './online_retail_II.xlsx.xlsx'
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
        
         
    def _get_user_choice(self):
        print("--------------------------------")
        dp = DataProcessor(self.df)
        flag = True
        while flag:
            print("\nSelect option from the list:")
            print("1. Level 1 analysis")
            print("2. Level 2 analysis")
            print("3. Level 3 analysis")
            print("Use 4, 'q' or 'exit' to quit")
            option = input("Select option - 1, 2, 3 or 4")
            match option:
                case "1":
                    report_data = dp._handle_level_1(self.final_count) 
                    rg = ReportGenerator()
                    rg.generate_level_1_report(report_data, "Level1_Report.pdf")  

                case "2":
                    # _handle_level_2()
                    pass
                case "3":
                    # _handle_level_3()
                    pass
                case "4":
                    print("Thank you for using Report Generator. Goodbye!")
                    print("---------------------------------------------")
                    flag=False
                case _:
                    print("❌ Invalid choice. Please select an option: 1, 2, 3 or 4\n")


    def run_analysis(self):
        print("💰 Welcome to Report Generator 💰", end="\n")
        self._get_user_choice()
        


            
        