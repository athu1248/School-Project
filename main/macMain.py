import copy
import datetime
import mysql.connector as mysql
import random
import tkinter
from tkinter import ttk
import tkinter.messagebox
import validators

global testDict
testDict = {
    "SAT": 1,
    "TOEFL": 2,
    "IELTS": 3,
    "SAT Maths 2": 4,
    "SAT Maths 1": 5,
    "SAT Literature": 6,
    "SAT Philosophy": 7,
    "SAT Japanese": 8,
    "SAT US History": 9,
    "SAT World History": 10,
    "JLPTN1": 11,
    "JLPTN2": 12,
    "JLPTN3": 13,
    "JLPTN4": 14,
    "JLPTN5": 15,
}
global testList
testList = list(testDict.keys())

global subjectDict
subjectDict = {
    "Maths": 1,
    "Physics": 2,
    "Chemistry": 3,
    "English": 4,
    "Biology": 5,
    "History": 6,
    "Economics": 7,
    "Entrepreneurship": 8,
    "Accounting": 9,
    "Computer Science": 10,
    "Psychology": 11,
}
global subjectList
subjectList = list(subjectDict.keys())

global monthDict
monthDict = {
    "Jan": "1",
    "Feb": "2",
    "Mar": "3",
    "Apr": "4",
    "May": "5",
    "Jun": "6",
    "Jul": "7",
    "Aug": "8",
    "Sep": "9",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12",
}
global monthList
monthList = list(monthDict.keys())

global font1
font1 = ("Verdana", 20, "bold")
global font2
font2 = ("Comic Sans MS", 20)

global smallfont1
smallfont1 = ("Verdana", 15, "bold")
global smallfont2
smallfont2 = ("Comic Sans MS", 15)

global con
con = mysql.connect(host="computerproject.ctyzmdqqhkym.ap-northeast-1.rds.amazonaws.com",
                    user="admin", passwd="athuchinlucy", database="tfdb")
if con.is_connected():
    print("Connection is successfull!!")
else:
    print("Not connected!")


class loginWindow:
    def __init__(self, window, errorText=""):
        for widget in window.winfo_children():
            widget.destroy()
        window.geometry("1000x500")
        self.frame1 = tkinter.Frame(window)
        self.frame2 = tkinter.Frame(window, bg="PaleTurquoise1")
        self.frame3 = tkinter.Frame(
            self.frame2,
            bg="PaleTurquoise2",
            borderwidth="1",
            padx="5",
            pady="5",
            relief=tkinter.GROOVE,
        )

        self.frame1.place(relx=0, relwidth=0.7, relheight=1)
        self.frame2.place(relx=0.7, relwidth=0.3, relheight=1)
        self.frame3.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        # Frame 1
        canvas1 = tkinter.Canvas(self.frame1, bg="blue")
        canvas1.pack(fill="both", expand=True)
        canvas1.update()
        welcomeText = canvas1.create_text(
            canvas1.winfo_width() // 2,
            500,
            width=canvas1.winfo_width()-100,
            justify=tkinter.CENTER,
            text="Welcome To Student-4-Student!",
            fill="White",
            font="Verdana 40 bold",
        )
        paratext = canvas1.create_text(
            canvas1.winfo_width() // 2,
            680,
            width=canvas1.winfo_width()-100,
            justify=tkinter.CENTER,
            text="Student-4-Student is an online service where students can either learn or teach a particular subject of their interest. One can also provide details regarding colleges, schools, tests, and courses for collaborative information sharing. As students, it isn't easy to find reliable direct information about universities, such as establishing direct contact with a student currently studying in the same university/school we are planning to apply to.",
            fill="White",
            font="Verdana 20 bold",
        )
        xinc = 0
        yinc = -1
        #yinc = 0.5

        while True:
            canvas1.move(welcomeText, xinc, yinc)
            canvas1.move(paratext, xinc, yinc)

            canvas1.update()

            y = canvas1.bbox(welcomeText)[1]
            if y < 50:
                break

        # Frame 3
        Emaillbl = tkinter.Label(
            self.frame3, text="Email", bg="PaleTurquoise1", fg="Blue4", font=font1
        )
        Emaillbl.pack()
        self.Email = tkinter.Entry(self.frame3, bg="alice blue", font=font2)
        self.Email.pack()

        passwordlbl = tkinter.Label(
            self.frame3, text="Password", bg="PaleTurquoise1", fg="Blue4", font=font1
        )
        passwordlbl.pack()
        self.password = tkinter.Entry(
            self.frame3, bg="alice blue", show="*", font=font2
        )
        self.password.pack()

        self.submit = tkinter.Button(
            self.frame3, text="Login", bg="RoyalBlue1", font=font1, command=self.login
        )
        self.submit.pack(side=tkinter.TOP)

        self.signup = tkinter.Button(
            self.frame3,
            text="Create new account",
            bg="RoyalBlue1",
            font=font1,
            command=self.signupwindow,
        )
        self.signup.pack(side=tkinter.TOP)

        self.loginErrlbl = tkinter.Label(
            self.frame2,
            text=errorText,
            bg="PaleTurquoise1",
            fg="red",
            font=smallfont1,
            wraplength=self.frame2.winfo_width() - 10,
        )
        if errorText != "":
            self.loginErrlbl.pack()

        # Adding bubles in frame1
        # bbl1 = tkinter.Canvas.create_oval(canvas1.winfo_height)

    def login(self):
        email = self.Email.get()
        password = self.password.get()
        cursor = con.cursor()
        cursor.execute(
            "SELECT * FROM AccDetails WHERE Email='"
            + str(email)
            + "'AND Password='"
            + str(password)
            + "';"
        )
        records = cursor.fetchall()
        if len(records) == 1:
            self.loginErrlbl.pack_forget()
            if records[0][0] == "admin":
                adminwindow(window)
            else:
                profileWindow(window, list(records[0]))
        else:
            self.loginErrlbl.configure(
                text="*Incorrect Email or Password. Please try again.*"
            )
            self.loginErrlbl.pack()
        cursor.close()

    def signupwindow(self):
        signupWindow(window)


