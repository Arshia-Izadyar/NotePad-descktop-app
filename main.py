from tkinter import Menu, END, Tk
from datetime import datetime
from tkinter import messagebox, filedialog, simpledialog
from tkinter.scrolledtext import ScrolledText


class NotePad:
    def __init__(self):
        self.main = Tk()
        self.main.title("NotePad")
        self.main.resizable(False, False)

        self.notepad = ScrolledText(self.main, width=100, height=50)
        self.file_name = ''

        self.create_menu()

        self.notepad.pack()
        self.main.mainloop()

    def create_menu(self):
        notepad_menu = Menu(self.main)
        self.main.configure(menu=notepad_menu)

        file_menu = Menu(notepad_menu, tearoff=False)
        notepad_menu.add_cascade(label='File', menu=file_menu)

        file_menu.add_command(label='New', command=self.cmd_new)
        file_menu.add_command(label='Open ...', command=self.cmd_open)
        file_menu.add_command(label='Save', command=self.cmd_save)
        file_menu.add_command(label='Save as...', command=self.cmd_save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.cmd_exit)

        edit_menu = Menu(notepad_menu, tearoff=False)
        notepad_menu.add_cascade(label='Edit', menu=edit_menu)

        edit_menu.add_command(label="Cut", command=self.cmd_cut)
        edit_menu.add_command(label="Copy", command=self.cmd_copy)
        edit_menu.add_command(label="Paste", command=self.cmd_paste)
        edit_menu.add_command(label="Delete", command=self.cmd_clear)
        edit_menu.add_separator()
        edit_menu.add_command(label="Find", command=self.cmd_find)
        edit_menu.add_separator()
        edit_menu.add_command(label="SelectAll", command=self.cmd_select_all)

    def cmd_new(self):
        if len(self.notepad.get('1.0', END + '-1c')) > 0:
            if messagebox.askyesno("Notepad", "Do you want to save?"):
                self.cmd_save()
            else:
                self.notepad.delete(0.0, END)
            self.main.title("NotePad")

    def cmd_open(self):
        file_dialog = filedialog.askopenfile(parent=self.main, mode='r')
        text = file_dialog.read()
        self.notepad.delete(0.0, END)
        self.notepad.insert(0.0, text)

    def cmd_save(self):
        file_dialog = filedialog.asksaveasfile(mode='w', defaultextension='.txt')
        if file_dialog is not None:
            text = self.notepad.get('1.0', END)
            try:
                file_dialog.write(text)
            except:
                messagebox.showerror(title="Error", message="Not able to save!")

    def cmd_save_as(self):
        file_dialog = filedialog.asksaveasfile(mode='w', defaultextension='.txt')
        text = self.notepad.get('1.0', END)
        try:
            file_dialog.write(text)
        except:
            messagebox.showerror(title="Error", message="Can't save file!")

    def cmd_exit(self):
        if messagebox.askyesno("Notepad", "Are you sure you want to exit?"):
            self.main.destroy()

    def cmd_cut(self):
        self.notepad.event_generate("<<Cut>>")

    def cmd_copy(self):
        self.notepad.event_generate("<<Copy>>")

    def cmd_paste(self):
        self.notepad.event_generate("<<Paste>>")

    def cmd_clear(self):
        self.notepad.event_generate("<<Clear>>")

    def cmd_select_all(self):
        self.notepad.event_generate("<<SelectAll>>")

    def cmd_find(self):
        self.notepad.tag_remove("Found", '1.0', END)
        find = simpledialog.askstring("Find", "Find what:")
        if find:
            idx = '1.0'
            while True:
                idx = self.notepad.search(find, idx, nocase=1, stopindex=END)
                if not idx:
                    break
                lastdex = '%s+%dc' % (idx, len(find))
                self.notepad.tag_add("Found", idx, lastdex)
                idx = lastdex
                self.notepad.tag_config("Found", foreground='white', background='red')
                self.notepad.bind("<1>", self.click)

    def click(self):
        self.notepad.tag_config('Found', background='white', foreground='black')

    def cmd_time_date(self):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        label = messagebox.showinfo("Time/Date", dt_string)


notepad = NotePad()
