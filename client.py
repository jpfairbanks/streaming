""" This client for msgpackrpc takes a file of numbers and binary
reduces them pairwise. By piping this into itself until you get only one number,
it will reduce the entire data set to the """
import msgpackrpc
import sys
import time

client = msgpackrpc.Client(msgpackrpc.Address("localhost", 18800))
fp = sys.stdin
tstart = time.time()
i = 0
num1 = 0 
num2 = 0 
function_name = 'sum'
for line in fp:
    num1 = float(line)
    result = client.call(function_name, num1, num2)  # = > 3
    if i % 2 == 0:
        print(result)
    i = i + 1
    num2 = num1
#end while loop
tend = time.time()
#print("run time: %f" % (tend-tstart))
