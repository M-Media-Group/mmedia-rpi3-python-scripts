import os
from datetime import datetime

# Import own package config and email modules
from .. import config
from ..memail import memail

import shutil

# Send an email to the admin that the device is online
def sendEmail():
	subject = config.settings['device']['id']+" is online"
	body = "Hi!\n\nA Raspberry Pi Bot ("+config.settings['device']['id']+") has come online.\n\nThis Bot has around "+str(measure_free_space())+" GB left on its memory and is currently running at "+measure_temp()
	return memail.sendEmail(subject, body)

# Measure the current temperature of the CPU on Raspberry P
def measure_temp():
    temp = os.popen("vcgencmd measure_temp").readline()
    print(temp)
    return (temp.replace("temp=",""))

# Measure the current free space on the / folder
def measure_free_space():
	total, used, free = shutil.disk_usage("/")
	free_space = free // (2**30)
	print("free_space: "+str(free_space)+" GB")
	return free_space