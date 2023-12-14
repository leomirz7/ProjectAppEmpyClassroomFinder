from datetime import date, timedelta
import os
import shutil
import json
import datetime
import re


from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import *

from website import db
from website.models import User
from website.util import restrict_user

user = Blueprint('user', __name__)

today = datetime.date.today()
year = today.year
month = today.month
day = today.day

date_format = "%Y-%m-%d"
#todayString = today.strftime(date_format)

""" todayString = "2023-11-23" """

""" print(todayString) """

with open(os.path.join("/home/mirza/ProjectAppEmpyClassroomFinder/calendar.json"), "r") as read_file:
    calendar = json.load(read_file)
    
with open(os.path.join("/home/mirza/ProjectAppEmpyClassroomFinder/DB/aule.json"), "r") as read_file:
    aule = json.load(read_file)

with open(os.path.join("/home/mirza/ProjectAppEmpyClassroomFinder/DB/sedi.json"), "r") as read_file:
    sedi = json.load(read_file)

with open(os.path.join("/home/mirza/ProjectAppEmpyClassroomFinder/DB/lezioni.json"), "r") as read_file:
    lezioni = json.load(read_file)
 
with open(os.path.join("/home/mirza/ProjectAppEmpyClassroomFinder/DB/insegnamenti.json"), "r") as read_file:
    insegnamenti = json.load(read_file)


def get_aule_oggi(date_time):
    aule_oggi = []
    #now = datetime.datetime.now()

    dateString = date_time.date().strftime(date_format)
    
    for a in calendar[dateString]:
        occupata = False
        for i,f, n in calendar[dateString][a]:
            inizio = datetime.datetime.strptime(i,'%H:%M')
            fine = datetime.datetime.strptime(f,'%H:%M')
            
            if date_time.time() > inizio.time() and date_time.time() < fine.time():
                occupata = True

        empty_room = {}
        empty_sede = {}

        if not occupata:
            """ print(a, calendar[todayString][a], '\n\n')   """
            for item in aule:
                if item["AULA_ID"] == a:
                    empty_room = item  
            
            for item in sedi:
                if item["SEDE_ID"] == empty_room["SEDE_ID"]:
                    empty_sede = item  

            edificio = re.findall(r'\(.*?\)', empty_sede["NOME"])[0]
            
            aule_oggi.append((empty_room["NOME"], empty_sede["NOME"].replace(edificio, ""), edificio.replace("(","").replace(")",""), a)) 
    
    return aule_oggi


@user.route('/', methods=['GET', 'POST'])
@login_required
def private():
    live = True
    user = User.query.get(int(current_user.id))
    db.session.commit()

    aule_oggi = []

    if(request.args.get('flag')):
        flag = request.args.get('flag')
    else:
        flag = True

    if(request.args.get('date')):
        date_out = request.args.get('date')
        date_out = datetime.datetime.strptime(date_out, '%Y-%m-%dT%H:%M')
    else:
        date_out = datetime.datetime.now()
    

    dateString = date_out.date().strftime(date_format)
    dateStringHtml = date_out.strftime('%Y-%m-%dT%H:%M')

    return render_template('user.html', user=current_user, user_data=user, live=flag, today=dateStringHtml, title="AVAILABLE ROOMS")


@user.route('/get_list', methods=['POST'])
@login_required
def get_list():
    if request.method == 'POST':

        date, flag =   request.data.decode().split(',', 1)

        date_out = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M')
        dateString = date_out.date().strftime(date_format)
        dateStringHtml = date_out.strftime('%Y-%m-%dT%H:%M')


        if calendar.get(dateString):

            return render_template('lista_aule.html', user=current_user, today=dateStringHtml, flag=flag, cal=get_aule_oggi(date_out))
        else:

            return "Non ci sono aule "


@user.route('/get_list_edificio', methods=['POST'])
@login_required
def get_list_edificio():
    if request.method == 'POST':
        nome_edifico, date =   request.data.decode().split(',', 1)

        date_out = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M')
        dateString = date_out.date().strftime(date_format)
        dateStringHtml = date_out.strftime('%Y-%m-%dT%H:%M')

        cal = get_aule_oggi(date_out)
        cal_edificio = []
        for a,b,c,d in cal:
            if nome_edifico in c:
                cal_edificio.append((a,b,c,d))
            

        if calendar.get(dateString):
            return render_template('lista_aule.html', user=current_user, today=dateStringHtml, cal=cal_edificio)
        else:
            return "Non ci sono aule libere"


@user.route('/get_geo', methods=['POST'])
@login_required
def get_geo():
    if request.method == 'POST':
        date_out = datetime.datetime.strptime(request.data.decode(), '%Y-%m-%dT%H:%M')
        dateString = date_out.date().strftime(date_format)

        with open(os.path.join("/home/mirza/ProjectAppEmpyClassroomFinder/geoSedi.json"), "r") as read_file:
            sediGeo = json.load(read_file)

        if calendar.get(dateString):
            cal = get_aule_oggi(date_out)
            edifici = set()

            for a,b,c,d in cal:
                edifici.add(c[9:])

            listGeo = []

            for a in sediGeo:
                if(a["properties"]["name"] in edifici):
                    listGeo.append(a)
        
            return json.dumps(listGeo)
        else:
            return []

        

@user.route('/map')
@login_required
def map():
    user = User.query.get(int(current_user.id))
    db.session.commit()


    if(request.args.get('flag')):
        flag = request.args.get('flag')
    else:
        flag = True

    if(request.args.get('date')):
        date_out = request.args.get('date')
        date_out = datetime.datetime.strptime(date_out, '%Y-%m-%dT%H:%M')
    else:
        date_out = datetime.datetime.now()
    

    dateString = date_out.date().strftime(date_format)
    dateStringHtml = date_out.strftime('%Y-%m-%dT%H:%M')


    if not calendar.get(dateString):
        return render_template('map2.html', user=current_user, live=flag, today=dateStringHtml, title="MAP", cal=[])


    return render_template('map2.html', user=current_user, live=flag, title="MAP", today=dateStringHtml, cal=get_aule_oggi(date_out))
 

@user.route('/profile')
@login_required
def profile():
    user = User.query.get(int(current_user.id))
    
    db.session.commit()

    return render_template('profile.html', user=current_user, title="PROFILE")


@user.route('/room')
@login_required
def room():
    user = User.query.get(int(current_user.id))
    db.session.commit()

    room_name = request.args.get('room_name')
    room_id = request.args.get('room_id')
    date = request.args.get('date')

    flag = request.args.get('flag')

    date_time = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M')
    dateString = date_time.date().strftime(date_format)
    dateStringHtml = date_time.strftime('%Y-%m-%dT%H:%M')

    ar_ids = []
    nomi_lezioni_oggi = []

    return render_template('room.html', user=current_user, cal=calendar[dateString][room_id], title=str(room_name), date=dateStringHtml, flag=flag)
    