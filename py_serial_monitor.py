
#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import tkinter
import serial
#import threading
import time

class simpleapp_tk(tkinter.Tk):
    def __init__(self,parent):
        tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()
        #self.after(100, self.checkS())
        self.checkForGroupUpdates()
        #time.sleep(2)
        self.i=0
        
    def initialize(self):
        self.grid()
        #self.grid_size()
        #self.Frame(master,width=200,height=100)

        self.entryVariable = tkinter.StringVar()
        self.entry = tkinter.Entry(self,textvariable=self.entryVariable)
        self.entry.grid(column=0,row=0,columnspan=2,sticky='EW')
        self.entry.bind("<Return>", self.OnPressEnter)
        self.entryVariable.set(u"Enter text here.")
        
        button = tkinter.Button(self,text=u"Send!",command=self.OnButtonClick)
        button.grid(column=2,columnspan=3,row=0)
        
        cb = tkinter.Checkbutton(self,text=u"Scorrimento automatico")
        cb.grid(column=0,row=2)

        self.labelVariable = tkinter.StringVar()
        self.labelVariable.set(u"waiting...")
        self.label = tkinter.Text(self,fg="blue",bg="white")
        #self.label.insert(tkinter.END,"SCHIFO!lbdlbadvsbkdbkbkzdbkbslkdbkzbdl vljzsbdcbzdhcbzhsbdchjzjh cjhzsjhdjhz jlhd ljh< zlk<dhjhsfdvhs<vycv<lz kzx")
        #self.label.insert(tkinter.END,"SCHIFO2!\n")
        self.label.grid(column=0,row=1,columnspan=3,sticky='EW')
        
        self.scroll=tkinter.Scrollbar(orient=tkinter.VERTICAL,command=self.label.yview)
        self.label["yscrollcommand"] = self.scroll.set  
        self.scroll.grid(column=4,row=1, sticky='NSWE')
        #self.label.configure(yscrollcommand=self.scroll.set)
        #self.scroll.pack(side=tkinter.RIGHT,fill=tkinter.Y)

        self.grid_columnconfigure(1,weight=1)
        #self.grid_columnconfigure(3,weight=1)

        self.grid_rowconfigure(1,weight=1)
        #self.grid_rowconfigure(2,weight=1)
        #self.resizable(True,False)
        self.update()
        self.geometry(self.geometry())
        self.entry.focus_set()
        self.entry.selection_range(0, tkinter.END)
        self.minsize(720,480)
        
        #serial
        self.S = serial.Serial('/dev/ttyACM0',9600)
        #self.after_idle(checkS())
        
        
        #thread = threading.Thread(target=read_from_port(), args=(self.S))
        #thread.start()
    def checkForGroupUpdates(self):
        self.checkS()
        self.after(10, self.checkForGroupUpdates)
    def checkS(self):
        if (self.S.inWaiting()>0):
            self.getS()
        #self.after(100, self.checkS())
    def getS(self):
        #print('aapp')
        self.label.insert(tkinter.END,self.xxx())
        #print(self.scroll.get()[1])
        if self.scroll.get()[1]==1.0:
            #print(self.scroll.get()[0])
            self.label.see(tkinter.END)
            
        if self.i == 0:
            self.label.delete("1.0", tkinter.END)
            #self.i=0
        self.i+=1
    def xxx(self):
        #print('xxx')
        data_str=''
        if (self.S.inWaiting()>0):
            data_str = self.S.read(self.S.inWaiting()).decode('ascii') #read the bytes and convert from binary array to ASCII
        #print(data_str, end='')
        return data_str
        
    '''def handle_data(data):
        print(data)
        self.label.insert(tkinter.END,data)
    
    def read_from_port(ser):
        while True:
           print("test")
           reading = ser.read().decode()
           self.handle_data(reading) '''   

    def OnButtonClick(self):
        #self.label.insert(tkinter.END,self.xxx())
        #self.labelVariable.set(self.entryVariable.get()+" (You clicked the button)" )
        self.S.write(bytes((self.entryVariable.get()).encode('ascii')))
        self.entry.focus_set()
        self.entry.selection_range(0, tkinter.END)

    def OnPressEnter(self,event):
        #self.label.insert(tkinter.END,self.entryVariable.get()+" (You pressed ENTER)")
        #self.labelVariable.set(self.entryVariable.get()+" (You pressed ENTER)")
        self.S.write(bytes((self.entryVariable.get().strip()).encode('ascii')))        
        self.entry.focus_set()
        self.entry.selection_range(0, tkinter.END)


if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('My serial monitor')
    #app.after(100, app.checkS())
    #app.after_idle(app.checkS())
    app.mainloop()
    #S=serial.Serial('/dev/ttyACM0',9600)
    #for i in range(2):
    #    print(S.read())
    
