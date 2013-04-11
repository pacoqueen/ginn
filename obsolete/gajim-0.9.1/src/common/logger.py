# -*- coding: utf-8 -*-
## logger.py
##
## Contributors for this file:
## - Yann Le Boulanger <asterix@lagaule.org>
## - Nikos Kouremenos <kourem@gmail.com>
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


# XXX Modificado por queen para deshabilitar el log y que así no necesite psqlite para funcionar.
# XXX Modificado para que vuelva a usar logger.
# OJO: Necesitará entonces psqlite y gnupg en los clientes (qué remedio).

import os
import sys
import time
import datetime

import exceptions
import i18n
_ = i18n._

try:
    from pysqlite2 import dbapi2 as sqlite
except ImportError:
    raise exceptions.PysqliteNotAvailable
#    pass

if os.name == 'nt':
    try:
        # Documents and Settings\[User Name]\Application Data\Gajim\logs.db
        LOG_DB_PATH = os.path.join(os.environ['appdata'], 'Gajim', 'logs.db')
    except KeyError:
        # win9x, ./logs.db
        LOG_DB_PATH = 'logs.db'
else: # Unices
    LOG_DB_PATH = os.path.expanduser('~/.gajim/logs.db')

try:
    LOG_DB_PATH = LOG_DB_PATH.decode(sys.getfilesystemencoding())
except:
    pass

class Constants:
    def __init__(self):
        (
            self.JID_NORMAL_TYPE,
            self.JID_ROOM_TYPE
        ) = range(2)
        
        (
            self.KIND_STATUS,
            self.KIND_GCSTATUS,
            self.KIND_GC_MSG,
            self.KIND_SINGLE_MSG_RECV,
            self.KIND_CHAT_MSG_RECV,
            self.KIND_SINGLE_MSG_SENT,
            self.KIND_CHAT_MSG_SENT
        ) = range(7)
        
        (
            self.SHOW_ONLINE,
            self.SHOW_CHAT,
            self.SHOW_AWAY,
            self.SHOW_XA,
            self.SHOW_DND,
            self.SHOW_OFFLINE
        ) = range(6)

constants = Constants()

