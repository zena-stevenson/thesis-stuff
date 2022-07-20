#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 15:45:47 2019

First tests on a set of functions to read/write to peer mentoring database from the 
sign in app.

https://stackoverflow.com/questions/372885/how-do-i-connect-to-a-mysql-database-in-python
http://www.mikusa.com/python-mysql-docs/index.html

@author: zenalisa


NOTES / meeting topics:
    should add a column to sign_in_info or whatever the table is that logs the 
    times for the class number they're here to get help with
    
    tour of tables we've made so far, what to else to add besides ^
    
    get username@IP of muggle test user, give database permissions to em
    
    
    
"""

import MySQLdb
import datetime

# TODO update with actual test user's info 
db = MySQLdb.connect(host="gryffindor.nmsu.edu",    # gryffindor's IP
                     user="zenalisa",           # test username
                     passwd="Test@2019",        # test password
                     db="signin")         # student info database

cur = db.cursor()
#------------------------------------------------------------------------------
def check_status(ID):
    '''Input (encoded?) ID number, get user's consent status (or 0 if they 
       haven't been here yet). What numbers stand for what status is still 
       TBD.'''
       
    status = 0
    cur.execute("SELECT * FROM student_info WHERE hashedID=%s" %ID) 
    #print (type(cur.fetchall()))
    for row in cur.fetchall():
        status = row[2] #I think column 2 is the DUA, will probs have to change again 
    
    return status
    #db.close() #not sure where this should go?
    
#------------------------------------------------------------------------------
def add_new_student(ID):
    '''Input (encoded?) ID number. Adds new student entry to student_info 
    table.'''
    
    print("You're new! Please read this agreement and enter whatever the right consent level is idk I'm not designing this part:")
    status = input()
    cur.execute("INSERT INTO student_info(hashedID, DUA) VALUES (%s, %s)" % (ID, status))
    db.commit()

#------------------------------------------------------------------------------
def sign_in_and_out(ID, classID, signed_in_ids):
    '''Input (encoded?) student ID number, the class they're looking for help with (ex. "EE210") and the dictionary 
    of ID numbers that are currently signed in. If the ID isn't currently 
    signed in, adds new entry to sign_in_record, logging ID 
    number and time in (current time). If they are signed in, signs them out.
    
    Returns the dictionary of ID's that are signed in, after adding or removing the new ID.'''
    
    if ID in signed_in_ids: #if they're already signed in, sign them out        
        cur.execute("UPDATE sign_in_record SET time_out=CURRENT_TIMESTAMP WHERE id='%s' AND time_in = time_out" %ID)
        db.commit()
        print('Signed out at %s' %str(datetime.datetime.now()))
        signed_in_ids.remove(ID)
        
    else: #if they aren't signed in, sign them in
        cur.execute("INSERT INTO sign_in_record(id, time_in, time_out, %s) VALUES (%s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1)" %(classID, ID))
        db.commit()
        print('Signed in at %s' %str(datetime.datetime.now()))
        signed_in_ids.append(ID) 
    return signed_in_ids
#------------------------------------------------------------------------------
#def sign_out(ID):
#    '''Input (encoded?) ID number. Sets most recent sign out time in 
#    sign_in_record to current time'''    
#    
#    cur.execute("UPDATE sign_in_record SET time_out=CURRENT_TIMESTAMP WHERE id='%s' AND time_in = time_out" %ID)
#    db.commit()
#    print('Signed out at %s' %str(datetime.datetime.now()))
    
#def update_status(ID, new_status):
#    '''Input (encoded?) ID number. For in case someone changes their consent 
#    status? Seems good to consider but I'm not 100% sure what it should look 
#    like on the front end''' 
    
#    cur.execute("UPDATE student_info SET permission=%d" %new_status)  
#    db.commit()
    
#------------------------------------------------------------------------------    
print("hi welcome to chili's what's your ID number?")
ID = input()
print("which class is making your life hard today? (ie 'EE123')")
classID = input()
signed_in_ids =  [] #list of who's currently signed in- might have a different name in Tony's code?
status = check_status(ID)
if status == 0:
    add_new_student(ID)
    status = check_status(ID)

yes = [1, 3] #consent statuses that mean they did say yes to us storing their sign in/sign out data. Actual values TBD   
if status in yes:
    #print ('HERE')
    signed_in_ids = sign_in_and_out(ID, classID, signed_in_ids)
    
db.close()