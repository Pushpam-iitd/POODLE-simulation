
PRE-REQUISITE:

1. code is written/tested in Python3
2. pycryptodome library is required, which can be istalled as :
	pip install pycryptodome or
	pip3 install pycryptodome

HOW TO RUN:

1. The code can be simply run by the typing the following command on cmd:
	python assignment_3.py

   It shows the simulation of attack on the default message
   msg = "hello this is secret and it should not be disclosed in any situation."

2. To run on any other plaintext:
   change the line:102 in the file "assignment_3.py" as:
   msg = any string you want with length > 32

   the plaintext length should be atleast greater than 32, as in the attack,
 character at the index 32 is decoded one-by-one.


