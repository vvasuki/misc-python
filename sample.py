#! /usr/bin/python 

#easy to use python documentation.. intended for reference and reuse of source code (sample code) slices.
#for help: install python-docs package.
#see this then: file:///usr/share/doc/python-docs-2.4.1/html/tut/tut.html

#to enter interactive mode, type: python
#to exit python shell: EOF character ..  ^d
#you can set an environment variable named PYTHONSTARTUP to the name of a file containing your start-up commands.

#interpreter can act as a calculator
#arithmatic operators as in c.
#>>> width = 20
#>>> height = 5*9
#>>> width * height
#900
#9+_    #note underscore (implicit variable)
#909

#complex numbers too
#>>> 1j * 1J
#(-1+0j)
#>>> 1j * complex(0,1)
#(-1+0j)
#>>> a=1.5+0.5j
#>>> a.real
#1.5
#>>> a.imag	#that is how you print in interactive mode.. directly quote the variable.
#0.5

#"python -c command [arg] ..."
#"python -m module [arg] ...", which executes the source file for module

#"python file" and "python <file" are different.. 
#in that the former gets input from stdin.

#sys.argv, a list of strings has the script name and additional arguments from shell.
#no arguments are given, 
#sys.argv[0] is an empty string. 
#When the script name is given as '-' (meaning standard input), sys.argv[0] is set to '-'. 
#When -c command is used, sys.argv[0] is set to '-c'. 
#When -m module is used, sys.argv[0] is set to the full name of the located module.

#There are six sequence types: strings, Unicode strings, lists, tuples, buffers, and xrange objects.
#lists are like: [a, b, c]
#tuples are like: a, b, c  or  ()  or  (d,)
#Buffer objects are not directly supported by Python syntax, but can be created by calling the builtin function buffer().
#Xrange objects are similar to buffers in that there is no specific syntax to create them, 
#but they are created using the xrange() function. 
#general sequence operators:
#in, not in, +, *, s[i], s[i:j], s[i:j:k], len, min, max

lstTmp = [[]] * 3
#>>> lists
#[[], [], []]
#>>> lists[0].append(3)
#>>> lists
#[[3], [3], [3]]
lstTmp[0:2] = []	#removed elements.. size of list changable. elemensts replacable too.
#functions on lists: 
#append extend insert remove(if the arg is matched) pop(can take args) index count sort reverse

#an inbuilt function to make list of numbers:
rngTmp=range(4)
rngTmp=range(2,8)

iTmp=1
iTmp,iTmp1=1,1
if iTmp:
	#indentation is necessary for blocks in python
	strTmp="iTmp is 1"
	print strTmp, " ", iTmp
strTmp='yeah, both single and double quotes can encapsulate strings.\n\
yeah, note the continuation of the string into the next line.'
print strTmp
#any non-zero integer value is true; zero is false. 
#The condition may also be a string or list value, in fact any sequence; 
#anything with a non-zero length is true, empty sequences are false.
#comparison operators as in C.

strTmp=r'this is a raw string \
oye. it works thus.'

strTmp="""
another way of writing multiline strings.
"""
strTmp='''
yet another way of writing multiline strings.
'''

strTmp="""
look at this piece of string concatenation!
""" "oye. write them side by side.\n" + "or use the '+' sign\n"+ "muaddib "*5
print strTmp

#slice notation: strTmp[0], strTmp[2,5] 
#strTmp[:5] and strTmp[0,5] are the same.
#>>> word[-1]     # The last character.. from the right. a negative index is used.

#strTmp[0]='p' is not allowed.
#>>> 'x' + word[1:]
#'xelpA'
#is ok.

#degenerate slices are handled gracefully:
#word='HelpA'
#>>> word[1:100]
#'elpA'
#>>> word[10:]
#''
#>>> word[2:1]
#''
#>>> word[-100:]
#'HelpA'
#>>> word[-10]    # error

ustrTmp= u' a unicode \u0020 string !'
#u'a unicode   string !'
#the lower 256 characters of Unicode are the same as the 256 characters of Latin-1.
#Codecs can convert are Latin-1, ASCII, UTF-8, and UTF-16.
ustrTmp.encode('utf-8')
print ustrTmp

#string formatting options
strTmp="string formatting or interpolation operator %% is like %(familiarFunction)s" \
%{'familiarFunction':"sprintf()"}
print strTmp;
#the following options may be used in %(varName)[formatting]option:
# d i o u x X e E f F g G c % 
# r s (for python objects, using repr and str functions)
#


#the following are string related functions:
#strip() len() capitalize() lower() swapcase() l/rjust() center() l/rstrip() title()
#join(sequenceOfStrings) [r]split(delimiter) splitlines()
#[r]find () count(substr[,start,end]) [r]index() translate(table[, deletechars])
#endswith() startswith()
#isalnum() isalpha() isdigit() islower() isspace() isupper() istitle()
#zfill()

#str(), unicode(), float(), int() and long() convert among datatypes

#decision statements: if, else, elif

#looping:
#while looping: while a<b:
#for statement iterates over the items of any sequence: for x in ['cat', 'window', 'defenestrate']:
#iterate over a sequence of numbers: use for with range.
#looping constructs can have else clauses.
#break and continue are as in C.



def function(iTmp):
	#reference to the argument is passed.
	#default value may be optionally specified..
	#it is the value evaluated at the time of making of the function object.
	"this is the function's optional docstring"
	print "oye, a function was defined here."
	#global variables cannot be directly assigned a value within a function 
	#(unless named in a global statement), although they may be referenced.
	#unless the function explicitly returns something, 
	#it returns None object.
	if iTmp:
		return [iTmp]
	else:
		return

print function.__doc__

#a function is actually an object in the global namespace too.
#function can be referenced only after it is defined... "interpreter".. remember?
print function 
print function(0), function(1)

iTmp = 5
def function(arg=iTmp):
    print arg
iTmp = 6


#default is evaluated only once. rest of the calls, it is shared... 
#to be expected. for the default is filled in when the function object is created.
function() #printeth 5
def function(a, L=[]):
    L.append(a)
    return L	#L has scope only within this here block
print function(1)
print function(2)
print function(3)
print function(1,[])
print function(3)	#hehe. [1, 2, 3, 3]

#the above function behaved thusly because the default was a mutable object..
#not an immutable one.. like below.
def function(a, L=None):
    if L is None:
        L = []
    L.append(a)
    return L

#keyword arguments.
def function(arg1,arg2='ole',arg3='jo'):
	pass	#this is an empty statement.
	print arg1
function(arg2=99, arg1=0231)

#all functions accept a tuple of arguments in place of passing a literal unpacked sequence.
#the contents of the literal tuple, 
#though they may contain references to objects, 
#are themselves passed by value.

tupTmp=(0231,99)
function(*tupTmp)
#the * operator unpacks the tuple

#variable number of arguments may be passed as below.
#they may be passed in the form of a tuple of arguments, and 
#also as a dictionary (hashtable) of arguments.
def function(arg, *argTuple, ** argDictionary):
	#see how a for loop is used with a tuple
	for argentum in argTuple: pass
	#see how argDictioary is used, and notice the use of the dictionary method keys: 
	keynen = argDictionary.keys()
	#see that the sequence keynen has a method called sort
	keynen.sort()
function("sa","asdfa","sdf","asdff", 
god="allah",
prophet="mohammed")

#lambda forms from Lisp.. functions used to make function objects
def function(arg):
	return lambda argLm: arg+argLm
	#Like nested function definitions, lambda forms can reference variables from the containing scope

fnTmp=function(strTmp)
print "lambda land ", fnTmp("sdf")




