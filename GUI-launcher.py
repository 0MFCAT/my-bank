from bank import *
from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import font

root = Tk()
root.iconbitmap("icon.ico")
root.title("Global Crypto Bank")
root.geometry("400x400")

#New font I made for the small and big Labels
regular_font = font.Font(family="Segoe UI", size=9)
big_font = font.Font(family="Segoe UI", size=12)
root.option_add("*Font", regular_font) #Establishing regular_font as the default font for all new widgets

#Creating a logging screen before accessing the bank system
logging = Toplevel()
logging.title("Log in please")

#adding Labels, Entries, a Frame and some Buttons
logging_label1 = Label(logging, font = big_font, text = "Please Log In") 
logging_frame = LabelFrame(logging, padx = 10, pady = 5)
logging_label2 = Label(logging_frame, text = "Email:", padx = 10)
logging_entry1 = Entry(logging_frame, width= 30)
logging_label3 = Label(logging_frame, text = "Password:", padx = 10)
logging_entry2 = Entry(logging_frame, width= 30)
#TODO: Finish the buttons +
#logging_button1 = Button(logging_frame, text = "Log in", command=  )
#logging_button2 = Button(logging_frame, text = "Sign up", command=  )
logging_button2 = Button(logging_frame, text = "Exit", command= root.quit)


#pushing the widgets on the logging screen
logging_label1.grid(row = 0, column = 0, columnspan= 3)
logging_frame.grid(row = 1, column = 0, columnspan= 3, padx = 10, pady = 5)
logging_label2.grid(row = 0, column = 0, sticky = W)
logging_entry1.grid(row = 1, column = 0, pady = 5, padx = 30)
logging_label3.grid(row = 2, column = 0, sticky = W)
logging_entry2.grid(row = 3, column = 0, pady = 5, padx = 30)

logging_button2.grid(row = 4, column = 3)

root.mainloop()