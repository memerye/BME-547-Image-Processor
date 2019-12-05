from tkinter import *
from tkinter import ttk, filedialog


# User login/create account
def login_window():

    root = Tk()
    root.title('Create Account/User Login')

    # Gap row/column
    gap_row = Label(root, text='  ')
    gap_row.grid(column=1, row=1)

    gap_row2 = Label(root, text='  ')
    gap_row2.grid(column=1, row=5)

    gap_row3 = Label(root, text='  ')
    gap_row3.grid(column=1, row=3)

    gap_col = Label(root, text='       ')
    gap_col.grid(column=0, row=2)

    gap_col2 = Label(root, text='       ')
    gap_col2.grid(column=3, row=2)

    # Enter username
    name_label = ttk.Label(root, text='      Username:      ')
    name_label.grid(column=1, row=2, columnspan=1)

    username = StringVar()  # store input from entry box (ttk variable)
    name_entry = ttk.Entry(root, textvariable=username)  # width=50)
    name_entry.grid(column=2, row=2)

    # Create account button
    def create_account():
        # from ** import **
        # username exists
        print('Username: {}'.format(username.get()))
        root.destroy()
        print('Account created successfully.')
        main_window(username.get())
        return

    ca_btn = ttk.Button(root, text='Create Account', command=create_account)
    ca_btn.grid(column=1, row=4)

    # Login button
    def login():
        # open main window
        root.destroy()
        main_window(username.get())
        return

    login_btn = ttk.Button(root, text='Login', command=login)
    login_btn.grid(column=2, row=4)

    root.mainloop()
    return


# Main window
def main_window(username):

    root = Tk()
    root.title('Image Processor')

    # Identify user
    user_label = ttk.Label(root,
                           text='You are logged in as: {}'.format(username))
    user_label.grid(column=0, row=1, columnspan=3, sticky=W)

    root.mainloop()
    return


if __name__ == '__main__':
    login_window()
