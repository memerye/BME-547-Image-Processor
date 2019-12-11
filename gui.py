from tkinter import *
from tkinter import ttk, filedialog
from zipfile36 import ZipFile
import os
import io
from PIL import Image, ImageTk
import matplotlib.image as mpimg
import numpy as np
from skimage import io as skio
from skimage import exposure
from time import time
import matplotlib.pyplot as plt
from en_de_code import image_to_b64, b64_to_image
import zipfile
from io import BytesIO
import base64
"""
Gui is the graphical user interface
for the image processor. The user will
first be asked to login or create a new
account which will be used to track the
user's history. After connected to a
specific account, the user will enter the
main window to upload, process, and download
images.

Author: Lucy Liang, Xiaoyu Qi,
Liangyu Xu, Ling Zhong.
"""


# User login/create account
def login_window():
    """
    The window created for login

    If a new user want to log in to the image processor,
    the input of the id is needed. If this id has existed
    in the database, the user would be inform in the window.
    While an old user, who has created the account before,
    can access the image processor by inputting the id in
    the box.

    Returns:
        None
    """
    root = Tk()
    root.title('Create Account/User Login')
    from GUI_client import request_check_id, post_user_id

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
        """
        This is the button that can create the account.

        Returns:
            None
        """
        # validate user
        if username.get() == '':
            id_error_label = Label(root,
                                   text='Please enter a username. ')
            id_error_label.grid(column=1, row=3, columnspan=3)
        else:
            user_id = {'user_id': username.get()}
            from GUI_client import request_check_id, post_user_id
            exist = request_check_id(username.get())
            if exist:
                exist_label = Label(root,
                                    text='Username already exists. '
                                         'Login or enter a new username.')
                exist_label.grid(column=1, row=3, columnspan=3)
            else:
                post_user_id(user_id)
                root.destroy()
                print('Account created successfully.')
                main_window(username.get())
        return

    ca_btn = ttk.Button(root, text='Create Account', command=create_account)
    ca_btn.grid(column=1, row=4)

    # Login button
    def login():
        """
        This is the button that used to log in to the image processor.

        Returns:
            None
        """
        if username.get() == '':
            id_error_label = Label(root,
                                   text='Please enter a username. ')
            id_error_label.grid(column=1, row=3, columnspan=3)
        else:
            exist = request_check_id(username.get())
            if exist:
                # open main window
                root.destroy()
                main_window(username.get())
            else:
                exist_label = Label(root,
                                    text='Username does not exist. '
                                         'Please create an account.')
                exist_label.grid(column=1, row=3, columnspan=3)
        return

    login_btn = ttk.Button(root, text='Login', command=login)
    login_btn.grid(column=2, row=4)

    root.mainloop()
    return


