import os
from zuc import zuc_function
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

itter = 10
total_val = 0
for ppp in range(0,itter):
    try:
        iv_rand = os.urandom(32/2).encode('hex')
        #print iv_rand
    except:
        iv_rand = "2bd6459f82c5b300952c49104881ff48"
    iv_rand = "0x" + iv_rand
    starting_iv = int(iv_rand,16)
    iv = str(hex(starting_iv))
    iv = iv[2:]

    # Number of iterations
    K = 128#2**20
    n = 4

    #print "--------------------------------------------------------------------------------"
    #print "Number of iterations: " + str(K)
    #print

    start_time = datetime.datetime.now() 
    #print "Start time : ",
    #print start_time

    output = [0] * 2**20


    for i in range(0,2**20):
        iv = str(hex(starting_iv))
        iv = iv[2:]
        output[i] = zuc_function(iv,"2bd6459f82c5b300952c49104881ff48",n)
        if(i % (1024*4) == 0):
            print "Iterations:" + str(i) 
        starting_iv = starting_iv + (itter*128) + 1
        #print starting_iv

    #print bin(output[0])

    #print "End time : ",
    end_time = datetime.datetime.now()
    #print end_time

    #print "Time taken for execution : ",
    #print end_time - start_time
    #print

    # The above makes a 2**20 x 256 matrix
    # Performing Columnar opertations
    relation_factor = [0] * 128

    for i in range(0,2**20+1):
        for j in range(0,128):
            try:
                if((output[i] >> j) & 1):
                    relation_factor[j] = relation_factor[j] + 1
            except:
                relation_factor[j] = relation_factor[j]


    #print relation_factor
    cat = [0] * 5

    for i in range(0,K):
        if(relation_factor[i] < 523850):
            cat[0] = cat[0] + 1
        elif(relation_factor[i] < 524151 and relation_factor[i] > 523850):
            cat[1] = cat[1] + 1
        elif(relation_factor[i] < 524431 and relation_factor[i] > 524149):
            cat[2] = cat[2] + 1
        elif(relation_factor[i] < 524751 and relation_factor[i] > 524430):
            cat[3] = cat[3] + 1
        elif(relation_factor[i] < 1048576 and relation_factor[i] > 524750):
            cat[4] = cat[4] + 1

    #print cat

    expect = [0.00] * 5
    expect[0] = 25#205674.00#expected(0,59,128,128)
    expect[1] = 25#207214.00#expected(59,63,128,128)
    expect[2] = 28#225948.00#expected(63,66,128,128)
    expect[3] = 27#217392.00#expected(66,70,128,128)
    expect[4] = 23#192348.00#expected(70,129,128,128)
    print ("Expected Values: ", expect);
    
    observe = [0.00] * 5
    for i in range(0,5):
        observe[i] = float(cat[i])

    print ("Observed Values: ",observe)

    observed_values = scipy.array([observe[0],observe[1],observe[2],observe[3],observe[4]]);
    expected_values = scipy.array([expect[0],expect[1],expect[2],expect[3],expect[4]]);
    #print ('p-value '),
    a = scipy.stats.chisquare(observed_values, f_exp=expected_values)
    print "ChiSqaure, p-value = " + str(a[1])
    total_val = total_val + a[1]
    #print "Iteration Number: " + str(ppp+1)
print total_val/itter
