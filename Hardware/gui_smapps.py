from tkinter import*
from firebase import firebase
from time import sleep

firebase = firebase.FirebaseApplication('https://login-f0a7b.firebaseio.com/', None)


root = Tk() #root is the blank window
logo=PhotoImage(file="logo.png")
root.title("smApps")
root.geometry("300x200")

w1=Label(root,image=logo).grid(row=0,column=1)

def readData():
        
    In = firebase.get('https://login-f0a7b.firebaseio.com/Barrier','servo_in')
    Out = firebase.get('https://login-f0a7b.firebaseio.com/Barrier','servo_out')
    Park = firebase.get('https://login-f0a7b.firebaseio.com/Barrier','Parking_available')
    
    label_1 = Label(root,text="             Gate In:")
    label_2 = Label(root,text="             Gate Out:")
    label_3 = Label(root,text="             Parking Available:")

    if In == "True":
        gate_1 = Label(root,text="Opened")
    else:
        gate_1 = Label(root,text="Closed ")
        
    if Out == "True":
        gate_2 = Label(root,text="Opened")
    else:
        gate_2 = Label(root,text="Closed ")

    park_3 = Label(root,text=Park)
  
    
    label_1.grid(row=1,sticky=E)
    label_2.grid(row=2,sticky=E)
    label_3.grid(row=3,sticky=E)
    gate_1.grid(row=1,column=1)
    gate_2.grid(row=2,column=1)
    park_3.grid(row=3,column=1)
    
    root.after(1000,readData)

readData()

root.mainloop()
