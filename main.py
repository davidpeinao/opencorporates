import logging, configparser, sys, json, requests, os.path, pandas as pd, csv
from datetime import datetime
from db_manager import insert_row, create_db, connect_to_db, close_connection

def build_url(company_name: str, API_KEY: str, API_VERSION: str) -> str:
    """Builds the URL that contains the query to search for the companies

    Args:
        company_name (str): The company or companies we are looking for
        API_KEY (str): The API key needed to invoke the API
        API_VERSION (str): The API version

    Returns:
        str: The URL that will be used to invoke the API
    """
    url = f"https://api.opencorporates.com/{API_VERSION}/companies" \
          f"/search?q={company_name}&fields=name" \
          f"&api_token={API_KEY}&per_page=100"
    return url

def search(company_name: str, API_KEY: str, 
           API_VERSION: str="v0.4") -> pd.DataFrame:
    """Builds the URL to make the API call, performs a check, then gets
    the number of companies matching the criteria

    Args:
        company_name (str): The company or companies we are looking for
        API_KEY (str): The API key needed to invoke the API
        API_VERSION (str, optional): The API version. Defaults to "v0.4".

    Returns:
        pd.DataFrame: The API call results in a table format
    """
    url = build_url(company_name, API_KEY, API_VERSION)
    response = requests.get(url)
    results = pd.DataFrame() 

    if response.status_code == 200:
        num_companies = json.loads(response.text)["results"]["total_count"]
        num_pages = int(json.loads(response.text)["results"]["total_pages"])
        
        logging.info(f"We have {num_companies} results!")
        results = get_results(url,num_pages)
    elif response.status_code == 403:
        logging.critical(f"Response code: {response.status_code}"
                     f" - {response.reason}. We are not properly authenticated" 
                     f" or we have exceeded the API rate limits")
        sys.exit()
    else:
        logging.error(f"Response code: {response.status_code}"
                     f" - {response.reason}")

    return results

def get_results(url: str, num_pages: int) -> pd.DataFrame:
    """Retrieves the details of all the companies that matched the criteria,
    iterating through the results pages

    Args:
        url (str): The base URL that will be used to retrieve the results
        num_pages (int): The number of pages of the resulting query

    Returns:
        pd.DataFrame: The details of the companies that matched the criteria
    """

    results = pd.DataFrame() 
    # Fecthing only the first 10000 companies (first 10 result pages)
    # for i in range(num_pages):
    for i in range(100):
        url += f"&page={i+1}"
        response = requests.get(url)
        companies = json.loads(response.text)["results"]["companies"]
        for company in companies:
            dfItem = pd.json_normalize(company["company"])
            results = results.append(dfItem) 
        logging.info(f"Retrieved the first {(i+1)*100} results...")

    return results

def upload_csv_to_db():
    """First it checks if the database exists, if it doesn't it will be created 
    along with the table that will store the companies' data. 
    Then it will upload every row of the csv file to that table
    """
    if not os.path.exists(DB_FILENAME):
        create_db()

    logging.info(f"Now uploading the csv file to the database")

    with open(CSV_FILENAME, "r", encoding='utf-8') as results:
        n_records = 0
        lines = csv.reader(results)
        next(lines, None)

        connection = connect_to_db()
        for line in lines:
            insert_row(line, connection)
            n_records += 1
            
        close_connection(connection)
        logging.info(f"{n_records} rows inserted in the table")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s — %(levelname)s: %(message)s")

    config = configparser.ConfigParser()
    config.read("config.ini")
    API_KEY = config["opencorporates"]["API_KEY"]
    API_VERSION = config["opencorporates"]["API_VERSION"]
    COMPANY_NAME = config["opencorporates"]["COMPANY_NAME"]
    CSV_FILENAME = config["opencorporates"]["CSV_FILENAME"]
    DB_FILENAME = config["opencorporates"]["DB_FILENAME"]

    logging.info(f"Searching for the list of companies that " \
                 f"have the word “{COMPANY_NAME}” in their name")
    
    results = search(COMPANY_NAME,API_KEY,API_VERSION)
    results = results.drop(["industry_codes","previous_names"], axis=1)

    logging.info(f"Storing the results in the csv file")
    results.to_csv(CSV_FILENAME, index = False)
    logging.info(f"Finished storing the results in the csv file")

    upload_csv_to_db()
