import logging
import sys
import os
import requests
import re

# id_array
ids = []
# Create a custom logger
logger = logging.getLogger("http_server")

def set_logger():
    try:
        logger.setLevel(logging.DEBUG)  # This needs to be DEBUG to capture all levels of logs
        # Create handlers
        c_handler = logging.StreamHandler()
        c_handler.setLevel(logging.DEBUG)  # Set to DEBUG to ensure all levels are logged to console
        # Add handlers to the logger
        logger.addHandler(c_handler)
    except Exception as e:
        print(f"Failed to configure logging: {e}")
        sys.exit(1)

def get_content(url):

    # Perform a GET request to the URL
    response = requests.get(url)

    if response.status_code == 200:
        return response.text
    else:
        logger.info("Failed to retrieve the webpage.")
        logger.info("all tasks failed")
        sys.exit(1)
    
def get_new_filename():

    folder_path = os.path.dirname(os.path.abspath(__file__))
    folder_path +=  "/tmp"

    id=1
    web_page_name = f"web_page{id}.html"

    # list all webpage name in folder tmp
    entries = os.listdir(folder_path)
    logger.info(f"{entries} already exists")

    # check available id in ids already used
    while web_page_name in entries:
        id+=1
        web_page_name = f"web_page{id}.html"
    
    logger.info(f"{web_page_name} will be created at {folder_path}")

    # return a new web page name
    return f"{folder_path}/{web_page_name}"

def write_content(content,filename):

    try:
        file = open(filename, 'w', encoding='utf-8')
        file.write(content)
        file.close()
        logger.info(f"Successfully wrote webpage to file {filename}")
    except Exception as e:
        logger.info(f"Failed to write webpage to file {filename} with error : {e}")
        logger.info("all tasks failed")
        
def main():
    set_logger()
    logger.info("Starting tasks...")

    write_content(get_content(sys.argv[1]),get_new_filename())

    logger.info("All tasks completed.")

# Exécuter la fonction principale
if __name__ == "__main__":
    main()
    
