chkcmd "/bin/uname" "no parameter, full pathname"
chkcmd "/bin/uname \n /bin/uname" "two commands, full pathname"
chkcmd "/bin/uname \n\n /bin/uname" "two commands, blank line in-between, full pathname"
chkcmd "uname" "no parameter, no pathname"													#must pass this one
chkcmd '/bin/cat /etc/passwd' "one parameter, full pathname"
chkcmd 'cat /etc/passwd' "one parameter, no pathname"										#should pass this one
chkcmd 'cat /etc/passwd | sort ' "pipe"
chkcmd 'cat /etc/passwd | sort | wc ' "2 pipes"
chkcmd 'cat < /etc/passwd' "redirect input"													#should pass this one
chkcmd 'uname > /tmp/x \n cat /tmp/x' "redirect output"
(echo "sleep 1" ; echo "echo 1") > /tmp/c1
chkcmd 'bash < /tmp/c1 &\n echo 2 \n sleep 3' "background"
chkcmd 'cd .. \n pwd' "change dir"															#must pass this one


question about the \n 
newlines in the .sh file

The part about the PATH I think he talked about it last week. so idk


/bin/uname
/bin/uname \n /bin/uname
/bin/uname \n\n /bin/uname
uname
/bin/cat /etc/passwd
cat /etc/passwd
cat /etc/passwd | sort 
cat < /etc/passwd
bash < /tmp/c1 &\n echo 2 \n sleep 3
cd .. \n pwd

uname > /tmp/x \n cat /tmp/x' "redirect output"
(echo "sleep 1" ; echo "echo 1") > /tmp/c1

