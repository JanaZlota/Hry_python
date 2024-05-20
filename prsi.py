from random import shuffle

class Karta:
    def __init__(self, barva, hodnota):
        self.barva = barva
        self.hodnota = hodnota    
    def __str__(self):
        return f"{self.barva}{self.hodnota}"

class Obyc(Karta):
    pass
    
class Eso(Karta):
    pass
    
class Filek(Karta):  

    def hrac_meni_barvu(self):
        slovnik_barev = {1:'♠', 2:'♥', 3:'♦', 4:'♣'}
        vyber_barvy = "nevim"
        while vyber_barvy not in {1, 2, 3, 4}:
            vyber_barvy = int(input(f"Na jakou barvu chces menit? Zadej cislo. {slovnik_barev}"))
        nova_barva = slovnik_barev[vyber_barvy]
        print(f"Nova barva je: {nova_barva}")
        return Karta(nova_barva, None)
              
    def pocitac_meni_barvu(self, barva):
        print(f"Pocitac meni barvu na: {barva}")
        return Karta(barva, None)

class Sedmicka(Karta):
    def nalizej_sedmicky(self, balicek_vyhozenych, seznam):
        spocitej_7 = reversed(balicek_vyhozenych)
        pocet_7 = 0
        i = next(spocitej_7)
        while isinstance(i, Sedmicka):
            pocet_7 += 1
            try:
                i = next(spocitej_7)
            except StopIteration:
                break
        kolikrat_lizu = pocet_7 * 2
        for j in range(kolikrat_lizu):
            seznam = lizni_si(balicek, balicek_vyhozenych, seznam)

seznam_obyc = []
seznam_eso = []
seznam_filek = []
seznam_sedmicka = []
for barva in '♠', '♥', '♦', '♣':  
    for hodnota in list(range(8, 11)) + ['spodek', 'kral']:
        karta = Obyc(barva, hodnota)
        seznam_obyc.append(karta)
    
    karta = Eso(barva, "eso")
    seznam_eso.append(karta)

    karta = Filek(barva, "filek")
    seznam_filek.append(karta)

    karta = Sedmicka(barva, 7)
    seznam_sedmicka.append(karta)


def rozdej(balicek):
    karty_hrace = []
    karty_pocitace = []
    for i in range(4):
        karta = balicek.pop()
        karty_hrace.append(karta)
    for i in range(4):
        karta = balicek.pop()
        karty_pocitace.append(karta)

    return karty_hrace, karty_pocitace


def tiskni_slovnik(slovnik):
    for klic, hodnota in slovnik.items():
        print(f"{klic}: {hodnota}")
    

def tah_hrace(karty_hrace):
    moznosti = ["n", range(1, len(karty_hrace)+1)]
    cislo = 0
    while cislo not in moznosti:
        slovnik_karet = {str(i): karta for i, karta in enumerate(karty_hrace, 1)}
        print(f"Tvoje karty jsou:")
        tiskni_slovnik(slovnik_karet)
        print('Pokud nemas, cim hrat, stiskni "n".') 
        cislo = input("Kterou kartou chces hrat?")
        if cislo.lower() == "n":
            return "n"
        elif cislo in slovnik_karet.keys():
            hrana_karta = slovnik_karet[cislo]
            return hrana_karta       
        if cislo not in moznosti:
            print("Nerozumim. Zadej cislo, ktere reprezentuje tvoji vybranou kartu.")    
    

def lizni_si(balicek, balicek_vyhozenych, seznam):
    if not balicek:
        posledni_karta = balicek_vyhozenych.pop()
        balicek = list(reversed(balicek_vyhozenych))
        balicek_vyhozenych = [posledni_karta]
    else:
        liznuta_karta = balicek.pop()
        seznam.append(liznuta_karta)
        return seznam


def uprav_balicek(karta, balicek_vyhozenych, seznam):
    balicek_vyhozenych.append(karta)
    if karta in seznam:    
        seznam.remove(karta)
    if balicek_vyhozenych[-2].hodnota == 7:
        puvodni_7 = Sedmicka(balicek_vyhozenych[-2].barva, 7)        
        balicek_vyhozenych[-2] = puvodni_7 # nahrazeni
    if balicek_vyhozenych[-2].hodnota == "eso":
        puvodni_eso = Eso(balicek_vyhozenych[-2].barva, "eso")
        balicek_vyhozenych[-2] = puvodni_eso
    if balicek_vyhozenych[-2].hodnota == None:
        del balicek_vyhozenych[-2]

