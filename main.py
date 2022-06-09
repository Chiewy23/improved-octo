from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

import character_sets.greek as greek

'''
TO-DO:
- Add accented options for letters.
- Replaced duplicate config values with global settings.
- Extract code/methods (general refactor).
- Add help options to menu for character set.
- Remove redundant code.
- Unit tests.
- Styling.
- Package and deployment.
'''

DEFAULT_BAR_COLOUR = "#696969"
DEFAULT_WIDTH = 4
DEFAULT_FONT_SIZE = 15
DEFAULT_FONT = "Helvetica"
DEFAULT_FONT_STYLE = "bold"


def info_about():
    messagebox.showinfo("About Octo", "Created using Python.")


class TextEditor:
    def __init__(self, _root):
        self.root = _root
        self.root.title("Octo")
        self.root.geometry("1200x700+200+150")
        self.filename = None
        self.title = StringVar()
        self.status = StringVar()

        # ##### TITLE BAR #####
        self.title_bar = Label(
            self.root,
            textvariable=self.title,
            font=(DEFAULT_FONT, DEFAULT_FONT_SIZE, DEFAULT_FONT_STYLE),
            bd=1,
            relief=GROOVE,
            bg=DEFAULT_BAR_COLOUR,
            height=2
        )

        self.title_bar.pack(side=TOP, fill=BOTH)
        self.set_title()

        # ##### STATUS BAR #####
        self.status_bar = Label(
            self.root,
            textvariable=self.status,
            font=(DEFAULT_FONT, DEFAULT_FONT_SIZE, DEFAULT_FONT_STYLE),
            bd=1,
            relief=GROOVE,
            bg=DEFAULT_BAR_COLOUR,
            height=2
        )

        self.status_bar.pack(side=BOTTOM, fill=BOTH)
        self.status.set("Welcome To Octo")

        # ##### MENU BAR #####
        self.menu_bar = Menu(
            self.root,
            font=(DEFAULT_FONT, DEFAULT_FONT_SIZE, DEFAULT_FONT_STYLE),
            activebackground="white"
        )

        self.root.config(menu=self.menu_bar)

        # ##### FILE MENU #####
        self.file_menu = Menu(
            self.menu_bar,
            font=(DEFAULT_FONT, DEFAULT_FONT_SIZE, DEFAULT_FONT_STYLE),
            activebackground="white",
            tearoff=0
        )

        self.file_menu.add_command(label="New", accelerator="Ctrl+N", command=self.new_file)
        self.file_menu.add_command(label="Open", accelerator="Ctrl+O", command=self.open_file)
        self.file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.save_file)
        self.file_menu.add_command(label="Save As", accelerator="Ctrl+A", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", accelerator="Ctrl+E", command=self.exit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # ##### EDIT MENU #####
        self.edit_menu = Menu(
            self.menu_bar,
            font=(DEFAULT_FONT, DEFAULT_FONT_SIZE, DEFAULT_FONT_STYLE),
            activebackground="white",
            tearoff=0
        )

        self.edit_menu.add_command(label="Cut", accelerator="Ctrl+X", command=self.cut)
        self.edit_menu.add_command(label="Copy", accelerator="Ctrl+C", command=self.copy)
        self.edit_menu.add_command(label="Paste", accelerator="Ctrl+V", command=self.paste)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Undo", accelerator="Ctrl+U", command=self.undo)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        # ##### HELP MENU #####
        self.help_menu = Menu(
            self.menu_bar,
            font=(DEFAULT_FONT, DEFAULT_FONT_SIZE, DEFAULT_FONT_STYLE),
            activebackground="white",
            tearoff=0
        )

        self.help_menu.add_command(label="About", command=info_about)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

        # ##### SCROLLBAR & TEXT AREA #####
        scroll_y = Scrollbar(self.root, orient=VERTICAL)
        self.text_area_input = Text(
            self.root,
            yscrollcommand=scroll_y.set,
            font=(DEFAULT_FONT, DEFAULT_FONT_SIZE),
            state="normal",
            relief=GROOVE,
            bg="white",
            fg="black",
            insertbackground="black"
        )

        scroll_y_output = Scrollbar(self.root, orient=VERTICAL)
        self.text_area_output = Text(
            self.root,
            yscrollcommand=scroll_y_output.set,
            font=(DEFAULT_FONT, DEFAULT_FONT_SIZE),
            state="normal",
            relief=GROOVE,
            bg="white",
            fg="black",
            insertbackground="black"
        )

        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y_output.pack(side=RIGHT, fill=Y)

        scroll_y.config(command=self.text_area_input.yview)
        scroll_y_output.config(command=self.text_area_output.yview())

        self.text_area_input.pack(fill=BOTH, expand=1)
        self.text_area_output.pack(fill=BOTH, expand=1)

        self.shortcuts()
        self.character_reader()

    def on_press(self, event):
        character = greek.CHARACTER_SET.get(event.keysym, "INVALID")

        if character != "INVALID":
            self.text_area_output.insert(END, character)

    def set_title(self):
        if self.filename:
            self.title.set(self.filename)
        else:
            self.title.set("Untitled")

    def new_file(self):
        self.text_area_input.delete("1.0", END)
        self.filename = None
        self.set_title()
        self.status.set("New File Created")

    def open_file(self):
        try:
            self.filename = filedialog.askopenfilename(
                title="Select file",
                filetypes=(("All Files", "*.*"), ("Text Files", "*.txt"), ("Python Files", "*.py"))
            )

            if self.filename:
                infile = open(self.filename, "r")
                self.text_area_input.delete("1.0", END)
                for line in infile:
                    self.text_area_input.insert(END, line)
                infile.close()
                self.set_title()
                self.status.set("Opened Successfully")
        except Exception as e:
            messagebox.showerror("Exception", str(e))

    def save_file(self):
        try:
            if self.filename:
                data = self.text_area_input.get("1.0", END)
                outfile = open(self.filename, "w")
                outfile.write(data)
                outfile.close()
                self.set_title()
                self.status.set("Saved Successfully")
            else:
                self.save_as_file()
        except Exception as e:
            messagebox.showerror("Exception", str(e))

    def save_as_file(self):
        try:
            untitled_file = filedialog.asksaveasfilename(
                title="Save file As",
                defaultextension=".txt",
                initialfile="Untitled.txt",
                filetypes=(("All Files", "*.*"), ("Text Files", "*.txt"), ("Python Files", "*.py"))
            )

            data = self.text_area_input.get("1.0", END)
            outfile = open(untitled_file, "w")
            outfile.write(data)
            outfile.close()
            self.filename = untitled_file
            self.set_title()
            self.status.set("Saved Successfully")
        except Exception as e:
            messagebox.showerror("Exception", str(e))

    def exit(self):
        op = messagebox.askyesno("WARNING", "Your Unsaved Data May be Lost!!")
        if op > 0:
            self.root.destroy()
        else:
            return

    def cut(self):
        self.text_area_input.event_generate("<<Cut>>")

    def copy(self):
        self.text_area_input.event_generate("<<Copy>>")

    def paste(self):
        self.text_area_input.event_generate("<<Paste>>")

    def undo(self):
        try:
            if self.filename:
                self.text_area_input.delete("1.0", END)
                infile = open(self.filename, "r")
                for line in infile:
                    self.text_area_input.insert(END, line)
                infile.close()
                self.set_title()
                self.status.set("Undone Successfully")
            else:
                self.text_area_input.delete("1.0", END)
                self.filename = None
                self.set_title()
                self.status.set("Undone Successfully")
        except Exception as e:
            messagebox.showerror("Exception", str(e))

    def shortcuts(self):
        self.text_area_input.bind("<Control-n>", self.new_file)
        self.text_area_input.bind("<Control-o>", self.open_file)
        self.text_area_input.bind("<Control-s>", self.save_file)
        self.text_area_input.bind("<Control-a>", self.save_as_file)
        self.text_area_input.bind("<Control-e>", self.exit)
        self.text_area_input.bind("<Control-x>", self.cut)
        self.text_area_input.bind("<Control-c>", self.copy)
        self.text_area_input.bind("<Control-v>", self.paste)
        self.text_area_input.bind("<Control-u>", self.undo)

    def character_reader(self):
        self.text_area_input.bind('<KeyPress>', self.on_press)


def main():
    root = Tk()
    TextEditor(root)
    root.mainloop()


if __name__ == '__main__':
    main()
