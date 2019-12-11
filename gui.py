from tkinter import *
from tkinter import ttk, filedialog
from zipfile36 import ZipFile
import os
import numpy as np
import io
from PIL import Image, ImageTk
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from skimage import io as skio
from en_de_code import image_to_b64, b64_to_image
import zipfile
from io import BytesIO
import base64


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
        # validate user
        user_id = {'user_id': '{}'.format(username.get())}
        # from GUI_client import validate_user
        # exist = validate_user(user_id)
        # # if exist ==

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
    # canvas = Canvas(root)
    # scrollbar = ttk.Scrollbar(root, orient="v", command=canvas.yview)
    # scrollbar.grid(row=0, column=8, rowspan=22, sticky='ns')

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

    # Select files to upload
    def select_img():
        # open local directory
        root.file = filedialog.askopenfilename(multiple=True, filetypes=[
            ('Image files', '.png .jpg .jpeg .tif .zip',)])
        # save file names into a list
        filename_ls = []
        for i in root.file:
            filename = os.path.basename(i)
            filename_ls.append(filename)
        # check type of file selected
        root.type = ck_type(filename_ls)
        print(root.type)
        file_label = ttk.Label(root, text='...{}'.format(root.file[0][-30::]),
                               width=30)
        file_label.grid(column=2, row=3, columnspan=1, sticky=W)
        return

    def upload_img():
        print('uploading')
        from en_de_code import image_to_b64
        # check if multiple files are selected
        if root.type == 'multiple img':
            imgs = []
            for i in root.file:
                img_array = read_img(i)
                encoded_img_array = image_to_b64(img_array)[0]
                imgs.append(encoded_img_array)
        elif root.type == 'zip':
            # read zip files into numpy array
            imgs = []
            zip_ref = ZipFile(root.file[0], "r")
            # returns a list of file names in the archive
            directory = zip_ref.namelist()
            for i in directory:
                img_bytes = zip_ref.read(i)
                data = io.BytesIO(img_bytes)
                img = Image.open(data)
                img_array = np.uint8(img)
                encoded_img_array = image_to_b64(img_array)[0]
                imgs.append(encoded_img_array)
            # read non-zip files into numpy array
        elif root.type == 'img':
            img_array = read_img(root.file[0])
            imgs = [image_to_b64(img_array)[0]]
            show_imgs = plt.imshow(img_array)
        else:
            print('cannot upload. wrong files selected.')
            # Open a warning window
            file_warning()
