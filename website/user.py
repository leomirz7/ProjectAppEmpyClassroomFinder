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
todayString = today.strftime(date_format)

print(todayString)

@user.route('/')
#@login_required
def private():
    """ user = User.query.get(int(current_user.id))
    
    db.session.commit() """

    with open(os.path.join("/home/mirza/ProjectAppEmpyClassroomFinder/calendar.json"), "r") as read_file:
        calendar = json.load(read_file)

    with open(os.path.join("/home/mirza/ProjectAppEmpyClassroomFinder/DB/aule.json"), "r") as read_file:
        aule = json.load(read_file)

    with open(os.path.join("/home/mirza/ProjectAppEmpyClassroomFinder/DB/sedi.json"), "r") as read_file:
        sedi = json.load(read_file)
        
    aule_oggi = []
    now = datetime.datetime.now()
        
    for a in calendar[todayString]:
        occupata = False
        for i,f in calendar[todayString][a]:
            inizio = datetime.datetime.strptime(i,'%H:%M')
            fine = datetime.datetime.strptime(f,'%H:%M')
            
            if now.time() > inizio.time() and now.time() < fine.time():
                occupata = True

        empty_room = {}
        empty_sede = {}

        if not occupata:
            print(a, calendar[todayString][a], '\n\n')  
            for item in aule:
                if item["AULA_ID"] == a:
                    empty_room = item  
            
            for item in sedi:
                if item["SEDE_ID"] == empty_room["SEDE_ID"]:
                    empty_sede = item  

            edificio = re.findall(r'\(.*?\)', empty_sede["NOME"])[0]
            
            aule_oggi.append((empty_room["NOME"], empty_sede["NOME"].replace(edificio, ""), edificio.replace("(","").replace(")",""))) 
            
             

    return render_template('user.html', user=current_user, user_data=user, cal=aule_oggi, today=todayString)

@user.route('/map')
#@login_required
def map():
    """ user = User.query.get(int(current_user.id))
    
    db.session.commit() """

    return render_template('map.html',user=current_user)
