# IMPORT DISCORD.PY. ALLOWS ACCESS TO DISCORD'S API.
import discord
from discord.ext import commands
from discord.utils import get
import pandas as pd
from table2ascii import table2ascii
from constante import COLOANELE_TABELULUI_CU_HAIDUCI, COLOANELE_TABELULUI_CU_SARCINI, DENUMIRI_COLIBE, JETON_ROBOCOP, PREFIXUL_COMENZILOR
from constante import NUMĂRUL_MAXIM_DE_ELEMENTE_DIN_TABLE, SEPARATOR_NUME_DE_DISCRIMINATOR_DISCORD, COLOANELE_TABELULUI_CU_CINE_SUNT_HAIDUCII_AFIȘAT_PE_DISCORD
from constante import COLOANELE_TABELULUI_CU_SARCINILE_HAIDUCILOR_AFIȘAT_PE_DISCORD, ELEMENTUL_NU_SE_AFLĂ_ÎN_COLOANA_DATĂ, HAIDUC_FĂRĂ_SARCINI
from constante import COLOANELE_TABELULUI_COMENZILOR_DE_AFIȘARE_PE_DISCORD, COLOANA_DATĂ_NU_EXISTĂ, COLIBA_DATĂ_NU_EXISTĂ, SERVER_ID
from constante import TABELUL_COMENZILOR_DE_AFIȘARE_PE_DISCORD_1, TABELUL_COMENZILOR_DE_AFIȘARE_PE_DISCORD_2, TABELUL_COMENZILOR_DE_AFIȘARE_PE_DISCORD_3
from constante import COLOANELE_TABELULUI_CU_SARCINILE_NEÎNCEPUTE_AFIȘAT_PE_DISCORD, COLOANELE_TABELULUI_CU_SARCINILE_GĂTATE_AFIȘAT_PE_DISCORD
from constante import ID_CANAL_HAIDE_CU_TUPEU, ROLURI
from funcții import dateleSuntActualizate, adaugăSarcină, sarcinileAcestuiHaiduc, formateazăDescriereDinTabel, pozițieElementÎnColoanaDinTabel, tabele, indexHaiducDupăIdentificator, identificatorMembru, ștergeSarcină
                    

# GETS THE BOT OBJECT FROM DISCORD.PY
intenții = discord.Intents.default()
intenții.members = True
robocop = commands.Bot(command_prefix=PREFIXUL_COMENZILOR, intents=intenții)

# EVENT LISTENER FOR WHEN THE BOT HAS SWITCHED FROM OFFLINE TO ONLINE.
@robocop.event
async def on_ready():
    dateleSuntActualizate(robocop)
    channel = robocop.get_channel(ID_CANAL_HAIDE_CU_TUPEU)
    print (channel)
    ghildă = robocop.get_guild(SERVER_ID)
    message = await channel.send("Salutare haiducule, în ce colibe vrei să fii?")
    listăDeObiecteDeRoluri = []
    for rol in ROLURI:
        print(rol)
        idRol = rol['id']
        emoji = rol['emoji']
        listăDeObiecteDeRoluri.append(get(ghildă.roles, id=idRol))
        await message.add_reaction(emoji)
        
    while True:
        # Wait for a reaction_add event, store the reacted emoji and user
        reacție, haiduc = await robocop.wait_for('reaction_add')
        print(haiduc)
        indexEmojiReacție = 0
        try:
            print(list(map(lambda x: x['emoji'], ROLURI)))
            indexEmojiReacție = list(map(lambda x: x['emoji'], ROLURI)).index(reacție)
        except ValueError:
            indexEmojiReacție = -1
        
        print(reacție)
        print(indexEmojiReacție)
        if indexEmojiReacție != -1:
            await haiduc.add_roles(listăDeObiecteDeRoluri[indexEmojiReacție])


@robocop.command(aliases=['1'])
async def ecou(ctx, arg):
    await ctx.send(arg)

