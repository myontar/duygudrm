#!/usr/bin/env python
# -*- coding: utf-8 -*

import sys
import time
import string
import socket
import select
import MySQLdb
import msnlib
import msncb
import re, urllib, os
"""
MSN Tk Client

This is a beta msn client based on msnlib. As you see, it's GUI based on the
Tk bindings, which provide an abstraction to create graphical interfaces; it
works both under linux, windows and probably others too.

For further information refer to the documentation or the source (which is
always preferred).
Please direct any comments to the msnlib mailing list,
msnlib-devel@auriga.wearlab.de.
You can find more information, and the package itself, at
http://users.auriga.wearlab.de/~alb/msnlib
"""

hkk="""
	Tmsn, Google translate kullanarak msn protokolü üzerinde 
	anında çeviri yapmaya olanak veren bir yazılımdır.
	
	Düzenleme: Sedat AYMA
	sedataym@hotmail.com
	http://www.sedatayma.blogspot.com
	"""


# main msnlib classes
m = msnlib.msnd()
m.cb = msncb.cb()

# void debug output
#def void(s): pass
#msnlib.debug = msncb.debug = void



#
# useful functions
#

#sys.setdefaultencoding(encoding)
encoding = 'iso-8859-1'
dl="tr"
dill=u"Türkçe"
def encode(s):
	try:
		return s.decode(encoding).encode('utf-8')
	except:
		return s

def decode(s):
	try:
		return s.decode('utf-8').encode(encoding)
	except:
		return s

def nick2email(nick):
	"Returns an email according to the given nick, or None if noone matches"
	for email in m.users.keys():
		if str(m.users[email].nick) == str(nick):
			return email
	if nick in m.users.keys():
		return nick
	return None

def email2nick(email):
	"Returns a nick accoriding to the given email, or None if noone matches"
	if email in m.users.keys():
		return m.users[email].nick
	else:
		return None

def now():
	"Returns the current time in format HH:MM:SSTT"
	return time.strftime('%I:%M:%S%p', time.localtime(time.time()) )

def quit():
	"Cleans up and quits everything"
	try:
		m.disconnect()
	except:
		pass
	root.quit()
	sys.exit(0)



#
# GUI classes
#

def callreq(user,message):
        global c  , db

        froms = str(user)
        c.execute("""SELECT s.id FROM auth_user as u , ddapp_userprofiles as s where s.user_id = u.id and u.email = %s """, (froms))
        data = c.fetchone()
        if data == None:
            m.sendmsg(froms, "you can't access i can't find your account please go to http://xxxx.com/help/gtalk")
        else:
            

        
        
            if message.find("@post") > -1:
                message = message.replace("@post","").strip()
                print data[0]
                title = message.decode("utf-8")
                print title
                c.execute(""" insert into ddapp_status (text,attachments,mood_point,from_user_id,last_update,send_time,rewrite,like_list,comment_list)
                values (%s,'[]',%s,%s,%s,%s,'sanami - email','[]','[]')
                """, (title,'5.5',int(data[0]),int(time.time()),int(time.time())))
                db.commit()
                newID = c.lastrowid
                c.execute(""" insert into ddapp_useractions (from_user_id , post_id , `times`) values (%s,%s,%s) """,(int(data[0]),int(newID),int(time.time())))
                db.commit()
                m.sendmsg(froms, "your message has been send. if you send this message on comment please type @reply [%s] your message" % str(newID))
            elif message.find("@live") > -1 and message.find("@livestop") == -1:
                message = message.replace("@live","").strip()
                m.sendmsg(froms, "starting live feed if do you want stop live feed send me message to '@livestop'")
            elif message.find("@livestop") > -1:
                m.sendmsg(froms, "live feed is stopped")
                print message
            elif message.find("@help") > -1:
                m.sendmsg(froms, "command list:\n@live > start live feed\n@post > send message\n@livestop > stop live feed\n@reply [msgid] > comment to message")
            else:
                m.sendmsg(froms, "sorry! can't progress your request please look http://xxxx.com/help/gtalk or send message to me '@help'")
            

db=MySQLdb.connect(db="ddgo")
c=db.cursor()
def cb_msg(md, type, tid, params, sbd):
	"Gets a message"
	t = tid.split(' ')
	email = t[0]
        print "################################"
        print email
	# parse
	lines = params.split('\n')
	headers = {} 
	eoh = 0
	for i in lines:
		# end of headers
		if i == '\r':
			break
		tv = i.split(':', 1)
		type = tv[0]
		value = tv[1].strip()
		headers[type] = value
		eoh += 1
	eoh +=1

	# ignore hotmail messages
	if email == 'Hotmail':
		return
	#print headers
	
	# typing notifications
	if (headers.has_key('Content-Type') and 
			headers['Content-Type'] == 'text/x-msmsgscontrol'):
                pass			
	# normal message
	else:
		if len(lines[eoh:]) > 1:
			
			msg += string.join(lines[eoh:], '')
			msg = msg.replace('\r', '')
			print "mesaj"
			callreq(email,msg)
		else:
                        print "mesaj"
                        callreq(email,lines[eoh])
		

	msncb.cb_msg(md, type, tid, params, sbd)
m.cb.msg = cb_msg


def close():
	cik = tkMessageBox._show(u"Programdan Çık",u"Programdan çıkmak istediğinize eminmisiniz?",tkMessageBox.QUESTION, tkMessageBox.YESNO)
	
	if cik=="yes":
		quit()
# main
#

# email - chatwindow dictionary


m.email = "mood@mstfyntr.com"
m.pwd = "neverdie"

# the encoding is utf-8 because the text class uses unicode directly
m.encoding = 'utf-8'



# login
try:
	m.login()
	m.sync()
except 'AuthError':
	tkMessageBox.showerror(u"Giriş", u"Bağlantı hatası: Parola hatalı")
	quit()

# start as invisible
m.change_status('online')


# main loop
while 1:
	fds = m.pollable()
	infd = fds[0]
	outfd = fds[1]
	
	try:
		# both network and gui checks
		fds = select.select(infd, outfd, [], 0)
		
	except KeyboardInterrupt:
		quit()
	except TclError:
		quit()

	for i in fds[0] + fds[1]:
		try:
			m.read(i)
		except ('SocketError', socket.error), err:
			if i != m:
				m.close(i)
			else:
				
				quit()
		
		# always redraw after a network event
		
	
	# sleep a bit so we don't take over the cpu
	time.sleep(0.05)


 
