# -*- coding: utf-8 -*-

from whatsapp_get_data import WhatsappBot
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from selenium.webdriver.common.keys import Keys
import time

class MenuProject:

    def __init__(self, name, token, project_select, whatsapp):
        self.name = name
        self.c = whatsapp
        self.token = token
        self.groups = project_select

    def message_open_cart(self, group_name, message):
        self.c.send_message(group_name, message)


sched = BlockingScheduler()
message_group = input('Deseja Ativar as mensagens agendadas? S/N').lower()
name = input('Nome do projeto: ')
get_api = WhatsappBot()
token = get_api.token()
project = get_api.project_select(token, name)
whatsapp = MenuProject(name, token, project, get_api)


def message_scheduled_time(qtd_groups: int, project):
    scheduled = []
    for m in range(qtd_groups):
        qtd_message = len(project['groups'][m]['message'])
        if qtd_message > 0:
            for s in range(qtd_message):
                date = project['groups'][m]['message'][s]['message_date_time']
                hours = str(date).split('T')[1].split('-')[0].replace('T', ' ')
                date = str(date).split('T')[0]
                time = str(date + " " + hours)
                scheduled.append(time)
        else:
            scheduled.append(None)
    return scheduled


def message_scheduled_text(qtd_groups: int, project):
    messages = []
    for m in range(qtd_groups):
        qtd_message = len(project['groups'][m]['message'])
        if qtd_message > 0:
            for s in range(qtd_message):
                message = project['groups'][m]['message'][s]['message']
                group_name = project['groups'][m]['name']
                group_and_message = message + ',GRUPO:' + group_name
                messages.append(group_and_message)
        else:
            messages.append(None)
    return messages


groups = len(project[0]['groups'])
message_text = message_scheduled_text(groups, project[0])
schedule_message = message_scheduled_time(groups, project[0])


def send_message_bot(schedule_message, message_text):
    date_time_now = datetime.now()
    date_time_in_text = date_time_now.strftime('%Y-%m-%d %H:%M')
    for i in range(len(message_text)):
        time_scheduled = schedule_message[i]
        if time_scheduled is not None:
            new_time = time_scheduled.split(':')
            new_time = new_time[0] + ':' + new_time[1]
            if new_time == date_time_in_text:
                group_message = message_text[i].split(',GRUPO:')
                message_group = group_message[0]
                group = group_message[1]
                message_group = str(message_group).replace("\r", " ")
                whatsapp.message_open_cart(group, str(message_group))


def message_open_cart_scheduled():
    send_message_bot(schedule_message, message_text)


if __name__ == '__main__':
    jobs = []
    for timer in range(len(schedule_message)):
        time_scheduled = schedule_message[timer]
        count = schedule_message.count(time_scheduled)
        if 'run_every_' + str(time_scheduled) not in jobs:
            if time_scheduled is not None:
                sched.add_job(message_open_cart_scheduled, 'date', id='run_every_' + str(time_scheduled), run_date=time_scheduled)
        jobs.append('run_every_' + str(time_scheduled))

sched.start()
