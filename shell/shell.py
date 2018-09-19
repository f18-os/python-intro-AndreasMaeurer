#!/usr/bin/env python3

import sys
import os
import time
import re

shellInput = ""

# function to launch the commands. not containing "/"  taken mostly from p3-exec.py
def launch(args):
	pid = os.getpid()
	#os.write(1, ("About to fork (pid:%d)\n" % pid).encode())		#for debugging
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
cd (a funtion to change directory)
cd Can not change the directory of it's parent if it's a separate program.  So it has to be implemented as a function of the shell
adapted from: https://brennan.io/2015/01/16/write-a-shell-in-c/
"""
def myCD(args):
	if (args[1] == None):							#check if the parameter exists
		print("Correct usage: cd <argument> ")		#print error message if it doesn't exist
	else:		
		(os.chdir(args[1])) 						#then call chdir(path)


# function to handle Input Redirects.  taken mostly from p4-redirect.py  (some overlap with launch() 
# and almost the same as outputRedirects)
def inputRedirect(redirectArgs):
	#print("The INPUT redirect method is runn")			#for debugging DELETE LATER
	#print(redirectArgs)								#for debugging DELETE LATER
	
	#this is specific to INPUT redirection
	i = redirectArgs.index("<")
	#print(i)											#for debugging DELETE LATER
	
	#The arguments. :i is everything before that index
	args = (redirectArgs[:i] + redirectArgs[i+1:])
	#print(args)										#for debugging DELETE LATER
				
	pid = os.getpid()               # get and remember pid

	#os.write(1, ("About to fork (pid=%d)\n" % pid).encode())

	rc = os.fork()

	if rc < 0:
		os.write(2, ("fork failed, returning %d\n" % rc).encode())
		sys.exit(1)

	elif rc == 0:                   # child
		#os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" % (os.getpid(), pid)).encode())
		#args = redirectArgs 	# ["wc", "p3-exec.py"]

		os.close(1)                 # redirect child's stdout
		#this line is gone because we don't need to define an output destination, right?
		#sys.stdout = open(outputFile, "w")			#"p4-output.txt" is now outputFile
		fd = sys.stdout.fileno() # os.open("p4-output.txt", os.O_CREAT)  #Note that from python help: fileno(...)  fileno() -> integer "file descriptor".  This is needed for lower-level file interfaces, such os.read().
		os.set_inheritable(fd, True)
		os.write(2, ("Child: opened fd=%d for writing\n" % fd).encode())  #TODO: decide wheather to keep this line or not

		for dir in re.split(":", os.environ['PATH']): # try each directory in path
			program = "%s/%s" % (dir, args[0])
			try:
				os.execve(program, args, os.environ) # try to exec program
			except FileNotFoundError:             # ...expected
				pass                              # ...fail quietly 

		os.write(2, ("Child:    Error: Could not exec %s\n" % args[0]).encode())
		sys.exit(1)                 # terminate with error

	else:                           # parent (forked ok)
		#os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" % (pid, rc)).encode())
		childPidCode = os.wait()
		#os.write(1, ("Parent: Child %d terminated with exit code %d\n" % childPidCode).encode())


# function to handle Output Redirects.  taken mostly from p4-redirect.py  (some overlap with launch() and inputRedirects)
# "works": wc p3-exec.py > p4-output.txt
# "works" but with wierd warning: uname > cat /tmp/x 
def outputRedirect(redirectArgs):
	#print("The redirect method is runn")		#for debugging DELETE LATER
	#print(redirectArgs)							#for debugging DELETE LATER
	
	#this is specific to output redirection
	i = redirectArgs.index(">")
	#print(i)									#for debugging DELETE LATER
	
	#The arguments. :i is everything before that index
	args = redirectArgs[:i]
	#print(args)									#for debugging DELETE LATER
	
	#The output File (maybe output destination is more descriptive) is whatever comes after the > symbol
	#I assume that the output destination always comes right after the > symbol
	outputFile = redirectArgs[i+1]
	#print(outputFile)
			
	pid = os.getpid()               # get and remember pid

	#os.write(1, ("About to fork (pid=%d)\n" % pid).encode())

	rc = os.fork()

	if rc < 0:
		os.write(2, ("fork failed, returning %d\n" % rc).encode())
		sys.exit(1)

	elif rc == 0:                   # child

		os.close(1)                 # redirect child's stdout
		sys.stdout = open(outputFile, "w")			#now outputFile
		fd = sys.stdout.fileno() # os.open("p4-output.txt", os.O_CREAT)  #Note that from python help: fileno(...)  fileno() -> integer "file descriptor".  This is needed for lower-level file interfaces, such os.read().
		os.set_inheritable(fd, True)
		os.write(2, ("Child: opened fd=%d for writing\n" % fd).encode())  #TODO: decide wheather to keep this line or not

		for dir in re.split(":", os.environ['PATH']): # try each directory in path
			program = "%s/%s" % (dir, args[0])
			try:
				os.execve(program, args, os.environ) # try to exec program
			except FileNotFoundError:             # ...expected
				pass                              # ...fail quietly 

		os.write(2, ("Child:    Error: Could not exec %s\n" % args[0]).encode())
		sys.exit(1)                 # terminate with error

	else:                           # parent (forked ok)
		#os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" % (pid, rc)).encode())
		childPidCode = os.wait()
		#os.write(1, ("Parent: Child %d terminated with exit code %d\n" % childPidCode).encode())


# The main loop of the shell.
while (True):
	# The user can exit the Shell by typing: quit, exit, Quit, Exit, q or Q 
	if ((shellInput == "quit") or (shellInput == "exit") or (shellInput == "Quit") or (shellInput == "Exit") or (shellInput == "q") or (shellInput == "Q")):
		sys.exit()
	
	#some notes on PS1:
	#print("PS1 Variable {}".format(os.environ['PS1']))
	#print("{}".format(os.environ['PS1']))
	#		\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\u@\h:\w\$
	#		\[\e]0;\u@\h: \w\a\]$
		
	#If there is a PS1 (prompt string #1) environment variable, then your shell's prompt should be its value (for test script)
	if ('PS1' in os.environ):
		myPrompt = os.environ['PS1']
	else:
		myPrompt = "$ "
		
	#The input() function allows user input.  (built into Python) 
	#according to: https://github.com/robustUTEP/os-shell the prompt should be: "$ "
	shellInput = input(myPrompt)  			
	
	userInput = shellInput.split()				#Split a string into a list where each word is a list item
	#print("user INPUT is: ")					#for debugging
	#print(userInput)							#for debugging		#TODO: consider deleting this line

	# hit enter without any input the Shell continues in the infinite loop, without issues.
	if not userInput:		#this is what executes when enter is pressed on an empty line
		continue
	
	# before you execute any code check if the arguments match the built in methods (in the end the only built in method is cd)
	# if yes run the built in methods here before the lauch method is reached.
	if (userInput == None):			#keep because cd would not work properly without this line
		continue	
	else:		
		if (">" in userInput):
			#print("yes > [for output redirect]")				#for debugging
			status = outputRedirect(userInput)
			
		if ("<" in userInput):
			#print("yes < [for input redirect]")				#for debugging
			status = inputRedirect(userInput)			
					
		if ((len(userInput) > 1) & (userInput[0] == "cd")):	
			#print("does this line ever get reached?")		
			if (userInput[1] == None):							#check if the parameter exists
				print("Correct usage: cd <argument> ")				
			else:
				myCD(userInput)
		else:
			#print("launch happening now")
			status = launch(userInput)
			
