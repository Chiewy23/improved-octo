from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

DEFAULT_BAR_COLOUR = "#696969"
DEFAULT_WIDTH = 4

CHARACTER_DIC = {
    'a': 'α',
    'b': 'β',
    'g': 'γ',
    'd': 'δ',
    'e': 'ε',
    'z': 'ζ',
    '@': 'η',
    '£': 'θ',
    'i': 'ι',
    'k': 'κ',
    'l': 'λ',
    'm': 'μ',
    'n': 'ν',
    '$': 'ξ',
    'o': 'ο',
    'p': 'π',
    'r': 'ρ',
    's': 'σ/ς',
    't': 'τ',
    'u': 'υ',
    '¢': 'φ',
    'x': 'χ',
    '%': 'ψ',
    '^': 'ω',
    'space': ' '
}


def info_about():
    messagebox.showinfo("About Didactic Tribble", "Created using Python.")


class TextEditor:
    def __init__(self, _root):
        self.root = _root
        self.root.title("Didactic Tribble")
        self.root.geometry("1200x700+200+150")
        self.filename = None
        self.title = StringVar()
        self.status = StringVar()

        # ##### TITLE BAR #####
        self.title_bar = Label(
            self.root,
            textvariable=self.title,
            font=("Helvetica", 15, "bold"),
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
            font=("Helvetica", 15, "bold"),
            bd=1,
            relief=GROOVE,
            bg=DEFAULT_BAR_COLOUR,
            height=2
        )

        self.status_bar.pack(side=BOTTOM, fill=BOTH)
        self.status.set("Welcome To Didactic Tribble")

        # ##### MENU BAR #####
        self.menu_bar = Menu(
            self.root,
            font=("Helvetica", 15, "bold"),
            activebackground="white"
        )

        self.root.config(menu=self.menu_bar)

        # ##### FILE MENU #####
        self.file_menu = Menu(
            self.menu_bar,
            font=("Helvetica", 12, "bold"),
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
            font=("Helvetica", 12, "bold"),
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
            font=("Helvetica", 12, "bold"),
            activebackground="white",
            tearoff=0
        )

        self.help_menu.add_command(label="About", command=info_about)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

        # ##### SCROLLBAR & TEXT AREA #####
        scroll_y = Scrollbar(self.root, orient=VERTICAL)
        self.text_area_english = Text(
            self.root,
            yscrollcommand=scroll_y.set,
            font=("Helvetica", 15),
            state="normal",
            relief=GROOVE,
            bg="white",
            fg="black",
            insertbackground="black"
        )

        scroll_y_greek = Scrollbar(self.root, orient=VERTICAL)
        self.text_area_greek = Text(
            self.root,
            yscrollcommand=scroll_y_greek.set,
            font=("Helvetica", 15),
            state="normal",
            relief=GROOVE,
            bg="white",
            fg="black",
            insertbackground="black"
        )

        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y_greek.pack(side=RIGHT, fill=Y)

        scroll_y.config(command=self.text_area_english.yview)
        scroll_y_greek.config(command=self.text_area_greek.yview())

        self.text_area_english.pack(fill=BOTH, expand=1)
        self.text_area_greek.pack(fill=BOTH, expand=1)

        self.shortcuts()
        self.character_reader()

    def on_press(self, event):
        character = CHARACTER_DIC.get(event.keysym, "INVALID")

        if character != "INVALID":
            self.text_area_greek.insert(END, character)

    def set_title(self):
        if self.filename:
            self.title.set(self.filename)
        else:
            self.title.set("Untitled")

    def new_file(self):
        self.text_area_english.delete("1.0", END)
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
                self.text_area_english.delete("1.0", END)
                for line in infile:
                    self.text_area_english.insert(END, line)
                infile.close()
                self.set_title()
                self.status.set("Opened Successfully")
        except Exception as e:
            messagebox.showerror("Exception", str(e))

    def save_file(self):
        try:
            if self.filename:
                data = self.text_area_english.get("1.0", END)
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

            data = self.text_area_english.get("1.0", END)
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
        self.text_area_english.event_generate("<<Cut>>")

    def copy(self):
        self.text_area_english.event_generate("<<Copy>>")

    def paste(self):
        self.text_area_english.event_generate("<<Paste>>")

    def undo(self):
        try:
            if self.filename:
                self.text_area_english.delete("1.0", END)
                infile = open(self.filename, "r")
                for line in infile:
                    self.text_area_english.insert(END, line)
                infile.close()
                self.set_title()
                self.status.set("Undone Successfully")
            else:
                self.text_area_english.delete("1.0", END)
                self.filename = None
                self.set_title()
                self.status.set("Undone Successfully")
        except Exception as e:
            messagebox.showerror("Exception", str(e))

    def shortcuts(self):
        self.text_area_english.bind("<Control-n>", self.new_file)
        self.text_area_english.bind("<Control-o>", self.open_file)
        self.text_area_english.bind("<Control-s>", self.save_file)
        self.text_area_english.bind("<Control-a>", self.save_as_file)
        self.text_area_english.bind("<Control-e>", self.exit)
        self.text_area_english.bind("<Control-x>", self.cut)
        self.text_area_english.bind("<Control-c>", self.copy)
        self.text_area_english.bind("<Control-v>", self.paste)
        self.text_area_english.bind("<Control-u>", self.undo)

    def character_reader(self):
        self.text_area_english.bind('<KeyPress>', self.on_press)


def main():
    root = Tk()
    TextEditor(root)
    root.mainloop()


if __name__ == '__main__':
    main()
