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

total = [0] * 224
a = '0'
for i in range(0,224):
    total[i] = list(a.zfill(1024))

itter = 1024
total_val = 0
iv_init = [0]* itter;
key_init= [0] * itter;
for i in range (itter):
    try:
        iv_init[i] = os.urandom(24/2).encode('hex')
        key_init[i] = os.urandom(32/2).encode('hex')
        #print iv_rand
    except:
        iv_init[i] = "2bd6459f82c5b300952c4910"
    	key_init[i] = "2bd6459f82c5b300952c49104881ff48"
      
#print 'IV : ', iv_init
#print 'Key : ', key_init
initial_key_stream = [0]* itter;
for i in range (itter):
    iv_rand = iv_init[i]
    #print iv_rand
    key_rand = key_init[i]
    #print key_rand
    
    iv_rand = "0x" + iv_rand
    key_rand = "0x" + key_rand

    iv_val = int(iv_rand,16)
    key_val = int(key_rand,16)

    iv = str(hex(iv_val))
    iv = iv[2:]
    key = str(hex(key_val))
    key = key[2:]
    
    n = (1024/32)
    if(iv[-1] == 'L'):
            iv = iv[0:-1]
    if(key[-1] == 'L'):
        key = key[0:-1]
    initial_key_stream[i] = espresso_function(iv,key,n)


ijk = 0
output = [0]*itter
p_val = [0]*224;
for ijk in range (96,97):
    for ppp in range(itter):
        #print 'iteration : ', ppp
        iv_rand = iv_init[ppp]
        #print iv_rand
        key_rand = key_init[ppp]
        #print key_rand
        
        iv_rand = "0x" + iv_rand
        key_rand = "0x" + key_rand

        iv_val = int(iv_rand,16)
        key_val = int(key_rand,16)

        iv = str(hex(iv_val))
        iv = iv[2:]
        key = str(hex(key_val))
        key = key[2:]

        n = (1024/32)

        #output = [0] * 1024

        #initial_key_stream = espresso_function(iv,key,n) 

        iv_bin = str(bin(iv_val))
        key_bin = str(bin(key_val))
        
        if(len(iv_bin) != 98):
            iv_bin = iv_bin[2:]
            iv_bin = iv_bin.zfill(96)
            iv_bin = "0b" + iv_bin

        if(len(key_bin) != 130):
            key_bin = key_bin[2:]
            key_bin = key_bin.zfill(128)
            key_bin = "0b" + key_bin

        
        #counter = 0
        #for i in range(0,128):
        iv_temp = iv_bin
        key_temp = key_bin

        if (ijk <= 95):
            iv_temp = list(iv_bin)
            #print 'IV initial : ', iv_temp
            if(iv_temp[97-ijk] == "0"):
                iv_temp[97-ijk] = "1"
            else:
                iv_temp[97-ijk] = "0"
            #print 'IV final : ', iv_temp
            iv_temp = "".join(iv_temp)
        if (ijk >95):
            key_temp = list(key_bin)
            #print 'Key initial : ', key_temp
            if(key_temp[225-ijk] == "0"):
                key_temp[225-ijk] = "1"
            else:
                key_temp[225-ijk] = "0"
            #print 'Key initial : ', key_temp
            key_temp = "".join(key_temp)
            
        iv_temp_c = str(hex(int(iv_temp,2)))
        key_temp_c = str(hex(int(key_temp,2)))
        iv_temp_c = iv_temp_c[2:]
        
        key_temp_c = key_temp_c[2:]
        
        
        if(iv_temp_c[-1] == 'L'):
            iv_temp_c = iv_temp_c[0:-1]
        if(key_temp_c[-1] == 'L'):
            key_temp_c = key_temp_c[0:-1]
        
        print 'initial : ',key_init[ppp]
        print 'final :', key_temp_c
        output[ppp] = espresso_function(iv_temp_c,key_temp_c,n) ^ espresso_function(iv_temp_c,key_init[ppp],n)
        print 'XOR:', output[ppp]
        output[ppp] = str(bin(output[ppp]))
        output[ppp] = output[ppp][2:]
        output[ppp] = output[ppp].zfill(1024)
        output[ppp] = list(output[ppp])

    #print 'Output : ',output

    relation_factor = [0]*itter

    for i in range (itter):
        for j in range (1024):
            relation_factor[i] = relation_factor[i]+ int(output[i][j]);
            
    #print relation_factor

    cat = [0] * 5
    for i in range(itter):
        if(relation_factor[i] < 499):
            cat[0] = cat[0] + 1
        elif(relation_factor[i] < 508 and relation_factor[i] > 497):
            cat[1] = cat[1] + 1
        elif(relation_factor[i] < 516 and relation_factor[i] > 507):
            cat[2] = cat[2] + 1
        elif(relation_factor[i] < 526 and relation_factor[i] > 515):
            cat[3] = cat[3] + 1
        elif(relation_factor[i] < 1025 and relation_factor[i] > 525):
            cat[4] = cat[4] + 1

    observe = [0.00] * 5
    for i in range(0,5):
        observe[i] = float(cat[i])

    print "Observed Values:"
    print observe

    expect = [0.00] * 5
    expect[0] = 204.1959578
    expect[1] = 194.4138841
    expect[2] = 202.0388511
    expect[3] = 219.1553493
    expect[4] = 204.1959578

    print "Expected Values:"
    print expect

    observed_values = scipy.array([observe[0],observe[1],observe[2],observe[3],observe[4]]);
    expected_values = scipy.array([expect[0],expect[1],expect[2],expect[3],expect[4]]);
    a = scipy.stats.chisquare(observed_values, f_exp=expected_values)
    p_val[ijk] = a[1];
    print "ChiSqaure, p-value for table  " + str(ijk) + " = " + str(a[1])
    
print 'p-value = ', p_val
'''

if(ppp % 128 == 0):
    print "Iteration: " + str(ppp) 

#print output[0][0]
for i in range(0,256):
    for k in range(0,1024):
        total[i][k] = int(total[i][k]) + int(output[i][k])
#print "------------------------------------------------------------" 
#print output[0]



print "------------------------------------------------------------"
print total[0]



cat = [0] * 5
for i in range(0,256):
    for k in range(0,1024):
        if(total[i][k] < 499):
            cat[0] = cat[0] + 1
        elif(total[i][k] < 508 and total[i][k] > 497):
            cat[1] = cat[1] + 1
        elif(total[i][k] < 516 and total[i][k] > 507):
            cat[2] = cat[2] + 1
        elif(total[i][k] < 526 and total[i][k] > 515):
            cat[3] = cat[3] + 1
        elif(total[i][k] < 1025 and total[i][k] > 525):
            cat[4] = cat[4] + 1

observe = [0.00] * 5
for i in range(0,5):
    observe[i] = float(cat[i])

print "Observed Values:"
print observe

expect = [0.00] * 5
expect[0] = 50014.00#expected(0,59,128,128)
expect[1] = 48901.00#expected(59,63,128,128)
expect[2] = 58032.00#expected(63,66,128,128)
expect[3] = 55183.00#expected(66,70,128,128)
expect[4] = 50014.00#expected(70,129,128,128)

print "Expected Values:"
print expect

observed_values = scipy.array([observe[0],observe[1],observe[2],observe[3],observe[4]]);
expected_values = scipy.array([expect[0],expect[1],expect[2],expect[3],expect[4]]);
a = scipy.stats.chisquare(observed_values, f_exp=expected_values)
print "ChiSqaure, p-value = " + str(a[1])
#print total_val/itter
'''