@robocop.command(aliases=['2'])
async def comenzi(ctx):
    tabeleDeComenzi = [TABELUL_COMENZILOR_DE_AFIȘARE_PE_DISCORD_1, TABELUL_COMENZILOR_DE_AFIȘARE_PE_DISCORD_2, TABELUL_COMENZILOR_DE_AFIȘARE_PE_DISCORD_3]

    for tabelDeComanda in tabeleDeComenzi:
        corpRăspuns = []
        for comandăDeAfișat in tabelDeComanda:
            corpRăspuns.append([comandăDeAfișat[0],
                                formateazăDescriereDinTabel(comandăDeAfișat[2]), formateazăDescriereDinTabel(comandăDeAfișat[3])])

        output = table2ascii(
                header = COLOANELE_TABELULUI_COMENZILOR_DE_AFIȘARE_PE_DISCORD,
                body = corpRăspuns,
            )
        await ctx.send(f"```\n{output}\n```")


@robocop.command(aliases=['3'])
async def numărulMeuHaiducesc(ctx):
    idulAutoruluiMesajului = identificatorMembru(ctx.message.author)
    răspuns = "Tu ești haiducul numărul " + str(indexHaiducDupăIdentificator(idulAutoruluiMesajului))
    await ctx.send(răspuns)

@robocop.command(aliases=['4'])
async def cineSuntHaiducii(ctx):
    obiectTabele = tabele(NUMĂRUL_MAXIM_DE_ELEMENTE_DIN_TABLE)
    tabelCuHaiduci = obiectTabele.tabelCuHaiduci.tabel
    corpRăspuns = []
    for index, linie in tabelCuHaiduci.iterrows():
        if linie.any():
            corpRăspuns.append([index, linie[1]])

    output = table2ascii(
        header = COLOANELE_TABELULUI_CU_CINE_SUNT_HAIDUCII_AFIȘAT_PE_DISCORD,
        body = corpRăspuns,
    )
    await ctx.send(f"```\n{output}\n```")
    
@robocop.command(aliases=['5'])
async def ceSarciniAmDeFăcut(ctx):
    obiectTabele = tabele(NUMĂRUL_MAXIM_DE_ELEMENTE_DIN_TABLE)
    tabelCuSarcini = obiectTabele.tabelCuSarcini.tabel
    răspuns = await sarcinileAcestuiHaiduc(ctx, ctx.message.author.name, ctx.message.author.discriminator, tabelCuSarcini, [], 0)
    if răspuns == HAIDUC_FĂRĂ_SARCINI:
        await ctx.send("Deocamdată nu ai de făcut nimic. Poate poți să ajuți pe cineva.")


@robocop.command(aliases=['6'])
async def ceSarciniAvemDeFăcut(ctx):
    obiectTabele = tabele(NUMĂRUL_MAXIM_DE_ELEMENTE_DIN_TABLE)
    (tabelCuHaiduci, tabelCuSarcini) = (obiectTabele.tabelCuHaiduci.tabel, obiectTabele.tabelCuSarcini.tabel)
    corpRăspuns = []
    numărSarcină = 0
    for indexHaiduc, haiduc in tabelCuHaiduci.iterrows():
        if haiduc.any():
            indexurileLiniilorUndeSeAflăSarcinileHaiducului = pozițieElementÎnColoanaDinTabel(indexHaiduc, 
                                                                                            COLOANELE_TABELULUI_CU_SARCINI[0], tabelCuSarcini, False)
            if indexurileLiniilorUndeSeAflăSarcinileHaiducului != ELEMENTUL_NU_SE_AFLĂ_ÎN_COLOANA_DATĂ:
                for index in indexurileLiniilorUndeSeAflăSarcinileHaiducului:
                    numărSarcină += 1
                    corpRăspuns.append([numărSarcină, haiduc[1], tabelCuSarcini.iloc[index, 1], 
                                                                formateazăDescriereDinTabel(tabelCuSarcini.iloc[index, 2])])
        
    if numărSarcină == 0:
        await ctx.send("Deocamdată nici un haiduc nu lucrează la ceva. Uită-te la sarciniile neîncepute, poate începi ceva de acolo!")
    else:
        output = table2ascii(
            header = COLOANELE_TABELULUI_CU_SARCINILE_HAIDUCILOR_AFIȘAT_PE_DISCORD,
            body = corpRăspuns,
        )
        await ctx.send(f"```\n{output}\n```")

