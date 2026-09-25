import asyncio
from urllib.parse import urlparse, urlunparse
import os
from dotenv import load_dotenv
import shutil
from urllib import robotparser
from crawl4ai import AsyncWebCrawler,CrawlerRunConfig,CacheMode,BrowserConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.content_filter_strategy import BM25ContentFilter
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from pathlib import Path
import logging
#==========Logger==============

logger = logging.getLogger(__name__)
#==========Logger===============


BASE_DIRT = Path(__file__).resolve().parent.parent
DB_PATHH = BASE_DIRT / "database" / "vector" / "temp_vector"



def retrieve(query):
    """"""

    logger.info("Successfully called retriver for vector retrieve")

    embeddding = OllamaEmbeddings(model="nomic-embed-text")

    vector_db = FAISS.load_local(str(DB_PATHH),embeddings=embeddding,allow_dangerous_deserialization=True)

    retrieve =vector_db.as_retriever(search_kwargs={"k":4})

    docs = retrieve.invoke(query)

    value = []
    

    for i, content in enumerate(docs,start=1):
        context = {}
        source = content.metadata.get("source","uknown")
        context["No."] = i
        context["source"] = source
        context["Content"] = content.page_content
        value.append(context)

  

    folder_path = os.getenv("deleting_folder")
    try:
        shutil.rmtree(folder_path)
        logger.debug(f"Successfully deleted {folder_path} and all its contents.")
    except Exception as e:
        logger.error(f"Error: {e}")

    logger.info("Retrieved data is generate")

    return value





def vector_store(results):
    """"""

    logger.info("Successfully called vectore_store for embedding")

    all_chunks=[]
    all_metadate=[]

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=200,chunk_overlap=50,separators=["\n\n", "\n"])

    embedding =OllamaEmbeddings(model="nomic-embed-text")

    for result in results:
        if result.success:
            if hasattr(result, 'markdown_v2') and result.markdown_v2:
                content =result.markdown_v2.fit_markdown
            elif hasattr(result, 'markdown'):
                content=result.markdown
            else:
                continue
        else:
            continue

        if not content:
            continue

        chunk = text_splitter.split_text(content)

        all_chunks.extend(chunk)

        for i in chunk:
            all_metadate.append({"source" : result.url})



    if all_chunks:
        vector_store = FAISS.from_texts(texts=all_chunks,embedding=embedding,metadatas=all_metadate)

        vector_store.save_local(str(DB_PATHH))
    logger.debug("Embedding successfull")
    return {"success": True, "error": ""}

    






async def web_crawl(url:list,query:str)->list:
    """Crawl the website for the provided links"""

    logger.info("Successfully called web_crawler")

    bm25_filter = BM25ContentFilter(user_query=query,bm25_threshold=2)
    mark = DefaultMarkdownGenerator(content_filter=bm25_filter)

    config =CrawlerRunConfig(
        markdown_generator=mark,
        excluded_tags=["nav","img","a","header","footer","form"],
        only_text=True,
        exclude_social_media_links=True,
        keep_data_attributes=False,
        page_timeout=20000,
        remove_overlay_elements=True,
        cache_mode=CacheMode.BYPASS

    )


    browser = BrowserConfig(browser_mode="chromium", headless=True,text_mode=True,light_mode=True)

    async with AsyncWebCrawler(config=browser) as crawler:
        #print("hi")
        results = await crawler.arun_many(url,config=config)

        return results
        








def clean_url(url):

    if not url:
        return None

    parsed = urlparse(url)

    domain = parsed.netloc.lower()
    path = parsed.path.lower()
    invalid_extensions = (
        ".jpg", ".jpeg", ".png", ".gif", ".svg", ".mp4", 
        ".pdf", ".zip", ".exe", ".css", ".js", ".json"
    )
    if path.endswith(invalid_extensions):
        return None

    spam_paths = ["/login", "/signin", "/signup", "/register", "/cart", "/checkout", "/password"]
    if any(spam in path for spam in spam_paths):
        return None

    if domain in {
        "accounts.google.com",
        "maps.google.com",
        "support.google.com",
        "policies.google.com",
        "youtube.com",
        "www.youtube.com",
        "www.reddit.com",
        ".gov.in",
        ".gov"
        "www.facebook.com",
        "www.instagram.com"
    }:
        return None

    if domain in {"google.com","www.google.com","google.co.in","www.google.co.in"}:
        if path in {"/search", "/webhp"}:
            return None

        print(path)
        if path.startswith("/intl/"):
            return None

    url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        parsed.query,
        ""
    ))
    
    return url




def allow(url,domain_cache):
    """Check which sitesa are alloweded to scrap"""
    try:
        parsed = urlparse(url)
        base_domain = f"{parsed.scheme}://{parsed.netloc}"
        robots_url = f"{base_domain}/robots.txt"
        #robots_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}/robots.txt"
        if base_domain not in domain_cache:
            rp = robotparser.RobotFileParser(robots_url)
            rp.read()
            domain_cache[base_domain] = rp


        rp = domain_cache[base_domain]

        if rp.can_fetch("*", url):
            return url
        else:
            print(f"Blocked by robots.txt: {url}")
            return None

    except Exception as e:
        # If the site doesn't have a robots.txt or it times out, assume it's allowed
        return url



async def content_extractor(page,query):
    """It will extract the content from the html page"""

    logger.info("Successfully called content_extractor")

    text = await page.locator("body").inner_text()
  
    clean = []
    links = await page.locator("a").evaluate_all("elements => elements.map(el => el.href)")

    domain_cache={}
    for link in links:
        a = clean_url(link)
        if a is None:
            continue
        clean.append(a)
    print(len(clean))
    allows= []
    for i in clean:
        b = allow(i,domain_cache)
        if b is None:
            continue
        allows.append(b)

    unique_links = list(set(allows))

    logger.debug(f"unique links - {unique_links}")

    # for i,link in enumerate(unique_links):
    #     print(f"{i}-> {link}")



    data = await web_crawl(url=unique_links,query=query)

    logger.info("Got results from web_crawler")

    vector_store(data)

    retrieve_outcome = retrieve(query=query)

    return {"success": True, "error": "","vector_data":retrieve_outcome}



    