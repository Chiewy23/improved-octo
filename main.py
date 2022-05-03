# Tkinter - Top create the GUI.
# PIL (Python Image Library) - To give the GUI window an icon.
# OS - To get the file path.

# python -m pip install pillow

from tkinter import *
import tkinter.filedialog as fd
import tkinter.messagebox as mb

from PIL import Image, ImageTk
import os


def open_file():
    file = fd.askopenfile(defaultextension=".txt", filetypes=[("All types", "*.*"), ("Text File", "*.txt*")])

    if file != "":
        root.title(f"{os.path.basename(file)}")
        text_area.delete(1.0, END)
        with open(file, "r") as file_:
            text_area.insert(1.0, file_.read())
            file_.close()
    else:
        file = None


def open_new_file():
    root.title("Untitled - Didactic Tribble")
    text_area.delete(1.0, END)


def save_file():
    global text_area
    file = text_area.get(1.0, END)

    if file != "":
        file = open(file, "w")
        file.write(text_area.get(1.0, END))
        file.close()
    else:
        file = None

    if file is None:
        file = fd.asksaveasfilename(initialfile="Untitled.txt", defaultextension=".txt", filetypes=[("Text File", "*.txt*"), ("Word Document", '*,docx*'), ("PDF", "*.pdf*")])
    else:
        file = open(file, "w")
        file.write(text_area.get(1.0, END))
        file.close()
        root.title(f"{os.path.basename(file)} - Didactic Tribble")


def exit_application():
    root.destroy()


def copy_text():
    text_area.event_generate("<<Copy>>")


def cut_text():
    text_area.event_generate("<<Cut>>")


def paste_text():
    text_area.event_generate("<<Paste>>")


def select_all():
    text_area.event_generate("Control-Keypress-A>>")


def delete_last_char():
    text_area.event_generate("<<KP_Delete>>")


def about_didactic_tribble():
    mb.showinfo("About Didactic Tribble", "One Tribble to rule them all.")


def about_commands():
    commands = """
    Under the File Menu:
    - 'New' clears the entire Text Area
    - 'Open' clears text and opens another file
    - 'Save As' - saves your file in the same/other extension
    
    Under the Edit Menu:
    - 'Copy' copies the selected text to your clipboard
    - 'Cut' cuts the selected text and removes it from the text area
    - 'Paste' pastes the copied/cut text
    - 'Select All' selects the entire text
    - 'Delete' deletes the last character
    """

    mb.showinfo(title="All commands", message=commands, width=60, height=40)


root = Tk()
root.title("Untitled - Didactic Tribble")
root.geometry("800x500")
root.resizable(0, 0)

# Specify the max. number of columns and rows available in the window.
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

icon = ImageTk.PhotoImage(Image.open("pi.png"))
root.iconphoto(False, icon)

root.update()
root.mainloop()

if __name__ == '__main__':
    print("Hello chickens...")