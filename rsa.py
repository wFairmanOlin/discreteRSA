import sympy
import random
import time

count = 0
"""
private keys
--> d
--> p
--> q
public keys
--> k
--> n
"""

"""
generate both private and public keys

upperBound: maximum value for p & q
"""
def generateKeys(upperBound):
    p = sympy.randprime(1e1, upperBound)
    q = sympy.randprime(1e1, upperBound)
    n = p*q

    #calculating totient
    phi = (p-1)*(q-1)

    k = []
    for i in range(2, phi):
        if phi % i != 0:
            k.append(i)

    #choose smallest k, calc d
    fail = True
    for x in k:
        fail = True
        for i in range(1000):
            i += 1
            d = (1 + i*phi)/x
            if (d % 1 == 0):
                k = x
                fail = False
                break
        if not fail:
            break

    if fail:
        raise 'ahhh'

    return p,q,n,k,d

"""
generate public and private keys with k == 65537
"""
def generateKeysK(upperBound):
    p = sympy.randprime(1e1, upperBound)
    q = sympy.randprime(1e1, upperBound)
    n = p*q

    #exponent dict
    keys = {}

    #calculating totient
    phi = (p-1)*(q-1)
    k = 65537
    pKey = []

    fail = True
    for i in range(2,k-1):
        i += 1
        d = (1 + i*phi)/k
        if (d % 1 == 0):
            pKey.append(d)
            fail = False
            break

    #choose smallest value for d
    d = pKey[0]

    if fail:
        raise 'ahhh'

    return p,q,n,k,d

"""
modular exponetiation
x: base
e: exponent
m: modulus

from: http://www-users.math.umn.edu/~garrett/crypto/Code/FastPow_Python.html
thanks umn!
"""
def f(x,e,m):
    X = x
    E = e
    Y = 1
    while E > 0:
        if E % 2 == 0:
            X = (X * X) % m
            E = E/2
        else:
            Y = (X * Y) % m
            E = E - 1
    return Y

"""
encrypt message with public keys
"""

def encryptMessage(k, n):
    m = ord(input("character here: "))
    c = f(m,k,n)
    print('og message:',m)
    print('encrypted:', c)
    return c

"""
decrypt message with private keys
"""
def decryptMessage(c, d, n):
    m = f(c,d,n)
    print('encrypted message:', c)
    print('decrypted message:', m)
    return m

"""
calculate d with public key, p, and q
"""
def findD(k, n, p, q):
    totient = (p-1)*(q-1)
    for i in range(2,n):
        if (i*totient + 1)/k % 1 == 0:
            return (i*totient + 1)/k


#quick example
p,q,n,k,d = generateKeys(1e2)
print(p,q,n,k,d)
c = encryptMessage(k,n)
m = decryptMessage(c,d,n)
print(chr(m))
print(findD(k,n,p,q))