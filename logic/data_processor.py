import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="darkgrid")
#plt.style.use('dark_background')

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
    
    def _handle_level_2(self):
        # Add new features
        self.df['Revenue'] = self.df['Quantity'] * self.df['Price']
        self.df['InvoiceDate'] = pd.to_datetime(self.df['InvoiceDate'])


        # Plot 1 - Top 10 countries by sales revenue
        # ------------------------------------------
        country_revenue = self.df.groupby('Country')['Revenue'].sum().sort_values(ascending=False).head(10)
        # Convert Series to DataFrame
        country_df = country_revenue.reset_index().copy()
        country_df.columns = ['Country', 'Revenue']       

        # Bar plot
        plt.figure(figsize=(10, 6))
        palette = sns.color_palette('Oranges_d', n_colors=10)
        ax = sns.barplot(data=country_df, x='Country', y='Revenue', palette=palette, hue='Country', legend=False)
        # Add labels on top of bars
        for p in ax.patches:
            height = p.get_height()
            ax.annotate(f'{height:,.0f}',
                        (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='bottom', fontsize=8, color='black')

        plt.title("Top 10 Countries by Revenue")
        plt.xlabel("Country")
        plt.ylabel("Revenue")
        plt.xticks(rotation=45)
        plt.grid(axis='y')
        plt.tight_layout()  # Proper function call
        plt.savefig("assets/top_countries_revenue.png")
        plt.close()
    
        # Plot 2 - Sales trend over time
        # ------------------------------------------
        self.df['Month'] = self.df['InvoiceDate'].dt.to_period('M')
        monthly_revenue = self.df.groupby("Month")['Revenue'].sum()
        monthly_revenue.index = monthly_revenue.index.astype(str)

        # Set style before plotting
        # Get a color from a seaborn palette
        palette = sns.color_palette('Oranges_d')  # or 'Blues', 'Purples', etc.
        #line_color = palette[10]  # Pick the first color from the palette
        plt.figure(figsize=(12, 6))
        plt.plot(monthly_revenue.index, monthly_revenue.values, marker='o', linestyle='-', color='#e28743', label="Revenue")
        # Add data labels
        for x, y in zip(monthly_revenue.index, monthly_revenue.values):
            plt.text(x, y + 1000, f'{y:,.0f}', ha='center', va='bottom', fontsize=8, color='black')
        plt.xticks(rotation=45)
        plt.title('Monthly Revenue Over Time')
        plt.xlabel('Year-Month')
        plt.ylabel('Revenue')
        plt.grid(True)
        # Save file to assets folder
        plt.tight_layout()
        plt.savefig("assets/monthly_revenue_trend.png")
        plt.close()
 

        # Plot 3 - Top 10 products by quantity sold
        # ------------------------------------------
        product_quantity = self.df.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10)
        product_df = product_quantity.reset_index().copy()
        product_df.columns = ['Product', 'Quantity']
        product_df['Product'] = product_df['Product'].str.slice(0, 40) + '...'

        # Bar plot (horizontal for better label fit)
        plt.figure(figsize=(10, 6))
        palette = sns.color_palette('Oranges_d', n_colors=10)
        ax = sns.barplot(data=product_df, x='Quantity', y='Product', palette=palette, hue='Product', legend=False)
        # Add labels to end of bars
        for p in ax.patches:
            width = p.get_width()
            ax.annotate(f'{width:,.0f}',
                        (width + 10, p.get_y() + p.get_height() / 2),
                        ha='left', va='center', fontsize=8, color='black')

        # Title and labels
        plt.title("Top 10 Products by Quantity Sold")
        plt.xlabel("Quantity Sold")
        plt.ylabel("Product Description")

        # Optional: Adjust font size if product names are very long
        plt.yticks(fontsize=8)

        plt.tight_layout()
        plt.savefig("assets/top_products_quantity.png")
        plt.close()


        plots = {
            "country_revenue_plot": "assets/top_countries_revenue.png",
            "monthly_revenue_plot": "assets/monthly_revenue_trend.png",
            "product_quantity_plot": "assets/top_products_quantity.png"}
        
        return plots
    
    def _handle_level_3(self):
        if 'Revenue' not in self.df.columns:
            self.df['Revenue'] = self.df['Quantity'] * self.df['Price']

        os.makedirs("assets", exist_ok=True)
        plots = {}

        # 1. Correlation Heatmap
        corr_df = self.df[['Quantity', 'Price', 'Revenue']].corr()
        plt.figure(figsize=(8, 6))
        sns.heatmap(corr_df, annot=True, cmap='Oranges', fmt=".2f")
        plt.title("Correlation Matrix")
        plt.tight_layout()
        path1 = "assets/correlation_heatmap.png"
        plt.savefig(path1)
        plt.close()
        plots["correlation_matrix_plot"] = path1

        # 2. KDE plot of Revenue (filtered to remove outliers)
        revenue_filtered = self.df[self.df['Revenue'] < self.df['Revenue'].quantile(0.99)]

        plt.figure(figsize=(8, 5))
        sns.kdeplot(revenue_filtered['Revenue'], fill=True, color='#e28743', linewidth=1.5)
        plt.title("KDE Plot of Revenue (Filtered - Below 99th Percentile)")
        plt.xlabel("Revenue")
        plt.tight_layout()
        path2 = "assets/kde_revenue.png"
        plt.savefig(path2)
        plt.close()
        plots["revenue_kde_plot"] = path2

        # 3. Scatter Plot (Quantity vs Revenue) with filtering and size/color encoding
        scatter_df = self.df[(self.df['Quantity'] < self.df['Quantity'].quantile(0.99)) &
                            (self.df['Revenue'] < self.df['Revenue'].quantile(0.99))]

        plt.figure(figsize=(10, 6))
        sns.scatterplot(
            data=scatter_df,
            x="Quantity",
            y="Revenue",
            hue="Country",
            size="Revenue",
            sizes=(20, 200),
            alpha=0.6,
            palette="tab10",  # Or try "Set2", "Dark2" for variation
        )
        plt.title("Scatter Plot of Quantity vs Revenue (Filtered)")
        plt.xlabel("Quantity")
        plt.ylabel("Revenue")
        plt.legend(title="Country", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        path3 = "assets/scatter_quantity_revenue.png"
        plt.savefig(path3)
        plt.close()
        plots["scatter_quantity_revenue_plot"] = path3

        # 4. Boxplot of UnitPrice by Country (top 5 countries)
        top_countries = self.df['Country'].value_counts().head(5).index
        top_country_df = self.df[self.df['Country'].isin(top_countries)]

        plt.figure(figsize=(10, 6))
        palette = sns.color_palette("Oranges_d", n_colors=5)  # Match number of countries
        sns.boxplot(
            data=top_country_df,
            x="Country",
            y="Price",
            hue="Country",            # <-- This is the fix!
            palette=palette,
            legend=False
        )
        plt.title("Boxplot of Unit Price by Top 5 Countries")
        plt.xlabel("Country")
        plt.ylabel("Unit Price")
        plt.tight_layout()
        path4 = "assets/boxplot_unitprice_country.png"
        plt.savefig(path4)
        plt.close()
        plots["price_boxplot_plot"] = path4

        return plots




