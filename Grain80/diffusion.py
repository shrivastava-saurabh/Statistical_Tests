import os
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

def str_to_blocks(K,length):
    k_b = [0]*length
    K = K.zfill(length*2)

    if(K[-1:] == 'L'):
        K = K[:-1]

    for cs in range(0,length):
        string = "0x" + K[(cs*2):(cs*2)+2]
        k_b[cs] = int(string,16)
    return k_b

def convert(iv_s,key_s):
    command = "./grain "
    #print len(key_s)
    for cs in range(0,10):
        command = command + str(key_s[cs]) + " "
    for cs in range(0,8):
        command = command + str(iv_s[cs]) + " "
    return command

total = [0] * 256
a = '0'
for i in range(0,256):
    total[i] = list(a.zfill(1024))

itter = 1024
total_val = 0
for ppp in range(0,itter):
    try:
        iv_rand = os.urandom(8).encode('hex')
        key_rand = os.urandom(10).encode('hex')
        #print iv_rand
    except:
        iv_rand = "2bd6459f82c5b300"
    	key_rand = "2bd6459f82c5b300952c"

    iv_rand = "0x" + iv_rand
    key_rand = "0x" + key_rand

    iv_val = int(iv_rand,16)
    key_val = int(key_rand,16)

    iv = str(hex(iv_val))
    iv = iv[2:]
    key = str(hex(key_val))
    key = key[2:]
    iv_s = str_to_blocks(iv,8)
    key_s = str_to_blocks(key,10)
    com = convert(iv_s,key_s)
    out = str(os.popen(com).read())
    output = "0x" + out
    
    output = int(output,16)

	#output = [0] * 1024

    initial_key_stream = output

    iv_bin = str(bin(iv_val))
    key_bin = str(bin(key_val))
    
    if(len(iv_bin) != 66):
        iv_bin = iv_bin[2:]
        iv_bin = iv_bin.zfill(64)
        iv_bin = "0b" + iv_bin

    if(len(key_bin) != 82):
        key_bin = key_bin[2:]
        key_bin = key_bin.zfill(80)
        key_bin = "0b" + key_bin

    changes = 80+64
    output = [0]*changes
    counter = 0

    for i in range(0,64):
        iv_temp = iv_bin
        key_temp = key_bin

        iv_temp = list(iv_bin)
        if(iv_temp[65-i] == "0"):
            iv_temp[65-i] = "1"
        else:
            iv_temp[65-i] = "0"
        iv_temp = "".join(iv_temp)
        
        iv_temp_c = str(hex(int(iv_temp,2)))
        key_temp_c = str(hex(int(key_temp,2)))
        iv_temp_c = iv_temp_c[2:]
        key_temp_c = key_temp_c[2:]
        iv_s = str_to_blocks(iv_temp_c,8)
        key_s = str_to_blocks(key_temp_c,10)
        com = convert(iv_s,key_s)
        out = str(os.popen(com).read())
        output[counter] = "0x" + out 
        output[counter] = int(output[counter],16) ^ initial_key_stream
        counter = counter + 1

    for i in range(0,80):
	# IV and Key reset
        iv_temp = iv_bin
        key_temp = key_bin

        key_temp = list(key_bin)
        if(key_temp[81-i] == "0"):
            key_temp[81-i] = "1"
        else:
            key_temp[81-i] = "0"
        key_temp = "".join(iv_temp)

        iv_temp_c = str(hex(int(iv_temp,2)))
        key_temp_c = str(hex(int(key_temp,2)))
        iv_temp_c = iv_temp_c[2:]
        key_temp_c = key_temp_c[2:]
        iv_s = str_to_blocks(iv_temp_c,8)
        key_s = str_to_blocks(key_temp_c,10)
        com = convert(iv_s,key_s)
        out = str(os.popen(com).read())
        output[counter] = "0x" + out 
        output[counter] = int(output[counter],16) ^ initial_key_stream
        counter = counter + 1
    
    
    for i in range(0,changes):
        output[i] = str(bin(output[i]))
        output[i] = output[i][2:]
        output[i] = output[i].zfill(1024)
        output[i] = list(output[i])
    if(ppp % 128 == 0):
        print "Iteration: " + str(ppp) 
    #print output[0][0]
    for i in range(0,changes):
        for k in range(0,1024):
            total[i][k] = int(total[i][k]) + int(output[i][k])
#print "------------------------------------------------------------" 
#print output[0]



print "------------------------------------------------------------"
print total[0]



cat = [0] * 5
for i in range(0,changes):
    for k in range(0,1024):
        if(total[i][k] <= 300 or total[i][k] >= 600):
            print "Index: " + str(i) + " " + str(j)
        if(total[i][k] < 499):
            cat[0] = cat[0] + 1
        elif(total[i][k] < 508 and total[i][k] > 498):
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
expect[0] = 29404.21792
expect[1] = 27995.59931
expect[2] = 29093.59455
expect[3] = 31558.3703
expect[4] = 29404.21792

print "Expected Values:"
print expect

observed_values = scipy.array([observe[0],observe[1],observe[2],observe[3],observe[4]]);
expected_values = scipy.array([expect[0],expect[1],expect[2],expect[3],expect[4]]);
a = scipy.stats.chisquare(observed_values, f_exp=expected_values)
print "ChiSqaure, p-value = " + str(a[1])
#print total_val/itter

chi_sq = 0
for i in range(5):
	chi_sq = chi_sq+ (((observed_values[i] - expected_values[i])**2)/expected_values[i])

print 'chi square = ', chi_sq