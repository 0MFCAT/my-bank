import requests.exceptions
import bank as bk
from tkinter import *
from tkinter import messagebox
from tkinter import font
from PIL import ImageTk, Image
from custom_errors import *

root = Tk()
root.withdraw()  # Hides the root windows until the user logs in
root.iconbitmap("icon.ico")
root.title("Global Crypto Bank")
root.resizable(False, False)
my_img = ImageTk.PhotoImage(Image.open("icon.ico"))  # Loads the logo of the bank


def bank_gui(main_bank_user, img):
    # Main Screen after the login, not the cleanest execution but the easiest way to make it
    # Next time I'll make everything right from the scratch
    def send():

        def cancel():
            toplevel_1.destroy()
            root.attributes("-disabled", False)

        def send_confirm():
            try:
                # sends USD from main account to another account using the bank ID
                main_bank_user.send_usd(float(entry_2.get()), int(entry_3.get()))
                # TODO: fix the window so it doesn't minimize after enabling it again
                messagebox.showinfo("Successful transaction", f"You have successfully sent {entry_2.get()} to the bank user with the ID: {entry_3.get()}") # TODO: Check This
                cancel()
            except NoBalance:
                messagebox.showerror("Not enough balance", "Insufficient founds for that transaction")
            except ValueError:
                messagebox.showerror("Wrong input", "The fields should contain valid numbers")
            except WrongFormatID:
                messagebox.showerror("ID Error", "ID must be a unique number of 9 digits")
            except WrongID:
                messagebox.showerror("ID Error", "The receiver ID doesn't exist")

        root.attributes("-disabled", True)
        toplevel_1 = Tk()
        toplevel_1.title("Send USD")
        toplevel_1.resizable(False, False)
        toplevel_1.configure(height=200, padx=10, pady=10, width=200)
        labelframe_1 = LabelFrame(toplevel_1)
        labelframe_1.configure(height=200, padx=10, pady=10, width=200)
        label_2 = Label(labelframe_1)
        label_2.configure(text='USD to send', width=10)
        label_2.grid(column=0, row=0)
        entry_2 = Entry(labelframe_1)
        entry_2.configure(justify="center", width=12)
        entry_2.grid(column=0, padx=10, pady=7, row=1)
        button_2 = Button(labelframe_1)
        button_2.configure(text='Send', command=send_confirm, width=5)
        button_2.grid(column=0, columnspan=2, pady=7, row=2)
        label_3 = Label(labelframe_1)
        label_3.configure(text='User ID', width=10)
        label_3.grid(column=1, row=0)
        entry_3 = Entry(labelframe_1)
        entry_3.configure(justify="center", width=12)
        entry_3.grid(column=1, padx=10, pady=5, row=1)
        button_3 = Button(labelframe_1)
        button_3.configure(text='Cancel', command=cancel)
        button_3.grid(column=0, columnspan=2, pady="7 0", row=3)
        labelframe_1.grid(column=0, row=0)

    def logout():
        root.withdraw()
        logging.deiconify()

    root.configure(height=200, padx=5, pady=5, width=200)
    labelframe1 = LabelFrame(root)
    labelframe1.configure(height=200, padx=10, pady=5, width=300)
    label0 = Label(labelframe1)
    label0.configure(image=img)
    label0.grid(column=0, pady="0 10", row=0, rowspan=2)
    label1 = Label(labelframe1)
    label1.configure(text=main_bank_user.bank_user.full_name)
    label1.grid(column=1, row=0)
    label2 = Label(labelframe1)
    label2.configure(text=f"ID: {main_bank_user.user_id}")
    label2.grid(column=1, row=1)
    label4 = Label(labelframe1)
    label4.configure(text=f'USD: {main_bank_user.usd}')
    label4.grid(column=0, columnspan=1, row=3, sticky="w")
    label5 = Label(labelframe1)
    label5.configure(text=f'USDT: {main_bank_user.usdt}')
    label5.grid(column=0, row=4, sticky="w")
    label6 = Label(labelframe1)
    label6.configure(text=f'BTC: {main_bank_user.btc}')
    label6.grid(column=0, row=5, sticky="w")
    label7 = Label(labelframe1)
    label7.configure(text=f'ETH: {main_bank_user.eth}')
    label7.grid(column=0, row=6, sticky="w")
    labelframe3 = LabelFrame(labelframe1)
    labelframe3.configure(height=200, width=200)
    label8 = Label(labelframe3)
    label8.configure(font="{segoe ui} 12 {}", state="normal", text='Exchange Pairs', width=18)
    label8.grid(row=0)
    label9 = Label(labelframe3)
    label9.configure(text=f'USD/CUP = {main_bank_user.pairUSD_CUP}', width=18)
    label9.grid(column=0, row=1)
    label10 = Label(labelframe3)
    label10.configure(text=f'BTC/USDT = {main_bank_user.pairBTC_USD}', width=18)
    label10.grid(column=0, row=2)
    label11 = Label(labelframe3)
    label11.configure(text=f'ETH/USDT = {main_bank_user.pairETH_USD}', width=18)
    label11.grid(column=0, row=3)
    label14 = Label(labelframe3)
    label14.configure(text=f'USDT/USD = {main_bank_user.pairUSDT_USD}', width=18)
    label14.grid(column=0, row=4)
    labelframe3.grid(column=2, columnspan=2, row=2, rowspan=5)
    label12 = Label(labelframe1)
    label12.configure(text='Total amount (USDT)')
    label12.grid(column=3, padx=5, row=0)
    label13 = Label(labelframe1)
    label13.configure(text=f'CUP: {main_bank_user.cup}')
    label13.grid(column=0, row=2, sticky="w")
    label15 = Label(labelframe1)
    label15.configure(text=f'${main_bank_user.total_value_usd()}')
    label15.grid(column=3, row=1, sticky="n")
    labelframe1.grid(column=0, columnspan=4, row=0)
    button1 = Button(root)
    button1.configure(
        justify="left",
        overrelief="flat",
        text='Exchange',
        width=7)
    button1.grid(column=0, padx=5, pady=5, row=1)
    button2 = Button(root)
    button2.configure(text='Send', width=7, command=send)
    button2.grid(column=1, padx=5, pady=5, row=1)
    button3 = Button(root)
    button3.configure(text='Stake', width=7)
    button3.grid(column=2, padx=5, pady=5, row=1)
    button4 = Button(root)
    button4.configure(text='Log Out', width=7, command=logout)
    button4.grid(column=3, padx=5, pady=5, row=1)


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
        # Creates the main user using the data from the database
        main_user = bk.User(db_values[0][0], db_values[0][1], db_values[0][2], db_values[0][3], db_values[0][4],
                            db_values[0][5])
        bank_values = bk.BankAccount.inst_bank(user_email)
        try:
            # Creates the main bank user with all the financial data from the database
            main_bank_user = bk.BankAccount(main_user, *bank_values)
            messagebox.showinfo("Success!",
                                f"Welcome back {main_user.full_name}")
            logging.withdraw()
            entry1_var.set("")
            entry2_var.set("")
            bank_gui(main_bank_user, my_img)
            root.deiconify()  # Shows the previously hidden root window using withdraw()
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Connection Error", "You must be online to log in")
    else:
        entry1_var.set("")
        entry2_var.set("")
        messagebox.showerror("ERROR", "Wrong Username or Password, please try again")


def sign_up():
    def sign_up_button():
        try:
            bk.User.sign_up(entry3.get(), entry4.get(), int(entry5.get()), entry6.get(), entry7.get(), entry8.get())
            bk.BankAccount.initialize_bank(entry7.get())
            messagebox.showinfo("You are in", "You successfully created your account")
            # TODO: close the screen and return to the logging screen
            toplevel1.destroy()
            logging.deiconify()
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
                       textvariable=entry1_var)  # I create a variable to control the text of the Entry
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
