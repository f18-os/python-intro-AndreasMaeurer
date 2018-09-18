#!/usr/bin/env python3

"""
Andreas Maeurer
September 17th 2018
Theory of OS Fall 2018

Collaborated:	I discussed redirection with Stephanie Medina
				With Sergio Ponce De Leon I discussed how to set up the shell to print to the File Descriptor
"""
"""
exit and cd work
Should a help function be implemented?
if so, what info should it print out to the user?
If it's not required, I'm leaving it out.
"""

import sys
import os
import time
import re

shellInput = ""

# Method to launch the commands.  Taken mostly from p3-exec.py
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
# Method to change directory
def myCD(args):
	if (args[0] == "cd"): 			#check if the parameter is "cd" (If we write no path (only 'cd'), then return out of this method)
		return 1	
	else:							# Else we change the directory to the one specified by the argument, (if possible)
		(os.chdir(args[1])) 		#then call chdir(path)
		return 0

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
		
	# hit enter without any input the Shell continues in the infinite loop, without issues.
	if not userInput:
		continue
	
	if (userInput[0] != "cd"):
		status = launch(userInput)
	else:
		myCD(userInput)
		