@robocop.command(aliases=['7'])
async def ceSarciniNeînceputeAvem(ctx):
    obiectTabele = tabele(NUMĂRUL_MAXIM_DE_ELEMENTE_DIN_TABLE)
    tabelCuSarciniNeîncepute = obiectTabele.tabelCuSarciniNeîncepute.tabel
    corpRăspuns = []
    numărSarcină = 0
    for indexSarcină, sarcină in tabelCuSarciniNeîncepute.iterrows():
        if sarcină.any():
            numărSarcină += 1
            corpRăspuns.append([numărSarcină, formateazăDescriereDinTabel(sarcină[0]), sarcină[1]])
        
    if numărSarcină == 0:
        await ctx.send("Nu avem sarcini neîncepute deocamdată. Scrie pe #haide-cu-tupeu o propunere ca să o putem adăuga.")
    else:
        output = table2ascii(
            header = COLOANELE_TABELULUI_CU_SARCINILE_NEÎNCEPUTE_AFIȘAT_PE_DISCORD,
            body = corpRăspuns,
        )
        await ctx.send(f"```\n{output}\n```")

@robocop.command(aliases=['8'])
async def careSuntSarcinileGătate(ctx):
    obiectTabele = tabele(NUMĂRUL_MAXIM_DE_ELEMENTE_DIN_TABLE)
    tabelCuSarciniGătate = obiectTabele.tabelCuSarciniGătate.tabel
    corpRăspuns = []
    numărSarcină = 0
    for indexSarcină, sarcină in tabelCuSarciniGătate.iterrows():
        if sarcină.any():
            numărSarcină += 1
            corpRăspuns.append([numărSarcină, sarcină[0], formateazăDescriereDinTabel(sarcină[1]), sarcină[2]])
        
    if numărSarcină == 0:
        await ctx.send("Nu avem sarcini neîncepute deocamdată. Scrie pe #haide-cu-tupeu o propunere ca să o putem adăuga.")
    else:
        output = table2ascii(
            header = COLOANELE_TABELULUI_CU_SARCINILE_GĂTATE_AFIȘAT_PE_DISCORD,
            body = corpRăspuns,
        )
        await ctx.send(f"```\n{output}\n```")

@robocop.command(aliases=['9'])
async def ceSarciniAreDeFăcutHaiduculZis(ctx, poreclă):
    obiectTabele = tabele(NUMĂRUL_MAXIM_DE_ELEMENTE_DIN_TABLE)
    (tabelCuHaiduci, tabelCuSarcini) = (obiectTabele.tabelCuHaiduci.tabel, obiectTabele.tabelCuSarcini.tabel)
    listăHaiduciCuPoreclaDată = pozițieElementÎnColoanaDinTabel(poreclă, COLOANELE_TABELULUI_CU_HAIDUCI[1], tabelCuHaiduci, False)
    if listăHaiduciCuPoreclaDată == ELEMENTUL_NU_SE_AFLĂ_ÎN_COLOANA_DATĂ:
        await ctx.send("Cine ești și ce cauți în acest adăpost?! Aici nu e nici un " + poreclă + "!!!")
    elif listăHaiduciCuPoreclaDată == COLOANA_DATĂ_NU_EXISTĂ:
        await ctx.send("A apărut o eroare te rog să-i transmiți Cristinei, lui Cornel sau Bob. Msms.")
    elif len(listăHaiduciCuPoreclaDată) > 1:
        await ctx.send("Din păcate numele ăsta nu-mi zice prea multe. Sper ca haiducii ziși și " + poreclă + " să-și găsească niște nume mai originale.")
    else:
        # EXISTĂ UN SINGUR HAIDUC CU PORECLA DATĂ
        haiduc = tabelCuHaiduci.iloc[listăHaiduciCuPoreclaDată[0], 0]
        nume = haiduc.split(SEPARATOR_NUME_DE_DISCRIMINATOR_DISCORD)[0]
        discriminator = haiduc.split(SEPARATOR_NUME_DE_DISCRIMINATOR_DISCORD)[1]
        răspuns = await sarcinileAcestuiHaiduc(ctx, nume, discriminator, tabelCuSarcini, [], 0)
        if răspuns == HAIDUC_FĂRĂ_SARCINI:
            await ctx.send("Deocamdată haiducul ăsta nu are de făcut nimic. Sugerează-i ceva.")

