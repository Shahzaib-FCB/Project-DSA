import operator
from importing import * 						# File containing utiliites that are required during indexing and serching
from math import *  							# For math operations
from heapq import *
from collections import * 						# For default dictionaries
import xml.etree.cElementTree as et
import socket									# to get host name; socket.gethostname()
import os 										# to get file size; os.stat().st_size
import time 									# to measure the time taken

# to fill data in indextime (contains our findings about indexing)
extras=open("indexTime.txt", "a")
index_start_time = time.time()
# need to reload to reload the attributes of sys object(to change encoding)
reload(sys)
sys.setdefaultencoding('utf-8') 				# Setting deafult to UTF-8 for indexing everything
# import collections	(defaultdict(list))
# comma seperated (backbone of reverse indexing) - Can't stress enough
# Dictionaries for title and text indexes
txI = defaultdict(list)
tI = defaultdict(list)
wPosition = {} 									# Positioning of words used for pickle library
oFiles = [] 									# Files for outputs
tPosition = [] 									# Positioning of titles used for pickle library
PagesPerFile = 2000 							# Pages per file
fCount = 0 										# Files counting
pCount = 0 										# Page counting
# command line argument
arguments = sys.argv
xmlF = arguments[1]
# gives SAX model (vs DOM) -- faster cuz indexable while running
# parse the document tag by tag (vs not whole doc)
# events : start tag <text>, end tag </text>
context= et.iterparse(xmlF, events=("start", "end"))
# makes context an iteratable object
context= iter(context)
tTags = open("text/title_tags.txt", "w") 		# Title Tags text files
for Event, Element in context: 					# Iterating events and elements
	tag =  re.sub(r"{.*}", "", Element.tag)
	if Event == "start" :
		if tag == "page" : 						# So basically if events starts then it counts the pages
			pCount += 1
			TitleWords = {} 					# Dictionary for title tags
			TextWords = {} 						# Dictionary for text tags
	if Event == "end" : 						# Same is the case for text tags but if events ends
		if tag == "text" :
			text = Element.text
			try : 								# If above criteria is passed we format it to required texts
				text = text.encode("utf-8") 	# Encodeing
				text = text.lower() 			# Lowering the text
				text = re.split(pattern, text) 	# Splitting like pattern mentioned in utility file
				WordsPerPage = 0
				for w in text : 				# Iterating word by word
					if w : 						# Checking against stop words
						if w not in stop_words :
							if w not in TextWords :
								TextWords[w] = 0
							TextWords[w] += 1 	# If not then increment it
			except :
				pass 							# Now we will do the same thing with titles
		if tag == "title" :
			text = Element.text
			try :
				text = text.encode("utf-8") 	# Encodeing
				tString = text + "\n"
				text = text.lower() 			# Lowering the text
				tPosition.append(tTags.tell()) 	# Appending the tags with their positions
				tTags.write(tString)
				text = re.split(pattern, text) 	# Splitting like pattern mentioned in utility file
				for w in text :
					if w :
						if w not in stop_words :# Checking against stop words
							if w not in TitleWords :
								TitleWords[w] = 0
							TitleWords[w] += 1 	# If not then increment it
			except :
				pass 							# Now we will do the indexing
		if tag == "page" :
			index = "d"+str(pCount) 			# We attached a d word for document number
			for w in TextWords : 				#Indexing for text tags
				s = index + ":" + str(TextWords[w]) #Making the format that we want
				txI[w].append(s) 				# Appending with index string
			for w in TitleWords : 				# Indexing for title tags
				s = index + ":" + str(TitleWords[w])
				tI[w].append(s)
			if pCount % PagesPerFile == 0 : 	# Now we will check the 200 pages per file criteria
				file = "text/" + "title" + str(fCount) + ".txt"
				oFile = open(file, "w") 		# Writing in the files
				for w in sorted(tI) : 			# Sorting the title indexes
					index = ",".join(tI[w])
					index = w + "-" + index+"\n"# Making the format discussed in presentation
					oFile.write(index)
				oFile.close() 					# Closing files of title tag indexing
                # Now we will do the same for text indexes
				file = "text/" + "text" + str(fCount) + ".txt"
				oFile = open(file, "w") 		# Writing in the files
				for w in sorted(txI) : 			# Sorting the title indexes
					index = ",".join(txI[w])
					index = w + "-" + index+"\n"# Making the format discussed in presentation
					oFile.write(index)
				oFile.close() 					# Closing files of title tag indexing
				oFile.close()
				fCount += 1 					# As we have indexed a whole file so we increment it
				tI.clear() 						# We carry this process until all title and text tags are indexed
				txI.clear()
		Element.clear()
tTags.close()
file = open("text/title_positions.pickle", "wb")# This process for positioning titles using pickle
pickle.dump(tPosition, file) 
file.close()
file = "text/" + "title" + str(fCount) + ".txt"
oFile = open(file, "w")
for w in sorted(tI) : 							#After making positions we will sort the new title indexes according to format
	index = ",".join(tI[w])
	index = w + "-" + index+"\n" 				# Making the format discussed in presentation
	oFile.write(index)
