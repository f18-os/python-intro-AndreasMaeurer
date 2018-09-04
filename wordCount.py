"""
Andreas Maeurer
September 3rd 2018
Theory of Operating Systems Fall 2018
"""
"""
This repository contains the code for the python introduction lab. The purpose is to have a fairly simple python assignment that 
introduces the basic features and tools of python

In the repository are two plain text files with lots of words. Your assignment is to create a python 2 program which:

    * takes as input the name of an input file and output file
    
    * example: 
		$ python wordCount.py input.txt output.txt

    * keeps track of the total the number of times each word occurs in the text file
    
    * excluding white space and punctuation
    
    * is case-insensitive
    
    * print out to the output file (overwriting if it exists) the list of words sorted in descending order with their respective totals 
      separated by a space, one word per line
"""
"""
To test your program we provide wordCountTest.py and two key files. This test program takes your output file and notes any 
differences with the key file. An example use is:

$ python wordCountTest.py declaration.txt myOutput.txt declarationKey.txt

The re regular expression library and python dictionaries should be used in your program.
"""

#! /usr/bin/env python3

import sys        # command line arguments
import re         # regular expression tools
import os         # checking if file exists

# set input and output files (same as in sample file)
if len(sys.argv) is not 3:
    print("Correct usage: wordCount.py <input text file> <output file>")
    exit()
    
textFname = sys.argv[1]
outputFname = sys.argv[2]

#stats (similar to sample file)
wordArray = []
#output = open(outputFname, 'w')										#for Debugging   #Not sure which error to leave in and which error to correct...
output = open("tempArray.txt", 'w')										#for Debugging	#I can't figure out how to touch the output file withouth making the rest of the program crash

#f= open(outputFname,"w+")
#f.close()

# Reading a text file and splitting it into single words				#I can't figure out how to touch the output file withouth making the rest of the program crash
with open(textFname,'r') as inputFile:
    for line in inputFile:
        for word in line.split():
           # print(word)												#display on Screen for Debugging
           word = word.replace(',', '')									#throw out the commas
           word = word.replace('.', '')                      			#throw out the periods
           word = word.replace(':', '')									#throw out the colons
           word = word.replace(';', '')									#throw out the semi colons
           word = word.replace('-', '')									#throw out the "minus sign" or the "dash" or whatever it's called
           wordArray.append(str(word).lower())							#append the current string to the wordArray (as a lowercase word)
           output.write(word + "\n")

print ("-----------------------------------------------------------------001")		#for Debugging
print(wordArray)

#so up to this point:
# the wordArray has all the words in the declaration
# and the same has been written to the text file 

#next task: sort the array alphabetically
print ("-----------------------------------------------------------------002")		#for Debugging
wordArray.sort() 
print(wordArray)

#next task: count the number of duplicates
print ("-----------------------------------------------------------------003")		#for Debugging
from collections import Counter
wordCount = Counter(wordArray)
print (wordCount.values())

print ("-----------------------------------------------------------------004")		#for Debugging
print (wordCount.keys())

print ("-----------------------------------------------------------------005")		#for Debugging
print(wordArray)

theWordCountValues = wordCount.values()
print (theWordCountValues)

theWordCountKeys = wordCount.keys()
print (theWordCountKeys)
print ("-----------------------------------------------------------------006")		#for Debugging

newArray = []
#are there no proper for loops in python?
i = 0
while i < len(wordCount):
	newArray.append(theWordCountKeys[i] + " " + str(theWordCountValues[i]))
	i+=1
print (newArray)

print ("-----------------------------------------------------------------007")		#for Debugging
newArray.sort()
print (newArray)

#get the sorted list into the output file
i = 0
with open(outputFname,'w') as f:
	while i < len(wordCount):		
		f.write(newArray[i] + "\n")
		i+=1
print (newArray)
