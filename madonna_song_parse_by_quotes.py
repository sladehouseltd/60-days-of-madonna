songCounter = 0
songArray = []

with open('madonna_all_songs_wikipedia.txt') as file_object:
#	contents = file_object.read()
	for line in file_object:
		print(line)
		if line[0] == "\"":
			songCounter = songCounter + 1 
			#songArray.append(line)
			songString = line.split("\"")[1]
			songArray.append(songString)

print(songCounter)

print(songArray)


outputFile = 'parsedSongList.txt'

with open(outputFile,'w') as file_object:
	for song in songArray:
		file_object.write(str("\"" + song + "\","))
		file_object.write("\n")

#print(contents)

#myString="Hello there !bob@"
#mySubString=myString[myString.find("!")+1:myString.find("@")]
#print(mySubString)

#songString = contents[contents.find("\"")+1:contents.find("\"")]
