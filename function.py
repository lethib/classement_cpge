import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

### Dictionnaries for data processing ###

fields = {
    'Établissement': 'Etablissement', 
    'Code départemental de l’établissement' : 'Departement', 
    'Région de l’établissement' : 'Region', 
    'Commune de l’établissement' : 'Ville', 
    'Filière de formation détaillée bis' : 'Filiere',
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

# This dictionnary is the output of the getRankEtudiant function. It needed to be processed by hand as the data scrapped were hard to process
dic_rank_2021 = {
    'Louis Le Grand (75)': '1', 
    'Henri IV (75)': '2', 
    'Sainte Geneviève (78)': '3', 
    'Lazaristes (69)': '4', 
    'Stanislas (75)': '5',
    'Hoche (78)': '6', 
    'Pasteur (92)': '7', 
    'Michelet (92)': '8', 
    'du Parc (69)': '9', 
    'Saint-Louis (75)': '10', 
    'Pierre De Fermat (31)': '11', 
    'Lakanal (92)': '12', 
    'Montaigne (33)': '13', 
    'Fénelon (75)': '14', 
    'Clemenceau (44)': '15', 
    'Champollion (38)': '16', 
    'Chaptal (75)': '17', 
    'Blaise Pascal (91)': '18', 
    'Masséna (06)': '19', 
    'Chateaubriand (35)': '20', 
    'Kléber (67)': '21', 
    'Thiers (13)': '22', 
    'Janson de Sailly (75)': '23', 
    'Corneille (76)': '24', 
    'Marcelin Berthelot (94)': '26', 
    'Cézanne (13)': '27', 
    'Descartes (78)': '27', 
    'Fénelon Sainte Marie (75)': '29', 
    'Saliège (31)': '30', 
    'Henri Poincaré (54)': '31', 
    'Faidherbe (59)': '32', 
    'Charlemagne (75)': '33', 
    'Déodat de Séverac (31)': '33', 
    'Joffre (34)': '33', 
    'Pierre de la Ramée (02)': '36', 
    'Wallon (59)': '37', 
    'Descartes (37)': '38', 
    'La Martinière Monplaisir (69)': '38', 
    'Condorcet (75)': '40', 
    'Fabert (57)': '40', 
    'Blaise Pascal (63)': '42', 
    'Carnot (21)': '42', 
    'Claude Fauriel (42)': '44', 
    'Kerichen (29)': '45', 
    'Jean Perrin (69)': '46', 
    'Buffon (75)': '47', 
    'Berthollet (74)': '48', 
    'Jacques Decour (75)': '49', 
    'Sainte Marie (92)': '49', 
    'Marceau (28)': '51', 
    'Camille Jullian (33)': '52', 
    'Montesquieu (72)': '53', 
    'Victor Hugo (25)': '53', 
    "Pierre d'Ailly (60)": '55', 
    'Louis Thuillier (80)': '56', 
    'Jean Baptiste Corot (91)': '57', 
    'Bellevue (31)': '58', 
    'Assomption (35)': '59', 
    'Robespierre (62)': '60', 
    'Victor Hugo (14)': '61', 
    'Chrestien de Troyes (10)': '62', 
    'Franklin Roosevelt (51)': '63', 
    'Baimbridge (971)': '64', 
    'Jean Bart (59)': '64', 
    'Carnot (75)': '66', 
    'Pothier (45)': '66', 
    'PrytanéeNationalMilitaireLaFlèche(72)': '66', 
    'Gay Lussac (87)': '69', 
    'Dupuy de Lôme (56)': '70', 
    'François Ier (77)': '71', 
    'Pierre Gilles de Gennes(ex ENCPB) (75)': '71', 
    "Jeanne d'Albret (78)": '73', 
    'Saint Brieuc (22)': '73', 
    'Lavoisier (75)': '75', 
    'Lapérouse (81)': '76', 
    'Schweitzer (68)': '76', 
    'Turgot (75)': '76', 
    'CIV Valbonne (06)': '79', 
    'Henri Bergson (49)': '80', 
    'Aristide Briand (27)': '81', 
    'Daudet (30)': '82', 
    'Aristide Briand (44)': '83', 
    'René Cassin (64)': '84', 
    'François Ier (76)': '85', 
    'Assomption Bellevue (69)': '86', 
    'Edmont Perrier (19)': '86', 
    'Albert Châtelet (59)': '88', 
    'François Arago (66)': '89', 
    'Gustave Monod (95)': '89', 
    'Schweitzer (93)': '91', 
    'Honoré de Balzac (75)': '92', 
    "L'Empéri (13)": '92', 
    'Louis Barthou (64)': '94', 
    'Amyot (77)': '95', 
    'Sainte MarieBeaucamps (59)': '96', 
    'Théophile Gautier (65)': '96', 
    'Camille Guérin (86)': '98', 
    'Saint Stanislas (44)': '98', 
    "Dumont d'Urville (83)": '100', 
    'Bellevue (972)': '101', 
    'Bertran de Born (24)': '101', 
    'Brizeux (29)': '101', 
    'Chartreux (69)': '101', 
    'Lalande (01)': '101', 
    'Leconte de Lisle (974)': '101', 
    'Saint Joseph (84)': '101'
}


### Functions ###

## Functions for the website ##
def createDicRanking(rank_list: list[str]) -> dict:
    """Create the dictionnary of the data scrapped on the website."""
    res = {}
    for i in range(3, len(rank_list)-1, 8):
        res[rank_list[i].replace(' ','').replace('-', ' ')] = rank_list[i+1].replace(' ','')
    return res

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
    return top/bot

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

if __name__ == '__main__':
    #print(getRankEtudiant('https://www.letudiant.fr/palmares/classement-prepa/maths-spe-pc/ecole-integree-panier.html'))
    df = pd.read_csv('data/2021_CPGE_PCSI.csv', delimiter=';', usecols=fields.keys()).rename(columns=fields).set_index('Etablissement')
    pro_dic = processDataDic(dic_rank_2021)
    # temp = df[notes.keys()]
    createMeanCol(df)
    createRanking(df)
    createSeriesRankingEtu(pro_dic, df)
    print(df.sort_values(by='classement_bac').head(19))
    # print(df.loc['Lycée Pierre Corneille'])
    # df.to_excel('classement.xlsx')
    df2 = pd.read_excel('classement_PCSI.xlsx')
    print(df2)