class Logger:
    def __init__(self):
        self.jids_already_in = [] # holds jids that we already have in DB
        
        if not os.path.exists(LOG_DB_PATH):
            # this can happen only the first time (the time we create the db)
            # db is not created here but in src/common/checks_paths.py
            return
        self.init_vars()
        
    def init_vars(self):
        # if locked, wait up to 20 sec to unlock
        # before raise (hopefully should be enough)
        self.con = sqlite.connect(LOG_DB_PATH, timeout = 20.0,
            isolation_level = 'IMMEDIATE')
        self.cur = self.con.cursor()
        
        self.get_jids_already_in_db()

    def get_jids_already_in_db(self):
        self.cur.execute('SELECT jid FROM jids')
        rows = self.cur.fetchall() # list of tupples: (u'aaa@bbb',), (u'cc@dd',)]
        for row in rows:
            # row[0] is first item of row (the only result here, the jid)
            self.jids_already_in.append(row[0])

    def jid_is_from_pm(self, jid):
        '''if jid is gajim@conf/nkour it's likely a pm one, how we know
        gajim@conf is not a normal guy and nkour is not his resource?
        we ask if gajim@conf is already in jids (with type room jid)
        this fails if user disables logging for room and only enables for
        pm (so higly unlikely) and if we fail we do not go chaos
        (user will see the first pm as if it was message in room's public chat)
        and after that all okay'''
        
        possible_room_jid, possible_nick = jid.split('/', 1)
        
        self.cur.execute('SELECT jid_id FROM jids WHERE jid="%s" AND type=%d' %\
            (possible_room_jid, constants.JID_ROOM_TYPE))
        row = self.cur.fetchone()
        if row is not None:
            return True
        else:
            return False
    
    def get_jid_id(self, jid, typestr = None):
        '''jids table has jid and jid_id
        logs table has log_id, jid_id, contact_name, time, kind, show, message
        so to ask logs we need jid_id that matches our jid in jids table
        this method asks jid and returns the jid_id for later sql-ing on logs
        '''
        if jid.find('/') != -1: # if it has a /
            jid_is_from_pm = self.jid_is_from_pm(jid)
            if not jid_is_from_pm: # it's normal jid with resource
                jid = jid.split('/', 1)[0] # remove the resource
        if jid in self.jids_already_in: # we already have jids in DB
            self.cur.execute('SELECT jid_id FROM jids WHERE jid="%s"' % jid)
            jid_id = self.cur.fetchone()[0]
        else: # oh! a new jid :), we add it now
            if typestr == 'ROOM':
                typ = constants.JID_ROOM_TYPE
            else:
                typ = constants.JID_NORMAL_TYPE
            self.cur.execute('INSERT INTO jids (jid, type) VALUES (?, ?)', (jid, typ))
            try:
                self.con.commit()
            except sqlite.OperationalError, e:
                print >> sys.stderr, str(e)
            jid_id = self.cur.lastrowid
            self.jids_already_in.append(jid)
        return jid_id
    
    def convert_human_values_to_db_api_values(self, kind, show):
        '''coverts from string style to constant ints for db'''
        if kind == 'status':
            kind_col = constants.KIND_STATUS
        elif kind == 'gcstatus':
            kind_col = constants.KIND_GCSTATUS
        elif kind == 'gc_msg':
            kind_col = constants.KIND_GC_MSG
        elif kind == 'single_msg_recv':
            kind_col = constants.KIND_SINGLE_MSG_RECV
        elif kind == 'single_msg_sent':
            kind_col = constants.KIND_SINGLE_MSG_SENT
        elif kind == 'chat_msg_recv':
            kind_col = constants.KIND_CHAT_MSG_RECV
        elif kind == 'chat_msg_sent':
            kind_col = constants.KIND_CHAT_MSG_SENT

        if show == 'online':
            show_col = constants.SHOW_ONLINE
        elif show == 'chat':
            show_col = constants.SHOW_CHAT
        elif show == 'away':
            show_col = constants.SHOW_AWAY
        elif show == 'xa':
            show_col = constants.SHOW_XA
        elif show == 'dnd':
            show_col = constants.SHOW_DND
        elif show == 'offline':
            show_col = constants.SHOW_OFFLINE
        elif show is None:
            show_col = None
        else: # invisible in GC when someone goes invisible
            # it's a RFC violation .... but we should not crash
            show_col = 'UNKNOWN'
        
        return kind_col, show_col
    
    def commit_to_db(self, values):
        #print 'saving', values
        sql = 'INSERT INTO logs (jid_id, contact_name, time, kind, show, message, subject) VALUES (?, ?, ?, ?, ?, ?, ?)'
        self.cur.execute(sql, values)
        try:
            self.con.commit()
        except sqlite.OperationalError, e:
            print >> sys.stderr, str(e)
    
    def write(self, kind, jid, message = None, show = None, tim = None, subject = None):
        '''write a row (status, gcstatus, message etc) to logs database
        kind can be status, gcstatus, gc_msg, (we only recv for those 3),
        single_msg_recv, chat_msg_recv, chat_msg_sent, single_msg_sent
        we cannot know if it is pm or normal chat message, we try to guess
        see jid_is_from_pm() which is called by get_jid_id()
        
        we analyze jid and store it as follows:
        jids.jid text column will hold JID if TC-related, room_jid if GC-related,
        ROOM_JID/nick if pm-related.'''

        if self.jids_already_in == []: # only happens if we just created the db
            self.con = sqlite.connect(LOG_DB_PATH, timeout = 20.0,
                isolation_level = 'IMMEDIATE')
            self.cur = self.con.cursor()
            
        jid = jid.lower()
        contact_name_col = None # holds nickname for kinds gcstatus, gc_msg
        # message holds the message unless kind is status or gcstatus,
        # then it holds status message
        message_col = message
        subject_col = subject
        if tim:
            time_col = int(float(time.mktime(tim)))
        else:
            time_col = int(float(time.time()))
        
        kind_col, show_col = self.convert_human_values_to_db_api_values(kind,
            show)

        # now we may have need to do extra care for some values in columns
        if kind == 'status': # we store (not None) time, jid, show, msg
            # status for roster items
            jid_id = self.get_jid_id(jid)
            if show is None: # show is None (xmpp), but we say that 'online'
                show_col = constants.SHOW_ONLINE

        elif kind == 'gcstatus':
            # status in ROOM (for pm status see status)
            if show is None: # show is None (xmpp), but we say that 'online'
                show_col = constants.SHOW_ONLINE
            jid, nick = jid.split('/', 1)
            jid_id = self.get_jid_id(jid, 'ROOM') # re-get jid_id for the new jid
            contact_name_col = nick

        elif kind == 'gc_msg':
            if jid.find('/') != -1: # if it has a /
                jid, nick = jid.split('/', 1)
            else:
                # it's server message f.e. error message
                # when user tries to ban someone but he's not allowed to
                nick = None
            jid_id = self.get_jid_id(jid, 'ROOM') # re-get jid_id for the new jid
            contact_name_col = nick
        else:
            jid_id = self.get_jid_id(jid)
        
        if show_col == 'UNKNOWN': # unknown show, do not log
            return
            
        values = (jid_id, contact_name_col, time_col, kind_col, show_col,
            message_col, subject_col)
        self.commit_to_db(values)

    def get_last_conversation_lines(self, jid, restore_how_many_rows,
        pending_how_many, timeout):
        '''accepts how many rows to restore and when to time them out (in minutes)
        (mark them as too old) and number of messages that are in queue
        and are already logged but pending to be viewed,
        returns a list of tupples containg time, kind, message,
        list with empty tupple if nothing found to meet our demands'''
        jid = jid.lower()
        jid_id = self.get_jid_id(jid)
        now = int(float(time.time()))
        timed_out = now - (timeout * 60) # before that they are too old
        # so if we ask last 5 lines and we have 2 pending we get
        # 3 - 8 (we avoid the last 2 lines but we still return 5 asked)
        self.cur.execute('''
            SELECT time, kind, message FROM logs
            WHERE jid_id = %d AND kind IN   (%d, %d, %d, %d) AND time > %d
            ORDER BY time DESC LIMIT %d OFFSET %d
            ''' % (jid_id, constants.KIND_SINGLE_MSG_RECV, constants.KIND_CHAT_MSG_RECV,
                constants.KIND_SINGLE_MSG_SENT, constants.KIND_CHAT_MSG_SENT,
                timed_out, restore_how_many_rows, pending_how_many)
            )

        results = self.cur.fetchall()
        results.reverse()
        return results
    
    def get_unix_time_from_date(self, year, month, day):
        # year (fe 2005), month (fe 11), day (fe 25)
        # returns time in seconds for the second that starts that date since epoch
        # gimme unixtime from year month day:
        d = datetime.date(year, month, day)
        local_time = d.timetuple() # time tupple (compat with time.localtime())
        start_of_day = int(time.mktime(local_time)) # we have time since epoch baby :)
        return start_of_day
    
    def get_conversation_for_date(self, jid, year, month, day):
        '''returns contact_name, time, kind, show, message
        for each row in a list of tupples,
        returns list with empty tupple if we found nothing to meet our demands'''
        jid = jid.lower()
        jid_id = self.get_jid_id(jid)
        
        start_of_day = self.get_unix_time_from_date(year, month, day)
        
        seconds_in_a_day = 86400 # 60 * 60 * 24
        last_second_of_day = start_of_day + seconds_in_a_day - 1
        
        self.cur.execute('''
            SELECT contact_name, time, kind, show, message FROM logs
            WHERE jid_id = %d
            AND time BETWEEN %d AND %d
            ORDER BY time
            ''' % (jid_id, start_of_day, last_second_of_day))
        
        results = self.cur.fetchall()
        return results

    def get_search_results_for_query(self, jid, query):
        '''returns contact_name, time, kind, show, message
        for each row in a list of tupples,
        returns list with empty tupple if we found nothing to meet our demands'''
        jid = jid.lower()
        jid_id = self.get_jid_id(jid)
        if False: #query.startswith('SELECT '): # it's SQL query
            try:
                self.cur.execute(query)
            except sqlite.OperationalError, e:
                results = [('', '', '', '', str(e))]
                return results
            
        else: # user just typed something, we search in message column
            like_sql = '%' + query + '%'
            self.cur.execute('''
                SELECT contact_name, time, kind, show, message, subject FROM logs
                WHERE jid_id = ? AND message LIKE ?
                ORDER BY time
                ''', (jid_id, like_sql))

        results = self.cur.fetchall()
        return results

    def get_days_with_logs(self, jid, year, month, max_day):
        '''returns the list of days that have logs (not status messages)'''
        return
        jid = jid.lower()
        jid_id = self.get_jid_id(jid)
        list = []

        # First select all date of month whith logs we want
        start_of_month = self.get_unix_time_from_date(year, month, 1)
        seconds_in_a_day = 86400 # 60 * 60 * 24
        last_second_of_month = start_of_month + (seconds_in_a_day * max_day) - 1

        self.cur.execute('''
            SELECT time FROM logs
            WHERE jid_id = %d
            AND time BETWEEN %d AND %d
            AND kind NOT IN (%d, %d)
            ORDER BY time
            ''' % (jid_id, start_of_month, last_second_of_month,
            constants.KIND_STATUS, constants.KIND_GCSTATUS))
        result = self.cur.fetchall()

        #Copy all interesant time in a temporary table 
        self.cur.execute('CREATE TEMPORARY TABLE blabla(time,INTEGER)') 
        for line in result: 
            self.cur.execute(''' 
                INSERT INTO blabla (time) VALUES (%d) 
                ''' % (line[0])) 

        #then search in this small temp table for each day 
        for day in xrange(1, max_day): 
            start_of_day = self.get_unix_time_from_date(year, month, day) 
            last_second_of_day = start_of_day + seconds_in_a_day - 1 

            # just ask one row to see if we have sth for this date 
            self.cur.execute(''' 
                SELECT time FROM blabla 
                WHERE time BETWEEN %d AND %d 
                LIMIT 1 
                ''' % (start_of_day, last_second_of_day)) 
            result = self.cur.fetchone() 
            if result: 
                list[0:0]=[day]

        #Delete temporary table 
        self.cur.execute('DROP TABLE blabla') 
        result = self.cur.fetchone()
        return list

    def get_last_date_that_has_logs(self, jid):
        '''returns last time (in seconds since EPOCH) for which
        we had logs (excluding statuses)'''
        jid = jid.lower()
        jid_id = self.get_jid_id(jid)
        self.cur.execute('''
            SELECT time FROM logs
            WHERE jid_id = ?
            AND kind NOT IN (?, ?)
            ORDER BY time DESC LIMIT 1
            ''', (jid_id, constants.KIND_STATUS, constants.KIND_GCSTATUS))

        results = self.cur.fetchone()
        if results is not None:
            result = results[0]
        else:
            result = None

        return result
