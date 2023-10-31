import datetime
import json
import os

aule_IDs = []

dirname = os.path.dirname(__file__)

with open(os.path.join(dirname, "aule_IDs.txt")) as f:
    aule_IDs = [line.rstrip('\n') for line in f]

#print(aule_IDs)

calendar = {}

today = datetime.date.today()
year = today.year
month = today.month
day = today.day

date_format = "%Y-%m-%d"

with open(os.path.join(dirname, "DB/lezioni.json"), "r") as read_file:
    lessons = json.load(read_file)

    lessons.sort(key=lambda item:item['INIZIO'])
    lessons.sort(key=lambda item:item['AULA_ID'])
    lessons.sort(key=lambda item:item['GIORNO'])
    
    for les in lessons:
        if les['GIORNO'] not in calendar and les["AULA_ID"] in aule_IDs:
            calendar[les['GIORNO']] = {}
        
        if les["AULA_ID"] in aule_IDs:
            if les["AULA_ID"] not in calendar[les['GIORNO']]:
                calendar[les['GIORNO']][les["AULA_ID"]] = []
                
            calendar[les['GIORNO']][les["AULA_ID"]].append((les["INIZIO"], les["FINE"]))

    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    print("Current Time =", current_time)

    print(today)
    
    today = today.strftime("%Y-%m-%d")
    
    for a in calendar[today]:
        occupata = False
        for i,f in calendar[today][a]:
            inizio = datetime.datetime.strptime(i,'%H:%M')
            fine = datetime.datetime.strptime(f,'%H:%M')
            
            if now.time() > inizio.time() and now.time() < fine.time():
                occupata = True

        if not occupata:
            print(a, calendar[today][a], '\n\n')

    with open(os.path.join(dirname,"calendar.json"), "w") as outfile: 
        json.dump(calendar, outfile)
