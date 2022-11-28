import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

### Dictionnaries for data processing ###

fields = {
    'Établissement': 'Etablissement', 
    'Code départemental de l’établissement' : 'Departement',
    'Région de l’établissement' : 'Region', 
    'Dont effectif des admis néo bacheliers sans mention au bac' : 'sans_mention', 
    'Dont effectif des admis néo bacheliers avec mention Assez Bien au bac' : 'assez_bien', 
    'Dont effectif des admis néo bacheliers avec mention Bien au bac' : 'bien', 
    'Dont effectif des admis néo bacheliers avec mention Très Bien au bac' : 'tres_bien', 
}

other = {
    'Commune de l’établissement' : 'Ville', 
    'Filière de formation détaillée bis' : 'Filiere',
    'Dont effectif des admis néo bacheliers avec mention Très Bien avec félicitations au bac' : 'tres_bien_avec_feli'
}

notes = {
    'sans_mention' : 11,
    'assez_bien' : 13,
    'bien' : 15,
    'tres_bien' : 17,
}

col_name_export = {
    'Departement' : 'Département',
    'Etablissement' : 'Établissement',
    'classement_PV' : 'Classement "Plus-Value" (2021)',
    'moyenne_bac' : 'Moyenne du Lycée au BAC (2019)',
    'classement_bac' : 'Classement Parcoursup (2019)',
    'classement_etu' : "Classement L'étudiant (2021)",
    'difference' : 'Différence'
}

#'tres_bien_avec_feli' : 19

### Functions ###

## Functions for the website ##
def createDicRanking(rank_list: list[str]) -> dict:
    """Create the dictionnary of the data scrapped on the website."""
    res = {}
    for i in range(3, len(rank_list)-1, 8):
        res[rank_list[i].replace(' ','').replace('-', ' ')] = rank_list[i+1].replace(' ','')
    return res

def getRankEtudiant2(url: str) -> dict:
    df = pd.read_html(url)
    return df

def getRankEtudiant(url: str) -> dict:
    """Scrap the website ton get the rank of each schools."""
    browser = webdriver.Safari()
    browser.get(url)
    table = browser.find_elements(By.TAG_NAME, 'td')
    table_text = []
    for ele in table:
        table_text.append(ele.text)
    return createDicRanking(table_text)

def processDataDic(ranking_dic: dict) -> dict:
    """Dictionnary data processing to easily handle the data."""
    res = {}
    for key, val in ranking_dic.items():
        name = key[:-5]
        dp = int(key[-3:-1])
        res[int(val)] = [name,dp]
    return res

def createSeriesRankingEtu(processed_dic: dict, df: pd.DataFrame) -> None:
    """Create the ranking in the DataFrame from the website"""
    res = {}
    for idx, row in df.iterrows():
        res[idx] = None
        for key, val in processed_dic.items():
            if idx.lower().find(val[0].lower()) != -1 and val[1] == int(row['Departement']):
                res[idx] = int(key)
    df['classement_etu'] = pd.Series(res.values(), index=res.keys())


## Functions to process the data from the database ##
def calcMean(row: pd.DataFrame) -> float:
    """Compute the mean at the baccaleureate for a given school."""
    temp = row[notes.keys()]
    bot = temp.sum()
    top = 0
    for idx, val in temp.iteritems():
        top += val*notes[idx]
    return round(top/bot, 2)

def createMeanCol(df: pd.DataFrame) -> None:
    """Create the Mean column in the DataFrame."""
    res = {}
    for idx, row in df.iterrows():
        res[idx] = calcMean(row)
    df['moyenne_bac'] = pd.Series(res.values(), index=res.keys())

def createRanking(df: pd.DataFrame) -> None:
    """Create the ranking of each schools based on their mean."""
    temp = df.sort_values(by='moyenne_bac', ascending=False)
    res = {}
    i = 1
    for idx, row in temp.iterrows():
        res[idx] = i
        i += 1
    df['classement_bac'] = pd.Series(res.values(), index=res.keys())

## Function for final ranking
def createFinalRanking(df: pd.DataFrame) -> None:
    df['difference'] = df['classement_bac'] - df['classement_etu']

def createPlusValueRanking(df: pd.DataFrame) -> None:
    temp = df.sort_values(by='difference', ascending=False)
    res = {}
    i = 1
    for idx, row in temp.iterrows():
        res[idx] = i
        i += 1
    df.insert(2, 'classement_PV', pd.Series(res.values(), index=res.keys()))

if __name__ == '__main__':
    getRankEtudiant2('https://www.letudiant.fr/palmares/classement-prepa/maths-spe-mp/ecole-integree-panier.html')