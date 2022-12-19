
import libnum
from params import genparams,primebits
import numpy as np
import random
from rsa import rsa_encrypt,rsa_decrypt,show_rsa_key,rsabits
import sys

# Demo times select 10 samples for time differences with up to 100 seconds in-between. Search with homomorphic encryption for a time difference of less than 20 seconds
starttime=1614205069
endtime=starttime+100
timediff=20 # 10 second difference
num=10 # number of samples


def encrypt(k,r):
  k1=pow(g,k,n*n)
  k2=pow(r,n,n*n)
  return pow(k1*k2,1,(n*n))

def decrypt(cipher):
  l = (pow(cipher, gLambda, n*n)-1) // n
  mess= pow((l * gMu),1, n)
  return mess

def add(cipher,cipher2):
  return pow((cipher* cipher2),1, (n*n))

def sub(cipher,cipher2):
  v1=(cipher* (libnum.invmod(cipher2,n*n)) % (n*n))
  v2=(cipher2* (libnum.invmod(cipher,n*n)) % (n*n))
  return v1,v2

def L(x,n):
	return ((x-1)//n)



######## Encrypting
gLambda, n, g, gMu, primesize = genparams()

r=random.randint(0,2e72)

print (f"RSA bits {rsabits}, primebit {primebits}")

if (2*primebits>rsabits):
  print("*** RSA key size must be at least twice homomorphic encryption key size ***")
  sys.exit()

a = np.random.randint(starttime,high=endtime, size=num)
b = np.random.randint(starttime,high=endtime, size=num)
contacts = np.random.randint(0,high=10, size=num)



enc_a = []
enc_b = []
enc_contacts = []

for i in range(0,len(a)):
  enc_a.append( rsa_encrypt(encrypt(int(a[i]),r)))
  enc_b.append( rsa_encrypt(encrypt(int(b[i]),r)))
  enc_contacts.append( encrypt(int(contacts[i]),r))

show_rsa_key()

print (f"=== Homomorphic key ===\nPublic key: g={g}, n={n}\nPrivate key: lambda={gLambda}, Mu={gMu}\n")
print (f"Samples: ={num}\n")
print (f"Time difference: {timediff} seconds\n")
print (f"Contacts: {contacts}\n")


contacts_total=encrypt(0,r)
count=0
for i in range(0,len(a)):
  cipher2_1,cipher2_2 = sub(rsa_decrypt(enc_a[i]),rsa_decrypt(enc_b[i]))
  mess1= decrypt(cipher2_1)
  mess2= decrypt(cipher2_2)
  res=mess1
  if (mess1>n/8): res=mess2
  if (res<timediff): 
    print(f"{(i)} - Time1={a[i]},Time2={b[i]}. Diff: {res}")
    print(f"  Enc={enc_a[i]},Enc={enc_b[i]}")
    contacts_total=add(contacts_total,enc_contacts[i])

contacts_final_total=decrypt(contacts_total)
print(f"\nContacts (enc)={contacts_total}")
print(f"\nContacts={contacts_final_total}")