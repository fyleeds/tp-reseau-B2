import logging
import sys
import os
import requests
import aiohttp
import aiofiles
import asyncio
ids = []

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
        return response.text
    else:
        logger.info("Failed to retrieve the webpage.")
        return None
    
def get_new_filename():

    folder_path = os.path.dirname(os.path.abspath(__file__))
    folder_path +=  "/tmp"

    logger.info(f"folder_path : {folder_path}")
    id=1
    web_page_name = f"web_page{id}.html"

    # list all webpage name in folder tmp
    entries = os.listdir(folder_path)
    logger.info(f"{entries} already exists")
    # check avalaible id in ids already used
    while web_page_name in entries:
        logger.info(f"web_page{id} already exists")
        id+=1
        web_page_name = f"web_page{id}.html"

    # return a new web page name
    return f"{folder_path}/{web_page_name}"

async def write_content(content,filename):

    if content == None:
        logger.info(f"Failed to get the content of {filename}")
    elif filename == None:
        logger.info(f"Failed to get filename :  {filename}")
    else:
        try:
            file = open(filename, 'w', encoding='utf-8')
            file.write(content)
            file.close()
            logger.info(f"Successfully wrote webpage to file {filename}")
        except Exception as e:
            logger.info(f"Failed to write webpage to file {filename} with error : {e}")


async def main():
    print("Starting tasks...")
    # write_content(get_content(sys.argv[1]),get_new_filename())
    # tasks=[get_content(sys.argv[1]),count_to_ten()]   
    # for task in tasks:
    #     await task
    async with aiohttp.ClientSession() as session:
        async with session.get(sys.argv[1]) as resp:
            resp = await resp.read()
            html_content = resp.decode('utf-8')
            # resp contient le contenu HTML de la page
            print(resp)
            
    async with aiofiles.open(get_new_filename(), "w", encoding='utf-8') as out:
        await out.write(html_content)
        await out.flush() 

    print("All tasks completed.")

# Exécuter la fonction principale
if __name__ == "__main__":
    asyncio.run(main())
