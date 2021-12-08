#!/usr/bin/python37all
import cgi
import cgitb
import json

#Setip for the creation of the new webpage
cgitb.enable(display=1)
data = cgi.FieldStorage()

#setting up the different variables
pin = data.getvalue('pin') #received from the webpage
dataDump = {'pin':pin,'selection':'openpage'} #create list called data dump containing the pin for the password

#check the pinData.txt for an existing pin and logging that within the system
with open('pinData.txt', 'r') as pinDataRead:
    pinData = json.load(pinDataRead)
    currentPin = pinData['pin'] #logging pin data as current pin within the system going to be used to compare latter

#Checking if the current pin and pin value is empty, if true create a webpage asking to input a new pin
if(currentPin == '' and pin == '') or (currentPin == '' and not pin.isdecimal() and pin.length() != 4):
    print('Content-type: text/html\n\n')
    print('''
    <html>
    <form action="/cgi-bin/open_page.py" method="POST">
        <b>Enter New Pin Using Four Numbers</b>
        <input type="text" name="pin"><br>
        <input type="submit" name="submit" value="submit"><br>
    </input>
    </form>
    </html>''')

#checking if the current pin does not equal pin and if pin is empty
elif(currentPin != pin and pin != ''):
    print('Content-type: text/html\n\n')
    print('''
    <html>
    <form action="/cgi-bin/open_page.py" method="POST">
        <b>Wrong Pin! Please enter a Pin</b>
        <input type="text" name="pin"><br>
        <input type="submit" name="submit" value="submit"><br>
    </input>
    </form>
    </html>''')

#checks to see if the pin entered was wrong
elif(currentPin != pin):
    print('Content-type: text/html\n\n')
    print('''
    <html>
    <form action="/cgi-bin/open_page.py" method="POST">
        <b>Wrong Pin! Please enter a Pin</b>
        <input type="text" name="pin"><br>
        <input type="submit" name="submit" value="submit"><br>
    </input>
    </form>
    </html>''')

#if the pin entered was the correct pin or a new pin was entered
else:
    with open('pinData.txt', 'w') as f:
        json.dump(dataDump, f)

    print('Content-type: text/html\n\n')
    print('''
    <html>
    <form action="/cgi-bin/alarm_page.py" method="POST">
        <b>Alarm Control Page</b><br>
        <b>Turn Off Alarm</b><br>
        <input type="submit" name="buttonHit" value="Turn Off Alarm"><br>
        <b>Arm Alarm</b><br>
        <input type="submit" name="buttonHit" value="Arm Alarm"><br>
        <b>Reset Pin Password:</b><br>
        <input type="text" name="Enter New Pin"><br>
        <input type="submit" name="buttonHit" value="Reset Pin"><br>
    </input>
    </form>
    </html>''')



#in case of wrong pin

#in case of new password containing letters or > 4 numbers