# Main window
def main_window(username):
    """
    This is the main window for the image processor that
    allows to process image(s) in multiple way.

    Args:
        username (string): The user name of the account.

    Returns:
        None
    """
    global raw_images, sizes, names
    raw_images = []
    sizes = []
    names = []
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
        """
        Show the user data

        The data includes:
        (1) user id
        (2) how many images have been uploaded
        (3) the total number of times of the various image processing steps.

        Returns:
            None
        """
        print('Get data summary from database')
        from GUI_client import request_user_info
        user_info = request_user_info(username)
        user_data_window(user_info)
        return

    user_data_btn = ttk.Button(root, text='View my user data',
                               command=user_data)
    user_data_btn.grid(column=3, row=1)

    # Images upload/choose from history
    action_label = ttk.Label(root, text='1. Choose an action to begin: ')
    action_label.grid(column=0, row=3, columnspan=2, sticky=W)

    # Select files to upload
    def select_img():
        """
        Select the files to upload.

        The user can select either "png", "jpg", "jpeg", "tif" or "zip"
        type of one image, list of images, or a zip archive of images.

        Returns:
            None
        """
        # open local directory
        root.file = filedialog.askopenfilename(multiple=True, filetypes=[
            ('Image files', '.png .jpg .jpeg .tif .zip',)])
        # save file names into a list
        root.filename_ls = []
        for i in root.file:
            filename = os.path.basename(i)
            root.filename_ls.append(filename)
        # check type of file selected
        root.type = ck_type(root.filename_ls)
        print(root.type)
        file_label = ttk.Label(root, text='...{}'.format(root.file[0][-30::]),
                               width=30)
        file_label.grid(column=2, row=4, columnspan=1, sticky=W)

    def upload_img():
        """
        Upload the image to database

        Returns:
            None
        """
        uploading_label = ttk.Label(root, text='Uploading ... ', width=30)
        uploading_label.grid(column=2, row=4, columnspan=1, sticky=W)
        root.imgs = []
        root.image_sizes = []
        from en_de_code import image_to_b64
        # check if multiple files are selected
        if root.type == 'multiple img':
            root.imgs = []
            root.image_sizes = []
            for i in root.file:
                img_array = read_img(i)
                encoded_img_array, image_size = image_to_b64(img_array)
                root.imgs.append(encoded_img_array)
                root.image_sizes.append(image_size)
        elif root.type == 'zip':
            # read zip files into numpy array
            root.imgs = []
            root.image_sizes = []
            zip_ref = ZipFile(root.file[0], "r")
            # returns a list of file names in the archive
            directory = zip_ref.namelist()
            for i in directory:
                img_bytes = zip_ref.read(i)
                data = io.BytesIO(img_bytes)
                img = Image.open(data)
                img_array = np.uint8(img)
                encoded_img_array, image_size = image_to_b64(img_array)
                root.image_sizes.append(image_size)
                root.imgs.append(encoded_img_array)
            # read non-zip files into numpy array
        elif root.type == 'img':
            img_array = read_img(root.file[0])
            encoded_img_array, image_size = image_to_b64(img_array)
            root.imgs = [encoded_img_array]
            root.image_sizes = [image_size]
            show_imgs = plt.imshow(img_array)
        else:
            print('cannot upload. wrong files selected.')
            # Open a warning window
            file_warning()
            return None
        global raw_images, sizes, names
        raw_images = root.imgs
        sizes = root.image_sizes
        names = root.filename_ls
        info = post_img_json()
        from GUI_client import post_img_GUI
        post_img_GUI(info)
        uploaded_label = ttk.Label(root, text='Upload complete. ', width=30)
        uploaded_label.grid(column=2, row=4, columnspan=1, sticky=W)
    select_btn = ttk.Button(root, text='Select image file(s)',
                            command=select_img)
    select_btn.grid(column=1, row=4, sticky=W)
    upld_btn = ttk.Button(root, text='Upload',
                          command=upload_img)
    upld_btn.grid(column=3, row=4, sticky=E)

    def post_img_json():
        """
       function to write json file
        for post image.

        Args:
            None
        Returns:
            post_img(dictionary): dictionary
            contain the info needed for post
            upload image info.
        """
        global raw_images, sizes, names
        post_img = {}
        post_img["user_id"] = username
        post_img["image"] = raw_images
        post_img["name"] = names
        post_img["size"] = sizes
        return post_img

    # function for reading non-zip image file
    def read_img(img_path):
        """
        Function for reading non-zip image file

        Args:
            img_path (string): The path of the image

        Returns:
            ndarray: the image is read as ndarray
        """
        print(Image.open(img_path).size)
        img_array = np.uint8(np.array(Image.open(img_path)))
        return img_array

    # History button
    def proc_history():
        """
        Create the history button

        Returns:
            None
        """
        # 1/time.../image.../operation
        from GUI_client import request_history_info
        history_info = request_history_info(username)
        hist_ls = []
        for i in range(len(history_info['name'])):
            op = cvt_proc_index(history_info['operation'][i])
            hist = '{}/{}/{}/{}' \
                .format(i + 1,
                        history_info['processed_time'][i],
                        op,
                        history_info['name'][i])
            hist_ls.append(hist)
        hist_tuple = tuple(hist_ls)
        # outputs history into pull down menu
        hist_combo['values'] = hist_tuple
        return

    hist_btn = ttk.Button(root, text='Choose from history',
                          command=proc_history)
    hist_btn.grid(column=1, row=5, sticky=W)

    # History pull down
    history = StringVar()
    hist_combo = ttk.Combobox(root, textvariable=history)
    hist_combo.grid(column=2, row=5, sticky=W)
    hist_combo.state(['readonly'])

    # Retrieve selected history info
    def retrieve():
        """
        function to retrieve image
        data from history.

        Args:
            None

        Returns:
            None
        """
        print(int(history.get()[0]))
        from GUI_client import request_one_history_info
        from en_de_code import b64_to_image
        root.one_history = request_one_history_info(username,
                                                    int(history.get()[0]))
        ls = []
        for i in range(len(root.one_history['name'])):
            print(i)
            hist_imgs = '{}/history: {}' \
                .format(i + 1,
                        root.one_history['name'][i])
            ls.append(hist_imgs)
        hist_tuple = tuple(ls)
        print(hist_tuple)
        # outputs history into pull down menu
        hist_display_combo['values'] = hist_tuple
        return

    retrieve_btn = ttk.Button(root, text='Retrieve', command=retrieve)
    retrieve_btn.grid(column=3, row=5, sticky=E)

    # process option
    process_opt = StringVar(None, 'Histogram Equalization')
    pro_label = ttk.Label(root, text='2. Choose a process option: ')
    pro_label.grid(column=0, row=7, columnspan=2, sticky=W)

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
        """
        Get the user selected processing method from GUI

        Returns:
            None
        """
        print('Process {} requested'.format(process_opt.get()))
        if process_opt.get() == 'Histogram Equalization':
            option = 0
            print("he")
        elif process_opt.get() == 'Contrast Stretching':
            option = 1
            print("cs")
        elif process_opt.get() == 'Log Compression':
            option = 2
            print("lc")
        elif process_opt.get() == 'Invert Image':
            option = 3
            print("ii")
        from GUI_client import post_process_opt,\
            request_recent_process_images
        opt_info = post_opt_json(option)
        post_process_opt(opt_info)
        root.recent_process = request_recent_process_images()
        ls = []
        for i in range(len(root.recent_process['name'])):
            print(i)
            hist_imgs = '{}/iupload: {}' \
                .format(i + 1,
                        root.recent_process['name'][i])
            ls.append(hist_imgs)
        hist_tuple = tuple(ls)
        # outputs history into pull down menu
        hist_display_combo['values'] = hist_tuple
        print(opt_info)
        return option

    # Process button
    process_btn = ttk.Button(root, text='Process', command=process)
    process_btn.grid(column=3, row=8, columnspan=1, sticky=E)

    def post_opt_json(option):
        """
        function to write json file
        for image process option.

        Args:
            option(int):
                0: Histogram Equalization
                1: Contrast Stretching
                2: Log Compression
                3: Invert Image

        Returns:
            post_opt(dictionary): dictionary
            contain the info needed for post
            process image info.
        """
        global raw_images, sizes, names
        post_opt = {"user_id": username,
                    "operation": option,
                    "raw_img": raw_images,
                    "size": sizes,
                    "name": names}
        return post_opt

    # Image Display
    display_label = ttk.Label(root, text='3. Display images and metadata')
    display_label.grid(column=0, row=11, columnspan=2, sticky=W)
    # root.img_frame = ttk.Frame(root, height=600, width=600)
    # root.img_frame.grid(column=6, row=2, columnspan=10, rowspan=16)

    hist_display = StringVar()
    hist_display_combo = ttk.Combobox(root, textvariable=hist_display)
    hist_display_combo.grid(column=1, row=12)
    hist_display_combo.state(['readonly'])

    def image_display():
        """
        function to select
        display image.

        Args:
            None

        Returns:
            None
        """
        ind = int(hist_display.get()[0])
        if hist_display.get()[2:9] == 'history':
            act = root.one_history
        else:
            act = root.recent_process
        process_info = display_info(ind-1, act)
        image_display_window(ind, act,
                             process_info)
        return

    process_btn = ttk.Button(root, text='Display',
                             command=image_display)
    process_btn.grid(column=3, row=12, columnspan=1, sticky=E)

    # Download Section
    download_opt = StringVar(None, 'jpeg')
    download_label = ttk.Label(root, text='4. Select download format: ')
    download_label.grid(column=0, row=14, columnspan=2, sticky=W)

    download_cb = ttk.Combobox(root, textvariable=download_opt)
    download_cb.grid(column=1, row=15, sticky=E)
    download_cb["values"] = ("jpeg", "png", "tiff", "jpg")  # no jpg
    download_cb.state(['readonly'])

    def decode_down_img(img_decoded, size_img):
        """
        function to decode image.

        Args:
            img_decoded(list):list of
            numpy array of decoded image.
            size_img(list): size of the image

        Returns:
            img_decoded_list(list):list
            of numpy array of decoded image.
        """
        img_decoded_list = []
        for num, i in enumerate(img_decoded):
            img_array = b64_to_image(img_decoded[num], tuple(size_img[num]))
            img_decoded_list.append(img_array)
        return img_decoded_list

    def if_multiple():
        """
        Write to zip if the downloaded images are multiple

        Returns:
            None
        """
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
        """
        Write multiple images into a zip

        Args:
            img_decoded (ndarray): the decoded images
            zip_file_name (string): the filename of zip

        Returns:
            None
        """
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
    download_btn.grid(column=3, row=15, sticky=E)

    # back to login function at main window
    def back_to_login():
        """
        The function that design to go back to login window

        Returns:
            None
        """
        root.destroy()
        login_window()
        return

    # back to login button
    back_to_login_btn = ttk.Button(root, text='Back to Login',
                                   command=back_to_login)
    back_to_login_btn.grid(column=2, row=17, sticky=E)

    # exit function at main window
    def exit():
        """
        The function that design to quit the image processor program.

        Returns:
            None
        """
        root.destroy()
        return

    # exit button
    exit_btn = ttk.Button(root, text='Exit',
                          command=exit)
    exit_btn.grid(column=3, row=17)

    # # process info include uploaded/processing time and image size
    # def process_info(ls):
    #     uptime_label = ttk.Label(root,
    #                              text='Uploaded time: {}'.format(ls[0]))
    #     uptime_label.grid(column=7, row=18, columnspan=1, sticky=W)
    #     protime_label = ttk.Label(root,
    #                               text='Processsing time: {}'.format(ls[1]))
    #     protime_label.grid(column=11, row=18, columnspan=1, sticky=W)
    #     size_label = ttk.Label(root,
    #                            text='Image size: {}'.format(ls[2]))
    #     size_label.grid(column=14, row=18, columnspan=1, sticky=W)
    #     return

    # gaps for aesthetic
    gap_row = Label(root, text='  ')
    gap_row.grid(column=0, row=0)

    gap_row2 = Label(root, text='  ')
    gap_row2.grid(column=0, row=2)

    gap_row3 = Label(root, text='  ')
    gap_row3.grid(column=0, row=6)

    gap_row4 = Label(root, text='  ')
    gap_row4.grid(column=0, row=10)

    gap_row5 = Label(root, text='  ')
    gap_row5.grid(column=0, row=13)

    gap_row6 = Label(root, text='  ')
    gap_row6.grid(column=0, row=16)

    gap_row7 = Label(root, text='  ')
    gap_row7.grid(column=0, row=18)

    gap_col = Label(root, text='  ')
    gap_col.grid(column=4, row=0)

    root.mainloop()
    return


