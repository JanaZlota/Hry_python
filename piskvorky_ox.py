def vyhodnot(pole, symbol_h, symbol_p):    
    if f"{symbol_h}{symbol_h}{symbol_h}" in pole:
        return "hrac"
            # Vyhral hrac s krizky.
    elif f"{symbol_p}{symbol_p}{symbol_p}" in pole:
        return "pocitac"
            # Vyhral hrac s kolecky - pocitac.
    elif "-" not in pole:
        return "!"
            # Nikdo nevyhral.
    else:
        return "-"
    
def tah(pole, cislo_policka, symbol):
    "Vrátí herní pole s daným symbolem umístěným na danou pozici"
    return pole[:cislo_policka] + symbol + pole[cislo_policka + 1:]

def tah_hrace(pole, symbol_h):
    nahrazovany_znak = "neznamy"
    while nahrazovany_znak != "-":
        cislo_policka = input("Na jake policko chces hrat?")
        try:
            cislo_policka = int(cislo_policka)
        except ValueError:
            print("To nebylo cislo!")
        else:
            if cislo_policka < 0 or cislo_policka > 19:
                print("Zadavej prosim cisla od 0 do 19.")
                continue
            nahrazovany_znak = pole[cislo_policka]
            if nahrazovany_znak == "x" or nahrazovany_znak == "o":
                print("Obsazeno! Vyber prazdne policko!")
            elif nahrazovany_znak == "-":
                return tah(pole, cislo_policka, symbol_h)
    
def tah_pocitace(pole, symbol_h, symbol_p):
    from random import randrange
    nahrazovany_znak = "neznamy"
    if f"{symbol_p}-{symbol_p}" in pole:        
        cislo_policka = pole.index(f"{symbol_p}-{symbol_p}") + 1
        nahrazovany_znak = pole[cislo_policka]
        return tah(pole, cislo_policka, symbol_p)
    
    elif f"-{symbol_p}{symbol_p}" in pole:
        cislo_policka = pole.index(f"-{symbol_p}{symbol_p}")
        nahrazovany_znak = pole[cislo_policka]
        return tah(pole, cislo_policka, symbol_p)

    elif f"{symbol_p}{symbol_p}-" in pole:
        cislo_policka = pole.index(f"{symbol_p}{symbol_p}-") + 2
        nahrazovany_znak = pole[cislo_policka]
        return tah(pole, cislo_policka, symbol_p)   
      
    elif f"{symbol_h}-{symbol_h}" in pole:        
        cislo_policka = pole.index(f"{symbol_h}-{symbol_h}") + 1
        nahrazovany_znak = pole[cislo_policka]
        return tah(pole, cislo_policka, symbol_p)
    
    elif f"-{symbol_h}{symbol_h}" in pole:
        cislo_policka = pole.index(f"-{symbol_h}{symbol_h}")
        nahrazovany_znak = pole[cislo_policka]
        return tah(pole, cislo_policka, symbol_p)
    
    elif f"{symbol_h}{symbol_h}-" in pole:
        cislo_policka = pole.index(f"{symbol_h}{symbol_h}-") + 2
        nahrazovany_znak = pole[cislo_policka]
        return tah(pole, cislo_policka, symbol_p)  
    
    elif f"-{symbol_p}" in pole:
        cislo_policka = pole.index(f"-{symbol_p}")
        nahrazovany_znak = pole[cislo_policka]
        return tah(pole, cislo_policka, symbol_p)
    
    elif f"{symbol_p}-" in pole:
        cislo_policka = pole.index(f"{symbol_p}-") + 1
        nahrazovany_znak = pole[cislo_policka]
        return tah(pole, cislo_policka, symbol_p)
    
    elif f"-{symbol_h}" in pole:
        cislo_policka = pole.index(f"-{symbol_h}")
        nahrazovany_znak = pole[cislo_policka]
        return tah(pole, cislo_policka, symbol_p)

    elif f"{symbol_h}-" in pole:
        cislo_policka = pole.index(f"{symbol_h}-") + 1
        nahrazovany_znak = pole[cislo_policka]
        return tah(pole, cislo_policka, symbol_p)
   
    else:
        while nahrazovany_znak != "-":
            cislo_policka = randrange(0, 20)
            nahrazovany_znak = pole[cislo_policka]
            return tah(pole, cislo_policka, symbol_p)

def piskvorky(pole):
    symbol_hrace = None
    mozne_symboly = ["x", "o"]
    while symbol_hrace not in mozne_symboly:
        symbol_hrace = input("Chces mit krizky nebo kolecka? Zmackni \"x\" nebo \"o\".")
        symbol_h = symbol_hrace
    mozne_symboly.remove(symbol_h)
    symbol_p = mozne_symboly[0]
            
    
    while vyhodnot(pole, symbol_h, symbol_p) == "-":
        
        pole = tah_hrace(pole, symbol_h)
        print("Tvuj tah:")
        print(pole)
        vysledek = vyhodnot(pole, symbol_h, symbol_p)
        
        if vysledek == "hrac":
            print("Vyhral jsi!")
            break
        elif vysledek == "!":
            print("Remiza. Nikdo nevyhral")
            break
        
        pole = tah_pocitace(pole, symbol_h, symbol_p)
        print("Tah pocitace:")
        print(pole)
        print("01234567890123456789") # vypsane pozice pro lepsi orientaci
        vysledek = vyhodnot(pole, symbol_h, symbol_p)
            
        if vysledek == "pocitac":
            print("Pocitac vyhral.")
            break
        elif vysledek == "!":
            print("Remiza. Nikdo nevyhral")
            break

piskvorky(pole = 20 * "-")