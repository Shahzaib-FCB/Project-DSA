from importing import *
import operator
import time 									# Library for getting time for queries
import socket 									# For getting host computer name

searchtimes= open("searchTime.txt", "a") 		# Text file for getting search timings for queries
tTags = open("text/title_tags.txt", "r")
tPosition = pickle.load(open("text/title_positions.pickle", "rb")) 	# Reading binary of Title positions using pickle
wPosition = pickle.load(open("text/word_positions.pickle", "rb"))	# Reading binary of w positions using pickle
field_map = {"title" : 0, "text" : 1} 			# Dictionary made for finding both things easily
files = [] 										# This list will contain files
for f in fChars : 								# Getting field characters from importing file
	file = "text/" + f + ".txt" 				# Making these text files
	fObject = open(file, "r") 					# Reading files
	files.append(fObject)	 					# Appending the object of read
while True :
	result_bags = []  							# List for getting results
	documents = {} 								# Dictionary for accessing documents
	user_queries = [] 							# User queries as a list 
	search_queries = raw_input("search> ")		# These are the inputs of queries
	q = search_queries
	search_queries = search_queries.lower().strip() 	# Lowering them and then are getting stripped
	start = time.time() 						# For getting time
	if (search_queries == "exit") : 			# If someone type exit then program ends
		break
	else : 										# This will check for multi words
		search_queries_bag = search_queries.split() 	# Splitting the queries
		length = len(search_queries_bag) 		# Finding length of them
		for w in search_queries_bag : 			# Getting each w of queries
			if w not in stop_words and w in wPosition: 	# Check for stop words
				user_queries.append(w) 			# Appending them in lists
		for w in user_queries : 				# Now we will find their positions
			positions = wPosition[w]
			for field in positions : 			# Getting each field of field map as mentioned above
				position = positions[field] 	# Each position of word
				files[field_map[field]].seek(position) 	# Getting positions in files list
				s = files[field_map[field]].readline()[: -1] # Getting each line of them
				if "," in s : 					# As the line were comma separated 
					dc = s.split(",") 			# So we splitted them against comma
					for d in dc :	 			# Iterating each document
						document, score = d.split(":") 	# Getting the document and its score by splitting against colon
						if document not in documents : 	# If we cannot find respective document
							documents[document] = 0.0	# We give score of 0.0
						documents[document] += float(score) # By casting it
				else :
					document, score = s.split(":") 		# Else we split them against colon
					if document not in documents : 		# If we cannot find respective document
						documents[document] = 0.0 		# We give score of 0.0
					documents[document] += float(score)
	documents = sorted(documents.items(), key = operator.itemgetter(1), reverse = True) # We sorted the document items and got the key using itemgetter
	nResults = 0 								# Initializing number of documents
	for document in documents :
		position = tPosition[int(document[0]) - 1] 		# Getting title positions in documents
		tTags.seek(position) 					# Positions of title tags
		title = tTags.readline()[: -1]
		result_bags.append(title) 				# Then we appended the results at the end
		nResults += 1 							# And incremented it for counting purpose
	searchtime = time.time() - start 			# This will give us search time
	if len(result_bags) == 0 : 					# If length is 0 then it means there is not any result of that query
		print "No reults found"
		print "Time taken - " + str(searchtime) + "s" 	# Time taken for searching
	else :
		print "results retrieved in - " + str(searchtime) + "s"

	for result in result_bags : 				# Printing the results
		print result

	print "Total Number of results : ", nResults 
    # The below line tells the search computer with no of results and their timing 
	searchtimes.write(socket.gethostname() + "\t" + str(nResults) + "\t\t" +str(searchtime) + "\t\t" + q +'\n') 