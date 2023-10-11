# - *- coding: utf- 8 - *-
from doctest import master
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import random
import time
import datetime;
import requests
import os.path
import language
import json
import datetime
import sys
from vk_api import keyboard
from vk_api.longpoll import VkLongPoll, VkEventType
import os
import re
import textwrap
import traceback
import io
from threading import Thread
import socket
import urllib3
import psycopg2

import token
Token = token.Token
GroupId = token.GroupId

#Логин в ВК
vk = vk_api.VkApi(token=Token)
vk._auth_token()
vk.get_api()
longpoll = VkBotLongPoll(vk, GroupId)
print('Бот успешно запущен в беседы')

#Подключаем библиотеки
import builtins
builtins.vk = vk
builtins.GroupId = GroupId
import BotApi


def SQLGetRequest(req):
    with psycopg2.connect(dbname='virtualQueue', user='postgres', password='123456', host='127.0.0.1') as conn:
        with conn.cursor() as cursor:
            cursor.execute(req)
            data = cursor.fetchall()
            return data
    return 0;
def SQLPostRequest(req):
    with psycopg2.connect(dbname='virtualQueue', user='postgres', password='123456', host='127.0.0.1') as conn:
        with conn.cursor() as cursor:
            cursor.execute(req)
    return;
    
def commandExecCycle():
    command = input()
    if command == u'exit' or command == u'close':
        os._exit(0)
hostCommandsExecThread = Thread(target=commandExecCycle)
hostCommandsExecThread.start()



class Task:
    clientId = 0
    serviceId = 0
    def __init__(self, clientId, serviceId):
        self.clientId = clientId
        self.serviceId = serviceId
    def __eq__(self, other):
        return (self.clientId == other.clientId) and (self.serviceId == other.serviceId);

def notifMaster(masterId, task): #Здесь можно настроить кнопки для основного интерфейса админа с информацией о клиенте
    vkkeyboard = VkKeyboard(one_time=True)
    vkkeyboard.add_button(clientAcceptedBtn, color=VkKeyboardColor.SECONDARY)
    vkkeyboard.add_button(clientIsLateBtn, color=VkKeyboardColor.NEGATIVE);
    BotApi.SendKeyboard(masterId, informationToTheMasterAboutTheClientMsg[0] + BotApi.GetUserName(task.clientId) + informationToTheMasterAboutTheClientMsg[1] + allServices[task.serviceId], vkkeyboard)

def getUserPosInQueue(clientId):
    return SQLGetRequest('SELECT * FROM (SELECT "clientId", ROW_NUMBER() over() as number FROM queue) WHERE ("clientId" = '+str(clientId)+');')[0][1];

def getNextClient(MasterId):
    sqlPresentTask = SQLGetRequest('SELECT * FROM "queue" LIMIT 1;');
    if sqlPresentTask != []:
        presentTask = Task(sqlPresentTask[0][0], sqlPresentTask[0][1])
        SQLPostRequest('DELETE FROM public."queue" WHERE ("clientId" = '+str(presentTask.clientId)+');');
        SQLPostRequest('UPDATE "presentRoles" SET "clientId"='+str(presentTask.clientId)+',"serviceId"='+str(presentTask.serviceId)+' WHERE "masterId"='+str(MasterId)+';');
        notifMaster(MasterId, presentTask)
        sqlMasterInfo = SQLGetRequest('SELECT * FROM "presentRoles" WHERE ("masterId" = '+str(UserId)+');');
        BotApi.SendMessage(presentTask.clientId, clientIsExpectedMsg+str(sqlMasterInfo[0][1]))
    else:
        BotApi.SendMessage(MasterId, noNewClientsMsg)
        SQLPostRequest('UPDATE "presentRoles" SET "clientId"=0,"serviceId"=0 WHERE "masterId"='+str(MasterId)+';');
        
def askAboutNextClient(MasterId): #Здесь можно настроить кнопки для вызова следующего клиента или завершении работы
    sqlGetQueueSize = SQLGetRequest('SELECT COUNT(*) FROM public.queue')
    vkkeyboard = VkKeyboard(one_time=True)
    vkkeyboard.add_button(inviteNextClientBtn, color=VkKeyboardColor.SECONDARY)
    vkkeyboard.add_button(workCompletedBtn, color=VkKeyboardColor.SECONDARY)
    BotApi.SendKeyboard(MasterId, askAboutNextClientMsg[0]+str(sqlGetQueueSize[0][0])+askAboutNextClientMsg[1], vkkeyboard)





