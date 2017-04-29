# -*- coding: utf-8 -*-
"""
Scrape the pages of the US Office of Government Ethics website that contain 
Financial Disclosure Reports and Ethics Agreements
"""

from collections import defaultdict
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
    
def grab_file_info(page, prefix = 'https://extapps2.oge.gov'):
    """
    Grab all of the pdf links in the given BeautifulSoup object
    Append the given prefix to all of the parsed link URLs
    Return a list of tuples that contain the following for each URL:
        the URL with the given prefix appended
        the person's name to whom the form belongs (first, middle, and last name and suffix)
        the year
        the type of form
        
    Examples of links:
        Biden, Jr., Joseph R.   2015Annual.pdf
        Acosta, Rene Alexander finalEA.pdf
        Charles-F-Bolden-Jr-2015Form278.pdf
        Janet -L-Yellen-2013EANewEntrant.pdf      
    """
    links = []

    # all of the URLs to pdfs have '$FILE' in them
    page_entries = page.select('a[href*="$FILE"]')
    
    # from each link, save the URL with prefix, the person's name, the year,
    # and the type of form
    for entry in page_entries:
        link = entry.attrs['href']
        
        form_type = entry.contents[0].contents[0].strip()
        year = ''

        # treat links differently depending on if they contain the year
        if re.search('\d{4}', link.split('/')[-1]):
            name, year, _ = re.search('(.*)(\d{4})(.*)', link.split('/')[-1]).groups()
            year = year.strip()       
        else:
            parts = re.split('\s+', link.split('/')[-1])
            name = " ".join(parts[0:-1])
            
            # try to get the year from the form_type
            contents_search = re.search('(.*)(\d{4})(.*)', form_type)
            if contents_search:
                _, year, _ = contents_search.groups()
            
        # clean up the name
        first_name, middle_name, last_name, suffix = parse_name(name)
        
        links.append(('{}{}'.format(prefix, link), first_name, middle_name, last_name, suffix, year, form_type))
    
    return links
    
def parse_name(name):
    """
    Takes in a name (e.g., Obama, Barack H.) and spits out the first name, 
    middle name, last name and suffix
    Those values are all empty if the given name doesn't have at least two parts
    
    Examples of names:
        Biden, Jr., Joseph R.
        Acosta, Rene Alexander
        Charles-F-Bolden-Jr-
        Janet -L-Yellen-
        Daniel-Yohannes-
        Melvin-L-Watt-07.23.
    """
    
    # figure out the delimiter
    if "-" in name:
        delim = "-"
    else:
        delim = ","
    
    # only add parts with a letter and that aren't blank
    # and remove punctuation
    name_parts = [re.sub('[\.,\-\'\"]*', '', a.strip()) for a in name.split(delim) if re.search('[a-zA-Z]', a) and (len(a.strip()) > 0)]
    
    first_name = ''
    middle_name = ''
    last_name = ''
    suffix = ''
    
    if len(name_parts) > 1:    
        if delim == ",":
            if " " in name_parts[-1]:
                first_name, middle_name = name_parts[-1].split(" ")
            else:
                first_name = name_parts[-1]
                
            last_name = name_parts[0]
            
            if len(name_parts) > 2:        
                suffix = name_parts[1]
        elif delim == "-":
            first_name = name_parts[0]
            
            if len(name_parts) == 2:
                last_name = name_parts[1]
            elif len(name_parts) == 3:
                middle_name = name_parts[1]
                last_name = name_parts[2]
            elif len(name_parts) == 4:
                middle_name = name_parts[1]
                last_name = name_parts[2]
                suffix = name_parts[3]
                
    return first_name, middle_name, last_name, suffix

    
def grab_and_parse_rows(page):
    """
    Grab all of the rows in the given BeautifulSoup object
    Return a dictionary with an individual's name as the key and the values as
    the list of files attributed to that individual
    """
    entries = defaultdict(list)
    delim = ", "
    key = None
    
    for row in page.findAll('td'):
        for entry in row.select('img[alt^="Hide details for"]'):
            parts = (re.search('for\s+(.*)$', entry['alt']).groups()[0]).split(delim)
            first_name, middle_initial, last_name, suffix = parse_name(delim.join(parts[0:2]))
            key = (first_name, middle_initial, last_name, suffix, parts[3])
            
        for entry in grab_file_info(row):
            entries[key].append(entry)
            
    return entries


def add_to_db(conn, links):
    """
    """
    success = False
    
    return success


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
    
