#!/usr/bin/python2.7
import speech
import text
import os
import sqlite3
import logging

conn = sqlite3.connect('/home/abhijeet/Documents/Assistant/command.db')
speech.speak("Hello, I am Enori. What can I do for you today?")
command = text.stt()
command = command.lower()
logging.basicConfig(filename='iosis.log',level=logging.INFO)

def createTable(conn):
    conn.execute('''CREATE TABLE COMMAND
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        SPEECH         TEXT NOT NULL,
        CMD            TEXT NOT NULL,
        ANSWER         TEXT NOT NULL);''')
    print("Table created")


def addCommand(conn, speech, cmd, answer):
    query = "INSERT INTO COMMAND (SPEECH,CMD,ANSWER) VALUES ('%s','%s', '%s');" % (speech , cmd, answer)
    conn.execute(query)
    conn.commit()

def findAllCommand(conn):
    query = "SELECT SPEECH FROM COMMAND"
    cursor = conn.execute(query)
    return cursor

def findCommand(conn, speech):
    query = "SELECT CMD, ANSWER FROM COMMAND WHERE SPEECH = '%s'" % (speech)
    logging.info(query)
    cursor = conn.execute(query)
    return cursor

def Action():
    if("command" in command):
        sp = raw_input("Enter the speech of the command : ")
        cmd = raw_input("Enter the command : ")
        answer = raw_input("Enter the answer of the command : ")
        addCommand(conn, sp, cmd, answer)
    elif command == 'open terminal':
        os.system('gnome-terminal')
        speech.speak('Opening Terminal')
    elif len(findCommand(conn, command).fetchall()) != 0:
        action = findCommand(conn, command)
        for row in action:
            os.system(row[0])
            speech.speak(row[1])
    else:
        print "Unable to process"
try:
    Action()
except:
    logging.info("hello")
    logging.info(command)
    speech.speak("Unable to process the Information")
