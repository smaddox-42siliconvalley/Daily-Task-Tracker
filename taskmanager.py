# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    taskmanager.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: smaddox <marvin@42.fr>                     +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/08/25 21:28:25 by smaddox           #+#    #+#              #
#    Updated: 2019/08/27 12:50:25 by smaddox          ###   ########.fr        #
#                                                                              #
#   This file contains the classes that handles task operations                #
#   and keep track of them                                                     #
#                                                                              #
# **************************************************************************** #

class taskmanager:
    def __init__(self, tasks):
        self.tasks = tasks
        self.num_tasks = len(self.tasks)
        self.index = 0

    def add_task(self, title, rank, notes):
        newtask = task(title, notes)
        self.tasks.append(newtask)
        self.num_tasks += 1

    def remove_task(self):
        if (self.num_tasks != 0):
            self.tasks.pop(self.index)
            self.index = 0
            self.num_tasks -= 1

    def next_task(self):
        if (self.num_tasks > 0):
            self.index += 1
            self.index %= self.num_tasks

    def prev_task(self):
        if (self.num_tasks > 0):
            self.index -= 1
            self.index %= self.num_tasks

    def get_tasks(self):
        return(self.tasks)

    def get_title(self):
        if (self.num_tasks > 0):
            return(self.tasks[self.index].title)
        else:
            return('none')

    def get_status(self):
        if (self.num_tasks > 0):
            return(self.tasks[self.index].status)
        else:
            return('none')

    def get_note(self):
        if (self.num_tasks > 0):
            return(self.tasks[self.index].notes)
        else:
            return('none')

    def get_num_tasks(self):
        return(self.num_tasks)

    def complete(self):
        if (self.num_tasks > 0):
            self.tasks[self.index].complete()

    def change_note(self, note):
        if (self.num_task > 0):
            self.tasks[self.index].change_note(note)

    def change_title(self, title):
        if (self.num_tasks > 0):
            self.tasks[self.index].change_title(title)

class task:
    def __init__(self, title, notes):
        self.title = title
        self.notes = notes
        self.status = 'incomplete'

    def complete(self):
        if (self.status == 'complete'):
            self.status = 'incomplete'
        else:
            self.status = 'complete'

    def change_note(self, note):
        self.note = note

    def change_title(self, title):
        self.title = title
