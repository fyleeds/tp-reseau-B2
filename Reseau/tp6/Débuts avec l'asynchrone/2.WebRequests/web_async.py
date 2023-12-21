import logging
import sys
import os
import requests
import aiohttp
import aiofiles
import asyncio
import re
import datetime

# id_array
ids = []
# Create a custom logger
logger = logging.getLogger("http_server")

async def set_logger():
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

async def get_new_filename():

    folder_path = os.path.dirname(os.path.abspath(__file__))
    folder_path +=  "/tmp"

    id=1
    web_page_name = f"web_page{id}.html"

    # list all webpage name in folder tmp
    entries = os.listdir(folder_path)
    logger.info(f"{entries} already exists")
    # check avalaible id in ids already used
    while web_page_name in entries:
        id+=1
        web_page_name = f"web_page{id}.html"
    
    logger.info(f"{web_page_name} will be created at {folder_path}")

    # return a new web page name
    return f"{folder_path}/{web_page_name}"

async def write_content(html_content,filename):
    try : 
        async with aiofiles.open(filename, "w", encoding='utf-8') as out:
            await out.write(html_content)
            await out.flush() 
            logger.info(f"{filename} has been created")
            logger.info("All tasks completed.")
    except Exception as e:
        logger.info(f"Failed to write the webpage in a document: {e}")
        logger.info("all tasks failed")
        sys.exit(1)

async def get_content(url):
    async with aiohttp.ClientSession() as session:
        try:
                async with session.get(url) as resp:
                    # resp contient le contenu HTML de la page
                    resp = await resp.read()
                    html_content = resp.decode('utf-8')
                    return html_content
                    logger.info(f"Success to retrieve the webpage {url}")
        except Exception as e:
            logger.info(f"Failed to retrieve the webpage: {e}")
            logger.info("all tasks failed")
            sys.exit(1)

async def main():
    # Capture start time
    start_time = datetime.datetime.now()

    await set_logger()
    logger.info("Starting tasks...")

    url = sys.argv[1]
    await write_content(await get_content(url),await get_new_filename())

    
    # Capture end time
    end_time = datetime.datetime.now()

    # Calculate the difference in seconds
    logger.info(f"{(end_time - start_time).total_seconds()} seconds elapsed" )


# Exécuter la fonction principale
if __name__ == "__main__":
    asyncio.run(main())
