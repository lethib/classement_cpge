import json
import pandas as pd

df = pd.read_csv('fr-esr-parcoursup-2.csv', delimiter=';')
print(df)

json_file = open('fr-esr-parcoursup-2.json')
json_str = json_file.read()

notes = {
    'sans_mention' : 11,
    'assez_bien' : 13,
    'bien' : 15,
    'tres_bien' : 17,
    'tres_bien_avec_feli' : 19
}

mention_field = {
    'sans_mention' : 'acc_sansmention',
    'assez_bien' : 'acc_ab',
    'bien' : 'acc_b',
    'tres_bien' : 'acc_tb',
    'tres_bien_avec_feli' : 'acc_tbf'
}

def getNumbers(jsonfile: dict) -> dict:
    res = {}
    for key, field in mention_field.items():
        res[key] = int(jsonfile['fields'][field])
    return res

def calcMean(nb_list : dict) -> float:
    bot = sum(nb_list.values())
    top = 0
    for mention, nb in nb_list.items():
        top += nb*notes[mention]
    return top/bot

etablissement = json.loads(json_str)[0]
print(etablissement['fields']['acc_tb'])
print(calcMean(getNumbers(etablissement)))

# PRISE EN MAIN OK - A REFAIRE AVEC PANDAS POUR UN RÉSULTAT PLUS PROPRE