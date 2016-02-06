#     t k P h o n e . p y
#
from Tkinter import *
import requests
import json
import tkMessageBox
import subprocess
import os
import signal
import time
#import nxppy

server_url = 'http://pointeuse/employee'


def killScript(scriptName):
        # get running processes with the ps aux command
        res = subprocess.check_output(["ps","aux"], stderr=subprocess.STDOUT)

        for line in res.split("\n"):
                # if one of the lines lists our process
                if line.find(scriptName) != -1:
                        info = []

                        # split the information into info[]
                        for part in line.split(" "):
                                if part.strip() != "":
                                        info.append(part)

                        # the PID is in the second slot
                        PID = info[1]
                        print type(PID)

                        #kill the PID
                        #subprocess.check_output(["sudo kill",PID],stderr=subprocess.STDOUT,shell=True)
                        #os.system("sudo kill %s" % (PID,signal.SIGKILL))
                        os.kill(int(PID),signal.SIGKILL)

data = {'username':'ph','password':'phil'}
r = requests.get(server_url+"/getAllEmployees", params = data)
jsonStr = json.loads(r.text)
#print(jsonStr)
phonelist = []
for employee in jsonStr:
    tmpArray = []
    #print employee['firstName']
    tmpArray.append(str(employee['lastName'].encode('utf8','ignore')) +', '+str(employee['firstName'].encode('utf8','ignore'))  )
    tmpArray.append(employee['userName'])
    phonelist.append(tmpArray)


def whichSelected () :
    print "At %s of %d" % (select.curselection(), len(phonelist))
    return int(select.curselection()[0])

def addEntry () :
    phonelist.append ([nameVar.get(), phoneVar.get()])
    setSelect ()

def updateEntry(phonelist) :
    phonelist[whichSelected()] = [nameVar.get(), phoneVar.get()]
    setSelect ()
    
def createBadge() :
    phonelist[whichSelected()] = [nameVar.get(), phoneVar.get()]
    tkMessageBox.showinfo(title="Creation d'un badge", message=nameVar.get())
    writeBadge(phoneVar.get())
    setSelect ()

def deleteEntry() :
    del phonelist[whichSelected()]
    setSelect()

def loadEntry() :
    name, phone = phonelist[whichSelected()]
    nameVar.set(name)
    phoneVar.set(phone)

def on_closing(): 
    print 'calling on_closing'    
#    subprocess.call(['/home/pi/launch.sh&'],shell=True)
    win.destroy()
    return

def center(win,width,height):
        """
        centers a tkinter window
        :param win: the root or Toplevel window to center
        """
        win.update_idletasks() 
        frm_width = win.winfo_rootx() - win.winfo_x()
        win_width = width + 2 * frm_width
        titlebar_height = win.winfo_rooty() - win.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = win.winfo_screenwidth() // 2 - win_width // 2
        y = win.winfo_screenheight() // 2 - win_height // 2

        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        win.deiconify()

def makeWindow () :
    global nameVar, phoneVar, select
    win = Tk()
    win.lift()
    win.attributes('-topmost', True)
    win.protocol("WM_DELETE_WINDOW",on_closing)
    center(win,600,500)

    frame1 = Frame(win)
    frame1.pack()

    Label(frame1, text="Name").grid(row=0, column=0, sticky=W)
    nameVar = StringVar()
    name = Entry(frame1, textvariable=nameVar)
    name.grid(row=0, column=1, sticky=W)

    #Label(frame1, text="Phone").grid(row=1, column=0, sticky=W)
    phoneVar= StringVar()
    #phone= Entry(frame1, textvariable=phoneVar)
    #phone.grid(row=1, column=1, sticky=W)

    frame2 = Frame(win)       # Row of buttons
    frame2.pack()
    #b1 = Button(frame2,text=" Add  ",command=addEntry)
    b2 = Button(frame2,text="Creer badge",command=createBadge)
    b3 = Button(frame2,text="Invalider",command=deleteEntry)
    b4 = Button(frame2,text=" Load ",command=loadEntry)
    b5 = Button(frame2,text=" Lire Badge ",command=readBadge)
    b6 = Button(frame2,text=" Chercher Salarie ",command=searchEmployee(win))

    #b1.pack(side=LEFT); 
    b2.pack(side=LEFT)
    b3.pack(side=LEFT); 
    b4.pack(side=LEFT)
    b5.pack(side=LEFT)
    b6.pack(side=LEFT)

    frame3 = Frame(win)       # select of names
    frame3.pack()
    scroll = Scrollbar(frame3, orient=VERTICAL)
    select = Listbox(frame3, yscrollcommand=scroll.set, height=25)
    scroll.config (command=select.yview)
    scroll.pack(side=RIGHT, fill=Y)
    select.pack(side=LEFT,  fill=BOTH, expand=1)
    return win

def searchEmployee(win):
    data = {'username':'ph','password':'phil','name':'anc'}
    r = requests.get(server_url+"/searchAllEmployees", params = data)
    jsonStr = json.loads(r.text)
    
    phonelist = []
    for employee in jsonStr:
        tmpArray = []
        #print employee['firstName']
        tmpArray.append(str(employee['lastName'].encode('utf8','ignore')) +', '+str(employee['firstName'].encode('utf8','ignore'))  )
        tmpArray.append(employee['userName'])
        phonelist.append(tmpArray)
    setSelect ()
    #select = Listbox(win.frame3, yscrollcommand=scroll.set, height=25)
    select.pack(side=LEFT,  fill=BOTH, expand=1)
    print phonelist

def writeBadge(username):
    print 'entering writeBadge'
    '''
    mifare = nxppy.Mifare()
    uid = mifare.select()
    print ('writing'+username)
    mifare.write_block(10, username)
    '''

def readBadge():
        print('starting cardreader')
        '''
        mifare = nxppy.Mifare()
        q = True
        while q:
            try:
                uid = mifare.select()
            #    print "Read uid", uid

                username = mifare.read_block(10)
                if username is not None:
                    print("username: "+username)
            
                    data = {'username':str(username)}
                    r = requests.get("http://192.168.1.21:8080/pointeuse/employee/getJSONEmployee", params = data)
                    print r.url

                    jsonStr = json.loads(r.text)
                    if jsonStr is not None:
                        hasError = (False if str(jsonStr['status'].encode('utf8','ignore')) == 'OK' else True)
                    if (hasError):
                # il y a une erreur: creation d'un message de warning
                        print 'error'
                    else:
                        print jsonStr
                        
                        nameVar.set(str(jsonStr['lastName'].encode('utf8','ignore')) +', '+str(jsonStr['firstName'].encode('utf8','ignore')))
                        phoneVar.set(str(jsonStr['userName'].encode('utf8','ignore')))
        
                    #self.sendDate(username)
                    q = False
                    return username
                
            except nxppy.SelectError:
                #print 'selectError' 
                pass
                #self.start()
            except nxppy.ReadError:
                print 'readError'
                self.readCard()
            time.sleep(1)
      '''

def setSelect ( ) :
    print 'calling setSelect'
   #print employeeList
    phonelist.sort()
    select.delete(0,END)
    for name,phone in phonelist :
        select.insert (END, name)



    
win = makeWindow()

killList = ["launch.py"]
#for script in killList:
        #killScript(script)
setSelect ()
win.mainloop()