disableIfWorkScheduleHasExpired = False #Если True, то бот будет работать, когда 001 кабинет не работает

servicesToGet = ["A", "B", "C", "D"]
servicesToGive = ["G", "H", "I", "J"]
fakeServicesToGet = ["E", "F"]
fakeServicesToGive = ["k", "l"]

sendingTheClientToTheSiteMsg = ['Данную услугу E можно получить на сайте личного кабинета: <ссылка>',
                                'Данную услугу F можно получить на сайте личного кабинета: <ссылка>',
                                'Данную услугу K можно получить на сайте личного кабинета: <ссылка>',
                                'Данную услугу L можно получить на сайте личного кабинета: <ссылка>']

windowIds = ['1', '2', '3', '4'] #Номера окон в кабинете


#Тексты сообщений для клиента
workScheduleHasExpiredMsg = 'Кабинет 001 закрыт (Время работы с 9 до 15)'
alreadyRecordedMsg = ['Вы уже записаны, ваш номер в очереди ', ', время ожидания примерно ', ' минут']
clientIsExpectedMsg = 'Вас ожидают в кабинете, номер окна: '
invitationToEnrollMsg = 'На что бы вы хотели записаться?'
clientSuccessfullyQueuedMsg = ['Вы успешно записались, ваш номер в очереди ', ', время ожидания примерно ', ' минут']
invitationToSubmitDocumentsMsg = 'На что бы вы хотели записаться?'
chooseToGiveOrGetMsg = 'На что бы вы хотели записаться?'
thankYouForYourVisitMsg = 'Спасибо за визит'
adminIsTiredOfWaitingMsg = 'Время ожидания оператора истекло, попробуйте снова встать в очередь'

#Тексты кнопок для клиента
giveDocumentsBtn = "Подать"
getDocumentsBtn = "Забрать"


#Тексты сообщений для админа
chooseWindowNumMsg = 'Чтобы начать смену, выберите номер своего окна'
adminChoosesToRemindOrDismissMsg = 'Выберите действие'
reminderSentToClientMsg = 'Напоминание отправлено'
workCompletedMsg = 'Работа завершена'
informationToTheMasterAboutTheClientMsg = ['Ожидайте пользователя ', ', который хочет ']
noNewClientsMsg = 'Пока у вас нет новых посетителей'
askAboutNextClientMsg = ['Пригласить следующего клиента? (В очереди сейчас ', ' клиентов)']

#Тексты кнопок для админа
clientAcceptedBtn = 'Принят'
clientIsLateBtn = 'Не пришёл'
inviteNextClientBtn = 'Пригласить'
workCompletedBtn = 'Завершить работу'
remindToClientBtn = 'Напомнить'
cancelClientBtn = 'Отменить'




allServices = servicesToGet+servicesToGive
allFakeServices = fakeServicesToGet+fakeServicesToGive

