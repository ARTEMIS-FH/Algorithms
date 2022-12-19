from Crypto.Util.number import getPrime
from Crypto.Random import get_random_bytes
from random import randint
import libnum

primebits=60


def genparams():
    p = getPrime(primebits, randfunc=get_random_bytes)
    q = getPrime(primebits, randfunc=get_random_bytes)
    n = p*q
    g=n
    while (gcd(g,n*n)!=1):
      g = randint(20,150)

    gLambda = lcm(p-1,q-1)
    l = (pow(g, gLambda, n*n)-1)//n
    gMu = libnum.invmod(l, n)
    return gLambda, n, g, gMu,primebits




def L(x,n):
	return ((x-1)//n)

def gcd(a,b):
    """Compute the greatest common divisor of a and b"""
    while b > 0:
        a, b = b, a % b
    return a
    
def lcm(a, b):
    """Compute the lowest common multiple of a and b"""
    return a * b // gcd(a, b)