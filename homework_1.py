import tkinter as tk
import sqlite3

teal = "#3d6466"
black = "#080808"

def load_database():
    conn = sqlite3.connect('student_database.db')

    c = conn.cursor()

    c.execute("DROP TABLE students")

    c.execute(""
              "CREATE TABLE IF NOT EXISTS students "
              "(ID integer NOT NULL, first_name text NOT NULL, last_name text NOT NULL, entry_time timestamp)")

    c.execute("INSERT INTO students VALUES (47, 'Aaron', 'Cole', CURRENT_TIMESTAMP)")
    c.execute("INSERT INTO students VALUES (23, 'Joe', 'Moe', CURRENT_TIMESTAMP)")
    c.execute("INSERT INTO students VALUES (76, 'Lacey', 'Fayre', CURRENT_TIMESTAMP)")
    c.execute("INSERT INTO students VALUES (62, 'Luke', 'Torre', CURRENT_TIMESTAMP)")
    c.execute("INSERT INTO students VALUES (19, 'Jack', 'Warren', CURRENT_TIMESTAMP)")
    # c.execute("INSERT INTO students VALUES (11, 'Jessica', 'Hess', CURRENT_TIMESTAMP)")
    # c.execute("INSERT INTO students VALUES (23, 'Joe', 'Moe', CURRENT_TIMESTAMP)")

    # for row in c.execute("SELECT * FROM students"):
    #     print(row)

    conn.commit()

    conn.close()

