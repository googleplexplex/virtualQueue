
# - *- coding: utf- 8 - *-
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import vk_api
import random
import time
import requests
import os.path
import language
import json
import datetime
import sys
import locale
import subprocess
import platform
import os
import re
import textwrap
import requests
import traceback

import builtins
vk = builtins.vk
GroupId = builtins.GroupId


def SendMessage(UserId = '', Text = '', Attach = '', Mention = 1):
	vk.method('messages.setActivity', { 'user_id':UserId, 'type':'typing' })
	vk.method('messages.send', { 'user_id':UserId, 'message':Text, 'random_id':0, 'attachment':Attach, 'disable_mentions':Mention })

def SendKeyboard(UserId = '', Text = '', KeyBoard = 0, Attach = '', Mention = 1):
	vk.method('messages.setActivity', { 'user_id':UserId, 'type':'typing' })
	vk.method("messages.send", { "user_id":UserId, "message":Text, "keyboard":KeyBoard.get_keyboard(), "random_id":random.randint(1000000, 9000000000000)})
	
def LoadImage(Image, Cons):
	UploadUrl = vk.method('photos.getMessagesUploadServer', { 'peer_id':Cons })
	Post = requests.post(UploadUrl['upload_url'], files={ 'photo':open(Image, 'rb') }).json()
	SavedPhoto = vk.method('photos.saveMessagesPhoto', { 'photo':Post['photo'], 'server':Post['server'], 'hash':Post['hash'] })[0]
	SavedPhoto = 'photo' + str(SavedPhoto['owner_id']) + '_' + str(SavedPhoto['id'])
	return SavedPhoto

def GetUser(id):
	return vk.method('users.get', { 'user_ids':id })

def GetUserName(id):
	user = GetUser(id)
	name = ((user[0]['first_name']) + ' ' + (user[0]['last_name']))
	return name

def GetGroup(id):
	return vk.method('groups.getById', { 'group_ids':id })

def KickUser(id, cons):
	try:
		vk.method('messages.removeChatUser', { 'chat_id': cons - 2000000000, 'member_id': id })
	except vk_api.exceptions.ApiError as e:
		if int(e.error['error_code']) == 15:
			return False
		return True
	return True

def KickGroup(id, cons):
	try:
		vk.method('messages.removeChatUser', { 'chat_id': cons - 2000000000, 'member_id': -id })
	except vk_api.exceptions.ApiError as e:
		if int(e.error['error_code']) == 15:
			return False
		return True
	return True

def GetConvMembers(chatId):
	return vk.method('messages.getConversationMembers',{ 'peer_id':chatId, })

def DeleteMessage(PeerId, cmid):
	return vk.method('messages.delete', {'peer_id': PeerId, 'delete_for_all': 1, 'cmids': cmid, 'group_id': GroupId})