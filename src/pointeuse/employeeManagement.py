# -*- coding: utf-8 -*-
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




class Manager(): 
    server_url = 'http://pointeuse/employee'
    global phonelist
    global win
    global select
    
    def killScript(self,scriptName):
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
    
    def init(self):
        data = {'username':'ph','password':'phil'}
        r = requests.get(self.server_url+"/getAllEmployees", params = data)
        jsonStr = json.loads(r.text)
        #print(jsonStr)
        self.phonelist = []
        for employee in jsonStr:
            tmpArray = []
            #print employee['firstName']
            tmpArray.append(str(employee['lastName'].encode('utf8','ignore')) +', '+str(employee['firstName'].encode('utf8','ignore'))  )
            tmpArray.append(employee['userName'])
            self.phonelist.append(tmpArray)
    
    
    def whichSelected (self) :
        #print "At %s of %d" % (select.curselection(), len(self.phonelist))
        return int(select.curselection()[0])
    
    def addEntry (self) :
        self.phonelist.append ([nameVar.get(), phoneVar.get()])
        self.setSelect ()
    
    def updateEntry(self,phonelist) :
        phonelist[self.whichSelected()] = [nameVar.get(), phoneVar.get()]
        self.setSelect ()
        
    def createBadge(self) :
        self.phonelist[self.whichSelected()] = [nameVar.get(), phoneVar.get()]
        tkMessageBox.showinfo(title="Creation d'un badge", message=nameVar.get())
        self.writeBadge(phoneVar.get())
        self.setSelect ()
        
    def deleteBadge(self) :
        self.phonelist[self.whichSelected()] = [nameVar.get(), phoneVar.get()]
        tkMessageBox.showinfo(title="Creation d'un badge", message=nameVar.get())
        self.writeBadge('')
        self.setSelect ()    
    
    def deleteEntry(self) :
        del self.phonelist[self.whichSelected()]
        self.setSelect()
    
    def loadEntry(self) :
        name, phone = self.phonelist[self.whichSelected()]
        nameVar.set(name)
        phoneVar.set(phone)
        
    def loadEntryFromClick(self,event):                           
        print("Double Click, so loadEntryFromClick") 
        name, phone = self.phonelist[self.whichSelected()]
        nameVar.set(name)
        phoneVar.set(phone)    
    
    def on_closing(self): 
        print 'calling on_closing'    
    #    subprocess.call(['/home/pi/launch.sh&'],shell=True)
        win.destroy()
        return
    
    def center(self,win,width,height):
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
    
    def makeWindow (self) :
        global nameVar, phoneVar, select
        win = Tk()
        win.title(u"gestionnaire des badges")
        win.lift()
        win.attributes('-topmost', True)
        win.protocol("WM_DELETE_WINDOW",self.on_closing)
        self.center(win,600,500)
    
        frame1 = Frame(win)
        frame1.pack()
    
        Label(frame1, text=u"Nom du salarié").grid(row=0, column=0, sticky=W)
        nameVar = StringVar()
        name = Entry(frame1, textvariable=nameVar)
        name.grid(row=0, column=1, sticky=W)
    
        #Label(frame1, text="Phone").grid(row=1, column=0, sticky=W)
        phoneVar= StringVar()
        #phone= Entry(frame1, textvariable=phoneVar)
        #phone.grid(row=1, column=1, sticky=W)
    
        frame2 = Frame(win)       # Row of buttons
        frame2.pack()
        b6 = Button(frame2,text=u" Chercher Salarié ",command=self.searchEmployee)
        b2 = Button(frame2,text=u"Créer badge",command=self.createBadge)
        b3 = Button(frame2,text="Invalider badge",command=self.deleteBadge)
        b4 = Button(frame2,text=u" Charger salarié ",command=self.loadEntry)
        b5 = Button(frame2,text=" Lire Badge ",command=self.readBadge)

        b6.pack(side=LEFT)
        #b4.pack(side=LEFT)
        b2.pack(side=LEFT)
        b3.pack(side=LEFT)
        b5.pack(side=LEFT)
       
        frame3 = Frame(win,bd=0)       # select of names
        win.bind('<Double-1>', self.loadEntryFromClick)
        #print 'frame3:'+frame3
        frame3.pack(fill='both', expand=True)
        scroll = Scrollbar(frame3, orient=VERTICAL)
        select = Listbox(frame3, yscrollcommand=scroll.set, height=25,bd=0,width=200)
        scroll.config (command=select.yview)
        scroll.pack(side=RIGHT, fill=Y)
        select.pack(side=LEFT,  fill=BOTH, expand=1)
        return win
    

    
    def searchEmployee(self):
        print 'entering searchEmployee'
        #print ('nameVar: '+nameVar.get())
        searchString = nameVar.get()
        splitString = searchString.split(',')
        #print ('searchString: '+splitString[0])
        data = {'username':'ph','password':'phil','name':splitString[0]}
        r = requests.get(self.server_url+"/searchAllEmployees", params = data)
        jsonStr = json.loads(r.text)
        
        self.phonelist = []
        for employee in jsonStr:
            tmpArray = []
            #print employee['firstName']
            tmpArray.append(str(employee['lastName'].encode('utf8','ignore')) +', '+str(employee['firstName'].encode('utf8','ignore'))  )
            tmpArray.append(employee['userName'])
            self.phonelist.append(tmpArray)
        print self.phonelist
        self.setSelect ()
          
        #frame = win.winfo_children()[2]
        #frame.pack_forget()
        #frame.destroy()
        #for w in win.children.values():
        #for w in win.winfo_children():
            #print w
        
        
        #frame3 = Frame(win)       # select of names
        #frame3.pack()
        #scroll = Scrollbar(frame3, orient=VERTICAL)
        #select = Listbox(frame3, yscrollcommand=scroll, height=25)
        #select = Listbox(win.frame3, yscrollcommand=scroll.set, height=25)
        select.pack(side=LEFT,  fill=BOTH, expand=1)
        print self.phonelist
    
    def writeBadge(self,username):
        print 'entering writeBadge'
        '''
        mifare = nxppy.Mifare()
        uid = mifare.select()
        print ('writing'+username)
        mifare.write_block(10, username)
        '''
    
    def readBadge(self):
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
    
    def setSelect (self) :
        print 'calling setSelect'
       #print employeeList
        self.phonelist.sort()
        select.delete(0,END)
        for name,phone in self.phonelist :
            select.insert (END, name)


if __name__ == '__main__':
    
    winManager = Manager()
    winManager.init()
    win = winManager.makeWindow()
    
    killList = ["launch.py"]
    #for script in killList:
            #killScript(script)
    winManager.setSelect ()
    win.mainloop()

