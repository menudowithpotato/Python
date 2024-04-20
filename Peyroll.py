#Joshua R. Galon
#IT1R7
#Date Compiled: May 31, 2023
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
import sqlite3
from datetime import datetime

MAX_LOGIN_ATTEMPTS = 3
login_attempts = 0

def check_login(username, password):
    global login_attempts
    
    if username == "admin" and password == "admin":
        messagebox.showinfo("Login Result", "Login Successful!")
        return True
    
    conn = sqlite3.connect("juswa.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM passwordmanagement WHERE Username = ? AND Password = ?", (username, password))
    account = cursor.fetchone()
    conn.close()
    
    if account is not None:
        messagebox.showinfo("Login Result", "Login Successful!")
        return True
    
    login_attempts += 1
    if login_attempts >= MAX_LOGIN_ATTEMPTS:
        messagebox.showerror("Login Result", "Invalid username or password! Maximum login attempts reached.")
        window.after(2000, window.quit)  # Exit after 2 seconds
    else:
        messagebox.showerror("Login Result", "Invalid username or password!")
    return False

def login(event=None):
    username = username_entry.get()
    password = password_entry.get()
    
    if not check_login(username, password):
        return
    
    window.withdraw()
    open_main_window()

def login_password():
    clear_entries()
    main_window.destroy()
    window.deiconify()

def clear_entries():
    username_entry.delete(0, END)
    password_entry.delete(0, END)

def open_main_window():
    global main_window
    main_window = Toplevel(window)
    main_window.title("Main Window")
    main_window.geometry("500x400")
    main_window.configure(bg="#FFFFFF")
    
    # Create the menu bar
    menubar = Menu(main_window)
    main_window.config(menu=menubar)
    
    # Create the 'File' menu
    
    System_Task = Menu(menubar, tearoff=0)
    System_Task.add_command(label="Employee's Registration Profile", command=newregister)
    System_Task.add_command(label="Employee's List", command=newlist)
    System_Task.add_separator()
    System_Task.add_command(label="Exit", command=exit_program)

    Payroll_Management = Menu(menubar, tearoff=0)
    Payroll_Management.add_command(label="Employee List  Deductions", command=Payroll)
    Payroll_Management.add_command(label="Payroll Summary List", command=display_summary_list)
    

    System_Maintainance = Menu(menubar, tearoff=0)
    System_Maintainance.add_command(label="Password Management", command=password_management)
    System_Maintainance.add_command(label="Login Password", command=login_password)

    menubar.add_cascade(label="System Task", menu=System_Task)
    menubar.add_cascade(label="Payroll Management", menu=Payroll_Management)
    menubar.add_cascade(label="System Maintenance", menu=System_Maintainance)

