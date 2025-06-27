
class DataProcessor:
    def __init__(self,df):
        self.df = df

    def _handle_level_1(self, final_count):
        
        # Add Description about the dataset
        data_desc = "This Online Retail II data set contains all the transactions occurring for a UK-based and registered, non-store online retail between 01/12/2009 and 09/12/2011.The company mainly sells unique all-occasion gift-ware. Many customers of the company are wholesalers."
        
        # Add table about column description
        data_columns = {
        "InvoiceNo" : "A 6-digit integral number uniquely assigned to each transaction. If this code starts with the letter 'C', it indicates a cancellation.",
        "StockCode": "A 5-digit integral number uniquely assigned to each distinct product.", 
        "Description" : "Product(item) name.",
        "Quantity" :"The quantities of each product(item) per transaction.",	
        "InvoiceDate" : "The day and time when a invoice was generated.", 
        "UnitPrice" : "Product price per unit in sterling (Â£).", 
        "CustomerID" : "A 5-digit integral number uniquely assigned to each customer.", 
        "Country" : "The name of the country where a customer resides."
        }

        # Add few important information dataset like type of each column
        data_types = {
        "InvoiceNo": "Text",
        "StockCode": "Text",
        "Description": "Text",
        "Quantity": "Numeric",
        "InvoiceDate": "Datetime",
        "UnitPrice": "Numeric",
        "CustomerID": "Numeric",
        "Country": "Text"
        }

        # Add 2 interesting fact about data
        num_countries = len(self.df['Country'].unique())

        data_analysis = {
            "interesting_fact1" : f"The dataset contains {final_count} cleaned transaction records spanning two years, after removing null CustomerIDs, cancellations, and zero-value rows.",
            "interesting_fact2" : f"There are {num_countries} unique countries in the dataset."
        }

        return {"description" : data_desc,
                "column_descriptions": data_columns,
                "data_types": data_types,
                "interesting_facts": data_analysis
                }


