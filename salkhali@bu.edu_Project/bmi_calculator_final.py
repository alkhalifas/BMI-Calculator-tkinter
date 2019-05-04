# -*- coding: utf-8 -*-
"""
Created on Sat May  4 15:06:44 2019

@author: alkhalifas
"""
# Import packages:

# Import tkinter to build the GUI interface of this app:
from tkinter import *

# Import sqlite to store the data we will generate:
import sqlite3

# Import time to manage the time of our entries:
import time
import datetime

# import image to add BU logo:
from PIL import Image
from PIL import ImageTk, Image



# Connect to the SQL database and create a shortcut for easy access:

BMIDB = sqlite3.connect("bmidatabase.db")
c = BMIDB.cursor()



class Welcome():
    
    def __init__ (self, master):
        
        self.master = master
        self.master.geometry('260x260+100+200')
        self.master.title('Welcome')
        self.master.configure(background='white')
        
        import random
        for x in range(10):
            happycalc = random.randint(1,4)

        happy = ['Amazing','Wonderful','Great','Awesome', 'Perfect']
        happyword = happy[happycalc]
        
        finalHappyText = "The " + happyword + " Boston University BMI Calculator"
        
        #print(happyword)

        self.label1 = Label(self.master, text = finalHappyText, fg='red', background = 'white').grid(row=1, column=1)
        
        
#        img = ImageTk.PhotoImage(Image.open("bu1.png"))
#        self.label2 = Label(self.master, image = img).grid(row=0, column=1)
        
        today = datetime.datetime.now()

        #print(today)

        repr(today)
        
        self.label3 = Label(self.master, text = today, fg='black', background = 'white').grid(row=8, column=1)

        
        
        self.button1 = Button(self.master, text= "BMI Calculator", fg = 'blue', command = self.gotobmicalculator).grid(row=3, column=1)
        self.button2 = Button(self.master, text = "Records", fg = 'blue', command = self.gotorecords).grid(row=5, column=1)
#        self.button3 = Button(self.master, text = "Settings",fg='blue',command=self.gotosettings).grid(row=3,column=3)
        self.button4 = Button(self.master, text = "Exit",fg='blue',command=self.exit).grid(row=7,column=1)
        
    def exit(self):
        # Create an exit 
        self.master.destroy()
    
    def gotobmicalculator(self):
        # The actual calcualtor 
        root2 = Toplevel(self.master)
        myGUIO = bmicalculator(root2)
    
    def gotorecords(self):
        #This is where the previous records are stored
        root2=Toplevel(self.master)
        mygui=records(root2)


class bmicalculator():
    #class created for the bmi calculator GUI 
    def __init__(self,master):

        c.execute('CREATE TABLE IF NOT EXISTS BMIStorage(timestamp TEXT,bodymassindex REAL,weightclass TEXT)')

        self.heightcm=DoubleVar()
        self.weightkg=DoubleVar()

        self.master=master
        self.master.geometry('260x250+100+200')
        self.master.title('BMI Calculator')
        self.master.configure(background='white')

        self.label2=Label(self.master,text='Welcome to the BMI Calculator',fg='red').grid(row=0,column=0)
        self.label2=Label(self.master,text='Please enter your height in centimetres',fg='black').grid(row=3,column=0)
        self.label2=Label(self.master,text='Please enter your weight in kilograms',fg='black').grid(row=4,column=0)

        self.myheight=Entry(self.master,textvariable=self.heightcm).grid(row=3,column=1)
        self.myweight=Entry(self.master,textvariable=self.weightkg).grid(row=4,column=1)
        self.button4=Button(self.master,text="Calculate BMI",fg='blue',command=self.bmicalculation).grid(row=7,column=0)
        self.button5=Button(self.master,text="Exit",fg='blue',command=self.exit).grid(row=9,column=0)
        
    
    def bmicalculation(self):
        bmiheight=self.heightcm.get()
        bmiweight=self.weightkg.get()
        bmi= float((bmiweight)/((bmiheight / 100)**2))
        bmi = round(bmi, 4)
        self.bmi = bmi
        self.label1=Label(self.master,text='Your BMI is %.2f' % bmi).grid(row=5,column=0)

        if bmi <= 18.5:
            self.label2=Label(self.master,text='You are slightly underweight.',fg='blue').grid(row=6,column=0)
            totalindex = 'underweight'
            self.totalindex = totalindex
        elif bmi >18.5 and bmi <25:
            self.label3=Label(self.master,text='You are in the healthy weight group.',fg='green').grid(row=6,column=0)
            totalindex = 'healthy'
            self.totalindex = totalindex
        elif bmi >= 25 and bmi < 30:
            self.label4=Label(self.master,text='You are slightly overweight.',fg='orange').grid(row=6,column=0)
            totalindex = 'overweight'
            self.totalindex = totalindex
        elif bmi >=30:
            self.label5=Label(self.master,text='You are in the obese weight group.',fg='red').grid(row=6,column=0)
            totalindex = 'obese'
            self.totalindex = totalindex

        if bmi >0 and bmi <999999999999999999999:
            self.button6=Button(self.master,text="Store Data",fg='red',command=self.dynamic_data_entry).grid(row=8,column=0)
            
    def dynamic_data_entry(self):
        global dynamic_data_entry

        timestamp = str(datetime.datetime.now().date())
        
        bodymassindex = self.bmi
        weightclass = self.totalindex
        
        c.execute("INSERT INTO BMIStorage (timestamp, bodymassindex, weightclass) VALUES (?, ?, ?)",(timestamp, bodymassindex, weightclass))
        BMIDB.commit()
        
        self.writetodatabase()

    def writetodatabase(self):
        for i in range(1):
            time.sleep(1)


    def exit(self):

        self.master.destroy()


class records():

    def __init__(self,master):
        self.master=master
        self.master.geometry('500x500+100+200')
        self.master.configure(background='white')

        self.master.title('Records')
        self.connection = sqlite3.connect('bmidatabase.db')
        self.cur = self.connection.cursor()
        self.dateLabel = Label(self.master, text="Date", width=10)
        self.dateLabel.grid(row=0, column=0)
        self.BMILabel = Label(self.master, text="BMI", width=10)
        self.BMILabel.grid(row=0, column=1)
        self.stateLabel = Label(self.master, text="Status", width=10)
        self.stateLabel.grid(row=0, column=2)
        self.showallrecords()
        self.button4=Button(self.master,text="Return",fg='red',command=self.exit).grid(row=7,column=0)

    def showallrecords(self):
        data = self.readfromdatabase()
        for index, dat in enumerate(data):
            Label(self.master, text=dat[0]).grid(row=index+1, column=0)
            Label(self.master, text=dat[1]).grid(row=index+1, column=1)
            Label(self.master, text=dat[2]).grid(row=index+1, column=2)

    def readfromdatabase(self):
        self.cur.execute("SELECT * FROM BMIStorage")
        return self.cur.fetchall()

    def exit(self):
        self.master.destroy()


def main():
     root = Tk()
     myGUIWelcome = Welcome(root)
     root.mainloop()

if __name__ == '__main__':
     main()