def Payroll():

    root = Tk()
    root.title("Employee's List")
    width = 1200
    height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))
    root.resizable(1, 1)
    root.configure(bg="#FFFFFF")
    
    def search_data():
        search_value = search_entry.get()
        if search_value == "":
            messagebox.showwarning("", "Please enter a search query.")
        else:
            conn = sqlite3.connect('juswa.db')
            cursor = conn.cursor()
            cursor.execute("SELECT emp_no firstname, lastname, age, address, contact, rate FROM member WHERE emp_no LIKE ? OR firstname LIKE ?", (f"%{search_value}%", f"%{search_value}%"))
            fetch = cursor.fetchall()

            tree.delete(*tree.get_children())
            for index, data in enumerate(fetch, start=1):
                emp_no = index
                firstname = data[1]
                lastname = data[1]
                age = data[2]
                address = data[3]
                contact = data[4]
                rate = data[5]
                tree.insert('', 'end', values=(emp_no, firstname, lastname, age, address, contact, rate))
            cursor.close()
            conn.close()

    def back_to_all_data():
        search_entry.delete(0, END)
        displayData()
     # Methods
    def Database():
        conn = sqlite3.connect('juswa.db')
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS member (
            mem_id INTEGER PRIMARY KEY AUTOINCREMENT,
            firstname TEXT,
            lastname TEXT,
            age INTEGER,
            address TEXT,
            contact TEXT,
            rate INTEGER)""")
        conn.commit()
        conn.close()

    def displayData():
        conn = sqlite3.connect('juswa.db')
        cursor = conn.cursor()
        cursor.execute("SELECT emp_no, firstname, lastname, age, address, contact, rate FROM member ORDER BY emp_no ASC")
        fetch = cursor.fetchall()
        tree.delete(*tree.get_children())
        for data in fetch:
            emp_no = data[0]
            firstname = data[1]
            lastname = data[2]
            age = data[3]
            address = data[4]
            contact = data[5]
            rate = data[6]
            tree.insert('', 'end', values=(emp_no, firstname, lastname, age, address, contact, rate))
        cursor.close()
        conn.close()

    def on_double_click(event):
        selected_item = tree.focus()
        if selected_item:
            values = tree.item(selected_item)['values']
            emp_no = values[0]
            firstname = values[1]
            lastname = values[2]

            # Fetch the data from the database based on emp_no
            conn = sqlite3.connect('juswa.db')
            cursor = conn.cursor()
            cursor.execute("SELECT emp_no, firstname, lastname, age, address, contact, rate FROM member WHERE emp_no=?", (emp_no,))
            data = cursor.fetchone()
            if data:
                emp_no = data[0]
                firstname = data[1]
                lastname = data[2]
                age = data[3]
                address = data[4]
                contact = data[5]
                rate = data[6]
                result = messagebox.askquestion("Confirm Edit", "Do you want to edit this user?")
                if result == 'yes':
                    def SSS(gross_pay):
                        if gross_pay < 4250:
                            return 180 + 10
                        elif 4250 <= gross_pay < 4750:
                            return 202.50 + 10
                        elif 4750 <= gross_pay < 5250:
                            return 225 + 10
                        elif 5250 <= gross_pay < 5750:
                            return 247.50 + 10
                        elif 5750 <= gross_pay < 6250:
                            return 270 + 10
                        elif 6250 <= gross_pay < 6750:
                            return 292.50 + 10
                        elif 6750 <= gross_pay < 7250:
                            return 315 + 10
                        elif 7250 <= gross_pay < 7750:
                            return 337.50 + 10
                        elif 7750 <= gross_pay < 8250:
                            return 360 + 10
                        elif 8250 <= gross_pay < 8750:
                            return 382.50 + 10
                        elif 8750 <= gross_pay < 9250:
                            return 405 + 10
                        elif 9250 <= gross_pay < 9750:
                            return 427.50 + 10
                        elif 9750 <= gross_pay < 10250:
                            return 450 + 10
                        elif 10250 <= gross_pay < 10750:
                            return 472.50 + 10
                        elif 10750 <= gross_pay < 11250:
                            return 495 + 10
                        elif 11250 <= gross_pay < 11750:
                            return 517.50 + 10
                        elif 11750 <= gross_pay < 12250:
                            return 540 + 10
                        elif 12250 <= gross_pay < 12750:
                            return 562.50 + 10
                        elif 12750 <= gross_pay < 13250:
                            return 585 + 10
                        elif 13250 <= gross_pay < 13750:
                            return 607.50 + 10
                        elif 13750 <= gross_pay < 14250:
                            return 630 + 10
                        elif 14250 <= gross_pay < 14750:
                            return 652.50 + 10
                        elif 14750 <= gross_pay < 15250:
                            return 675 + 30
                        elif 15250 <= gross_pay < 15750:
                            return 697.50 + 30
                        elif 15750 <= gross_pay < 16250:
                            return 720 + 30
                        elif 16250 <= gross_pay < 16750:
                            return 742.50 + 30
                        elif 16750 <= gross_pay < 17250:
                            return 765 + 30
                        elif 17250 <= gross_pay < 17750:
                            return 787.50 + 30
                        elif 17750 <= gross_pay < 18250:
                            return 810 + 30
                        elif 18250 <= gross_pay < 18750:
                            return 832.50 + 30
                        elif 18750 <= gross_pay < 19250:
                            return 855 + 30
                        elif 19250 <= gross_pay < 19750:
                            return 877.50 + 30
                        elif 19750 <= gross_pay < 20250:
                            return 900 + 30
                        elif 20250 <= gross_pay < 20750:
                            return 900 + 30 + 22.50
                        elif 20750 <= gross_pay < 21250:
                            return 900 + 30 + 45
                        elif 21250 <= gross_pay < 21750:
                            return 900 + 30 + 67.50
                        elif 21750 <= gross_pay < 22250:
                            return 900 + 30 + 90
                        elif 22250 <= gross_pay < 22750:
                            return 900 + 30 + 112.50
                        elif 22750 <= gross_pay < 23250:
                            return 900 + 30 + 135
                        elif 23250 <= gross_pay < 23750:
                            return 900 + 30 + 157.50
                        elif 23750 <= gross_pay < 24250:
                            return 900 + 30 + 180
                        elif 24250 <= gross_pay < 24750:
                            return 900 + 30 + 202.50
                        elif 24750 <= gross_pay < 25250:
                            return 900 + 30 + 225
                        elif 25250 <= gross_pay < 25750:
                            return 900 + 30 + 247.50
                        elif 25750 <= gross_pay < 26250:
                            return 900 + 30 + 270
                        elif 26250 <= gross_pay < 26750:
                            return 900 + 30 + 292.50
                        elif 26750 <= gross_pay < 27250:
                            return 900 + 30 + 315
                        elif 27250 <= gross_pay < 27750:
                            return 900 + 30 + 337.50
                        elif 27750 <= gross_pay < 28250:
                            return 900 + 30 + 360
                        elif 28250 <= gross_pay < 28750:
                            return 900 + 30 + 382.50
                        elif 28750 <= gross_pay < 29250:
                            return 900 + 30 + 405
                        elif 29250 <= gross_pay < 29750:
                            return 900 + 30 + 427.50
                        elif gross_pay >= 29750:
                            return 900 + 30 + 450
                        
                    def PAGIBIG(gross_pay):
                        if 1000 <= gross_pay < 1500:
                            return gross_pay * 0.01
                        elif 1500 <= gross_pay < 5000:
                            return gross_pay * 0.02
                        elif gross_pay >= 5000:
                            return gross_pay * 0.03
                        
                    def philhealth(gross_pay):
                        if 10000 <= gross_pay < 90000:
                            return gross_pay * 0.045
                        else:
                            return 0

                    def calculate_deductions(event=None):
                        try:
                            rate = float(rate_entry.get())
                            hours = float(hrs_wrk_entry.get())
                            
                            
                            gross_pay = rate * hours
                            gross_pay_entry.configure(state="normal")
                            gross_pay_entry.delete(0, "end")
                            gross_pay_entry.insert(0, gross_pay)
                            gross_pay_entry.configure(state="readonly")

                            sss_deduction = SSS(gross_pay)
                            sss_entry.configure(state="normal")
                            sss_entry.delete(0, "end")
                            sss_entry.insert(0, sss_deduction)
                            sss_entry.configure(state="readonly")

                            pagibig_deduction = PAGIBIG(gross_pay)
                            pagibig_entry.configure(state="normal")
                            pagibig_entry.delete(0, "end")
                            pagibig_entry.insert(0, pagibig_deduction)
                            pagibig_entry.configure(state="readonly")

                            philhealth_deduction = philhealth(gross_pay)
                            philhealth_entry.configure(state="normal")
                            philhealth_entry.delete(0, "end")
                            philhealth_entry.insert(0, philhealth_deduction)
                            philhealth_entry.configure(state="readonly")
                            
                            cash_advance = float(cash_advance_entry.get())
                            total_deductions = sss_deduction + pagibig_deduction + philhealth_deduction + cash_advance
                            total_deduc_entry.configure(state="normal")
                            total_deduc_entry.delete(0, "end")
                            total_deduc_entry.insert(0, total_deductions)
                            total_deduc_entry.configure(state="readonly")
                            
                            net_pay = gross_pay - total_deductions
                            net_pay_entry.configure(state="normal")
                            net_pay_entry.delete(0, "end")
                            net_pay_entry.insert(0, net_pay)
                            net_pay_entry.configure(state="readonly")
                            # Show a message box with the message "Deductions done"
                            

                        except ValueError:
                            messagebox.showerror("Error", "Please enter valid numeric values for Rate and Hours.")
                    
                    edit_window = Toplevel(root)
                    edit_window.title("Edit User")
                    edit_window.geometry("900x550")
                    edit_window.configure(bg='#FFFFFF')

                    top_label = Label(edit_window, text="Payroll Edit Profile", bg="#f0f0f0", fg="#333333", font=("Helvetica", 16, "bold"))
                    top_label.pack(pady=20)

                    form_frame = Frame(edit_window, bg="#f0f0f0")
                    form_frame.pack(padx=20, pady=20)
                    
                    emp_no_label = Label(form_frame, text="Employee Number", bg="#f0f0f0", fg="#333333", font=("Helvetica", 12, "bold"))
                    emp_no_entry = Entry(form_frame, bg="#ffffff", fg="#333333", font=("Helvetica", 12,))
                    

                    firstname_label = Label(form_frame, text="First Name", bg="#f0f0f0", fg="#333333", font=("Helvetica", 12, "bold"))
                    firstname_entry = Entry(form_frame, bg="#ffffff", fg="#333333", font=("Helvetica", 12,))
                    


                    lastname_label = Label(form_frame, text="Last Name", bg="#f0f0f0", fg="#333333", font=("Helvetica", 12, "bold"))
                    lastname_entry = Entry(form_frame, bg="#ffffff", fg="#333333", font=("Helvetica", 12))

                    age_label = Label(form_frame, text="Age", bg="#f0f0f0", fg="#333333", font=("Helvetica", 12, "bold"))
                    age_combobox = ttk.Combobox(form_frame, values=[str(i) for i in range(1, 101)], state="readonly", font=("Helvetica", 12))

                    address_label = Label(form_frame, text="Address", bg="#f0f0f0", fg="#333333", font=("Helvetica", 12, "bold"))
                    address_entry = Entry(form_frame, bg="#ffffff", fg="#333333", font=("Helvetica", 12))

                    contact_label = Label(form_frame, text="Contact Number", bg="#f0f0f0", fg="#333333", font=("Helvetica", 12, "bold"))
                    contact_entry = Entry(form_frame, bg="#ffffff", fg="#333333", font=("Helvetica", 12))

                    rate_label = Label(form_frame, text="Rate per Hour", bg="#f0f0f0", fg="#333333", font=("Helvetica", 12, "bold"))
                    rate_entry = Entry(form_frame, bg="#ffffff", fg="#333333", font=("Helvetica", 12))

                    # Position the labels and entry fields using grid layout
                    emp_no_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
                    emp_no_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

                    firstname_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
                    firstname_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

                    lastname_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
                    lastname_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

                    age_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
                    age_combobox.grid(row=4, column=1, padx=9, pady=9, sticky="w")

                    address_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")
                    address_entry.grid(row=5, column=1, padx=10, pady=10, sticky="w")

                    contact_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")
                    contact_entry.grid(row=6, column=1, padx=10, pady=10, sticky="w")

                    rate_label.grid(row=7, column=0, padx=10, pady=10, sticky="w")
                    rate_entry.grid(row=7, column=1, padx=10, pady=10, sticky="w")


                    # Second column
                    hrs_wrk_label = Label(form_frame, text="Hours Worked", bg="#f0f0f0", fg="#333333", font=("Helvetica", 12, "bold"))
                    hrs_wrk_entry = Entry(form_frame, bg="#ffffff", fg="#333333", font=("Helvetica", 12))

                    gross_pay_label = Label(form_frame, text="Gross Pay", bg="#f0f0f0", fg="#333333", font=("Helvetica", 12, "bold"))
                    gross_pay_entry = Entry(form_frame, bg="#ffffff", fg="#333333", font=("Helvetica", 12))

                    sss_label = Label(form_frame, text="SSS", bg="#f0f0f0", fg="#333333", font=("Helvetica", 12, "bold"))
                    sss_entry = Entry(form_frame, bg="#ffffff", fg="#333333", font=("Helvetica", 12))

                    philhealth_label = Label(form_frame, text="PhilHealth", bg="#f0f0f0", fg="#333333", font=("Helvetica", 12, "bold"))
                    philhealth_entry = Entry(form_frame, bg="#ffffff", fg="#333333", font=("Helvetica", 12))

                    pagibig_label = Label(form_frame, text="Pag-IBIG", bg="#f0f0f0", fg="#333333", font=("Helvetica", 12, "bold"))
                    pagibig_entry = Entry(form_frame, bg="#ffffff", fg="#333333", font=("Helvetica", 12))

                    total_deduc_label = Label(form_frame, text="Total Deductions", bg="#f0f0f0", fg="#333333", font=("Helvetica", 12, "bold"))
                    total_deduc_entry = Entry(form_frame, bg="#ffffff", fg="#333333", font=("Helvetica", 12))

                    net_pay_label = Label(form_frame, text="Net Pay", bg="#f0f0f0", fg="#333333", font=("Helvetica", 12, "bold"))
                    net_pay_entry = Entry(form_frame, bg="#ffffff", fg="#333333", font=("Helvetica", 12))

                    # Position the labels and entry fields in the second column
                    

                    hrs_wrk_label.grid(row=1, column=2, padx=10, pady=10, sticky="w")
                    hrs_wrk_entry.grid(row=1, column=3, padx=10, pady=10, sticky="w")

                    gross_pay_label.grid(row=2, column=2, padx=10, pady=10, sticky="w")
                    gross_pay_entry.grid(row=2, column=3, padx=10, pady=10, sticky="w")

                    sss_label.grid(row=3, column=2, padx=10, pady=10, sticky="w")
                    sss_entry.grid(row=3, column=3, padx=10, pady=10, sticky="w")

                    philhealth_label.grid(row=4, column=2, padx=10, pady=10, sticky="w")
                    philhealth_entry.grid(row=4, column=3, padx=10, pady=10, sticky="w")

                    pagibig_label.grid(row=5, column=2, padx=10, pady=10, sticky="w")
                    pagibig_entry.grid(row=5, column=3, padx=10, pady=10, sticky="w")

                    total_deduc_label.grid(row=6, column=2, padx=10, pady=10, sticky="w")
                    total_deduc_entry.grid(row=6, column=3, padx=10, pady=10, sticky="w")

                    net_pay_label.grid(row=7, column=2, padx=10, pady=10, sticky="w")
                    net_pay_entry.grid(row=7, column=3, padx=10, pady=10, sticky="w")
                    cash_advance_label = Label(form_frame, text="Cash Advance", bg="#f0f0f0", fg="#333333", font=("Helvetica", 12, "bold"))
                    cash_advance_entry = Entry(form_frame, bg="#ffffff", fg="#333333", font=("Helvetica", 12))
                    cash_advance_label.grid(row=8, column=0, padx=10, pady=10, sticky="w")
                    cash_advance_entry.grid(row=8, column=1, padx=10, pady=10, sticky="w")
                    def save_payroll():
                        # Validate the input fields
                        if not all([firstname_entry.get(), lastname_entry.get(), rate_entry.get(), hrs_wrk_entry.get()]):
                            messagebox.showerror("Error", "Please input all fields before saving the data.")
                            return

                        # Perform the necessary calculations
                        rate = float(rate_entry.get())
                        hrs_wrk = float(hrs_wrk_entry.get())
                        gross_pay = rate * hrs_wrk

                        sss_deduction = SSS(gross_pay)
                        pagibig_deduction = PAGIBIG(gross_pay)
                        philhealth_deduction = philhealth(gross_pay)
                        cash_advance = float(cash_advance_entry.get())
                        total_deductions = sss_deduction + pagibig_deduction + philhealth_deduction + cash_advance
                        net_pay = gross_pay - total_deductions

                        # Display a confirmation dialog
                        result = messagebox.askquestion("Confirm Save", "Do you want to save the payroll?")

                        if result == "yes":
                            # Connect to the database and create the table if it doesn't exist
                            conn = sqlite3.connect('juswa.db')
                            cursor = conn.cursor()
                            cursor.execute("""
                                CREATE TABLE IF NOT EXISTS summary_list (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    date TEXT,
                                    firstname TEXT,
                                    lastname TEXT,
                                    rate FLOAT,
                                    hrs_wrk FLOAT,
                                    gross_pay FLOAT,
                                    sss FLOAT,
                                    philheath FLOAT,
                                    pagibig FLOAT,
                                    total_deduc FLOAT,
                                    net_pay FLOAT,
                                    cash_advance FLOAT
                                )
                            """)

                            # Get the input values
                            date = datetime.now().strftime("%Y-%m-%d")
                            firstname = firstname_entry.get()
                            lastname = lastname_entry.get()

                            conn = sqlite3.connect('juswa.db')
                            cursor = conn.cursor()
                            cursor.execute("""
                                REPLACE INTO summary_list (id, date, firstname, lastname, rate, hrs_wrk, gross_pay, sss, philheath, pagibig, total_deduc, net_pay, cash_advance)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """, (emp_no, date, firstname, lastname, rate, hrs_wrk, gross_pay, sss_deduction, philhealth_deduction, pagibig_deduction, total_deductions, net_pay, cash_advance))
                            conn.commit()
                            conn.close()

                            messagebox.showinfo("Payroll Saved", "The payroll has been saved.")
                            edit_window.destroy()
                            displayData()  # Update the displayed data
                        else:
                            edit_window.destroy()



                           



                        
                    edit_button = Button(edit_window, text="Save Payroll", bg="#4caf50", fg="#ffffff", font=("Helvetica", 12, "bold"),command=save_payroll)
                    edit_button.pack(pady=20)
                    
                    emp_no_entry.insert(0, emp_no)
                    firstname_entry.insert(0, firstname)
                    lastname_entry.insert(0, lastname)
                    age_combobox.set(age)
                    address_entry.insert(0, address)
                    contact_entry.insert(0, contact)
                    rate_entry.insert(0, rate)
                    
                    edit_window.bind('<Return>', calculate_deductions)
                    edit_window.mainloop()
                    
    font_style = ('Arial', 12)

    search_frame = Frame(root, bg="#f9f9f9", bd=2, relief=RIDGE)
    search_frame.pack(pady=10, padx=10)

    search_label = Label(search_frame, text="Search:", bg="#f9f9f9", fg="#333333", font=font_style)
    search_label.grid(row=0, column=0, padx=10, pady=5)

    search_entry = Entry(search_frame, font=font_style, bd=2)
    search_entry.grid(row=0, column=1, padx=10, pady=5)

    search_button = Button(search_frame, text="Search", font=font_style, bd=2, bg="#4caf50", fg="#ffffff", command=search_data)
    search_button.grid(row=0, column=2, padx=10, pady=5)

    back_button = Button(search_frame, text="↵", font=font_style, bd=2, bg="#f44336", fg="#ffffff", command=back_to_all_data)
    back_button.grid(row=0, column=3, padx=10, pady=5)
    
    TableMargin = Frame(root, width=500)
    TableMargin.pack(side=TOP)



    # Tables
    scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
    scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
    tree = ttk.Treeview(
        TableMargin,
        columns=("EmpNo", "Firstname", "Lastname", "Age", "Address", "Contact", "RatePerHour"),
        height=400,
        selectmode="extended",
        yscrollcommand=scrollbary.set,
        xscrollcommand=scrollbarx.set
    )
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('EmpNo', text="Employee Number", anchor=W)
    tree.heading('Firstname', text="Firstname", anchor=W)
    tree.heading('Lastname', text="Lastname", anchor=W)
    tree.heading('Age', text="Age", anchor=W)
    tree.heading('Address', text="Address", anchor=W)
    tree.heading('Contact', text="Contact", anchor=W)
    tree.heading('RatePerHour', text="Rate per Hour", anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=150)
    tree.column('#2', stretch=NO, minwidth=0, width=120)
    tree.column('#3', stretch=NO, minwidth=0, width=120)
    tree.column('#4', stretch=NO, minwidth=0, width=80)
    tree.column('#5', stretch=NO, minwidth=0, width=120)
    tree.column('#6', stretch=NO, minwidth=0, width=120)
    tree.bind("<Double-1>", on_double_click) 
    tree.pack()
    Database()  # Call the Database function to create the member table if needed
    displayData()  # Call displayData to populate the treeview with initial data

    root.mainloop()
    


    font_style = ('Arial', 12)

    search_frame = Frame(root, bg="#f9f9f9", bd=2, relief=RIDGE)
    search_frame.pack(pady=10, padx=10)

    search_label = Label(search_frame, text="Search:", bg="#f9f9f9", fg="#333333", font=font_style)
    search_label.grid(row=0, column=0, padx=10, pady=5)

    search_entry = Entry(search_frame, font=font_style, bd=2)
    search_entry.grid(row=0, column=1, padx=10, pady=5)

    search_button = Button(search_frame, text="Search", font=font_style, bd=2, bg="#4caf50", fg="#ffffff", command=search_data)
    search_button.grid(row=0, column=2, padx=10, pady=5)

    back_button = Button(search_frame, text="↵", font=font_style, bd=2, bg="#f44336", fg="#ffffff", command=back_to_all_data)
    back_button.grid(row=0, column=3, padx=10, pady=5)
    
    TableMargin = Frame(root, width=500)
    TableMargin.pack(side=TOP)



    # Tables
    scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
    scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
    tree = ttk.Treeview(
        TableMargin,
        columns=("EmpNo", "Firstname", "Lastname", "Age", "Address", "Contact", "RatePerHour"),
        height=400,
        selectmode="extended",
        yscrollcommand=scrollbary.set,
        xscrollcommand=scrollbarx.set
    )
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('EmpNo', text="Employee Number", anchor=W)
    tree.heading('Firstname', text="Firstname", anchor=W)
    tree.heading('Lastname', text="Lastname", anchor=W)
    tree.heading('Age', text="Age", anchor=W)
    tree.heading('Address', text="Address", anchor=W)
    tree.heading('Contact', text="Contact", anchor=W)
    tree.heading('RatePerHour', text="Rate per Hour", anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=150)
    tree.column('#2', stretch=NO, minwidth=0, width=120)
    tree.column('#3', stretch=NO, minwidth=0, width=120)
    tree.column('#4', stretch=NO, minwidth=0, width=80)
    tree.column('#5', stretch=NO, minwidth=0, width=120)
    tree.column('#6', stretch=NO, minwidth=0, width=120)
    tree.bind("<Double-1>", on_double_click) 
    tree.pack()
    Database()  # Call the Database function to create the member table if needed
    displayData()  # Call displayData to populate the treeview with initial data

    root.mainloop()
    font_style = ('Arial', 12)

    search_frame = Frame(root, bg="#f9f9f9", bd=2, relief=RIDGE)
    search_frame.pack(pady=10, padx=10)

    search_label = Label(search_frame, text="Search:", bg="#f9f9f9", fg="#333333", font=font_style)
    search_label.grid(row=0, column=0, padx=10, pady=5)

    search_entry = Entry(search_frame, font=font_style, bd=2)
    search_entry.grid(row=0, column=1, padx=10, pady=5)

    search_button = Button(search_frame, text="Search", font=font_style, bd=2, bg="#4caf50", fg="#ffffff", command=search_data)
    search_button.grid(row=0, column=2, padx=10, pady=5)

    back_button = Button(search_frame, text="↵", font=font_style, bd=2, bg="#f44336", fg="#ffffff", command=back_to_all_data)
    back_button.grid(row=0, column=3, padx=10, pady=5)
    
    TableMargin = Frame(root, width=500)
    TableMargin.pack(side=TOP)



    # Tables
    scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
    scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
    tree = ttk.Treeview(
        TableMargin,
        columns=("EmpNo", "Firstname", "Lastname", "Age", "Address", "Contact", "RatePerHour"),
        height=400,
        selectmode="extended",
        yscrollcommand=scrollbary.set,
        xscrollcommand=scrollbarx.set
    )
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('EmpNo', text="Employee Number", anchor=W)
    tree.heading('Firstname', text="Firstname", anchor=W)
    tree.heading('Lastname', text="Lastname", anchor=W)
    tree.heading('Age', text="Age", anchor=W)
    tree.heading('Address', text="Address", anchor=W)
    tree.heading('Contact', text="Contact", anchor=W)
    tree.heading('RatePerHour', text="Rate per Hour", anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=150)
    tree.column('#2', stretch=NO, minwidth=0, width=120)
    tree.column('#3', stretch=NO, minwidth=0, width=120)
    tree.column('#4', stretch=NO, minwidth=0, width=80)
    tree.column('#5', stretch=NO, minwidth=0, width=120)
    tree.column('#6', stretch=NO, minwidth=0, width=120)
    tree.bind("<Double-1>", on_double_click) 
    tree.pack()
     

    Database()  # Call the Database function to create the member table if needed
    displayData()  # Call displayData to populate the treeview with initial data

    
   
    font_style = ('Arial', 12)

    search_frame = Frame(root, bg="#f9f9f9", bd=2, relief=RIDGE)
    search_frame.pack(pady=10, padx=10)

    search_label = Label(search_frame, text="Search:", bg="#f9f9f9", fg="#333333", font=font_style)
    search_label.grid(row=0, column=0, padx=10, pady=5)

    search_entry = Entry(search_frame, font=font_style, bd=2)
    search_entry.grid(row=0, column=1, padx=10, pady=5)

    search_button = Button(search_frame, text="Search", font=font_style, bd=2, bg="#4caf50", fg="#ffffff", command=search_data)
    search_button.grid(row=0, column=2, padx=10, pady=5)

    back_button = Button(search_frame, text="↵", font=font_style, bd=2, bg="#f44336", fg="#ffffff", command=back_to_all_data)
    back_button.grid(row=0, column=3, padx=10, pady=5)
    
    TableMargin = Frame(root, width=500)
    TableMargin.pack(side=TOP)



    # Tables
    scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
    scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
    tree = ttk.Treeview(
        TableMargin,
        columns=("EmpNo", "Firstname", "Lastname", "Age", "Address", "Contact", "RatePerHour"),
        height=400,
        selectmode="extended",
        yscrollcommand=scrollbary.set,
        xscrollcommand=scrollbarx.set
    )
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('EmpNo', text="Employee Number", anchor=W)
    tree.heading('Firstname', text="Firstname", anchor=W)
    tree.heading('Lastname', text="Lastname", anchor=W)
    tree.heading('Age', text="Age", anchor=W)
    tree.heading('Address', text="Address", anchor=W)
    tree.heading('Contact', text="Contact", anchor=W)
    tree.heading('RatePerHour', text="Rate per Hour", anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=150)
    tree.column('#2', stretch=NO, minwidth=0, width=120)
    tree.column('#3', stretch=NO, minwidth=0, width=120)
    tree.column('#4', stretch=NO, minwidth=0, width=80)
    tree.column('#5', stretch=NO, minwidth=0, width=120)
    tree.column('#6', stretch=NO, minwidth=0, width=120)
    tree.bind("<Double-1>", on_double_click) 
    tree.pack()
     

    Database()  # Call the Database function to create the member table if needed
    displayData()  # Call displayData to populate the treeview with initial data

    
    root.mainloop()
    font_style = ('Arial', 12)

    search_frame = Frame(root, bg="#f9f9f9", bd=2, relief=RIDGE)
    search_frame.pack(pady=10, padx=10)

    search_label = Label(search_frame, text="Search:", bg="#f9f9f9", fg="#333333", font=font_style)
    search_label.grid(row=0, column=0, padx=10, pady=5)

    search_entry = Entry(search_frame, font=font_style, bd=2)
    search_entry.grid(row=0, column=1, padx=10, pady=5)

    search_button = Button(search_frame, text="Search", font=font_style, bd=2, bg="#4caf50", fg="#ffffff", command=search_data)
    search_button.grid(row=0, column=2, padx=10, pady=5)

    back_button = Button(search_frame, text="↵", font=font_style, bd=2, bg="#f44336", fg="#ffffff", command=back_to_all_data)
    back_button.grid(row=0, column=3, padx=10, pady=5)
    
    TableMargin = Frame(root, width=500)
    TableMargin.pack(side=TOP)



    # Tables
    scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
    scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
    tree = ttk.Treeview(
        TableMargin,
        columns=("EmpNo", "Firstname", "Lastname", "Age", "Address", "Contact", "RatePerHour"),
        height=400,
        selectmode="extended",
        yscrollcommand=scrollbary.set,
        xscrollcommand=scrollbarx.set
    )
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('EmpNo', text="Employee Number", anchor=W)
    tree.heading('Firstname', text="Firstname", anchor=W)
    tree.heading('Lastname', text="Lastname", anchor=W)
    tree.heading('Age', text="Age", anchor=W)
    tree.heading('Address', text="Address", anchor=W)
    tree.heading('Contact', text="Contact", anchor=W)
    tree.heading('RatePerHour', text="Rate per Hour", anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=150)
    tree.column('#2', stretch=NO, minwidth=0, width=120)
    tree.column('#3', stretch=NO, minwidth=0, width=120)
    tree.column('#4', stretch=NO, minwidth=0, width=80)
    tree.column('#5', stretch=NO, minwidth=0, width=120)
    tree.column('#6', stretch=NO, minwidth=0, width=120)
    tree.bind("<Double-1>", on_double_click) 
    tree.pack()
     

    Database()  # Call the Database function to create the member table if needed
    displayData()  # Call displayData to populate the treeview with initial data
    


def display_summary_list():
    def delete_data():
        selected_items = tree.selection()
        if not selected_items:
            messagebox.showwarning("", "Please select an entry to delete.")
        else:
            confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected entry?")
            if confirm:
                conn = sqlite3.connect('juswa.db')
                cursor = conn.cursor()
                for item in selected_items:
                    id = tree.item(item)['values'][0]
                    cursor.execute("DELETE FROM summary_list WHERE id=?", (id,))
                    if tree.exists(item):  # Check if the item exists in the treeview
                        tree.delete(item)  # Remove the item from the treeview
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo("", "Data deleted successfully.")
    def displayData(tree):
        conn = sqlite3.connect('juswa.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM summary_list")
        fetch = cursor.fetchall()

        tree.delete(*tree.get_children())
        for data in fetch:
            id = data[0]
            date = data[1]
            firstname = data[2]
            lastname = data[3]
            rate = data[4]
            hrs_wrk = data[5]
            gross_pay = data[6]
            sss = data[7]
            philheath = data[8]
            pagibig = data[9]
            total_deduc = data[10]
            net_pay = data[11]
            cash_advance = data[12]

            tree.insert('', 'end', values=(id, date, firstname, lastname, rate, hrs_wrk, gross_pay, sss, philheath, pagibig, total_deduc, net_pay, cash_advance))

        cursor.close()
        conn.close()
    def search_data():
        search_value = search_entry.get()
        if search_value == "":
            messagebox.showwarning("", "Please enter a search query.")
        else:
            conn = sqlite3.connect('juswa.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM summary_list WHERE firstname LIKE ? OR lastname LIKE ?", (f"%{search_value}%", f"%{search_value}%"))
            fetch = cursor.fetchall()

            tree.delete(*tree.get_children())
            for data in fetch:
                id = data[0]
                date = data[1]
                firstname = data[2]
                lastname = data[3]
                rate = data[4]
                hrs_wrk = data[5]
                gross_pay = data[6]
                sss = data[7]
                philheath = data[8]
                pagibig = data[9]
                total_deduc = data[10]
                net_pay = data[11]

                tree.insert('', 'end', values=(id, date, firstname, lastname, rate, hrs_wrk, gross_pay, sss, philheath, pagibig, total_deduc, net_pay))

            cursor.close()
            conn.close()
    
                


    def back_to_all_data():
        search_entry.delete(0, END)
        conn = sqlite3.connect('juswa.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM summary_list")
        fetch = cursor.fetchall()

        tree.delete(*tree.get_children())
        for data in fetch:
            id = data[0]
            date = data[1]
            firstname = data[2]
            lastname = data[3]
            rate = data[4]
            hrs_wrk = data[5]
            gross_pay = data[6]
            sss = data[7]
            philheath = data[8]
            pagibig = data[9]
            total_deduc = data[10]
            net_pay = data[11]

            tree.insert('', 'end', values=(id, date, firstname, lastname, rate, hrs_wrk, gross_pay, sss, philheath, pagibig, total_deduc, net_pay))

        cursor.close()
        conn.close()



                
    

    # Create the root window
    root = Tk()
    root.title("Payroll Summary List")
    width = 1500
    height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))
    root.resizable(1, 1)
    root.configure(bg="#000000")

    font_style = ('Arial', 12)

    search_frame = Frame(root, bg="#f9f9f9", bd=2, relief=RIDGE)
    search_frame.pack(pady=10, padx=10)

    search_label = Label(search_frame, text="Search:", bg="#f9f9f9", fg="#333333", font=font_style)
    search_label.grid(row=0, column=0, padx=10, pady=5)

    search_entry = Entry(search_frame, font=font_style, bd=2)
    search_entry.grid(row=0, column=1, padx=10, pady=5)

    search_button = Button(search_frame, text="Search", font=font_style, bd=2, bg="#4caf50", fg="#ffffff",command=search_data)
    search_button.grid(row=0, column=2, padx=10, pady=5)

    back_button = Button(search_frame, text="↵", font=font_style, bd=2, bg="#f44336", fg="#ffffff", command=back_to_all_data)
    back_button.grid(row=0, column=3, padx=10, pady=5)
    
    # Create the delete button
    delete_button = Button(search_frame, text="Delete", font=font_style, bd=2, bg="#f44336", fg="#ffffff", command=delete_data)
    delete_button.grid(row=0, column=4, padx=10, pady=5)

   
    

    # Create the table frame
    table_frame = Frame(root)
    table_frame.pack(side=TOP)

    # Create the scrollbars
    scrollbarx = Scrollbar(table_frame, orient=HORIZONTAL)
    scrollbary = Scrollbar(table_frame, orient=VERTICAL)
    tree = ttk.Treeview(
    table_frame,
    columns=("Emp_No", "Date", "First Name", "Last Name", "Rate", "Hours Worked", "Gross Pay",
             "SSS Deduction", "PhilHealth Deduction", "PAGIBIG Deduction",
             "Total Deductions", "Net Pay", "Cash Advance"),
    height=400,
    selectmode="extended",
    yscrollcommand=scrollbary.set,
    xscrollcommand=scrollbarx.set
    )

    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)

    tree.heading('Emp_No', text="Emp No", anchor=W)
    tree.heading('Date', text="Date Covered", anchor=W)
    tree.heading('First Name', text="First Name", anchor=W)
    tree.heading('Last Name', text="Last Name", anchor=W)
    tree.heading('Rate', text="Rate Per Hr", anchor=W)
    tree.heading('Hours Worked', text="Hrs. Worked", anchor=W)
    tree.heading('Gross Pay', text="Gross Pay", anchor=W)
    tree.heading('SSS Deduction', text="SSS", anchor=W)
    tree.heading('PhilHealth Deduction', text="PhilHealth", anchor=W)
    tree.heading('PAGIBIG Deduction', text="PagIBIG", anchor=W)
    tree.heading('Total Deductions', text="Total Deductions", anchor=W)
    tree.heading('Net Pay', text="Net Pay", anchor=W)
    tree.heading('Cash Advance', text="Cash Advance", anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=120)
    tree.column('#2', stretch=NO, minwidth=0, width=120)
    tree.column('#3', stretch=NO, minwidth=0, width=100)
    tree.column('#4', stretch=NO, minwidth=0, width=120)
    tree.column('#5', stretch=NO, minwidth=0, width=120)
    tree.column('#6', stretch=NO, minwidth=0, width=120)
    tree.column('#7', stretch=NO, minwidth=0, width=90)
    tree.column('#8', stretch=NO, minwidth=0, width=120)
    tree.column('#9', stretch=NO, minwidth=0, width=120)
    tree.column('#10', stretch=NO, minwidth=0, width=120)
    tree.column('#11', stretch=NO, minwidth=0, width=120)
    tree.column('#12', stretch=NO, minwidth=0, width=120)

    tree.pack()
    displayData(tree)
    


   



def password_management():
    def Database():
        conn = sqlite3.connect('juswa.db')
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwordmanagement (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Username TEXT,
            Password TEXT,
            Firstname TEXT,
            Lastname TEXT
        )""")
        conn.commit()
        conn.close()
        
    def displayData():
        Database()
        conn = sqlite3.connect('juswa.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, Username, Password, Firstname, Lastname FROM passwordmanagement ORDER BY Username")
        fetch = cursor.fetchall()
        tree.delete(*tree.get_children())
        for data in fetch:
            id = data[0]
            username = data[1]
            password = data[2]
            firstname = data[3]
            lastname = data[4]

            tree.insert('', 'end', values=(id, username, '*' * len(password), firstname, lastname))
        cursor.close()
        conn.close()
    
    def addData():
        add_window = Toplevel(main_window)
        add_window.title("New Password Management")
        add_window.geometry("500x300")

        username_label = Label(add_window, text="Username:")
        username_label.pack()
        username_entry = Entry(add_window)
        username_entry.pack()

        password_label = Label(add_window, text="Password:")
        password_label.pack()
        password_entry = Entry(add_window, show="")  # Show password as asterisks
        password_entry.pack()

        firstname_label = Label(add_window, text="First Name:")
        firstname_label.pack()
        firstname_entry = Entry(add_window)
        firstname_entry.pack()

        lastname_label = Label(add_window, text="Last Name:")
        lastname_label.pack()
        lastname_entry = Entry(add_window)
        lastname_entry.pack()

        def registerdone():
            username = username_entry.get()
            password = password_entry.get()
            firstname = firstname_entry.get()
            lastname = lastname_entry.get()

            if not username or not password or not firstname or not lastname:
                messagebox.showerror("Error", "Please fill in all fields.")
                return

            conn = sqlite3.connect('juswa.db')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO passwordmanagement (Username, Password, Firstname, Lastname) VALUES (?, ?, ?, ?)",
                (username, password, firstname, lastname))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", "Registration successful!")
            displayData()

        register_button = Button(add_window, text="Register", bg="#4caf50", command=registerdone)
        register_button.pack()

        # Store the Entry widget values as global variables
        global username, password, firstname, lastname
        username = username_entry
        password = password_entry
        firstname = firstname_entry
        lastname = lastname_entry
    
    def deleteData():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("", "Please select an entry to delete.")
        else:
            confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected entry?")
            if confirm:
                conn = sqlite3.connect('juswa.db')
                cursor = conn.cursor()
                for item in selected_item:
                    values = tree.item(item)["values"]
                    id = values[0]
                    cursor.execute("DELETE FROM passwordmanagement WHERE id=?", (id,))
                conn.commit()
                cursor.close()
                conn.close()
                displayData()

    def edit_data():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("", "Please select an entry to edit.")
        else:
            edit_window = Toplevel(main_window)
            edit_window.title("Edit Password")
            edit_window.geometry("400x300")

            def update_entry():
                new_username = username_entry.get()
                new_password = password_entry.get()
                new_firstname = firstname_entry.get()
                new_lastname = lastname_entry.get()
                if not new_username or not new_password or not new_firstname or not new_lastname:
                    messagebox.showwarning("", "Please fill out all fields.")
                else:
                    conn = sqlite3.connect('juswa.db')
                    cursor = conn.cursor()
                    values = tree.item(selected_item[0])["values"]
                    id = values[0]
                    cursor.execute(
                        "UPDATE passwordmanagement SET Username=?, Password=?, Firstname=?, Lastname=? WHERE id=?",
                        (new_username, new_password, new_firstname, new_lastname, id))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    displayData()
                    edit_window.destroy()
                    messagebox.showinfo("Success", "Update profile successfully!")

            username_label = Label(edit_window, text="Username:")
            username_label.pack()
            username_entry = Entry(edit_window)
            username_entry.pack()

            password_label = Label(edit_window, text="Password:")
            password_label.pack()
            password_entry = Entry(edit_window, show="")  # Show password as asterisks
            password_entry.pack()

            firstname_label = Label(edit_window, text="First Name:")
            firstname_label.pack()
            firstname_entry = Entry(edit_window)
            firstname_entry.pack()

            lastname_label = Label(edit_window, text="Last Name:")
            lastname_label.pack()
            lastname_entry = Entry(edit_window)
            lastname_entry.pack()

            # Populate fields with existing values
            values = tree.item(selected_item[0])["values"]
            
            old_username = values[1]
            old_password = values[2]
            old_firstname = values[3]
            old_lastname = values[4]
            
            username_entry.insert(0, old_username)
            password_entry.insert(0, old_password)
            firstname_entry.insert(0, old_firstname)
            lastname_entry.insert(0, old_lastname)
            update_button = Button(edit_window, text="Update", bg="#4caf50", command=update_entry)
            update_button.pack()
        

    


    def search_data():
        search_value = search_entry.get()
        if search_value == "":
            messagebox.showwarning("", "Please enter a search query.")
        else:
            conn = sqlite3.connect('juswa.db')
            cursor = conn.cursor()
            cursor.execute("SELECT id, Username, Password, Firstname, Lastname FROM passwordmanagement WHERE Username LIKE ? OR Firstname LIKE ? OR Lastname LIKE ? ORDER BY Username", (f"%{search_value}%", f"%{search_value}%", f"%{search_value}%"))
            fetch = cursor.fetchall()
            tree.delete(*tree.get_children())
            for data in fetch:
                id = data[0]
                username = data[1]
                password = data[2]
                firstname = data[3]
                lastname = data[4]
                tree.insert('', 'end', values=(id, username, '*' * len(password), firstname, lastname))
               
            cursor.close()
            conn.close()
    
    def back_to_all_data():
        search_entry.delete(0, END)
        displayData()
    
    main_window = Tk()
    main_window.title("Password Management")
    main_window.geometry("800x500")
    main_window.configure(bg="black")

   

    font_style = ('Arial', 12)

    search_frame = Frame(main_window, bg="#f9f9f9", bd=2, relief=RIDGE)
    search_frame.pack(pady=10, padx=10)

    search_label = Label(search_frame, text="Search:", bg="#f9f9f9", fg="#333333", font=font_style)
    search_label.grid(row=0, column=0, padx=10, pady=5)

    search_entry = Entry(search_frame, font=font_style, bd=2)
    search_entry.grid(row=0, column=1, padx=10, pady=5)

    search_button = Button(search_frame, text="Search", font=font_style, bd=2, bg="#4caf50", fg="#ffffff", command=search_data)
    search_button.grid(row=0, column=2, padx=10, pady=5)

    back_button = Button(search_frame, text="↵", font=font_style, bd=2, bg="#f44336", fg="#ffffff", command=back_to_all_data)
    back_button.grid(row=0, column=3, padx=10, pady=5)

    tree_frame = Frame(main_window)
    tree_frame.pack(pady=20)

    tree = ttk.Treeview(tree_frame)
    tree["columns"] = ("Employee No", "Username", "Password", "First Name", "Last Name")
    tree.column("#0", width=0, stretch=NO)
    tree.column("Employee No", width=150, anchor=CENTER)
    tree.column("Username", width=150, anchor=CENTER)
    tree.column("Password", width=150, anchor=CENTER)
    tree.column("First Name", width=150, anchor=CENTER)
    tree.column("Last Name", width=150, anchor=CENTER)
    tree.heading("Employee No", text="Employee No")
    tree.heading("Username", text="Username")
    tree.heading("Password", text="Password")
    tree.heading("First Name", text="First Name")
    tree.heading("Last Name", text="Last Name")
    tree.pack()

    button_frame = Frame(main_window)
    button_frame.pack(pady=10)
    button_frame.configure(bg="black")


    add_button = Button(button_frame, text="Add", bg="#4caf50", command=addData)
    add_button.grid(row=0, column=0, padx=10)

    delete_button = Button(button_frame, text="Delete", bg="#f44336", command=deleteData)
    delete_button.grid(row=0, column=1, padx=10)

    edit_button = Button(button_frame, text="Edit", bg="#4caf50", command=edit_data)
    edit_button.grid(row=0, column=2, padx=10)

    displayData()




