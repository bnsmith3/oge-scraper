# -*- coding: utf-8 -*-
"""
Tests _some_ of the functions in scraper.py
"""

import unittest
import scraper as scpr


class TestScraperMethods(unittest.TestCase):
    
    def test_parse_name(self):       
        names = [('Biden, Jr., Joseph R.   ', ",", ('Joseph', 'R', 'Biden', 'Jr')), \
            ('Acosta, Rene Alexander ', ",", ('Rene', 'Alexander', 'Acosta', '')), \
            ('Charles-F-Bolden-Jr-', "-", ('Charles', 'F', 'Bolden', 'Jr')), \
            ('Janet -L-Yellen-', "-", ('Janet', 'L', 'Yellen', '')), \
            ('Obama, Barack H.', ",", ('Barack', 'H', 'Obama', '')), \
            ('Daniel-Yohannes-', "-", ('Daniel', '', 'Yohannes', '')), \
            ('Melvin-L-Watt-07.23.', "-", ('Melvin', 'L', 'Watt', ''))]
        for name, delim, ans in names:
            first, middle, last, suffix = scpr.parse_name(name, delim)
            self.assertEqual((first, middle, last, suffix), ans)

if __name__ == '__main__':
    unittest.main()

