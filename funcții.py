from pydoc import describe
import pandas as pd
from table2ascii import table2ascii
from constante import COLOANELE_TABELULUI_CU_SARCINI,  DENUMIREA_FIȘIERULUI_TABELULUI_CU_HAIDUCI, DENUMIREA_FIȘIERULUI_TABELULUI_CU_SARCINI
from constante import COLOANELE_TABELULUI_CU_HAIDUCI, SEPARATOR_NUME_DE_DISCRIMINATOR_DISCORD, NUMĂRUL_MAXIM_DE_ELEMENTE_DIN_TABLE, COLOANA_DATĂ_NU_EXISTĂ
from constante import ELEMENTUL_NU_SE_AFLĂ_ÎN_COLOANA_DATĂ, HAIDUCUL_A_PLECAT_DIN_GHILDĂ, NUMĂRUL_HAIDUCULUI_VIRTUAL_CU_SARCINI_DE_ÎNDEPLINIT, SERVER_ID
from constante import NUMĂR_MAXIM_DE_CARACTERE_DINTR_O_LINIE, COLOANELE_TABELULUI_CU_SARCINILE_UNUI_HAIDUC_AFIȘAT_PE_DISCORD, HAIDUC_FĂRĂ_SARCINI
from constante import DENUMIREA_FIȘIERULUI_TABELULUI_CU_SARCINI_NEÎNCEPUTE, COLOANELE_TABELULUI_CU_SARCINI_NEÎNCEPUTE, DENUMIREA_FIȘIERULUI_TABELULUI_CU_SARCINI_GĂTATE
from constante import COLOANELE_TABELULUI_CU_SARCINI_GĂTATE

# CLASE
class Tabel():
    tabel = pd.DataFrame()
    locație = ""

class ObiectTabele():
    tabelCuHaiduci = Tabel()
    tabelCuSarcini = Tabel()
    tabelCuSarciniNeîncepute = Tabel()
    tabelCuSarciniGătate = Tabel()
# PRE-DEFINED FUNCTIONS

# FUNCȚIA RETURNEAZĂ LISTA DE POZIȚII UNDE APARE ELEMENTUL PRIMIT ÎN COLOANA CU NUMELE DAT DIN TABEL. 
# VALOAREA -1 ESTE RETURNATĂ ÎN CAZUL ÎN CARE ACEST ELEMENT NU SE AFLĂ ÎN TABEL
def pozițieElementÎnColoanaDinTabel(element, coloană, tabel, doarPrimul):
    coloane = tabel.columns.values.tolist()
    pozițieColoană = 0
    try:
        pozițieColoană = coloane.index(coloană)
    except ValueError:
        return COLOANA_DATĂ_NU_EXISTĂ
    
    listăElementeDinColoanaDată = tabel.iloc[:, pozițieColoană].tolist()
    pozițiiElementÎnColoană = [i for i, s in enumerate(listăElementeDinColoanaDată) if element == s]
    if pozițiiElementÎnColoană:
        if doarPrimul:
            pozițiePrimulElement = pozițiiElementÎnColoană[0]
            return pozițiePrimulElement
        else:
            return pozițiiElementÎnColoană
    else:
        return ELEMENTUL_NU_SE_AFLĂ_ÎN_COLOANA_DATĂ

# FUNCȚIA RETURNEAZĂ IDENTIFICATORUL FOLOSIT DE DISCORD PENTRU PROFILUL UNUI HAIDUC
def identificatorMembru(membru):
    return membru.name + SEPARATOR_NUME_DE_DISCRIMINATOR_DISCORD + membru.discriminator

# FUNCȚIA RETURNEAZĂ TABELUL PRIMIT CĂRUIA I S-A ADĂUGAT O LINIE
def adaugăLinieÎnTabel(linie, tabel):
    tabel.loc[len(tabel)] = linie
    return tabel

