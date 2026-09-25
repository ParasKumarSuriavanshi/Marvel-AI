import re
import asyncio
import time
import subprocess
import os
from playwright.async_api import async_playwright

from web.content_extractor import content_extractor

from urllib.parse import quote_plus
import logging
#==========Logger==============

logger = logging.getLogger(__name__)
#==========Logger===============




CDP_URL = "http://localhost:9222"


async def web_search(query):
    """Open chrome and search URL or query"""

    logger.info("Successfully logged in to web_search")
    # subprocess.Popen("chromium",stdout=subprocess.DEVNULL, 
    #         stderr=subprocess.DEVNULL)

    await asyncio.sleep(1)

    playwright = await async_playwright().start()

    result = subprocess.run(['pgrep', '-i', 'chromium'], capture_output=True)
    running = (result.returncode == 0)


    if not running:
        logger.debug("New chrome window is opened")
        subprocess.run(['hyprctl', 'dispatch', 'workspace', 'empty'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.Popen("chromium",stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2) 
    browser = await playwright.chromium.connect_over_cdp("http://localhost:9222")

    page = None
    context = browser.contexts[0]
    exist = False
    for p in context.pages:
        if query == p.url or f"https://www.google.com/search?q={quote_plus(query)}" == p.url:
            page = p
            exist = True
            await page.bring_to_front()
            subprocess.run(["hyprctl", "dispatch", "focuswindow", "class:chromium"],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            break
        elif "about:blank" in p.url or 'chrome://new-tab-page/' in p.url or "chrome-extension://hipekcciheckooncpjeljhnekcoolahp/index.html" in p.url:
            page = p
            break
    if not exist:
        if not page:
            page = await context.new_page()
            
        try:
            await page.goto(query, wait_until='load')
        except:
            search_url = f"https://www.google.com/search?q={quote_plus(query)}"
            await page.goto(search_url, wait_until='load')
        subprocess.run(["hyprctl", "dispatch", "focuswindow", "class:chromium"],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
    await asyncio.sleep(1)

    outcome = await content_extractor(page=page,query=query)
    logger.info("successfully got the data")
    await playwright.stop()


    return outcome
