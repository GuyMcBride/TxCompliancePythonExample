import threading

import CrossThreadFunctionInvoker

#########
# Program
# Enables validation of the CrossThreadFunctionInvoker class
#########
def Foo():
	print("...Foo...")

def Foo1(arg):
	print("...Foo1({})...".format(arg))

def Foo2(arg1,arg2):
	print("...Foo2({} {})...".format(arg1, arg2))

def Foo3(arg1,arg2,arg3):
	print("...Foo3({} {} {})...".format(arg1, arg2, arg3))

def Foo4(arg1,arg2,arg3,arg4):
	print("...Foo4({} {} {} {})...".format(arg1, arg2, arg3, arg4))

def Foo5(arg1,arg2,arg3,arg4,arg5):
	print("...Foo5({} {} {} {} {})...".format(arg1, arg2, arg3, arg4, arg5))

def FooReturn():
	print("...FooReturn...")
	return None

def Foo1Return(arg):
	print("...Foo1Return({})...".format(arg))
	return arg

def Foo2Return(arg1,arg2):
	print("...Foo1Return({} {})...".format(arg1, arg2))
	return arg1, arg2

def Foo3Return(arg1,arg2, arg3):
	print("...Foo3Return({} {} {})...".format(arg1, arg2, arg3))
	return arg1, arg2, arg3

def Foo4Return(arg1,arg2, arg3, arg4):
	print("...Foo4Return({} {} {} {})...".format(arg1, arg2, arg3, arg4))
	return arg1, arg2, arg3, arg4

def Foo5Return(arg1,arg2, arg3, arg4, arg5):
	print("...Foo5Return({} {} {} {} {})...".format(arg1, arg2, arg3, arg4, arg5))
	return arg1, arg2, arg3, arg4, arg5

function_invoker = CrossThreadFunctionInvoker.CrossThreadFunctionInvoker()

def RunA():
	global function_invoker
	try:
		print("Run A starting")
		print("Execute methods singly")
		print("These methods return nothing")
		function_invoker.Execute(Foo)
		function_invoker.Execute(Foo1,"1")
		function_invoker.Execute(Foo2,"1",2)
		function_invoker.Execute(Foo3,"1",2,"3")
		function_invoker.Execute(Foo4,"1",2,"3",4)
		function_invoker.Execute(Foo5,"1",2,"3",4,"5")

		print("These methods return a tuple of their arguments")
		print(function_invoker.Execute(FooReturn))
		print(function_invoker.Execute(Foo1Return,"1"))
		print(function_invoker.Execute(Foo2Return,"1",2))
		print(function_invoker.Execute(Foo3Return,"1",2,"3"))
		print(function_invoker.Execute(Foo4Return,"1",2,"3",4))
		print(function_invoker.Execute(Foo5Return,"1",2,"3",4,"5"))
		print("Run A complete")
	except Exception as e:
		print(e)
	function_invoker.Release()

def RunB():
	global function_invoker
	try:
		print("Run B starting")
		print("Execute a batch of methods that return nothing")
		function_invoker.Add(Foo1,"1")
		function_invoker.Add(Foo2,"1",2)
		function_invoker.Add(Foo3,"1",2,"3")
		function_invoker.Add(Foo4,"1",2,"3",4)
		function_invoker.Add(Foo5,"1",2,"3",4,"5")
		function_invoker.ExecuteAdded()
		print("Run B complete")
	except Exception as e:
		print(e)
	function_invoker.Release()

#function_invoker.Debug = True

print("Program starting")

threading.Thread(target=RunA).start()
function_invoker.BlockAndWait()

threading.Thread(target=RunB).start()
function_invoker.BlockAndWait()

print("Program complete")