def exit_program():
    window.quit()



def register():
    # Your code for creating the window and entry fields goes here
    
    window.withdraw()
    firstname = firstname_entry.get()
    lastname = lastname_entry.get()
    age = age_combobox.get()
    address = address_entry.get()
    contact = contact_entry.get()
    rate = rate_entry.get()
    
    # Perform validation checks (add your own validation rules)
    if not firstname or not lastname or not age or not address or not contact or not rate:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    # Check if contact is a valid number
    try:
        contact = int(contact)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid contact number.")
        return

    # Check if rate is a valid number
    try:
        rate = float(rate)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid rate per hour.")
        return
        # Create the "member" table if it doesn't exist
    conn = sqlite3.connect("juswa.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS member (emp_no INTEGER PRIMARY KEY AUTOINCREMENT, firstname TEXT, lastname TEXT, "
        "age INTEGER, address TEXT, contact TEXT, rate INTEGER)"
    )
    conn.commit()

    # Save the data to the database
    cursor.execute(
        "INSERT INTO member (firstname, lastname, age, address, contact, rate) VALUES (?, ?, ?, ?, ?, ?)",
        (firstname, lastname, age, address, contact, rate))
    conn.commit()
    
    # Retrieve the auto-incremented emp_no value
    emp_no = cursor.lastrowid

    cursor.close()
    conn.close()
    messagebox.showinfo("Success", "Registration successful!")
    
    # Optional: Clear the form fields after successful registration
    firstname_entry.delete(0, END)
    lastname_entry.delete(0, END)
    age_combobox.set('')
    address_entry.delete(0, END)
    contact_entry.delete(0, END)
    rate_entry.delete(0, END)


    
