'''
Extracts a Monash SETU pdf file from 
https://www.monash.edu/ups/setu/about/setu-results/unit-evaluation-reports 
and exports it into a csv file (coming soon)

Notes: Having some issues extracting Options from the table because 
they tend to be concatenated after using the pdf parser.

Author: Jarret Jheng Ch'ng 
Date: 4/12/2019
'''

import pdfScraper
import re
import os

def extractAgreeRates(setuFile):
	file = pdfScraper.extract_text_from_pdf(setuFile)

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

	return agreeRate

def extractSetuFolder(folderName):
	'''Extracts agree rates from every pdf file in a given folder'''
	output = []

	# lists all pdfs in a given folder
	filesToExtract = findPDFs(folderName)

	print("Extracting files:", filesToExtract)

	# extracts agree rates in each file
	for file in filesToExtract:
		rates = extractAgreeRates(folderName + "/" + file)
		print("Parsed:",file)
		output.append((file,rates))

	return output

def findPDFs(folderName):
	'''Return a list of pdfs filenames in the given folderName'''
	pdfFiles = []

	# get the current working directory + folder name
	folder = os.walk(os.getcwd() + "/" + folderName)

	# go through the provided folder
	for i in folder:
		files = i[-1] # take the last item in i (all files in folder)
		for names in files:
			if (".pdf" in names) and ("CLAYTON" in names): # find files with .pdf in the name
				pdfFiles.append(names)
		break 
		# only the first iteration is useful for our use
		# hence the break

	return pdfFiles

if __name__ == '__main__':
	# print(extractAgreeRates("sampleSetuFile1.pdf"))
	print(extractSetuFolder("sampleSetuPDFs"))
