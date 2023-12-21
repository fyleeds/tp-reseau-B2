import logging
import sys
import os
import re
import asyncio
import requests
import aiohttp
import aiofiles
import datetime


# tasks array
tasks = []
# urls array
urls = []
# Create a custom logger
logger = logging.getLogger("http_server")

async def check_and_get_url(url):

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
            logger.info(f"URL is valid: {url}")
            return url
        
        logger.info("URL is not valid please reenter a valid url ")
        logger.info("all tasks failed")
        return url

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

async def get_content(session,url):
    try:
        async with session.get(url) as resp:
            # resp contient le contenu HTML de la page
            resp = await resp.read()
            html_content = resp.decode('utf-8')
            logger.info(f"Success to retrieve the webpage {url}")
            return html_content
                
    except Exception as e:
        logger.info(f"Failed to retrieve the webpage: {url} with error :  {e}")
        logger.info("all tasks failed")
        sys.exit(1)
    
async def get_new_filename(url):

    folder_path = os.path.dirname(os.path.abspath(__file__))
    folder_path +=  "/tmp"

    web_page_name = f"web_{url}.html"

    # list all webpage name in folder tmp
    # entries = os.listdir(folder_path)
    # logger.info(f"{entries} already exists")
    
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
        
async def task(session, url):
    url_modified = await check_and_get_url(url)
    if url_modified:
        filename = await get_new_filename(url_modified)
        html_content = await get_content(session, url)
        await write_content(html_content, filename)

async def main():
    
    # Capture start time
    start_time = datetime.datetime.now()

    await set_logger()

    logger.info("Starting tasks...")

    urls = sys.argv[1:]  # Get URLs from command line arguments
    
    async with aiohttp.ClientSession() as session:
        tasks = [task(session, url) for url in urls]
        await asyncio.gather(*tasks)

    logger.info("All tasks completed.")

    # Capture end time
    end_time = datetime.datetime.now()

    # Calculate the difference in seconds
    logger.info(f"{(end_time - start_time).total_seconds()} seconds elapsed" )

# Exécuter la fonction principale
if __name__ == "__main__":
    asyncio.run(main())

