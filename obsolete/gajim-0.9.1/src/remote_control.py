##	remote_control.py
##
## Contributors for this file:
##	- Yann Le Boulanger <asterix@lagaule.org>
##	- Nikos Kouremenos <kourem@gmail.com>
##	- Dimitur Kirov <dkirov@gmail.com>
##	- Andrew Sayman <lorien420@myrealbox.com>
##
## Copyright (C) 2003-2004 Yann Le Boulanger <asterix@lagaule.org>
##                         Vincent Hanquez <tab@snarc.org>
## Copyright (C) 2005 Yann Le Boulanger <asterix@lagaule.org>
##                    Vincent Hanquez <tab@snarc.org>
##                    Nikos Kouremenos <nkour@jabber.org>
##                    Dimitur Kirov <dkirov@gmail.com>
##                    Travis Shirk <travis@pobox.com>
##                    Norman Rasmussen <norman@rasmussen.co.za>
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published
## by the Free Software Foundation; version 2 only.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##

import gobject
import gtk
import os
import sys

import systray

from common import exceptions
from common import gajim
from common import helpers
from time import time
from common import i18n
from dialogs import AddNewContactWindow
_ = i18n._

import dbus_support
if dbus_support.supported:
	import dbus
	if dbus_support.version >= (0, 41, 0):
		import dbus.service
		import dbus.glib # cause dbus 0.35+ doesn't return signal replies without it
		DbusPrototype = dbus.service.Object
	elif dbus_support.version >= (0, 20, 0):
		DbusPrototype = dbus.Object
	else: #dbus is not defined
		DbusPrototype = str 

INTERFACE = 'org.gajim.dbus.RemoteInterface'
OBJ_PATH = '/org/gajim/dbus/RemoteObject'
SERVICE = 'org.gajim.dbus'

STATUS_LIST = ['offline', 'connecting', 'online', 'chat', 'away', 'xa', 'dnd',
	'invisible']

class Remote:
	def __init__(self):
		self.signal_object = None
		session_bus = dbus_support.session_bus.SessionBus()
		
		if dbus_support.version[1] >= 41:
			service = dbus.service.BusName(SERVICE, bus=session_bus)
			self.signal_object = SignalObject(service)
		elif dbus_support.version[1] <= 40 and dbus_support.version[1] >= 20:
			service=dbus.Service(SERVICE, session_bus)
			self.signal_object = SignalObject(service)

	def raise_signal(self, signal, arg):
		if self.signal_object:
			self.signal_object.raise_signal(signal, repr(arg))
		

