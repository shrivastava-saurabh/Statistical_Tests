import os
from espresso import espresso_function
import datetime
import operator as op
import scipy
from scipy.stats import chisquare
import binascii
from functools import reduce

def bitcout(number):
    a = number
    count = 0
    for jj in range(0,128):
        x = a>>jj
        if(x&1):
            count = count + 1
    return count

# Definition for finding Expected Value
def expected(lb,ub,iv_size,iterations):
    exp = 0
    val = float(0.5)**iv_size
    
    for i in range(lb,ub):
        exp = exp + float(ncr(iv_size,i))
    
    return val*exp*iterations

def ncr(n,r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    
    #print float(numer / denom)
    return float(numer / denom)



# Testing hundred iterations with IV fixed and K number of keys
# Let K = 100 here
itter = 1
total_val = 0
for ppp in range(0,itter):
    K = 2**20
    print "--------------------------------------------------------------------------------"
    #print "Number of iterations = " + str(K)

    iv = ['0']*K
    output = [0]*K
    relation_factor = [0.0]*K
    relation = 0
    total_probability = 0.00


    for i in range(0,K):
        iv[i] = os.urandom(24/2).encode('hex')
        nn = "0x" + iv[i]
        output[i] = espresso_function("0",iv[i],4)
        output[i] = hex(output[i])
        temp = output[i]
        output[i] = temp[0:24+2]
        output[i] = int(output[i],16) 
        relation = output[i]^int(nn,16)
        relation_factor[i] = bitcout(relation)
        if(i % 1024 == 0):
            print "Iteration: " + str(i)

    for i in range(0,K):
        total_probability = total_probability + relation_factor[i]
    total_probability = total_probability/(128*K)

    cat = [0] * 5

    for i in range(0,K):
        if(relation_factor[i] < 45):
            cat[0] = cat[0] + 1
        elif(relation_factor[i] < 48 and relation_factor[i] > 44):
            cat[1] = cat[1] + 1
        elif(relation_factor[i] < 51 and relation_factor[i] > 47):
            cat[2] = cat[2] + 1
        elif(relation_factor[i] < 54 and relation_factor[i] > 50):
            cat[3] = cat[3] + 1
        elif(relation_factor[i] < 97 and relation_factor[i] > 53):
            cat[4] = cat[4] + 1


    expect = [0.00] * 5
    expect[0] = 217220.00#expected(0,59,128,K)
    expect[1] = 222286.00#expected(59,63,128,K)
    expect[2] = 250901.00#expected(63,66,128,K)
    expect[3] = 196932.00#expected(66,70,128,K)
    expect[4] = 161237.00#expected(70,129,128,K)

    print ("Expected Values: ", expect);

    observe = [0.00] * 5
    for i in range(0,5):
        observe[i] = float(cat[i])

    print ("Observed Values: ",observe)

    observed_values = scipy.array([observe[0],observe[1],observe[2],observe[3],observe[4]]);
    expected_values = scipy.array([expect[0],expect[1],expect[2],expect[3],expect[4]]);
    #print ('p-value '),
    a = scipy.stats.chisquare(observed_values, f_exp=expected_values);
    print "ChiSqaure, p-value = " + str(a[1])
    total_val = total_val + a[1]
    #print "Iteration Number: " + str(ppp+1)
print total_val/itter
