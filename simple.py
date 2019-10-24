"""Import the compiled Python for .Net module"""
import clr
import sys

print()
print ('clr version = {}'.format(str(clr.__version__)))

"""Import the Keysight automated test app remote library DLL"""
sys.path.append(r'C:\ProgramData\Keysight\DigitalTestApps\Remote Toolkit\Version 6.3\Tools')
clr.AddReference("Keysight.DigitalTestApps.Framework.Remote")
import Keysight.DigitalTestApps.Framework.Remote as KtRemote
"""Connect to the automated test application running on the scope
This will wait for the application to be fully launched and ready
before proceeding"""
scopeIpAddress = "127.0.0.1"
remoteObj = KtRemote.RemoteAteUtilities.GetRemoteAte(scopeIpAddress)
remoteApp = KtRemote.IRemoteAte(remoteObj)

print (remoteApp.ApplicationName)