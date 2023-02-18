"""
Question:

Design a database application using Python GUI that allows the user to add, delete,
view student details from mysql database. Also create a login page

"""
from tkinter import *
from tkinter import filedialog
import pandas as pd
import random


def Login():
	# declare global variable
	global name 
	global pword
	global rootA

	rootA = Tk() # creating an obj. of tkinter
	rootA.title('Login') # this make the window tile 'Login' 

	instruction = Label(rootA, text = 'Please Login\n') # add label
	instruction.grid(sticky = E)

	nameL = Label(rootA, text = 'Username: ')
	pwordL = Label(rootA, text = 'Password ')
	nameL.grid(row = 1, column = 2, sticky = W)
	pwordL.grid(row = 2, column = 2, sticky = W)

	name = Entry(rootA)
	pword = Entry(rootA, show = '*')
	name.grid(row = 1, column = 3)
	pword.grid(row = 2, column = 3)

	loginB = Button(rootA, text = 'Login', command = CheckLogin, relief=GROOVE, borderwidth=4)
	# command is for to go login function
	loginB.grid(columnspan = 2,rowspan = 5, column = 3, sticky = W)

	cancelB = Button(rootA, text = 'Cancel', command = Cancel, relief=GROOVE, borderwidth=4)
	cancelB.grid(row = 3, column = 4, sticky = W)

	rootA.geometry('400x200')
	rootA.mainloop()

def CheckLogin():
	if name.get() == 'admin' and pword.get() == 'admin': # check the username and paswword
		r = Tk()
		r.title('Home')
		r.geometry('500x200')

		Teacher_data = Label(r, text = "Insert Teacher data: ")
		non_avail = Label(r, text = "Enter non available teachers name: ")
		no_day = Label(r, text = "Enter number of Days: ")
		no_exam = Label(r, text = "Enter number of exam per Day: ")
		
		Teacher_data.grid(row = 1, column = 2, sticky = W)
		non_avail.grid(row = 2, column = 2, sticky = W)
		no_day.grid(row = 3, column = 2, sticky = W) 
		no_exam.grid(row = 4, column = 2, sticky = W) 
		
		
		global aE 
		global natE 
		global dayE
		global examE

		aE = Entry(r)
		natE = Entry(r) # non avialable teachers entry
		dayE = Entry(r)
		examE = Entry(r)

		aE.grid(row = 1, column = 3)
		natE.grid(row = 2, column = 3)
		dayE.grid(row = 3, column = 3)
		examE.grid(row = 4, column = 3)
		
		BrowseB  = Button(r, text = "browse", command = show_options, relief= GROOVE, borderwidth=4)
		BrowseB.grid(row = 1, column = 4, sticky = W)
		
		assignB = Button(r, text = "Assign", command = assign_duty, relief= GROOVE, borderwidth=4)
		assignB.grid(row = 8,column = 2, sticky = W)

		ShowClassB = Button(r, text = "Show Class Data", command = show_class_data, relief= GROOVE, borderwidth=4)
		ShowClassB.grid(row = 8, column = 3, sticky = W)
		
		ShowTeacherB = Button(r, text = "Show Teacher Data", command = show_Teacher_data, relief= GROOVE, borderwidth=4)
		ShowTeacherB.grid(row = 8, column = 4, sticky = W)
		
		global txt_result
		txt_result = Label(r, text = "")
		txt_result.grid(row = 9, column = 2, sticky = W)
		
		rootA.destroy()
		r.mainloop()

	else:
		r = Tk()
		r.title("Invalid Login")
		r.geometry("300x150")
		rlbl = Label(r, text = "\n[!] Invalid Login") 
		rlbl.pack()

		r.mainloop()

def Cancel():
	global rootA
	rootA.destroy()


def show_options():
	root = Tk()
	root.fileName = filedialog.askopenfilename(filetypes = (("csv files", ".csv"),("All files","*.*")))
	a = str(root.fileName)
	global aE
	aE.insert(0,a)
	root.destroy()

def assign_duty():
	read_data()
	update_dataFrame()
	create_examDuty()
	assign_a_duty()

def read_data():
	global aE
	global df
	df = pd.read_csv(aE.get())
	print(df)


def update_dataFrame():
	global natE
	global lst
	global df
	lst = list(natE.get().split(","))
	df["Available"] = df["Teacher_name"].map(to_avialable)
	df["counter"] = df["Available"].map(assign_counter)
	print(df)

def to_avialable(x):
    global lst
    if x in lst :
        return "No"
    if df[df["Teacher_name"] == x]["Designation"].any() == "hod":
        return "No"
    return "Yes"

def create_examDuty():
	global dayE
	global examE
	global ExamDuty
	global count
	global rooms

	days = int(dayE.get())
	rooms = int(examE.get())
	count = rooms
	lst = []
	for i in range(1,days+1):
		lst.append("Day"+str(i))

	lst1 = []
	for i in range(1,rooms+1):
		lst1.append("R10"+str(i))

	lst2 = []
	for i in range(0,days):
		lst3 = []
		for j in range(0,rooms):
			lst3.append("NaN")

		lst2.append(lst3)
	    


	ExamDuty = pd.DataFrame(data =lst2, columns = lst1)
	ExamDuty["day"] = lst
	ExamDuty.set_index("day", inplace = True)
	print(ExamDuty)

