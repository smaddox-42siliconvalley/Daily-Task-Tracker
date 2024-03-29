# Daily-Task-Tracker
Productivity tool written in python

This app helps you keep track of things you need to accomplish

![alt text](img/viewEntriesPage.png)


**Installation Instructions**

Windows: 

Download python 3 [here](https://www.python.org/downloads)

Download ZIP file

Extract contents into a new folder

double click app.pyw

MacOs:

Install HomeBrew
```
mkdir $HOME/.brew && curl -fsSL https://github.com/Homebrew/brew/tarball/master | tar xz --strip 1 -C $HOME/.brew
mkdir -p /tmp/.$(whoami)-brew-locks
mkdir -p $HOME/.brew/var/homebrew
ln -s /tmp/.$(whoami)-brew-locks $HOME/.brew/var/homebrew/locks
export PATH="$HOME/.brew/bin:$PATH"
brew update && brew upgrade
```
update your .zshrc
```
mkdir -p /tmp/.$(whoami)-brew-locks
export PATH="$HOME/.brew/bin:$PATH"
```

then use HomeBrew to install python 3

```
brew install python3
```

clone this repository

```
git clone https://github.com/M3n3laus/Daily-Task-Tracker.git Daily-Task-Tracker
```

Run the program with the following

```
cd Daily-Task-Tracker
python3 app.pyw
```

**Using the program:**

**Add a new task:**

Click *New Task* under the file menu

![alt text](img/filemenu.png)

This will bring up the task entry page

![alt text](img/taskEntryPage.png)


A task's title cannot contain more than 50 characters

Notes are optional


**Reporting**

Upload and Download reports

Reports will appear in the reports folder inside your repository 

![alt text](img/reportmenu.png)


For reports:

On track is the completion of all tasks

**License**

Daily-Task-Tracker is licensed under the GNU General Public License
