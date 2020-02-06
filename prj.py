from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
import cx_Oracle
from bs4 import BeautifulSoup
import requests
import socket

root = Tk()
root.title("S. M. S.")

#screen_width=root.winfo_screenwidth()
#screen_height=root.winfo_screenheight()
root.focus()
root.geometry("800x450+350+80")


res=requests.get("https://www.brainyquote.com/quote_of_the_day")
soup=BeautifulSoup(res.text,"lxml")
quote=soup.find("img",{"class":"p-qotd"})

try:
	city="Mumbai"
	socket.create_connection(("www.google.co.in",80))
	a1="http://api.openweathermap.org/data/2.5/weather?units=metric"
	a2="&q="+city
	a3="&appid=813b137c642ba7e2bd0a0113404c9008"
	api_address=a1+a2+a3
	res1=requests.get(api_address)
	wdata=requests.get(api_address).json()
	print(wdata)
	temp=wdata["main"]["temp"]
	city=wdata["name"]
	country=wdata["sys"]["country"]
	msg="You are in "+city+","+country+" and temperature of "+city+","+country+" is: "+str(temp)+" oC"
except OSError:
	print("Check network")

s=Canvas(root,width=800,height=700)
bg_image = PhotoImage(file="board4.png")
image = s.create_image(750,60, anchor = NE,image=bg_image)
s.create_text(400,150,text="Welcome to Student Management System",fill="White",font="calibri 16")
s.create_text(400,200,text="Quote of the day is\n"+quote["alt"],fill="White",font="calibri 14")
s.create_text(430,300,text=msg,fill="White",font="calibri 14")
s.pack()
root.after(6000,lambda:s.destroy())
root.deiconify()


vist = Toplevel(root)
vist.title("View Student")
vist.geometry("600x500+350+150")
vist.withdraw()

stData = scrolledtext.ScrolledText(vist,width=50,height=10)
stData.pack()

def f4():
	stData.config(state=NORMAL)
	stData.delete('1.0',END)
	#stData.delete(first=0,last=100)
	vist.withdraw()
	root.deiconify()
btnBack = Button(vist, text="Back To Main Menu",font = ("Arial",10,"bold"), width=20, bd=5, command=f4)
btnBack.pack()

def f1():
	root.withdraw()
	adst.deiconify()
	entAddRno.focus()
btnAdd = Button(root, text="Add Student Info.", font = ("Arial",15,"bold"),width=35,bd=5 ,command=f1)

def f3():
	root.withdraw()
	vist.deiconify()
	stData.delete(1.0,END)
	con = None
	cursor = None
	try:
		con = cx_Oracle.connect('system/iupui')
		cursor = con.cursor()
		sql = "select rno,name,physics,maths,chemistry from student"
		cursor.execute(sql)
		data = cursor.fetchall()
		msg = ""
		stData.config(state=NORMAL)
		for d in data:
			add = int(d[2]) + int(d[3]) + int(d[4])
			add_by = add*100
			per = add_by/300.0
			msg = msg + " Rno:"+str(d[0])+"  Name:"+str(d[1])+" P:"+str(d[2])+"  M:"+str(d[3])+"  C:"+str(d[4])+" Per:"+str(round(per,2))+"%"+"\n"
		stData.insert(INSERT,msg)
		stData.config(state=DISABLED)
		
	except cx_Oracle.DatabaseError as e:
		messagebox.showerror("Select Issue ", e)
	
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()
			
btnView = Button(root, text="View Student Info.",font = ("Arial",15,"bold"), width=35, bd=5, command=f3)
btnAdd.pack(pady=20)
btnView.pack(pady=20)

adst = Toplevel(root)
adst.title("Add Student")
adst.geometry("500x625+300+10")
adst.withdraw()

lblAddRno = Label(adst, text="Enter Roll No.", font = ("Arial",10,"bold"))
entAddRno = Entry(adst, font = ("Arial",10,"bold"),bd=5)
lblAddName = Label(adst, text="Enter Name:", font = ("Arial",10,"bold"))
entAddName = Entry(adst, font = ("Arial",10,"bold"),bd=5)

lblMarks = Label(adst, text="Enter Marks", font = ("Arial",15,"bold"))
lblPhysics = Label(adst,text="Physics:-",font = ("Arial",10,"bold"))
entPhysics = Entry(adst,font = ("Arial",10,"bold"),bd=5)

lblMaths = Label(adst,text="Maths:-",font=("Arial",10,"bold"))
entMaths = Entry(adst,font = ("Arial",10,"bold"),bd=5)