# FUNCȚIA RETURNEAZĂ TABELELE HAIDUCI ȘI SARCINI CITITE DIN LOCAL
def tabele(numărMaximDeLinii):
    obiectTabele = ObiectTabele()
    tabelCuHaiduci = Tabel()
    tabelCuHaiduci.tabel = pd.read_csv(DENUMIREA_FIȘIERULUI_TABELULUI_CU_HAIDUCI, nrows=numărMaximDeLinii, usecols=range(len(COLOANELE_TABELULUI_CU_HAIDUCI) + 1), index_col=0)
    tabelCuHaiduci.locație = DENUMIREA_FIȘIERULUI_TABELULUI_CU_HAIDUCI
    tabelCuSarcini = Tabel()
    tabelCuSarcini.tabel = pd.read_csv(DENUMIREA_FIȘIERULUI_TABELULUI_CU_SARCINI, nrows=numărMaximDeLinii, usecols=range(len(COLOANELE_TABELULUI_CU_SARCINI) + 1), index_col=0)
    tabelCuSarcini.locație = DENUMIREA_FIȘIERULUI_TABELULUI_CU_SARCINI
    tabelCuSarciniNeîncepute = Tabel()
    tabelCuSarciniNeîncepute.tabel = pd.read_csv(DENUMIREA_FIȘIERULUI_TABELULUI_CU_SARCINI_NEÎNCEPUTE, nrows=numărMaximDeLinii, usecols=range(len(COLOANELE_TABELULUI_CU_SARCINI_NEÎNCEPUTE) + 1), index_col=0)
    tabelCuSarciniNeîncepute.locație = DENUMIREA_FIȘIERULUI_TABELULUI_CU_SARCINI_NEÎNCEPUTE
    tabelCuSarciniGătate = Tabel()
    tabelCuSarciniGătate.tabel = pd.read_csv(DENUMIREA_FIȘIERULUI_TABELULUI_CU_SARCINI_GĂTATE, nrows=numărMaximDeLinii, usecols=range(len(COLOANELE_TABELULUI_CU_SARCINI_GĂTATE) + 1), index_col=0)
    tabelCuSarciniGătate.locație = DENUMIREA_FIȘIERULUI_TABELULUI_CU_SARCINI_GĂTATE
    obiectTabele.tabelCuHaiduci = tabelCuHaiduci
    obiectTabele.tabelCuSarcini = tabelCuSarcini
    obiectTabele.tabelCuSarciniNeîncepute = tabelCuSarciniNeîncepute
    obiectTabele.tabelCuSarciniGătate = tabelCuSarciniGătate
    return obiectTabele

def eliminăHaiduculCareNuMaiEÎnGhildăCuTotCuSarcinileLui(index, linie, membriiÎnFormațiaCurentăAGhildei, tabelCuHaiduci, tabelCuSarcini, tabelCuSarciniNeîncepute):
    numeHaiducVechi = linie[COLOANELE_TABELULUI_CU_HAIDUCI[0]]
    membriiÎnFormațiaCurentăAGhildeiPrelucrat = list(map(identificatorMembru, membriiÎnFormațiaCurentăAGhildei))
    try:
        pozițieHaiducVechi = membriiÎnFormațiaCurentăAGhildeiPrelucrat.index(numeHaiducVechi)
    except ValueError:
        pozițieHaiducVechi = HAIDUCUL_A_PLECAT_DIN_GHILDĂ
    
    # DACĂ HAIDUCUL A PLECAT DIN GHILDĂ ÎI DĂM DROP DIN TABELUL CU HAIDUCI ȘI DIN LISTA DE SARCINI
    if pozițieHaiducVechi == HAIDUCUL_A_PLECAT_DIN_GHILDĂ:
        pozițieHaiducVechiDinTabelulCuHaiduci = pozițieElementÎnColoanaDinTabel(numeHaiducVechi, COLOANELE_TABELULUI_CU_HAIDUCI[0], tabelCuHaiduci, True)
        if pozițieHaiducVechiDinTabelulCuHaiduci == ELEMENTUL_NU_SE_AFLĂ_ÎN_COLOANA_DATĂ:
            print("EROARE: HAIDUCUL PRIMIT CA PARAMETRU, INEXISTENT ÎN LISTA MEMBRILOR ACTUALI AI GHILDEI NU APARE ÎN TABELUL CU HAIDUCI")
            return ELEMENTUL_NU_SE_AFLĂ_ÎN_COLOANA_DATĂ
        elif pozițieHaiducVechiDinTabelulCuHaiduci == COLOANA_DATĂ_NU_EXISTĂ:
            print("EROARE: DENUMIRILE COLOANELOR DIN TABELUL CU HAIDUCI NU COINCID CU CELE DIN FIȘIERUL DE CONSTANTE")
            return COLOANA_DATĂ_NU_EXISTĂ
        listăPozițiiHaiducVechiDinTabelulDeSarcini = pozițieElementÎnColoanaDinTabel(   pozițieHaiducVechiDinTabelulCuHaiduci, 
                                                                                        COLOANELE_TABELULUI_CU_SARCINI[0], tabelCuSarcini, False)
        tabelCuHaiduci = tabelCuHaiduci.drop(index)
        
        # DACĂ HAIDUCUL CARE A PLECAT DIN GHILDĂ MAI AVEA DE FĂCUT SARCINI ATUNCI 
        if listăPozițiiHaiducVechiDinTabelulDeSarcini != ELEMENTUL_NU_SE_AFLĂ_ÎN_COLOANA_DATĂ:
            liniiDeAdăugat = tabelCuSarcini.iloc[listăPozițiiHaiducVechiDinTabelulDeSarcini]
            tabelCuSarcini.drop(tabelCuSarcini.index[listăPozițiiHaiducVechiDinTabelulDeSarcini], inplace = True)
            tabelCuSarciniNeîncepute = tabelCuSarciniNeîncepute.append(liniiDeAdăugat.iloc[:, [1,2]])
        elif pozițieHaiducVechiDinTabelulCuHaiduci == COLOANA_DATĂ_NU_EXISTĂ:
            print("EROARE: DENUMIRILE COLOANELOR DIN TABELUL CU SARCINI NU COINCID CU CELE DIN FIȘIERUL DE CONSTANTE")
            return COLOANA_DATĂ_NU_EXISTĂ
    return (tabelCuHaiduci, tabelCuSarcini, tabelCuSarciniNeîncepute)

