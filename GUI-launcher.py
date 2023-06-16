from bank import *
from tkinter import *
from tkinter import messagebox
from tkinter import font

root = Tk()
root.withdraw()  # Hides the root windows until the user logs in
root.iconbitmap("icon.ico")
root.title("Global Crypto Bank")
root.geometry("400x400")

# New font I made for the small and big Labels
regular_font = font.Font(family="Segoe UI", size=9)
big_font = font.Font(family="Segoe UI", size=12)
root.option_add("*Font", regular_font)  # Establishing regular_font as the default font for all new widgets

# Creating a logging screen before accessing the bank system
logging = Toplevel()
logging.title("Log in please")

# Creating TKinter Variables
entry1_var = StringVar()
entry2_var = StringVar()


# Buttons Functions for loggin
def login():  # TODO: Make the loggic so at the momment you succesfully log in the system instantiates you with all the properties from the database
    user_email = logging_entry1.get()
    user_password = logging_entry2.get()
    if User.logging(user_email, user_password):
        # Get my database values on a variable
        database_values = db.construct_user(logging_entry1.get(), logging_entry2.get())
        # Create the main user using the data from the database
        main_user = User(database_values[0][0], database_values[0][1], database_values[0][2], database_values[0][3], database_values[0][4], database_values[0][5])
        messagebox.showinfo("Success!",
                            f"Welcome back {main_user.full_name}")
        logging.destroy()
        root.deiconify()  # Shows the previously hidden root window using withdraw()

    else:
        entry1_var.set("")
        entry2_var.set("")
        messagebox.showerror("ERROR", "Wrong Username or Password, please try again")


def sign_up():
    pass


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
