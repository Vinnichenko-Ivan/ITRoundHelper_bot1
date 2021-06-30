import Note

class User:
    userId = 0
    timeZone = 'Etc/GMT+7'
    doing = 'reg'
    notes = []
    notesHeading = []

    tasks = []
    tasksHeading = []
    tasksTime = []
    tasksReminder = []

def findUser(id, users):
    for i in range(len(users)):
        if(users[i].userId == id):
            return i
    return -1
