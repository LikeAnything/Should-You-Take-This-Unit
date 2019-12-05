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

def extractSetuFolder(folderName,verbose=False):
	'''Extracts agree rates from every pdf file in a given folder'''
	output = []

	# lists all pdfs in a given folder
	filesToExtract = findPDFs(folderName)

	if verbose:
		print("Files to parse:", filesToExtract)

	# extracts agree rates in each file
	for file in filesToExtract:
		rates = extractAgreeRates(folderName + "/" + file)
		# Uncomment for verbose mode

		if verbose:
			print("Parsed:",file)

		output.append((file,rates))

	return output


def extractFolderToCSV(folderName):
	'''Parses the folder full of pdfs and turn it into a csv format'''

	# column headers for the csv file
	csvFile = "Unit,Campus,Learning outcomes were clear,Assessments were clear,\
	Assessments allowed me to demonstrate the learning outcomes,\
	Feedback helped me achieve the learning outcomes,\
	Resources helped me achieve the learning outcomes,Activities helped me achieve the learning outcomes,\
	Attempted to engage in this unit,Is satisfied with the unit,I could see how the topics were related,\
	Online resources were useful,Workload was manageable,Tutorial/pracs were useful,Pre-class activities were useful\n"

	# Extract the tables from each file
	data = extractSetuFolder(folderName)

	# Laying down the name and the information of each file
	for (name,info) in data:
		# Get formatted version of filename
		formattedFileName = cleanUpSetuFilename(name)

		# Add unit name and campus
		csvFile += formattedFileName[0] + "," + formattedFileName[1] + "," 
		
		# Writes info of each table to the columns
		for percentage in info:
			csvFile += str(percentage) + ","

		csvFile += "\n" # prepare it for a new entry/file

	return csvFile


def cleanUpSetuFilename(name):
	'''Formats the filename into a usable format'''
	output = []
	name = name.split("-")
	# print(name)

	# Take unit name
	output.append(name[2].split("_")[0])

	# Take Campus
	output.append(name[2].split("_")[1])

	# Take Semester
	output.append(name[3].split("_")[-1])

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
			if (".pdf" in names) and ("CLAYTON" in names) and ("CAMPUS_ON" in names): 
			# find files with .pdf in the name and is from clayton and is on campus
				pdfFiles.append(names)
		break 
		# only the first iteration is useful for our use
		# hence the break

	return pdfFiles

if __name__ == '__main__':
	# print(extractAgreeRates("sampleSetuFile1.pdf"))
	print(extractFolderToCSV("sampleSetuPDFs"))
	# cleanUpSetuFilename("UE00389-Unit_Evaluation_Report-FIT4441_CLAYTON_ON-CAMPUS_ON_S1-01-1946232_ffb075ed-48d0-4d57-88d2-5fe2cb1e32a5en-US.pdf")