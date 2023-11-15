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

""" todayString = "2023-11-03" """

""" print(todayString) """

with open(os.path.join("/home/mirza/ProjectAppEmpyClassroomFinder/calendar.json"), "r") as read_file:
    calendar = json.load(read_file)

with open(os.path.join("/home/mirza/ProjectAppEmpyClassroomFinder/DB/aule.json"), "r") as read_file:
    aule = json.load(read_file)

with open(os.path.join("/home/mirza/ProjectAppEmpyClassroomFinder/DB/sedi.json"), "r") as read_file:
    sedi = json.load(read_file)

def get_aule_oggi():
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
            """ print(a, calendar[todayString][a], '\n\n')   """
            for item in aule:
                if item["AULA_ID"] == a:
                    empty_room = item  
            
            for item in sedi:
                if item["SEDE_ID"] == empty_room["SEDE_ID"]:
                    empty_sede = item  

            edificio = re.findall(r'\(.*?\)', empty_sede["NOME"])[0]
            
            aule_oggi.append((empty_room["NOME"], empty_sede["NOME"].replace(edificio, ""), edificio.replace("(","").replace(")",""))) 
    
    return aule_oggi


@user.route('/')
@login_required
def private():
    user = User.query.get(int(current_user.id))
    db.session.commit()

    aule_oggi = []
    now = datetime.datetime.now()
        
    if not calendar.get(todayString):
        return render_template('user.html', user=current_user, user_data=user, cal=aule_oggi, today=todayString)

    return render_template('user.html', user=current_user, user_data=user, cal=get_aule_oggi(), today=todayString, title="AVAILABLE ROOMS")


@user.route('/map')
@login_required
def map():
    user = User.query.get(int(current_user.id))
    db.session.commit()

    return render_template('map2.html', user=current_user, title="MAP", cal=get_aule_oggi())


@user.route('/profile')
@login_required
def profile():
    user = User.query.get(int(current_user.id))
    
    db.session.commit()

    return render_template('profile.html', user=current_user, title="PROFILE")