class SignalObject(DbusPrototype):
	''' Local object definition for /org/gajim/dbus/RemoteObject. This doc must 
	not be visible, because the clients can access only the remote object. '''
	
	def __init__(self, service):
		self.first_show = True
		self.vcard_account = None

		# register our dbus API
		if dbus_support.version[1] >= 41:
			DbusPrototype.__init__(self, service, OBJ_PATH)
		elif dbus_support.version[1] >= 30:
			DbusPrototype.__init__(self, OBJ_PATH, service)
		else:
			DbusPrototype.__init__(self, OBJ_PATH, service, 
			[	self.toggle_roster_appearance,
				self.show_next_unread,
				self.list_contacts,
				self.list_accounts,
				self.change_status,
				self.open_chat,
				self.send_message,
				self.contact_info,
				self.send_file,
				self.prefs_list,
				self.prefs_store,
				self.prefs_del,
				self.prefs_put,
				self.add_contact,
				self.remove_contact,
				self.get_status,
			])

	def raise_signal(self, signal, arg):
		''' raise a signal, with a single string message '''
		if dbus_support.version[1] >= 30:
			from dbus import dbus_bindings
			message = dbus_bindings.Signal(OBJ_PATH, INTERFACE, signal)
			i = message.get_iter(True)
			i.append(arg)
			self._connection.send(message)
		else:
			self.emit_signal(INTERFACE, signal, arg)

	
	# signals 
	def VcardInfo(self, *vcard):
		pass

	def get_status(self, *args):
		'''get_status(account = None)
		returns status (show to be exact) which is the global one
		unless account is given'''
		account = self._get_real_arguments(args, 1)[0]
		accounts = gajim.contacts.keys()
		if not account:
			# If user did not ask for account, returns the global status
			return helpers.get_global_show()
		# return show for the given account
		index = gajim.connections[account].connected
		return STATUS_LIST[index]

	def send_file(self, *args):
		'''send_file(file_path, jid, account=None) 
		send file, located at 'file_path' to 'jid', using account 
		(optional) 'account' '''
		file_path, jid, account = self._get_real_arguments(args, 3)
		accounts = gajim.contacts.keys()
		
		# if there is only one account in roster, take it as default
		# if user did not ask for account
		if not account and len(accounts) == 1:
			account = accounts[0]
		if account:
			if gajim.connections[account].connected > 1: # account is  online
				connected_account = gajim.connections[account]
		else:
			for account in accounts:
				if gajim.contacts[account].has_key(jid) and \
					gajim.connections[account].connected > 1: # account is  online
					connected_account = gajim.connections[account]
					break
		if gajim.contacts.has_key(account) and \
			gajim.contacts[account].has_key(jid):
			contact = gajim.get_highest_prio_contact_from_contacts(
				gajim.contacts[account][jid])
		else:
			contact = jid
		
		if connected_account:
			if os.path.isfile(file_path): # is it file?
				gajim.interface.instances['file_transfers'].send_file(account, 
					contact, file_path)
				return True
		return False
		
	def send_message(self, *args):
		''' send_message(jid, message, keyID=None, account=None)
		send 'message' to 'jid', using account (optional) 'account'.
		if keyID is specified, encrypt the message with the pgp key '''
		jid, message, keyID, account = self._get_real_arguments(args, 4)
		if not jid or not message:
			return None # or raise error
		if not keyID:
			keyID = ''
		connected_account = None
		accounts = gajim.contacts.keys()
		
		# if there is only one account in roster, take it as default
		if not account and len(accounts) == 1:
			account = accounts[0]
		if account:
			if gajim.connections[account].connected > 1: # account is  online
				connected_account = gajim.connections[account]
		else:
			for account in accounts:
				if gajim.contacts[account].has_key(jid) and \
					gajim.connections[account].connected > 1: # account is  online
					connected_account = gajim.connections[account]
					break
		if connected_account:
			res = connected_account.send_message(jid, message, keyID)
			return True
		return False

	def open_chat(self, *args):
		''' start_chat(jid, account=None) -> shows the tabbed window for new 
		message to 'jid', using account(optional) 'account' '''
		jid, account = self._get_real_arguments(args, 2)
		if not jid:
			# FIXME: raise exception for missing argument (dbus0.35+)
			return None
		if jid.startswith('xmpp:'):
			jid = jid[5:] # len('xmpp:') = 5

		if account:
			accounts = [account]
		else:
			accounts = gajim.connections.keys()
			if len(accounts) == 1:
				account = accounts[0]
		connected_account = None
		first_connected_acct = None
		for acct in accounts:
			if gajim.connections[acct].connected > 1: # account is  online
				if gajim.interface.instances[acct]['chats'].has_key(jid):
					connected_account = acct
					break
				# jid is in roster
				elif gajim.contacts[acct].has_key(jid):
					connected_account = acct
					break
				# we send the message to jid not in roster, because account is specified,
				# or there is only one account
				elif account: 
					connected_account = acct
				elif first_connected_acct is None:
					first_connected_acct = acct
		
		# if jid is not a conntact, open-chat with first connected account
		if connected_account is None and first_connected_acct:
			connected_account = first_connected_acct
		
		if connected_account:
			gajim.interface.roster.new_chat_from_jid(connected_account, jid)
			# preserve the 'steal focus preservation'
			win = gajim.interface.instances[connected_account]['chats'][jid].window
			if win.get_property('visible'):
				win.window.focus()
			return True
		return False
	
	def change_status(self, *args, **keywords):
		''' change_status(status, message, account). account is optional -
		if not specified status is changed for all accounts. '''
		status, message, account = self._get_real_arguments(args, 3)
		if status not in ('offline', 'online', 'chat', 
			'away', 'xa', 'dnd', 'invisible'):
			# FIXME: raise exception for bad status (dbus0.35)
			return None
		if account:
			gobject.idle_add(gajim.interface.roster.send_status, account, 
				status, message)
		else:
			# account not specified, so change the status of all accounts
			for acc in gajim.contacts.keys():
				gobject.idle_add(gajim.interface.roster.send_status, acc, 
					status, message)
		return None

	def show_next_unread(self, *args):
		''' Show the window(s) with next waiting messages in tabbed/group chats. '''
		#FIXME: when systray is disabled this method does nothing.
		if len(gajim.interface.systray.jids) != 0:
			gajim.interface.systray.handle_first_event()

	def contact_info(self, *args):
		''' get vcard info for a contact. This method returns nothing.
		You have to register the 'VcardInfo' signal to get the real vcard. '''
		[jid] = self._get_real_arguments(args, 1)
		if not isinstance(jid, unicode):
			jid = unicode(jid)
		if not jid:
			# FIXME: raise exception for missing argument (0.3+)
			return None

		accounts = gajim.contacts.keys()
		
		for account in accounts:
			if gajim.contacts[account].__contains__(jid):
				self.vcard_account =  account
				gajim.connections[account].request_vcard(jid)
				break
		return None

	def list_accounts(self, *args):
		''' list register accounts '''
		if gajim.contacts:
			result = gajim.contacts.keys()
			if result and len(result) > 0:
				result_array = []
				for account in result:
					result_array.append(account.encode('utf-8'))
				return result_array
		return None

	def list_contacts(self, *args):
		''' list all contacts in the roster. If the first argument is specified,
		then return the contacts for the specified account '''
		[for_account] = self._get_real_arguments(args, 1)
		result = []
		if not gajim.contacts or len(gajim.contacts) == 0:
			return None
		if for_account:
			if gajim.contacts.has_key(for_account):
				for jid in gajim.contacts[for_account]:
					item = self._serialized_contacts(
						gajim.contacts[for_account][jid])
					if item:
						result.append(item)
			else:
				# 'for_account: is not recognised:', 
				return None
		else:
			for account in gajim.contacts:
				for jid in gajim.contacts[account]:
					item = self._serialized_contacts(gajim.contacts[account][jid])
					if item:
						result.append(item)
		# dbus 0.40 does not support return result as empty list
		if result == []:
			return None
		return result

	def toggle_roster_appearance(self, *args):
		''' shows/hides the roster window '''
		win = gajim.interface.roster.window
		if win.get_property('visible'):
			gobject.idle_add(win.hide)
		else:
			win.present()
			# preserve the 'steal focus preservation'
			if self._is_first():
				win.window.focus()
			else:
				win.window.focus(long(time()))

	def prefs_list(self, *args):
		prefs_dict = {}
		def get_prefs(data, name, path, value):
			if value is None:
				return
			key = ""
			if path is not None:
				for node in path:
					key += node + "#"
			key += name
			prefs_dict[key] = unicode(value[1])
		gajim.config.foreach(get_prefs)
		return repr(prefs_dict)
		
	def prefs_store(self, *args):
		try:
			gajim.interface.save_config()
		except Exception, e:
			return False
		return True
	
	def prefs_del(self, *args):
		[key] = self._get_real_arguments(args, 1)
		if not key:
			return False
		key_path = key.split('#', 2)
		if len(key_path) != 3:
			return False
		if key_path[2] == '*':
			gajim.config.del_per(key_path[0], key_path[1])
		else:
			gajim.config.del_per(key_path[0], key_path[1], key_path[2])
		return True
		
	def prefs_put(self, *args):
		[key] = self._get_real_arguments(args, 1)
		if not key:
			return False
		key_path = key.split('#', 2)
		if len(key_path) < 3:
			subname, value = key.split('=', 1)
			gajim.config.set(subname, value)
			return True
		subname, value = key_path[2].split('=', 1)
		gajim.config.set_per(key_path[0], key_path[1], subname, value)
		return True
		
	def add_contact(self, *args):
		[account] = self._get_real_arguments(args, 1)
		if gajim.contacts.has_key(account):
			AddNewContactWindow(account)
			return True
		return False
	
	def remove_contact(self, *args):
		[jid, account] = self._get_real_arguments(args, 2)
		accounts = gajim.contacts.keys()
		
		# if there is only one account in roster, take it as default
		if account:
			accounts = [account]
		else:
			accounts = gajim.contacts.keys()
		contact_exists = False
		for account in accounts:
			if gajim.contacts[account].has_key(jid):
				gajim.connections[account].unsubscribe(jid)
				for contact in gajim.contacts[account][jid]:
					gajim.interface.roster.remove_contact(contact, account)
				del gajim.contacts[account][jid]
				contact_exists = True
		return contact_exists
		
	def _is_first(self):
		if self.first_show:
			self.first_show = False
			return True
		return False

	def _get_real_arguments(self, args, desired_length):
		# supresses the first 'message' argument, which is set in dbus 0.23
		if dbus_support.version[1] == 20:
			args=args[1:]
		if desired_length > 0:
			args = list(args)
			args.extend([None] * (desired_length - len(args)))
			args = args[:desired_length]
		return args

	def _serialized_contacts(self, contacts):
		''' get info from list of Contact objects and create a serialized
		dict for sending it over dbus '''
		if not contacts:
			return None
		prim_contact = None # primary contact
		for contact in contacts:
			if prim_contact == None or contact.priority > prim_contact.priority:
				prim_contact = contact
		contact_dict = {}
		contact_dict['name'] = prim_contact.name
		contact_dict['show'] = prim_contact.show
		contact_dict['jid'] = prim_contact.jid
		if prim_contact.keyID:
			keyID = None
			if len(prim_contact.keyID) == 8:
				keyID = prim_contact.keyID
			elif len(prim_contact.keyID) == 16:
				keyID = prim_contact.keyID[8:]
			if keyID:
				contact_dict['openpgp'] = keyID
		contact_dict['resources'] = []
		for contact in contacts:
			contact_dict['resources'].append(tuple([contact.resource, 
				contact.priority, contact.status]))
		return repr(contact_dict)
	
	
	if dbus_support.version[1] >= 30 and dbus_support.version[1] <= 40:
		method = dbus.method
		signal = dbus.signal
	elif dbus_support.version[1] >= 41:
		method = dbus.service.method
		signal = dbus.service.signal

	if dbus_support.version[1] >= 30:
		# prevent using decorators, because they are not supported 
		# on python < 2.4
		# FIXME: use decorators when python2.3 (and dbus 0.23) is OOOOOOLD
		toggle_roster_appearance = method(INTERFACE)(toggle_roster_appearance)
		list_contacts = method(INTERFACE)(list_contacts)
		list_accounts = method(INTERFACE)(list_accounts)
		show_next_unread = method(INTERFACE)(show_next_unread)
		change_status = method(INTERFACE)(change_status)
		open_chat = method(INTERFACE)(open_chat)
		contact_info = method(INTERFACE)(contact_info)
		send_message = method(INTERFACE)(send_message)
		send_file = method(INTERFACE)(send_file)
		VcardInfo = signal(INTERFACE)(VcardInfo)
		prefs_list = method(INTERFACE)(prefs_list)
		prefs_put = method(INTERFACE)(prefs_put)
		prefs_del = method(INTERFACE)(prefs_del)
		prefs_store = method(INTERFACE)(prefs_store)
		remove_contact = method(INTERFACE)(remove_contact)
		add_contact = method(INTERFACE)(add_contact)
		get_status = method(INTERFACE)(get_status)
