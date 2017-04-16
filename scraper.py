# -*- coding: utf-8 -*-
"""
Scrape the pages of the US Office of Government Ethics website that contain 
Financial Disclosure Reports and Ethics Agreements
"""

from bs4 import BeautifulSoup as bs
import requests

def grab_page(url):
	"""
	Retrieves the contents at the given url 
	If the retrieval is a success, it returns a BeautifulSoup object with the contents.
	Otherwise, None is returned
	"""
	contents = None
	r = requests.get(url)
	
	if r.status_code == 200:
		# only attempt to return bs object if the get was successful
		contents = bs(r.content, 'html.parser')
	
	return contents


if __name__ == "__main__":
    
	# get the page with the President and VP's reports
    vp_and_pres = grab_page('https://extapps2.oge.gov/201/Presiden.nsf/President%20and%20Vice%20President%20Index?OpenView&ExpandView')
    
    # get the page with the reports from other executive officers
	others = grab_page('https://extapps2.oge.gov/201/Presiden.nsf/PAS%20Index?OpenView')
	