# FUNCȚIA RETURNEAZĂ TABELUL CU HAIDUCI CĂRUIA I S-A ADĂUGAT O LINE DACĂ HAINUCUL PRIMIT NU SE AFLA DEJA ÎN TABEL
def adaugăMembruÎnTabelulCuHaiduci(membru, tabelCuHaiduci):
    identificatorHaiduc = identificatorMembru(membru)
    pozițieMembru = pozițieElementÎnColoanaDinTabel(identificatorHaiduc, COLOANELE_TABELULUI_CU_HAIDUCI[0], tabelCuHaiduci, True)
    if pozițieMembru == ELEMENTUL_NU_SE_AFLĂ_ÎN_COLOANA_DATĂ:
        # ADAUGĂ NUMELE UTILIZATORULUI DACĂ ACESTA NU ARE SETAT UN ALIAS
        poreclă = membru.nick and membru.nick or membru.name.split(SEPARATOR_NUME_DE_DISCRIMINATOR_DISCORD)[0]
        idMembru = identificatorMembru(membru)
        return adaugăLinieÎnTabel([idMembru, poreclă], tabelCuHaiduci)
    elif pozițieMembru == COLOANA_DATĂ_NU_EXISTĂ:
            print("EROARE: DENUMIRILE COLOANELOR DIN TABELUL CU HAIDUCI NU COINCID CU CELE DIN FIȘIERUL DE CONSTANTE")
            return COLOANA_DATĂ_NU_EXISTĂ
    else:
        return tabelCuHaiduci

# SALVEAZĂ TABELELE CU NOILE DATE
def salveazăTabelele(obiectTabele):
    for obiectulTabel, conținutulObiectuluiTabel in vars(obiectTabele).items():
        conținutulObiectuluiTabel.tabel.to_csv(conținutulObiectuluiTabel.locație)

def obiectTabeleActualizat(obiectTabele, tabelCuHaiduci, tabelCuSarcini, tabelCuSarciniNeîncepute, tabelCuSarciniGătate):
    obiectTabele.tabelCuHaiduci.tabel = tabelCuHaiduci
    obiectTabele.tabelCuSarcini.tabel = tabelCuSarcini
    obiectTabele.tabelCuSarciniNeîncepute.tabel = tabelCuSarciniNeîncepute
    obiectTabele.tabelCuSarciniGătate.tabel = tabelCuSarciniGătate
    return obiectTabele

