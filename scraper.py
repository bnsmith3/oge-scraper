# -*- coding: utf-8 -*-
"""
Scrape the pages of the US Office of Government Ethics website that contain 
Financial Disclosure Reports and Ethics Agreements
"""

from bs4 import BeautifulSoup as bs
import requests
import re

def grab_page(url, local=True):
    """
    Retrieves the contents at the given URL
    It looks for the file on the local drive if the local parameter is True but otherwise it looks on the web
    If the retrieval is a success, it returns a BeautifulSoup object with the contents.
    Otherwise, None is returned
    """
    contents = None
    
    if local:
        with open(url, 'r') as f:
            response = " ".join(f.readlines())
            contents = bs(response, 'html.parser')
    else:
        response = requests.get(url)
    
        if response.status_code == 200:
            # only attempt to return bs object if the get was successful
            contents = bs(response.content, 'html.parser')
    
    return contents
    
def grab_and_parse_rows(page, prefix = 'https://extapps2.oge.gov'):
    """
    Grab all of the pdf links in the given BeautifulSoup object
    Append the given prefix to all of the parsed link URLs
    Return a list of tuples that contain the following for each URL:
        the URL with the given prefix appended
        the person's name to whom the form belongs
        the year
        the type of form
    """
    links = []

    # all of the URLs to pdfs have '$FILE' in them
    page_entries = page.select('a[href*="$FILE"]')
    
    # from each link, save the URL with prefix, the person's name, the year,
    # and the type of form
    for entry in page_entries:
        link = entry.attrs['href']
        name, year, form_type = re.search('(.*)(\d{4})(.*)', link.split('/')[-1]).groups()
        year = year.strip()
        
        # remove the extension from the form type
        form_type = (form_type.split('.')[0]).strip()
        
        # remove the extraneous punctuation from the name
        name = parse_name(name)
        
        links.append(('{}{}'.format(prefix, link), name, year, form_type))
    
    return links
    
def parse_name(name):
    """
    """
    name = name.strip()
    
    return name


if __name__ == "__main__":
   
    # get the page with the President and VP's reports
    #vp_and_pres = grab_page('https://extapps2.oge.gov/201/Presiden.nsf/President%20and%20Vice%20President%20Index?OpenView&ExpandView', False)
    vp_and_pres = grab_page('examples/pres_filings.htm')
    
    # parse the results if we were able to retrieve them
    if vp_and_pres:
        # all of the links to pdfs have '$FILE' in them
        vp_and_pres_entries = grab_and_parse_rows(vp_and_pres)
    
    
    # get the page with the reports from other executive officers
    #others = grab_page('https://extapps2.oge.gov/201/Presiden.nsf/PAS%20Index?OpenView', False)
    