class signupWindow:
    def __init__(self, window):
        window.configure(bg="Blue")
        window.geometry("1200x500")
        for widget in window.winfo_children():
            widget.destroy()

        # FRAME 1
        self.frame1 = tkinter.Frame(
            window,
            bg="PaleTurquoise2",
            borderwidth="1",
            padx="25",
            pady="35",
            relief=tkinter.GROOVE,
        )

        accLbl = tkinter.Label(
            self.frame1, text="Please enter your account details", font=font1)
        accLbl.grid(row=0, column=0, columnspan=2)
        notelbl = tkinter.Label(
            self.frame1, text="Note: Email, First Name, and Last Name cannot be changed later.", font=smallfont1, bg="PaleTurquoise2")
        notelbl.grid(row=1, column=0, columnspan=2)

        Emaillbl = tkinter.Label(
            self.frame1, text="Email*:", bg="PaleTurquoise1", fg="Blue4", font=font1
        )
        Emaillbl.grid(row=2, column=0)
        self.Email = tkinter.Entry(self.frame1, font=font2)
        self.Email.grid(row=2, column=1)

        passwordlbl = tkinter.Label(
            self.frame1, text="Password*:", bg="PaleTurquoise1", fg="Blue4", font=font1
        )
        passwordlbl.grid(row=3, column=0)
        self.Password = tkinter.Entry(self.frame1, show="*", font=font2)
        self.Password.grid(row=3, column=1)

        firstnamelbl = tkinter.Label(
            self.frame1, text="First Name*:", bg="PaleTurquoise1", fg="Blue4", font=font1
        )
        firstnamelbl.grid(row=4, column=0)
        self.FirstName = tkinter.Entry(self.frame1, font=font2)
        self.FirstName.grid(row=4, column=1)

        lastnamelbl = tkinter.Label(
            self.frame1, text="Last Name*:", bg="PaleTurquoise1", fg="Blue4", font=font1
        )
        lastnamelbl.grid(row=5, column=0)
        self.LastName = tkinter.Entry(self.frame1, font=font2)
        self.LastName.grid(row=5, column=1)

        randomlbl = tkinter.Label(
            self.frame1, text="* is a required field", font=smallfont2, bg="PaleTurquoise2")
        randomlbl.grid(row=6, column=0)

        self.cancel1 = tkinter.Button(
            self.frame1,
            text="Cancel",
            bg="RoyalBlue1",
            font=font1,
            command=self.cancelBtnFunc,
        )
        self.cancel1.grid(row=7, column=0)

        self.next1 = tkinter.Button(
            self.frame1,
            text="Next",
            bg="RoyalBlue1",
            font=font1,
            command=self.nextBtnFunc1,
        )
        self.next1.grid(row=7, column=1)

        self.lblx = tkinter.Label(
            window, bg="blue", fg="red", font=smallfont1)

        self.frame1.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        # FRAME 2
        self.frame2 = tkinter.Frame(
            window,
            bg="PaleTurquoise2",
            borderwidth="1",
            padx="15",
            pady="15",
            relief=tkinter.GROOVE,
        )

        lbl1 = tkinter.Label(self.frame2, text="Enter your qualifications:-",
                             bg="PaleTurquoise1", fg="Blue4", font=smallfont1)
        lbl1.grid(row=0, column=0, columnspan=2)

        hslbl = tkinter.Label(
            self.frame2,
            text="High School:",
            bg="PaleTurquoise1",
            fg="Blue4",
            font=smallfont1,
        )
        hslbl.grid(row=1, column=0)
        self.Highschool = tkinter.Entry(self.frame2, font=smallfont2)
        self.Highschool.grid(row=1, column=1)

        uglbl = tkinter.Label(
            self.frame2,
            text="Undergraduate School:",
            bg="PaleTurquoise1",
            fg="Blue4",
            font=smallfont1,
        )
        uglbl.grid(row=2, column=0)
        self.Undergraduate = tkinter.Entry(self.frame2, font=smallfont2)
        self.Undergraduate.grid(row=2, column=1)

        glbl = tkinter.Label(
            self.frame2,
            text="Graduate School:",
            bg="PaleTurquoise1",
            fg="Blue4",
            font=smallfont1,
        )
        glbl.grid(row=3, column=0)
        self.Graduate = tkinter.Entry(self.frame2, font=smallfont2)
        self.Graduate.grid(row=3, column=1)

        doblbl = tkinter.Label(
            self.frame2, text="Enter your Date of Birth:-", bg="PaleTurquoise1", fg="Blue4", font=smallfont1
        )
        doblbl.grid(row=4, column=0, columnspan=2)

        yearlbl = tkinter.Label(
            self.frame2,
            text="Year*:",
            bg="PaleTurquoise1",
            fg="Blue4",
            font=smallfont1,
        )
        yearlbl.grid(row=5, column=0)
        self.Year = ttk.Combobox(
            self.frame2, values=self.getAllYears(), font=smallfont2)
        self.Year["state"] = "readonly"
        self.Year.grid(row=5, column=1)
        self.Year.bind("<<ComboboxSelected>>", self.disableYear)
        monthlbl = tkinter.Label(
            self.frame2,
            text="Month*:",
            bg="PaleTurquoise1",
            fg="Blue4",
            font=smallfont1,
        )
        monthlbl.grid(row=6, column=0)
        self.Month = ttk.Combobox(
            self.frame2,
            values=monthList,
            font=smallfont2
        )
        self.Month["state"] = "disabled"
        self.Month.grid(row=6, column=1)
        self.Month.bind("<<ComboboxSelected>>", self.disableMonth)
        daylbl = tkinter.Label(
            self.frame2, text="Day*:", bg="PaleTurquoise1", fg="Blue4", font=smallfont1
        )
        daylbl.grid(row=7, column=0)
        self.Day = ttk.Combobox(self.frame2, values=[], font=smallfont2)
        self.Day["state"] = "disabled"
        self.Day.grid(row=7, column=1)
        self.Day.bind("<<ComboboxSelected>>", self.disableDay)

        self.resetDOBBtn = tkinter.Button(
            self.frame2,
            text="Reset DOB",
            bg="RoyalBlue1",
            font=smallfont1,
            command=self.resetDOB,
        )
        self.resetDOBBtn.grid(row=8, column=1)

        randomlbl1 = tkinter.Label(
            self.frame2, text="* is a required field", font=smallfont2, bg="PaleTurquoise2")
        randomlbl1.grid(row=8, column=0)

        subjectSelectlbl = tkinter.Label(
            self.frame2, text="Select subjects and tests you want to TEACH:", font=font1
        )
        subjectSelectlbl.grid(row=0, column=2, columnspan=4)

        sub1lbl = tkinter.Label(
            self.frame2, text="Subject 1:", bg="PaleTurquoise1", fg="Blue4", font=smallfont1
        )
        sub1lbl.grid(row=1, column=2)
        self.Sub1 = ttk.Combobox(self.frame2, values=[
                                 "None"] + subjectList, font=smallfont2)
        self.Sub1.current(0)
        self.Sub1["state"] = "readonly"
        self.Sub1.grid(row=1, column=3)
        self.Sub1.bind("<<ComboboxSelected>>", self.disableSub1)

        sub2lbl = tkinter.Label(
            self.frame2, text="Subject 2:", bg="PaleTurquoise1", fg="Blue4", font=smallfont1
        )
        sub2lbl.grid(row=2, column=2)
        self.Sub2 = ttk.Combobox(self.frame2, values=[], font=smallfont2)
        self.Sub2["state"] = "disabled"
        self.Sub2.grid(row=2, column=3)
        self.Sub2.bind("<<ComboboxSelected>>", self.disableSub2)

        sub3lbl = tkinter.Label(
            self.frame2, text="Subject 3:", bg="PaleTurquoise1", fg="Blue4", font=smallfont1
        )
        sub3lbl.grid(row=3, column=2)
        self.Sub3 = ttk.Combobox(self.frame2, values=[], font=smallfont2)
        self.Sub3["state"] = "disabled"
        self.Sub3.grid(row=3, column=3)
        self.Sub3.bind("<<ComboboxSelected>>", self.disableSub3)

        sub4lbl = tkinter.Label(
            self.frame2, text="Subject 4:", bg="PaleTurquoise1", fg="Blue4", font=smallfont1
        )
        sub4lbl.grid(row=4, column=2)
        self.Sub4 = ttk.Combobox(self.frame2, values=[], font=smallfont2)
        self.Sub4["state"] = "disabled"
        self.Sub4.grid(row=4, column=3)
        self.Sub4.bind("<<ComboboxSelected>>", self.disableSub4)

        sub5lbl = tkinter.Label(
            self.frame2, text="Subject 5:", bg="PaleTurquoise1", fg="Blue4", font=smallfont1
        )
        sub5lbl.grid(row=5, column=2)
        self.Sub5 = ttk.Combobox(self.frame2, values=[], font=smallfont2)
        self.Sub5["state"] = "disabled"
        self.Sub5.grid(row=5, column=3)
        self.Sub5.bind("<<ComboboxSelected>>", self.disableSub5)

        test1lbl = tkinter.Label(
            self.frame2, text="Test 1:", bg="PaleTurquoise1", fg="Blue4", font=smallfont1
        )
        test1lbl.grid(row=1, column=4)
        self.Test1 = ttk.Combobox(
            self.frame2, values=["None"] + testList, font=smallfont2)
        self.Test1.current(0)
        self.Test1["state"] = "readonly"
        self.Test1.grid(row=1, column=5)
        self.Test1.bind("<<ComboboxSelected>>", self.disableTest1)

        test2lbl = tkinter.Label(
            self.frame2, text="Test 2:", bg="PaleTurquoise1", fg="Blue4", font=smallfont1
        )
        test2lbl.grid(row=2, column=4)
        self.Test2 = ttk.Combobox(self.frame2, values=[], font=smallfont2)
        self.Test2["state"] = "disabled"
        self.Test2.grid(row=2, column=5)
        self.Test2.bind("<<ComboboxSelected>>", self.disableTest2)

        test3lbl = tkinter.Label(
            self.frame2, text="Test 3:", bg="PaleTurquoise1", fg="Blue4", font=smallfont1
        )
        test3lbl.grid(row=3, column=4)
        self.Test3 = ttk.Combobox(self.frame2, values=[], font=smallfont2)
        self.Test3["state"] = "disabled"
        self.Test3.grid(row=3, column=5)
        self.Test3.bind("<<ComboboxSelected>>", self.disableTest3)

        test4lbl = tkinter.Label(
            self.frame2, text="Test 4:", bg="PaleTurquoise1", fg="Blue4", font=smallfont1
        )
        test4lbl.grid(row=4, column=4)
        self.Test4 = ttk.Combobox(self.frame2, values=[], font=smallfont2)
        self.Test4["state"] = "disabled"
        self.Test4.grid(row=4, column=5)
        self.Test4.bind("<<ComboboxSelected>>", self.disableTest4)

        test5lbl = tkinter.Label(
            self.frame2, text="Test 5:", bg="PaleTurquoise1", fg="Blue4", font=smallfont1
        )
        test5lbl.grid(row=5, column=4)
        self.Test5 = ttk.Combobox(self.frame2, values=[], font=smallfont2)
        self.Test5["state"] = "disabled"
        self.Test5.grid(row=5, column=5)
        self.Test5.bind("<<ComboboxSelected>>", self.disableTest5)

        self.resetSubsBtn = tkinter.Button(
            self.frame2,
            text="Reset Subjects",
            bg="RoyalBlue1",
            font=smallfont1,
            command=self.resetSubjects,
        )
        self.resetSubsBtn.grid(row=6, column=3)

        self.resetTestsBtn = tkinter.Button(
            self.frame2,
            text="Reset Tests",
            bg="RoyalBlue1",
            font=smallfont1,
            command=self.resetTests,
        )
        self.resetTestsBtn.grid(row=6, column=5)

        self.cancel2 = tkinter.Button(
            self.frame2,
            text="Cancel",
            bg="RoyalBlue1",
            font=font1,
            command=self.cancelBtnFunc,
        )
        self.cancel2.grid(row=9, column=3)

        self.submit = tkinter.Button(
            self.frame2,
            text="Sign up",
            bg="RoyalBlue1",
            font=font1,
            command=self.checksignup,
        )
        self.submit.grid(row=9, column=5)

        self.lblx2 = tkinter.Label(
            window, bg="blue", fg="red", font=smallfont1)

    def getAllYears(self):
        yearList = []
        yearNow = datetime.datetime.now().year
        for i in range(yearNow - 100, yearNow + 1, 1):
            yearList.append(i)
        return yearList

    def getAllDays(self):
        dayList = []
        month = self.Month.get()
        if month == "Feb":
            if int(self.Year.get()) % 4 == 0:
                for i in range(1, 30, 1):
                    dayList.append(i)
            else:
                for i in range(1, 29, 1):
                    dayList.append(i)
        elif month in ["Apr", "Jun", "Sep", "Nov"]:
            for i in range(1, 31, 1):
                dayList.append(i)
        else:
            for i in range(1, 32, 1):
                dayList.append(i)
        return dayList

    def nextBtnFunc1(self):
        if self.Email.get() == "":
            self.lblx.configure(text="*Email not entered*")
            self.lblx.pack()
        elif len(self.Email.get()) > 50:
            self.lblx.configure(
                text="*Email is too long (50 character limit)*")
            self.lblx.pack()
        elif validators.email(self.Email.get()) != True:
            self.lblx.configure(text="*Please enter a valid email*")
            self.lblx.pack()
        elif self.Password.get() == "":
            self.lblx.configure(text="*Password not entered*")
            self.lblx.pack()
        elif len(self.Password.get()) > 50:
            self.lblx.configure(
                text="*Password is too long (50 character limit)*")
            self.lblx.pack()
        elif self.FirstName.get() == "":
            self.lblx.configure(text="*First name not entered*")
            self.lblx.pack()
        elif len(self.FirstName.get()) > 50:
            self.lblx.configure(
                text="*First name is too long (50 character limit)*")
            self.lblx.pack()
        elif self.LastName.get() == "":
            self.lblx.configure(text="*Last name not entered*")
            self.lblx.pack()
        elif len(self.LastName.get()) > 50:
            self.lblx.configure(
                text="*Last name is too long (60 character limit)*")
            self.lblx.pack()
        else:
            cursor = con.cursor()
            cursor.execute(
                "SELECT * FROM AccDetails WHERE Email = '{}'".format(self.Email.get()))
            records = cursor.fetchall()
            cursor.close()
            if len(records) == 0:
                self.lblx.pack_forget()
                self.frame1.place_forget()
                self.frame2.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
            else:
                self.lblx.configure(text="*Email is already used*")
                self.lblx.pack()

    def cancelBtnFunc(self):
        loginWindow(window)

    def disableYear(self, *args):
        self.Year["state"] = "disabled"
        self.Month["state"] = "readonly"

    def disableMonth(self, *args):
        self.Month["state"] = "disabled"
        self.Day["state"] = "readonly"
        self.Day["values"] = self.getAllDays()

    def disableDay(self, *args):
        self.Day["state"] = "disabled"

    def disableSub1(self, *args):
        self.Sub1["state"] = "disabled"
        self.Sub2["state"] = "readonly"
        self.Sub2["values"] = ["None"] + self.changeSubList()
        self.Sub2.current(0)

    def disableSub2(self, *args):
        self.Sub2["state"] = "disabled"
        self.Sub3["state"] = "readonly"
        self.Sub3["values"] = ["None"] + self.changeSubList()
        self.Sub3.current(0)

    def disableSub3(self, *args):
        self.Sub3["state"] = "disabled"
        self.Sub4["state"] = "readonly"
        self.Sub4["values"] = ["None"] + self.changeSubList()
        self.Sub4.current(0)

    def disableSub4(self, *args):
        self.Sub4["state"] = "disabled"
        self.Sub5["state"] = "readonly"
        self.Sub5["values"] = ["None"] + self.changeSubList()
        self.Sub5.current(0)

    def disableSub5(self, *args):
        self.Sub5["state"] = "disabled"

    def disableTest1(self, *args):
        self.Test1["state"] = "disabled"
        self.Test2["state"] = "readonly"
        self.Test2["values"] = ["None"] + self.changeTestList()
        self.Test2.current(0)

    def disableTest2(self, *args):
        self.Test2["state"] = "disabled"
        self.Test3["state"] = "readonly"
        self.Test3["values"] = ["None"] + self.changeTestList()
        self.Test3.current(0)

    def disableTest3(self, *args):
        self.Test3["state"] = "disabled"
        self.Test4["state"] = "readonly"
        self.Test4["values"] = ["None"] + self.changeTestList()
        self.Test4.current(0)

    def disableTest4(self, *args):
        self.Test4["state"] = "disabled"
        self.Test5["state"] = "readonly"
        self.Test5["values"] = ["None"] + self.changeTestList()
        self.Test5.current(0)

    def disableTest5(self, *args):
        self.Test5["state"] = "disabled"

    def changeSubList(self):
        subList = copy.deepcopy(subjectList)
        if self.Sub1.get() in subjectList:
            subList.remove(self.Sub1.get())
        if self.Sub2.get() in subjectList:
            subList.remove(self.Sub2.get())
        if self.Sub3.get() in subjectList:
            subList.remove(self.Sub3.get())
        if self.Sub4.get() in subjectList:
            subList.remove(self.Sub4.get())
        if self.Sub5.get() in subjectList:
            subList.remove(self.Sub5.get())
        return subList

    def changeTestList(self):
        tList = copy.deepcopy(testList)
        if self.Test1.get() in tList:
            tList.remove(self.Test1.get())
        if self.Test2.get() in tList:
            tList.remove(self.Test2.get())
        if self.Test3.get() in tList:
            tList.remove(self.Test3.get())
        if self.Test4.get() in tList:
            tList.remove(self.Test4.get())
        if self.Test5.get() in tList:
            tList.remove(self.Test5.get())
        return tList

    def resetSubjects(self):
        self.Sub1["values"] = ["None"] + subjectList
        self.Sub1["state"] = "readonly"
        self.Sub2["state"] = "disabled"
        self.Sub3["state"] = "disabled"
        self.Sub4["state"] = "disabled"
        self.Sub5["state"] = "disabled"
        self.Sub1.current(0)
        self.Sub1.set("")
        self.Sub2.set("")
        self.Sub3.set("")
        self.Sub4.set("")
        self.Sub5.set("")

    def resetTests(self):
        self.Test1["values"] = ["None"] + testList
        self.Test1["state"] = "readonly"
        self.Test2["state"] = "disabled"
        self.Test3["state"] = "disabled"
        self.Test4["state"] = "disabled"
        self.Test5["state"] = "disabled"
        self.Test1.current(0)
        self.Test1.set("")
        self.Test2.set("")
        self.Test3.set("")
        self.Test4.set("")
        self.Test5.set("")

    def resetDOB(self):
        self.Year["state"] = "readonly"
        self.Month["state"] = "disabled"
        self.Day["state"] = "disabled"
        self.Year.set("")
        self.Month.set("")
        self.Day.set("")

    def checksignup(self):
        if self.Year.get() == "":
            self.lblx2.configure(text="Year not entered")
            self.lblx2.pack()
        elif self.Month.get() == "":
            self.lblx2.configure(text="Month not entered")
            self.lblx2.pack()
        elif self.Day.get() == "":
            self.lblx2.configure(text="Day not entered")
            self.lblx2.pack()
        elif len(self.Highschool.get()) > 50:
            self.lblx.configure(
                text="*High school is too long (50 character limit)*")
            self.lblx.pack()
        elif len(self.Undergraduate.get()) > 50:
            self.lblx.configure(
                text="*Undergraduate is too long (50 character limit)*")
            self.lblx.pack()
        elif len(self.Graduate.get()) > 50:
            self.lblx.configure(
                text="*Graduate is too long (50 character limit)*")
            self.lblx.pack()
        else:
            DOB1 = (
                self.Year.get()
                + "-"
                + monthDict[self.Month.get()]
                + "-"
                + self.Day.get()
            )

            S1 = self.Sub1.get()
            if S1 == "None" or S1 == "":
                S1 = ""
            S2 = self.Sub2.get()
            if S2 == "None" or S2 == "":
                S2 = ""
            S3 = self.Sub3.get()
            if S3 == "None" or S3 == "":
                S3 = ""
            S4 = self.Sub4.get()
            if S4 == "None" or S4 == "":
                S4 = ""
            S5 = self.Sub5.get()
            if S5 == "None" or S5 == "":
                S5 = ""

            T1 = self.Test1.get()
            if T1 == "None" or T1 == "":
                T1 = ""
            T2 = self.Test2.get()
            if T2 == "None" or T2 == "":
                T2 = ""
            T3 = self.Test3.get()
            if T3 == "None" or T3 == "":
                T3 = ""
            T4 = self.Test4.get()
            if T4 == "None" or T4 == "":
                T4 = ""
            T5 = self.Test5.get()
            if T5 == "None" or T5 == "":
                T5 = ""

            self.signup(
                DOB1,
                S1,
                S2,
                S3,
                S4,
                S5,
                T1,
                T2,
                T3,
                T4,
                T5,
            )

    def signup(
        self,
        DOB1,
        S1,
        S2,
        S3,
        S4,
        S5,
        T1,
        T2,
        T3,
        T4,
        T5,
    ):
        cursor = con.cursor()
        try:
            cursor.execute(
                "INSERT INTO AccDetails values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}', 'no')".format(
                    self.Email.get(),
                    self.Password.get(),
                    self.FirstName.get(),
                    self.LastName.get(),
                    self.Highschool.get(),
                    self.Undergraduate.get(),
                    self.Graduate.get(),
                    DOB1,
                    S1,
                    S2,
                    S3,
                    S4,
                    S5,
                    T1,
                    T2,
                    T3,
                    T4,
                    T5,
                )
            )

            con.commit()

            cursor.execute(
                "SELECT * FROM AccDetails WHERE Email='" + str(self.Email.get()) + "';")
            records = cursor.fetchall()
            cursor.close()
            if len(records) == 1:
                profileWindow(window, list(records[0]))

        except mysql.Error as Err:
            print(Err)


