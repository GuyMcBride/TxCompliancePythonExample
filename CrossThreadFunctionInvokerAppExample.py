import queue as Queue
import time
import threading
import sys

# Import the compiled Python for .Net module
import clr

# Import .NET types
clr.AddReference("System.Windows.Forms")
import System.Windows.Forms as Forms
clr.AddReference("System.Runtime.Remoting")
import System.Runtime.Remoting as Remoting

# Import Keysight automated test app remote library  types
keysightRemotePath = r"C:\ProgramData\Keysight\DigitalTestApps\Remote Toolkit\Version 6.3\Tools"
sys.path.append(keysightRemotePath)
clr.AddReference("Keysight.DigitalTestApps.Framework.Remote")
import Keysight.DigitalTestApps.Framework.Remote as KtRemote

import CrossThreadFunctionInvoker

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

# Establish callback path
#TODO: Replace with location of the .config file
configFileFullPath = keysightRemotePath + r'\Keysight.DigitalTestApps.Framework.Remote.config'
try:
    Remoting.RemotingConfiguration.Configure(configFileFullPath, False)
except Remoting.RemotingException:
    pass
eventSink = KtRemote.RemoteAteUtilities.CreateAteEventSink(remoteApp, None, scopeIpAddress)

function_invoker = CrossThreadFunctionInvoker.CrossThreadFunctionInvoker()

# Define a Run function to be executed in a worker thread
# This frees up Main to watch for function_invoker requests occuring inside callbacks
def Run(remoteApp,eventSink):
    try:
        print("Run starting.")
        remoteApp.Run()  # While this is executing, message callbacks from the automated test app will occur
        print("Run completed.")
    except Exception as e:
        print("===Exception in Run()============")
        print(e)
        print("=================================")

    function_invoker.Release()

def InvokeMessageNotHandled(args, test):
    print("Test: {}\nArgs: {}".format(test, args))
    print("Message Not Handled, returning Cancel...")
    
def DoSomethingRequiringMainThread1():
    print("Action 1 requiring execution on main thread...")

def DoSomethingRequiringMainThread2(parm):
    print("Action 2 requiring execution on main thread... {}".format(parm))

# Define the event callback handler
def SimpleMessageEventHandler(source, args):
    print("Callback handler starting")
    print("Message = {}".format(args.Message))

    if args.Message.find("Please Configure the DUT") >= 0:
        function_invoker.Add(DoSomethingRequiringMainThread1)
        function_invoker.Add(DoSomethingRequiringMainThread2, "my parameter")
        function_invoker.ExecuteAdded()
        args.Response = Forms.DialogResult.OK
    elif args.Message.find("All selected tests completed") >= 0:
        args.Response = Forms.DialogResult.OK
    else:
        function_invoker.Execute(InvokeMessageNotHandled, args, availableTests[0])
        args.Response = Forms.DialogResult.Cancel

    print("Callback handler completed")

# Use this statement to see debug output from the function invoker
function_invoker.Debug = False

try:
    print("Program starting.")
    eventSink.RedirectMessagesToClient = True
    eventSink.SimpleMessageEvent += SimpleMessageEventHandler
    remoteApp.ConnectionPromptAction = KtRemote.CustomPromptAction.AutoRespond
    #TODO: Replace with actual test ID from automated test application
    print("Available Tests:")
    availableTests = remoteApp.GetCurrentOptions("TestsInfo")
    for test in availableTests:
        print(test)
    remoteApp.SelectedTests = [availableTests[0].ID] 

    # Start the run in a worker thread to enable the program to proceed to the next statement
    threading.Thread(target=Run, args=(remoteApp,eventSink,)).start()

    function_invoker.BlockAndWait() 
    print("Program completed.")
    exportOptions = KtRemote.ExportCsvOptions()
    # Un comment when the framework supports extended result format
    exportOptions.DataFormat = 2

    if remoteApp.GetResults().CsvResults:
        resultPath = remoteApp.ExportResultsCsvCustom(exportOptions)
        print("Exported results to {}".format(resultPath))
    else:
        print("No results to report")
except Exception as e:
    print("===Exception in Main()===========")
    print (e)
    print("=================================")
finally:
    eventSink.Dispose()

