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
		for dir in re.split(":", os.environ['PATH']): # try each directory in the path
			program = "%s/%s" % (dir, args[0])
			try:
				os.execve(program, args, os.environ) 	# try to exec program
			except FileNotFoundError:             		# ...expected
				pass                              		# ...fail quietly

		sys.exit(1)                 # terminate with error

	else:                           # parent (forked ok)
		childPidCode = os.wait()
		
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

# The main loop of the shell.
while (True):
	# The user can exit the Shell by typing: quit, exit, Quit, Exit, q or Q 
	if ((shellInput == "quit") or (shellInput == "exit") or (shellInput == "Quit") or (shellInput == "Exit") or (shellInput == "q") or (shellInput == "Q")):
		sys.exit()
	print('')									#To go to a newline.  Makes the prompt look nicer.
	shellInput = input('$: ')					#The input() function allows user input.  (built into Python) according to: https://github.com/robustUTEP/os-shell the prompt should be: "$ "
	userInput = shellInput.split()				#Split a string into a list where each word is a list item
	#print("user Input is: ")
	#print(userInput)							#for debugging		#TODO: consider deleting this line

	# hit enter without any input the Shell continues in the infinite loop, without issues.
	if not userInput:
		continue
	
	# before you execute any code check if the arguments match the built in methods
	# if yes run the built in methods here before the lauch method is reached.
	if (userInput == None):
		#print("yes this is what is happening")
		continue	
	else:					
		if ((len(userInput) > 1) & (userInput[0] == "cd")):			
			if (userInput[1] == None):							#check if the parameter exists
				print("Correct usage: cd <argument> ")				
			else:
				myCD(userInput)
		else:
			status = launch(userInput)
			
