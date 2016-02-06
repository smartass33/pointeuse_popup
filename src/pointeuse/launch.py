'''
Created on 31 janv. 2016

@author: henri
'''
'''
Created on 31 janv. 2016

@author: henri
'''
#!/usr/bin/env python
import Tkinter as tk
import tkFont
import requests
import json
import sys
import tkMessageBox
#import nxppy


class Popup():
    def center(self,win,width,height):
        """
        centers a tkinter window
        :param win: the root or Toplevel window to center
        """
        win.update_idletasks()
        #width = win.winfo_width()
        print ('width: '+str(width)) 
        frm_width = win.winfo_rootx() - win.winfo_x()
        win_width = width + 2 * frm_width
        #height = win.winfo_height()
        titlebar_height = win.winfo_rooty() - win.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = win.winfo_screenwidth() // 2 - win_width // 2
        y = win.winfo_screenheight() // 2 - win_height // 2
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        win.deiconify()

    def sendDate(self):
        print('entering senDate')
        data = {'username':'ali'}
        r = requests.get("http://192.168.1.31/employee/dummy", params = data)
        jsonStr = json.loads(r.text)
        hasError = (False if str(jsonStr['status'].encode('utf8','ignore')) == 'OK' else True)
        if (hasError):
            # il y a une erreur: creation d'un message de warning
            self.displayWarning(str(jsonStr['status'].encode('utf8','ignore')))
        else:
            self.displayPopup(jsonStr)


    def displayWarning(self,status):
        root = tk.Tk()
        root.withdraw()
        tkMessageBox.showwarning("Probleme de pointage", "Il y a eu un probleme avec le pointage:\n\n"+status)

    def displayPopup(self,jsonStr):
        firstName = jsonStr['firstName']
        lastName = jsonStr['lastName']
        loggingTime = jsonStr['loggingTime']
        inOrOutType = ('SORTIE' if (jsonStr['type'].encode('utf8','ignore')) is'S' else 'ENTREE')
        isEntry = (False if (jsonStr['type'].encode('utf8','ignore')) is'S' else True)
        root = tk.Tk()
        #root.withdraw()
        root.attributes('-alpha', 0.0)
        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=root.destroy)
        menubar.add_cascade(label="File", menu=filemenu)
        root.config(menu=menubar)
        frm = tk.Frame(root, bd=4, relief='raised')
        frm.pack(fill='x')
        #lab = tk.Label(frm, text='Hello World!', bd=4, relief='sunken')
        #lab.pack(ipadx=4, padx=4, ipady=4, pady=4, fill='both')
        #mycolor = '#%02x%02x%02x' % (64, 204, 208)  # set your favourite rgb color
        #mycolor2 = '#40E0D0'  # or use hex if you prefer 
        #backGroundColor = 'green'
        
        if (isEntry): 
            backGroundColor = 'green'
            greeting = 'Bonjour'
        else:
            backGroundColor = 'red'
            greeting = 'Au revoir'
        
        root.tk_setPalette(background=backGroundColor, foreground='white',
                   activeBackground='black', activeForeground=backGroundColor)
        customFont = tkFont.Font(family="Arial", size=24)
        text = tk.Text(root, width=20, height=2, font=customFont)
        text.insert(tk.INSERT,greeting+" "+firstName+" "+lastName+"\n\n")
        text.insert(tk.END, inOrOutType+": "+loggingTime+"\n")
        text.pack(expand=1,fill=tk.BOTH)
        
        # adding a tag to a part of text specifying the indices
        self.center(root,400,100)
    
        root.attributes('-alpha', 1.0)
        root.attributes("-topmost", True)
        root.after(5000, lambda: root.destroy())
        root.mainloop()
       # root.deiconify()

def main(args):
    global popup
    #mifare = nxppy.Mifare()
    print('starting NFC reading...')
    popup = Popup()
    jsonStr = popup.sendDate()
'''
    while True:
        try:
            uid = mifare.select()
            print('Read uid: '+uid)
            popup = Popup()
            jsonStr = popup.sendDate()
        except nxppy.SelectError:
            pass
'''
    #popup.display(jsonStr)

if __name__ == "__main__":
    main(sys.argv)
