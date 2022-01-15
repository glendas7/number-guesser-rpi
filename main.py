import firebase_admin
from firebase_admin import credentials, firestore
from signal import pause
import constant
from gpiozero import Button, LED

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

#######################################
##### Simulattion of Light Control ####
#######################################

led1 = LED(21)  # Light

# Create a callback on_snapshot function to capture changes
def on_leddoc_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        print(f'Received document snapshot: {doc.to_dict()}')
        led1_status = doc.to_dict()["led1"]
        print(f'LED1 {led1_status}')
        if led1_status == True:
            led1.on()
        else:
            led1.off()

doc_led_ref = db.collection(constant.COLLECTION_NAME).document(constant.DOCUMENT_LEDS)

# Watch the LED document
doc_led_watch = doc_led_ref.on_snapshot(on_leddoc_snapshot)

#######################################
##### Simulation of Door monitoring ###
#######################################

# Button setup & watch
doc_button_ref = db.collection(constant.COLLECTION_NAME).document(constant.DOCUMENT_BUTTONS)

button1 = Button(19)

def button_pressed():
    print('Button pressed')
    doc_button_ref.update({u'button1': True})

def button_released():
    print('Button released')
    doc_button_ref.update({u'button1': False})

button1.when_pressed = button_pressed
button1.when_released = button_released

pause()
