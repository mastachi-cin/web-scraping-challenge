from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    #executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    #return Browser("chrome", **executable_path, headless=False)
    return

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

    return (news_title, news_parag)

def scrape_mars_featured_img():
    #Set up browser
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of page to be scraped
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    # Open browser for searching
    browser.visit(url)

    # Click on full image button
    browser.click_link_by_partial_text('FULL IMAGE')

    # Time needed
    time.sleep(1)

    # Click on more info button
    browser.click_link_by_partial_text('more info')

    # Create BeautifulSoup object; parse with html.parser
    html = browser.html
    soup = bs(html, 'html.parser')

    # Time needed for parsing completition
    time.sleep(1)
    result = soup.find('figure', class_='lede')

    # Relative path
    rel_image_url = result.find('a')['href']

    # Absolute path
    abs_image_url = 'https://www.jpl.nasa.gov' + rel_image_url

    # Close browser
    browser.quit()

    return abs_image_url


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

    return html_table

def scrape():
    #browser = init_browser()

    # Visit visitcostarica.herokuapp.com
    #url = "https://visitcostarica.herokuapp.com/"
    #browser.visit(url)

    #time.sleep(1)

    # Scrape page into Soup
    #html = browser.html
    #soup = bs(html, "html.parser")

    news_t, news_p = scrape_mars_news()

    featured_image_url = scrape_mars_featured_img()

    facts_table = scrape_mars_facts()



    # Store data in a dictionary
    mars_data = {
        "news_title": news_t,
        "news_paragraph": news_p,
        "featured_image": featured_image_url,
        "facts": facts_table
    }


    # Return results
    return mars_data