def assign_a_duty():
	global ExamDuty
	n, m =  ExamDuty.shape
	for i in range(1,n+1):
		for j in range(1,m+1):
			t = assign()
			ExamDuty.set_value("Day"+str(i),"R10"+str(j), t)

	txt_result.config(text = "Exam Duty assign succesfully", fg = "green")
	
def assign_counter(x):
    if x =="No" :
        return 1
    else:
        return 0


def assign():
	global count
	global rooms
	global df
	while True:
		if count == 0:
			count = rooms
			df.set_value(df[(df["Designation"]=="teacher") & (df["counter"] == 0)].index.values,"Available", "Yes")


		if sum(df["No_Duty"]) == sum(df[df["Available"]=="No"]["No_Duty"]) or df["Available"].all == "No" :
			count -= 1
			return "x"

		m,n = df.shape
		i = random.randint(0,m-1)

		if df.iloc[i]["Designation"] != "hod":

			if df.iloc[i]["Available"] == "Yes":

				if df.iloc[i]["No_Duty"] > 0:

					df.set_value(i,"No_Duty",df.iloc[i]["No_Duty"]-1)
					df.set_value(i,"Available", "No")
					count -= 1
					return df.iloc[i]["Teacher_name"]


def show_class_data():
	global ExamDuty
	global r1 
	
	r1 = Tk()
	r1.title("Class data")
	window =  Frame(r1, bd =2, relief = RIDGE)
	window.pack()
	r1.geometry('400x200')
	lst = ExamDuty.columns
	label = Label(window, text = "Days")
	label.grid(row = 1, column = 0)
	for i in range(0,len(lst)):
		label = Label(window, text = lst[i])
		label.grid(row = 1, column = i+1)

	lst = ExamDuty.index
	for i in range(0,len(lst)):
		label = Label(window, text = lst[i])
		label.grid(row = i+2, column = 0)

	n,m = ExamDuty.shape
	
	for j in range(0,n):
		
		for i in range(0,m):
			label = Label(window, text = ExamDuty.iloc[j]["R10"+str(i+1)])
			label.grid(row = j+2, column = i+1)

	SaveB = Button(r1, text = "Save",command = Save_class,  relief= GROOVE, borderwidth=4)
	SaveB.pack()
	
def Create_Teacher_Dataframe():
	global df
	global Teacher_Data
	global ExamDuty
	global dayE
	global examE

	days = int(dayE.get())
	sessions = int(examE.get())

	lst7 = ExamDuty.index
	x,y = df.shape
	
	lst5 = []
	for i in range(0,x):
		lst5.append(df.get_value(i,"Teacher_name"))

	lst4 = []
	for i in range(0,x):
		lst6 = []
		for j in range(0,days):
			lst6.append("x")
		lst4.append(lst6)

	Teacher_Data = pd.DataFrame(data =lst4, columns = lst7)
	Teacher_Data["Teacher_name"] = lst5
	Teacher_Data.set_index("Teacher_name", inplace = True)

	for i in range(1,days+1):
		for j in range(1,sessions+1):
			if ExamDuty.loc["Day"+str(i)]["R10"+str(j)] in Teacher_Data.index.values:
				Teacher_Data.set_value(ExamDuty.loc["Day"+str(i)]["R10"+str(j)],"Day"+str(i), "R10"+str(j))
			
	

def show_Teacher_data():
	Create_Teacher_Dataframe()
	global Teacher_Data
	global r

	r = Tk()
	r.title("Teacher data")
	window =  Frame(r, bd =2, relief = RIDGE)
	window.pack()
	r.geometry('700x300')
	lst = Teacher_Data.columns
	label = Label(window, text = "Teachers")
	label.grid(row = 1, column = 0)

	for i in range(0,len(lst)):
		label = Label(window, text = lst[i])
		label.grid(row = 1, column = i+1)
	
	n,m = Teacher_Data.shape

	lst = Teacher_Data.index
	for i in range(0,len(lst)):
		label = Label(window, text = lst[i])
		label.grid(row = i+2, column = 0)

	for j in range(0,n):
		
		for i in range(0,m):
			label = Label(window, text = Teacher_Data.iloc[j]["Day"+str(i+1)])
			label.grid(row = j+2, column = i+1)

	SaveB = Button(r, text = "Save",command = Save_Teacher,  relief= GROOVE, borderwidth=4)
	SaveB.pack()

def Save_class():
	global ExamDuty
	global r1

	ExamDuty.to_csv("Class Assign.csv")
	r1.destroy()
	txt_result.config(text = "data save successfully", fg = "green")

def Save_Teacher():
	global Teacher_Data
	global r 

	Teacher_Data.to_csv("Teacher Assign.csv")
	r.destroy()
	txt_result.config(text = "data save successfully", fg = "green")

Login()