def dateleSuntActualizate(robocop):
    ghildă = robocop.get_guild(SERVER_ID)
    membriiGhildă = ghildă.members
    obiectTabele = tabele(NUMĂRUL_MAXIM_DE_ELEMENTE_DIN_TABLE)
    (tabelCuHaiduci, tabelCuSarcini, tabelCuSarciniNeîncepute, tabelCuSarciniGătate) = (obiectTabele.tabelCuHaiduci.tabel, obiectTabele.tabelCuSarcini.tabel, obiectTabele.tabelCuSarciniNeîncepute.tabel, obiectTabele.tabelCuSarciniGătate.tabel)
    # ELIMINĂ MEMBRII CARE AU IEȘIT DIN GHILDĂ DIN TABELE
    for index, linie in tabelCuHaiduci.iterrows():
        if linie.any():
            valoareReturnată = eliminăHaiduculCareNuMaiEÎnGhildăCuTotCuSarcinileLui(index, linie, membriiGhildă, tabelCuHaiduci, tabelCuSarcini, tabelCuSarciniNeîncepute)
            
            if valoareReturnată == ELEMENTUL_NU_SE_AFLĂ_ÎN_COLOANA_DATĂ:
                print("EROARE: DATELE NU AU PUTUT FI ACTUALIZATE")
                return False
            elif valoareReturnată == COLOANA_DATĂ_NU_EXISTĂ:
                print("EROARE: DATELE NU AU PUTUT FI ACTUALIZATE")
                return False
            else:
                (tabelCuHaiduci, tabelCuSarcini, tabelCuSarciniNeîncepute) = valoareReturnată

    # ADAUGĂ MEMBRII NOI ÎN TABEL
    for membru in membriiGhildă:
        răspunsAdăugare = adaugăMembruÎnTabelulCuHaiduci(membru, tabelCuHaiduci)
        if not isinstance(răspunsAdăugare, pd.DataFrame) and răspunsAdăugare == COLOANA_DATĂ_NU_EXISTĂ:
            print("ERROARE: MEMBRUL " + identificatorMembru(membru) + " NU A PUTUT SĂ FIE ADĂUGAT ÎN TABEL")
    # print(tabelCuSarcini)
    salveazăTabelele(obiectTabeleActualizat(obiectTabele, tabelCuHaiduci, tabelCuSarcini, tabelCuSarciniNeîncepute, tabelCuSarciniGătate))
    return True

# FUNCȚIA RETURNEAZĂ NUMĂRUL LINIEI DIN TABELUL CU HAIDUCI UNDE SE GĂSEȘTE IDENTIFICATORUL DE DISCORD PRIMIT
def indexHaiducDupăIdentificator(identificator):
    obiectTabele = tabele(NUMĂRUL_MAXIM_DE_ELEMENTE_DIN_TABLE)
    tabelCuHaiduci = obiectTabele.tabelCuHaiduci.tabel
    
    for index, linie in tabelCuHaiduci.iterrows():
        if linie.any():
            if linie[0] == identificator:
                return index

# FUNCȚIA RETURNEAZĂ LINIA + DESPĂRȚIREA ÎN SILABE DE LA FINALUL LINIEI DACĂ ESTE CAZUL
def ajutăLaFormatare(descriereParțială):
    if descriereParțială[len(descriereParțială) - 1] != ' ':
        return descriereParțială + '-'
    else:
        return descriereParțială

# FUNCȚIA RETURNEAZĂ DESCRIEREA CARE O SĂ APARĂ ÎN TABELUL CU HAIDUCI ÎMPĂRȚITĂ PE LINII
def formateazăDescriereDinTabel(descriere):
    descriereFormatată = '\n'.join([ajutăLaFormatare(descriere[i:i + NUMĂR_MAXIM_DE_CARACTERE_DINTR_O_LINIE])
                                                for i in range(0, len(descriere), NUMĂR_MAXIM_DE_CARACTERE_DINTR_O_LINIE)])
    # ULTIMUL CARACTER VA FI - AȘA CĂ ÎN ELIMINĂM
    return descriereFormatată[0: len(descriereFormatată) - 1]

