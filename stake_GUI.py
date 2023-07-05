#!/usr/bin/python3
import tkinter as tk
import bank as bk
from custom_errors import *
from tkinter import messagebox


class Stake_GUI:

    def back(self):
        self.master.attributes("-disabled", False)
        self.mainwindow.destroy()

    @staticmethod
    def stake(bank_user, master):

        def back():
            master.attributes("-disabled", False)
            toplevel_1.destroy()

        def stake():
            try:
                if float(entry_1.get()) <= 0:
                    raise ValueError("")
                bank_user.stake(float(entry_1.get()))
                messagebox.showinfo("Success", f"You staked {float(entry_1.get())} USD successfully, you can claim them in 7 days or more")
                back()
            except ValueError:
                messagebox.showerror("Value Error", "Expecting USD real numbers, no negative values, no characters or empty line")
            except NoMultiStake:
                messagebox.showerror("Can't stake more", "Can't stake more than once, please unstake before trying to stake again")
            except NoBalance:
                messagebox.showerror("No Balance", "Not enough USD to stake, please check your amount")
            finally:
                entry1_text.set("")

        master.attributes("-disabled", True)
        toplevel_1 = tk.Tk() if master is None else tk.Toplevel(master)
        toplevel_1.resizable(False, False)
        toplevel_1.title("Stake")
        toplevel_1.protocol("WM_DELETE_WINDOW", back)
        toplevel_1.configure(height=200, width=200)
        labelframe_1 = tk.LabelFrame(toplevel_1)
        labelframe_1.configure(height=200, padx=5, pady=5, width=200)
        label_1 = tk.Label(labelframe_1)
        label_1.configure(
            font="{Segoe UI} 12 {}",
            justify="center",
            text='How much USD to stake')
        entry1_text = tk.StringVar()
        label_1.grid(column=0, columnspan=2, padx=5, pady=5, row=0)
        entry_1 = tk.Entry(labelframe_1)
        entry_1.configure(width=10, textvariable=entry1_text)
        entry_1.grid(column=0, columnspan=2, padx=5, pady=5, row=1)
        button_1 = tk.Button(labelframe_1)
        button_1.configure(text='Stake', width=6, command=stake)
        button_1.grid(column=0, padx=5, pady=5, row=2)
        button_2 = tk.Button(labelframe_1)
        button_2.configure(text='Cancel', width=6, command=back)
        button_2.grid(column=1, padx=5, pady=5, row=2)
        labelframe_1.grid(column=0, padx=5, pady=5, row=0)

    def unstake(self):
        try:
            self.bank_user.return_stake()
            messagebox.showinfo("Success", "You unstaked your USD successfully, please consider staking more")
        except StakeTimeError as error:
            messagebox.showerror("Stake Time Error", f"{error.message}")
        except WrongStakeID as error:
            messagebox.showerror("ID Error", error.message)

    def update_values(self):
        try:
            text1 = self.bank_user.check_staked_usd()
        except WrongStakeID:
            text1 = 0
        self.label_3.configure(text=text1)
        try:
            text2 = self.bank_user.check_expected_return()
        except WrongStakeID:
            text2 = 0
        self.label_5.configure(text=text2)
        self.toplevel_1.after(1000, self.update_values)

    def __init__(self, bank_user, master=None):
        # build ui
        self.bank_user = bank_user
        self.master = master
        toplevel_1 = tk.Tk() if master is None else tk.Toplevel(master)
        toplevel_1.resizable(False, False)
        toplevel_1.title("Stake")
        self.toplevel_1 = toplevel_1
        self.toplevel_1.after(1000, self.update_values)
        self.toplevel_1.protocol("WM_DELETE_WINDOW", self.back)
        self.toplevel_1.configure(height=200, width=200)
        labelframe_1 = tk.LabelFrame(toplevel_1)
        labelframe_1.configure(height=200, padx=5, pady=5, width=200)
        label_1 = tk.Label(labelframe_1)
        label_1.configure(
            font="{Segoe UI} 12 {}",
            justify="center",
            text='Staking')
        label_1.grid(column=0, columnspan=2, row=0)
        labelframe_2 = tk.LabelFrame(labelframe_1)
        labelframe_2.configure(height=200, width=200)
        label_2 = tk.Label(labelframe_2)
        label_2.configure(padx=5, pady=5, text='Staked Amount')
        label_2.grid(column=0, row=1)

        label_3 = tk.Label(labelframe_2)
        self.label_3 = label_3
        try:
            text1 = self.bank_user.check_staked_usd()
        except WrongStakeID:
            text1 = 0
        self.label_3.configure(padx=5, pady=5, text=text1)
        self.label_3.grid(column=0, row=2)
        labelframe_2.grid(column=0, padx=10, pady=5, row=3)
        self.labelframe_3 = tk.LabelFrame(labelframe_1)
        self.labelframe_3.configure(height=200, width=200)
        label_4 = tk.Label(self.labelframe_3)
        label_4.configure(padx=5, pady=5, text='Current reward')
        label_4.grid(column=1, row=1)
        label_5 = tk.Label(self.labelframe_3)
        self.label_5 = label_5
        try:
            text2 = self.bank_user.check_expected_return()
        except WrongStakeID:
            text2 = 0
        self.label_5.configure(padx=5, pady=5, text=text2)
        self.label_5.grid(column=1, row=2)
        self.labelframe_3.grid(column=1, padx=10, pady=5, row=3)
        button_1 = tk.Button(labelframe_1)
        button_1.configure(text='Stake', width=7, command=lambda: self.stake(self.bank_user, self.toplevel_1))
        button_1.grid(column=0, row=4)
        button_2 = tk.Button(labelframe_1)
        button_2.configure(text='Unstake', width=7, command=self.unstake)
        button_2.grid(column=1, row=4)
        button_3 = tk.Button(labelframe_1)
        button_3.configure(text='Cancel', width=7, command=self.back)
        button_3.grid(column=0, columnspan=2, pady="10 0", row=6)
        labelframe_1.grid(column=0, padx=5, pady=5, row=0)

        # Main widget
        self.mainwindow = self.toplevel_1


    def run(self):
        self.mainwindow.mainloop()