def vyhodnot(hrana_karta, balicek_vyhozenych, karty_hrace):
    if hrana_karta == "n":
        if isinstance(balicek_vyhozenych[-1], Eso):
            zahrane_eso = balicek_vyhozenych[-1]
            falesne_eso = Obyc(zahrane_eso.barva, "eso")   
            del balicek_vyhozenych[-1]
            balicek_vyhozenych.append(falesne_eso) 
            print("Stojis.")    
            return "hrala jsem", karty_hrace
        
        elif isinstance(balicek_vyhozenych[-1], Sedmicka):
            balicek_vyhozenych[-1].nalizej_sedmicky(balicek_vyhozenych, karty_hrace)  
            print("Lizes si za sedmicky.")                    
            return "nemam 7", karty_hrace  
          
        else:
            karty_hrace = lizni_si(balicek, balicek_vyhozenych, karty_hrace)  
            print("Lizes kartu z balicku.")   
            return "hrala jsem", karty_hrace 
        
    elif isinstance(balicek_vyhozenych[-1], Eso):
        if hrana_karta.hodnota != balicek_vyhozenych[-1].hodnota:
            print("Pozor! Eso lze prebit pouze esem. Zkus to znovu.")
            return "neplatny tah", karty_hrace
        else:
            uprav_balicek(hrana_karta, balicek_vyhozenych, karty_hrace)
            return "hrala jsem", karty_hrace
        
    elif isinstance(balicek_vyhozenych[-1], Sedmicka):
        if hrana_karta.hodnota != balicek_vyhozenych[-1].hodnota:
            print("Pozor! Sedmicku lze prebit pouze sedmickou. Zkus to znovu.")
            return "neplatny tah", karty_hrace
        else:
            uprav_balicek(hrana_karta, balicek_vyhozenych, karty_hrace)
            return "hrala jsem 7", karty_hrace
        
    elif isinstance(hrana_karta, Filek):
        uprav_balicek(hrana_karta, balicek_vyhozenych, karty_hrace)
        prozatimni_karta = hrana_karta.hrac_meni_barvu()
        uprav_balicek(prozatimni_karta, balicek_vyhozenych, karty_hrace)
        return "hrala jsem", karty_hrace
    
    elif hrana_karta.barva == balicek_vyhozenych[-1].barva or hrana_karta.hodnota == balicek_vyhozenych[-1].hodnota:
        uprav_balicek(hrana_karta, balicek_vyhozenych, karty_hrace)
        return "hrala jsem", karty_hrace
    else:
        print("Toto neni platny tah. Karty musi mit stejnou barvu nebo hodnotu. Zkus to znovu!")
        return "neplatny tah", karty_hrace
    


def tah_pocitace(balicek_vyhozenych, karty_pocitace):
    
    pocet_list = 0
    pocet_srdce = 0
    pocet_kara = 0
    pocet_piky = 0
    pocet_8 = 0
    pocet_9 = 0
    pocet_10 = 0
    pocet_spodek = 0
    pocet_kral = 0

    for karta in karty_pocitace:
        
        if karta.hodnota == 8:
            pocet_8 += 1
        elif karta.hodnota == 9:
            pocet_9 += 1
        elif karta.hodnota == 10:
            pocet_10 += 1
        elif karta.hodnota == "spodek":
            pocet_spodek += 1
        elif karta.hodnota == "kral":
            pocet_kral += 1
       
        if karta.barva == '♠':
            pocet_list += 1
        elif karta.barva == '♥':
            pocet_srdce += 1
        elif karta.barva == '♦':
            pocet_kara += 1
        elif karta.barva == '♣':
            pocet_piky += 1
        
    pocetnost_hodnot = [(pocet_8, 8), (pocet_9, 9), (pocet_10, 10), (pocet_spodek, "spodek"), (pocet_kral, "kral")]
    pocetnost_hodnot.sort(key = lambda prvek_seznamu: prvek_seznamu[0], reverse=True)

    pocetnost_barev = [(pocet_list, "♠"), (pocet_srdce, "♥"), (pocet_kara, "♦"), (pocet_piky, "♣")]
    pocetnost_barev.sort(key = lambda prvek_seznamu: prvek_seznamu[0], reverse=True)

    if isinstance(balicek_vyhozenych[-1], Eso): 
        vybira_eso = []
        for karta in karty_pocitace: 
            if karta.hodnota == "eso":
                vybira_eso.append(karta)
        if not vybira_eso:
            print("Pocitac nema eso. Stoji. Jsi na rade.\n")
            zahrane_eso = balicek_vyhozenych[-1]
            falesne_eso = Obyc(zahrane_eso.barva, "eso")   
            del balicek_vyhozenych[-1]
            balicek_vyhozenych.append(falesne_eso) 
            return "nema eso", karty_pocitace
        for pocet, barva in pocetnost_barev:
            for karta in vybira_eso:
                if barva == karta.barva:
                    karta_pocitace = karta
                    print(f"Pocitac vyhazuje: {karta_pocitace}\n") 
                    return karta_pocitace, karty_pocitace
        

    if isinstance(balicek_vyhozenych[-1], Sedmicka):
        vybira_7 = []
        for karta in karty_pocitace: 
            if karta.hodnota == 7:
                vybira_7.append(karta) # karty_pocitace podle vyskytu, vyber barvu 7 podle vyskytu
        if not vybira_7:
            print("Poctac nema sedmicku. Lize. Hrajes.\n")
            balicek_vyhozenych[-1].nalizej_sedmicky(balicek_vyhozenych, karty_pocitace)
            return "nema 7", karty_pocitace
        for pocet, barva in pocetnost_barev:
            for karta in vybira_7:
                if barva == karta.barva:
                    karta_pocitace = karta
                    print(f"Pocitac vyhazuje: {karta_pocitace}\n") 
                    return karta_pocitace, karty_pocitace


    moznosti = []
    for karta in karty_pocitace:
        if karta.barva == balicek_vyhozenych[-1].barva or karta.hodnota == balicek_vyhozenych[-1].hodnota:
            moznosti.append(karta)
            for karta in moznosti:
                if isinstance(karta, Filek):
                    moznosti.remove(karta)
                elif isinstance(karta, Sedmicka):
                    karta_pocitace = karta
                    print(f"Pocitac vyhazuje: {karta_pocitace}\n") 
                    return karta_pocitace, karty_pocitace
                
                elif isinstance(karta, Eso):
                    karta_pocitace = karta
                    print(f"Pocitac vyhazuje: {karta_pocitace}\n") 
                    return karta_pocitace, karty_pocitace
                
                else:
                    if pocetnost_hodnot[0][0] >= pocetnost_barev[0][0]:
                        for pocet, hodnota in pocetnost_hodnot:
                            for karta in moznosti:
                                if hodnota == karta.hodnota:
                                    karta_pocitace = karta
                                    print(f"Pocitac vyhazuje: {karta}\n") 
                                    return karta_pocitace, karty_pocitace 
                    elif pocetnost_barev[0][0] > pocetnost_hodnot[0][0]:
                        for pocet, barva in pocetnost_barev:
                            for karta in moznosti:
                                if barva == karta.barva:
                                    karta_pocitace = karta
                                    print(f"Pocitac vyhazuje: {karta}\n") 
                                    return karta_pocitace, karty_pocitace   

    if not moznosti:
        for karta in karty_pocitace:
            if isinstance(karta, Filek):
                uprav_balicek(karta, balicek_vyhozenych, karty_pocitace)
                cislo, barva = pocetnost_barev[0]
                prozatimni_karta = karta.pocitac_meni_barvu(barva)                
                return prozatimni_karta, karty_pocitace
            
        print("Pocitac si lize. Hraj!\n")
        lizni_si(balicek, balicek_vyhozenych, karty_pocitace)
        return "lize", karty_pocitace
    


