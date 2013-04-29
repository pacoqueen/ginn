## groupchat_window.py
##
## Contributors for this file:
## - Yann Le Boulanger <asterix@lagaule.org>
## - Nikos Kouremenos <kourem@gmail.com>
## - Travis Shirk <travis@pobox.com>
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

import gtk
import gtk.glade
import pango
import gobject
import time
import os

import dialogs
import vcard
import chat
import cell_renderer_image
import gtkgui_helpers
import history_window
import tooltips

from gajim import Contact
from common import gajim
from common import helpers
from gettext import ngettext
from common import i18n

_ = i18n._
Q_ = i18n.Q_
APP = i18n.APP
gtk.glade.bindtextdomain(APP, i18n.DIR)
gtk.glade.textdomain(APP)

#(status_image, type, nick, shown_nick)
(
C_IMG, # image to show state (online, new message etc)
C_TYPE, # type of the row ('contact' or 'group')
C_NICK, # contact nickame or group name
C_TEXT, # text shown in the cellrenderer
) = range(4)

GTKGUI_GLADE = 'gtkgui.glade'

class GroupchatWindow(chat.Chat):
	'''Class for Groupchat window'''
	def __init__(self, room_jid, nick, account):
		# we check that on opening new windows
		self.always_compact_view = gajim.config.get('always_compact_view_gc')
		chat.Chat.__init__(self, account, 'groupchat_window')

		# alphanum sorted
		self.muc_cmds = ['ban', 'chat', 'query', 'clear', 'close', 'compact', 'help', 'invite',
			'join', 'kick', 'leave', 'me', 'msg', 'nick', 'part', 'say', 'topic']

		self.nicks = {} # our nick for each groupchat we are in
		self.list_treeview = {}
		self.subjects = {}
		self.name_labels = {}
		self.subject_tooltip = {}
		self.room_creation = {}
		self.nick_hits = {} # possible candidates for nick completion
		self.cmd_hits = {} # possible candidates for command completion
		self.last_key_tabs = {}
		self.hpaneds = {} # used for auto positioning
		# holds the iter's offset which points to the end of --- line per jid
		self.focus_out_end_iter_offset = {}
		self.allow_focus_out_line = {}
		self.hpaned_position = gajim.config.get('gc-hpaned-position')
		self.gc_refer_to_nick_char = gajim.config.get('gc_refer_to_nick_char')
		self.new_room(room_jid, nick)
		self.show_title()
		self.tooltip = tooltips.GCTooltip()


		# NOTE: if it not a window event, connect in new_room function
		signal_dict = {
'on_groupchat_window_destroy': self.on_groupchat_window_destroy,
'on_groupchat_window_delete_event': self.on_groupchat_window_delete_event,
'on_groupchat_window_focus_in_event': self.on_groupchat_window_focus_in_event,
'on_chat_notebook_key_press_event': self.on_chat_notebook_key_press_event,
'on_chat_notebook_switch_page': self.on_chat_notebook_switch_page,
		}

		self.xml.signal_autoconnect(signal_dict)

		# get size and position from config
		if gajim.config.get('saveposition') and \
			not gtkgui_helpers.one_window_opened('gc'):
			gtkgui_helpers.move_window(self.window,
				gajim.config.get('gc-x-position'),
				gajim.config.get('gc-y-position'))
			gtkgui_helpers.resize_window(self.window,
				gajim.config.get('gc-width'),
				gajim.config.get('gc-height'))
		self.window.show_all()

	def save_var(self, room_jid):
		if not room_jid in self.nicks:
			return {}
		return {
			'nick': self.nicks[room_jid],
			'model': self.list_treeview[room_jid].get_model(),
			'subject': self.subjects[room_jid],
			'contacts': gajim.gc_contacts[self.account][room_jid],
			'connected': gajim.gc_connected[self.account][room_jid],
		}

	def load_var(self, room_jid, var):
		if not self.xmls.has_key(room_jid):
			return
		self.list_treeview[room_jid].set_model(var['model'])
		self.list_treeview[room_jid].expand_all()
		self.set_subject(room_jid, var['subject'])
		self.subjects[room_jid] = var['subject']
		gajim.gc_contacts[self.account][room_jid] = var['contacts']
		gajim.gc_connected[self.account][room_jid] = var['connected']
		if gajim.gc_connected[self.account][room_jid]:
			self.got_connected(room_jid)

	def confirm_close(self, room_jid = None):
		'''Returns True if we confirm we want to close
		Returns False if we don't want to close anymore
		if room_jid is given, ask only for it else ask for all opened rooms'''
		# whether to ask for comfirmation before closing muc
		if gajim.config.get('confirm_close_muc'):
			names = []
			if not room_jid:
				for r_jid in self.xmls:
					if gajim.gc_connected[self.account][r_jid]:
						names.append(gajim.get_nick_from_jid(r_jid))
			else:
				names = [room_jid]

			rooms_no = len(names)
			if rooms_no >= 2: # if we are in many rooms
				pritext = _('Are you sure you want to leave rooms "%s"?') % ', '.join(names)
				sectext = _('If you close this window, you will be disconnected from these rooms.')

			elif rooms_no == 1: # just in one room
				pritext = _('Are you sure you want to leave room "%s"?') % names[0]
				sectext = _('If you close this window, you will be disconnected from this room.')

			if rooms_no > 0:
				dialog = dialogs.ConfirmationDialogCheck(pritext, sectext,
					_('Do _not ask me again'))

				if dialog.is_checked():
					gajim.config.set('confirm_close_muc', False)
					dialog.destroy()

				if dialog.get_response() != gtk.RESPONSE_OK:
					return False
		return True

	def on_groupchat_window_delete_event(self, widget, event):
		'''close window'''
		if not self.confirm_close():
			return True # stop propagation of the delete event
		for room_jid in self.xmls:
			if gajim.gc_connected[self.account][room_jid]:
				gajim.connections[self.account].send_gc_status(self.nicks[room_jid],
					room_jid, 'offline', 'offline')

		if gajim.config.get('saveposition'):
			# save window position and size
			gajim.config.set('gc-hpaned-position', self.hpaned_position)
			x, y = self.window.get_position()
			gajim.config.set('gc-x-position', x)
			gajim.config.set('gc-y-position', y)
			width, height = self.window.get_size()
			gajim.config.set('gc-width', width)
			gajim.config.set('gc-height', height)

	def on_groupchat_window_destroy(self, widget):
		chat.Chat.on_window_destroy(self, widget, 'gc')
		for room_jid in self.xmls:
			del gajim.gc_contacts[self.account][room_jid]
			del gajim.gc_connected[self.account][room_jid]

	def on_groupchat_window_focus_in_event(self, widget, event):
		'''When window gets focus'''
		room_jid = self.get_active_jid()
		self.allow_focus_out_line[room_jid] = True
		chat.Chat.on_chat_window_focus_in_event(self, widget, event)

	def check_and_possibly_add_focus_out_line(self, room_jid):
		'''checks and possibly adds focus out line for room_jid if it needs it
		and does not already have it as last event. If it goes to add this line
		it removes previous line first'''

		if room_jid == self.get_active_jid() and self.window.get_property('has-toplevel-focus'):
			# it's the current room and it's the focused window.
			# we have full focus (we are reading it!)
			return

		if not self.allow_focus_out_line[room_jid]:
			# if room did not receive focus-in from the last time we added
			# --- line then do not readd
			return

		print_focus_out_line = False
		textview = self.conversation_textviews[room_jid]
		buffer = textview.get_buffer()

		if self.focus_out_end_iter_offset[room_jid] is None:
			# this happens only first time we focus out on this room
			print_focus_out_line = True

		else:
			if self.focus_out_end_iter_offset[room_jid] != buffer.get_end_iter().get_offset():
				# this means after last-focus something was printed
				# (else end_iter's offset is the same as before)
				# only then print ---- line (eg. we avoid printing many following
				# ---- lines)
				print_focus_out_line = True

		if print_focus_out_line and buffer.get_char_count() > 0:
			buffer.begin_user_action()

			# remove previous focus out line if such focus out line exists
			if self.focus_out_end_iter_offset[room_jid] is not None:
				end_iter_for_previous_line = buffer.get_iter_at_offset(
					self.focus_out_end_iter_offset[room_jid])
				begin_iter_for_previous_line = end_iter_for_previous_line.copy()
				begin_iter_for_previous_line.backward_chars(2) # img_char+1 (the '\n')

				# remove focus out line
				buffer.delete(begin_iter_for_previous_line,
					end_iter_for_previous_line)

			# add the new focus out line
			path_to_file = os.path.join(gajim.DATA_DIR, 'pixmaps', 'muc_separator.png')
			focus_out_line_pixbuf = gtk.gdk.pixbuf_new_from_file(path_to_file)
			end_iter = buffer.get_end_iter()
			buffer.insert(end_iter, '\n')
			buffer.insert_pixbuf(end_iter, focus_out_line_pixbuf)

			end_iter = buffer.get_end_iter()
			before_img_iter = end_iter.copy()
			before_img_iter.backward_char() # one char back (an image also takes one char)
			buffer.apply_tag_by_name('focus-out-line', before_img_iter, end_iter)
			#FIXME: remove this workaround when bug is fixed
			# c http://bugzilla.gnome.org/show_bug.cgi?id=318569

			self.allow_focus_out_line[room_jid] = False

			# update the iter we hold to make comparison the next time
			self.focus_out_end_iter_offset[room_jid] = buffer.get_end_iter(
				).get_offset()

			buffer.end_user_action()

			# scroll to the end (via idle in case the scrollbar has appeared)
			gobject.idle_add(textview.scroll_to_end)

	def on_chat_notebook_key_press_event(self, widget, event):
		chat.Chat.on_chat_notebook_key_press_event(self, widget, event)

	def on_chat_notebook_switch_page(self, notebook, page, page_num):
		old_child = notebook.get_nth_page(notebook.get_current_page())
		new_child = notebook.get_nth_page(page_num)
		old_jid = ''
		new_jid = ''
		for room_jid in self.xmls:
			if self.childs[room_jid] == new_child:
				new_jid = room_jid
				self.redraw_tab(new_jid, 'active')
			elif self.childs[room_jid] == old_child:
				old_jid = room_jid
				self.redraw_tab(old_jid, 'active')
			if old_jid != '' and new_jid != '': # we found both jids
				break # so stop looping

		subject = self.subjects[new_jid]
		subject_escaped = gtkgui_helpers.escape_for_pango_markup(subject)
		new_jid_escaped = gtkgui_helpers.escape_for_pango_markup(new_jid)

		name_label = self.name_labels[new_jid]
		name_label.set_markup('<span weight="heavy" size="x-large">%s</span>\n%s'\
			% (new_jid_escaped, subject_escaped))
		event_box = name_label.get_parent()
		if subject == '':
			subject = _('This room has no subject')
		self.subject_tooltip[new_jid].set_tip(event_box, subject)

		if len(self.xmls) > 1 and old_jid != '': # if we have more than one tab
			# and we have the old_jid (eg we did NOT close the tab
			# but we just switched)
			# then add the focus-out line to the tab we are leaving
			self.check_and_possibly_add_focus_out_line(old_jid)
		chat.Chat.on_chat_notebook_switch_page(self, notebook, page, page_num)

	def get_role_iter(self, room_jid, role):
		model = self.list_treeview[room_jid].get_model()
		fin = False
		iter = model.get_iter_root()
		if not iter:
			return None
		while not fin:
			role_name = model[iter][C_NICK].decode('utf-8')
			if role == role_name:
				return iter
			iter = model.iter_next(iter)
			if not iter:
				fin = True
		return None

	def get_contact_iter(self, room_jid, nick):
		model = self.list_treeview[room_jid].get_model()
		fin = False
		role_iter = model.get_iter_root()
		if not role_iter:
			return None
		while not fin:
			fin2 = False
			user_iter = model.iter_children(role_iter)
			if not user_iter:
				fin2 = True
			while not fin2:
				if nick == model[user_iter][C_NICK].decode('utf-8'):
					return user_iter
				user_iter = model.iter_next(user_iter)
				if not user_iter:
					fin2 = True
			role_iter = model.iter_next(role_iter)
			if not role_iter:
				fin = True
		return None

	def get_nick_list(self, room_jid):
		'''get nicks of contacts in a room'''
		return gajim.gc_contacts[self.account][room_jid].keys()

	def remove_contact(self, room_jid, nick):
		'''Remove a user from the contacts_list'''
		model = self.list_treeview[room_jid].get_model()
		iter = self.get_contact_iter(room_jid, nick)
		if not iter:
			return
		if gajim.gc_contacts[self.account][room_jid].has_key(nick):
			del gajim.gc_contacts[self.account][room_jid][nick]
		parent_iter = model.iter_parent(iter)
		model.remove(iter)
		if model.iter_n_children(parent_iter) == 0:
			model.remove(parent_iter)

	def add_contact_to_roster(self, room_jid, nick, show, role, jid, affiliation, status):
		model = self.list_treeview[room_jid].get_model()
		resource = ''
		role_name = helpers.get_uf_role(role, plural = True)

		if jid:
			jids = jid.split('/', 1)
			j = jids[0]
			if len(jids) > 1:
				resource = jids[1]
		else:
			j = ''

		name = nick

		role_iter = self.get_role_iter(room_jid, role)
		if not role_iter:
			role_iter = model.append(None,
				(gajim.interface.roster.jabber_state_images['16']['closed'], 'role', role,
				'<b>%s</b>' % role_name))
		iter = model.append(role_iter, (None, 'contact', nick, name))
		if not gajim.gc_contacts[self.account][room_jid].has_key(nick):
			gajim.gc_contacts[self.account][room_jid][nick] = \
				Contact(jid = j, name = nick, show = show, resource = resource,
				role = role, affiliation = affiliation, status = status)
		self.draw_contact(room_jid, nick)
		if nick == self.nicks[room_jid]: # we became online
			self.got_connected(room_jid)
		self.list_treeview[room_jid].expand_row((model.get_path(role_iter)),
			False)
		return iter

	def draw_contact(self, room_jid, nick, selected=False, focus=False):
		iter = self.get_contact_iter(room_jid, nick)
		if not iter:
			return
		model = self.list_treeview[room_jid].get_model()
		contact = gajim.gc_contacts[self.account][room_jid][nick]
		state_images = gajim.interface.roster.jabber_state_images['16']
		if gajim.awaiting_events[self.account].has_key(room_jid + '/' + nick):
			image = state_images['message']
		else:
			image = state_images[contact.show]

		name = gtkgui_helpers.escape_for_pango_markup(contact.name)
		status = contact.status
		# add status msg, if not empty, under contact name in the treeview
		if status and gajim.config.get('show_status_msgs_in_roster'):
			status = status.strip()
			if status != '':
				status = gtkgui_helpers.reduce_chars_newlines(status, max_lines = 1)
				# escape markup entities and make them small italic and fg color
				color = gtkgui_helpers._get_fade_color(self.list_treeview[room_jid],
					selected, focus)
				colorstring = "#%04x%04x%04x" % (color.red, color.green, color.blue)
				name += '\n' '<span size="small" style="italic" foreground="%s">%s</span>'\
					% (colorstring, gtkgui_helpers.escape_for_pango_markup(status))

		model[iter][C_IMG] = image
		model[iter][C_TEXT] = name

	def draw_roster(self, room_jid):
		model = self.list_treeview[room_jid].get_model()
		model.clear()
		for nick in gajim.gc_contacts[self.account][room_jid]:
			contact = gajim.gc_contacts[self.account][room_jid][nick]
			fjid = contact.jid
			if contact.resource:
				fjid += '/' + contact.resource
			self.add_contact_to_roster(room_jid, nick, contact.show, contact.role,
				fjid, contact.affiliation, contact.status)

	def get_role(self, room_jid, nick):
		if gajim.gc_contacts[self.account][room_jid].has_key(nick):
			return gajim.gc_contacts[self.account][room_jid][nick].role
		else:
			return 'visitor'

	def draw_all_roster(self):
		for room_jid in self.list_treeview:
			self.draw_roster(room_jid)

	def chg_contact_status(self, room_jid, nick, show, status, role, affiliation,
		jid, reason, actor, statusCode, new_nick, account):
		'''When an occupant changes his or her status'''
		if show == 'invisible':
			return
		if not role:
			role = 'visitor'
		if not affiliation:
			affiliation = 'none'
		if show in ('offline', 'error'):
			if statusCode == '307':
				if actor is None: # do not print 'kicked by None'
					s = _('%(nick)s has been kicked: %(reason)s') % {
						'nick': nick,
						'reason': reason }
				else:
					s = _('%(nick)s has been kicked by %(who)s: %(reason)s') % {
						'nick': nick,
						'who': actor,
						'reason': reason }
				self.print_conversation(s, room_jid)
			elif statusCode == '301':
				if actor is None: # do not print 'banned by None'
					s = _('%(nick)s has been banned: %(reason)s') % {
						'nick': nick,
						'reason': reason }
				else:
					s = _('%(nick)s has been banned by %(who)s: %(reason)s') % {
						'nick': nick,
						'who': actor,
						'reason': reason }
				self.print_conversation(s, room_jid)
			elif statusCode == '303': # Someone changed his or her nick
				if nick == self.nicks[room_jid]: # We changed our nick
					self.nicks[room_jid] = new_nick
					s = _('You are now known as %s') % new_nick
				else:
					s = _('%s is now known as %s') % (nick, new_nick)
				self.print_conversation(s, room_jid)

			if not gajim.awaiting_events[self.account].has_key(
				room_jid + '/' + nick):
				self.remove_contact(room_jid, nick)
			else:
				c = gajim.gc_contacts[self.account][room_jid][nick]
				c.show = show
				c.status = status
			if nick == self.nicks[room_jid] and statusCode != '303': # We became offline
				self.got_disconnected(room_jid)
		else:
			iter = self.get_contact_iter(room_jid, nick)
			if not iter:
				iter = self.add_contact_to_roster(room_jid, nick, show, role, jid,
					affiliation, status)
			else:
				actual_role = self.get_role(room_jid, nick)
				if role != actual_role:
					self.remove_contact(room_jid, nick)
					self.add_contact_to_roster(room_jid, nick, show, role, jid,
						affiliation, status)
				else:
					c = gajim.gc_contacts[self.account][room_jid][nick]
					if c.show == show and c.status == status and \
						c.affiliation == affiliation: #no change
						return
					c.show = show
					c.affiliation = affiliation
					c.status = status
					self.draw_contact(room_jid, nick)
		if (time.time() - self.room_creation[room_jid]) > 30 and \
				nick != self.nicks[room_jid] and statusCode != '303':
			if show == 'offline':
				st = _('%s has left') % nick
			else:
				st = _('%s is now %s') % (nick, helpers.get_uf_show(show))
			if status:
				st += ' (' + status + ')'
			self.print_conversation(st, room_jid)

	def set_subject(self, room_jid, subject):
		self.subjects[room_jid] = subject
		name_label = self.name_labels[room_jid]
		full_subject = None

		subject = gtkgui_helpers.reduce_chars_newlines(subject, 0, 2)
		subject = gtkgui_helpers.escape_for_pango_markup(subject)
		name_label.set_markup(
		'<span weight="heavy" size="x-large">%s</span>\n%s' % (room_jid, subject))
		event_box = name_label.get_parent()
		if subject == '':
			subject = _('This room has no subject')

		if full_subject is not None:
			subject = full_subject # tooltip must always hold ALL the subject
		self.subject_tooltip[room_jid].set_tip(event_box, subject)

	def get_specific_unread(self, room_jid):
		# returns the number of the number of unread msgs
		# for room_jid & number of unread private msgs with each contact
		# that we have
		nb = 0
		for nick in self.get_nick_list(room_jid):
			fjid = room_jid + '/' + nick
			if gajim.awaiting_events[self.account].has_key(fjid):
				# gc can only have messages as event
				nb += len(gajim.awaiting_events[self.account][fjid])
		return nb

	def on_change_subject_menuitem_activate(self, widget):
		room_jid = self.get_active_jid()
		subject = self.subjects[room_jid]
		instance = dialogs.InputDialog(_('Changing Subject'),
			_('Please specify the new subject:'), subject)
		response = instance.get_response()
		if response == gtk.RESPONSE_OK:
			subject = instance.input_entry.get_text().decode('utf-8')
			gajim.connections[self.account].send_gc_subject(room_jid, subject)

	def on_change_nick_menuitem_activate(self, widget):
		room_jid = self.get_active_jid()
		nick = self.nicks[room_jid]
		title = _('Changing Nickname')
		prompt = _('Please specify the new nickname you want to use:')
		self.show_change_nick_input_dialog(title, prompt, nick, room_jid)

	def show_change_nick_input_dialog(self, title, prompt, proposed_nick = None,
		room_jid = None):
		'''asks user for new nick and on ok it sets it on room'''
		instance = dialogs.InputDialog(title, prompt, proposed_nick)
		response = instance.get_response()
		if response == gtk.RESPONSE_OK:
			nick = instance.input_entry.get_text().decode('utf-8')
			self.nicks[room_jid] = nick
			gajim.connections[self.account].change_gc_nick(room_jid, nick)

	def on_configure_room_menuitem_activate(self, widget):
		room_jid = self.get_active_jid()
		gajim.connections[self.account].request_gc_config(room_jid)

	def on_bookmark_room_menuitem_activate(self, widget):
		room_jid = self.get_active_jid()
		bm = {
				'name': room_jid,
				'jid': room_jid,
				'autojoin': '0',
				'password': '',
				'nick': self.nicks[room_jid]
			}

		for bookmark in gajim.connections[self.account].bookmarks:
			if bookmark['jid'] == bm['jid']:
				dialogs.ErrorDialog(
					_('Bookmark already set'),
					_('Room "%s" is already in your bookmarks.') %bm['jid']).\
						get_response()
				return

		gajim.connections[self.account].bookmarks.append(bm)
		gajim.connections[self.account].store_bookmarks()

		gajim.interface.roster.make_menu()

		dialogs.InformationDialog(
				_('Bookmark has been added successfully'),
				_('You can manage your bookmarks via Actions menu in your roster.'))

	def on_message_textview_key_press_event(self, widget, event):
		'''we use this cb instead of my_key_press to catch everything else
		that is not registered as binding (see message_textview.py)'''
		chat.Chat.on_message_textview_key_press_event(self, widget, event)

	def on_message_textview_mykeypress_event(self, widget, event_keyval,
	event_keymod):
		'''When a key is pressed:
		if enter is pressed without the shift key, message (if not empty) is sent
		and printed in the conversation. Tab does autocomplete in nicknames'''
		# NOTE: handles mykeypress which is custom signal connected to this
		# CB in new_room(). for this singal see message_textview.py
		room_jid = self.get_active_jid()
		message_buffer = widget.get_buffer()
		start_iter, end_iter = message_buffer.get_bounds()
		message = message_buffer.get_text(start_iter, end_iter,
			False).decode('utf-8')

		# construct event instance from binding
		event = gtk.gdk.Event(gtk.gdk.KEY_PRESS) # it's always a key-press here
		event.keyval = event_keyval
		event.state = event_keymod
		event.time = 0 # assign current time

		if event.keyval == gtk.keysyms.ISO_Left_Tab: # SHIFT + TAB
			if (event.state & gtk.gdk.CONTROL_MASK): # CTRL + SHIFT + TAB
				self.notebook.emit('key_press_event', event)
		elif event.keyval == gtk.keysyms.Tab: # TAB
			if event.state & gtk.gdk.CONTROL_MASK: # CTRL + TAB
				self.notebook.emit('key_press_event', event)
			else: # just TAB
				cursor_position = message_buffer.get_insert()
				end_iter = message_buffer.get_iter_at_mark(cursor_position)
				text = message_buffer.get_text(start_iter, end_iter,
					False).decode('utf-8')
				if not text or text.endswith(' '):
					# if we are nick cycling, last char will always be space
					if not self.last_key_tabs[room_jid]:
						return False

				splitted_text = text.split()
				# command completion
				if text.startswith('/') and len(splitted_text) == 1:
					text = splitted_text[0]
					if len(text) == 1: # user wants to cycle all commands
						self.cmd_hits[room_jid] = self.muc_cmds
					else:
						# cycle possible commands depending on what the user typed
						if self.last_key_tabs[room_jid] and \
								self.cmd_hits[room_jid][0].startswith(text.lstrip('/')):
							self.cmd_hits[room_jid].append(self.cmd_hits[room_jid][0])
							self.cmd_hits[room_jid].pop(0)
						else: # find possible commands
							self.cmd_hits[room_jid] = []
							for cmd in self.muc_cmds:
								if cmd.startswith(text.lstrip('/')):
									self.cmd_hits[room_jid].append(cmd)
					if len(self.cmd_hits[room_jid]):
						message_buffer.delete(start_iter, end_iter)
						message_buffer.insert_at_cursor('/' + \
							self.cmd_hits[room_jid][0] + ' ')
						self.last_key_tabs[room_jid] = True
					return True

				# nick completion
				# check if tab is pressed with empty message
				if len(splitted_text): # if there are any words
					begin = splitted_text[-1] # last word we typed

					if len(self.nick_hits[room_jid]) and \
							self.nick_hits[room_jid][0].startswith(begin.replace(
							self.gc_refer_to_nick_char, '')) and \
							self.last_key_tabs[room_jid]: # we should cycle
						self.nick_hits[room_jid].append(self.nick_hits[room_jid][0])
						self.nick_hits[room_jid].pop(0)
					else:
						self.nick_hits[room_jid] = [] # clear the hit list
						list_nick = self.get_nick_list(room_jid)
						for nick in list_nick:
							if nick.lower().startswith(begin.lower()): # the word is the begining of a nick
								self.nick_hits[room_jid].append(nick)
					if len(self.nick_hits[room_jid]):
						if len(splitted_text) == 1: # This is the 1st word of the line
							add = self.gc_refer_to_nick_char + ' '
						else:
							add = ' '
						start_iter = end_iter.copy()
						if self.last_key_tabs[room_jid] and begin.endswith(', '):
							# have to accomodate for the added space from last completion
							start_iter.backward_chars(len(begin) + 2)
						elif self.last_key_tabs[room_jid]:
							# have to accomodate for the added space from last completion
							start_iter.backward_chars(len(begin) + 1)
						else:
							start_iter.backward_chars(len(begin))

						message_buffer.delete(start_iter, end_iter)
						message_buffer.insert_at_cursor(self.nick_hits[room_jid][0] \
							+ add)
						self.last_key_tabs[room_jid] = True
						return True
				self.last_key_tabs[room_jid] = False
				return False
		elif event.keyval == gtk.keysyms.Return or \
			event.keyval == gtk.keysyms.KP_Enter: # ENTER
			if (event.state & gtk.gdk.SHIFT_MASK):
				self.last_key_tabs[room_jid] = False
				return False
			if gajim.config.get('send_on_ctrl_enter'):
				# here, we emulate GTK default action on ENTER (add new line)
				# normally I would add in keypress but it gets way to complex
				# to get instant result on changing this advanced setting
				if event.state == 0: # no ctrl, no shift just ENTER add newline
					end_iter = message_buffer.get_end_iter()
					message_buffer.insert_at_cursor('\n')
					send_message = False
				elif event.state & gtk.gdk.CONTROL_MASK: # CTRL + ENTER
					send_message = True
			else: # send on Enter, do newline on Ctrl Enter
				if event.state & gtk.gdk.CONTROL_MASK: # Ctrl + ENTER
					end_iter = message_buffer.get_end_iter()
					message_buffer.insert_at_cursor('\n')
					send_message = False
				else: # ENTER
					send_message = True
				
			if gajim.connections[self.account].connected < 2:
				# we are not connected
				dialogs.ErrorDialog(_('A connection is not available'),
					_('Your message can not be sent until you are connected.')).get_response()
				send_message = False

			if send_message:
				self.send_gc_message(message) # send the message
			return True
		elif event.keyval == gtk.keysyms.Up:
			if event.state & gtk.gdk.CONTROL_MASK: # Ctrl+UP
				self.sent_messages_scroll(room_jid, 'up', widget.get_buffer())
				return True # override the default gtk+ thing for ctrl+up
		elif event.keyval == gtk.keysyms.Down:
			if event.state & gtk.gdk.CONTROL_MASK: # Ctrl+Down
				self.sent_messages_scroll(room_jid, 'down', widget.get_buffer())
				return True # override the default gtk+ thing for ctrl+down

	def on_send_button_clicked(self, widget):
		'''When send button is pressed: send the current message'''
		room_jid = self.get_active_jid()
		message_textview = self.message_textviews[room_jid]
		message_buffer = message_textview.get_buffer()
		start_iter = message_buffer.get_start_iter()
		end_iter = message_buffer.get_end_iter()
		message = message_buffer.get_text(start_iter, end_iter, 0).decode('utf-8')

		# send the message
		self.send_gc_message(message)

	def send_gc_message(self, message):
		'''call this function to send our message'''
		if not message:
			return
		room_jid = self.get_active_jid()
		message_textview = self.message_textviews[room_jid]
		message_buffer = message_textview.get_buffer()
		conv_textview = self.conversation_textviews[room_jid]
		if message != '' or message != '\n':
			self.save_sent_message(room_jid, message)

			if message.startswith('/') and not message.startswith('/me'):
				message = message[1:]
				message_array = message.split(' ', 1)
				command = message_array.pop(0).lower()
				if message_array == ['']:
					message_array = []
				if command == 'clear':
					# clear the groupchat window
					conv_textview.clear()
					self.clear(message_textview)
				elif command == 'compact':
					# set compact mode
					self.set_compact_view(not self.compact_view_current_state)
					self.clear(message_textview)
				elif command == 'nick':
					# example: /nick foo
					if len(message_array):
						nick = message_array[0]
						gajim.connections[self.account].change_gc_nick(room_jid,
							nick)
						self.clear(message_textview)
					else:
						self.get_command_help(command)
				elif command == 'query' or command == 'chat':
					# Open a chat window to the specified nick
					# example: /query foo
					if len(message_array):
						nick = message_array.pop(0)
						nicks = self.get_nick_list(room_jid)
						if nick in nicks:
							self.on_send_pm(nick = nick)
							self.clear(message_textview)
						else:
							self.print_conversation(_('Nickname not found: %s') % nick,
								room_jid)
					else:
						self.get_command_help(command)
				elif command == 'msg':
					# Send a message to a nick.  Also opens a private message window.
					# example: /msg foo Hey, what's up?
					if len(message_array):
						message_array = message_array[0].split()
						nick = message_array.pop(0)
						room_nicks = self.get_nick_list(room_jid)
						if nick in room_nicks:
							privmsg = ' '.join(message_array)
							self.on_send_pm(nick=nick, msg=privmsg)
							self.clear(message_textview)
						else:
							self.print_conversation(_('Nickname not found: %s') % nick,
								room_jid)
					else:
						self.get_command_help(command)
				elif command == 'topic':
					# display or change the room topic
					# example: /topic : print topic
					# /topic foo : change topic to foo
					if len(message_array):
						new_topic = message_array.pop(0)
						gajim.connections[self.account].send_gc_subject(room_jid,
							new_topic)
					else:
						self.print_conversation(self.subjects[room_jid], room_jid)
					self.clear(message_textview)
				elif command == 'invite':
					# invite a user to a room for a reason
					# example: /invite user@example.com reason
					if len(message_array):
						message_array = message_array[0].split()
						invitee = message_array.pop(0)
						if invitee.find('@') >= 0:
							reason = ' '.join(message_array)
							gajim.connections[self.account].send_invite(room_jid,
								invitee, reason)
							s = _('Invited %(contact_jid)s to %(room_jid)s.') % {
								'contact_jid': invitee,
								'room_jid': room_jid}
							self.print_conversation(s, room_jid)
							self.clear(message_textview)
						else:
							#%s is something the user wrote but it is not a jid so we inform
							s = _('%s does not appear to be a valid JID') % invitee
							self.print_conversation(s, room_jid)
					else:
						self.get_command_help(command)
				elif command == 'join':
					# example: /join room@conference.example.com/nick
					if len(message_array):
						message_array = message_array[0]
						if message_array.find('@') >= 0:
							room, servernick = message_array.split('@')
							if servernick.find('/') >= 0:
								server, nick = servernick.split('/', 1)
							else:
								server = servernick
								nick = ''
							#join_gc window is needed in order to provide for password entry.
							if gajim.interface.instances[self.account].has_key('join_gc'):
								gajim.interface.instances[self.account]['join_gc'].\
									window.present()
							else:
								try:
									gajim.interface.instances[self.account]['join_gc'] =\
										dialogs.JoinGroupchatWindow(self.account,
											server = server, room = room, nick = nick)
								except RuntimeError:
									pass
							self.clear(message_textview)
						else:
							#%s is something the user wrote but it is not a jid so we inform
							s = _('%s does not appear to be a valid JID') % message_array
							self.print_conversation(s, room_jid)
					else:
						self.get_command_help(command)
				elif command == 'leave' or command == 'part' or command == 'close':
					# Leave the room and close the tab or window
					# FIXME: Sometimes this doesn't actually leave the room.  Why?
					reason = 'offline'
					if len(message_array):
						reason = message_array.pop(0)
					self.remove_tab(room_jid, reason)
				elif command == 'ban':
					if len(message_array):
						message_array = message_array[0].split()
						nick = message_array.pop(0)
						room_nicks = self.get_nick_list(room_jid)
						reason = ' '.join(message_array)
						if nick in room_nicks:
							ban_jid = gajim.construct_fjid(room_jid, nick)
							gajim.connections[self.account].gc_set_affiliation(room_jid,
								ban_jid, 'outcast', reason)
							self.clear(message_textview)
						elif nick.find('@') >= 0:
							gajim.connections[self.account].gc_set_affiliation(room_jid,
								nick, 'outcast', reason)
							self.clear(message_textview)
						else:
							self.print_conversation(_('Nickname not found: %s') % nick,
								room_jid)
					else:
						self.get_command_help(command)
				elif command == 'kick':
					if len(message_array):
						message_array = message_array[0].split()
						nick = message_array.pop(0)
						room_nicks = self.get_nick_list(room_jid)
						reason = ' '.join(message_array)
						if nick in room_nicks:
							gajim.connections[self.account].gc_set_role(room_jid, nick,
								'none', reason)
							self.clear(message_textview)
						else:
							self.print_conversation(_('Nickname not found: %s') % nick,
								room_jid)
					else:
						self.get_command_help(command)
				elif command == 'help':
					if len(message_array):
						subcommand = message_array.pop(0)
						self.get_command_help(subcommand)
					else:
						self.get_command_help(command)
					self.clear(message_textview)
				elif command == 'say':
					if len(message_array):
						gajim.connections[self.account].send_gc_message(room_jid,
							message[4:])
						self.clear(message_textview)
					else:
						self.get_command_help(command)
				else:
					self.print_conversation(
						_('No such command: /%s (if you want to sent this prefix it with /say)') % command,
						room_jid)
				return # don't print the command

		gajim.connections[self.account].send_gc_message(room_jid, message)
		message_buffer.set_text('')
		message_textview.grab_focus()

	def get_command_help(self, command):
		room_jid = self.get_active_jid()
		if command == 'help':
			self.print_conversation(_('Commands: %s') % self.muc_cmds, room_jid)
		elif command == 'ban':
			s = _('Usage: /%s <nickname|JID> [reason], bans the JID from the room.'
			' The nickname of an occupant may be substituted, but not if it contains "@".'
			' If the JID is currently in the room, he/she/it will also be kicked.'
			' Does NOT support spaces in nickname.') % command
			self.print_conversation(s, room_jid)
		elif command == 'chat' or command == 'query':
			self.print_conversation(_('Usage: /%s <nickname>, opens a private chat window \
to the specified occupant.') % command, room_jid)
		elif command == 'clear':
			self.print_conversation(_('Usage: /%s, clears the text window.') % command,
				room_jid)
		elif command == 'close' or command == 'leave' or command == 'part':
			self.print_conversation(_('Usage: /%s [reason], closes the current window \
or tab, displaying reason if specified.') % command, room_jid)
		elif command == 'compact':
			self.print_conversation(_('Usage: /%s, sets the groupchat window to \
compact mode.') % command, room_jid)
		elif command == 'invite':
			self.print_conversation(_('Usage: /%s <JID> [reason], invites JID to the \
current room, optionally providing a reason.') % command, room_jid)
		elif command == 'join':
			self.print_conversation(_('Usage: /%s <room>@<server>[/nickname], offers to \
join room@server optionally using specified nickname.') % command, room_jid)
		elif command == 'kick':
			self.print_conversation(_('Usage: /%s <nickname> [reason], removes the \
occupant specified by nickname from the room and optionally displays a \
reason. Does NOT support spaces in nickname.') % command, room_jid)
		elif command == 'me':
			self.print_conversation(_('Usage: /%s <action>, sends action to the \
current room. Use third person. (e.g. /%s explodes.)') %
				(command, command), room_jid)
		elif command == 'msg':
			s = _('Usage: /%s <nickname> [message], opens a private message window and sends message to the occupant specified by nickname.') % command
			self.print_conversation(s, room_jid)
		elif command == 'nick':
			s = _('Usage: /%s <nickname>, changes your nickname in current room.') % command
			self.print_conversation(s, room_jid)
		elif command == 'topic':
			self.print_conversation(_('Usage: /%s [topic], displays or updates the \
current room topic.') % command, room_jid)
		elif command == 'say':
			self.print_conversation(_('Usage: /%s <message>, sends a message without looking for other commands.') % command, room_jid)
		else:
			self.print_conversation(_('No help info for /%s') % command, room_jid)

	def print_conversation(self, text, room_jid, contact = '', tim = None):
		'''Print a line in the conversation:
		if contact is set: it's a message from someone
		if contact is not set: it's a message from the server or help'''
		if isinstance(text, str):
			text = unicode(text, 'utf-8')
		other_tags_for_name = []
		other_tags_for_text = []
		if contact:
			if contact == self.nicks[room_jid]: # it's us
				kind = 'outgoing'
			else:
				kind = 'incoming'
				# muc-specific chatstate
				self.redraw_tab(room_jid, 'newmsg')
		else:
			kind = 'status'


		nick = self.nicks[room_jid]

		if kind == 'incoming': # it's a message NOT from us
			# highlighting and sounds
			(highlight, sound) = self.highlighting_for_message(text, nick, tim)
			if highlight:
				self.redraw_tab(room_jid, 'attention') # muc-specific chatstate
				other_tags_for_name.append('bold')
				other_tags_for_text.append('marked')
			if sound == 'received':
				helpers.play_sound('muc_message_received')
			elif sound == 'highlight':
				helpers.play_sound('muc_message_highlight')

			self.check_and_possibly_add_focus_out_line(room_jid)

		chat.Chat.print_conversation_line(self, text, room_jid, kind, contact,
			tim, other_tags_for_name, [], other_tags_for_text)

	def highlighting_for_message(self, text, nick, tim):
		'''Returns a 2-Tuple. The first says whether or not to highlight the
		text, the second, what sound to play.'''
		highlight, sound = (None, None)

		# Do we play a sound on every muc message?
		if gajim.config.get_per('soundevents', 'muc_message_received', 'enabled'):
			if gajim.config.get('notify_on_all_muc_messages'):
				sound = 'received'

		# Are any of the defined highlighting words in the text?
		if self.needs_visual_notification(text, nick):
			highlight = True
			if gajim.config.get_per('soundevents', 'muc_message_highlight',
									'enabled'):
				sound = 'highlight'

		# Is it a history message? Don't want sound-floods when we join.
		if tim != time.localtime():
			sound = None

		return (highlight, sound)

	def needs_visual_notification(self, text, nick):
		'''checks text to see whether any of the words in (muc_highlight_words
		and nick) appear.'''

		special_words = gajim.config.get('muc_highlight_words').split(';')
		special_words.append(nick)
		# Strip empties: ''.split(';') == [''] and would highlight everything.
		# Also lowercase everything for case insensitive compare.
		special_words = [word.lower() for word in special_words if word]
		text = text.lower()

		text_splitted = text.split()
		for word in text_splitted: # get each word of the text
			for special_word in special_words:
				if word.startswith(special_word):
					return True

		return False

	def kick(self, widget, room_jid, nick):
		'''kick a user'''
		# ask for reason
		instance = dialogs.InputDialog(_('Kicking %s') % nick,
			_('You may specify a reason below:'))
		response = instance.get_response()
		if response == gtk.RESPONSE_OK:
			reason = instance.input_entry.get_text().decode('utf-8')
		else:
			return # stop kicking procedure
		gajim.connections[self.account].gc_set_role(room_jid, nick, 'none',
			reason)

	def grant_voice(self, widget, room_jid, nick):
		'''grant voice privilege to a user'''
		gajim.connections[self.account].gc_set_role(room_jid, nick, 'participant')

	def revoke_voice(self, widget, room_jid, nick):
		'''revoke voice privilege to a user'''
		gajim.connections[self.account].gc_set_role(room_jid, nick, 'visitor')

	def grant_moderator(self, widget, room_jid, nick):
		'''grant moderator privilege to a user'''
		gajim.connections[self.account].gc_set_role(room_jid, nick, 'moderator')

	def revoke_moderator(self, widget, room_jid, nick):
		'''revoke moderator privilege to a user'''
		gajim.connections[self.account].gc_set_role(room_jid, nick, 'participant')

	def ban(self, widget, room_jid, jid):
		'''ban a user'''
		# to ban we know the real jid. so jid is not fakejid
		nick = gajim.get_nick_from_jid(jid)
		# ask for reason
		instance = dialogs.InputDialog(_('Banning %s') % nick,
			_('You may specify a reason below:'))
		response = instance.get_response()
		if response == gtk.RESPONSE_OK:
			reason = instance.input_entry.get_text().decode('utf-8')
		else:
			return # stop banning procedure
		gajim.connections[self.account].gc_set_affiliation(room_jid, jid,
			'outcast', reason)

	def grant_membership(self, widget, room_jid, jid):
		'''grant membership privilege to a user'''
		gajim.connections[self.account].gc_set_affiliation(room_jid, jid,
			'member')

	def revoke_membership(self, widget, room_jid, jid):
		'''revoke membership privilege to a user'''
		gajim.connections[self.account].gc_set_affiliation(room_jid, jid,
			'none')

	def grant_admin(self, widget, room_jid, jid):
		'''grant administrative privilege to a user'''
		gajim.connections[self.account].gc_set_affiliation(room_jid, jid, 'admin')

	def revoke_admin(self, widget, room_jid, jid):
		'''revoke administrative privilege to a user'''
		gajim.connections[self.account].gc_set_affiliation(room_jid, jid,
			'member')

	def grant_owner(self, widget, room_jid, jid):
		'''grant owner privilege to a user'''
		gajim.connections[self.account].gc_set_affiliation(room_jid, jid, 'owner')

	def revoke_owner(self, widget, room_jid, jid):
		'''revoke owner privilege to a user'''
		gajim.connections[self.account].gc_set_affiliation(room_jid, jid, 'admin')

	def on_info(self, widget, room_jid, nick):
		'''Call vcard_information_window class to display user's information'''
		c = gajim.gc_contacts[self.account][room_jid][nick]
		if c.jid and c.resource:
			# on GC, we know resource only if we're mod and up
			jid = c.jid
			fjid = c.jid + '/' + c.resource
		else:
			fjid = gajim.construct_fjid(room_jid, nick)
			jid = fjid
		if gajim.interface.instances[self.account]['infos'].has_key(jid):
			gajim.interface.instances[self.account]['infos'][jid].window.present()
		else:
			# we copy contact because c.jid must contain the fakeJid for vcard
			c2 = Contact(jid = jid, name = c.name, groups = c.groups,
				show = c.show, status = c.status, sub = c.sub,
				resource = c.resource, role = c.role, affiliation = c.affiliation)
			gajim.interface.instances[self.account]['infos'][jid] = \
				vcard.VcardWindow(c2, self.account, False)

	def on_history(self, widget, room_jid, nick):
		jid = gajim.construct_fjid(room_jid, nick)
		self.on_history_menuitem_clicked(jid = jid)

	def on_add_to_roster(self, widget, jid):
		dialogs.AddNewContactWindow(self.account, jid)

	def on_send_pm(self, widget=None, model=None, iter=None, nick=None, msg=None):
		'''opens a chat window and msg is not None sends private message to a
		contact in a room'''
		if nick is None:
			nick = model[iter][C_NICK].decode('utf-8')
		room_jid = self.get_active_jid()
		fjid = gajim.construct_fjid(room_jid, nick) # 'fake' jid
		if not gajim.interface.instances[self.account]['chats'].has_key(fjid):
			show = gajim.gc_contacts[self.account][room_jid][nick].show
			u = Contact(jid = fjid, name =  nick, groups = ['none'], show = show,
				sub = 'none')
			gajim.interface.roster.new_chat(u, self.account)

		#make active here in case we need to send a message
		gajim.interface.instances[self.account]['chats'][fjid].set_active_tab(fjid)

		if msg:
			gajim.interface.instances[self.account]['chats'][fjid].send_message(msg)
		gajim.interface.instances[self.account]['chats'][fjid].window.present()

	def on_voice_checkmenuitem_activate(self, widget, room_jid, nick):
		if widget.get_active():
			self.grant_voice(widget, room_jid, nick)
		else:
			self.revoke_voice(widget, room_jid, nick)

	def on_moderator_checkmenuitem_activate(self, widget, room_jid, nick):
		if widget.get_active():
			self.grant_moderator(widget, room_jid, nick)
		else:
			self.revoke_moderator(widget, room_jid, nick)

	def on_member_checkmenuitem_activate(self, widget, room_jid, jid):
		if widget.get_active():
			self.grant_membership(widget, room_jid, jid)
		else:
			self.revoke_membership(widget, room_jid, jid)

	def on_admin_checkmenuitem_activate(self, widget, room_jid, jid):
		if widget.get_active():
			self.grant_admin(widget, room_jid, jid)
		else:
			self.revoke_admin(widget, room_jid, jid)

	def on_owner_checkmenuitem_activate(self, widget, room_jid, jid):
		if widget.get_active():
			self.grant_owner(widget, room_jid, jid)
		else:
			self.revoke_owner(widget, room_jid, jid)

	def mk_menu(self, room_jid, event, iter):
		'''Make contact's popup menu'''
		model = self.list_treeview[room_jid].get_model()
		nick = model[iter][C_NICK].decode('utf-8')
		c = gajim.gc_contacts[self.account][room_jid][nick]
		jid = c.jid
		target_affiliation = c.affiliation
		target_role = c.role

		# looking for user's affiliation and role
		user_nick = self.nicks[room_jid]
		user_affiliation = gajim.gc_contacts[self.account][room_jid][user_nick].\
			affiliation
		user_role = self.get_role(room_jid, user_nick)

		# making menu from glade
		xml = gtk.glade.XML(GTKGUI_GLADE, 'gc_occupants_menu', APP)

		# these conditions were taken from JEP 0045
		item = xml.get_widget('kick_menuitem')
		item.connect('activate', self.kick, room_jid, nick)
		if user_role != 'moderator' or \
			(user_affiliation == 'admin' and target_affiliation == 'owner') or \
			(user_affiliation == 'member' and target_affiliation in ('admin', 'owner')) or \
			(user_affiliation == 'none' and target_affiliation != 'none'):
			item.set_sensitive(False)

		item = xml.get_widget('voice_checkmenuitem')
		item.set_active(target_role != 'visitor')
		if user_role != 'moderator' or \
			user_affiliation == 'none' or \
			(user_affiliation=='member' and target_affiliation!='none') or \
			target_affiliation in ('admin', 'owner'):
			item.set_sensitive(False)
		item.connect('activate', self.on_voice_checkmenuitem_activate, room_jid,
			nick)

		item = xml.get_widget('moderator_checkmenuitem')
		item.set_active(target_role == 'moderator')
		if not user_affiliation in ('admin', 'owner') or \
			target_affiliation in ('admin', 'owner'):
			item.set_sensitive(False)
		item.connect('activate', self.on_moderator_checkmenuitem_activate,
			room_jid, nick)

		item = xml.get_widget('ban_menuitem')
		if not user_affiliation in ('admin', 'owner') or \
			(target_affiliation in ('admin', 'owner') and\
			user_affiliation != 'owner'):
			item.set_sensitive(False)
		item.connect('activate', self.ban, room_jid, jid)

		item = xml.get_widget('member_checkmenuitem')
		item.set_active(target_affiliation != 'none')
		if not user_affiliation in ('admin', 'owner') or \
			(user_affiliation != 'owner' and target_affiliation in ('admin','owner')):
			item.set_sensitive(False)
		item.connect('activate', self.on_member_checkmenuitem_activate,
			room_jid, jid)

		item = xml.get_widget('admin_checkmenuitem')
		item.set_active(target_affiliation in ('admin', 'owner'))
		if not user_affiliation == 'owner':
			item.set_sensitive(False)
		item.connect('activate', self.on_admin_checkmenuitem_activate,
			room_jid, jid)

		item = xml.get_widget('owner_checkmenuitem')
		item.set_active(target_affiliation == 'owner')
		if not user_affiliation == 'owner':
			item.set_sensitive(False)
		item.connect('activate', self.on_owner_checkmenuitem_activate,
			room_jid, jid)

		item = xml.get_widget('information_menuitem')
		item.connect('activate', self.on_info, room_jid, nick)

		item = xml.get_widget('history_menuitem')
		item.connect('activate', self.on_history, room_jid, nick)

		item = xml.get_widget('add_to_roster_menuitem')
		if not jid:
			item.set_sensitive(False)
		item.connect('activate', self.on_add_to_roster, jid)

		item = xml.get_widget('send_private_message_menuitem')
		item.connect('activate', self.on_send_pm, model, iter)

		# show the popup now!
		menu = xml.get_widget('gc_occupants_menu')
		menu.popup(None, None, None, event.button, event.time)
		menu.show_all()

	def remove_tab(self, room_jid, reason = 'offline'):
		if not self.confirm_close(room_jid):
			return

		chat.Chat.remove_tab(self, room_jid, 'gc')
		if len(self.xmls) > 0:
			gajim.connections[self.account].send_gc_status(self.nicks[room_jid],
				room_jid, show='offline', status=reason)
		del self.nicks[room_jid]
		# They can already be removed by the destroy function
		if gajim.gc_contacts[self.account].has_key(room_jid):
			del gajim.gc_contacts[self.account][room_jid]
			del gajim.gc_connected[self.account][room_jid]
		del self.list_treeview[room_jid]
		del self.subjects[room_jid]
		del self.name_labels[room_jid]
		del self.hpaneds[room_jid]

	def got_connected(self, room_jid):
		gajim.gc_connected[self.account][room_jid] = True
		message_textview = self.message_textviews[room_jid]
		message_textview.set_sensitive(True)
		self.xmls[room_jid].get_widget('send_button').set_sensitive(True)

	def got_disconnected(self, room_jid):
		model = self.list_treeview[room_jid].get_model()
		model.clear()
		gajim.gc_contacts[self.account][room_jid] = {}
		gajim.gc_connected[self.account][room_jid] = False
		message_textview = self.message_textviews[room_jid]
		message_textview.set_sensitive(False)
		self.xmls[room_jid].get_widget('send_button').set_sensitive(False)

	def iter_contact_rows(self, room_jid):
		'''iterate over all contact rows in the tree model'''
		model = self.list_treeview[room_jid].get_model()
		role_iter = model.get_iter_root()
		while role_iter:
			contact_iter = model.iter_children(role_iter)
			while contact_iter:
				yield model[contact_iter]
				contact_iter = model.iter_next(contact_iter)
			role_iter = model.iter_next(role_iter)

	def on_list_treeview_style_set(self, treeview, style):
		'''When style (theme) changes, redraw all contacts'''
		# Get the room_jid from treeview
		for room_jid in self.list_treeview:
			if self.list_treeview[room_jid] == treeview:
				break
		for contact in self.iter_contact_rows(room_jid):
			nick = contact[C_NICK].decode('utf-8')
			self.draw_contact(room_jid, nick)

	def on_list_treeview_selection_changed(self, selection):
		model, selected_iter = selection.get_selected()
		# get room_jid from model
		for room_jid in self.list_treeview:
			mod = self.list_treeview[room_jid].get_model()
			if model == mod:
				break
		if self._last_selected_contact is not None:
			# update unselected row
			room_jid, nick = self._last_selected_contact
			# last selected can be in a closed room, so prevent KeyError
			if room_jid in self.list_treeview.keys():
				self.draw_contact(room_jid, nick)
		if selected_iter is None:
			self._last_selected_contact = None
			return
		contact = model[selected_iter]
		nick = contact[C_NICK].decode('utf-8')
		self._last_selected_contact = (room_jid, nick)
		if contact[C_TYPE] != 'contact':
			return
		self.draw_contact(room_jid, nick, selected=True, focus=True)

	def new_room(self, room_jid, nick):
		self.names[room_jid] = room_jid.split('@')[0]
		self.xmls[room_jid] = gtk.glade.XML(GTKGUI_GLADE, 'gc_vbox', APP)
		self.childs[room_jid] = self.xmls[room_jid].get_widget('gc_vbox')
		self.nicks[room_jid] = nick
		self.subjects[room_jid] = ''
		self.room_creation[room_jid] = time.time()
		self.nick_hits[room_jid] = []
		self.cmd_hits[room_jid] = []
		self.focus_out_end_iter_offset[room_jid] = None
		self.allow_focus_out_line[room_jid] = True
		self.last_key_tabs[room_jid] = False
		self.hpaneds[room_jid] = self.xmls[room_jid].get_widget('hpaned')
		list_treeview = self.list_treeview[room_jid] = self.xmls[room_jid].get_widget(
			'list_treeview')
		list_treeview.get_selection().connect('changed',
			self.on_list_treeview_selection_changed)
		list_treeview.connect('style-set', self.on_list_treeview_style_set)
		self._last_selected_contact = None # None or holds jid, account tupple

		self.subject_tooltip[room_jid] = gtk.Tooltips()

		chat.Chat.new_tab(self, room_jid)

		# we want to know when the the widget resizes, because that is
		# an indication that the hpaned has moved...
		# FIXME: Find a better indicator that the hpaned has moved.
		self.list_treeview[room_jid].connect('size-allocate',
			self.on_treeview_size_allocate)
		conv_textview = self.conversation_textviews[room_jid]
		self.name_labels[room_jid] = self.xmls[room_jid].get_widget(
			'banner_name_label')
		self.paint_banner(room_jid)

		# connect the menuitems to their respective functions
		xm = gtk.glade.XML(GTKGUI_GLADE, 'gc_popup_menu', APP)
		xm.signal_autoconnect(self)
		self.gc_popup_menu = xm.get_widget('gc_popup_menu')

		#status_image, type, nickname, shown_nick
		store = gtk.TreeStore(gtk.Image, str, str, str)
		store.set_sort_column_id(C_TEXT, gtk.SORT_ASCENDING)
		column = gtk.TreeViewColumn('contacts')
		renderer_image = cell_renderer_image.CellRendererImage()
		renderer_image.set_property('width', 20)
		column.pack_start(renderer_image, expand = False)
		column.add_attribute(renderer_image, 'image', 0)
		renderer_text = gtk.CellRendererText()
		column.pack_start(renderer_text, expand = True)
		column.set_attributes(renderer_text, markup = C_TEXT)
		column.set_cell_data_func(renderer_image, self.tree_cell_data_func, None)
		column.set_cell_data_func(renderer_text, self.tree_cell_data_func, None)

		self.list_treeview[room_jid].append_column(column)
		self.list_treeview[room_jid].set_model(store)

		# workaround to avoid gtk arrows to be shown
		column = gtk.TreeViewColumn() # 2nd COLUMN
		renderer = gtk.CellRendererPixbuf()
		column.pack_start(renderer, expand = False)
		self.list_treeview[room_jid].append_column(column)
		column.set_visible(False)
		self.list_treeview[room_jid].set_expander_column(column)

		# set the position of the current hpaned
		self.hpaneds[room_jid] = self.xmls[room_jid].get_widget('hpaned')
		self.hpaneds[room_jid].set_position(self.hpaned_position)

		self.redraw_tab(room_jid)
		self.show_title()
		# set an empty subject to show the room_jid
		self.set_subject(room_jid, '')
		self.got_disconnected(room_jid) #init some variables
		conv_textview.grab_focus()
		self.childs[room_jid].show_all()

	def on_message(self, room_jid, nick, msg, tim):
		if not nick:
			# message from server
			self.print_conversation(msg, room_jid, tim = tim)
		else:
			# message from someone
			self.print_conversation(msg, room_jid, nick, tim)

	def on_private_message(self, room_jid, nick, msg, tim):
		# Do we have a queue?
		fjid = room_jid + '/' + nick
		qs = gajim.awaiting_events[self.account]
		no_queue = True
		if qs.has_key(fjid):
			no_queue = False

		# We print if window is opened
		if gajim.interface.instances[self.account]['chats'].has_key(fjid):
			chat_win = gajim.interface.instances[self.account]['chats'][fjid]
			chat_win.print_conversation(msg, fjid, tim = tim)
			return

		if no_queue:
			qs[fjid] = []
		qs[fjid].append(('chat', (msg, '', 'incoming', tim, False, '')))
		self.nb_unread[room_jid] += 1

		autopopup = gajim.config.get('autopopup')
		autopopupaway = gajim.config.get('autopopupaway')
		iter = self.get_contact_iter(room_jid, nick)
		path = self.list_treeview[room_jid].get_model().get_path(iter)
		if not autopopup or ( not autopopupaway and \
			gajim.connections[self.account].connected > 2):
			if no_queue: # We didn't have a queue: we change icons
				model = self.list_treeview[room_jid].get_model()
				state_images = gajim.interface.roster.get_appropriate_state_images(room_jid)
				image = state_images['message']
				model[iter][C_IMG] = image
				if gajim.interface.systray_enabled:
					gajim.interface.systray.add_jid(fjid, self.account, 'pm')
			self.show_title()
		else:
			show = gajim.gc_contacts[self.account][room_jid][nick].show
			c = Contact(jid = fjid, name = nick, groups = ['none'], show = show,
				ask = 'none')
			gajim.interface.roster.new_chat(c, self.account)
		# Scroll to line
		self.list_treeview[room_jid].expand_row(path[0:1], False)
		self.list_treeview[room_jid].scroll_to_cell(path)
		self.list_treeview[room_jid].set_cursor(path)


	def set_state_image(self, jid):
		# FIXME: Tab notifications?
		pass

	def on_list_treeview_motion_notify_event(self, widget, event):
		model = widget.get_model()
		props = widget.get_path_at_pos(int(event.x), int(event.y))
		if self.tooltip.timeout > 0:
			if not props or self.tooltip.id != props[0]:
				self.tooltip.hide_tooltip()
		if props:
			[row, col, x, y] = props
			iter = None
			try:
				iter = model.get_iter(row)
			except:
				self.tooltip.hide_tooltip()
				return
			room_jid = self.get_active_jid()
			typ = model[iter][C_TYPE].decode('utf-8')
			if typ == 'contact':
				account = self.account

				if self.tooltip.timeout == 0 or self.tooltip.id != props[0]:
					self.tooltip.id = row
					nick = model[iter][C_NICK].decode('utf-8')
					self.tooltip.timeout = gobject.timeout_add(500,
						self.show_tooltip, gajim.gc_contacts[account][room_jid][nick])

	def on_list_treeview_leave_notify_event(self, widget, event):
		model = widget.get_model()
		props = widget.get_path_at_pos(int(event.x), int(event.y))
		if self.tooltip.timeout > 0:
			if not props or self.tooltip.id == props[0]:
				self.tooltip.hide_tooltip()

	def show_tooltip(self, contact):
		room_jid = self.get_active_jid()
		pointer = self.list_treeview[room_jid].get_pointer()
		props = self.list_treeview[room_jid].get_path_at_pos(pointer[0], pointer[1])
		if props and self.tooltip.id == props[0]:
			# check if the current pointer is at the same path
			# as it was before setting the timeout
			rect =  self.list_treeview[room_jid].get_cell_area(props[0],props[1])
			position = self.list_treeview[room_jid].window.get_origin()
			pointer = self.window.get_pointer()
			self.tooltip.show_tooltip(contact, (0, rect.height),
				(self.window.get_screen().get_display().get_pointer()[1],
				position[1] + rect.y))
		else:
			self.tooltip.hide_tooltip()

	def on_treeview_size_allocate(self, widget, allocation):
		'''The MUC treeview has resized. Move the hpaneds in all tabs to match'''
		thisroom_jid = self.get_active_jid()
		self.hpaned_position = self.hpaneds[thisroom_jid].get_position()
		for room_jid in self.xmls:
			self.hpaneds[room_jid].set_position(self.hpaned_position)

	def tree_cell_data_func(self, column, renderer, model, iter, data=None):
		theme = gajim.config.get('roster_theme')
		if model.iter_parent(iter):
			bgcolor = gajim.config.get_per('themes', theme, 'contactbgcolor')
		else: # it is root (eg. group)
			bgcolor = gajim.config.get_per('themes', theme, 'groupbgcolor')
		if bgcolor:
			renderer.set_property('cell-background', bgcolor)
		else:
			renderer.set_property('cell-background', None)

	def on_list_treeview_button_press_event(self, widget, event):
		'''popup user's group's or agent menu'''
		room_jid = self.get_active_jid()
		if event.button == 3: # right click
			try:
				path, column, x, y = widget.get_path_at_pos(int(event.x),
					int(event.y))
			except TypeError:
				widget.get_selection().unselect_all()
				return
			widget.get_selection().select_path(path)
			model = widget.get_model()
			iter = model.get_iter(path)
			if len(path) == 2:
				self.mk_menu(room_jid, event, iter)
			return True

		elif event.button == 2: # middle click
			try:
				path, column, x, y = widget.get_path_at_pos(int(event.x),
					int(event.y))
			except TypeError:
				widget.get_selection().unselect_all()
				return
			widget.get_selection().select_path(path)
			model = widget.get_model()
			iter = model.get_iter(path)
			if len(path) == 2:
				nick = model[iter][C_NICK].decode('utf-8')
				fjid = gajim.construct_fjid(room_jid, nick)
				if not gajim.interface.instances[self.account]['chats'].has_key(fjid):
					show = gajim.gc_contacts[self.account][room_jid][nick].show
					u = Contact(jid = fjid, name = nick, groups = ['none'],
						show = show, sub = 'none')
					gajim.interface.roster.new_chat(u, self.account)
				gajim.interface.instances[self.account]['chats'][fjid].set_active_tab(fjid)
				gajim.interface.instances[self.account]['chats'][fjid].window.present()
			return True

		elif event.button == 1: # left click
			try:
				path, column, x, y = widget.get_path_at_pos(int(event.x),
					int(event.y))
			except TypeError:
				widget.get_selection().unselect_all()
				return

			model = widget.get_model()
			iter = model.get_iter(path)
			nick = model[iter][C_NICK].decode('utf-8')
			if not nick in gajim.gc_contacts[self.account][room_jid]: #it's a group
				if x < 20: # first cell in 1st column (the arrow SINGLE clicked)
					if (widget.row_expanded(path)):
						widget.collapse_row(path)
					else:
						widget.expand_row(path, False)

	def on_list_treeview_key_press_event(self, widget, event):
		if event.keyval == gtk.keysyms.Escape:
			widget.get_selection().unselect_all()

	def on_list_treeview_row_activated(self, widget, path, col = 0):
		'''When an iter is double clicked: open the chat window'''
		model = widget.get_model()
		iter = model.get_iter(path)
		if len(path) == 1: # It's a group
			if (widget.row_expanded(path)):
				widget.collapse_row(path)
			else:
				widget.expand_row(path, False)
		else: # We want to send a private message
			room_jid = self.get_active_jid()
			nick = model[iter][C_NICK].decode('utf-8')
			jid = gajim.construct_fjid(room_jid, nick)
			if not gajim.interface.instances[self.account]['chats'].has_key(jid):
				show = gajim.gc_contacts[self.account][room_jid][nick].show
				contact = Contact(jid = jid, name = nick, groups = ['none'],
					show = show, sub = 'none')
				gajim.interface.roster.new_chat(contact, self.account)
				jid = contact.jid
			gajim.interface.instances[self.account]['chats'][jid].set_active_tab(jid)
			gajim.interface.instances[self.account]['chats'][jid].window.present()

	def on_list_treeview_row_expanded(self, widget, iter, path):
		'''When a row is expanded: change the icon of the arrow'''
		model = widget.get_model()
		image = gajim.interface.roster.jabber_state_images['16']['opened']
		model[iter][C_IMG] = image

	def on_list_treeview_row_collapsed(self, widget, iter, path):
		'''When a row is collapsed: change the icon of the arrow'''
		model = widget.get_model()
		image = gajim.interface.roster.jabber_state_images['16']['closed']
		model[iter][C_IMG] = image