lblChemistry = Label(adst,text="Chemistry",font=("Arial",10,"bold"))
entChemistry = Entry(adst,font = ("Arial",10,"bold"),bd=5)

def f5():
	con = None
	cursor = None
	try:
		con = cx_Oracle.connect('system/iupui')
		rno = int(entAddRno.get())
		ph = int(entPhysics.get())
		ma = int(entMaths.get())
		ch = int(entChemistry.get())
		if rno < 0 or ph < 0 or ma <0 or ch < 0:
			messagebox.showerror("Failure","Only Positive Values!!")
			entAddRno.delete(first=0,last=100)
			entAddName.delete(first=0,last=100)
			entPhysics.delete(first=0,last=100)
			entMaths.delete(first=0,last=100)
			entChemistry.delete(first=0,last=100)
			entAddRno.focus()
			return;
			
		name = entAddName.get()
		if len(name) == 0:
			messagebox.showerror("Failure"," Empty Fields!! Fill All Fields!! ")
			entAddRno.delete(first=0,last=100)
			entAddName.delete(first=0,last=100)
			entPhysics.delete(first=0,last=100)
			entMaths.delete(first=0,last=100)
			entChemistry.delete(first=0,last=100)
			entAddRno.focus()
			return;
			
		if not(name.isalpha()):
			messagebox.showerror("Issue in Name"," Only Alphabets Allowed For Name!!")
			entAddRno.delete(first=0,last=100)
			entAddName.delete(first=0,last=100)
			entPhysics.delete(first=0,last=100)
			entMaths.delete(first=0,last=100)
			entChemistry.delete(first=0,last=100)
			entAddRno.focus()
			return;
			
		if ph>100 or ma>100 or ch>100:
			messagebox.showerror("Marks > 100","Marks Cannot be Greater than 100!!")
			entPhysics.delete(first=0,last=100)
			entMaths.delete(first=0,last=100)
			entChemistry.delete(first=0,last=100)
			entPhysics.focus()
			return;
			
		sql = "insert into student values('%d','%s','%d','%d','%d')"
		args = (rno,name,ph,ma,ch)
		cursor = con.cursor()
		cursor.execute(sql%args)
		con.commit()
		msg = str(cursor.rowcount)+" records inserted "
		entAddRno.delete(first=0,last=100)
		entAddName.delete(first=0,last=100)
		entPhysics.delete(first=0,last=100)
		entMaths.delete(first=0,last=100)
		entChemistry.delete(first=0,last=100)
		messagebox.showinfo("Success",msg)
		entAddRno.focus()
		
	except ValueError as me:
		messagebox.showerror("Failure", "Empty Fields!! Fill All Fields!!")
		entAddRno.delete(first=0,last=100)
		entAddName.delete(first=0,last=100)
		entPhysics.delete(first=0,last=100)
		entMaths.delete(first=0,last=100)
		entChemistry.delete(first=0,last=100)
		entAddRno.focus()
	except cx_Oracle.DatabaseError as e:
		con.rollback()
		messagebox.showerror("Failure", e)
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()
btnAddSave = Button(adst, text="Save Student Info.",font = ("Arial",10,"bold"),width=20,bd=5, command=f5)

def f2():
	entAddRno.delete(first=0,last=100)
	entAddName.delete(first=0,last=100)
	adst.withdraw()
	root.deiconify()
btnAddBack = Button(adst, text="Back to Main Menu",font = ("Arial",10,"bold"),width=20,bd=5,command=f2)

lblAddRno.pack(pady=10)
entAddRno.pack(pady=10)
lblAddName.pack(pady=10)
entAddName.pack(pady=10)
lblMarks.pack(pady=10)
lblPhysics.pack(pady=10)
entPhysics.pack(pady=10)
lblMaths.pack(pady=10)
entMaths.pack(pady=10)
lblChemistry.pack(pady=10)
entChemistry.pack(pady=10)
btnAddSave.pack(pady=10)
btnAddBack.pack(pady=10)

upst = Toplevel(root)
upst.title("Update Student")
upst.geometry("500x600+350+190")
upst.withdraw()

lblUpdateRno = Label(upst,text='Enter Roll No.',font = ("Arial",10,"bold"))
entUpdateRno = Entry(upst,font = ("Arial",10,"bold"),bd=5)
lblUpdateName = Label(upst,text='Enter Name:',font = ("Arial",10,"bold"))
entUpdateName = Entry(upst,font = ("Arial",10,"bold"),bd=5)
entUpdateMarks = Entry(upst,font = ("Arial",10,"bold"),bd=5)

