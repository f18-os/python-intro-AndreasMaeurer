#!/usr/bin/env python3

"""
Andreas Maeurer
September 17th 2018
Theory of OS Fall 2018

Collaborated:	I discussed redirection with Stephanie Medina
				With Sergio Ponce De Leon I discussed how to set up the shell to print to the File Descriptor
"""

import sys
import os
import time
import re

shellInput = ""

# function to launch the commands.  taken mostly from p3-exec.py
def launch(args):
	pid = os.getpid()
	os.write(1, ("About to fork (pid:%d)\n" % pid).encode())		#for debugging
	rc = os.fork()	
	
	if rc < 0:
		os.write(2, ("fork failed, returning %d\n" % rc).encode())
		sys.exit(1)
		
	elif rc == 0:                   # child
		#os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" % (os.getpid(), pid)).encode())		#for debugging
		#args = ["wc", "AMshell.py"]
		for dir in re.split(":", os.environ['PATH']): # try each directory in the path
			program = "%s/%s" % (dir, args[0])
			#os.write(1, ("Child:  ...trying to exec %s\n" % program).encode())
			try:
				os.execve(program, args, os.environ) 	# try to exec program
			except FileNotFoundError:             		# ...expected
				pass                              		# ...fail quietly

		#os.write(2, ("Child:    Could not exec %s\n" % args[0]).encode())							#for debugging
		sys.exit(1)                 # terminate with error

	else:                           # parent (forked ok)
		#os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" % (pid, rc)).encode())					#for debugging
		childPidCode = os.wait()
		#os.write(1, ("Parent: Child %d terminated with exit code %d\n" % childPidCode).encode())	#for debugging

"""
cd (change directory) Can not change the directory of it's parent if it's a separate program.  So it has to be implemented as a function of the shell
adapted from: https://brennan.io/2015/01/16/write-a-shell-in-c/
It checks for errors, and returns
"""
def myCD(args):
	if (args[1] == None):							#check if the parameter exists [or should that be done below?]
		print("Correct usage: cd <argument> ")		#print error message if it doesn't exist
	else:		
		#print("What is parameter at this point: " + parameter)	#for debugging		#TODO: consider deleting this line
		(os.chdir(args[1])) 						#then call chdir(path)
		
"""
exit and cd work
Should a help function be implemented?
if so, what info should it print out to the user?
If it's not required, I'm leaving it out.
"""

"""
BUG:  When you hit enter without any input the Shell exits (CRASHES!)
"""

# The main loop of the shell.
while (True):
	# The user can exit the Shell by typing: quit, exit, Quit, Exit, q or Q 
	if ((shellInput == "quit") or (shellInput == "exit") or (shellInput == "Quit") or (shellInput == "Exit") or (shellInput == "q") or (shellInput == "Q")):
		sys.exit()
	print('')									#To go to a newline.  Makes the prompt look nicer.
	shellInput = input('$: ')					#The input() function allows user input.  (built into Python) according to: https://github.com/robustUTEP/os-shell the prompt should be: "$ "
	userInput = shellInput.split()				#Split a string into a list where each word is a list item
	print("user Input is: ")
	print(userInput)							#for debugging		#TODO: consider deleting this line
	# os.write(1, ("%s\n" % userInput).encode())  # for debugging	#1 is the File Descriptor, right?  #TODO: consider deleting this line
	
	#validate(userInput)
	
	
	# before you execute any code check if the arguments match the built in methods
	# if yes run the built in methods here before the lauch method is reached.
	if (userInput == None):
		print("yes this is what is happening")
		continue	
	else:					
		if ((len(userInput) > 1) & (userInput[0] == "cd")):
			# BUG BUG BUG: Maybe I should check at this point if the Parameter exits?
			if (userInput[1] == None):							#check if the parameter exists						#BUG BUG BUG: When you type in cd by itself it crashes here.
				print("Correct usage: cd <argument> ")
			#print("this line has been reached") #for debugging		#TODO: consider deleting this line
			else:
				myCD(userInput)
		else:
			status = launch(userInput)
			
	"""
	
	if (len(userInput) > 0):
		if (userInput[0] == "cd"):
			# BUG BUG BUG: Maybe I should check at this point if the Parameter exits?
			if (userInput[1] == None):							#check if the parameter exists						#BUG BUG BUG: When you type in cd by itself it crashes here.
				print("Correct usage: cd <argument> ")
			#print("this line has been reached") #for debugging		#TODO: consider deleting this line
			else:
				myCD(userInput[1])
	else:
		status = launch(userInput)
	"""
	
	"""
	if (userInput == None):
		print("yes this LInE HerE Is bEIng rEAcheD")
		continue
	else:
		status = launch(userInput)
	"""
