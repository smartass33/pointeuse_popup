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
        #print(r.url)
        #print(r.text)
        jsonStr = json.loads(r.text)
        #firstName = jsonStr['firstName']
        #lastName = jsonStr['lastName']
        #loggingTime = jsonStr['loggingTime']
        #inOrOutType = jsonStr['type']
        #print ('firstName:' +firstName)
        #status = jsonStr['status']
        self.display(jsonStr)

    def display(self,jsonStr):
        firstName = jsonStr['firstName']
        lastName = jsonStr['lastName']
        loggingTime = jsonStr['loggingTime']
        inOrOutType = jsonStr['type']
        inOrOutType = ('SORTIE' if jsonStr['type'] is'S' else 'ENTREE')
        isEntry = (False if jsonStr['type'] is'S' else True)
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
        #backGroundColor = 'greaen'
        
        if (isEntry): 
            backGroundColor = 'green'
        else:
            backGroundColor = 'red'
        
        root.tk_setPalette(background=backGroundColor, foreground='white',
                   activeBackground='black', activeForeground=backGroundColor)
        customFont = tkFont.Font(family="Helvetica", size=24)
        text = tk.Text(root, width=20, height=2, font=customFont)
        text.insert(tk.INSERT, "Bonjour, "+firstName+" "+lastName+"!\n")
        text.insert(tk.END, inOrOutType+": "+loggingTime+"\n")
        text.pack(expand=1,fill=tk.BOTH)
        
        # adding a tag to a part of text specifying the indices
        self.center(root,500,400)
    
        root.attributes('-alpha', 1.0)
        root.after(5000, lambda: root.destroy())
        root.mainloop()
       # root.deiconify()

def main(args):
    global popup
    popup = Popup()
    jsonStr = popup.sendDate()
    popup.display(jsonStr)

if __name__ == "__main__":
    main(sys.argv)
