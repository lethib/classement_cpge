import pandas as pd

fields = {
    'Établissement': 'Etablissement', 
    'Code départemental de l’établissement' : 'Departement', 
    'Région de l’établissement' : 'Region', 
    'Commune de l’établissement' : 'Ville', 
    'Filière de formation' : 'Filiere',
    'Dont effectif des admis néo bacheliers sans mention au bac' : 'sans_mention', 
    'Dont effectif des admis néo bacheliers avec mention Assez Bien au bac' : 'assez_bien', 
    'Dont effectif des admis néo bacheliers avec mention Bien au bac' : 'bien', 
    'Dont effectif des admis néo bacheliers avec mention Très Bien au bac' : 'tres_bien', 
    'Dont effectif des admis néo bacheliers avec mention Très Bien avec félicitations au bac' : 'tres_bien_avec_feli'
}


notes = {
    'sans_mention' : 11,
    'assez_bien' : 13,
    'bien' : 15,
    'tres_bien' : 17,
    'tres_bien_avec_feli' : 19
}

def calcMean(row: pd.DataFrame) -> float:
    temp = row[notes.keys()]
    bot = temp.sum()
    top = 0
    for idx, val in temp.iteritems():
        top += val*notes[idx]
    return top/bot

def createMeanCol(df: pd.DataFrame) -> None:
    res = {}
    for idx, row in df.iterrows():
        res[idx] = calcMean(row)
    df['moyenne_bac'] = pd.Series(res.values(), index=res.keys())

if __name__ == '__main__':
    df = pd.read_csv('data/fr-esr-parcoursup-3.csv', delimiter=';', usecols=fields.keys()).rename(columns=fields).set_index('Etablissement')
    temp = df[notes.keys()]
    bot = temp.sum(axis=1)
    print(temp)
    createMeanCol(df)
    print(df)
