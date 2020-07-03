POODLE ​stands for ( ​P​adding ​O​racle ​O​n ​D​owngraded ​L​egacy ​E​ncryption). In this  vulnerability, an attacker has to be a Man-in-the-Middle(MiTM).  When cipher block chaining is combined with SSLv3.0, padding is required to make  the cipher blocks of constant size. This attack exploits the padding method to get  access to 1 character from the message at a time. 
This is a simulation of the POODLE attack in ssl v3 protocol. For the proof of concept, it is shown how an attacker who has access to the encrypted message can use this vulnerability to decode the message.  

### INTRODUCTION:

1. The report contains the following things:
	- SSL in general, and about v3.0 focussing on things that causes POODLE  
	- About POODLE, How can it be implemented, its impacts, measures to safeguard against it. 
	- On paper implementation of you as an attacker trying to exploit this vulnerability, explaining your code and its nuances 
2. The code *poodle.py* contains the encryption/decryption functions, with the sslv3 protocol. And further demonstrates the poodle attack on the protocol. The code is well documented and the print output on the console helps to understand the state of the code at any point.


### PRE-REQUISITE:

1. code is written/tested in Python3
2. pycryptodome library is required, which can be istalled as :
	```
	pip install pycryptodome or
	pip3 install pycryptodome
	```

### HOW TO RUN:

1. The code can be simply run by the typing the following command on cmd:
	```
	python poodle.py
	```
   
   It shows the simulation of attack on the default message
   > msg = "hello this is secret and it should not be disclosed in any situation."

2. To run on any other plaintext:
   change the line:102 in the file "poodle.py" as:
   > msg = any string you want with length > 32

   the plaintext length should be atleast greater than 32, as in the attack,
 character at the index 32 is decoded one-by-one.


