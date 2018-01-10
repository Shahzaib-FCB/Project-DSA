# Importing the required python libraries
import re
import os
import sys
import pickle
import base64

# ^ : char that is not...
pattern = re.compile("[^a-zA-Z]") 				# Pattern to get text from the files
fChars = ["title", "text"] 						# Two main things that are required in form of list
stop_words = {} 								# Dictionary of stop words
reg = re.compile("\"|,| ") 						# Regex for the pattern
stFile = open("Stop_words.txt", "r") 			#reading the stop words text file
context = stFile.read() 						# getting context from it
context = re.split(reg, context) 				# splitting it according to regex
for word in context : 							# boolean for checking if the word is in stop words file or not
	if word :
		stop_words[word] = True