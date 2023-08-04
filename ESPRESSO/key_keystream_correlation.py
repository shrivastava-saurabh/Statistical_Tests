import os
from espresso import espresso_function
import datetime
import operator as op
import scipy
from scipy.stats import chisquare
from functools import reduce

p = [0.000000000000]*2;
# Definition for nCr
def ncr(n,r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    
    #print float(numer / denom)
    return float(numer / denom)

# Definition for finding Expected Value
def expected(lb,ub,key_size,iterations):
    exp = 0
    val = float(0.5)**key_size
    
    for i in range(lb,ub):
        exp = exp + float(ncr(key_size,i))
    
    return val*exp*iterations

# This function finds the weight of a given value
def bitcout(number):
    a = number

    count = 0
    for jj in range(0,128):
        x = a >> jj
        if(x&1):
            count = count + 1
    
    return count

itter = 1
total_val = 0
for ppp in range(0,itter):
    # Testing hundred iterations with IV fixed and K number of keys
    # Let K = 100 here
    K = 2**20
#K=100;
    print "-----------------------------------------------------------"
    #print "Number of iterations = " + str(K)


    key = ['0']*K
    output = [0]*K
    relation_factor = [0.0]*K
    relation = 0
    total_probability = 0.00

    #Printing Start Time
    start_time = datetime.datetime.now()
    #print "Start time : ",
    #print start_time

    for i in range(0,K):
        key[i] = os.urandom(32/2).encode('hex')
    
        nn = "0x" + key[i]

        output[i] = espresso_function(key[i],"0",4)
        relation = output[i]^int(nn,16)
        if(i % 1024 == 0):
            print "Iteration: " + str(i)
        relation_factor[i] = bitcout(relation)
        #print relation_factor[i]
    end_time = datetime.datetime.now()
    #print "End time : ",
    #print end_time

    #print "Time taken for execution : ",
    #print end_time - start_time
    #print 



    #print "Defined ranges: "
    #print "Range 1 : 0 - 58"
    #print "Range 2 : 59 - 62"
    #print "Range 3 : 63 - 65"
    #print "Range 4 : 66 - 69"
    #print "Range 5 : 70 - 128"

    cat = [0] * 5

    for i in range(0,K):
        if(relation_factor[i] < 59):
            cat[0] = cat[0] + 1
        elif(relation_factor[i] < 63 and relation_factor[i] > 58):
            cat[1] = cat[1] + 1
        elif(relation_factor[i] < 66 and relation_factor[i] > 62):
            cat[2] = cat[2] + 1
        elif(relation_factor[i] < 70 and relation_factor[i] > 65):
            cat[3] = cat[3] + 1
        elif(relation_factor[i] < 129 and relation_factor[i] > 69):
            cat[4] = cat[4] + 1


    expect = [0.00] * 5
    expect[0] = 205674.00#expected(0,59,128,128)
    expect[1] = 207214.00#expected(59,63,128,128)
    expect[2] = 225948.00#expected(63,66,128,128)
    expect[3] = 217392.00#expected(66,70,128,128)
    expect[4] = 192348.00#expected(70,129,128,128)
    print ("Expected Values: ", expect);
    
    #print expect

    observe = [0.00] * 5
    for i in range(0,5):
        observe[i] = float(cat[i])

    print "Observed Values: ",
    print observe

    observed_values = scipy.array([observe[0],observe[1],observe[2],observe[3],observe[4]]);
    expected_values = scipy.array([expect[0],expect[1],expect[2],expect[3],expect[4]]);
    #print ('p-value '),
    a = scipy.stats.chisquare(observed_values, f_exp=expected_values);
    print "ChiSqaure, p-value = " + str(a[1])
    total_val = total_val + a[1]
    #print "Iteration Number: " + str(ppp+1)
print total_val/itter
