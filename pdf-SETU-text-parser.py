'''
Extracts a Monash SETU pdf file from 
https://www.monash.edu/ups/setu/about/setu-results/unit-evaluation-reports 
and exports it into a csv file.

Author: Jarret Jheng Ch'ng 
Date: 4/12/2019
'''

from pdf-scraper.py import extract_text_from_pdf

extract_text_from_pdf("sampleSetuFile1")