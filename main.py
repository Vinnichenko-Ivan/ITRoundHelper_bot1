import telebot
from time import sleep, time
from functools import wraps
from apscheduler.schedulers.background import BackgroundScheduler
import User
import datetime as dt
import pytz
import datetime
import logging

time_now = dt.datetime.now(pytz.utc)
token = '1850071919:AAEb5d3-wJ-wDQBrAgD6qNzGoTxDhZtpbII'
bot = telebot.TeleBot(token)
users = []
timeZone = ['GMT+0' ,'GMT+1' ,'GMT+2' ,'GMT+3' ,'GMT+4' ,'GMT+5' ,'GMT+6' ,'GMT+7' ,'GMT+8' ,'GMT+9' ,'GMT+10' ,'GMT+11' ,'GMT+12' ,'GMT-1' ,'GMT-2' ,'GMT-3' ,'GMT-4' ,'GMT-5' ,'GMT-6' ,'GMT-7' ,'GMT-8' ,'GMT-9' ,'GMT-10' ,'GMT-11' ,'GMT-12']
time_now = dt.datetime.now(pytz.utc)

def getTime(userId):
    buff2 = users[userId].timeZone
    if('+' in buff2): #костыль из-за странностей в pitz
        buff2 = buff2.replace('+','-')
    else:
        buff2 = buff2.replace('-', '+')
    timezone = pytz.timezone(buff2)
    date = dt.datetime.now(timezone)
    newDate = datetime.datetime(date.year,date.month,date.day,date.hour,date.minute)
    return (newDate)

def timeUpdater(*args, **kwargs):#тут будет отправка уведомлений
    time_now = dt.datetime.now(pytz.utc)
    for i in range (0, len(users)):
        date_for_user = getTime(i)
        for n in range(0,len(users[i].tasksReminder)):
            if(date_for_user >= users[i].tasksReminder[n]):
                buff = 'Вы просили напомнить о ' + users[i].tasksHeading[n]
                bot.send_message(users[i].userId, buff)
                bot.send_message(users[i].userId, users[i].tasks[n])
                buff = 'Время события ' + str(users[i].tasksTime[n])
                bot.send_message(users[i].userId, buff)
                users[i].tasksHeading.pop(n)
                users[i].tasks.pop(n)
                users[i].tasksTime.pop(n)
                users[i].tasksReminder.pop(n)
    print(time_now)

sched = BackgroundScheduler()
sched.add_job(timeUpdater, 'interval', seconds=1)
sched.start()

commands = ['/start','/time','/setTime','/help','/myNotes','/addNote','/displayNote','/removeNote','/displayTasks','/displayTask','/removeTask','/addTask']

helpingText = '/start - Напишите для начала работы. \n' \
              '/setTime - Напишите для смены часового пояся. \n' \
              '/time - Напишите, если хотите узнать время в вашем часовом поясе на данный момент. \n' \
              '/addNote - Напишите, если хотите добавить заметку. \n' \
              '/myNotes - Напишите, если хотите посмотреть все номера и заголовки всех заметок. \n' \
              '/displayNote - Напишите для того, что бы посмотреть конкретную заметку.\n' \
              '/removeNote - Напишите для того, что бы удалить конкретную заметку.\n' \
              '/addTask - Напишите, если хотите добавить задачу.\n' \
              '/displayTasks - Напишите, если хотите посмотреть все номера и заголовки всех задач. \n' \
              '/displayTask - Напишите для того, что бы удалить конкретную задачу.\n' \
              '/removeTask - Напишите для того, что бы удалить конкретную задачу.\n' \
              '/help - Выведет это сообщение.\n' \
              '/about - Вывет информацию о боте.' \

aboutText = 'Данный бот - бот помошник. Он поможет вам не забыть о чем то важном. ' \
            'В его функционал входит создание задач, о которых он напомнит вам и создание заметок, ' \
            'которые вы можете прочитать в любое время.'


