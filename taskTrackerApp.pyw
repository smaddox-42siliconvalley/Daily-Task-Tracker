#####################################################################
#                                                                   #
#                                                                   #
#                                                                   #
#                   created by: smaddox                             #
#                                                                   #
#                   Purpose:                                        #
#                   This is file contains all of the code           #
#                   in this project. It creates and maintains       #
#                   a gui interface for tracking your everday       #
#                   tasks                                           #
#                                                                   #  
#####################################################################


import datetime
import webbrowser
import platform
import os
import shutil
import sys
import pickle
import tkinter as tk
from tkinter import messagebox

    
class app(tk.Tk):
    def __init__(self):
        self.now = datetime.datetime.now()
        self.date = str(self.now.year) + '-' + str(self.now.month) + '-' + str(self.now.day)
        self.f = open('config/tasks.txt', 'rb')
        try:
            self.tasks = pickle.load(self.f)
        except:
            self.tasks = []
        self.f.close()
        self.num_tasks = len(self.tasks)
        self.index = 0
        tk.Tk.__init__(self)
        self.geometry("600x400")
        container = tk.Frame(self)
        container.pack()
        self.frames = {}
        menu = amenu(self, self)
        for F in (newEntry, viewEntries):
            frame_name = F.__name__
            frame = F(container, self)
            self.frames[frame_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.show_frame("viewEntries")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def add_task(self, task):
        self.tasks.append(task)
        self.tasks.sort(key = lambda x: x.priority)
        self.num_tasks += 1

    def remove_task(self):
        if (self.num_tasks != 0):
            self.tasks.pop(self.index)
            self.index = 0
            self.num_tasks -= 1
        else:
            pass

    def get_help(self):
        if platform.system() == 'Windows':
            webbrowser.open("https://github.com/M3n3laus/Daily-Task-Tracker")
        elif platform.system() == 'Darwin':
            path = 'open -a /Applications/Safari.app %s'
            webbrowser.get(path).open("https://github.com/M3n3laus/Daily-Task-Tracker")
        self.show_frame("viewEntries")

    def getmeouttahere(self):
        self.f = open('config/tasks.txt', 'wb')
        pickle.dump(self.tasks, self.f)
        self.f.close()
        self.destroy()
        sys.exit(0)

    def generate_report(self):
        if len(self.tasks) == 0:
            messagebox.showinfo("Report Generator", "Nothing to report")
            return
        reportfile = open('reports/' + self.date + '.txt', 'w+')
        ontrack = 1
        perfect = 1
        
        for task in self.tasks:
            temp = 'Task: ' + task.title + '\nPriority level: ' + task.priority + '\nStatus: ' + task.status + '\nNotes: ' + task.notes + '\n\n'

            if task.priority == '1' and task.status == 'incomplete':
                ontrack = 0

            if task.priority != 3 and task.status == 'incomplete':
                perfect = 0

            reportfile.write(temp)

        if ontrack == 0:
            reportfile.write('On track: False\n')
        else:
            reportfile.write('On track: True\n')

        if perfect == 1:
            reportfile.write('Main tasks accomplished: True\n')
        else:
            reportfile.write('Main tasks accomplished: False\n')
        reportfile.close()   
        messagebox.showinfo("Report Generator", "Report Successfully generated")
        
class amenu(tk.Menu):
    def __init__(self, parent, controller):
        tk.Menu.__init__(self, parent)
        cascade_menu = tk.Menu(self, tearoff = 0)
        another_cascade_menu = tk.Menu(self, tearoff = 0)
        another_cascade_menu.add_command(label="Get Help", command = parent.get_help)
        cascade_menu.add_command(label="New Task", command = lambda: parent.show_frame("newEntry"))
        cascade_menu.add_command(label="Generate Report", command = parent.generate_report)
        self.add_cascade(label="File", menu = cascade_menu)
        self.add_cascade(label="Help", menu = another_cascade_menu)
        controller.config(menu = self)
        
    
    
class newtask:

    def __init__(self, title, rank, notes):
        self.title = title
        self.priority = rank
        self.notes = notes
        self.status = 'incomplete'

    def complete(self):
        if (self.status == 'complete'):
            self.status = 'incomplete'
        else:
            self.status = 'complete'

    def change_note(self, note):
        self.notes = note

    def rerank(self, rank):
        self.priority = rank


    
class viewEntries(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.title = tk.StringVar()
        self.priority = tk.StringVar()
        self.status = tk.StringVar()
        self.notes = tk.StringVar()

        self.label_frame = tk.Frame(self)
        button_frame = tk.Frame(self)
        
        title_label = tk.Label(self.label_frame, textvariable = self.title)
        priority_label = tk.Label(self.label_frame, textvariable = self.priority)
        self.label_frame.status_label = tk.Label(self.label_frame, textvariable = self.status)
        notes_label = tk.Label(self.label_frame, textvariable = self.notes)

        next_b = tk.Button(button_frame, text = "  next  ", command = self.next_button)
        prev_b = tk.Button(button_frame, text = "previous", command = self.prev_button)
        complete_b = tk.Button(button_frame, text = "toggle complete", command = self.complete_button)
        remove_b = tk.Button(button_frame, text = "remove task", fg = "red", command = self.remove_button)

        self.update_view()

        title_label.grid(row=0, column=1)
        priority_label.grid(row=1, column=1)
        notes_label.grid(row=2, column=1)
        self.label_frame.status_label.grid(row=3, column=1)
        next_b.grid(row=4, column=2, sticky='nesw', padx=10, pady=20)
        prev_b.grid(row=4, column=0, padx=10, pady=20)
        complete_b.grid(row=4, column=1, padx=10, pady=20)
        remove_b.grid(row =6, column=1, pady=10)

        self.label_frame.grid()
        button_frame.grid()

    def remove_button(self, *args):
        self.controller.remove_task()
        self.update_view(self)
        
    def complete_button(self, *args):
        if (self.controller.num_tasks > 0):
            self.controller.tasks[self.controller.index].complete()
            self.update_view(self)
        
    def next_button(self, *args):
        if (self.controller.num_tasks > 0):
            self.controller.index += 1
            self.controller.index %= self.controller.num_tasks
            self.update_view(self)

    def prev_button(self, *args):
        if (self.controller.num_tasks > 0):
            self.controller.index -= 1
            self.controller.index %= self.controller.num_tasks
            self.update_view(self)

        
    def update_view(self, *args):
        if (self.controller.num_tasks > 0):
            self.title.set("Title: " + self.controller.tasks[self.controller.index].title)
            self.priority.set("Priority: " + self.controller.tasks[self.controller.index].priority)
            self.status.set("Status: " + self.controller.tasks[self.controller.index].status)
            if self.controller.tasks[self.controller.index].status == 'complete':
                self.label_frame.status_label.config(fg="green")
            else:
                self.label_frame.status_label.config(fg="red")
            self.notes.set("Notes: " + self.controller.tasks[self.controller.index].notes)
        else:
            self.title.set("Title: none")
            self.priority.set("Priority: none")
            self.label_frame.status_label.config(fg="black")
            self.status.set("Status: none")
            self.notes.set("Notes: none")
        
            
class newEntry(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        title_label = tk.Label(self, text = "Title:")
        priority_label = tk.Label(self, text = "Priority:")
        self.priority_spinbox = tk.Spinbox(self, values=(1, 2, 3))
        notes_label = tk.Label(self, text = "Notes:")

        self.title_entry = tk.Entry(self)
        self.notes_entry = tk.Entry(self)

        done_b = tk.Button(self, text = "Done", command = self.done_button)
        
        
        title_label.grid()
        self.title_entry.grid()
        priority_label.grid()
        self.priority_spinbox.grid()
        notes_label.grid()
        self.notes_entry.grid()
        done_b.grid()

    def done_button(self, *args):
        self.title = self.title_entry.get()
        self.priority = int(self.priority_spinbox.get())
        self.notes= self.notes_entry.get()
        try:
            if (self.priority < 1 or self.priority > 3):
                raise Exception("bad priority")
            if (len(self.title) == 0):
                raise Exception("empty_field")
            if (len(self.notes) > 50 or len(self.title) > 50):
                raise Exception("longfield")
            
            task = newtask(self.title_entry.get(), self.priority_spinbox.get(), self.notes_entry.get())
            self.controller.add_task(task)
            self.title_entry.delete(0, 'end')
            self.notes_entry.delete(0, 'end')
            self.controller.show_frame("viewEntries")
            self.controller.frames["viewEntries"].update_view()
        except:
            messagebox.showwarning("error", "Field(s) not correct")
                

    
if __name__ == "__main__":
    thisapp = app()
    thisapp.title("Task Tracker")
    thisapp.protocol("WM_DELETE_WINDOW", thisapp.getmeouttahere)
    thisapp.mainloop()
