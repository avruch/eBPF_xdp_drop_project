#!/usr/bin/python3

import sys
import numpy as np
sys.path.append('/usr/local/lib/python3.8/dist-packages')
sys.path.append('/usr/lib/python3/dist-packages')
from bcc import BPF
import ctypes as ct
import time
import RepeatedTimer


i=0 #itr counter.
param = 1000  #default parameter for ebpf protection,1000 mili percent drop rate.
function = sys.argv[2]
args = sys.argv[3:]


b = BPF(src_file="xdp_random_drop_func.c", cflags=["-w", "-DPARAM=\"%d\"" % param], debug=0) # BPF loading prog

fn = b.load_func("drop_func",BPF.XDP,None) #  loading XDP prog

device = sys.argv[1] #name of desired interface

b.attach_xdp(device, fn, 0) # attaching XDP prog to intf

# BPF Maps monitoring.
user_param = b["user_param"]
user_param[ct.c_int(0)] = ct.c_int(param)

def constant_func(args):
   param = int(args[0])
   user_param[ct.c_int(0)] = ct.c_int(param) # Updating drop_rate in BPF_MAP

def step_func(args):
    global i
    start_val = int(args[0])
    end_val = int(args[1])
    jump = int(args[2])
    if i >100 :
        i -= 100
    if i < jump:
        user_param[ct.c_int(0)] = ct.c_int(start_val)
    else :
        user_param[ct.c_int(0)] = ct.c_int(end_val)
    i += 1

def pyramid_func(args):
    global i
    range_start=int(args[0])
    range_end=int(args[1])
    delta=int(args[2])
    arr = np.arange(range_start, range_end, delta)
    arr1 = np.arange(range_end, range_start, -delta)
    con = np.concatenate((arr, arr1)) # Use concatenate() to join two arrays
    param = int(con[i % len(con)])
    user_param[ct.c_int(0)] = ct.c_int(param)
    i+=1

if args:
    if function == "constant_func":
        rt = RepeatedTimer.RepeatedTimer(1,constant_func,args) # Updating Function's drop_rate
    if function == "pyramid_func":
        rt = RepeatedTimer.RepeatedTimer(0.1,pyramid_func,args)
    if function == "step_func":
        rt = RepeatedTimer.RepeatedTimer(1,step_func,args)

while 1:
    time.sleep(1)
b.remove_xdp(device)