lblUpdateMarks = Label(upst,text="Update Student Marks",font=("Arial",10,"bold"))
subject = IntVar()
#subject.set(1)
radio_physics = Radiobutton(upst,text="Physics",variable=subject,value=1,font=("Airal",10,"bold"))
radio_maths = Radiobutton(upst,text="Mathematics",variable=subject,value=2,font=("Airal",10,"bold"))
radio_chemistry = Radiobutton(upst,text="Chemistry",variable=subject,value=3,font=("Airal",10,"bold"))

def up_marks():
	r = subject.get()
	if(r==1):
		con = None
		cursor = None
		try:
			con = cx_Oracle.connect('system/iupui')
			rno = int(entUpdateRno.get())
			mar = int(entUpdateMarks.get())
			if rno < 0 or mar < 0:
				messagebox.showerror("Failure","Only Positive Values Allowed!!")
				entUpdateRno.delete(first=0,last=100)
				entUpdateMarks.delete(first=0,last=100)
				entUpdateRno.focus()
				return;
				
			if mar > 100:
				messagebox.showerror("Failure","Marks > 100")
				entUpdateMarks.delete(first=0,last=100)
				entUpdateMarks.focus()
				return;
				
			sql = "update student set physics=%d where rno=%d"
			args = (mar,rno)
			cursor = con.cursor()
			cursor.execute(sql%args)
			con.commit()
			msg = str(cursor.rowcount)+" records Updated "
			messagebox.showinfo("Success",msg)
			entUpdateRno.delete(first=0,last=100)
			entUpdateMarks.delete(first=0,last=100)
			entUpdateRno.focus()
			
		except ValueError as me:
			messagebox.showerror("Failure", "Rno or Marks cannot be Empty!!")
			entUpdateRno.delete(first=0,last=100)
			entUpdateMarks.delete(first=0,last=100)
			entUpdateRno.focus()
			
		except cx_Oracle.DatabaseError as e:
			con.rollback()
			messagebox.showerror("Failure :- Update Issue", e)
		finally:
			if cursor is not None:
				cursor.close()
			if con is not None:
				con.close()
	elif(r==2):
		con = None
		cursor = None
		try:
			con = cx_Oracle.connect('system/iupui')
			rno = int(entUpdateRno.get())
			mar = int(entUpdateMarks.get())
			if rno < 0 or mar < 0:
				messagebox.showerror("Failure","Only Positive Values Allowed!!")
				entUpdateRno.delete(first=0,last=100)
				entUpdateMarks.delete(first=0,last=100)
				entUpdateRno.focus()
				return;
				
			if mar > 100:
				messagebox.showerror("Failure","Marks > 100")
				entUpdateMarks.delete(first=0,last=100)
				entUpdateMarks.focus()
				return;
			 
			sql = "update student set maths=%d where rno=%d"
			args = (mar,rno)
			cursor = con.cursor()
			cursor.execute(sql%args)
			con.commit()
			msg = str(cursor.rowcount)+" records Updated "
			messagebox.showinfo("Success",msg)
			entUpdateRno.delete(first=0,last=100)
			entUpdateMarks.delete(first=0,last=100)
			entUpdateRno.focus()
			
		except ValueError as me:
			messagebox.showerror("Failure", "Rno or Marks cannot be Empty!!")
			entUpdateRno.delete(first=0,last=100)
			entUpdateMarks.delete(first=0,last=100)
			entUpdateRno.focus()
		
		except cx_Oracle.DatabaseError as e:
			con.rollback()
			messagebox.showerror("Failure :- Update Issue", e)
		finally:
			if cursor is not None:
				cursor.close()
			if con is not None:
				con.close()
	elif(r==3):
		con = None
		cursor=None
		try:
			con = cx_Oracle.connect('system/iupui')
			rno = int(entUpdateRno.get())
			mar = int(entUpdateMarks.get())
			if rno < 0 or mar < 0:
				messagebox.showerror("Failure","Only Positive Values Allowed!!")
				entUpdateRno.delete(first=0,last=100)
				entUpdateMarks.delete(first=0,last=100)
				entUpdateRno.focus()
				return;
				
			if mar > 100:
				messagebox.showerror("Failure","Marks > 100")
				entUpdateMarks.delete(first=0,last=100)
				entUpdateMarks.focus()
				return;
			
			sql = "update student set chemistry=%d where rno=%d"
			args = (mar,rno)
			cursor = con.cursor()
			cursor.execute(sql%args)
			con.commit()
			msg = str(cursor.rowcount)+" records Updated "
			messagebox.showinfo("Success",msg)
			entUpdateRno.delete(first=0,last=100)
			entUpdateMarks.delete(first=0,last=100)
			entUpdateRno.focus()
			
		except ValueError as me:
			messagebox.showerror("Failure", "Rno or Marks cannot be Empty!!")
			entUpdateRno.delete(first=0,last=100)
			entUpdateMarks.delete(first=0,last=100)
			entUpdateRno.focus()
		
		except cx_Oracle.DatabaseError as e:
			con.rollback()
			messagebox.showerror("Failure :- Update Issue", e)
		finally:
			if cursor is not None:
				cursor.close()
			if con is not None:
				con.close()