# function to check type of file selected
def ck_type(filename):
    """
    Function to check type of file selected

    Args:
        filename (string): The name of the file

    Returns:
        string: the type of the file
    """
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


# function to convert process index to process name
def cvt_proc_index(index):
    """
    function that read the
    index of the selected process
    option and translate to method.

    Arg:
        index(int): image process option index (0,1,2,3)

    Returns:
        (string):
        'Histogram Equalization':
        process option
        'Contrast Stretching':
        process option
        'Log Compression':
        process option
        'Invert Image':
        process option
        False(boolean): return false
        if the index does not present any
        process options.
    """
    if index == 0:
        return 'Histogram Equalization'
    elif index == 1:
        return 'Contrast Stretching'
    elif index == 2:
        return 'Log Compression'
    elif index == 3:
        return 'Invert Image'
    else:
        return False


def plotimages(img_raw, img_processed):
    """
    function that plot the histogram
    on the display window.

    Arg:
        img_raw(ndarray): a uint8 array of the original
        image data received from server
        img_processed(ndarray): a uint8 array of the
        processed image data received from server

    Returns:
        hist_img(ndarray): an array of image with original and
        processed image with their corresponding histogram
    """
    color_list = ["r", "g", "b", "c", "m", "y", "k", "w"]
    n = img_raw.shape[2]
    fig = plt.figure()
    fig.tight_layout(pad=0)
    gs0 = fig.add_gridspec(2 * n, 2)
    ax1 = fig.add_subplot(gs0[0:3, 0])
    ax1.imshow(img_raw)
    ax1.set_title("Raw Image")
    ax1.set_axis_off()
    ax2 = fig.add_subplot(gs0[0:3, 1])
    ax2.imshow(img_processed)
    ax2.set_title("Processed Image")
    ax2.set_axis_off()
    for s1 in range(n):
        ax = fig.add_subplot(gs0[s1 + n, 0])
        img_hist, img_bins = exposure.histogram(img_raw[:, :, s1])
        ax.plot(img_bins, img_hist, color_list[s1])
        ax = fig.add_subplot(gs0[s1 + n, 1])
        img_hist, img_bins = exposure.histogram(img_processed[:, :, s1])
        ax.plot(img_bins, img_hist, color_list[s1])
    fig.canvas.draw()
    s, (w, h) = fig.canvas.print_to_buffer()
    # plt.show()
    hist_img = np.fromstring(fig.canvas.tostring_rgb(),
                             dtype="uint8").reshape((h, w, 3))
    return hist_img


