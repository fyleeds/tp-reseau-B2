import logging
import sys
import os
import requests

ids = [0]

try:
      # Create a custom logger
      logger = logging.getLogger("http_server")
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
        logger.info("Successfully retrieved webpage.")
        return response.text
    else:
        logger.info("Failed to retrieve the webpage.")
        return None
    
def get_new_filename():

    folder_path = os.path.dirname(os.path.abspath(__file__))

    id=1
    # check avalaible id in ids already used
    while id in ids:
        id+=1
    ids.append(id)

    # get a new web page name
    web_page_name = f"web_page{id}"

    return f"{folder_path}/tmp/{web_page_name}.html"

def write_content(content,filename):

    if content == None:
        logger.info(f"Failed to write webpage to file {filename}.html")
    elif filename != None:
        logger.info(f"Failed to write webpage to file {filename}.html")
    else:
        try:
            file = open(filename, 'w')
            file.write(content)
            file.close()
            logger.info(f"Successfully wrote webpage to file {filename}.html")
        except Exception as e:
            logger.info(f"Failed to write webpage to file {filename}.html with error : {e}")

# Exécuter la fonction principale
if __name__ == "__main__":
    write_content(get_content("https://www.ynov.com"),get_new_filename())