# FUNCȚIA RETURNEAZĂ RĂSPUNSUL CU SARCINILE UNUI SINGUR HAIDUC
async def sarcinileAcestuiHaiduc(ctx, nume, discriminator, tabelCuSarcini, corpRăspuns, numărSarcină):
    identificatorHaiduc = nume + SEPARATOR_NUME_DE_DISCRIMINATOR_DISCORD + discriminator
    indexurileLiniilorUndeSeAflăSarcinileHaiducului = pozițieElementÎnColoanaDinTabel(indexHaiducDupăIdentificator(identificatorHaiduc), 
                                                                                        COLOANELE_TABELULUI_CU_SARCINI[0], tabelCuSarcini, False)
    
    if indexurileLiniilorUndeSeAflăSarcinileHaiducului != ELEMENTUL_NU_SE_AFLĂ_ÎN_COLOANA_DATĂ:
        for index in indexurileLiniilorUndeSeAflăSarcinileHaiducului:
            numărSarcină += 1
            corpRăspuns.append([numărSarcină, formateazăDescriereDinTabel(tabelCuSarcini.iloc[index, 1]), tabelCuSarcini.iloc[index, 2]])

        output = table2ascii(
            header= COLOANELE_TABELULUI_CU_SARCINILE_UNUI_HAIDUC_AFIȘAT_PE_DISCORD,
            body=corpRăspuns,
        )
        await ctx.send(f"```\n{output}\n```")
        return corpRăspuns
    elif indexurileLiniilorUndeSeAflăSarcinileHaiducului == COLOANA_DATĂ_NU_EXISTĂ:
            await ctx.send("A apărut o eroare te rog să-i transmiți Cristinei, lui Cornel sau Bob. Msms.")
            print("EROARE: DENUMIRILE COLOANELOR DIN TABELUL CU SARCINI NU COINCID CU CELE DIN FIȘIERUL DE CONSTANTE")
            return COLOANA_DATĂ_NU_EXISTĂ
    else:
        return HAIDUC_FĂRĂ_SARCINI

# FUNCȚIA VA ADĂUGA O SARCINĂ UNUI UTILIZATOR
def adaugăSarcină(numărHaiduc, numărSarcină):
    obiectTabele = tabele(NUMĂRUL_MAXIM_DE_ELEMENTE_DIN_TABLE)
    sarcinăNeîncepută = obiectTabele.tabelCuSarciniNeîncepute.tabel.iloc[numărSarcină]
    descriere = sarcinăNeîncepută.iloc[0]
    colibă = sarcinăNeîncepută.iloc[1]
    obiectTabele.tabelCuSarcini.tabel = adaugăLinieÎnTabel([numărHaiduc, descriere, colibă], obiectTabele.tabelCuSarcini.tabel)

    obiectTabele.tabelCuSarciniNeîncepute.tabel.drop(obiectTabele.tabelCuSarciniNeîncepute.tabel.index[numărSarcină], inplace=True)
    salveazăTabelele(obiectTabele)

# FUNCȚIA VA ADĂUGA O SARCINĂ UNUI UTILIZATOR
def ștergeSarcină(numărSarcină, numărHaiduc):
    obiectTabele = tabele(NUMĂRUL_MAXIM_DE_ELEMENTE_DIN_TABLE)
    tabelCuSarcini = obiectTabele.tabelCuSarcini.tabel
    
    sarciniNumărate = 0
    for indexSarcină, sarcină in tabelCuSarcini.iterrows():
        if sarcină.any():
            if sarcină.iloc[0] == numărHaiduc:
                sarciniNumărate = sarciniNumărate + 1
                if sarciniNumărate == numărSarcină:
                    print(tabelCuSarcini.iloc[indexSarcină])
                    obiectTabele.tabelCuSarciniGătate.tabel = obiectTabele.tabelCuSarciniGătate.tabel.append(tabelCuSarcini.iloc[indexSarcină])
                    print(obiectTabele.tabelCuSarciniGătate.tabel)
                    tabelCuSarcini = tabelCuSarcini.drop([indexSarcină])
                    obiectTabele.tabelCuSarcini.tabel = tabelCuSarcini
                    salveazăTabelele(obiectTabele)
                    return True
    if sarciniNumărate < numărSarcină:
        return False 