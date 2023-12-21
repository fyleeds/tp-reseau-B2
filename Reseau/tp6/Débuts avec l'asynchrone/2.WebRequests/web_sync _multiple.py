import logging
import sys
import os
import requests
import re
import datetime

# id_array
ids = []
# Create a custom logger
logger = logging.getLogger("http_server")

def check_and_get_url(url):

    # Perform a GET request to the URL
    # pattern = r'^(https?:\/\/)([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$'
    pattern = r'^(https?:\/\/)([\da-z\.-]+)\.([a-z\.]{2,6})$'
    matches = re.findall(pattern, url)
    for match in matches:
        # Extract numbers from each match and convert them to integers
        url = ""
        if len(match) > 1:
            # Get url without http:// or https://
            url = match[1] + "." + match[2]
            logger.info(f"URL is valid:{url}")
            return url
        
        logger.info("URL is not valid please reenter a valid url ")
        logger.info("all tasks failed")
        return url

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
    
def get_new_filename(url):

    folder_path = os.path.dirname(os.path.abspath(__file__))
    folder_path +=  "/tmp"

    id=0
    web_page_name = f"web_{url}.html"

    # list all webpage name in folder tmp
    # entries = os.listdir(folder_path)

    # check available id in ids already used
    # while web_page_name in entries:
    #     id+=1
    #     web_page_name = f"web_{url}{id}.html"
    
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
        sys.exit(1)
        
def main():
    # Capture start time
    start_time = datetime.datetime.now()

    set_logger()
    logger.info("Starting tasks...")
    for i in range(1,len(sys.argv)):
        logger.info(f"task {i} : {sys.argv[i]}")
        url = check_and_get_url(sys.argv[i])
        if url != "":
            write_content(get_content(sys.argv[i]),get_new_filename(url))

    logger.info("All tasks completed.")

    # Capture end time
    end_time = datetime.datetime.now()

    # Calculate the difference in seconds
    logger.info(f"{(end_time - start_time).total_seconds()} seconds elapsed" )

# Exécuter la fonction principale
if __name__ == "__main__":
    main()
    