def registrathion(message, userId):#функция регистрации
    bot.send_message(message.from_user.id, 'Привет!')
    if (userId != -1):
        bot.send_message(message.from_user.id, 'Ну не честно регистрироваться дважды. У меня так бд лопнет!!! Не буду регать.')
    else:
        bot.send_message(message.from_user.id, 'Первый раз тебя тут вижу! Я тебя запомнил)')
        newUser = User.User()
        newUser.userId = message.from_user.id
        newUser.doing = 'setTime'
        bot.send_message(message.from_user.id, 'Раз ты тут первый раз, то я задам тебе пару вопросов. Начнем. Какой у вас часовой пояс? у меня вот GMT+7. Мне просто нужно знать это, что бы присылать уведомления вовремя. ')
        bot.send_message(message.from_user.id, 'Пожалуйста выберите один из вариантов и напишите его номер: \n 0:GMT+0 \n 1:GMT+1 \n 2:GMT+2 \n 3:GMT+3 \n 4:GMT+4 \n 5:GMT+5 \n 6:GMT+6 \n 7:GMT+7 \n 8:GMT+8 \n 9:GMT+9 \n 10:GMT+10 \n 11:GMT+11 \n 12:GMT+12 \n 13:GMT-1 \n 14:GMT-2 \n 15:GMT-3 \n 16:GMT-4 \n 17:GMT-5 \n 18:GMT-6 \n 19:GMT-7 \n 20:GMT-8 \n 21:GMT-9 \n 22:GMT-10 \n 23:GMT-11 \n 24:GMT-12')
        users.append(newUser)

def setTime(message, userId):#функция смены часового пояса
    if(message.text.lower().isnumeric()):
        if(0 <= int(message.text.lower()) <= 24):
            users[userId].timeZone = 'Etc/' + timeZone[int(message.text.lower())]
            users[userId].doing = 'working'
            bot.send_message(message.from_user.id, 'Отлично! Я запомнил. Все мои функции ты можешь посмотреть написав в чат /help')
        else:
            bot.send_message(message.from_user.id, 'Такого варианта нет!).')
            bot.send_message(message.from_user.id, 'Пожалуйста выберите один из вариантов и напишите его номер: \n 0:GMT+0 \n 1:GMT+1 \n 2:GMT+2 \n 3:GMT+3 \n 4:GMT+4 \n 5:GMT+5 \n 6:GMT+6 \n 7:GMT+7 \n 8:GMT+8 \n 9:GMT+9 \n 10:GMT+10 \n 11:GMT+11 \n 12:GMT+12 \n 13:GMT-1 \n 14:GMT-2 \n 15:GMT-3 \n 16:GMT-4 \n 17:GMT-5 \n 18:GMT-6 \n 19:GMT-7 \n 20:GMT-8 \n 21:GMT-9 \n 22:GMT-10 \n 23:GMT-11 \n 24:GMT-12')
    else:
        bot.send_message(message.from_user.id, 'Такого варианта нет!).')
        bot.send_message(message.from_user.id, 'Пожалуйста выберите один из вариантов и напишите его номер: \n 0:GMT+0 \n 1:GMT+1 \n 2:GMT+2 \n 3:GMT+3 \n 4:GMT+4 \n 5:GMT+5 \n 6:GMT+6 \n 7:GMT+7 \n 8:GMT+8 \n 9:GMT+9 \n 10:GMT+10 \n 11:GMT+11 \n 12:GMT+12 \n 13:GMT-1 \n 14:GMT-2 \n 15:GMT-3 \n 16:GMT-4 \n 17:GMT-5 \n 18:GMT-6 \n 19:GMT-7 \n 20:GMT-8 \n 21:GMT-9 \n 22:GMT-10 \n 23:GMT-11 \n 24:GMT-12')

def time(message, userId): #фукция отправки времени пользователю
    buff = 'Ваш часовой пояс => ' + users[userId].timeZone
    bot.send_message(message.from_user.id, buff)
    buff = 'Сейчас у вас ' + str(getTime(userId))
    bot.send_message(message.from_user.id, buff)

def addNoteHeading(message, userId):#функция добавления заголовка заметки
    users[userId].notesHeading.append(message.text)
    users[userId].doing = 'addNote'
    bot.send_message(message.from_user.id, 'Теперь напишите саму заметку.')

