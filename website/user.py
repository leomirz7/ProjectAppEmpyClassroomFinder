from datetime import date, timedelta
import os
import shutil
import json
import datetime

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



    return render_template('user.html', user=current_user, user_data=user, cal=calendar, today=todayString)

