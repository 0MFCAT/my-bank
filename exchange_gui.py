#!/usr/bin/python3
import tkinter as tk
import bank as bk
from custom_errors import *
from tkinter import messagebox


class Exchange_GUI:

    def back(self):
        self.master.attributes("-disabled", False)
        self.mainwindow.destroy()

    def __init__(self, bank_user, master=None):
        # build ui
        self.bank_user = bank_user
        self.master = master
        toplevel_1 = tk.Tk() if master is None else tk.Toplevel(master)
        toplevel_1.protocol("WM_DELETE_WINDOW", self.back)
        toplevel_1.configure(height=200, width=200)
        labelframe_1 = tk.LabelFrame(toplevel_1)
        labelframe_1.configure(height=200, padx=5, pady=5, width=200)
        labelframe_2 = tk.LabelFrame(labelframe_1)
        labelframe_2.configure(height=200, width=200)
        self.tkvar1 = tk.StringVar()
        self.tkvar1.set("CUP")
        __values = ["CUP", "USDT", "BTC", "ETH"]
        self.optionmenu_1 = tk.OptionMenu(labelframe_2, self.tkvar1, *__values)
        self.optionmenu_1.configure(width=4)
        self.optionmenu_1.grid(column=0, row=3)
        button_2 = tk.Button(labelframe_2)
        button_2.configure(padx=20, text='Exchange')
        button_2.grid(column=0, columnspan=2, padx=5, pady="10 5", row=5)
        button_2.configure(command=self.exchanger_to_usd)
        label_4 = tk.Label(labelframe_2)
        label_4.configure(text='to USD')
        label_4.grid(column=1, row=3)
        self.entry_2 = tk.Entry(labelframe_2)
        entry2_var = tk.StringVar()
        self.entry2_var = entry2_var
        self.entry_2.configure(justify="center", width=10, textvariable=self.entry2_var)
        self.entry_2.grid(column=0, columnspan=2, pady="7 0", row=4)
        labelframe_2.grid(column=0, columnspan=2, row=3)
        labelframe_3 = tk.LabelFrame(labelframe_1)
        labelframe_3.configure(height=200, width=200)
        self.tkvar2 = tk.StringVar()
        self.tkvar2.set("CUP")
        self.optionmenu_2 = tk.OptionMenu(labelframe_3, self.tkvar2, *__values)
        self.optionmenu_2.configure(width=4)
        self.optionmenu_2.grid(column=1, row=1)
        label_2 = tk.Label(labelframe_3)
        label_2.configure(text='USD to')
        label_2.grid(column=0, row=1)
        button_1 = tk.Button(labelframe_3)
        button_1.configure(padx=20, text='Exchange')
        button_1.grid(column=0, columnspan=2, padx=5, pady="10 5", row=3)
        button_1.configure(command=self.exchanger_from_usd)
        entry1_var = tk.StringVar()
        self.entry1_var = entry1_var
        self.entry_1 = tk.Entry(labelframe_3)
        self.entry_1.configure(justify="center", width=10, textvariable=self.entry1_var)
        self.entry_1.grid(column=0, columnspan=2, pady="7 0", row=2)
        labelframe_3.grid(column=0, pady="10 2", row=2)
        label_5 = tk.Label(labelframe_1)
        label_5.configure(
            font="{Segoe UI} 12 {underline}",
            text='Currency Converter')
        label_5.grid(column=0, pady="0 5", row=1)
        button_3 = tk.Button(labelframe_1)
        button_3.configure(padx=10, text='Back', command=self.back)
        button_3.grid(column=0, pady="5 2", row=5)
        labelframe_1.grid(column=0, padx=10, pady=10, row=0)
        labelframe_1.rowconfigure(0, pad=5, weight=5)

        # Main widget
        self.mainwindow = toplevel_1

    def run(self):
        self.mainwindow.mainloop()

    def exchanger_to_usd(self):
        try:
            self.bank_user.exchange_to_usd(self.tkvar1.get(), float(self.entry_2.get()))
            messagebox.showinfo("Exchanged", f"You successfully exchanged {self.entry_2.get()} {self.tkvar1.get()} to USD.")
        except NoBalance:
            messagebox.showerror("No Balance", f"Not enough {self.tkvar1.get()} for that transaction")
        except ValueError:
            messagebox.showerror("Wrong Input", "The fields should contain valid numbers")
        finally:
            self.entry1_var.set("")
            self.entry2_var.set("")

    def exchanger_from_usd(self):
        try:
            self.bank_user.exchange_from_usd(self.tkvar2.get(), float(self.entry_1.get()))
            messagebox.showinfo("Exchanged", f"You successfully exchanged {self.entry_1.get()} USD to {self.tkvar2.get()}.")
        except NoBalance:
            messagebox.showerror("No Balance", f"Not enough USD for that transaction")
        except ValueError:
            messagebox.showerror("Wrong Input", "The fields should contain valid numbers")
        finally:
            self.entry1_var.set("")
            self.entry2_var.set("")