@robocop.command(aliases=['10'])
async def ceSarciniAreDeFăcutHaiduculNumărul(ctx, număr):
    obiectTabele = tabele(NUMĂRUL_MAXIM_DE_ELEMENTE_DIN_TABLE)
    (tabelCuHaiduci, tabelCuSarcini) = (obiectTabele.tabelCuHaiduci.tabel, obiectTabele.tabelCuSarcini.tabel)
    if int(număr) > len(tabelCuHaiduci):    
        await ctx.send("Încă nu suntem atât de mulți haiduci.")
    elif int(număr) < 0:
        await ctx.send("Haiduci negativi...hmh...abstraact.")
    else:
        haiduc = tabelCuHaiduci.iloc[int(număr), 0]
        nume = haiduc.split(SEPARATOR_NUME_DE_DISCRIMINATOR_DISCORD)[0]
        discriminator = haiduc.split(SEPARATOR_NUME_DE_DISCRIMINATOR_DISCORD)[1]
        răspuns = await sarcinileAcestuiHaiduc(ctx, nume, discriminator, tabelCuSarcini, [], 0)
        if răspuns == HAIDUC_FĂRĂ_SARCINI:
            await ctx.send("Deocamdată haiducul ăsta nu are de făcut nimic. Sugerează-i ceva.")

@robocop.command(aliases=['11'])
async def ceSarciniSuntDeFăcutÎnColiba(ctx, numeColibă):
    pozițieColibă = 0
    try:
        pozițieColibă = DENUMIRI_COLIBE.index(numeColibă)
    except ValueError:
        pozițieColibă = COLIBA_DATĂ_NU_EXISTĂ
    if pozițieColibă == COLIBA_DATĂ_NU_EXISTĂ:
        await ctx.send("Nu există o asemenea colibă. Poți cere un rebranding de colibă. Uite un site util pentru a te documenta: https://360advertising.ro/rebranding/")
    else:
        obiectTabele = tabele(NUMĂRUL_MAXIM_DE_ELEMENTE_DIN_TABLE)
        (tabelCuHaiduci, tabelCuSarcini) = (obiectTabele.tabelCuHaiduci.tabel, obiectTabele.tabelCuSarcini.tabel)
        corpRăspuns = []
        numărSarcină = 0
        indexurileLiniilorSarcinilorColibeiDate = pozițieElementÎnColoanaDinTabel(numeColibă, COLOANELE_TABELULUI_CU_SARCINI[2], tabelCuSarcini, False)
        if not(indexurileLiniilorSarcinilorColibeiDate == ELEMENTUL_NU_SE_AFLĂ_ÎN_COLOANA_DATĂ or indexurileLiniilorSarcinilorColibeiDate == COLOANA_DATĂ_NU_EXISTĂ):
                for index in indexurileLiniilorSarcinilorColibeiDate:
                    numărSarcină += 1
                    numărHaiduc = tabelCuSarcini.iloc[index, 0]
                    poreclăHaiduc = tabelCuHaiduci.iloc[numărHaiduc, 1]
                    corpRăspuns.append([numărSarcină, poreclăHaiduc, formateazăDescriereDinTabel(
                                                                tabelCuSarcini.iloc[index, 1]), 
                                                                tabelCuSarcini.iloc[index, 2]])
            
        if numărSarcină == 0:
            await ctx.send("Coliba nu are de făcut nici o sarcină. Ce mai aștepți?! Sparge tu gheața!")
        else:
            output = table2ascii(
                header = COLOANELE_TABELULUI_CU_SARCINILE_HAIDUCILOR_AFIȘAT_PE_DISCORD,
                body = corpRăspuns,
            )
            await ctx.send(f"```\n{output}\n```")

