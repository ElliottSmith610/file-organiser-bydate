import os
from datetime import datetime as dt
import shutil
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.messagebox import askokcancel, showerror, showinfo

SOURCE = None
DESTINATION = None
NUM_FILES = 0


def file_sort(s_folder, d_folder):
    for file in os.listdir(s_folder):
        source = f"{s_folder}/{file}"
        if os.path.isdir(source):
            file_sort(source, DESTINATION)

        if os.path.isfile(source):
            create_time = os.path.getmtime(f"{s_folder}/{file}")
            date = dt.utcfromtimestamp(create_time)
            year, month, day = date.year, date.strftime("%B"), date.day

            destination = f"{d_folder}/{year}/{month}/{file}"

            try:
                # copy2 preserves metadata
                shutil.copy2(source, destination)
            except FileNotFoundError:
                try:
                    os.mkdir(f"{d_folder}/{year}/{month}")
                except FileNotFoundError:
                    os.mkdir(f"{d_folder}/{year}")
                    os.mkdir(f"{d_folder}/{year}/{month}")
                finally:
                    shutil.copy2(source, destination)
            except PermissionError:
                pass
            finally:
                global NUM_FILES
                NUM_FILES += 1


def select_source():
    global SOURCE, DESTINATION
    SOURCE = askdirectory()
    DESTINATION = f"{SOURCE}-Sorted"
    s = "/".join(SOURCE.split("/")[-3:])
    d = "/".join(DESTINATION.split("/")[-3:])
    source_text.config(text=s)
    dest_text.config(text=d)
    dest_button.grid(row=0, column=1, pady=(0, 20), padx=(10, 10))


def select_dest():
    global DESTINATION
    DESTINATION = f"{SOURCE}-Sorted"
    destination = askdirectory()
    if destination != "":
        DESTINATION = destination
        s = "/".join(SOURCE.split("/")[-1:])
        DESTINATION = f"{DESTINATION}/{s}-Sorted"
        d = "/".join(DESTINATION.split("/")[-3:])
        dest_text.config(text=d)


def go():
    if SOURCE is None or DESTINATION is None:
        showerror(title="Error", message="No folder selected")
    elif askokcancel(title="Confirm", message="Are you sure"):
        os.mkdir(DESTINATION)
        file_sort(SOURCE, DESTINATION)
        showinfo(title="Complete", message=f"Successfully moved {NUM_FILES} files.")


window = Tk()
window.maxsize(400, 200)
window.minsize(400, 200)
window.config(padx=30, pady=30)
source_button = Button(text="Select Folder", command=select_source)
dest_button = Button(text="Change Destination Folder", command=select_dest)
go_button = Button(text="Go!", command=go)
source_label = Label(text="       Source:")
dest_label = Label(text="Destination:")
source_text = Label(text="", justify=LEFT)
dest_text = Label(text="", justify=LEFT)

source_button.grid(row=0, column=0, pady=(0, 20))
go_button.grid(row=3, column=0, pady=(20, 0))
source_label.grid(row=1, column=0)
source_text.grid(row=1, column=1, columnspan=3)
dest_label.grid(row=2, column=0)
dest_text.grid(row=2, column=1, columnspan=3)

window.mainloop()
