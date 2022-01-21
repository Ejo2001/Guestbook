#Imports
import os
import sys
import sqlite3


#Connect to database
Conn = sqlite3.connect('Guestbook.db')

Cursor = Conn.cursor()

#Try to set up a database if non exist
try:
    Cursor.execute('''CREATE TABLE Entries
                                      (Id, Name, Message)''')
except:
    print("Database already exist")

#Here will all values be loaded to when the code is running.
Guestbook = []

#This is were all entries are registered
class Entry:
    def __init__(self, Name, Message, DB):
        self.Name = Name
        self.Message = Message
        self.Id = len(Guestbook) + 1
        if DB == False:
            Cursor.execute("INSERT INTO Entries (Id, Name, Message) VALUES (?, ?, ?)", (len(Guestbook) + 1, Name, Message))
            Cursor.execute("SELECT * FROM Entries")
            Conn.commit()

    def Add():
        while True:
            Name = input("\n\nName: ")
            if len(Name) <= 0:
                print("Name can't be empty, please try again!")
            else:
                break
        while True:
            Message = input("\n\nMessage: ")
            if len(Message) <= 0:
                    print("Message can't be empty, please try again!")
            else:
                break
        Guestbook.append(Entry(Name, Message, False))

    def Remove(Number):
        Guestbook.pop(Number - 1)
        Cursor.execute(f"DELETE FROM Entries WHERE Id={Number}")
        Cursor.execute("SELECT * FROM Entries")
        Conn.commit()

    def ReadAll():
        for i, Entry in enumerate(Guestbook):
            print("\n\nGuestbook entry number ", i + 1, "\nName: ", Entry.Name, "\nMessage: ", Entry.Message, "\n\n")

    def ReadNum(Num):
        Number = Num - 1
        print(Guestbook[Number])
        print("\n\nGuestbook entry number ", Num, "\nName: ", Guestbook[Number].Name, "\nMessage: ", Guestbook[Number].Message, "\n\n")
        
    def Search(Name):
        Found = 0
        for i, Entry in enumerate(Guestbook):
            if str(Entry.Name).find(Name) != -1:
                print("\n\nGuestbook entry number ", i + 1, "\nName: ", Entry.Name, "\nMessage: ", Entry.Message, "\n\n")
                Found += 1
        if Found > 0:
            print("We found ", Found, " results!")
        else:
            print("Sorry, no search results")


    def Load():
        Cursor.execute("SELECT * FROM Entries")
        for i in Cursor.fetchall():
            Guestbook.insert(i[0], Entry(i[1], i[2], True))

#Load previous entries from database
Entry.Load()


#Menu
while True:
    Answer = input("\n\nGUESTBOOK\n\n1. Add entry\n2. Read entries\n3. Read specific entry\n4. Search for entry by name\n5. remove entry\n6. Exit\n\n What would you like to do: ")
    if int(Answer) == 1:
        Entry.Add()
    elif int(Answer) == 2:
        Entry.ReadAll()
    elif int(Answer) == 3:
        Num = input("Number: ")
        Entry.ReadNum(int(Num))    
    elif int(Answer) == 4:
        Name = input("Name: ")
        Entry.Search(Name)
    elif int(Answer) == 5:
        ToRemove = input("Which entry would you like to remove? (Number): ")
        Entry.Remove(int(ToRemove))
    elif int(Answer) == 6:
        Cursor.execute("SELECT * FROM Entries")
        Conn.commit()
        sys.exit("Alrighty, have a good day!")
    else:
        print("\n\nError! Please try again!")