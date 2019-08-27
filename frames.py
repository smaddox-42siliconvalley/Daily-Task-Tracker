# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    frames.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: smaddox <marvin@42.fr>                     +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/08/25 21:17:00 by smaddox           #+#    #+#              #
#    Updated: 2019/08/26 17:53:56 by smaddox          ###   ########.fr        #
#                                                                              #
#   This file contains the classes for each window in the gui                  #
#                                                                              #
# **************************************************************************** #

import tkinter as tk

class initPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.user_label = tk.Label(self, text = "Enter your ftp username:")
        self.pass_label = tk.Label(self, text = "Enter the password for the ftp server:")
        self.pass_entry = tk.Entry(self)
        self.user_entry = tk.Entry(self)
        self.done_b = tk.Button(self, text = "Done", command=self.get_vals)

        self.user_label.grid()
        self.user_entry.grid()
        self.pass_label.grid()
        self.pass_entry.grid()
        self.done_b.grid()


    def get_vals(self):
        self.controller.configs.set_username(self.user_entry.get())
        self.controller.configs.set_password(self.pass_entry.get())
        self.controller.configs.write_config()
        self.controller.show_frame("viewEntries")
            
        
class viewEntries(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.title = tk.StringVar()
        self.priority = tk.StringVar()
        self.status = tk.StringVar()

        self.label_frame = tk.Frame(self)
        button_frame = tk.Frame(self)
        
        title_label = tk.Label(self.label_frame, textvariable = self.title)
        priority_label = tk.Label(self.label_frame, textvariable = self.priority)
        self.label_frame.status_label = tk.Label(self.label_frame, textvariable = self.status)
        notes_label = tk.Label(self.label_frame, text = "Notes:")

        self.notes_textbox = tk.Text(self.label_frame, height = 10, width = 50, bg='gray75')

        next_b = tk.Button(button_frame, text = "  next  ", command = self.next_button)
        prev_b = tk.Button(button_frame, text = "previous", command = self.prev_button)
        complete_b = tk.Button(button_frame, text = "toggle complete", command = self.complete_button)
        remove_b = tk.Button(button_frame, text = "remove task", fg = "red", command = self.remove_button)

        self.update_view()

        title_label.grid(row=0, column=1)
        priority_label.grid(row=1, column=1)
        notes_label.grid(row=2, column=1)
        self.label_frame.status_label.grid(row=4, column=1)

        self.notes_textbox.grid(row=3, column=1)
        self.notes_textbox.config(state='disabled')

        next_b.grid(row=4, column=2, sticky='nesw', padx=10, pady=20)
        prev_b.grid(row=4, column=0, padx=10, pady=20)
        complete_b.grid(row=4, column=1, padx=10, pady=20)
        remove_b.grid(row =6, column=1, pady=10)

        self.label_frame.grid()
        button_frame.grid()


    def remove_button(self, *args):
        self.controller.taskmanager.remove_task()
        self.update_view(self)
        
    def complete_button(self, *args):
        self.controller.taskmanager.complete()
        self.update_view(self)
        
    def next_button(self, *args):
        self.controller.taskmanager.next_task()
        self.update_view(self)

    def prev_button(self, *args):
            self.controller.taskmanager.prev_task()
            self.update_view(self)

        
    def update_view(self, *args):
        self.title.set("Title: " + self.controller.taskmanager.get_title())
        self.priority.set("Priority: " + str(self.controller.taskmanager.get_priority()))
        self.status.set("Status: " + self.controller.taskmanager.get_status())
        self.notes_textbox.config(state='normal')
        self.notes_textbox.delete(1.0, tk.END)
        self.notes_textbox.insert(1.0, self.controller.taskmanager.get_note())
        self.notes_textbox.config(state='disabled')
        if self.controller.taskmanager.get_status() == 'complete':
            self.label_frame.status_label.config(fg="green")
        elif self.controller.taskmanager.get_status() == 'incomplete':
            self.label_frame.status_label.config(fg="red")
        else:
            self.label_frame.status_label.config(fg="black")
        
            
class newEntry(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        title_label = tk.Label(self, text = "Title:")
        priority_label = tk.Label(self, text = "Priority:")
        self.priority_spinbox = tk.Spinbox(self, values=(1, 2, 3))
        notes_label = tk.Label(self, text = "Notes:")

        self.title_entry = tk.Entry(self)

        self.notes_entry = tk.Text(self, height=10, width=50, bg='gray75')

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
        self.notes = self.notes_entry.get(1.0, tk.END)
        try:
            if (self.priority < 1 or self.priority > 3):
                raise Exception("bad priority")
            if (len(self.title) == 0):
                raise Exception("empty_field")
            if (len(self.title) > 50):
                raise Exception("longfield")
            
            self.controller.taskmanager.add_task(self.title, self.priority, self.notes)
            self.title_entry.delete(0, 'end')
            self.notes_entry.delete(1.0, tk.END)
            self.controller.show_frame("viewEntries")
            self.controller.frames["viewEntries"].update_view()
        except:
            self.controller.throw_info_plz("error", "Field(s) not correct")