while True:
    try:
        for event in longpoll.listen():
            
            print(event, "\n\n");

            if event.type == VkBotEventType.MESSAGE_NEW:
                try:
                    MessageText = event.message['text']
                    UserId = event.object.message['from_id']

                    if event.object.message['peer_id'] < 2000000000:

                        if disableIfWorkScheduleHasExpired and (datetime.datetime.now().hour < 9 or datetime.datetime.now().hour > 15):
                            BotApi.SendMessage(UserId, workScheduleHasExpiredMsg)
                            continue;

                        sqlRoleCheck = SQLGetRequest('SELECT * FROM "roles" WHERE ("masterId" = '+str(UserId)+');');

                        if sqlRoleCheck == []:
                            sqlQueueCheck = SQLGetRequest('SELECT * FROM "queue" WHERE ("clientId" = '+str(UserId)+');');
                            sqlClientInfo = SQLGetRequest('SELECT * FROM "presentRoles" WHERE ("clientId" = '+str(UserId)+');');
                            if sqlQueueCheck != []:
                                userPos = getUserPosInQueue(UserId)
                                BotApi.SendMessage(UserId, alreadyRecordedMsg[0]+str(userPos)+alreadyRecordedMsg[1]+str(userPos*5)+alreadyRecordedMsg[2])
                                continue;
                            if sqlClientInfo != []:
                                BotApi.SendMessage(UserId, clientIsExpectedMsg+str(sqlClientInfo[0][1]))
                                continue;
                            
                            if MessageText == giveDocumentsBtn: #Здесь можно настроить кнопки для запроса на подачу документов
                                vkkeyboard = VkKeyboard(one_time=True)
                                vkkeyboard.add_button(servicesToGet[0], color=VkKeyboardColor.SECONDARY)
                                vkkeyboard.add_button(servicesToGet[1], color=VkKeyboardColor.SECONDARY)
                                vkkeyboard.add_button(servicesToGet[2], color=VkKeyboardColor.SECONDARY)
                                vkkeyboard.add_line()
                                vkkeyboard.add_button(servicesToGet[3], color=VkKeyboardColor.SECONDARY)
                                vkkeyboard.add_button(fakeServicesToGet[0], color=VkKeyboardColor.SECONDARY)
                                vkkeyboard.add_button(fakeServicesToGet[1], color=VkKeyboardColor.SECONDARY)
                                BotApi.SendKeyboard(UserId, invitationToEnrollMsg, vkkeyboard)

                            elif MessageText == getDocumentsBtn: #Здесь можно настроить кнопки для запроса на получение документов
                                vkkeyboard = VkKeyboard(one_time=True)
                                vkkeyboard.add_button(servicesToGive[0], color=VkKeyboardColor.SECONDARY)
                                vkkeyboard.add_button(servicesToGive[1], color=VkKeyboardColor.SECONDARY)
                                vkkeyboard.add_button(servicesToGive[2], color=VkKeyboardColor.SECONDARY)
                                vkkeyboard.add_line()
                                vkkeyboard.add_button(servicesToGive[3], color=VkKeyboardColor.SECONDARY)
                                vkkeyboard.add_button(fakeServicesToGive[0], color=VkKeyboardColor.SECONDARY)
                                vkkeyboard.add_button(fakeServicesToGive[1], color=VkKeyboardColor.SECONDARY)
                                BotApi.SendKeyboard(UserId, invitationToSubmitDocumentsMsg, vkkeyboard)

                            elif MessageText in allServices:
                                SQLPostRequest('INSERT INTO public."queue" ("clientId", "serviceId") VALUES ( '+str(UserId)+', '+str(allServices.index(MessageText))+' );');
                                userPos = getUserPosInQueue(UserId)
                                BotApi.SendMessage(UserId, clientSuccessfullyQueuedMsg[0]+str(userPos)+clientSuccessfullyQueuedMsg[1]+str(userPos*5)+clientSuccessfullyQueuedMsg[2])
                                sqlUsersInWork = SQLGetRequest('SELECT "masterId" FROM public."presentRoles" WHERE "clientId"=0;')
                                if sqlUsersInWork != []:
                                    askAboutNextClient(sqlUsersInWork[0][0]);
                            
                            elif MessageText in allFakeServices:
                                BotApi.SendMessage(UserId, sendingTheClientToTheSiteMsg[allFakeServices.index(MessageText)])

                            else: #Здесь можно настроить кнопки для выбора секции подачи или получения документов
                                vkkeyboard = VkKeyboard(one_time=True)
                                vkkeyboard.add_button(giveDocumentsBtn, color=VkKeyboardColor.SECONDARY)
                                vkkeyboard.add_line()
                                vkkeyboard.add_button(getDocumentsBtn, color=VkKeyboardColor.SECONDARY)
                                BotApi.SendKeyboard(UserId, chooseToGiveOrGetMsg, vkkeyboard)
                                
                        else:
                            sqlMasterInfo = SQLGetRequest('SELECT * FROM "presentRoles" WHERE ("masterId" = '+str(UserId)+');');

                            if sqlMasterInfo == []:
                                if not MessageText in windowIds: #Здесь можно настроить кнопки для выдачи ссылок на личный кабинет
                                    vkkeyboard = VkKeyboard(one_time=True)
                                    vkkeyboard.add_button(windowIds[0], color=VkKeyboardColor.SECONDARY)
                                    vkkeyboard.add_button(windowIds[1], color=VkKeyboardColor.SECONDARY)
                                    vkkeyboard.add_line()
                                    vkkeyboard.add_button(windowIds[2], color=VkKeyboardColor.SECONDARY)
                                    vkkeyboard.add_button(windowIds[3], color=VkKeyboardColor.SECONDARY)
                                    BotApi.SendKeyboard(UserId, chooseWindowNumMsg, vkkeyboard)
                                else:
                                    SQLPostRequest('INSERT INTO public."presentRoles" ("masterId", "window", "clientId", "serviceId") VALUES ( '+str(UserId)+', '+str(MessageText)+', 0,0 );');
                                    askAboutNextClient(UserId)
                                continue
                            
                            if MessageText == clientAcceptedBtn: 
                                SQLPostRequest('UPDATE "presentRoles" SET "clientId"=0,"serviceId"=0 WHERE "masterId"='+str(UserId)+';');
                                BotApi.SendMessage(sqlMasterInfo[0][2], thankYouForYourVisitMsg)
                                askAboutNextClient(UserId);
                            elif MessageText == clientIsLateBtn: #Здесь можно настроить кнопки для выбора напомнить клиенту или отменить его
                                vkkeyboard = VkKeyboard(one_time=True)
                                vkkeyboard.add_button(remindToClientBtn, color=VkKeyboardColor.SECONDARY)
                                vkkeyboard.add_button(cancelClientBtn, color=VkKeyboardColor.SECONDARY)
                                BotApi.SendKeyboard(UserId, adminChoosesToRemindOrDismissMsg, vkkeyboard)
                            elif MessageText == remindToClientBtn:
                                BotApi.SendMessage(sqlMasterInfo[0][2], clientIsExpectedMsg+str(sqlMasterInfo[0][1]))
                                BotApi.SendMessage(UserId, reminderSentToClientMsg)
                                notifMaster(UserId, Task(sqlMasterInfo[0][2], sqlMasterInfo[0][3]))
                            elif MessageText == cancelClientBtn:
                                BotApi.SendMessage(sqlMasterInfo[0][2], adminIsTiredOfWaitingMsg)
                                SQLPostRequest('UPDATE "presentRoles" SET "clientId"=0,"serviceId"=0 WHERE "masterId"='+str(UserId)+';');
                                askAboutNextClient(UserId);
                            elif MessageText == inviteNextClientBtn:
                                getNextClient(UserId)
                            elif MessageText == workCompletedBtn:
                                SQLPostRequest('DELETE FROM public."presentRoles" WHERE ("masterId" = '+str(UserId)+');');
                                BotApi.SendMessage(UserId, workCompletedMsg)
                            else:
                                if sqlMasterInfo[0][3] == 0:
                                    askAboutNextClient(UserId)
                                else:
                                    notifMaster(UserId, Task(sqlMasterInfo[0][2], sqlMasterInfo[0][3]))

                    
                except vk_api.exceptions.ApiError as e:
                    if e.code == 15:
                        continue; #Игнорируем попытки удалить сообщения администраторов 
                    print('==========')
                    with io.open('LastErrorLog.txt', 'w', encoding="utf-8") as ErrorLogFile:
                        ErrorLogFile.write(repr(event) + '\n\n' + traceback.format_exc())
                    print(traceback.format_exc())
                except Exception as e:
                    print('==========')
                    with io.open('LastErrorLog.txt', 'w', encoding="utf-8") as ErrorLogFile:
                        ErrorLogFile.write(repr(event) + '\n\n' + traceback.format_exc())
                    print(traceback.format_exc())
            
                    
    except (requests.exceptions.ReadTimeout, socket.timeout, urllib3.exceptions.ReadTimeoutError):
        #Игнорируем тайм-аут
        pass
    except Exception as e:
        print('==========')
        print('Exception вызван внутри основного тела цикла бота, подробнее:')
        print(traceback.format_exc())