oFile.close() 									# Closing the output file
file = "text/" + "text" + str(fCount) + ".txt" 	# Will carry the same process for text tags
oFile = open(file, "w")
for w in sorted(txI) : 							#After making positions we will sort the new text indexes according to format
	index = ",".join(txI[w])
	index = w + "-" + index+"\n" 				# Making the format discussed in presentation
	oFile.write(index)
oFile.close() 									# Closing the output file
fCount += 1 									# After the above steps one file is completed and this process will carry on until 2000 files
for f in fChars :
	heap = [] 
	IFiles = [] 								# Making input files as lists
	file = "text/" + f + ".txt"
	fObject = open(file, "w") 					# Object for opening files
	oFiles.append(fObject) 						# Appending the output files to object
	OFindex = len(oFiles) - 1 					# Length of output file index
	for i in range(fCount) : 					# Making an iterator for files
		file = "text/" + f + str(i) + ".txt"
		if not os.stat(file).st_size == 0 :
			fObject = open(file, "r") 			# We will read the files to append this object
			IFiles.append(fObject) 				# Appending the output files to object
		else :
			try : 								# If any file doesnt hold the formating we remove it
				del IFiles[i] 					# It will help us in searching
				os.remove(file)
			except :
				pass
	if len(IFiles) == 0 : 						# If any input file has nothing we break the loop
		break
	for i in range(fCount) : 					# Iterating the files
		try : 									#Now we will append it with heap to make the lookup time lower
			s = IFiles[i].readline()[:-1]
			heap.append((s, i))
		except :
			pass
	heapify(heap) 								# Applying the heap property to heap
	i = 0
	try :
		while i < fCount : 						# Iterating the new files
			s, index = heappop(heap)
			w = s[: s.find("-")]
			pList = s[s.find("-") + 1 :] 		# Making a posting list for formats
			nL = IFiles[index].readline()[: -1] # Reading next lines
			if nL :  							# Pushing the new lines on heap
				heappush(heap, (nL, index))
			else :
				i += 1
			if i == fCount : 					# If still i = fcount we break it
				break
			while True : 						# Loop on all the objects of heap
				try :
					nST, nIndex = heappop(heap) # Reading next string and next indexes
				except IndexError : 			# If its a index error then break it
					break
				nWord = nST[: nST.find("-")] 	# Reading it word by word
				npList = nST[nST.find("-") + 1 :]	# Doing again with next posting lists
				if nWord == w : 				# After formatting we check if that word founds in list
					pList = pList + "," + npList# If yes then we append with comma
					nLin = IFiles[nIndex].readline()# Reading next lines
					if nLin : 					# If found then pushing it with index on heap
						heappush(heap, (nLin, nIndex))
					else :
						i += 1
				else : 							# Else push next string instead of whole lines
					heappush(heap, (nST, nIndex))
					break 						# and break the process
			if w not in wPosition : 			# If any word has not any position
				wPosition[w] = {} 				# Word position dictionary
			wPosition[w][f] = oFiles[OFindex].tell()# Reverse indexing by finding position in respective file
			psti = pList.split(",") 			# Comma splitted posting lists
			docu = {} 							# Dictionary for each document
			idlog = log10(pCount / len(psti)) 	# tf:idf technique for rankings
			for pst in psti : 					# iterating each posting in posting lists
				d = pst[pst.find("d") + 1 : pst.find(":")] # Finding frequency by colon
				freq = pst[pst.find(":") + 1 :]
				freq = int(freq) 				# casting integer frequency
				tf = 1 + log10(freq) 			# Finding term frequncy
				docu[str(d)] = round(idlog * tf, 2)# Finding collective rank with tf:idf technique
			docu = sorted(docu.items(), key = operator.itemgetter(1), reverse = True) # Getting required items by itemgetter
			nResults = 0
			score = "" 							# Score in sense of frequency
			for document in docu : 				# Getting results in respective document
				if nResults == 10 : 			# Displaying top 10 results
					break 						# and then break it
				score = score + document[0] + ":" + str(document[1]) + "," # After completing each document
				nResults += 1 					# inc each result
			score = score[:-1] + "\n"
			oFiles[OFindex].write(score) 		# Getting score in each output file
	except IndexError : 						# If any index error then break it
		pass
	oFiles[OFindex].close() 					# Closing the output file indexed files
	try : 										# Checking formating of text files
		for i in range(fCount) :
			file = "t/" + f + str(i) + ".txt" 	# According to this format
			IFiles[i].close() 					# Closing correct files
			os.remove(file) 					# Removing other
	except :
		pass
file = open("text/word_positions.pickle", "wb") # Writing binary or positions
pickle.dump(wPosition, file) 					# Dumping the files in pickle
file.close() 									# At last closing all files
index_elapsed_time = time.time() - index_start_time # This will give the time elapsed for results purpose
print "Indexing Time : ", index_elapsed_time
print "File Size : " + str(os.stat(xmlF).st_size * 0.000001) + " MBs" # This will give the files in MBs
# Below line will tell the host computer where this whole process was done
extras.write(socket.gethostname() + "\t" + str(index_elapsed_time) + "\tIndexing\t" + str(os.stat(xmlF).st_size * 0.000001) + " MBs\n" )