class profileWindow:
    def __init__(self, window, record):
        self.record1 = record
        for widget in window.winfo_children():
            widget.destroy()

        window.configure(bg="Blue")
        window.geometry("1300x500")
        for widget in window.winfo_children():
            widget.destroy()

        self.record = record

        self.frame1 = tkinter.Frame(
            window,
            bg="PaleTurquoise2",
            borderwidth="1",
            padx="25",
            pady="35",
            relief=tkinter.GROOVE,
        )

        if record[-1] == "no":
            qualifyLbl = tkinter.Label(window, text="To be searched by other students in Tutor Look-up!, please email certificates of your qualifications to admstudent4student@gmail.com",
                                       wraplength=window.winfo_width() - 10, font=smallfont1)
            qualifyLbl.pack()

        profileFrame(self.frame1, self.record)

        tutorlookup = tkinter.Button(
            self.frame1,
            text="Tutor Look-up!",
            bg="RoyalBlue1",
            font=font1,
            command=self.search,
        )
        tutorlookup.grid(row=9, column=0)

        update = tkinter.Button(
            self.frame1,
            text="Update",
            bg="RoyalBlue1",
            command=self.update,
            font=font1,
        )
        update.grid(row=0, column=8)

        signOut = tkinter.Button(
            self.frame1,
            text="Sign out",
            bg="RoyalBlue1",
            command=self.signout,
            font=font1,
        )
        signOut.grid(row=1, column=8)

        self.frame1.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.frame1.update()

    def profilepic(self):
        pic1 = tkinter.PhotoImage(file="./pig.png")
        pic2 = tkinter.PhotoImage(file="./bear.png")
        pic3 = tkinter.PhotoImage(file="./elephant.png")
        pic4 = tkinter.PhotoImage(file="./horse.png")
        pic5 = tkinter.PhotoImage(file="./dog.png")
        lst = [pic1, pic2, pic3, pic4, pic5]
        pic = random.choice(lst)
        return pic

    def search(self):
        searchWindow(window, self.record1)

    def signout(self):
        loginWindow(window)

    def update(self):
        updateWindow(window, self.record)


