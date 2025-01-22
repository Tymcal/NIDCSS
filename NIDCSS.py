
# ----------------------------- Set up things -----------------------------

import os
import smtplib # Import smtplib for the actual sending function
from email.mime.text import MIMEText # email package modules
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

import cv2

import time
# import RPi.GPIO as GPIO
# Setup GPIO for servo motor control
# GPIO.setmode(GPIO.BCM)
# servo_pin = 18  # Change this to the GPIO pin connected to the servo
# GPIO.setup(servo_pin, GPIO.OUT)
# servo = GPIO.PWM(servo_pin, 50)  # 50 Hz frequency for most servos
# servo.start(0)  # Start PWM with 0% duty cycle

while(1):
    # House numbers' database
    house_num = [
        ["96/448", "teema.khawjit@gmail.com"],
        ["118", "65010507@kmitl.ac.th"],
        ["949/11", "65010507@kmitl.ac.th"],
        ]

    # /////////////// Workflow start

    # ----------------------------- Identify house number -----------------------------

    inputNumber = str(input("กรุณาใส่บ้านเลขที่ปลายทาง: "))
    print("คุณกำลังไปบ้านเลขที่ " + inputNumber)

    # ----------------------------- Identify visitor's ID -----------------------------

    count = 0
    # Load the Haar Cascade classifier for ID card detection
    id_card_cascade = cv2.CascadeClassifier("idcarddetector.xml")  # Provide the path to your Haar Cascade XML file

    # Initialize the camera
    cap = cv2.VideoCapture(0)  # 0 is usually the default camera, but you can change it if needed

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read a frame.")
            break

        # Convert the frame to grayscale for detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect ID cards in the frame
        id_cards = id_card_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in id_cards:
            # Draw a rectangle around the detected ID card
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Save the current frame as an image
            count += 1 # Increment sample face image
            print(count)
            #break

        if count == 5:
            break
            
    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

    # ----------------------------- Gate function -----------------------------

    # def servomove(x):
    #     servo.ChangeDutyCycle(x)  # 7.5% duty cycle for 90 degrees
    #     time.sleep(1)  # Wait for the servo to move
    #     servo.ChangeDutyCycle(0)  # Stop the servo

    # servomove(7.5) # gate opens (moves up)
    print("Grand KMITLsiri Boulevard Oriental Casa Park Villa Ville ยินดีต่้อนรับ")
    # # wait till the car pass through
    # time.sleep(5)
    # servomove(2.5) # gate closes (moves down)

    # ----------------------------- sending mail to resident -----------------------------
    house_index = 0

    # Identify house number's existence
    for i in range(len(house_num)):
        if inputNumber == house_num[i][0]:
            house_index = i
            print("House index: " + str(house_index))
            break

    message = MIMEMultipart()
    message["From"] = "65010490@kmitl.ac.th" # Sender email address
    password = "@Kmitl-1164741-#B1" # Sender email password
    message["To"] = house_num[house_index][1] # Receiver email address
    message["Subject"] = "New Visitor Alert" # Subject

    image = cv2.imencode("newvisitor.jpeg", frame)[1].tobytes() # write image in binary mode.
    message.attach(MIMEImage(image, name=os.path.basename("visitor ID"))) # attach file
    text = "หากไม่ใช่ผู้ที่มาเยี่ยม โปรดแจ้ง 02-777-7777"
    text2 = "Grand KMITLsiri Boulevard Oriental Casa Park Villa Ville"
    message.attach(MIMEText(text)) # write text message
    message.attach(MIMEText(text2)) # write text message

    server=smtplib.SMTP('smtp.gmail.com',port=587) # initialize connection to SMTP server
    server.starttls() # start communicate with TLS encryption
    server.login(message["From"], password) # login to the email server
    server.sendmail(message["From"], message["To"], message.as_string()) # send the mail
    print("Mail sent")
    server.quit() # Logout of the email server

# servo.stop()
# GPIO.cleanup()