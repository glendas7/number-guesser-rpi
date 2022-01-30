import firebase_admin
from firebase_admin import credentials, firestore
from signal import pause
import constant
from gpiozero import Button, LED
from time import *
import time
import random
cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

ledGreen = LED(20)  
ledYellow = LED(12)
ledBlue = LED(25)
ledWhite = LED(16)
ledRed = LED(21)
answer = 0
guess = 0
ledBlue.off()
ledWhite.off()

# Create a callback on_snapshot function to capture changes
def on_buttondoc_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        print(f'Received document snapshot: {doc.to_dict()}')
        submitButton_status = doc.to_dict()["submitButton"]
        startButton_status = doc.to_dict()["startButton"]

        if submitButton_status == True:
            if startButton_status == False:
                print('submit button')
                ledWhite.on()
                sleep(1)
                ledWhite.off()
                doc_button_ref.update({u'submitButton': False})
                if guess == answer:
                    print('correct')
                    for _ in range(answer):
                        ledGreen.blink()
                        time.sleep(1.8)
                        ledGreen.off()
                if guess != answer:
                    print('not correct')
                    for _ in range(answer):
                        ledRed.blink()
                        time.sleep(1.8)
                        ledRed.off()
        if startButton_status == True:
            if submitButton_status == False:
                print('start button')
                ledBlue.on()
                sleep(1)
                ledBlue.off()
                doc_button_ref.update({u'startButton': False})

def on_gamedatadoc_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        global answer, guess
        print(f'Received document snapshot: {doc.to_dict()}')
        guess_status = doc.to_dict()["guess"]
        answer_status = doc.to_dict()["answer"]
        print(f'guess {guess_status}')
        print(f'answer {answer_status}')

        answer = answer_status
        guess = guess_status

doc_button_ref = db.collection(constant.COLLECTION_NAME).document(constant.DOCUMENT_BUTTONS)
doc_button_watch = doc_button_ref.on_snapshot(on_buttondoc_snapshot)
doc_gamedata_ref = db.collection(constant.COLLECTION_NAME).document(constant.DOCUMENT_GAMEDATA)
doc_gamedata_watch = doc_gamedata_ref.on_snapshot(on_gamedatadoc_snapshot)

doc_gamedata_ref.update({u'answer': answer})
doc_gamedata_ref.update({u'guess': guess})

button1 = Button(26)#increment guess buttons
button2 = Button(19)#submit button
button3 = Button(13)#start button



def button_pressed():
    global guess
    guess +=1
    doc_gamedata_ref.update({u'guess': guess})
    ledYellow.on()

def button_released():
    ledYellow.off()

def finish_entry():
    print('Entry Submitted!')
    doc_button_ref.update({u'startButton': False})
    doc_button_ref.update({u'submitButton': True}) 

def start_entry():
    print('You may now start your entry!')
    global guess
    global answer
    guess = 0
    answer = random.randint(1, 10)
    doc_gamedata_ref.update({u'answer': answer})
    doc_gamedata_ref.update({u'guess': guess})
    doc_button_ref.update({u'submitButton': False})
    doc_button_ref.update({u'startButton': True})

button1.when_pressed = button_pressed
button1.when_released = button_released
button2.when_pressed = finish_entry
button3.when_pressed = start_entry
pause()
