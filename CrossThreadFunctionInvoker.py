import queue
import threading
import time

###############
# Class Definition
# Use this class when you want to invoke a function from inside a dummy thread but have that function execute in the Main thread
# Ensure only one dummy thread is adding/executing functions at a time
###############
class CrossThreadFunctionInvoker:

	#=================
	# Public Interface
	#=================
	# Set this to True to get status/diagnostic messages in the output
	Debug = False

	# Call this from the Main thread
	# Main thread will be blocked until another thread calls Release()
	def BlockAndWait(this):
		this.__WaitForActivate()

	# Call this from a dummy thread to immediately execute the specified function on the Main thread
	# If a function takes arguments, pass them in after the function name, e.g. Execute(Foo,"arg1",arg2)
	# Maximum of 5 arguments supported (see function __ExecuteAll below to extend this)
	# Dummy thread will be blocked until the function is completed
	def Execute(this,*args):
		return this.__ExecuteSingle(args)

	# Call this from a dummy thread to specify a function to be executed on the Main thread
	# Function will not be executed until you call ExecuteAdded()
	# If you need to exeucte multiple functions, you may add each one before executing
	# If a function takes arguments, pass them in after the function name, e.g. Add(Foo,"arg1",arg2)
	# Maximum of 5 arguments supported (see function __ExecuteAll below to extend this)
	def Add(this,*args):
		this.__AddTupleToQueue(args)

	# Call this from a dummy thread to execute all the functions you specified using Add()
	# Dummy thread will be blocked until all functions are completed
	# Functions are executed one at at time, in the order they were added
	def ExecuteAdded(this):
		this.__ActivateAndWait()

	# Call this from another thread to pause this object and unblock the Main thread
	def Release(this):
		this.__SetStop()

	#---------------
	# Implementation
	#---------------
	__queue = queue.Queue()
	__activated = False
	__stop = False
	__ReturnValue = ""

	def __WaitForActivate(this):
		if this.Debug == True:
			print("CrossThreadFunctionInvoker: Begin waiting for function requests")
		while this.__stop == False:
			if this.__activated == True:
				this.__ExecuteAll()
				this.__activated = False
			time.sleep(0.1)
		this.__stop = False
		if this.Debug == True:
			print("CrossThreadFunctionInvoker: End waiting for function requests")

	def __ExecuteSingle(this,tuple):
		this.__AddTupleToQueue(tuple)
		this.__ActivateAndWait()
		return this.__ReturnValue

	def __AddTupleToQueue(this,tuple):
		this.__queue.put(tuple)

	def __ActivateAndWait(this):
		this.__activated = True
		while this.__activated == True:
			time.sleep(0.1)

	def __ExecuteAll(this):
		while this.__queue.qsize() > 0:
			entry = this.__queue.get()
			if this.Debug == True:
				print("CrossThreadFunctionInvoker: Begin executing")
				print("   {} in {}".format(entry[0], threading.current_thread()))
			if len(entry) == 1:
				this.__ReturnValue = entry[0]()
			elif len(entry) == 2:
				this.__ReturnValue = entry[0](entry[1])
			elif len(entry) == 3:
				this.__ReturnValue = entry[0](entry[1],entry[2])
			elif len(entry) == 4:
				this.__ReturnValue = entry[0](entry[1],entry[2],entry[3])
			elif len(entry) == 5:
				this.__ReturnValue = entry[0](entry[1],entry[2],entry[3],entry[4])
			elif len(entry) == 6:
				this.__ReturnValue = entry[0](entry[1],entry[2],entry[3],entry[4],entry[5])
			if this.Debug == True:
				print ("CrossThreadFunctionInvoker: End executing {}".format(entry[0]))

	def __SetStop(this):
		this.__stop = True