btnMarkUpdate = Button(upst,text="Update Student Marks Info.",font=("Arial",10,"bold"),command=up_marks)
		
def f6():
	con = None
	cursor = None	
	try:
		con = cx_Oracle.connect('system/iupui')
		rno_update = int(entUpdateRno.get())
		if rno_update < 0:
			messagebox.showerror("Failure","Rno Should be positive!!")
			entUpdateRno.delete(first=0,last=100)
			entUpdateName.delete(first=0,last=100)
			entUpdateRno.focus()
			return;
			
		name_update = entUpdateName.get()
		if len(name_update) == 0:
			messagebox.showerror("Failure","Name Field Empty!!")
			entUpdateRno.delete(first=0,last=100)
			entUpdateName.delete(first=0,last=100)
			entUpdateRno.focus()
			return;
			
		if not(name_update.isalpha()):
			messagebox.showerror("Failure","Only Alphabets Allowed!!")
			entUpdateRno.delete(first=0,last=100)
			entUpdateName.delete(first=0,last=100)
			entUpdateRno.focus()
			return;
			
		sql = "update student set name='%s' where rno='%d'"
		args = (name_update,rno_update)
		cursor = con.cursor()
		cursor.execute(sql%args)
		con.commit()
		msg = str(cursor.rowcount)+" records Updated "
		messagebox.showinfo("Success",msg)
		entUpdateRno.delete(first=0,last=100)
		entUpdateName.delete(first=0,last=100)
		entUpdateRno.focus()
	
	except ValueError as ve:
		messagebox.showerror("Failure","Empty Fields!!")
		entUpdateRno.delete(first=0,last=100)
		entUpdateName.delete(first=0,last=100)
		entUpdateRno.focus()
		
	except cx_Oracle.DatabaseError as e:
		con.rollback()
		messagebox.showerror("Failure :- Update Issue", e)
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()
btnUpdateSave = Button(upst,text='Save Update of Student Name',font = ("Arial",10,"bold"),width=25,command=f6)

def f7():
	entUpdateRno.delete(first=0,last=100)
	entUpdateName.delete(first=0,last=100)
	upst.withdraw()
	root.deiconify()
btnUpdateBack = Button(upst, text='Back to Main Menu',font = ("Arial",10,"bold"),width=20,command=f7)

lblUpdateRno.pack(pady=10)
entUpdateRno.pack(pady=10)
lblUpdateName.pack(pady=10)
entUpdateName.pack(pady=10)
btnUpdateSave.pack(pady=10)
lblUpdateMarks.pack(pady=10)

entUpdateMarks.pack(pady=10)

radio_physics.pack(pady=10)
radio_maths.pack(pady=10)
radio_chemistry.pack(pady=10)

btnMarkUpdate.pack(pady=10)
btnUpdateBack.pack(pady=10)

def f8():
	root.withdraw()
	upst.deiconify()
	entUpdateRno.focus()
btnUpdate = Button(root, text='Update Student Info.', font = ("Arial",15,"bold"),width=35, bd=5, command=f8)
btnUpdate.pack(pady=20)

dest = Toplevel(root)
dest.title("Delete Student")
dest.geometry("500x500+350+150")
dest.withdraw()

lblDeleteRno = Label(dest, text="Enter Roll No.",font = ("Arial",10,"bold"))
entDeleteRno = Entry(dest, font = ("Arial",10,"bold"),bd=5)

