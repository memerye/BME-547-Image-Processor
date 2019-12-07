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

    # Upload button
    def upload_img():
        # open local directory
        # right now, only one file can be selected
        root.file = filedialog.askopenfilename(filetypes=[
            ('Image files', '.png .jpg .jpeg .tif .zip',)])

        file_label = ttk.Label(root, text='...{}'.format(root.file[-50::]),
                               width=50)
        file_label.grid(column=2, row=3, columnspan=2)
        return

    upld_btn = ttk.Button(root, text='Upload image file(s)',
                          command=upload_img)
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

    # process option
    process_opt = StringVar(None, 'Histogram Equalization')
    pro_label = ttk.Label(root, text='2. Choose a process option: ')
    pro_label.grid(column=0, row=6, columnspan=2, sticky=W)

    # process option select button
    botton1 = ttk.Radiobutton(root, text='Histogram Equalization',
                              variable=process_opt,
                              value='Histogram Equalization')
    botton1.grid(column=1, row=8, columnspan=1, sticky=W)
    botton2 = ttk.Radiobutton(root, text='Contrast Stretching',
                              variable=process_opt,
                              value='Contrast Stretching')
    botton2.grid(column=2, row=8, columnspan=1, sticky=W)
    botton3 = ttk.Radiobutton(root, text='Log Compression',
                              variable=process_opt,
                              value='Log Compression')
    botton3.grid(column=1, row=10, columnspan=1, sticky=W)
    botton4 = ttk.Radiobutton(root, text='Invert Image',
                              variable=process_opt,
                              value='Invert Image')
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
    #
    # # Image Display frame
    # img_frame = ttk.Frame(root, height=600, width=700)
    # # img_frame.pack()
    # # img_frame.columnconfigure(2, weight=1)
    # # img_frame.rowconfigure(2, weight=1)
    # img_frame.grid(column=1, row=13, columnspan=4)
    # # processed image frame
    # img_pro_frame = ttk.LabelFrame(img_frame, text='Processed Image',
    #                                height=250, width=300)
    # img_pro_frame.grid(column=1, row=1, columnspan=1)
    # # original image frame
    # img_orig_frame = ttk.LabelFrame(img_frame, text='Original Image',
    #                                 height=250, width=300)
    # img_orig_frame.grid(column=2, row=1, columnspan=1)
    # # histogram for processed image frame
    # hist_pro_frame = ttk.LabelFrame(img_frame,
    #                                 text='Processed Img. Histogram',
    #                                 height=250, width=300)
    # hist_pro_frame.grid(column=1, row=2, columnspan=1)
    # # histogram for original image frame
    # hist_pro_frame = ttk.LabelFrame(img_frame,
    #                                 text='Original Img. Histogram',
    #                                 height=250, width=300)
    # hist_pro_frame.grid(column=2, row=2, columnspan=1)
    # # previous/next frame
    # prev_frame = ttk.Frame(root, height=600, width=20)
    # prev_frame.grid(column=0, row=13)
    # next_frame = ttk.Frame(root, height=600, width=20)
    # next_frame.grid(column=5, row=13)

    # previous/next button
    def previous_img():
        print('get previous image from server')
        print('display images')
        return

    def next_img():
        print('get previous image from server')
        print('display images')
        return

    # prev_btn = ttk.Button(prev_frame, text='<',
    #                       width=1, command=previous_img)
    # prev_btn.grid(column=1, row=1)
    # next_btn = ttk.Button(next_frame, text='>', width=1, command=next_img)
    # next_btn.grid(column=1, row=1)

    # Download Section
    download_opt = StringVar(None, 'jpeg')
    download_label = ttk.Label(root, text='4. Select download format: ')
    download_label.grid(column=0, row=14, columnspan=2, sticky=W)

    download_cb = ttk.Combobox(root, textvariable=download_opt)
    download_cb.grid(column=1, row=16, sticky=E)
    download_cb["values"] = ("jpeg", "png", "tiff")
    download_cb.state(['readonly'])

    def download():
        root.file = filedialog.\
            asksaveasfilename(title='Download Image',
                              defaultextension='.{}'.format(
                                  download_opt.get()),
                              initialdir='/',
                              initialfile='Image.{}'
                              .format(download_opt.get()),
                              filetypes=[(download_opt.get(), '*.{}'
                                          .format(download_opt.get()))])

    download_btn = ttk.Button(root, text='Download', command=download)
    download_btn.grid(column=3, row=16, sticky=E)

    # upload time function
    # def upload_time():
    #     global time_upload
    #     time_upload = str(datetime.datetime.now())
    #     print(time_upload)
    #     return

    # back to login function at main window
    def back_to_login():
        root.destroy()
        login_window()
        return

    # back to login button
    back_to_login_btn = ttk.Button(root, text='Back to Login',
                                   command=back_to_login)
    back_to_login_btn.grid(column=5, row=21, sticky=E)

    # exit function at main window
    def exit():
        root.destroy()
        return

    # exit button
    exit_btn = ttk.Button(root, text='Exit',
                          command=exit)
    exit_btn.grid(column=6, row=21, sticky=E)

    # process info include uploaded/processing time and image size
    uptime_label = ttk.Label(root, text='Uploaded time: b')
    uptime_label.grid(column=0, row=19, columnspan=2, sticky=W)
    protime_label = ttk.Label(root, text='Processsing time: a')
    protime_label.grid(column=2, row=19, columnspan=2, sticky=W)
    size_label = ttk.Label(root, text='Image size: c')
    size_label.grid(column=0, row=20, columnspan=2, sticky=W)

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