def fetch_db(frame):
    conn = sqlite3.connect('student_database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    fetchtable = c.fetchall()
    conn.commit()
    id = "ID"
    fname = "First_Name"
    lname = "Last_Name"
    time = "Timestamp"
    headerFormat = "%s %30s %20s %20s" % (id, fname, lname, time)
    tk.Label(frame, text=headerFormat, font=('Arial', 12), bg=black).place(x=10, y=230)
    tk.Label(frame, text="----------------------------------------------------------------", bg=black).place(x=10, y=250)
    startY = 290
    for i in fetchtable:
        data = ("%s %30s %25s %30s" % (i[0], i[1], i[2], i[3]))
        tk.Label(frame, text=data, font=('Arial', 12), bg=black).place(x=10, y=startY)
        startY += 30
    c.close()

def login_status(username, password):
    passwordInput = password.get()
    usernameInput = username.get()
    # passwordInput = "password"
    # usernameInput = "admin"
    if passwordInput == "password" and usernameInput == "admin":
        load_frame2()
    else:
        clearwindow(frame1)
        load_frame3()

def clearwindow(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def load_frame1():
    password = tk.StringVar()
    username = tk.StringVar()
    frame1.grid(row=0, column=0)
    frame1.pack_propagate(False)

    # Frame 1 design

    tk.Label(frame1, text="Welcome to the Sun Labs Database.\n --- ADMIN LOGIN ---", font=("Ariel", 16), bg=black).pack()
    # Username entry
    tk.Label(frame1, text="Username:", bg=black).pack()
    tk.Entry(frame1, width=30, font=('Arial', 12), textvariable=username).pack()
    # Password entry
    tk.Label(frame1, text="Password:", bg=black).pack()
    tk.Entry(frame1, width=30, font=('Arial', 12), textvariable=password, show="*").pack()
    # Log in button
    tk.Button(frame1, text="Log in", command=lambda: login_status(username, password), bg=black).pack()
    # Quit button
    tk.Button(frame1, text="Quit", command=root.destroy, bg=black).pack()

# Frame for successful login

def load_frame2():
    clearwindow(frame4)
    clearwindow(frame1)
    firstname = tk.StringVar()
    lastname = tk.StringVar()
    frame2.pack_propagate(False)
    frame2.grid(row=0, column=0)
    tk.Label(frame2, text="Successful login to database.\n--- Welcome Admin --- \nIf you would like to search for a "
                          "specific user, \nplease search by first and last in the appropriate fields.",
             font=('Ariel', 14), bg=black).pack()
    tk.Label(frame2, text="First Name", font=("Ariel", 12), bg=black).pack()
    tk.Entry(frame2, width=30, font=('Arial', 12), textvariable=firstname).pack()
    tk.Label(frame2, text="Last Name", font=("Ariel", 12), bg=black).pack()
    tk.Entry(frame2, width=30, font=('Arial', 12), textvariable=lastname).pack()
    tk.Button(frame2, text="Search", command=lambda: search_frame(firstname, lastname), bg=black).pack()
    tk.Button(frame2, text="Insert", command=lambda: insert_user(firstname, lastname), bg=black).pack()
    fetch_db(frame2)

def insert_user(firstname, lastname):
    conn = sqlite3.connect('student_database.db')
    c = conn.cursor()
    f_name = firstname.get()
    l_name = lastname.get()
    c.execute("""INSERT INTO students VALUES(10, ?, ?, CURRENT_TIMESTAMP)""", (f_name, l_name))
    clearwindow(frame2)
    load_frame2()

# Frame for failed login

def load_frame3():
    clearwindow(frame1)
    clearwindow(frame3)
    username = tk.StringVar()
    password = tk.StringVar()
    frame3.pack_propagate(False)
    frame3.grid(row=0, column=0)
    tk.Label(frame3, text="Invalid login credentials.\nPlease try again...", font=("Ariel", 16),bg=black).pack()
    tk.Label(frame3, text="Username:", bg=black).pack()
    tk.Entry(frame3, width=30, font=('Arial', 12), textvariable=username).pack()
    tk.Label(frame3, text="Password:", bg=black).pack()
    tk.Entry(frame3, width=30, font=('Arial', 12), show="*", textvariable=password).pack()
    tk.Button(frame3, text="Log in", command=lambda: login_status(username, password), bg=black).pack()
    tk.Button(frame3, text="Quit", command=root.destroy, bg=black).pack()

def frame2load():
    frame2.pack_propagate(False)
    load_frame2()

def reset():
    clearwindow(frame4)
    load_frame2()

def search_frame(f_name, l_name):
    clearwindow(frame2)
    clearwindow(frame3)
    clearwindow(frame1)
    root.update()
    frame4.pack_propagate(False)
    frame4.grid(row=0, column=0)
    firstname = f_name.get()
    lastname = l_name.get()
    # firstname = "Joe"
    # lastname = "Moe"
    conn = sqlite3.connect('student_database.db')
    c = conn.cursor()
    c.execute("""SELECT * FROM students WHERE first_name=? AND last_name=?;""", (firstname, lastname))
    results = c.fetchall()

    if len(results) > 0:


        tk.Label(frame4, text="Results for: %s %s" % (firstname, lastname), font=("Arial", 14), bg=black).place(x=165, y=75)
        tk.Button(frame4, text="Reset", command=lambda: reset(), font=("Arial", 12), bg=black).place(x=200, y=125)

        id = "ID"
        fname = "First_Name"
        lname = "Last_Name"
        time = "Timestamp"
        headerFormat = "%s %30s %20s %20s" % (id, fname, lname, time)
        tk.Label(frame4, text=headerFormat, font=('Arial', 12), bg=black).place(x=10, y=230)
        tk.Label(frame4, text="----------------------------------------------------------------", bg=black).place(x=10, y=250)
        startY = 270
        for i in results:
            data = ("%s %30s %25s %30s" % (i[0], i[1], i[2], i[3]))
            tk.Label(frame4, text=data, font=('Arial', 12), bg=black).place(x=10, y=startY)
            startY += 30
    else:
        tk.Label(frame4, text="Username does not exist in database.", font=('Arial', 14), bg=black).place(x=115, y=75)
        tk.Button(frame4, text="Reset", command=lambda: reset(), font=("Arial", 12), bg=black).place(x=200, y=125)

    conn.commit()
    conn.close()

root = tk.Tk()
root.title("testing")
root.eval("tk::PlaceWindow . center")

frame1 = tk.Frame(root, width=500, height=500, bg=black)
frame2 = tk.Frame(root, width=500, height=500, bg=black)
frame3 = tk.Frame(root, width=500, height=500, bg=black)
frame4 = tk.Frame(root, width=500, height=500, bg=black)
insertframe = tk.Frame(root, width=500, height=500, bg=black)
load_database()

load_frame1()

root.mainloop()
