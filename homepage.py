# import module
import streamlit as st
import pandas as pd
from ScrapeShopee import ScrapeData 


st.set_page_config(page_title = 'Shopee Web Scraping')
# Title
st.title("Shopee Web Scraping")

# Text Input
# save the input text in the variable 'name'
# first argument shows the title of the text input box
# second argument displays a default text inside the text input area
product_name = st.text_input("Enter product name")
num = st.number_input('No of data', min_value=10, max_value=540) 

# display the name when the submit button is clicked
# .title() is used to get the input text string
if(st.button('Submit')):
	product_name_string = product_name.title() # get user input
	
	if product_name != "":
		scraper = ScrapeData() # Initialize ScrapeData class object
		scraper.main(product_name_string, num) # pass the product name and run the main funtion
		st.success("Scraping Successful")
	else:
		st.error("Please Enter Product Name!")

# Downloading functionality
try:
	df = pd.read_csv("ShopeeData.csv")

	@st.experimental_memo
	def convert_df(df):
		return df.to_csv(index=False).encode('utf-8')

	csv_file = convert_df(df)

	st.download_button(
		label = "Download", 
		data = csv_file, 
		file_name='ShopeeData.csv', 
		mime="text/csv", 
		key='download-csv'
	)
except:
	st.button(label='Download', disabled=True)