def newregister():
    window.withdraw()
    global firstname_entry, lastname_entry, age_combobox, address_entry, contact_entry, rate_entry

    new_window = Toplevel()
    new_window.title("Registration Form")
    new_window.geometry("400x550")
    new_window.configure(bg='#FFFFFF')

    top_label = Label(new_window, text="Payroll Registration Profile", bg="#f0f0f0", fg="#333333", font=("Helvetica", 16, "bold"))
    top_label.pack(pady=20)

    # Create a frame for the form fields
    form_frame = Frame(new_window, bg="#f0f0f0")
    form_frame.pack(padx=20, pady=20)

    firstname_label = Label(form_frame, text="First Name", bg="#f0f0f0", fg="#333333", font=("Helvetica", 12, "bold"))
    firstname_entry = Entry(form_frame, bg="#ffffff", fg="#333333", font=("Helvetica", 12))

    lastname_label = Label(form_frame, text="Last Name", bg="#f0f0f0", fg="#333333", font=("Helvetica", 12, "bold"))
    lastname_entry = Entry(form_frame, bg="#ffffff", fg="#333333", font=("Helvetica", 12))

    age_label = Label(form_frame, text="Age", bg="#f0f0f0", fg="#333333", font=("Helvetica", 12, "bold"))
    age_combobox = ttk.Combobox(form_frame, values=[str(i) for i in range(1, 101)], state="readonly", font=("Helvetica", 12))

    address_label = Label(form_frame, text="Address", bg="#f0f0f0", fg="#333333", font=("Helvetica", 12, "bold"))
    address_entry = Entry(form_frame, bg="#ffffff", fg="#333333", font=("Helvetica", 12))

    contact_label = Label(form_frame, text="Contact Number", bg="#f0f0f0", fg="#333333", font=("Helvetica", 12, "bold"))
    contact_entry = Entry(form_frame, bg="#ffffff", fg="#333333", font=("Helvetica", 12))

    rate_label = Label(form_frame, text="Rate per Hour", bg="#f0f0f0", fg="#333333", font=("Helvetica", 12, "bold"))
    rate_entry = Entry(form_frame, bg="#ffffff", fg="#333333", font=("Helvetica", 12))

    register_button = Button(new_window, text="Register", bg="#4CAF50", fg="#ffffff", font=("Helvetica", 14, "bold"), relief="flat", command=register)

    # Position the labels and entry fields using grid layout
    firstname_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    firstname_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    lastname_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    lastname_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    age_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    age_combobox.grid(row=2, column=1, padx=9, pady=9, sticky="w")

    address_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
    address_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

    contact_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
    contact_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")

    rate_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")
    rate_entry.grid(row=5, column=1, padx=10, pady=10, sticky="w")

    register_button.pack(pady=20)


