# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    newapp.pyw                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: smaddox <marvin@42.fr>                     +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/08/25 20:30:41 by smaddox           #+#    #+#              #
#    Updated: 2019/08/26 21:35:00 by smaddox          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

#from frames import * 
import frames
import taskmanager
import configure
import webbrowser
import os
import platform
import sys
import tkinter as tk
from tkinter import messagebox


class app(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.configs = configure.configs(self)
        self.taskmanager = taskmanager.taskmanager(self.configs.load_pickle())
        self.geometry("600x400")
        container = tk.Frame(self)
        container.pack()
        self.frames = { }
        menu = new_menu(self, self)

        for F in (frames.newEntry, frames.viewEntries, frames.initPage):
            frame_name = F.__name__
            frame = F(container, self)
            self.frames[frame_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        if (self.configs.check_firsttime()):
            self.show_frame("initPage")
        else:
            self.configs.ftp_init()
            self.show_frame("viewEntries")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def get_tasks(self):
        return(self.taskmanager.get_tasks())

    def quit_app(self):
        self.configs.dump_pickle(self.taskmanager.get_tasks())
        self.destroy()
        sys.exit(0)
    
    def throw_info_plz(self, title, content):
        messagebox.showinfo(title, content)

class new_menu(tk.Menu):
    def __init__(self, parent, controller):
        tk.Menu.__init__(self, parent)
        
        menu_one = tk.Menu(self, tearoff = 0)
        menu_two = tk.Menu(self, tearoff = 0)

        menu_one.add_command(label = "New Task", command = lambda: parent.show_frame("newEntry"))
        menu_one.add_command(label = "Exit", command = parent.quit_app)

        menu_two.add_command(label = "Download Reports", command = parent.configs.ftp_get)
        menu_two.add_command(label = "Upload Reports", command = parent.configs.ftp_post)

        #menu_three.add_command(label = "Get Help", command = parent.get_help)

        self.add_cascade(label = "File", menu = menu_one)
        self.add_cascade(label = "Reporting", menu = menu_two)
        controller.config(menu = self)

def main():
    my_app = app()
    my_app.title("Task Tracker")
    my_app.protocol("WM_DELETE_WINDOW", my_app.quit_app)
    my_app.mainloop()

      
if __name__ == "__main__":
    main()
    

