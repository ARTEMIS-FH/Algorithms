# RSA bit
from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Random import get_random_bytes 
import Crypto
import libnum

rsabits=128
p = Crypto.Util.number.getPrime(rsabits, randfunc=get_random_bytes)
q = Crypto.Util.number.getPrime(rsabits, randfunc=get_random_bytes)

n = p*q
PHI=(p-1)*(q-1)

e=65537
d=libnum.invmod(e,PHI)


def rsa_encrypt(val):
  return (pow(val,e,n))

def rsa_decrypt(val):
  return (pow(val,d,n)) 

def show_rsa_key():
  print (f"=== RSA key ===\nPublic key: {e},{n}\nPrivate key: {d},{n}\n")  
####