class updateWindow:
    def __init__(self, window, record):
        window.configure(bg="Blue")
        window.geometry("1200x500")
        for widget in window.winfo_children():
            widget.destroy()

        self.record = record

        # FRAME 1
        self.frame1 = tkinter.Frame(
            window,
            bg="PaleTurquoise2",
            borderwidth="1",
            padx="15",
            pady="15",
            relief=tkinter.GROOVE,
        )

        self.frame1.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        lbl1 = tkinter.Label(self.frame1, text="Enter your qualifications:-",
                             bg="PaleTurquoise1", fg="Blue4", font=smallfont1)
        lbl1.grid(row=0, column=0, columnspan=2)

        hslbl = tkinter.Label(
            self.frame1,
            text="High School:",
            bg="PaleTurquoise1",
            fg="Blue4",
            font=smallfont1,
        )
        hslbl.grid(row=1, column=0)
        self.Highschool = tkinter.Entry(self.frame1, font=smallfont2)
        self.Highschool.insert(0, record[4])
        self.Highschool.grid(row=1, column=1)

        uglbl = tkinter.Label(
            self.frame1,
            text="Undergraduate School:",
            bg="PaleTurquoise1",
            fg="Blue4",
            font=smallfont1,
        )
        uglbl.grid(row=2, column=0)
        self.Undergraduate = tkinter.Entry(self.frame1, font=smallfont2)
        self.Undergraduate.insert(0, record[5])
        self.Undergraduate.grid(row=2, column=1)

        glbl = tkinter.Label(
            self.frame1,
            text="Graduate School:",
            bg="PaleTurquoise1",
            fg="Blue4",
            font=smallfont1,
        )
        glbl.grid(row=3, column=0)
        self.Graduate = tkinter.Entry(self.frame1, font=smallfont2)
        self.Graduate.insert(0, record[6])
        self.Graduate.grid(row=3, column=1)

        changeplbl = tkinter.Label(
            self.frame1,
            text="Change Password:",
            bg="PaleTurquoise1",
            fg="Blue4",
            font=smallfont1,
        )
        changeplbl.grid(row=5, column=0)

        oldplbl = tkinter.Label(
            self.frame1,
            text="Old Password:",
            bg="PaleTurquoise1",
            fg="Blue4",
            font=smallfont1,
        )
        oldplbl.grid(row=6, column=0)
        self.oldPassword = tkinter.Entry(self.frame1, font=smallfont2)
        self.oldPassword.grid(row=6, column=1)

        newplbl = tkinter.Label(
            self.frame1,
            text="New Password:",
            bg="PaleTurquoise1",
            fg="Blue4",
            font=smallfont1,
        )
        newplbl.grid(row=7, column=0)
        self.newPassword = tkinter.Entry(self.frame1, font=smallfont2)
        self.newPassword.grid(row=7, column=1)

        subjectSelectlbl = tkinter.Label(
            self.frame1, text="Select subjects and tests you want to TEACH:", font=font1
        )
        subjectSelectlbl.grid(row=0, column=2, columnspan=4)

        sub1lbl = tkinter.Label(
            self.frame1, text="Subject 1:", bg="PaleTurquoise1", fg="Blue4", font=smallfont1
        )
        sub1lbl.grid(row=1, column=2)
        self.Sub1 = ttk.Combobox(self.frame1, values=[
                                 "None"] + subjectList, font=smallfont2)
        self.Sub1.grid(row=1, column=3)
        self.Sub1.bind("<<ComboboxSelected>>", self.disableSub1)

        sub2lbl = tkinter.Label(
            self.frame1, text="Subject 2:", bg="PaleTurquoise1", fg="Blue4", font=smallfont1
        )
        sub2lbl.grid(row=2, column=2)
        self.Sub2 = ttk.Combobox(self.frame1, values=[
                                 "None"] + subjectList, font=smallfont2)
        self.Sub2.grid(row=2, column=3)
        self.Sub2.bind("<<ComboboxSelected>>", self.disableSub2)

        sub3lbl = tkinter.Label(
            self.frame1, text="Subject 3:", bg="PaleTurquoise1", fg="Blue4", font=smallfont1
        )
        sub3lbl.grid(row=3, column=2)
        self.Sub3 = ttk.Combobox(self.frame1, values=[
                                 "None"] + subjectList, font=smallfont2)
        self.Sub3.grid(row=3, column=3)
        self.Sub3.bind("<<ComboboxSelected>>", self.disableSub3)

        sub4lbl = tkinter.Label(
            self.frame1, text="Subject 4:", bg="PaleTurquoise1", fg="Blue4", font=smallfont1
        )
        sub4lbl.grid(row=4, column=2)
        self.Sub4 = ttk.Combobox(self.frame1, values=[
                                 "None"] + subjectList, font=smallfont2)
        self.Sub4.grid(row=4, column=3)
        self.Sub4.bind("<<ComboboxSelected>>", self.disableSub4)

        sub5lbl = tkinter.Label(
            self.frame1, text="Subject 5:", bg="PaleTurquoise1", fg="Blue4", font=smallfont1
        )
        sub5lbl.grid(row=5, column=2)
        self.Sub5 = ttk.Combobox(self.frame1, values=[
                                 "None"] + subjectList, font=smallfont2)
        self.Sub5.grid(row=5, column=3)

        test1lbl = tkinter.Label(
            self.frame1, text="Test 1:", bg="PaleTurquoise1", fg="Blue4", font=smallfont1
        )
        test1lbl.grid(row=1, column=4)
        self.Test1 = ttk.Combobox(
            self.frame1, values=["None"] + testList, font=smallfont2)
        self.Test1.grid(row=1, column=5)
        self.Test1.bind("<<ComboboxSelected>>", self.disableTest1)

        test2lbl = tkinter.Label(
            self.frame1, text="Test 2:", bg="PaleTurquoise1", fg="Blue4", font=smallfont1
        )
        test2lbl.grid(row=2, column=4)
        self.Test2 = ttk.Combobox(
            self.frame1, values=["None"] + testList, font=smallfont2)
        self.Test2.grid(row=2, column=5)
        self.Test2.bind("<<ComboboxSelected>>", self.disableTest2)

        test3lbl = tkinter.Label(
            self.frame1, text="Test 3:", bg="PaleTurquoise1", fg="Blue4", font=smallfont1
        )
        test3lbl.grid(row=3, column=4)
        self.Test3 = ttk.Combobox(
            self.frame1, values=["None"] + testList, font=smallfont2)
        self.Test3.grid(row=3, column=5)
        self.Test3.bind("<<ComboboxSelected>>", self.disableTest3)

        test4lbl = tkinter.Label(
            self.frame1, text="Test 4:", bg="PaleTurquoise1", fg="Blue4", font=smallfont1
        )
        test4lbl.grid(row=4, column=4)
        self.Test4 = ttk.Combobox(
            self.frame1, values=["None"] + testList, font=smallfont2)
        self.Test4.grid(row=4, column=5)
        self.Test4.bind("<<ComboboxSelected>>", self.disableTest4)

        test5lbl = tkinter.Label(
            self.frame1, text="Test 5:", bg="PaleTurquoise1", fg="Blue4", font=smallfont1
        )
        test5lbl.grid(row=5, column=4)
        self.Test5 = ttk.Combobox(
            self.frame1, values=["None"] + testList, font=smallfont2)
        self.Test5.grid(row=5, column=5)

        self.curValue()

        self.resetSubsBtn = tkinter.Button(
            self.frame1,
            text="Reset Subjects",
            bg="RoyalBlue1",
            font=smallfont1,
            command=self.resetSubjects,
        )
        self.resetSubsBtn.grid(row=6, column=3)

        self.resetTestsBtn = tkinter.Button(
            self.frame1,
            text="Reset Tests",
            bg="RoyalBlue1",
            font=smallfont1,
            command=self.resetTests,
        )
        self.resetTestsBtn.grid(row=6, column=5)

        self.cancel1 = tkinter.Button(
            self.frame1,
            text="Cancel",
            bg="RoyalBlue1",
            font=font1,
            command=self.cancelBtnFunc,
        )
        self.cancel1.grid(row=9, column=3)

        self.submit = tkinter.Button(
            self.frame1,
            text="Update",
            bg="RoyalBlue1",
            font=font1,
            command=self.checkupdate,
        )
        self.submit.grid(row=9, column=5)

        self.deleteBtn = tkinter.Button(
            self.frame1,
            text="Delete Account",
            bg="RoyalBlue1",
            font=font1,
            command=self.delete,
        )
        self.deleteBtn.grid(row=9, column=4)

        self.lblx = tkinter.Label(window, bg="blue", fg="red")

    def curValue(self):
        record1 = self.record[8:]
        if record1[0] == "None" or record1[0] == None or record1[0] == "":
            self.Sub1.current(0)
            self.Sub1["state"] = "readonly"
            self.Sub2["state"] = "disabled"
            self.Sub3["state"] = "disabled"
            self.Sub4["state"] = "disabled"
            self.Sub5["state"] = "disabled"
        else:
            self.Sub1.current(subjectDict[record1[0]])
            self.Sub1["state"] = "disabled"
            if record1[1] == "None" or record1[1] == None or record1[1] == "":
                self.disableSub1()
                self.Sub2.current(0)
                self.Sub2["state"] = "readonly"
                self.Sub3["state"] = "disabled"
                self.Sub4["state"] = "disabled"
                self.Sub5["state"] = "disabled"
            else:
                self.Sub2.current(subjectDict[record1[1]])
                self.Sub2["state"] = "disabled"
                if record1[2] == "None" or record1[2] == None or record1[2] == "":
                    self.disableSub2()
                    self.Sub3.current(0)
                    self.Sub3["state"] = "readonly"
                    self.Sub4["state"] = "disabled"
                    self.Sub5["state"] = "disabled"
                else:
                    self.Sub3.current(subjectDict[record1[2]])
                    self.Sub3["state"] = "disabled"
                    if record1[3] == "None" or record1[3] == None or record1[3] == "":
                        self.disableSub3()
                        self.Sub4.current(0)
                        self.Sub4["state"] = "readonly"
                        self.Sub5["state"] = "disabled"
                    else:
                        self.Sub4.current(subjectDict[record1[3]])
                        self.Sub4["state"] = "disabled"
                        if record1[4] == "None" or record1[4] == None or record1[4] == "":
                            self.disableSub4()
                            self.Sub5.current(0)
                            self.Sub5["state"] = "readonly"
                        else:
                            self.Sub5.current(subjectDict[record1[4]])
                            self.disableSub5()

        if record1[5] == "None" or record1[5] == None or record1[5] == "":
            self.Test1.current(0)
            self.Test1["state"] = "readonly"
            self.Test2["state"] = "disabled"
            self.Test3["state"] = "disabled"
            self.Test4["state"] = "disabled"
            self.Test5["state"] = "disabled"
        else:
            self.Test1.current(testDict[record1[5]])
            self.Test1["state"] = "disabled"
            if record1[6] == "None" or record1[6] == None or record1[6] == "":
                self.disableTest1()
                self.Test2.current(0)
                self.Test2["state"] = "readonly"
                self.Test3["state"] = "disabled"
                self.Test4["state"] = "disabled"
                self.Test5["state"] = "disabled"
            else:
                self.Test2.current(testDict[record1[6]])
                self.Test2["state"] = "disabled"
                if record1[7] == "None" or record1[7] == None or record1[7] == "":
                    self.disableTest2()
                    self.Test3.current(0)
                    self.Test3["state"] = "readonly"
                    self.Test4["state"] = "disabled"
                    self.Test5["state"] = "disabled"
                else:
                    self.Test3.current(testDict[record1[7]])
                    self.Test3["state"] = "disabled"
                    if record1[8] == "None" or record1[8] == None or record1[8] == "":
                        self.disableTest3()
                        self.Test4.current(0)
                        self.Test4["state"] = "readonly"
                        self.Test5["state"] = "disabled"
                    else:
                        self.Test4.current(testDict[record1[8]])
                        self.Test4["state"] = "disabled"
                        if record1[9] == "None" or record1[9] == None or record1[9] == "":
                            self.disableTest4()
                            self.Test5.current(0)
                            self.Test5["state"] = "readonly"
                        else:
                            self.Test5.current(testDict[record1[9]])
                            self.disableTest5()

    def cancelBtnFunc(self):
        profileWindow(window, self.record)

    def disableSub1(self, *args):
        self.Sub1["state"] = "disabled"
        self.Sub2["state"] = "readonly"
        self.Sub2["values"] = ["None"] + self.changeSubList()
        self.Sub2.current(0)

    def disableSub2(self, *args):
        self.Sub2["state"] = "disabled"
        self.Sub3["state"] = "readonly"
        self.Sub3["values"] = ["None"] + self.changeSubList()
        self.Sub3.current(0)

    def disableSub3(self, *args):
        self.Sub3["state"] = "disabled"
        self.Sub4["state"] = "readonly"
        self.Sub4["values"] = ["None"] + self.changeSubList()
        self.Sub4.current(0)

    def disableSub4(self, *args):
        self.Sub4["state"] = "disabled"
        self.Sub5["state"] = "readonly"
        self.Sub5["values"] = ["None"] + self.changeSubList()
        self.Sub5.current(0)

    def disableSub5(self, *args):
        self.Sub5["state"] = "disabled"

    def disableTest1(self, *args):
        self.Test1["state"] = "disabled"
        self.Test2["state"] = "readonly"
        self.Test2["values"] = ["None"] + self.changeTestList()
        self.Test2.current(0)

    def disableTest2(self, *args):
        self.Test2["state"] = "disabled"
        self.Test3["state"] = "readonly"
        self.Test3["values"] = ["None"] + self.changeTestList()
        self.Test3.current(0)

    def disableTest3(self, *args):
        self.Test3["state"] = "disabled"
        self.Test4["state"] = "readonly"
        self.Test4["values"] = ["None"] + self.changeTestList()
        self.Test4.current(0)

    def disableTest4(self, *args):
        self.Test4["state"] = "disabled"
        self.Test5["state"] = "readonly"
        self.Test5["values"] = ["None"] + self.changeTestList()
        self.Test5.current(0)

    def disableTest5(self, *args):
        self.Test5["state"] = "disabled"

    def changeSubList(self):
        subList = copy.deepcopy(subjectList)
        if self.Sub1.get() in subjectList:
            subList.remove(self.Sub1.get())
        if self.Sub2.get() in subjectList:
            subList.remove(self.Sub2.get())
        if self.Sub3.get() in subjectList:
            subList.remove(self.Sub3.get())
        if self.Sub4.get() in subjectList:
            subList.remove(self.Sub4.get())
        if self.Sub5.get() in subjectList:
            subList.remove(self.Sub5.get())
        return subList

    def changeTestList(self):
        tList = copy.deepcopy(testList)
        if self.Test1.get() in tList:
            tList.remove(self.Test1.get())
        if self.Test2.get() in tList:
            tList.remove(self.Test2.get())
        if self.Test3.get() in tList:
            tList.remove(self.Test3.get())
        if self.Test4.get() in tList:
            tList.remove(self.Test4.get())
        if self.Test5.get() in tList:
            tList.remove(self.Test5.get())
        return tList

    def resetSubjects(self):
        self.Sub1["values"] = ["None"] + subjectList
        self.Sub1["state"] = "readonly"
        self.Sub2["state"] = "disabled"
        self.Sub3["state"] = "disabled"
        self.Sub4["state"] = "disabled"
        self.Sub5["state"] = "disabled"
        self.Sub1.current(0)
        self.Sub2.set("")
        self.Sub3.set("")
        self.Sub4.set("")
        self.Sub5.set("")

    def resetTests(self):
        self.Test1["values"] = ["None"] + testList
        self.Test1["state"] = "readonly"
        self.Test2["state"] = "disabled"
        self.Test3["state"] = "disabled"
        self.Test4["state"] = "disabled"
        self.Test5["state"] = "disabled"
        self.Test1.current(0)
        self.Test2.set("")
        self.Test3.set("")
        self.Test4.set("")
        self.Test5.set("")

    def checkPassword(self):
        old = self.oldPassword.get()
        new = self.newPassword.get()
        password = self.record[1]
        if old == "":
            return True
        elif old == password:
            if new == "":
                self.lblx.configure(text="*Please enter a new password*")
                self.lblx.pack()
                return False
            else:
                self.record[1] = new
                return True
        else:
            self.lblx.configure(text="*Old password does not match*")
            self.lblx.pack()
            return False

    def checkupdate(self):
        if len(self.Highschool.get()) > 50:
            self.lblx.configure(
                text="*High school is too long (50 character limit)*")
            self.lblx.pack()
        elif len(self.Undergraduate.get()) > 50:
            self.lblx.configure(
                text="*Undergraduate is too long (50 character limit)*")
            self.lblx.pack()
        elif len(self.Graduate.get()) > 50:
            self.lblx.configure(
                text="*Graduate is too long (50 character limit)*")
            self.lblx.pack()
        elif self.checkPassword():
            request = False

            hs = self.Highschool.get()
            if hs == self.record[4]:
                pass
            else:
                request = True

            us = self.Undergraduate.get()
            if us == self.record[5]:
                pass
            else:
                request = True

            gs = self.Graduate.get()
            if gs == self.record[6]:
                pass
            else:
                request = True

            S1 = self.Sub1.get()
            if S1 == "None" or S1 == "":
                S1 = ""
            S2 = self.Sub2.get()
            if S2 == "None" or S2 == "":
                S2 = ""
            S3 = self.Sub3.get()
            if S3 == "None" or S3 == "":
                S3 = ""
            S4 = self.Sub4.get()
            if S4 == "None" or S4 == "":
                S4 = ""
            S5 = self.Sub5.get()
            if S5 == "None" or S5 == "":
                S5 = ""

            T1 = self.Test1.get()
            if T1 == "None" or T1 == "":
                T1 = ""
            T2 = self.Test2.get()
            if T2 == "None" or T2 == "":
                T2 = ""
            T3 = self.Test3.get()
            if T3 == "None" or T3 == "":
                T3 = ""
            T4 = self.Test4.get()
            if T4 == "None" or T4 == "":
                T4 = ""
            T5 = self.Test5.get()
            if T5 == "None" or T5 == "":
                T5 = ""

            self.update(
                self.Highschool.get(),
                self.Undergraduate.get(),
                self.Graduate.get(),
                S1,
                S2,
                S3,
                S4,
                S5,
                T1,
                T2,
                T3,
                T4,
                T5,
                request
            )

    def update(
        self,
        Highschool,
        Undergraduate,
        Graduate,
        Sub1,
        Sub2,
        Sub3,
        Sub4,
        Sub5,
        Test1,
        Test2,
        Test3,
        Test4,
        Test5,
        request
    ):

        cursor1 = con.cursor()
        if request == False:
            cursor1.execute(
                "UPDATE AccDetails SET Password='{}', FirstName= '{}', LastName='{}', HighSchool = '{}' ,UndergraduateSchool='{}',GraduateSchool='{}',DOB='{}',Sub1='{}',Sub2='{}',Sub3='{}',Sub4='{}',Sub5='{}',Test1='{}',Test2='{}',Test3='{}',Test4='{}',Test5='{}' WHERE Email = '{}'".format(
                    self.record[1],
                    self.record[2],
                    self.record[3],
                    Highschool,
                    Undergraduate,
                    Graduate,
                    self.record[7],
                    Sub1,
                    Sub2,
                    Sub3,
                    Sub4,
                    Sub5,
                    Test1,
                    Test2,
                    Test3,
                    Test4,
                    Test5,
                    self.record[0],
                )
            )
        else:
            cursor1.execute(
                "UPDATE AccDetails SET Password='{}', FirstName= '{}', LastName='{}', HighSchool = '{}' ,UndergraduateSchool='{}',GraduateSchool='{}',DOB='{}',Sub1='{}',Sub2='{}',Sub3='{}',Sub4='{}',Sub5='{}',Test1='{}',Test2='{}',Test3='{}',Test4='{}',Test5='{}', Qualified = 'no' WHERE Email = '{}'".format(
                    self.record[1],
                    self.record[2],
                    self.record[3],
                    Highschool,
                    Undergraduate,
                    Graduate,
                    self.record[7],
                    Sub1,
                    Sub2,
                    Sub3,
                    Sub4,
                    Sub5,
                    Test1,
                    Test2,
                    Test3,
                    Test4,
                    Test5,
                    self.record[0],
                )
            )

        con.commit()

        cursor1.execute(
            "SELECT * FROM AccDetails WHERE Email='" + str(self.record[0]) + "';")
        records = cursor1.fetchall()
        cursor1.close()
        if len(records) == 1:
            profileWindow(window, list(records[0]))

    def delete(self):
        result = tkinter.messagebox.askquestion(
            'Delete', 'Are you sure you want to delete your account?')
        if result == 'yes':
            cursor = con.cursor()
            sql = "DELETE FROM AccDetails WHERE Email= '{}';".format(
                self.record[0])
            cursor.execute(sql)
            con.commit()
            cursor.close()
            loginWindow(window, "Account has been succesfully deleted!")


