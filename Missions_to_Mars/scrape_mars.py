from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import time


def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_mars_news():
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'

    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'lxml'
    soup = bs(response.text, 'lxml')

    # Retrieve div and class slide
    result = soup.find('div', class_='slide')

    # Scrape the news title
    news_title = result.find('div', class_='content_title').text.replace("\n\n", "")

    # Scrape the news paragraph text
    news_parag = result.find('div', class_='rollover_description_inner').text.replace("\n", "")

    # Return results
    return (news_title, news_parag)

def scrape_mars_featured_img(browser):
    # URL of page to be scraped
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    # Open browser for searching
    browser.visit(url)

    # Click on full image button
    browser.click_link_by_partial_text('FULL IMAGE')

    # Time needed to display page
    time.sleep(2)

    # Click on more info button
    browser.click_link_by_partial_text('more info')

    # Create BeautifulSoup object; parse with html.parser
    html = browser.html
    soup = bs(html, 'html.parser')

    # Time needed for parsing completition
    time.sleep(2)
    result = soup.find('figure', class_='lede')

    # Relative path
    rel_image_url = result.find('a')['href']

    # Absolute path
    abs_image_url = 'https://www.jpl.nasa.gov' + rel_image_url

    # Return results
    return abs_image_url

def scrape_mars_weather(browser):

    # URL of page to be scraped
    url = 'https://twitter.com/marswxreport?lang=en'

    # Open browser for searching
    browser.visit(url)

    # Time needed for loading entire page
    time.sleep(5)

    # Create BeautifulSoup object; parse with html.parser
    html = browser.html
    soup = bs(html, 'html.parser')

    # Find latest mars weather tweet
    result = soup.find('div', class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")
    mars_weather = result.text

    # Return results
    return mars_weather

def scrape_mars_facts():
    # URL of page to be scraped
    url = 'https://space-facts.com/mars/'

    # Scrape tabular data
    tables = pd.read_html(url)

    # Name columns 
    df = tables[0]
    df.columns = ['description', 'value']

    # Set the index to the description column
    df.set_index('description', inplace=True)

    # Convert the data to a HTML table string
    html_table = df.to_html(classes='data', header="true")

    # Strip unwanted newlines to clean up the table
    html_table = html_table.replace('\n', '')

    # Return results
    return html_table

def scrape_mars_hemisp(browser):

    # URL of page to be scraped
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # Open browser for searching
    browser.visit(url)

    # Create BeautifulSoup object; parse with html.parser
    html = browser.html
    soup = bs(html, 'html.parser')

    # results as an iterable list
    results = soup.find_all('div', class_="description")

    # List of dictionaries
    hemisphere_image_urls = []

    # Loop through returned results
    for result in results:
        # Error handling
        try:
            # Image title
            title = result.a.h3.text
        
            # Click on image title
            browser.click_link_by_partial_text(title)
        
            # Create a second BeautifulSoup object; parse with html.parser
            html_fullimg = browser.html
            soup_fullimg = bs(html_fullimg, 'html.parser')
        
            # Find full image
            result2 = soup_fullimg.find('div', class_='downloads')
            result_fullimg = result2.find_all('li')
            url_fullimg = result_fullimg[0].a['href']
        
            # Add dictionary to images list
            hemisphere_image_urls.append({'title': title, 'img_url': url_fullimg})
        
            # Back to initial page
            browser.back()
        except AttributeError as e:
            print(e)

    # Return results
    return hemisphere_image_urls

def scrape():
    
    # Scrape mars latest news
    news_t, news_p = scrape_mars_news()

    #Set up browser
    browser = init_browser()

    # Scrape mars featured image
    featured_image_url = scrape_mars_featured_img(browser)

    # Scrape mars weather
    weather = scrape_mars_weather(browser)

    # Scrape mars images hemispheres
    hemisp_images = scrape_mars_hemisp(browser)

    # Close browser
    browser.quit()

    # Scrape mars facts
    facts_table = scrape_mars_facts()

    # Store data in a dictionary
    mars_data = {
        "news_title": news_t,
        "news_paragraph": news_p,
        "featured_image": featured_image_url,
        "weather": weather,
        "facts": facts_table,
        "hemisp_image": hemisp_images
    }

    # Return results
    return mars_data
