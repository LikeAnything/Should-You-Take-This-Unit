'''
Extracts a Monash SETU pdf file from 
https://www.monash.edu/ups/setu/about/setu-results/unit-evaluation-reports 
and exports it into a csv file.

Notes: Having some issues extracting Options from the table because 
they tend to be concatenated after using the pdf parser.

Author: Jarret Jheng Ch'ng 
Date: 4/12/2019
'''

import pdfScraper
import re

file = pdfScraper.extract_text_from_pdf("sampleSetuFile1.pdf")

# semiParsed is a list of tables
# "\d\. " is a regex that finds a digit then a full stop then a space
# e.g. "100. " would be accepted by the regex
# we split it by this regex to find each table
semiParsed = re.split("\d\. ",file)

# a list to hold all of the percentages from each table
agreeRate = []

# go through each of the tables and extract the Strongly Agree/Agree part of the table
# first item is ignored because that is the very first table that is split by "1. "
for i in semiParsed[1:]:
	# Split by the keyword and by the % so that we can extract the numeric value of it
	agreeRate.append(float(i.split("Strongly Agree/Agree:")[-1].split("%")[0]))

print(agreeRate)