def NewRegister(event=None):
    window.withdraw()
    global firstname_entry, lastname_entry, age_combobox, address_entry, contact_entry, rate_entry

    new_window = Toplevel()
    new_window.title("Registration Form")
    new_window.geometry("400x550")
    new_window.configure(bg='#FFFFFF')

    top_label = Label(new_window, text="Payroll Registration Profile", bg="#f0f0f0", fg="#333333", font=("Helvetica", 16, "bold"))
    top_label.pack(pady=20)

    # Create a frame for the form fields
    form_frame = Frame(new_window, bg="#f0f0f0")
    form_frame.pack(padx=20, pady=20)

    firstname_label = Label(form_frame, text="First Name", bg="#f0f0f0", fg="#333333", font=("Helvetica", 12, "bold"))
    firstname_entry = Entry(form_frame, bg="#ffffff", fg="#333333", font=("Helvetica", 12))

    lastname_label = Label(form_frame, text="Last Name", bg="#f0f0f0", fg="#333333", font=("Helvetica", 12, "bold"))
    lastname_entry = Entry(form_frame, bg="#ffffff", fg="#333333", font=("Helvetica", 12))

    age_label = Label(form_frame, text="Age", bg="#f0f0f0", fg="#333333", font=("Helvetica", 12, "bold"))
    age_combobox = ttk.Combobox(form_frame, values=[str(i) for i in range(1, 101)], state="readonly", font=("Helvetica", 12))

    address_label = Label(form_frame, text="Address", bg="#f0f0f0", fg="#333333", font=("Helvetica", 12, "bold"))
    address_entry = Entry(form_frame, bg="#ffffff", fg="#333333", font=("Helvetica", 12))

    contact_label = Label(form_frame, text="Contact Number", bg="#f0f0f0", fg="#333333", font=("Helvetica", 12, "bold"))
    contact_entry = Entry(form_frame, bg="#ffffff", fg="#333333", font=("Helvetica", 12))

    rate_label = Label(form_frame, text="Rate per Hour", bg="#f0f0f0", fg="#333333", font=("Helvetica", 12, "bold"))
    rate_entry = Entry(form_frame, bg="#ffffff", fg="#333333", font=("Helvetica", 12))

    update_button = Button(new_window, text="Update", bg="#4CAF50", fg="#ffffff", font=("Helvetica", 14, "bold"), relief="flat", command=register)

    # Position the labels and entry fields using grid layout
    firstname_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    firstname_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    lastname_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    lastname_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    age_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    age_combobox.grid(row=2, column=1, padx=9, pady=9, sticky="w")

    address_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
    address_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

    contact_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
    contact_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")

    rate_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")
    rate_entry.grid(row=5, column=1, padx=10, pady=10, sticky="w")

    update_button.pack(pady=20)

    
