#!/usr/bin/python
# -*- coding: utf-8 -*-

# PyGtalkRobot: A simple jabber/xmpp bot framework using Regular Expression Pattern as command controller
# Copyright (c) 2008 Demiao Lin <ldmiao@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Homepage: http://code.google.com/p/pygtalkrobot/
#

#
# This is an sample PyGtalkRobot that serves to set the show type and status text of robot by receiving message commands.
#

import sys
import time
import MySQLdb
from PyGtalkRobot import GtalkRobot
db=MySQLdb.connect(db="ddgo")
c=db.cursor()
############################################################################################################################

class SampleBot(GtalkRobot):
    
    #Regular Expression Pattern Tips:
    # I or IGNORECASE <=> (?i)      case insensitive matching
    # L or LOCALE <=> (?L)          make \w, \W, \b, \B dependent on the current locale
    # M or MULTILINE <=> (?m)       matches every new line and not only start/end of the whole string
    # S or DOTALL <=> (?s)          '.' matches ALL chars, including newline
    # U or UNICODE <=> (?u)         Make \w, \W, \b, and \B dependent on the Unicode character properties database.
    # X or VERBOSE <=> (?x)         Ignores whitespace outside character sets
    
    #"command_" is the command prefix, "001" is the priviledge num, "setState" is the method name.
    #This method is used to change the state and status text of the bot.
    def command_001_setState(self, user, message, args):
        #the __doc__ of the function is the Regular Expression of this command, if matched, this command method will be called. 
        #The parameter "args" is a list, which will hold the matched string in parenthesis of Regular Expression.
        '''(available|online|on|busy|dnd|away|idle|out|off|xa)( +(.*))?$(?i)'''
        show = args[0]
        status = args[1]
        jid = user.getStripped()

        # Verify if the user is the Administrator of this bot
        if jid == 'mustafa@lookmyart.com':
            print jid, " ---> ",bot.getResources(jid), bot.getShow(jid), bot.getStatus(jid)
            self.setState(show, status)
            self.replyMessage(user, "State settings changed！")

    #This method is used to send email for users.
    def command_002_SendEmail(self, user, message, args):
        
        #email ldmiao@gmail.com hello dmeiao, nice to meet you, bla bla ...
        '''[email|mail|em|m]\s+(.*?@.+?)\s+(.*?),\s*(.*?)(?i)'''
        email_addr = args[0]
        subject = args[1]
        body = args[2]
        #call_send_email_function(email_addr, subject,  body)
        
        self.replyMessage(user, "\nEmail sent to "+ email_addr +" at: "+time.strftime("%Y-%m-%d %a %H:%M:%S", time.gmtime()))
    
    #This method is used to response users.
    def command_100_default(self, user, message, args):
        '''.*?(?s)(?m)'''
        global c  , db

        froms = str(user).split("/")[0]
        c.execute("""SELECT s.id FROM auth_user as u , ddapp_userprofiles as s where s.user_id = u.id and u.email = %s """, (froms))
        data = c.fetchone()
        if data == None:
            self.replyMessage(user, "you can't access i can't find your account please go to http://xxxx.com/help/gtalk")
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
                self.replyMessage(user, "your message has been send. if you send this message on comment please type @reply [%s] your message" % str(newID))
            elif message.find("@live") > -1 and message.find("@livestop") == -1:
                message = message.replace("@live","").strip()
                self.replyMessage(user, "starting live feed if do you want stop live feed send me message to '@livestop'")
            elif message.find("@livestop") > -1:
                self.replyMessage(user, "live feed is stopped")
                print message
            elif message.find("@help") > -1:
                self.replyMessage(user, "command list:\n@live > start live feed\n@post > send message\n@livestop > stop live feed\n@reply [msgid] > comment to message")
            else:
                self.replyMessage(user, "sorry! can't progress your request please look http://xxxx.com/help/gtalk or send message to me '@help'")
            

############################################################################################################################
if __name__ == "__main__":
    bot = SampleBot()
    bot.setState('available', "Mood Gtalk")
    bot.start("mood@mstfyntr.com", "neverdie")
