# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 12:51:06 2019

@author: salkhali

Title: GUI-Based BMI Calculator
"""

# Import packages:

# Import tkinter to build the GUI interface
from tkinter import *

# Import sqlite to manage our data:
import sqlite3

# import time to manage the time of our entries
import time
import datetime

# Connect to the SQL database and create a shortcut:

conn = sqlite3.connect("bmidatabase.db")
c = conn.cursor()

# Create a class for the first page. This page will allow for navigation to subsequent pages in the calculator:

class Welcome():
    
    def __init__ (self, master):
        
        self.master = master
        self.master.geometry('200x200+100+200')
        self.master.title('Welcome')
        
        self.label1 = Label(self.master, text = "Welcome to the BMI Calculator", fg='red').grid(row=0, column=3)
        self.button1 = Button(self.master, text= "BMI Calculator", fg = 'blue', command = self.gotobmicalculator).grid(row=1, column=3)
        self.button2 = Button(self.master, text = "Records", fg = 'blue', command = self.gotorecords).grid(row=2, column=3)
        self.button3 = Button(self.master, text = "Settings",fg='red',command=self.gotosettings).grid(row=3,column=3)
        self.button4 = Button(self.master, text = "Exit",fg='red',command=self.exit).grid(row=4,column=3)
        
    def exit(self):
        # Create an exit protocol for the user
        self.master.destroy()
    
    def gotobmicalculator(self):
        # The actual calcualtor from the home page:
        root2 = Toplevel(self.master)
        myGUIO = bmicalculator(root2)
    
    def gotorecords(self):
        #This is where the previous records of BMI will be kept, hasn't been put in yet#
        root2=Toplevel(self.master)
        mygui=records(root2)
        
    def gotosettings(self):
        # settings page:
        root2 = Toplevel(self.master)
        mygui=settings(root2)

# create a class for the settings page of the app:

class settings():
    def __init__(self, master):
        
        # SQL to create a table
        c.execute('CREATE TABLE IF NOT EXISTS SETTINGSStorage(name TEXT, age REAL, gender, TEXT)')
        
        self.name = StringVar()
        self.age = DoubleVar()
        self.gender = StringVar()
        
        self.master = master
        self.master.geometry('250x200+100+200')
        self.master.title('Settings')

        
        self.label = Label(self.master,text = 'Welcome to your Settings',).grid(row=0,column=0)
        self.label2 = Label(self.master,text = 'What is Your Name?',).grid(row=1,column=0)
        self.label3 = Label(self.master,text= 'What is Your Gender?',).grid(row=3,column=0)
        self.label4 = Label(self.master,text = 'What is Your Age?',).grid(row=2,column=0)
        self.button6 = Button(self.master,text = "Store Data",fg='red',command=self.dynamic_data_entry).grid(row=4,column=0)
        self.button7 = Button(self.master,text = "Return",fg='blue',command=self.exit).grid(row=4, column = 1)
        
        self.yourname = Entry(self.master,textvariable = self.name).grid(row=1,column=1)
        self.yourage = Entry(self.master,textvariable = self.age).grid(row=2,column=1)
        self.yourgender = OptionMenu(self.master,self.gender,"Male","Female","Other",).grid(row=3,column=1)

    def dynamic_data_entry(self):
        
        # This will add new BMI data to the database
        # Bmi has to be changed to the value of bmi
        # weightclass has to be change to the weightclass
        
        # Define the inputs:
        thename = str(self.name.get())
        theage = int(self.age.get())
        thegender = str(self.gender.get())
        
        # Execute SQL query to add the data into the database
        c.execute("INSERT INTO SETTINGSStorage (name, age, gender) VALUES (?, ?, ?)",(thename, theage, thegender))
        conn.commit() 
        self.writetodatabase()
        
    def writetodatabase(self):
        for i in range(1):
            time.sleep(1)
            
    def exit(self):
        #Exit protocol for the exit button. This part is completely done.#
        self.master.destroy()

class bmicalculator():
    #class created for the bmi calculator GUI and processing the numbers
    def __init__(self,master):

        c.execute('CREATE TABLE IF NOT EXISTS BMIStorage(timestamp TEXT,bodymassindex REAL,weightclass TEXT)')

        self.heightcm=DoubleVar()
        self.weightkg=DoubleVar()

        self.master=master
        self.master.geometry('250x200+100+200')
        self.master.title('BMI Calculator')

        self.label2=Label(self.master,text='Welcome to the BMI Calculator',fg='red').grid(row=0,column=0)
        self.label2=Label(self.master,text='Please enter your height in centimetres',fg='black').grid(row=3,column=0)
        self.label2=Label(self.master,text='Please enter your weight in kilograms',fg='black').grid(row=4,column=0)

        self.myheight=Entry(self.master,textvariable=self.heightcm).grid(row=3,column=1)
        self.myweight=Entry(self.master,textvariable=self.weightkg).grid(row=4,column=1)
        self.button4=Button(self.master,text="Calculate BMI",fg='red',command=self.bmicalculation).grid(row=7,column=0)
        self.button5=Button(self.master,text="Exit",fg='red',command=self.exit).grid(row=9,column=0)
        
    
    def bmicalculation(self):
        bmiheight=self.heightcm.get()
        bmiweight=self.weightkg.get()
        bmi= float((bmiweight)/((bmiheight / 100)**2))
        self.bmi = bmi
        self.label1=Label(self.master,text='Your BMI is %.2f' % bmi).grid(row=5,column=0)

        if bmi <= 18.5:
            self.label2=Label(self.master,text='This places you in the underweight group.',fg='blue').grid(row=6,column=0)
            totalindex = 'underweight'
            self.totalindex = totalindex
        elif bmi >18.5 and bmi <25:
            self.label3=Label(self.master,text='This places you in the healthy weight group.',fg='green').grid(row=6,column=0)
            totalindex = 'healthy'
            self.totalindex = totalindex
        elif bmi >= 25 and bmi < 30:
            self.label4=Label(self.master,text='This places you in the overweight group.',fg='orange').grid(row=6,column=0)
            totalindex = 'overweight'
            self.totalindex = totalindex
        elif bmi >=30:
            self.label5=Label(self.master,text='This places you in the obese group.',fg='red').grid(row=6,column=0)
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
        conn.commit()
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