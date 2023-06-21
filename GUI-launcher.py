import bank as bk
from tkinter import *
from tkinter import messagebox
from tkinter import font

root = Tk()
root.withdraw()  # Hides the root windows until the user logs in
root.iconbitmap("icon.ico")
root.title("Global Crypto Bank")
root.geometry("400x400")
root.resizable(False, False)

# New font I made for the small and big Labels
regular_font = font.Font(family="Segoe UI", size=9)
big_font = font.Font(family="Segoe UI", size=12, underline=True)
root.option_add("*Font", regular_font)  # Establishing regular_font as the default font for all new widgets

# Creating a logging screen before accessing the bank system
logging = Toplevel()
logging.resizable(False, False)
logging.title("Log in")
logging.iconbitmap("icon.ico")

# Creating TKinter Variables
entry1_var = StringVar()
entry2_var = StringVar()


# Buttons Functions for login
def login():
    user_email = logging_entry1.get()
    user_password = logging_entry2.get()
    db_values = bk.User.logging(user_email, user_password)
    if db_values:
        # Create the main user using the data from the database
        main_user = bk.User(db_values[0][0], db_values[0][1], db_values[0][2], db_values[0][3], db_values[0][4],
                            db_values[0][5])
        messagebox.showinfo("Success!",
                            f"Welcome back {main_user.full_name}")
        logging.destroy()
        root.deiconify()  # Shows the previously hidden root window using withdraw()

    else:
        entry1_var.set("")
        entry2_var.set("")
        messagebox.showerror("ERROR", "Wrong Username or Password, please try again")


def sign_up():
    def sign_up_button():
        try:
            bk.User.sign_up(entry3.get(), entry4.get(), int(entry5.get()), entry6.get(), entry7.get(), entry8.get())
            messagebox.showinfo("You are in", "You successfully created your account")
            # TODO: close the screen and return to the logging screen
        except ValueError:
            messagebox.showerror("Fatal Error", "Please fill all the fields with valid information")

    def sign_cancel_button():
        toplevel1.destroy()
        logging.deiconify()

    toplevel1 = Toplevel(root)
    toplevel1.resizable(False, False)
    toplevel1.iconbitmap("icon.ico")
    toplevel1.title("Sign Up")
    toplevel1.configure(height=300, padx=10, pady=10, width=300)
    logging.withdraw()
    label1 = Label(toplevel1)
    label1.configure(
        font="{Segoe UI} 12 {underline}",
        pady=2,
        state="normal",
        text='Please Sign Up')
    label1.grid(column=0, columnspan=3, row=0)
    labelframe2 = LabelFrame(toplevel1)
    labelframe2.configure(height=0, padx=0, pady=5)
    label5 = Label(labelframe2)
    label5.configure(
        font="{segoe ui} 9 {}",
        padx=15,
        pady=3,
        text='First name:')
    label5.grid(column=0, row=0, sticky="w")
    entry3 = Entry(labelframe2)
    entry3.configure(borderwidth=3, width=25)
    entry3.grid(column=0, columnspan=3, padx=35, row=1)
    label7 = Label(labelframe2)
    label7.configure(
        font="{segoe ui} 9 {}",
        padx=15,
        pady=3,
        text='Last name:')
    label7.grid(column=0, row=2, sticky="w")
    entry4 = Entry(labelframe2)
    entry4.configure(borderwidth=3, width=25)
    entry4.grid(column=0, columnspan=3, padx=35, row=3)
    label8 = Label(labelframe2)
    label8.configure(
        font="{segoe ui} 9 {}",
        padx=15,
        pady=3,
        text='Year of birth:')
    label8.grid(column=0, row=4, sticky="w")
    entry5 = Entry(labelframe2)
    entry5.configure(borderwidth=3, width=25)
    entry5.grid(column=0, columnspan=3, padx=35, row=5)
    label9 = Label(labelframe2)
    label9.configure(
        font="{segoe ui} 9 {}",
        padx=15,
        pady=3,
        text='Country:')
    label9.grid(column=0, row=6, sticky="w")
    entry6 = Entry(labelframe2)
    entry6.configure(borderwidth=3, width=25)
    entry6.grid(column=0, columnspan=3, padx=35, row=7)
    label10 = Label(labelframe2)
    label10.configure(
        font="{segoe ui} 9 {}",
        padx=15,
        pady=3,
        text='Email:')
    label10.grid(column=0, row=8, sticky="w")
    entry7 = Entry(labelframe2)
    entry7.configure(borderwidth=3, width=25)
    entry7.grid(column=0, columnspan=3, padx=35, row=9)
    label11 = Label(labelframe2)
    label11.configure(
        font="{segoe ui} 9 {}",
        padx=15,
        pady=3,
        text='Password:')
    label11.grid(column=0, row=10, sticky="w")
    entry8 = Entry(labelframe2)
    entry8.configure(borderwidth=3, width=25)
    entry8.grid(column=0, columnspan=3, padx=35, row=11)
    labelframe2.grid(column=0, columnspan=3, row=1)
    button2 = Button(toplevel1)
    button2.configure(text='Sign Up', width=10)
    button2.grid(column=0, pady=5, row=2)
    button2.configure(command=sign_up_button)
    button3 = Button(toplevel1)
    button3.configure(text='Cancel', width=10)
    button3.grid(column=2, pady=5, row=2)
    button3.configure(command=sign_cancel_button)


# adding Labels, Entries, a Frame and some Buttons
logging_label1 = Label(logging, font=big_font, text="Please Log In")
logging_frame = LabelFrame(logging, padx=10, pady=3)
logging_label2 = Label(logging_frame, text="Email:", padx=10)
logging_entry1 = Entry(logging_frame, width=30, bd=3,
                       textvariable=entry1_var)  # I create a textvariable to control the text of the Entry
logging_label3 = Label(logging_frame, text="Password:", padx=10)
logging_entry2 = Entry(logging_frame, width=30, bd=3, textvariable=entry2_var)

logging_button1 = Button(logging_frame, text="Log in", width=7, pady=3, command=login)
logging_button2 = Button(logging_frame, text="Sign up", width=7, pady=3, command=sign_up)
logging_button3 = Button(logging_frame, text="Exit", width=7, pady=3, command=root.quit)

# pushing the widgets on the logging screen
logging_label1.grid(row=0, column=0, columnspan=3)
logging_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=5)
logging_label2.grid(row=0, column=0, columnspan=3, sticky=W)
logging_entry1.grid(row=1, column=0, columnspan=3, pady=5, padx=30)
logging_label3.grid(row=2, column=0, columnspan=3, sticky=W)
logging_entry2.grid(row=3, column=0, columnspan=3, pady=5, padx=30)

logging_button1.grid(row=4, column=0)
logging_button2.grid(row=4, column=1)
logging_button3.grid(row=4, column=2)

root.mainloop()