# remember to change encoded_img_array to string when sending to server!!
# remember to also get size from image_to_b64
        return

    select_btn = ttk.Button(root, text='Select image file(s)',
                            command=select_img)
    select_btn.grid(column=1, row=3, sticky=W)
    upld_btn = ttk.Button(root, text='Upload',
                          command=upload_img)
    upld_btn.grid(column=3, row=3, sticky=E)

    # function for reading non-zip image file
    def read_img(img_path):
        img_array = np.uint8(np.array(Image.open(img_path)))
        return img_array

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
    botton3.grid(column=1, row=9, columnspan=1, sticky=W)
    botton4 = ttk.Radiobutton(root, text='Invert Image',
                              variable=process_opt,
                              value='Invert Image')
    botton4.grid(column=2, row=9, columnspan=1, sticky=W)

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
    process_btn.grid(column=3, row=10, columnspan=1, sticky=E)

    # Image Display frame
    display_label = ttk.Label(root, text='3. Display images and metadata')
    display_label.grid(column=6, row=1, columnspan=10, sticky=W)
    img_frame = ttk.Frame(root, height=500, width=700)
    # img_frame.pack()
    # img_frame.columnconfigure(2, weight=1)
    # img_frame.rowconfigure(2, weight=1)
    img_frame.grid(column=6, row=2, columnspan=10, rowspan=16)
    # processed image frame
    img_pro_frame = ttk.LabelFrame(img_frame, text='Processed Image',
                                   height=250, width=300)
    img_pro_frame.grid(column=1, row=1, columnspan=1)
    # original image frame
    img_orig_frame = ttk.LabelFrame(img_frame, text='Original Image',
                                    height=250, width=300)
    img_orig_frame.grid(column=2, row=1, columnspan=1)
    # histogram for processed image frame
    hist_pro_frame = ttk.LabelFrame(img_frame,
                                    text='Processed Img. Histogram',
                                    height=250, width=300)
    hist_pro_frame.grid(column=1, row=2, columnspan=1)
    # histogram for original image frame
    hist_pro_frame = ttk.LabelFrame(img_frame,
                                    text='Original Img. Histogram',
                                    height=250, width=300)
    hist_pro_frame.grid(column=2, row=2, columnspan=1)
    # previous/next frame

    prev_frame = ttk.Frame(root, height=600, width=10)
    prev_frame.grid(column=5, row=8)
    next_frame = ttk.Frame(root, height=600, width=10)
    next_frame.grid(column=16, row=8)

    # previous/next button
    def previous_img():
        print('get previous image from server')
        print('display images')
        return

    def next_img():
        print('get previous image from server')
        print('display images')
        return

    prev_btn = ttk.Button(prev_frame, text='<',
                          width=1, command=previous_img)
    prev_btn.grid(column=1, row=1)
    next_btn = ttk.Button(next_frame, text='>', width=1, command=next_img)
    next_btn.grid(column=1, row=1)

    # Download Section
    download_opt = StringVar(None, 'jpeg')
    download_label = ttk.Label(root, text='4. Select download format: ')
    download_label.grid(column=0, row=14, columnspan=2, sticky=W)

    download_cb = ttk.Combobox(root, textvariable=download_opt)
    download_cb.grid(column=1, row=16, sticky=E)
    download_cb["values"] = ("jpeg", "png", "tiff", "jpg")  # no jpg
    download_cb.state(['readonly'])

    def decode_down_img(img_decoded, size_img):
        img_decoded_list = []
        for num, i in enumerate(img_decoded):
            img_array = b64_to_image(img_decoded[num], tuple(size_img[num]))
            img_decoded_list.append(img_array)
        return img_decoded_list

    def if_multiple():
        from GUI_client import request_download_file
        encoded_json = request_download_file(username)
        size_img = encoded_json["size"]
        ori_en = encoded_json["raw_img"]
        process_en = encoded_json["processed_img"]
        orig_name = encoded_json["name"]
        ori_encoded = decode_down_img(ori_en, size_img)
        process_encoded = decode_down_img(process_en, size_img)
        if len(ori_encoded) > 1:
            root.file = filedialog. \
                asksaveasfilename(title='Download Image',
                                  defaultextension='.zip',
                                  initialdir='/',
                                  initialfile='Image.zip',
                                  filetypes=[('zip', '*.zip')])
            write_to_zip(ori_encoded, process_encoded, root.file, orig_name)
            return
        elif len(ori_encoded) == 1:
            root.file = filedialog. \
                asksaveasfilename(title='Download Image',
                                  defaultextension='.{}'.format(
                                      download_opt.get()),
                                  initialdir='/',
                                  initialfile='Image.{}'
                                  .format(download_opt.get()),
                                  filetypes=[(download_opt.get(), '*.{}'
                                              .format(download_opt.get()))])
            new_im = Image.fromarray(ori_encoded[0])
            new_im.save(root.file)
            new_im = Image.fromarray(process_encoded[0])
            path = os.path.dirname(root.file)
            file_n = os.path.basename(root.file)
            new_im.save("{}/{}{}".format(path, "processed_", file_n))
            return
        return

    # need encoded image, file_name
    def write_to_zip(ori_encoded, process_encoded, zip_file_name, orig_name):
        print("Creating archive: {:s}".format(zip_file_name))
        with zipfile.ZipFile(zip_file_name, mode="w") as zf:
            for num, i in enumerate(ori_encoded):
                n = orig_name[num]
                na = os.path.splitext(n)[0]
                plt.imshow(i)
                buf = io.BytesIO(i)
                plt.axis('off')
                plt.savefig(buf, bbox_inches='tight', pad_inches=0)
                plt.close()
                img_name = "{}.{}".format(na, download_opt.get())
                print("  Writing image {:s} in the archive".format(img_name))
                zf.writestr(img_name, buf.getvalue())
            for num, i in enumerate(process_encoded):
                n = orig_name[num]
                na = os.path.splitext(n)[0]
                plt.imshow(i)
                buf = io.BytesIO(i)
                plt.axis('off')
                plt.savefig(buf, bbox_inches='tight', pad_inches=0)
                plt.close()
                img_name = "{}{}.{}".format(na, "_processed",
                                            download_opt.get())
                print("  Writing image {:s} in the archive".format(img_name))
                zf.writestr(img_name, buf.getvalue())
            zf.close()

    download_btn = ttk.Button(root, text='Download', command=if_multiple)
    download_btn.grid(column=3, row=16, sticky=E)

    # back to login function at main window
    def back_to_login():
        root.destroy()
        login_window()
        return

    # back to login button
    back_to_login_btn = ttk.Button(root, text='Back to Login',
                                   command=back_to_login)
    back_to_login_btn.grid(column=14, row=19, sticky=E)

    # exit function at main window
    def exit():
        root.destroy()
        return

    # exit button
    exit_btn = ttk.Button(root, text='Exit',
                          command=exit)
    exit_btn.grid(column=15, row=19)

    # process info include uploaded/processing time and image size
    uptime_label = ttk.Label(root, text='Uploaded time: b')
    uptime_label.grid(column=7, row=18, columnspan=1, sticky=W)
    protime_label = ttk.Label(root, text='Processsing time: a')
    protime_label.grid(column=11, row=18, columnspan=1, sticky=W)
    size_label = ttk.Label(root, text='Image size: c')
    size_label.grid(column=14, row=18, columnspan=1, sticky=W)

    root.mainloop()
    return


# function to check type of file selected
def ck_type(filename):
    typ = ''
    if len(filename) != 1:
        for i in filename:
            if '.zip' in i:
                typ = 'zip and multiple'
            else:
                typ = 'multiple img'
    else:
        if '.zip' in filename[0]:
            typ = 'zip'
        else:
            typ = 'img'
    return typ


def user_data_window():
    root = Tk()
    root.title('Your User Data Summary')
    data_label = Label(root,
                       text='You have done ** things # number of times')
    data_label.grid(column=0, row=1)
    root.mainloop()
    return


def file_warning():
    root = Toplevel()
    root.title('Please select another set of files')

    original = Image.open("warning.jpg")
    resized = original.resize((30, 30), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(resized)
    panel = Canvas(root, width=30, height=30)
    panel.create_image(0, 0, image=image, anchor=NW, tags="IMG")
    panel.grid(column=1, row=1)

    warn_label1 = Label(root, text='You can either upload multiple image '
                                   'files(.jpg .jpeg .png .tif) '
                                   'or a single ZIP archive file. '
                                   'Not both.')
    warn_label1.grid(column=2, row=1, columnspan=1)

    root.mainloop()
    return


if __name__ == '__main__':
    login_window()
    # file_warning()