def newlist():
    root = Tk()
    root.title("Employee's Registration List")
    width = 1000
    height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))
    root.resizable(1, 1)
    root.configure(bg="#000000")
    
    def search_data():
        search_value = search_entry.get()
        if search_value == "":
            messagebox.showwarning("", "Please enter a search query.")
        else:
            conn = sqlite3.connect('juswa.db')
            cursor = conn.cursor()
            cursor.execute("SELECT emp_no firstname, lastname, age, address, contact, rate FROM member WHERE emp_no LIKE ? OR firstname LIKE ?", (f"%{search_value}%", f"%{search_value}%"))
            fetch = cursor.fetchall()

            tree.delete(*tree.get_children())
            for index, data in enumerate(fetch, start=1):
                emp_no = index
                firstname = data[1]
                lastname = data[1]
                age = data[2]
                address = data[3]
                contact = data[4]
                rate = data[5]
                tree.insert('', 'end', values=(emp_no, firstname, lastname, age, address, contact, rate))
            cursor.close()
            conn.close()

    def back_to_all_data():
        search_entry.delete(0, END)
        displayData()


        
    font_style = ('Arial', 12)

    search_frame = Frame(root, bg="#f9f9f9", bd=2, relief=RIDGE)
    search_frame.pack(pady=10, padx=10)

    search_label = Label(search_frame, text="Search:", bg="#f9f9f9", fg="#333333", font=font_style)
    search_label.grid(row=0, column=0, padx=10, pady=5)

    search_entry = Entry(search_frame, font=font_style, bd=2)
    search_entry.grid(row=0, column=1, padx=10, pady=5)

    search_button = Button(search_frame, text="Search", font=font_style, bd=2, bg="#4caf50", fg="#ffffff", command=search_data)
    search_button.grid(row=0, column=2, padx=10, pady=5)

    back_button = Button(search_frame, text="↵", font=font_style, bd=2, bg="#f44336", fg="#ffffff", command=back_to_all_data)
    back_button.grid(row=0, column=3, padx=10, pady=5)
    
    # Variables
    FIRSTNAME = StringVar()
    LASTNAME = StringVar()
    AGE = IntVar()
    ADDRESS = StringVar()
    CONTACT = StringVar()
    RATE = IntVar()

    # Methods
    def Database():
        conn = sqlite3.connect('juswa.db')
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS member (
                emp_no INTEGER PRIMARY KEY AUTOINCREMENT,
                firstname TEXT,
                lastname TEXT,
                age INTEGER,
                address TEXT,
                contact TEXT,
                rate INTEGER
            )
        """)
        conn.commit()
        conn.close()


    def displayData():
        conn = sqlite3.connect('juswa.db')
        cursor = conn.cursor()
        cursor.execute("SELECT emp_no, firstname, lastname, age, address, contact, rate FROM member ORDER BY emp_no ASC")
        fetch = cursor.fetchall()
        tree.delete(*tree.get_children())
        for data in fetch:
            emp_no = data[0]
            firstname = data[1]
            lastname = data[2]
            age = data[3]
            address = data[4]
            contact = data[5]
            rate = data[6]
            tree.insert('', 'end', values=(emp_no, firstname, lastname, age, address, contact, rate))
        cursor.close()
        conn.close()
    def DeleteData():
        selected_items = tree.selection()
        if not selected_items:
            messagebox.showwarning("", "Please select an entry to delete.")
        else:
            confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected entry?")
            if confirm:
                conn = sqlite3.connect('juswa.db')
                cursor = conn.cursor()
                for item in selected_items:
                    emp_no = tree.item(item)['values'][0]
                    cursor.execute("DELETE FROM member WHERE emp_no=?", (emp_no,))
                
                conn.commit()
                cursor.close()
                conn.close()
                # Remove deleted items from the treeview
            for item in selected_items:
                tree.delete(item)

            messagebox.showinfo("", "Entry deleted successfully.")
                
    #=========================================================================sfsdfsdf=================
    def EditData():
        global firstname_entry, lastname_entry, age_combobox, address_entry, contact_entry, rate_entry

        # Get the selected item from the tree
        selected_item = tree.focus()

        if selected_item:
            # Retrieve the data from the selected item
            item_data = tree.item(selected_item)
            data = item_data['values']

            # Extract the values from the data
            firstname = data[1]
            lastname = data[2]
            age = data[3]
            address = data[4]
            contact = data[5]
            rate = data[6]

            # Create the edit window
            new_window = Toplevel()
            new_window.title("Edit Form")
            new_window.geometry("400x550")
            new_window.configure(bg='#FFFFFF')

            top_label = Label(new_window, text="Payroll Edit Profile", bg="#f0f0f0", fg="#333333",
                            font=("Helvetica", 16, "bold"))
            top_label.pack(pady=20)

            # Create a frame for the form fields
            form_frame = Frame(new_window, bg="#f0f0f0")
            form_frame.pack(padx=20, pady=20)

            def UpdateData():
                if (
                    firstname_entry.get() == "" or lastname_entry.get() == "" or
                    age_combobox.get() == "" or address_entry.get() == "" or contact_entry.get() == "" or rate_entry.get() == ""
                ):
                    messagebox.showwarning('', 'Kindly Fill Out The Required Field.', icon="warning")
                else:
                    conn = sqlite3.connect("juswa.db")
                    cursor = conn.cursor()

                    # Get the selected item from the Treeview widget
                    selected_item = tree.selection()
                    if not selected_item:
                        messagebox.showwarning('', 'Please Select a Record to Update!', icon="warning")
                        return

                    # Get the values of the selected item
                    values = tree.item(selected_item)['values']
                    old_firstname = values[1]
                    old_lastname = values[2]

                    # Update the record
                    cursor.execute(
                        "UPDATE member SET firstname=?, lastname=?, age=?, address=?, contact=?, rate=? WHERE firstname=? AND lastname=?",
                        (
                            firstname_entry.get(),
                            lastname_entry.get(),
                            age_combobox.get(),
                            address_entry.get(),
                            contact_entry.get(),
                            rate_entry.get(),
                            old_firstname,
                            old_lastname,
                        )
                    )

                    # Commit the changes to the database
                    conn.commit()

                    # Clear the entry fields
                    firstname_entry.delete(0, END)
                    lastname_entry.delete(0, END)
                    age_combobox.set('')
                    address_entry.delete(0, END)
                    contact_entry.delete(0, END)
                    rate_entry.delete(0, END)

                    # Refresh the data in the Treeview widget
                    displayData()

                    cursor.close()
                    conn.close()


                    messagebox.showinfo('', 'Update Successful!', icon="info")
                    new_window.destroy()

            # Create labels and entry fields for each form field
            firstname_label = Label(form_frame, text="First Name", bg="#f0f0f0", fg="#333333",
                                    font=("Helvetica", 12, "bold"))
            firstname_entry = Entry(form_frame, bg="#ffffff", fg="#333333", font=("Helvetica", 12))

            lastname_label = Label(form_frame, text="Last Name", bg="#f0f0f0", fg="#333333",
                                font=("Helvetica", 12, "bold"))
            lastname_entry = Entry(form_frame, bg="#ffffff", fg="#333333", font=("Helvetica", 12))

            age_label = Label(form_frame, text="Age", bg="#f0f0f0", fg="#333333", font=("Helvetica", 12, "bold"))
            age_combobox = ttk.Combobox(form_frame, values=[str(i) for i in range(1, 101)], state="readonly",
                                        font=("Helvetica", 12))

            address_label = Label(form_frame, text="Address", bg="#f0f0f0", fg="#333333",
                                font=("Helvetica", 12, "bold"))
            address_entry = Entry(form_frame, bg="#ffffff", fg="#333333", font=("Helvetica", 12))

            contact_label = Label(form_frame, text="Contact Number", bg="#f0f0f0", fg="#333333",
                                font=("Helvetica", 12, "bold"))
            contact_entry = Entry(form_frame, bg="#ffffff", fg="#333333", font=("Helvetica", 12))

            rate_label = Label(form_frame, text="Rate per Hour", bg="#f0f0f0", fg="#333333",
                            font=("Helvetica", 12, "bold"))
            rate_entry = Entry(form_frame, bg="#ffffff", fg="#333333", font=("Helvetica", 12))

            update_button = Button(new_window, text="Update", bg="#4CAF50", fg="#ffffff",
                                font=("Helvetica", 14, "bold"), relief="flat", command=UpdateData)

            firstname_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
            firstname_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

            lastname_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
            lastname_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

            age_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
            age_combobox.grid(row=4, column=1, padx=9, pady=9, sticky="w")

            address_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")
            address_entry.grid(row=5, column=1, padx=10, pady=10, sticky="w")

            contact_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")
            contact_entry.grid(row=6, column=1, padx=10, pady=10, sticky="w")

            rate_label.grid(row=7, column=0, padx=10, pady=10, sticky="w")
            rate_entry.grid(row=7, column=1, padx=10, pady=10, sticky="w")

            update_button.pack(pady=20)

            # Populate the entry fields with the retrieved data
            firstname_entry.insert(0, firstname)
            lastname_entry.insert(0, lastname)
            age_combobox.set(str(age))
            address_entry.insert(0, address)
            contact_entry.insert(0, contact)
            rate_entry.insert(0, str(rate))


    
    # Frames
    Mid = Frame(root, width=500, bg="#000000")
    Mid.pack(side=TOP)
    MidRight = Frame(Mid, width=100)
    MidRight.pack(side=RIGHT, pady=10)
    TableMargin = Frame(root, width=500)
    TableMargin.pack(side=TOP)

    # Buttons
    btn_delete = Button(MidRight, text="Delete", bg="#FF1E1E", width=10, font=('arial', 11, 'bold'), command=DeleteData)
    btn_delete.pack(side=RIGHT)
    btn_edit = Button(MidRight, text="Edit", bg="#4CAF50", width=10, font=('arial', 11, 'bold'), command=EditData)
    btn_edit.pack(side=RIGHT)

    # Tables
    scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
    scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
    tree = ttk.Treeview(
        TableMargin,
        columns=("EmpNo", "Firstname", "Lastname", "Age", "Address", "Contact", "RatePerHour"),
        height=400,
        selectmode="extended",
        yscrollcommand=scrollbary.set,
        xscrollcommand=scrollbarx.set
    )
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('EmpNo', text="Employee Number", anchor=W)
    tree.heading('Firstname', text="Firstname", anchor=W)
    tree.heading('Lastname', text="Lastname", anchor=W)
    tree.heading('Age', text="Age", anchor=W)
    tree.heading('Address', text="Address", anchor=W)
    tree.heading('Contact', text="Contact", anchor=W)
    tree.heading('RatePerHour', text="Rate per Hour", anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=150)
    tree.column('#2', stretch=NO, minwidth=0, width=120)
    tree.column('#3', stretch=NO, minwidth=0, width=120)
    tree.column('#4', stretch=NO, minwidth=0, width=80)
    tree.column('#5', stretch=NO, minwidth=0, width=120)
    tree.column('#6', stretch=NO, minwidth=0, width=120)
    tree.pack()

    Database()  # Call the Database function to create the member table if needed
    displayData()  # Call displayData to populate the treeview with initial data



window = Tk()
window.title("Login Form")
window.geometry("340x440")

window.configure(bg='#000000')

# Creating a Login Form
title_label = Label(window, text="Payroll Login", font=("Arial", 18), fg="#E50914", bg="#000000")
title_label.pack(pady=20)
username_label = Label(window, text="Username", font=("Arial", 14), fg="#FFFFFF", bg="#000000")
username_label.pack()
username_entry = Entry(window, font=("Arial", 14), fg="#000000", bg="#FFFFFF")
username_entry.pack(pady=10)
password_label = Label(window, text="Password", font=("Arial", 14), fg="#FFFFFF", bg="#000000")
password_label.pack()
password_entry = Entry(window, show="*", font=("Arial", 14), fg="#000000", bg="#FFFFFF")
password_entry.pack(pady=10)

login_button = Button(window, text="Login", font=("Arial", 14), fg="#FFFFFF", bg="#E50914", command=login)
login_button.pack(pady=20)
login_button.bind("<Return>", login)


window.mainloop()
    