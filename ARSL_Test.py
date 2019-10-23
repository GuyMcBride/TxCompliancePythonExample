# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 21:24:40 2018

@author: walked
"""


# Import the compiled Python for .Net module
import clr
import sys

# Import Keysight automated test app remote library  types
#sys.path.append(r'C:\ProgramData\Keysight\DigitalTestApps\Remote Toolkit\Version 5.90\Tools')
clr.AddReference("Keysight.DigitalTestApps.Framework.Remote")
from  Keysight.DigitalTestApps.Framework.Remote import *
# Import Keysight automated test app remote library  types
#clr.AddReference("Keysight.DigitalTestApps.Framework.Remote")

print('connecting....')

scopeIpAddress = "localhost"
try:
    remoteObj = RemoteAteUtilities.GetRemoteAte(scopeIpAddress)
except Exception as e:
    print('Wah - {}'.format(str(e)))
#remoteApp = IRemoteAte(remoteObj)

# Verify Connection
#print(remoteApp.ApplicationName)

input("Press any Key")