def display_info(ind, act):
    """
    function that read upload and process
     time and image size from json.

    Arg:
        ind(int): index position of
        the displayed image in the
        image list.
        act(dictionary): the dictionary
        read from most_recent_post.

    Returns:
        uptime(string): timestamp when
        the image is uploaded.
        protime(float): seconds that
        the image need to process
        size_a(int): column of the image
        size_b(int): row of the image
    """
    global uptime, protime, size_a, size_b
    uptime = act["up_time"][ind]
    protime = act["run_time"][ind]
    imgsize = act["size"][ind]
    size_a = imgsize[0]
    size_b = imgsize[1]
    return uptime, protime, size_a, size_b


def image_display_window(ind, one_history, info):
    """
    Create the window that can display the
    original image and the processed image
    with its histogram.

    Returns:
        None
    """
    root = Toplevel()
    root.title('Display Images and Color Histograms')
    i = ind - 1
    from en_de_code import b64_to_image
    raw = b64_to_image(one_history['raw_img'][i],
                       one_history['size'][i])
    processed = b64_to_image(one_history['processed_img'][i],
                             one_history['size'][i])
    hist_img = plotimages(raw, processed)
    desired_size = 600
    img_obj = Image.fromarray(hist_img)
    old_size = img_obj.size
    ratio = float(desired_size) / max(old_size)
    new_size = tuple([int(x * ratio) for x in old_size])
    im = img_obj.resize(new_size, Image.ANTIALIAS)
    # create a new image and paste the resized on it
    new_im = Image.new("RGB", (desired_size, desired_size),
                       color=(255, 255, 255))
    new_im.paste(im, ((desired_size - new_size[0]) // 2,
                      (desired_size - new_size[1]) // 2))
    image = ImageTk.PhotoImage(new_im)
    panel = Canvas(root, width=600, height=600)
    panel.create_image(0, 0, image=image, anchor=NW, tags="IMG")
    panel.grid(column=0, row=0, columnspan=16)

    uptime_label = ttk.Label(root, text='Uploaded time: {}'.format(info[0]))
    uptime_label.grid(column=1, row=2, columnspan=2, sticky=W)
    protime_label = ttk.Label(root,
                              text='Processing time: {0:.5f}s'
                              .format(info[1]))
    protime_label.grid(column=7, row=2, columnspan=2, sticky=W)
    size_label = ttk.Label(root,
                           text='Image size: {}x{}'
                           .format(info[2], info[3]))
    size_label.grid(column=14, row=2, columnspan=2, sticky=W)
    root.mainloop()
    return


def user_data_window(user_info):
    """
    Create the window that can visualize the user information

    Returns:
        None
    """
    root = Tk()
    root.title('Your User Account Summary')
    data_label = Label(root,
                       text=' Time Created: '
                            '{} '.format(user_info['create_time']))
    data_label.grid(column=0, row=1, sticky=W)
    data_label = Label(root,
                       text=' Histogram Equalization: '
                            '{} '.format(user_info['histeq']))
    data_label.grid(column=0, row=2, sticky=W)
    data_label = Label(root,
                       text=' Contrast Stretching: '
                            '{} '.format(user_info['constr']))
    data_label.grid(column=0, row=3, sticky=W)
    data_label = Label(root,
                       text=' Log Compression: '
                            '{} '.format(user_info['logcom']))
    data_label.grid(column=0, row=4, sticky=W)
    data_label = Label(root,
                       text=' Invert Image: '
                            '{} '.format(user_info['invert']))
    data_label.grid(column=0, row=5, sticky=W)
    root.mainloop()
    return


def file_warning():
    """
    Create the window that gives the warning message
        when the user wrongly select the type of the image(s).

    Returns:
        None
    """
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
    # main_window('1_a')
    login_window()
    # file_warning()
