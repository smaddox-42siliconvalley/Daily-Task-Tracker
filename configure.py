# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    configure.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: smaddox <marvin@42.fr>                     +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/08/25 18:36:25 by smaddox           #+#    #+#              #
#    Updated: 2019/08/26 15:40:08 by smaddox          ###   ########.fr        #
#                                                                              #
#   This file contains the class that handle I/O and ftp                       #
#                                                                              #
# **************************************************************************** #

import os
import pickle
import platform
import datetime
import csv
import taskmanager
import ftplib

class configs:
    def __init__(self, parent):
        self.parent = parent
        self.reportpath = './reports/'
        self.configpath = './config/'
        self.picklefilename = 'tasks.txt'
        self.configfilename = 'setup.txt'
        self.server_ip = '10.10.138.142'
        self.data = { }
        self.now = datetime.datetime.now()
        self.date = str(self.now.year) + '-' + str(self.now.month) + '-' + str(self.now.day)
        self.server_path = 'files/' + self.date
        self.check_folder()
        self.load_config()

    def get_username(self):
        return(self.data['username'])

    def get_password(self):
        return(self.data['password'])
   
    def set_username(self, username):
        self.data['username'] = username

    def set_password(self, password):
        self.data['password'] = password

    def get_date(self):
        return(self.date)

    def check_folder(self):
        found = 0
        report_dirs = next(os.walk(self.reportpath))[1]
        for dirs in report_dirs:
            if dirs == self.date:
                found = 1
        if found == 0:
            os.mkdir(self.reportpath + self.date)

    def load_pickle(self):
        self.pickle_file = open(self.configpath + self.picklefilename, 'rb')
        try:
            self.tasks = pickle.load(self.pickle_file)
        except:
            self.tasks = []
        self.pickle_file.close()
        return(self.tasks)

    def load_config(self):
        self.setup = open(self.configpath + self.configfilename)
        csv_values = csv.reader(self.setup)
        for row in csv_values:
            self.data.update( {row[0] : row[1]} )
        self.setup.close()

    def check_firsttime(self):
        if (self.data['firsttime'] == 'yes'):
            return(1)
        elif (self.data['firsttime'] == 'no'):
            return(0)

    def write_config(self):
        self.setup = open(self.configpath + self.configfilename, 'w')
        self.data['firsttime'] = 'no'
        key = [ ]
        values = [ ]
        
        for keys in self.data.keys():
            key.append(keys)
        
        for vals in self.data.values():
            values.append(vals)

        for i in range(0, len(key)):
            self.setup.write("%s,%s\n"%(key[i], values[i]))

        self.setup.close()


    def dump_pickle(self, tasks):
        self.picklefile = open(self.configpath + self.picklefilename, 'wb')
        pickle.dump(tasks, self.picklefile)
        self.picklefile.close()

    def ftp_init(self):
        self.session = ftplib.FTP(self.server_ip)
        self.session.login(self.data['username'], self.data['password'])
        self.session.cwd(self.server_path)

    def ftp_post(self):
        try:
            if(self.report_generator()):
                return
            myfile = open(self.reportpath + self.date + '/' + self.data['username'] + '.txt', 'rb')
            self.session.storbinary('STOR ' + self.data['username'] + '.txt', myfile)
            myfile.close()
            self.parent.throw_info_plz("ftp client", "Report sent successfully")
        except:
            self.parent.throw_info_plz("ftp client", "Report failed to send")

    def ftp_get(self):
        try:
            nlst = self.session.nlst()
            for files in nlst:
                temp = open(self.reportpath + self.date + '/' + files, 'wb')
                self.session.retrbinary('RETR ' + files, temp.write)
                temp.close()
            self.parent.throw_info_plz("ftp client", "Reports successfully downloaded")
        except:
            self.parent.throw_info_plz("ftp client", "Download failed")


    def report_generator(self):
        tasks = self.parent.get_tasks()
        reportpath = self.reportpath + self.date + '/' + self.data['username'] + '.txt'

        if len(tasks) == 0:
            self.parent.throw_info_plz("Report Generator", "Nothing to report")
            return(1)
        
        reportfile = open(reportpath, 'w+')
        ontrack = 1
        perfect = 1

        for task in tasks:
            temp = 'Title: ' + task.title + \
                    '\nPriority level: ' + str(task.priority) + \
                    '\nStatus: ' + task.status + \
                    '\nNotes: \n' + task.notes + \
                    '\n\n'
            
            if task.priority == 1 and task.status == 'incomplete':
                ontrack = 0
            if task.priority != 3 and task.status == 'incomplete':
                perfect = 0

            reportfile.write(temp)

        reportfile.write('On track: ' + str(ontrack) + '\n')
        reportfile.write('Main task accomplished: ' + str(perfect) + '\n')
        reportfile.close()
        