def f9():
	con = None
	cursor = None	
	try:
		con = cx_Oracle.connect('system/iupui')
		rno_delete = int(entDeleteRno.get())
		if rno_delete < 0:
			messagebox.showerror("Failure","Only Positive Values!!")
			entDeleteRno.delete(first=0,last=100)
			entDeleteRno.focus()
			return;
		
		sql = "delete from student where rno='%d'"
		args = (rno_delete)
		cursor = con.cursor()
		cursor.execute(sql%args)
		con.commit()
		msg = str(cursor.rowcount)+" records Deleted "
		messagebox.showinfo("Success",msg)
		entDeleteRno.delete(first=0,last=100)
		entDeleteRno.focus()
	
	except ValueError as e:
		messagebox.showerror("Failure","Empty Field")
		entDeleteRno.delete(first=0,last=100)
		entDeleteRno.focus()
	
	except cx_Oracle.DatabaseError as e:
		con.rollback()
		messagebox.showerror("Failure : Delete Issue", e)
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()
btnDeleteSave = Button(dest,text='Delete Student Info.',font = ("Arial",10,"bold"),width=20,command=f9)

def f10():
	entDeleteRno.delete(first=0,last=100)
	dest.withdraw()
	root.deiconify()
btnDeleteBack = Button(dest,text='Back To Main Menu',font = ("Arial",10,"bold"),width=20,command=f10)

lblDeleteRno.pack(pady=10)
entDeleteRno.pack(pady=10)
btnDeleteSave.pack(pady=10)
btnDeleteBack.pack(pady=10)

def f11():
	root.withdraw()
	dest.deiconify()
	entDeleteRno.focus()
btnDelete = Button(root, text='Delete Student Info.', font = ("Arial",15,"bold"),width=35, bd=5, command=f11)
btnDelete.pack(pady=20)

#-------------------------------------Graph----------------------------------#
from matplotlib import pyplot as plt
import numpy as np

'''graphView = Toplevel(root)
graphView.title("Student Marks Graph")
graphView.geometry('1200x630+50+50')
graphView.withdraw()
'''
'''def f13():
	graphView.withdraw()
	root.deiconify()
btnBackGraph = Button(graphView,text="Back to Main Menu",command=f13)
btnBackGraph.pack(pady=10)
'''
def f12():
	#root.withdraw()
	#graphView.deiconify()
	con = None
	cursor_name = None
	cursor_physics = None
	cursor_maths = None
	cursor_chemistry = None
	try:
		con = cx_Oracle.connect('system/iupui')
		cursor_name = con.cursor()
		sql_name = "select name from student"
		cursor_name.execute(sql_name)
		data_name = cursor_name.fetchall()
		list_name = list()
		for d in data_name:
			list_name.append(str(d[0]))
			
		cursor_physics = con.cursor()
		sql_physics = "select physics from student"
		cursor_physics.execute(sql_physics)
		data_physics = cursor_physics.fetchall()
		list_physics = list()
		for d1 in data_physics:
			list_physics.append(int(d1[0]))
			
		cursor_maths = con.cursor()
		sql_maths = "select maths from student"
		cursor_maths.execute(sql_maths)
		data_maths = cursor_maths.fetchall()
		list_maths = list()
		for d2 in data_maths:
			list_maths.append(int(d2[0]))
			
		cursor_chemistry = con.cursor()
		sql_chemistry = "select chemistry from student"
		cursor_chemistry.execute(sql_chemistry)
		data_chemistry = cursor_chemistry.fetchall()
		list_chemistry = list()
		for d3 in data_chemistry:
			list_chemistry.append(int(d3[0]))
		
		print(list_name)
		print(list_physics)
			
		x = np.arange(len(list_name))
		plt.bar(x,list_physics,width=0.25,label="Physics Marks",color="r")
		plt.bar(x+0.25,list_maths,width=0.25,label="Maths Marks",color="b")
		plt.bar(x+0.50,list_chemistry,width=0.25,label="Chemistry Marks",color="g")
		plt.xticks(x,list_name,fontsize=10)
		
		plt.xlabel("Name",fontsize=20)
		plt.ylabel("Marks",fontsize=20)
		plt.legend(shadow=True)
		plt.grid()
		plt.show()
		
	except IndexError as ie:
		messagebox.showerror("No Records to form Graph!!")
		
	except cx_Oracle.DatabaseError as e:
		messagebox.showerror("Select Issue ", e)
		
		
btnViewGraph = Button(root,text="View Marks Graph",font = ("Arial",15,"bold"),width=35, bd=5, command=f12)
btnViewGraph.pack(pady=20)

root.mainloop()