class Checkbar(tkinter.Frame):
    def __init__(self, window, picks=[]):
        tkinter.Frame.__init__(self, window)
        self.vars = []
        for pick in picks:
            var = tkinter.StringVar()
            chk = tkinter.Checkbutton(
                self, text=pick, variable=var, offvalue=None, onvalue=pick, font=smallfont2
            )
            chk.deselect()
            chk.pack(side=tkinter.LEFT, anchor=tkinter.W, expand=tkinter.YES)
            self.vars.append(var)

    def state(self):
        return map((lambda var: var.get()), self.vars)


class searchWindow:
    def __init__(self, window, record):
        window.configure(bg="Blue")
        window.geometry("1300x700")
        for widget in window.winfo_children():
            widget.destroy()

        self.record1 = record
        # FRAME 1
        self.frame1 = tkinter.Frame(
            window,
            bg="Yellow",
            borderwidth="1",
            relief=tkinter.GROOVE,
        )
        self.frame2 = tkinter.Frame(
            window,
            bg="Pink",
            borderwidth="1",
            relief=tkinter.GROOVE,
        )
        self.frame1.place(relx=0, relwidth=0.3, relheight=1)

        self.headinglbl = tkinter.Label(
            self.frame1, text="Search tutors by:", font=font1)
        self.headinglbl.grid(row=0, column=0)

        self.sublbl = tkinter.Label(
            self.frame1, text="By subjects:", font=smallfont1, bg="PaleTurquoise1")
        self.sublbl.grid(row=1, column=0)

        i = 0
        row1 = 2
        self.CheckBars = []
        while True:
            length1 = len(subjectList)
            if i >= length1:
                break
            else:
                subCheckBar = Checkbar(self.frame1, subjectList[i:i+3])
                subCheckBar.grid(row=row1, column=0)
                i += 3
                row1 += 1
                self.CheckBars.append(subCheckBar)

        self.testlbl = tkinter.Label(
            self.frame1, text="By tests:", font=smallfont1, bg="PaleTurquoise1")
        self.testlbl.grid(row=row1, column=0)
        row1 += 1
        i = 0
        while True:
            length1 = len(testList)
            if i >= length1:
                break
            else:
                testCheckBar = tkinter.Variable()
                testCheckBar = Checkbar(self.frame1, testList[i:i+3])
                testCheckBar.grid(row=row1, column=0)
                i += 3
                row1 += 1
                self.CheckBars.append(testCheckBar)

        self.schoollbl = tkinter.Label(
            self.frame1, text="By schools:", font=smallfont1, bg="PaleTurquoise1")
        self.schoollbl.grid(row=row1, column=0)
        row1 += 1

        hslbl = tkinter.Label(
            self.frame1,
            text="High School:",
            bg="PaleTurquoise1",
            fg="Blue4",
            font=smallfont1,
        )
        hslbl.grid(row=row1, column=0)
        row1 += 1
        self.Highschool = tkinter.Entry(self.frame1, font=smallfont2)
        self.Highschool.grid(row=row1, column=0)
        row1 += 1

        uglbl = tkinter.Label(
            self.frame1,
            text="Undergraduate School:",
            bg="PaleTurquoise1",
            fg="Blue4",
            font=smallfont1,
        )
        uglbl.grid(row=row1, column=0)
        row1 += 1
        self.Undergraduate = tkinter.Entry(self.frame1, font=smallfont2)
        self.Undergraduate.grid(row=row1, column=0)
        row1 += 1

        glbl = tkinter.Label(
            self.frame1,
            text="Graduate School:",
            bg="PaleTurquoise1",
            fg="Blue4",
            font=smallfont1,
        )
        glbl.grid(row=row1, column=0)
        row1 += 1
        self.Graduate = tkinter.Entry(self.frame1, font=smallfont2)
        self.Graduate.grid(row=row1, column=0)
        row1 += 1

        self.enterBtn = tkinter.Button(
            self.frame1, text="Search", font=font1, command=self.search)
        self.enterBtn.grid(sticky=tkinter.S)

        self.enterBtn = tkinter.Button(
            self.frame1, text="Go back", font=font1, command=self.goback)
        self.enterBtn.grid(sticky=tkinter.S)

        # FRAME 2

        self.frame2.place(relx=0.3, relwidth=0.7, relheight=1)

    def getData(self):
        checkBoxes = list(self.CheckBars)
        searchList1 = []
        for checkBox in checkBoxes:
            list1 = list(checkBox.state())
            for element in list1:
                if element == "0":
                    pass
                else:
                    searchList1.append(element)
        hs = self.Highschool.get()[0:50]
        if hs == "":
            pass
        else:
            searchList1.append(hs)

        ug = self.Undergraduate.get()[0:50]
        if ug == "":
            pass
        else:
            searchList1.append(ug)

        g = self.Graduate.get()[0:50]
        if g == "":
            pass
        else:
            searchList1.append(g)
        return searchList1

    def search(self):
        cursor = con.cursor()
        cursor.execute(
            "SELECT Email, HighSchool, UndergraduateSchool, GraduateSchool, Sub1, Sub2, Sub3, Sub4, Sub5, Test1, Test2, Test3, Test4, Test5 FROM AccDetails WHERE Qualified = 'yes';"
        )
        tosearch = self.getData()
        searchList = []
        records = cursor.fetchall()
        for record in records:
            if record[0] == self.record1[0]:
                pass
            elif record[0] == "admin":
                pass
            else:
                check = all(item in record[1:] for item in tosearch)
                if check is True:
                    cursor.execute(
                        "SELECT * FROM AccDetails WHERE Email = '{}'".format(
                            record[0])
                    )
                    searchList.extend(list(cursor.fetchall()))
        cursor.close()
        self.results(searchList)

    def results(self, resultList):
        widgets = self.frame2.winfo_children()
        for widget in widgets:
            widget.destroy()

        # FOR THE SCROLL BARS
        # 1. Create A Main Frame
        main_frame = tkinter.Frame(self.frame2)
        main_frame.pack(fill=tkinter.BOTH, expand=1)
        # 2. Create A Canvas
        canvas1 = tkinter.Canvas(main_frame)
        canvas1.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
        #canvas1.pack(anchor="nw", fill=tkinter.BOTH, expand = 1)
        # 3. Add a scroll bar to the Canvas
        scrollv = ttk.Scrollbar(
            main_frame, orient=tkinter.VERTICAL, command=canvas1.yview)
        scrollv.pack(side=tkinter.LEFT, fill="y")
        #scrollv.pack(side=tkinter.RIGHT, anchor="ne", fill="y")
        #scrollh = ttk.Scrollbar(main_frame, orient=tkinter.HORIZONTAL, command=canvas1.xview)
        #scrollh.pack(side=tkinter.BOTTOM, fill="x", anchor="sw")
        # 4. Configure to canvas
        #canvas1.configure(xscrollcommand=scrollh.set, yscrollcommand=scrollv.set)
        canvas1.configure(yscrollcommand=scrollv.set)
        canvas1.bind("<Configure>", lambda e: canvas1.configure(
            scrollregion=canvas1.bbox("all")))
        # Cretae ANOTHER Frame INSIDE the Canvas
        second_frame = tkinter.Frame(canvas1)
        # Add the New Frame to a Window in the Canvas
        canvas1.create_window((0, 0), window=second_frame, anchor="nw")

        i = 0
        for record in resultList:
            accFrame = tkinter.Frame(
                second_frame, bg="Blue4", highlightbackground="black", highlightthickness="2")
            profileFrame(accFrame, record, smallfont1, smallfont2)
            accFrame.pack(side=tkinter.TOP, padx=5, pady=20)
            i += 1

    def goback(self):
        profileWindow(window, self.record1)


