import imaplib
import email
import quopri
import time
import email
from email.header import decode_header
from email.parser import HeaderParser
from email.Message import Message
import MySQLdb

imap = imaplib.IMAP4_SSL('imap.gmail.com', 993)
imap.login('mood@mstfyntr.com', 'neverdie')
i = True


while i:
    print "fetch"
    imap.select()
    typ, data = imap.search(None, 'UnSeen')
    data2 = data
    for num in data[0].split():
        typ, data = imap.fetch(num, '(RFC822)')
        
        db=MySQLdb.connect(db="ddgo")
        c=db.cursor()
        #print data[0][1]
        msgs = HeaderParser().parsestr(data[0][1])
        print msgs['Subject']
        title =  decode_header(msgs['Subject'])[0][0]
        froms = msgs['from'].split("<")[1].split(">")[0]
        c.execute("""SELECT s.id FROM auth_user as u , ddapp_userprofiles as s where s.user_id = u.id and u.email = %s """, (froms))
        data = c.fetchone()
        if data:
            print data[0]    
            c.execute(""" insert into ddapp_status (text,attachments,mood_point,from_user_id,last_update,send_time,rewrite,like_list,comment_list)
            values (%s,'[]',%s,%s,%s,%s,'sanami - email','[]','[]')
            """, (title,'5.5',int(data[0]),int(time.time()),int(time.time())))
            db.commit()
            newID = c.lastrowid
            c.execute(""" insert into ddapp_useractions (from_user_id , post_id , `times`) values (%s,%s,%s) """,(int(data[0]),int(newID),int(time.time())))
            db.commit()
        db.close()
        imap.store(data2[0].replace(' ',','),'+FLAGS','\Seen')
    time.sleep(10)
imap.close()
imap.logout()