balicek = seznam_obyc + seznam_eso + seznam_filek + seznam_sedmicka
shuffle(balicek)

karty_hrace, karty_pocitace = rozdej(balicek)

vyhozena_karta = balicek.pop()
print(f"Vyhozena karta je: {vyhozena_karta}")
balicek_vyhozenych = []
balicek_vyhozenych.append(vyhozena_karta)

while karty_hrace or karty_pocitace:
    pocet_karet_pocitace = len(karty_pocitace)
    if pocet_karet_pocitace == 1:
        print("Pocitac ma v ruce posledni kartu.")
    elif pocet_karet_pocitace in range(2, 5):
        print(f"Pocitac ma {pocet_karet_pocitace} karty.")
    elif pocet_karet_pocitace >=5:
        print(f"Pocitac ma {pocet_karet_pocitace} karet.")
    print(f"Posledni karta je: {balicek_vyhozenych[-1]}")
    hrana_karta = tah_hrace(karty_hrace)
    print(f"Vybral sis: {hrana_karta}\n")
    vyhodnoceni_tahu, karty_hrace = vyhodnot(hrana_karta, balicek_vyhozenych, karty_hrace)
    if vyhodnoceni_tahu == "neplatny tah":
        continue
    elif vyhodnoceni_tahu == "nemam 7":
        zahrana_7 = balicek_vyhozenych[-1]
        falesna_7 = Obyc(zahrana_7.barva, 7)
        balicek_vyhozenych[-1] = falesna_7
    if not karty_hrace: # jiny zapis pro: if len(karty_hrace) == 0:
        print("Vyhral jsi. Gratuluji!\n")
        break

    vysledek, karty_pocitace = tah_pocitace(balicek_vyhozenych, karty_pocitace)
    if vysledek == "nema 7":
        zahrana_7 = balicek_vyhozenych[-1]
        falesna_7 = Obyc(zahrana_7.barva, 7)
        balicek_vyhozenych[-1] = falesna_7
    elif vysledek == "nema eso":
        continue
    elif vysledek == "lize":
        continue
    else:
        karta_pocitace = vysledek 
        uprav_balicek(karta_pocitace, balicek_vyhozenych, karty_pocitace)
    if not karty_pocitace:
        print("Pocitac vyhral.")
        break
print("Konec hry.")