class profileFrame:
    def __init__(self, window, record, font1=font1, font2=font2):
        self.record = record

        profilelbl = tkinter.Label(
            window, text="PROFILE", font=font1)
        profilelbl.grid(row=0, column=0, columnspan=2, rowspan=2)

        pic = self.profilepic()
        piclbl = tkinter.Label(window, image=pic, font=font1)
        piclbl.image = pic
        piclbl.grid(row=1, column=0, columnspan=2, rowspan=6)

        self.dataFrame = tkinter.Frame(window)
        self.dataFrame.grid(row=1, column=2, rowspan=6, columnspan=4)

        Emaillbl = tkinter.Label(
            self.dataFrame, text="Email:", font=font1)
        Emaillbl.grid(row=0, column=0)

        EmailVallbl = tkinter.Label(
            self.dataFrame, text=record[0], font=font2)
        EmailVallbl.grid(row=0, column=1)

        FirstNameLbl = tkinter.Label(
            self.dataFrame, text="First Name:", font=font1
        )
        FirstNameLbl.grid(row=1, column=0)

        FirstNameValLbl = tkinter.Label(
            self.dataFrame, text=record[2], font=font2
        )
        FirstNameValLbl.grid(row=1, column=1)

        LastNameLbl = tkinter.Label(
            self.dataFrame, text="Last Name:", font=font1
        )
        LastNameLbl.grid(row=2, column=0)

        LastNameValLbl = tkinter.Label(
            self.dataFrame, text=record[3], font=font2
        )
        LastNameValLbl.grid(row=2, column=1)

        DateLbl = tkinter.Label(
            self.dataFrame, text="DOB:", font=font1)
        DateLbl.grid(row=3, column=0)

        rdate = str(record[7])
        # Months from 1-12 but lists start at 0
        month = monthList[int(rdate[5:7])-1]
        date = rdate[0:5] + month + rdate[7:]
        DateValLbl = tkinter.Label(
            self.dataFrame, text=date, font=font2)
        DateValLbl.grid(row=3, column=1)

        HighschoolLbl = tkinter.Label(
            self.dataFrame, text="Highschool:", font=font1)
        HighschoolLbl.grid(row=4, column=0)

        HighschoolValLbl = tkinter.Label(
            self.dataFrame, text=record[4], font=font2)
        HighschoolValLbl.grid(row=4, column=1)

        UndergradLbl = tkinter.Label(
            self.dataFrame, text="Undergraduate:", font=font1)
        UndergradLbl.grid(row=5, column=0)

        UndergradValLbl = tkinter.Label(
            self.dataFrame, text=record[5], font=font2)
        UndergradValLbl.grid(row=5, column=1)

        GradLbl = tkinter.Label(
            self.dataFrame, text="Graduate:", font=font1)
        GradLbl.grid(row=6, column=0)

        GradValLbl = tkinter.Label(
            self.dataFrame, text=record[6], font=font2)
        GradValLbl.grid(row=6, column=1)

        subPrefLbl = tkinter.Label(
            self.dataFrame, text="Subject Preferences", font=font1
        )
        subPrefLbl.grid(row=0, column=4)

        testPrefLbl = tkinter.Label(
            self.dataFrame, text="Test Preferences", font=font1
        )
        testPrefLbl.grid(row=0, column=5)

        sub1Lbl = tkinter.Label(
            self.dataFrame, text=record[8], font=font2)
        sub1Lbl.grid(row=1, column=4)

        sub2Lbl = tkinter.Label(
            self.dataFrame, text=record[9], font=font2)
        sub2Lbl.grid(row=2, column=4)

        sub3Lbl = tkinter.Label(
            self.dataFrame, text=record[10], font=font2)
        sub3Lbl.grid(row=3, column=4)

        sub4Lbl = tkinter.Label(
            self.dataFrame, text=record[11], font=font2)
        sub4Lbl.grid(row=4, column=4)

        sub5Lbl = tkinter.Label(
            self.dataFrame, text=record[12], font=font2)
        sub5Lbl.grid(row=5, column=4)

        test1Lbl = tkinter.Label(
            self.dataFrame, text=record[13], font=font2)
        test1Lbl.grid(row=1, column=5)

        test2Lbl = tkinter.Label(
            self.dataFrame, text=record[14], font=font2)
        test2Lbl.grid(row=2, column=5)

        test3Lbl = tkinter.Label(
            self.dataFrame, text=record[15], font=font2)
        test3Lbl.grid(row=3, column=5)

        test4Lbl = tkinter.Label(
            self.dataFrame, text=record[16], font=font2)
        test4Lbl.grid(row=4, column=5)

        test5Lbl = tkinter.Label(
            self.dataFrame, text=record[17], font=font2)
        test5Lbl.grid(row=5, column=5)

    def profilepic(self):
        pic1 = tkinter.PhotoImage(file="./pig.png")
        pic2 = tkinter.PhotoImage(file="./bear.png")
        pic3 = tkinter.PhotoImage(file="./elephant.png")
        pic4 = tkinter.PhotoImage(file="./horse.png")
        pic5 = tkinter.PhotoImage(file="./dog.png")
        lst = [pic1, pic2, pic3, pic4, pic5]
        pic = random.choice(lst)
        return pic


