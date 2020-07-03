#!/usr/bin/env python
# coding: utf-8

# In[45]:


from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Hash import HMAC
from Crypto import Random


# In[46]:



# Encrypt function which takes a plaintext and the
# encryption key as an argument, and returns the ciphertext

def encrypt(plaintext, aes_key):
    
    # Generate a random IV
    iv = Random.new().read(AES.block_size)
    
    # Generate the MAC for the plaintext
    h = HMAC.new(b'topsecret')
    h.update(bytes(plaintext, 'ascii'))
    mac = h.digest()
    # Add MAC to the plaintext before encryption
    text_with_mac =  bytes(plaintext, 'ascii') + mac
    
    # Compute the padding to be inserted
    len_padding = 16 - len(text_with_mac)%16
    if(len_padding == 0):    # if integral multiple then add a whole block
        len_padding=16
    for i in range(len_padding):  # otherwise add suitable padding bytes
        text_with_mac += (bytes([len_padding])) 
    padded_text_with_mac = text_with_mac
    
    # Encrypt plaintext | MAC
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(padded_text_with_mac)
    
    # return encrypted text along with the IV
    return iv + ciphertext


# In[47]:



# Decrypt function takes the encoded message, and the encryption key
# as argument and returns success/failure depending on the mac verification.

def decrypt(enc_message, key):
  
    # Get the IV from the message
    iv = enc_message[0:16]
    ciphertext = enc_message[16:]
    
    # Decrypt the message
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decr_message = cipher.decrypt(ciphertext)
    pad_length = decr_message[-1]   # last byte is the pad-length

    decr_message = decr_message[:-pad_length] # remove the padding
    mac = decr_message[-16:]                  # remove the old MAC
    plaintext = decr_message[:-16]      # remaining is the decrypted palintext
    
    # Compute the new MAC, of the decrypted plaintext
    h = HMAC.new(b'topsecret')
    h.update(plaintext)
    computed_mac = h.digest()
    
    # If the computed MAC equals the ciphertext MAC, return success
    if computed_mac == mac:
        return 1    #print("decryption success")
    #else:
        #print("decryption invalid !")
    return 0


# In[48]:



# helper function to rotate the plaintext byte-wise to obtain all the bytes
# at last byte of P2, one by one
def rotate_message(msg):   
    new_msg = msg[-1] + msg[:-1]
    return new_msg

# helper function to rearrange all the decoded characters to form the original plaintext
def rearrange(msg):
    decoded_msg = ''
    length = len(msg)
    for i in range(length):
        decoded_msg += msg[(length + 31-i)%length]
    return decoded_msg

# generate any plaintext message.
msg = "hello this is secret and it should not be disclosed in any situation."

# generate an encryption key
key = get_random_bytes(16)

# the actual function to perform the attack on the plaintext (msg)
def hack():
    print("The plaintext message is : \n","'",msg,"'\n")
    print("The key is : ",key,"\n")
    #local variable for msg
    temp_msg = msg
    # tweak the message length so that, it is integral multiple of block size(16)
    if(len(temp_msg)%16 != 0):
        for i in range(16-len(temp_msg)%16):
            temp_msg += '#'
    
            
    decoded_msg =''   #will finally contain the decoded plaintext
    
    print("----------- Starting to decode the message -----------")
    number_of_chars_decoded = 0
    
    # find all the characters one by one in the loop. the plaintext is rotated in the loop
    # so that all characters come as last byte of C2 one-by-one
    for i in range (len(temp_msg)):
        count = 0  # to count the number of iterations taken to compute each character
        
        # loop runs till the character is decoded
        # i.e, 15 comes as last byte of decrypted text D, after the decryption
        # on an average it takes 256 iterations.
        while(1):  
            count+=1
            enc_message = encrypt(temp_msg,key)  #encrypt the plaintext
            # second block of plaintext as C0 is IV
            c2_block = enc_message[32:48]    
            #replace the last block of enc_m(Cn) with C2, as we want to find the last byte corresponding to C2 
            enc_message = enc_message[:-16] + c2_block     
           
            # if decryption succeeds even after the above replacement, then we are sure that 
            # decryption of last byte of C2 is 16.
            # then we can use the formula :
            #  P2[15] = Cn-1[15]  xor C1[15]  xor 16
            # to find the plaintext character.
            # in this implementation, it is the 32 chacter of plaintext.
            if(decrypt(enc_message,key)!=0):
                print("decryption success")
                c2_last = enc_message[31]
                cnminus1_last = enc_message[-17]
                found_byte = cnminus1_last^c2_last^16
                char = chr(found_byte)
                if(char!='#'):
                    decoded_msg +=char
                    number_of_chars_decoded += 1
                    print("number of characters decoded till now: ",number_of_chars_decoded)
                    print("character decoded : '",chr(found_byte),"'")
                    print("actual location in the plaintext : ",(32-number_of_chars_decoded+len(msg))%len(msg))
                    print("decoded after ",count," iterations.")
                    print("scrambled decoded string till now: '",decoded_msg,"'")
                    print("------")
                    print("")
                break
        new_msg = rotate_message(temp_msg)   # rotate the msg to find the next character
        temp_msg = new_msg
    print("Scrambled string obtained after attack : ")    
    print(decoded_msg,"\n")
    
    decoded_msg = rearrange(decoded_msg)
    print("Final rearranged string : ")
    print(decoded_msg)
        
    
hack() 


# In[49]:





# In[ ]:




