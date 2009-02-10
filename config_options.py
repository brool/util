# build config options that mirror the current module list
# 
# usage: python config_options.py kernel-source-directory

import re
import os
import sys
import subprocess

printed = set()

for line in sys.stdin.readlines():
    if line.startswith("Module"): 
        continue

    modname = line.split()[0]
    modinfo = subprocess.Popen(["modinfo", modname], stdout=subprocess.PIPE).communicate()[0]
    modinfo = modinfo.split('\n')[0]
    modfname = modinfo.split()[1]

    # take everything after "kernel"
    modfname = modfname[modfname.find("/kernel/") + 8:]

    # get the base module name
    base_module = os.path.splitext(os.path.split(modfname)[1])[0]
    base_path   = os.path.split(modfname)[0]
    
    # read in the makefile
    try:
        for mline in file(sys.argv[1] + base_path + '/Makefile'):
            g = re.match(".+\$\((CONFIG_[^)]+)\).+%s\.o" % (base_module,), mline.strip())
            if g and g.group(1) not in printed:
                printed.add(g.group(1))
                print g.group(1)
                
    except Exception:
        pass