class adminwindow:
    def __init__(self, window):
        widgets = window.winfo_children()
        for widget in widgets:
            widget.destroy()
        """
        self.frame1 = tkinter.Frame(
            window,
            bg="Yellow",
            borderwidth="1",
            relief=tkinter.GROOVE,
        )
        """

        #self.frame1.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER, fill=tkinter.BOTH, expand=1)
        # FOR THE SCROLL BARS
        # 1. Create A Main Frame
        main_frame = tkinter.Frame(window)
        main_frame.pack(fill=tkinter.BOTH, expand=1)
        # 2. Create A Canvas
        canvas1 = tkinter.Canvas(main_frame)
        canvas1.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
        #canvas1.pack(anchor="nw", fill=tkinter.BOTH, expand = 1)
        # 3. Add a scroll bar to the Canvas
        scrollv = ttk.Scrollbar(
            main_frame, orient=tkinter.VERTICAL, command=canvas1.yview)
        scrollv.pack(side=tkinter.LEFT, fill="y")
        #scrollv.pack(side=tkinter.RIGHT, anchor="ne", fill="y")
        #scrollh = ttk.Scrollbar(main_frame, orient=tkinter.HORIZONTAL, command=canvas1.xview)
        #scrollh.pack(side=tkinter.BOTTOM, fill="x", anchor="sw")
        # 4. Configure to canvas
        #canvas1.configure(xscrollcommand=scrollh.set, yscrollcommand=scrollv.set)
        canvas1.configure(yscrollcommand=scrollv.set)
        canvas1.bind("<Configure>", lambda e: canvas1.configure(
            scrollregion=canvas1.bbox("all")))
        # Cretae ANOTHER Frame INSIDE the Canvas
        second_frame = tkinter.Frame(canvas1)
        # Add the New Frame to a Window in the Canvas
        canvas1.create_window((0, 0), window=second_frame, anchor="nw")

        i = 0
        cursor = con.cursor()
        cursor.execute("SELECT * FROM AccDetails WHERE qualified='no'")
        resultList = cursor.fetchall()
        cursor.close()
        self.tickBtnList = []
        for record in resultList:
            #list1 = []
            """
            accFrame = tkinter.Frame(second_frame, bg="Blue4", highlightbackground="black", highlightthickness="2")
            profileFrame(accFrame, record, smallfont1, smallfont2)
            tickBtn = tkinter.Button(accFrame, text="Yes", font=font1, command = self.tick)
            tickBtn.record1 = record
            tickBtn.grid(row=0, rowspan=7, column=6)
            self.tickBtnList.append(tickBtn)
            crossBtn = tkinter.Button(accFrame, text="Yes", font=font1)
            crossBtn.grid(row=0, rowspan=7, column=7)
            accFrame.pack(side=tkinter.TOP, padx=5, pady=20)
            """
            accFrame(second_frame, record)

            i += 1

        signOut = tkinter.Button(
            main_frame,
            text="Sign out",
            bg="RoyalBlue1",
            command=self.signout,
            font=font1,
        )
        signOut.pack(side=tkinter.RIGHT)

    def signout(self):
        loginWindow(window)


class accFrame:
    def __init__(self, frame1, record):
        self.record1 = record
        self.theFrame = tkinter.Frame(
            frame1, bg="Blue4", highlightbackground="black", highlightthickness="2")
        profileFrame(self.theFrame, record, smallfont1, smallfont2)
        self.tickBtn = tkinter.Button(
            self.theFrame, text="Yes", font=font1, command=self.tick)
        self.tickBtn.grid(row=0, rowspan=7, column=6)
        #self.tickBtnList.append(tickBtn)
        self.crossBtn = tkinter.Button(self.theFrame, text="No", font=font1)
        self.crossBtn.grid(row=0, rowspan=7, column=7)
        self.theFrame.pack(side=tkinter.TOP, padx=5, pady=20)

    def tick(self):
        cursor = con.cursor()
        cursor.execute(
            "UPDATE AccDetails SET Qualified = 'yes' WHERE Email = '{}'".format(self.record1[0]))
        con.commit()
        #cursor.execute("SELECT * FROM AccDetails;")
        #result = cursor.fetchall()
        #print(result)
        cursor.close()
        adminwindow(window)


window = tkinter.Tk()
window.title("Student4Student!")
loginWindow(window)
window.mainloop()
con.close()