def addNote(message, userId):#функция добавления самой заметки
    users[userId].notes.append(message.text)
    users[userId].doing = 'working'
    bot.send_message(message.from_user.id, 'Заметка добавлена.')

def displayNotesHeading(message, userId):#функция выдачи пользователю всех его заметок
    if(len(users[userId].notes) == 0):
        bot.send_message(message.from_user.id, 'У вас нет заметок.')
    else:
        buff = ''
        for n in range(0,len(users[userId].notes)):
            buff += str(n)
            buff += ' - '
            buff += users[userId].notesHeading[n]
            buff += '\n'
        bot.send_message(message.from_user.id, buff)
def displayNote(message, userId):#показ конкреткой замекти по её номеру
    if(len(users[userId].notes) == 0):
        bot.send_message(message.from_user.id, 'У вас нет заметок.')
        users[userId].doing = 'working'

    elif (message.text.lower() == '-1'):
        displayNotesHeading(message, userId)

    else:
        if (message.text.lower().isnumeric()):
            if (0 <= int(message.text.lower()) <  len(users[userId].notes)):
                users[userId].doing = 'working'
                bot.send_message(message.from_user.id, users[userId].notesHeading[int(message.text.lower())])
                bot.send_message(message.from_user.id, users[userId].notes[int(message.text.lower())])
            else:
                bot.send_message(message.from_user.id, 'Такой заметки нет.')
        else:
            bot.send_message(message.from_user.id, 'Такого варианта нет!).')
def removeNote(message, userId):#удаление заметки по номеру
    if(len(users[userId].notes) == 0):
        bot.send_message(message.from_user.id, 'У вас нет заметок.')
        users[userId].doing = 'working'

    elif (message.text.lower() == '-1'):
        displayNotesHeading(message, userId)

    elif (message.text.lower() == '-2'):
        bot.send_message(message.from_user.id, 'Удаление отменено')
        users[userId].doing = 'working'

    elif(message.text.lower().isnumeric()):
        if (0 <= int(message.text.lower()) <  len(users[userId].notes)):
            users[userId].doing = 'working'
            users[userId].notesHeading.pop(int(message.text.lower()) )
            users[userId].notes.pop(int(message.text.lower()))
            bot.send_message(message.from_user.id, 'Заметка удалена')
        else:
            bot.send_message(message.from_user.id, 'Такой заметки нет.')

    else:
        bot.send_message(message.from_user.id, 'Такого варианта нет!).')

def addTask(message, userId):
    users[userId].tasks.append(message.text)
    users[userId].doing = 'addTaskTime'
    bot.send_message(message.from_user.id, 'Описание добавленно. Введите время события, о котором пишите. Время вводить в формате: год месяц число часы минуты через пробел. Введите -1, если хотите указать время на данный момент')

def addTaskTime(message, userId):
    if(message.text == '-1'):
        bot.send_message(message.from_user.id, 'Ок. Теперь введите время уведомления')
        users[userId].tasksTime.append(dt.datetime.now(pytz.utc))
        users[userId].doing = 'addTaskReminder'
    else:
        pars = message.text.split(' ')
        if(len(pars) != 5):
            bot.send_message(message.from_user.id, 'Укажите время правильно')
        elif(all(temp.isnumeric() for temp in pars) == False):
            bot.send_message(message.from_user.id, 'Укажите время правильно')
        else:
            year = int(pars[0])
            month = int(pars[1])
            day = int(pars[2])
            hour = int(pars[3])
            minute = int(pars[4])
            try:
                date = datetime.datetime(year,month,day,hour,minute,0)
                if(date < getTime(userId)):
                    bot.send_message(message.from_user.id, 'Оно уже прошло, но я его запомню)')
                else:
                    bot.send_message(message.from_user.id, 'Сейчас запишем')
                users[userId].tasksTime.append(date)
                users[userId].doing = 'addTaskReminder'
                bot.send_message(message.from_user.id, 'Введите время, когда вам напомнить об этом. Формат тот же.')
            except:
                bot.send_message(message.from_user.id, 'Укажите время правильно')


def addTaskHeading(message, userId):
    users[userId].tasksHeading.append(message.text)
    users[userId].doing = 'addTask'
    bot.send_message(message.from_user.id, 'Заголовок задачи добавлен. Теперь введите её описание')

