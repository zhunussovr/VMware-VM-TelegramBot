# -*- coding: utf-8 -*-

import config # Config file
import telegram
import os
import subprocess
import sys
import shlex
import datetime
from subprocess import Popen, PIPE
from telegram.ext import CommandHandler
from imp import reload # module for updating annother modules

from telegram.ext import Updater
updater = Updater(token=config.token)
dispatcher = updater.dispatcher

# Executing shell command and displaying result in Telegram
def run_command(command):
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    global textoutput
    textoutput = ''
    while True:
        global output
        output = process.stdout.readline()
        output = output.decode('utf8')
        if output == '' and process.poll() is not None:
            break
        if output:
            print (output.strip())
        textoutput = textoutput + '\n' + output.strip()
    rc = process.poll()
    return rc
    
# Function for Start command
def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Hi, I'm waintig your command, sir.")

# Function for Help command
def help(bot, update):
    reload(config)
    bot.sendMessage(chat_id=update.message.chat_id, text='''List of available commands: 
    /id - Your user id
    /statevm - Current state of VM
    /resetvm - Restart VM (hard)
    /stopvm - Power Off VM
    /startvm - Power On VM
    /pingvm - ICMP request to guest OS
    /pingesxi - ICMP request to ESXi host
    ''')

# Function for command - id
def myid(bot, update):
    userid = update.message.from_user.id
    bot.sendMessage(chat_id=update.message.chat_id, text=userid)
    

# Function for command State
def statevm(bot, update):
    reload(config) 
    user = str(update.message.from_user.id)
    if user in config.admin: # if user id is in the admin list the command will be executed
        run_command("vmware-cmd -H HOST_IP -U HOST_USER -P USER_PASSWORD /vmfs/volumes/597c1d14-9a03b50a-8402-3417ebf1255f/VMNAME/VMNAME.vmx getstate")
        bot.sendMessage(chat_id=update.message.chat_id, text=textoutput) # Display result in Telegram

# Function for command - pingvm
def pingvm(bot, update):
    reload(config) 
    user = str(update.message.from_user.id)
    if user in config.admin: # if user id is in the admin list the command will be executed
        run_command("ping -c 4 GUEST_VM_IP")
        bot.sendMessage(chat_id=update.message.chat_id, text=textoutput) # Display result in Telegram

# Function for command - pingesxi
def pingesxi(bot, update):
    reload(config) 
    user = str(update.message.from_user.id)
    if user in config.admin: # if user id is in the admin list the command will be executed
        run_command("ping -c 4 ESXI_IP")
        bot.sendMessage(chat_id=update.message.chat_id, text=textoutput) # Display result in Telegram

# Function for command - stopvm (PowerOff VM)
def stopvm(bot, update):
    reload(config)
    user = str(update.message.from_user.id)
    if user in config.admin: # if user id is in the admin list the command will be executed
        run_command("vmware-cmd -H HOST_IP -U HOST_USER -P USER_PASSWORD /vmfs/volumes/597c1d14-9a03b50a-8402-3417ebf1255f/VMNAME/VMNAME.vmx stop hard")
        bot.sendMessage(chat_id=update.message.chat_id, text=textoutput) # Display result in Telegram

# Function for command - resetvm (Hard reset of VM)
def resetvm(bot, update):
    reload(config)
    user = str(update.message.from_user.id)
    if user in config.admin: # if user id is in the admin list the command will be executed
        run_command("vmware-cmd -H HOST_IP -U HOST_USER -P USER_PASSWORD /vmfs/volumes/597c1d14-9a03b50a-8402-3417ebf1255f/VMNAME/VMNAME.vmx reset hard")
        bot.sendMessage(chat_id=update.message.chat_id, text=textoutput) # Display result in Telegram

# Function for command - startvm (Start of VM)
def startvm(bot, update):
    reload(config)
    user = str(update.message.from_user.id)
    if user in config.admin: # if user id is in the admin list the command will be executed
        run_command("vmware-cmd -H HOST_IP -U HOST_USER -P USER_PASSWORD /vmfs/volumes/597c1d14-9a03b50a-8402-3417ebf1255f/VMNAME/VMNAME.vmx start hard")
        bot.sendMessage(chat_id=update.message.chat_id, text=textoutput) # Display result in Telegram


    
    
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

statevm_handler = CommandHandler('statevm', statevm)
dispatcher.add_handler(statevm_handler)

pingvm_handler = CommandHandler('pingvm', pingvm)
dispatcher.add_handler(pingvm_handler)

pingesxi_handler = CommandHandler('pingesxi', pingesxi)
dispatcher.add_handler(pingesxi_handler)

stopvm_handler = CommandHandler('stopvm', stopvm)
dispatcher.add_handler(stopvm_handler)

startvm_handler = CommandHandler('startvm', startvm)
dispatcher.add_handler(startvm_handler)

resetvm_handler = CommandHandler('resetvm', resetvm)
dispatcher.add_handler(resetvm_handler)


myid_handler = CommandHandler('id', myid)
dispatcher.add_handler(myid_handler)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)


updater.start_polling()

