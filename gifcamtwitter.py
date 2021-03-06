import picamera
from time import sleep
import time
import RPi.GPIO as GPIO
from os import system
import os
from twython import Twython
import random, string

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
button = 19 #Button GPIO Pin

GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
led_1 = 21 #Status LED GPIO Pin
GPIO.setup(led_1, GPIO.OUT)
led_2 = 12 #ON/OFF LED Pin
GPIO.setup(led_2, GPIO.OUT)

########################
### Variables Config ###
########################
num_pics = 8 #Number of pictures to take in Gif
gif_delay = 15 #How much delay in between those pictures (in milliseconds)

APP_KEY = 'YOUR APP KEY'
APP_SECRET = 'YOUR APP SECRET'
OAUTH_TOKEN = 'YOUR OAUTH TOKEN'
OAUTH_TOKEN_SECRET = 'YOUR OAUTH TOKEN SECRET'

#setup the twitter api client
twitter = Twython(APP_KEY, APP_SECRET,
                  OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
                  
def random_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def tweet_pics():
    print('Posting to Twitter')
    photo = open(filename + ".gif", 'rb')
    response = twitter.upload_media(media=photo)
    twitter.update_status(status='Taken with #Pix-E LoFi Gif Camera', media_ids=[response['media_id']])     

camera = picamera.PiCamera()
camera.resolution = (540, 405)
camera.rotation = 90
#camera.brightness = 70
camera.image_effect = 'none'
print('System Ready')

while True:
    input_state = GPIO.input(button) # Sense the button 
    randomstring = random_generator()
    if input_state == False:
    	# Switch off LED
        GPIO.output(led_1, 1)
        GPIO.output(led_2, 1)
        print('Gif Started')
        for i in range(num_pics):
    		camera.capture('image{0:04d}.jpg'.format(i))
        filename = '/home/pi/gifcam/gifs/' + randomstring + '-0'
        GPIO.output(led_1, 0)
    	print('Processing')
        graphicsmagick = "gm convert -delay " + str(gif_delay) + " " + "*.jpg " + filename + ".gif" 
        os.system(graphicsmagick)
        tweet_pics()
        print('Done')
    else :
        # Switch on LED
        GPIO.output(led_1, 1)
        time.sleep(0.35)
        GPIO.output(led_1, 0)
        time.sleep(0.35)
        
       