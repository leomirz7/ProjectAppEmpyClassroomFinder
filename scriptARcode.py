import json, csv
import os

dirname = os.path.dirname(__file__)

sediID = []
with open(os.path.join(dirname, "DB/sedi.json"), "r") as read_file:
    data = json.load(read_file)
    for a in data:
        if "Torino" in a["NOME"]:
            sediID.append(a["SEDE_ID"])
print(sediID)

auleID = []
with open(os.path.join(dirname, "DB/aule.json"), "r") as read_file:
    data = json.load(read_file)
    for a in data:
        if a["SEDE_ID"] in sediID:
            
            auleID.append(a["AULA_ID"])
print(auleID)

""" arID = set()
with open("DB/lezioni.json", "r") as read_file:
    data = json.load(read_file)
    for a in data:
        if a["AULA_ID"] in auleID:
            arID.add(a["AR_ID"])
print(arID) """

open(os.path.join(dirname, 'aule_IDs.txt'), 'w').close()     #empties the old file
for id in auleID:
    print(a, "\n")
    with open("aule_IDs.txt", "a") as aule_id_file:
        aule_id_file.write(id + '\n')
