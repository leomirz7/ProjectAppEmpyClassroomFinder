import requests
import os

prefix = "https://apps.unive.it/sitows/didattica/"

names = ['aule', 'corsi', 'corsiinsegnamenti', 'docenti', 'insegnamenti', 'insegnamentidocenti', 'lezioni', 'sedi']

dirname = os.path.dirname(__file__)

for name in names:
    url = prefix + name
    r = requests.get(url, allow_redirects=True)
    file = 'DB/' + name + '.json'
    open(os.path.join(dirname, file), 'wb').write(r.content)