@robocop.command(aliases=['12'])
async def cumÎiZiceHaiduculuiĂluiaCuNumărul(ctx, număr):
    obiectTabele = tabele(NUMĂRUL_MAXIM_DE_ELEMENTE_DIN_TABLE)
    tabelCuHaiduci = obiectTabele.tabelCuHaiduci.tabel
    if int(număr) > len(tabelCuHaiduci):    
        await ctx.send("Încă nu suntem atât de mulți haiduci.")
    elif int(număr) < 0:
        await ctx.send("Haiduci negativi...hmh...abstraact.")
    else:
        poreclă = tabelCuHaiduci.iloc[int(număr), 1]
        răspuns = "Ăla e haiducul " + poreclă
        await ctx.send(răspuns)

@robocop.command(aliases=['13'])
async def ceNumărAreHaiduculZisȘi(ctx, poreclă):
    obiectTabele = tabele(NUMĂRUL_MAXIM_DE_ELEMENTE_DIN_TABLE)
    tabelCuHaiduci = obiectTabele.tabelCuHaiduci.tabel
    listăHaiduciCuPoreclaDată = pozițieElementÎnColoanaDinTabel(poreclă, COLOANELE_TABELULUI_CU_HAIDUCI[1], tabelCuHaiduci, False)
    if listăHaiduciCuPoreclaDată == ELEMENTUL_NU_SE_AFLĂ_ÎN_COLOANA_DATĂ:
        await ctx.send("Cine ești și ce cauți în acest adăpost?! Aici nu e nici un " + poreclă + "!!!")
    elif len(listăHaiduciCuPoreclaDată) > 1:
        await ctx.send("Din păcate numele ăsta nu-mi zice prea multe. Sper ca haiducii ziși și " + poreclă + " să-și găsească niște nume mai originale.")
    else:
        răspuns = "Ăla e haiducul " + str(listăHaiduciCuPoreclaDată[0])
        await ctx.send(răspuns)

@robocop.command(aliases=['14'])
async def nouaMeaSarcinăEste(ctx, numărSarcină):
    idulAutoruluiMesajului = identificatorMembru(ctx.message.author)
    numărHaiduc = indexHaiducDupăIdentificator(idulAutoruluiMesajului)
    adaugăSarcină(numărHaiduc, int(numărSarcină) - 1)
    await ctx.send("Acum ai o nouă sarcină. Spor la treabă!")

@robocop.command(aliases=['15'])
async def amTerminatSarcina(ctx, număr):
    if int(număr) <= 0:
        await ctx.send("Numărul sarcinii începe de la 1")
    else:
        idulAutoruluiMesajului = identificatorMembru(ctx.message.author)
        numărHaiduc = indexHaiducDupăIdentificator(idulAutoruluiMesajului)
        sarcinaAFostȘtearsă = ștergeSarcină(int(număr), numărHaiduc)
        if sarcinaAFostȘtearsă:
            await ctx.send("Bravo! Ține-o tot așa!")
        else: 
            await ctx.send("Nu ai încă atâtea sarcini. Poate voiai să scrii alt număr.")

# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
robocop.run(JETON_ROBOCOP)