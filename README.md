# Where does Hearing Difficulty and Language Barriers Overlap Among 65+ Adults in King County

Setup:
* Python 3 with libraries pandas, geopandas, seaborn, matplotlib, scipy, requests, and dotenv (if want to refetch ACS data)
* Unzip the data folder into the project's root folder. It contains the 2020-2024 ACS 5-year CSVs for tables B16004 and B18102, and the TIGER/Line 2024 Washington tract shapefile.

Python Files:
* main.py: runs whole project in order
* download_acs.py: fetches ACS tables from Census API and saves them as CSVs
* clean_data.py: removes missing data and creates the columns needed with the data for analysis
* test_data.py: asserts that there are no negative codes, 482 unique tracts with 11-digit GEOIDs are there, percentages are between 0 and 100, and every tract matches a corresponding TIGER tract
* create_plots.py: Creates the plots needed for the EDA
* test_cleaned_data.py: tests if the calculations done for the created columns were correct
* validity.py: checks the statistical validity of the data.

How to run:
1. Unzip the data files into project root folder
2. Run python main.py. It uses the saved CSVs, does not refetch the data with the API key.

If you want to refetch the data:
1. Get a free key at https://api.census.gov/data/key_signup.html
2. Save it in an .env file, with variable name CENSUS_API_KEY={insert your key}
3. Run python download_acs.py
