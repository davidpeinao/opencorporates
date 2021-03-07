import sqlite3, configparser, logging

logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s — %(levelname)s: %(message)s")
config = configparser.ConfigParser()
config.read("config.ini")
TABLE_NAME = config["opencorporates"]["TABLE_NAME"] 
DB_FILENAME = config["opencorporates"]["DB_FILENAME"]

def connect_to_db() -> sqlite3.Connection:
    connection = sqlite3.connect("database.db")
    return connection

def close_connection(connection: sqlite3.Connection):
    connection.close()


def insert_row(row: list, connection: sqlite3.Connection): 
    """Inserts a row in the table

    Args:
        row (list): The list of values to be inserted in the row
        connection ([sqlite3.Connection]): The connection to the database
    """
    cursor = connection.cursor()
    values = "?" + ",?"*(len(row)-1)
    sql = f"INSERT INTO {TABLE_NAME} VALUES ({values})"
    cursor.execute(sql, row)
    connection.commit()


def create_db():
    """Creates the sqlite3 database file and creates the table that we
    are going to be using to store the results from the csv file.

    This table's schema has been created choosing all the columns from our
    csv file except 'industry_codes' and 'previous_names' (which could be 
    stored in separate tables and be linked to the main one, creating a star 
    schema)
    """

    connection = sqlite3.connect(DB_FILENAME)
    cursor = connection.cursor()
    logging.info(f"We didn't have a database yet! So it has been created")

    sql = f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            name TEXT,
            company_number TEXT,
            jurisdiction_code TEXT,
            incorporation_date TEXT,
            dissolution_date TEXT,
            company_type TEXT,
            registry_url TEXT,
            branch TEXT,
            branch_status TEXT,
            inactive TEXT,
            current_status TEXT,
            created_at TEXT,
            updated_at TEXT,
            retrieved_at TEXT,
            opencorporates_url TEXT,
            registered_address_in_full TEXT,
            restricted_for_marketing TEXT,
            native_company_number TEXT,
            source_publisher TEXT,
            source_url TEXT,
            source_retrieved_at TEXT,
            registered_address_street_address TEXT,
            registered_address_locality TEXT,
            registered_address_region TEXT,
            registered_address_postal_code TEXT,
            registered_address_country TEXT,
            registered_address TEXT,
            source_terms TEXT,
            source_terms_url TEXT
        ) """

    cursor.execute(sql)
    logging.info(f"The table '{TABLE_NAME}' has been created")

    connection.commit()
    connection.close()