def addTaskReminder(message, userId):
    if (message.text == '-1'):
        bot.send_message(message.from_user.id, 'Время уведомления не может быть таким')
    else:
        pars = message.text.split(' ')
        if (len(pars) != 5):
            bot.send_message(message.from_user.id, 'Укажите время правильно')
        elif (all(temp.isnumeric() for temp in pars) == False):
            bot.send_message(message.from_user.id, 'Укажите время правильно')
        else:
            year = int(pars[0])
            month = int(pars[1])
            day = int(pars[2])
            hour = int(pars[3])
            minute = int(pars[4])
            try:
                date = datetime.datetime(year, month, day, hour, minute, 0)
                date_now = getTime(userId)
                if (date < date_now):
                    bot.send_message(message.from_user.id, 'Оно уже прошло... Я не смогу напомнить вам в прошлом...')
                else:
                    bot.send_message(message.from_user.id, 'Сейчас запишем. Ждите напоминания.')
                    users[userId].tasksReminder.append(date)
                    users[userId].doing = 'working'
            except:
                bot.send_message(message.from_user.id, 'Укажите время правильно')


def displayTasks(message, userId):
    if (len(users[userId].tasks) == 0):
        bot.send_message(message.from_user.id, 'У вас нет задач.')
    else:
        buff = ''
        for n in range(0, len(users[userId].tasks)):
            buff += str(n)
            buff += ' - '
            buff += users[userId].tasksHeading[n]
            buff += '\n'
        bot.send_message(message.from_user.id, buff)

def displayTask(message, userId):
    if (len(users[userId].tasks) == 0):
        bot.send_message(message.from_user.id, 'У вас нет задач.')
        users[userId].doing = 'working'

    elif (message.text.lower() == '-1'):
        displayTasks(message, userId)

    else:
        if (message.text.lower().isnumeric()):
            if (0 <= int(message.text.lower()) < len(users[userId].tasks)):
                users[userId].doing = 'working'
                bot.send_message(message.from_user.id, 'Задача : ' + users[userId].tasksHeading[int(message.text.lower())])
                bot.send_message(message.from_user.id, 'Описание : ' + users[userId].tasks[int(message.text.lower())])
                bot.send_message(message.from_user.id, 'Время задачи : ' + str(users[userId].tasksTime[int(message.text.lower())]))
                bot.send_message(message.from_user.id, 'Когда уведомить : ' + str(users[userId].tasksReminder[int(message.text.lower())]))
            else:
                bot.send_message(message.from_user.id, 'Такой задачи нет.')
        else:
            bot.send_message(message.from_user.id, 'Такого варианта нет!).')

def removeTask(message, userId):
    if (len(users[userId].tasks) == 0):
        bot.send_message(message.from_user.id, 'У вас нет задач.')
        users[userId].doing = 'working'

    elif (message.text.lower() == '-1'):
        displayTasks(message, userId)

    elif (message.text.lower() == '-2'):
        users[userId].doing = 'working'
        bot.send_message(message.from_user.id, 'Удаление отменено.')

    else:
        if (message.text.lower().isnumeric()):
            if (0 <= int(message.text.lower()) < len(users[userId].tasks)):
                users[userId].doing = 'working'
                users[userId].tasksHeading.pop(int(message.text.lower()))
                users[userId].tasks.pop(int(message.text.lower()))
                users[userId].tasksTime.pop(int(message.text.lower()))
                users[userId].tasksReminder.pop(int(message.text.lower()))
                bot.send_message(message.from_user.id, 'Задача успешно удалена.')
            else:
                bot.send_message(message.from_user.id, 'Такой задачи нет.')
        else:
            bot.send_message(message.from_user.id, 'Такого варианта нет!).')

