import requests
import os
import json

prefix = "https://apps.unive.it/sitows/didattica/"

names = ['aule', 'corsi', 'corsiinsegnamenti', 'docenti', 'insegnamenti', 'insegnamentidocenti', 'lezioni', 'sedi']

dirname = os.path.dirname(__file__)

for name in names:
    url = prefix + name
    r = requests.get(url, allow_redirects=True)
    file = 'DB/' + name + '.json'
    open(os.path.join(dirname, file), 'wb').write(r.content)


with open(os.path.join(dirname,"DB/lezioni.json"), "r") as read_file:
    lezioni = json.load(read_file)


seen = set()
new_l = []
for d in lezioni:
    t = tuple(d.items())
    if t not in seen:
        seen.add(t)
        new_l.append(d)
        """ print(d, '\n') """

with open(os.path.join(dirname,"DB/lezioni.json"), "w") as outfile: 
    json.dump(new_l, outfile)

print(len(lezioni))
print(len(new_l))