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

    # View user data
    def user_data():
        print('Get data summary from database')
        user_data_window()
        return

    user_data_btn = ttk.Button(root, text='View my user data',
                               command=user_data)
    user_data_btn.grid(column=3, row=1)

    # Images upload/choose from history
    action_label = ttk.Label(root, text='1. Choose an action to begin: ')
    action_label.grid(column=0, row=2, columnspan=2, sticky=W)

    # Images upload/choose from history
    process_opt = StringVar(None, 'Histogram Equalization')
    action_label = ttk.Label(root, text='2. Choose a process option: ')
    action_label.grid(column=0, row=6, columnspan=2, sticky=W)

    # select button
    botton1 = ttk.Radiobutton(root, text='Histogram Equalization', variable=process_opt, value='Histogram Equalization')
    botton1.grid(column=1, row=8, columnspan=1, sticky=W)
    botton2 = ttk.Radiobutton(root, text='Contrast Stretching', variable=process_opt, value='Contrast Stretching')
    botton2.grid(column=2, row=8, columnspan=1, sticky=W)
    botton3 = ttk.Radiobutton(root, text='Log Compression', variable=process_opt, value='Log Compression')
    botton3.grid(column=1, row=10, columnspan=1, sticky=W)
    botton4 = ttk.Radiobutton(root, text='Invert Image', variable=process_opt, value='Invert Image')
    botton4.grid(column=2, row=10, columnspan=1, sticky=W)

    # start to process image
    def process():
        print('Process {} requested'.format(process_opt.get()))
        if process_opt.get() == 'Histogram Equalization':
            print("he")
            return
        elif process_opt.get() == 'Contrast Stretching':
            print("cs")
            return
        elif process_opt.get() == 'Log Compression':
            print("lc")
            return
        elif process_opt.get() == 'Invert Image':
            print("ii")
            return
        return

    # Process button
    process_btn = ttk.Button(root, text='Process', command=process)
    process_btn.grid(column=3, row=12, columnspan=1, sticky=E)

    # Upload button
    def upload_img():
        # open local directory
        # right now, only one file can be selected
        root.file = filedialog.askopenfilename(filetypes=[
            ('Image files', '.png .jpg .jpeg .tif .zip',)])
        file_label = ttk.Label(root, text='{}'.format(root.file), width=50)
        file_label.grid(column=2, row=3, columnspan=2, sticky=W)
        return

    upld_btn = ttk.Button(root, text='Upload image file(s)', command=upload_img)
    upld_btn.grid(column=1, row=3, sticky=W)

    # History button
    def history():
        print('Retrieve')
        # outputs history into pull down menu
        donor_center_combo['values'] = ('values will be output of history',
                                        'None')
        return

    hist_btn = ttk.Button(root, text='Choose from history', command=history)
    hist_btn.grid(column=1, row=4, sticky=W)

    # History pull down
    history = StringVar()
    donor_center_combo = ttk.Combobox(root, textvariable=history)
    donor_center_combo.grid(column=2, row=4, sticky=W)
    donor_center_combo.state(['readonly'])

    root.mainloop()
    return


def user_data_window():
    root = Tk()
    root.title('Your User Data Summary')
    data_label = ttk.Label(root,
                           text='You have done ** things # number of times')
    data_label.grid(column=0, row=1)
    root.mainloop()
    return


if __name__ == '__main__':
    login_window()
