# -*- coding: utf-8 -*-
"""
Tests _some_ of the functions in scraper.py
"""

import unittest
import scraper as scpr


class TestScraperMethods(unittest.TestCase):
    
    def test_parse_name(self):       
        names = [('Biden, Jr., Joseph R.   ', ('Joseph', 'R', 'Biden', 'Jr')), \
            ('Acosta, Rene Alexander ', ('Rene', 'Alexander', 'Acosta', '')), \
            ('Charles-F-Bolden-Jr-', ('Charles', 'F', 'Bolden', 'Jr')), \
            ('Janet -L-Yellen-', ('Janet', 'L', 'Yellen', '')), \
            ('Obama, Barack H.', ('Barack', 'H', 'Obama', '')), \
            ('Daniel-Yohannes-', ('Daniel', '', 'Yohannes', '')), \
            ('Melvin-L-Watt-07.23.', ('Melvin', 'L', 'Watt', ''))]
        for name, ans in names:
            first, middle, last, suffix = scpr.parse_name(name)
            self.assertEqual((first, middle, last, suffix), ans)


    def test_grab_file_info(self):
        links = [("<a href='/201/Presiden.nsf/President and Vice President Index/0A9239BE1465EF0B852580B5004908BC/$FILE/Obama, Barack H.   2011Annual.pdf'><img alt='download pdf' src='Adobe_PDF_file_icon_24x24.png'>Annual (2011)</a>", \
            [('https://extapps2.oge.gov/201/Presiden.nsf/President and Vice President Index/0A9239BE1465EF0B852580B5004908BC/$FILE/Obama, Barack H.   2011Annual.pdf', 'Barack', 'H', 'Obama', '', '2011', 'Annual (2011)')]),\
        ("<a href='/201/Presiden.nsf/PAS+Index/5A96447F978BF42185257FC20010DB73/$FILE/Melvin-L-Watt-07.23.2015Form278-T.pdf'><img alt='download pdf' src='Adobe_PDF_file_icon_24x24.png'>278 Transaction (07/23/2015)</a>", \
            [('https://extapps2.oge.gov/201/Presiden.nsf/PAS+Index/5A96447F978BF42185257FC20010DB73/$FILE/Melvin-L-Watt-07.23.2015Form278-T.pdf', 'Melvin', 'L', 'Watt', '', '2015', '278 Transaction (07/23/2015)')]),\
        ("<a href='/201/Presiden.nsf/PAS+Index/FA938A404D0D6153852580C1002C7A86/$FILE/Shulkin, David J.  finalAMENDEDEA.pdf'><img alt='download pdf' src='Adobe_PDF_file_icon_24x24.png'>Ethics Agreement</a>", \
            [('https://extapps2.oge.gov/201/Presiden.nsf/PAS+Index/FA938A404D0D6153852580C1002C7A86/$FILE/Shulkin, David J.  finalAMENDEDEA.pdf', 'David', 'J', 'Shulkin', '', '', 'Ethics Agreement')]), \
        ("<a href='/201/Presiden.nsf/PAS+Index/98119BCF69AC9DE7852580DE002C800A/$FILE/Acosta, Rene Alexander final278.pdf'><img alt='download pdf' src='Adobe_PDF_file_icon_24x24.png'>Nominee 278 (03/07/2017)</a>", \
            [('https://extapps2.oge.gov/201/Presiden.nsf/PAS+Index/98119BCF69AC9DE7852580DE002C800A/$FILE/Acosta, Rene Alexander final278.pdf', 'Rene', 'Alexander', 'Acosta', '', '2017', 'Nominee 278 (03/07/2017)')])]

        for entry, ans in links:
            self.assertEqual(scpr.grab_file_info(scpr.bs(entry, 'html.parser')), ans)
                    
            
if __name__ == '__main__':
    unittest.main()