@bot.message_handler()
def get_text_messages(message):#обработчик сообщений.
    #try:
        userId = User.findUser(message.from_user.id, users)
        if message.text.lower() == '/start':
            registrathion(message, userId)
            print(users)

        elif message.text.lower()  == '/help':
            bot.send_message(message.from_user.id, helpingText)

        elif message.text.lower() == '/about':
            bot.send_message(message.from_user.id, aboutText)

        elif(userId == -1):
            bot.send_message(message.from_user.id, 'Прости, но ты не зарегистрированн. Напиши /start для начала регистрации')

        elif users[userId].doing == 'setTime':
            setTime(message, userId)

        elif users[userId].doing == 'addNoteHeading':
            addNoteHeading(message,userId)

        elif users[userId].doing == 'addNote':
            addNote(message, userId)

        elif users[userId].doing == 'displayNote':
            displayNote(message, userId)

        elif users[userId].doing == 'removeNote':
            removeNote(message, userId)

        elif users[userId].doing == 'addTask':
            addTask(message, userId)

        elif users[userId].doing == 'addTaskTime':
            addTaskTime(message, userId)

        elif users[userId].doing == 'addTaskHeading':
            addTaskHeading(message, userId)

        elif users[userId].doing == 'addTaskReminder':
            addTaskReminder(message, userId)

        elif users[userId].doing == 'displayTask':
            displayTask(message, userId)

        elif users[userId].doing == 'removeTask':
            removeTask(message, userId)

        elif message.text == '/myNotes':
            displayNotesHeading(message, userId)

        elif message.text == '/removeNote':
            if (len(users[userId].notes) == 0):
                bot.send_message(message.from_user.id, 'У вас нет заметок.')
                users[userId].doing = 'working'
            else:
                bot.send_message(message.from_user.id, 'Пожалуйста напишите номер заметки что бы удалить её, -1 что бы показать все заметки или -2 для отмены')
                users[userId].doing = 'removeNote'

        elif message.text == '/addTask':
            bot.send_message(message.from_user.id, 'Введите название задачи: ')
            users[userId].doing = 'addTaskHeading'

        elif message.text == '/displayTask':
            if (len(users[userId].tasks) == 0):
                bot.send_message(message.from_user.id, 'У вас нет задач.')
            else:
                users[userId].doing = 'displayTask'
                bot.send_message(message.from_user.id, 'Введите номер задачи: ')

        elif message.text == '/displayTasks':
            displayTasks(message, userId)

        elif message.text == '/removeTask':
            if (len(users[userId].tasks) == 0):
                bot.send_message(message.from_user.id, 'У вас нет задач.')
            else:
                bot.send_message(message.from_user.id, 'Введите номер задачи: ')
                users[userId].doing = 'removeTask'

        elif message.text == '/setTime':
            users[userId].doing = 'setTime'
            bot.send_message(message.from_user.id, 'Пожалуйста выберите один из вариантов и напишите его номер: \n 0:GMT+0 \n 1:GMT+1 \n 2:GMT+2 \n 3:GMT+3 \n 4:GMT+4 \n 5:GMT+5 \n 6:GMT+6 \n 7:GMT+7 \n 8:GMT+8 \n 9:GMT+9 \n 10:GMT+10 \n 11:GMT+11 \n 12:GMT+12 \n 13:GMT-1 \n 14:GMT-2 \n 15:GMT-3 \n 16:GMT-4 \n 17:GMT-5 \n 18:GMT-6 \n 19:GMT-7 \n 20:GMT-8 \n 21:GMT-9 \n 22:GMT-10 \n 23:GMT-11 \n 24:GMT-12')
            bot.send_message(message.from_user.id, 'К сожалению, все созданные вами задачи будут работать по старому времени')
        elif message.text.lower() == '/time':
            time(message,userId)

        elif message.text == '/addNote':
            users[userId].doing = 'addNoteHeading'
            bot.send_message(message.from_user.id, 'Пожалуйста напишите заголовок заметки')

        elif message.text == '/displayNote':
            if (len(users[userId].notes) == 0):
                bot.send_message(message.from_user.id, 'У вас нет заметок.')
                users[userId].doing = 'working'
            else:
                users[userId].doing = 'displayNote'
                bot.send_message(message.from_user.id, 'Напишите номер заметки или -1 для того, что бы показать все заметки')


        else:
            bot.send_message(message.from_user.id, 'Не понимаю, что это значит.')
    #except:
    #    bot.send_message(message.from_user.id, 'Я сломался...')


bot.polling(none_stop=True)
