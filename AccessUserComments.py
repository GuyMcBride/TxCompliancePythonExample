import sys

# Import the compiled Python for .Net module
import clr

import json

# Import .NET types
import System.Windows.Forms as Forms
import System.Runtime.Remoting as Remoting

# Import Keysight automated test app remote library  types
keysightRemotePath = r"C:\ProgramData\Keysight\DigitalTestApps\Remote Toolkit\Version 5.90\Tools"
sys.path.append(keysightRemotePath)
clr.AddReference("Keysight.DigitalTestApps.Framework.Remote")
import Keysight.DigitalTestApps.Framework.Remote as KtRemote

###################################
# Automated Test App Automation Program
# See TODO comments to identify statements you may need to change to make this program work with your application.
# Caution: This program attempts to print messages and exceptions originating from the automation test application;
# such text may need special handling else the print statement may generate a UnicodeEncodeError exception
# Please see your Python documentation for more information on printing Unicode text.
###################################

# Connect to the automated test application running on the scope
#TODO: Replace with actual IP Address
scopeIpAddress = "localhost"
remoteObj = KtRemote.RemoteAteUtilities.GetRemoteAte(scopeIpAddress)
remoteApp = KtRemote.IRemoteAte(remoteObj)

# Verify Connection
print(remoteApp.ApplicationName)

# Try out using User Comments to hold JSON data
params = {
	"PSU(V)" : "3.45",
	"Temp(C)" : "22.0",
	"Def1" : "User Defined 1",
	"Def2" : "User Defined 2"
		  }
jparams = json.dumps(params)
remoteApp.SetConfig('UserComments', jparams)

# Read it back and convert back to a dictionary
params_out = remoteApp.GetConfig('UserComments')
print(json.loads(params_out))


