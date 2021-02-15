""" Tento objekt bude zodpovedať, za sprcovanie vstupu od použivateľa,
a za zobrazovanie súčasného stavu hry."""

import pygame as pg
import ChessEngine

pg.init()
vysk = sirka = 512
""" Hracie  okno šachu bude 512 * 512 """
dim = 8
""" Šachovnicu tvorí plocha 8 * 8 štvorcov """
StvorcVelk = vysk//dim
maxim_FPS = 15
Figurky_Obrazky = {}

def nacitanie_obrazkov():
    """ Táto funkcia incializuje slovník obrázkov zo súboru Image, označené farbou a prislušnou figurkou,
    kde kľúčom je príslušna dvojica písmen, a danému kľúču prinaleží daný obrázok zo súboru Image.
    Takto možme jednoducho pomocou slovníku sprístupnit obrázky figurok"""

    polepomoc = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bp', 'wp', 'wR', 'wN', 'wB', 'wQ', 'wK']
    for figurka in polepomoc:
        Figurky_Obrazky[figurka] = pg.transform.scale(pg.image.load("Images/" + figurka + ".png"), (StvorcVelk, StvorcVelk))

def main():
    obrazovka = pg.display.set_mode((vysk, sirka))
    hodinky = pg.time.Clock()
    obrazovka.fill(pg.Color("white"))
    SH = ChessEngine.StavHry()
    """Inicializujem stav Hry pomocou pomocného python projectu,
     ktorý je zodopovedný za ukladanie informácií o hre, a kontrolovaní príslušných ťahov.
     StavHry je príslušná funkcia v súbore ChessEngine"""
    beh_hry = True
    anim = False
    """Boolean premenná ktorá ukladá informáciu o tom , či má prebehnuť animácia (pri ťahu) alebo nie (pri vracaní ťahu)"""
    nacitanie_obrazkov()
    """Obrázky budeme načitavť len raz, aby sme šetrili rýchlosťou"""
    Mozne_pohyb = SH.Generator_moznych_pohybov()
    """Generujeme všatky možne pohyby"""
    Doslo_k_tahu = False
    """Generovanie pohybov je časovo drahá časová záležitosť, kvôli for cyklu - ktorým prehľadávame šachovnicu.
    Preto chcem generovat pohyby čo najmenej krát a teda,
    táto premenna 'Doslo_k_tahu' nám povie či hrač už daný povolený tah vykonal alebo nie"""
    stvorecdocas = ()
    """ Premenna tuple (riadok,stlpec) , ktorá bude udržiavat polohu posledného kliknutia myšou"""
    Posledny_tah = []
    """List tuplov o velkosti 2 , ktorý bude udrziavat polohu posledných dvoch kliknutí myšou"""
    Konec_hry = False
    """Premenná, ktorá bude rozhodovať o tom, či hra pokračuje alebo je niektorý z hráčov v šach-mate, a hra teda končí"""
    while beh_hry:
        for udalost in pg.event.get():
            if udalost.type == pg.QUIT:
                beh_hry = False
            elif udalost.type == pg.MOUSEBUTTONDOWN:
                if not Konec_hry:
                    pozicia_mysky = pg.mouse.get_pos()
                    """ Táto podmienka zachytáva kliknutia myše. V premennej pozícia myšky je potom uchovaná poloha (Y,X),
                    kde bolo myšou kliknuté na šachovnici."""
                    riadok = pozicia_mysky[1]//StvorcVelk
                    stlpec = pozicia_mysky[0]//StvorcVelk
                    """Týmto získame index nakliknutého štvrčeka ako tuple (riadok,stlpec)"""
                    if stvorecdocas == (riadok, stlpec):
                        stvorecdocas = ()
                        Posledny_tah = []
                        """ Ak použivatel klikne dva krát po sebe na ten istý štvorček, tak figurka nebude presunutá na to isté
                        miesto, ale bude to brané ako keby hráč si rozmyslel kliknutie a vrátil figurku na miesto."""
                    else:
                        stvorecdocas = (riadok, stlpec)
                        Posledny_tah.append(stvorecdocas)
                        """Ak hráč klikne na inú pozíciu, tak pozícia je uložená  do premennej Posledny_tah"""
                    if len(Posledny_tah) == 2 and Posledny_tah[0] != ():
                        """Ak su v liste uložene dva kliknutia ... tak chceme vykonať ťah. 
                        Za ťahy bude zodpovedná trieda class-Pohyby - v ChessEngine.py"""
                        Tah = ChessEngine.Pohyby(Posledny_tah[0], Posledny_tah[1], SH.sachovnica)
                        """Táto trieda ako parametre berie dva posledne pozície (x,y) kliknutí myšou, a hraciu plochu """
                        for i in range(len(Mozne_pohyb)):
                            if Tah == Mozne_pohyb[i]:
                                SH.Tah_Figurkou(Mozne_pohyb[i])
                                Doslo_k_tahu = True
                                """Za konkrétny pohyb na šachovnici je však zodpovedná fukcia SH.TahFigurkou"""
                                anim = True
                                """Ak došlo k pohybu , tak taktiež dôjde k animácií"""
                                print(Tah.Preklad_do_notácie())
                                """Ťahy , resp. pozicie ťahov sú spracované pomocou pomocnej triedy ChessEngine.Pohyby,
                                ktorá ako argumenty berie pozicie jednotlivých štvorcov prvého a druhého kliknutia myšou"""
                                stvorecdocas = ()
                                Posledny_tah = []
                                """Po vykonaní ťahu (ktorý je uložený v SH.historia) musíme vynulovať pomocné premenné,
                                aby sa if podmienka mohla opakovať, inak by sme dookola appendovali na pomocny list,
                                a podmienka if by už nikdy nebola splnená"""
                                if SH.sach_mat:
                                    print("Šach - Mat")
                                elif  SH.Sach():
                                    print("Šach na strane ","bieleho" if SH.Bielytaha else "čierneho"," hráča")
                                """Táto čásť bude v dolnom okne vypisovať text, či je nejaký hráč šachovaný"""
                                if Tah.promo_pesiaka:
                                    print(f"pre výber figúrky použí klávesu Q - Dáma, N - Kôň, V - Veža, B - Strelec")
                                """Ak je možná promocia pešiaka, tak dáme používatelovi na výber figurku."""
                    if not Doslo_k_tahu:
                        Posledny_tah = [stvorecdocas]
                        """Ak mam nakliknutú figurku ale rozhodnem sa tahať inou figurkou,
                        tak prekliknutie na inu figurku nieje dovolený ťah ale predpokladáme, 
                        že uživateľ to myslí ako zmenu výberu figurky,ktrou  chce ťahať. 
                        Preto, aby to nemspôsobovalo problémy s hromadnými klkmi na figurky, tak tento nedovolený klik,
                        je braný ako prvé nakliknutie figurky myšou"""
            elif udalost.type == pg.KEYDOWN:
                """Kontrola výberu figúrky od použivateľa pri promcoií pešiaka"""
                if Tah.promo_pesiaka:
                    if udalost.key == pg.K_q:
                        SH.sachovnica[Tah.Riadok_Konec][Tah.Stlpec_Konec] = Tah.Nakliknuta_Figurka[0] + 'Q'
                    elif udalost.key == pg.K_n:
                        SH.sachovnica[Tah.Riadok_Konec][Tah.Stlpec_Konec] = Tah.Nakliknuta_Figurka[0] + 'N'
                    elif udalost.key == pg.K_b:
                        SH.sachovnica[Tah.Riadok_Konec][Tah.Stlpec_Konec] = Tah.Nakliknuta_Figurka[0] + 'B'
                    elif udalost.key == pg.K_v:
                        SH.sachovnica[Tah.Riadok_Konec][Tah.Stlpec_Konec] = Tah.Nakliknuta_Figurka[0] + 'R'
                if udalost.key == pg.K_z:
                    SH.Undofunkcia()
                    Doslo_k_tahu = True
                    """Ak hráč stalčí klavesu "z" tak vráti 1 pohyb späť. To zabezpečí funcia - Undofunkcia()"""
                    anim = False
                    """Pri undo - funkcií nechceme aby došlo k animácií"""
                if udalost.key == pg.K_r:
                    """Pomocou klávesnice "r" je možné resetovať hru, jednoduchým resetovaním jednotlivých premenných"""
                    SH = ChessEngine.StavHry()
                    Mozne_pohyb = SH.Generator_moznych_pohybov()
                    stvorecdocas = ()
                    Posledny_tah = []
                    anim = False
                    Doslo_k_tahu = False

        if Doslo_k_tahu == True:
            if anim:
                animacia(SH.historia[-1], obrazovka, SH.sachovnica, hodinky)
            Mozne_pohyb = SH.Generator_phybov_neveducich_dosachu()
            Doslo_k_tahu = False
            """Ak hráč urobil pohyb ktorý je správny vrámci pravidiel šachu, tak sa vygeneruje nový list možných pohybov"""
            anim = False

        Vyobrazenie_stavuHry(obrazovka, SH, Mozne_pohyb, stvorecdocas)
        """Po ťahu skontrolujeme či niektorý hrač nemá šach-mat"""
        if SH.sach_mat:
            Konec_hry = True
            if SH.Bielytaha:
                kreslenie(obrazovka, "Čierny vyhráva")
            else:
                kreslenie(obrazovka, "Biely vyhráva")

        hodinky.tick(maxim_FPS)
        pg.display.flip()

"""
Funkcia zodpovedná za zvýraznenie miesta ktoré používateľ naklikol (ak na ňom stojí figúrka),
 a taktiež možných miest presunu figurky.
"""
def highlighting(obrazovka, SH, Generator_phybov_neveducich_dosachu, nakliknuty_stvorec):
    if nakliknuty_stvorec != ():
        riad, stlp = nakliknuty_stvorec
        """Podmienka na to, či vybraný štvorec je figúrka ktorou sa dá hýbať"""
        if SH.sachovnica[riad][stlp][0] == ('w' if SH.Bielytaha else 'b'):
            """Zvýraznenie nakliknutého štvorca"""
            plocha = pg.Surface((StvorcVelk, StvorcVelk))
            plocha.set_alpha(100) # transparentnosť štvrcov
            plocha.fill(pg.Color('blue'))
            obrazovka.blit(plocha, (stlp * StvorcVelk, riad * StvorcVelk))
            """Zvýraznenie pohybov z daného nakliknutého štvorca"""
            plocha.fill(pg.Color('yellow'))
            for pohyb in Generator_phybov_neveducich_dosachu:
                if pohyb.Stlpec_Poc == stlp and pohyb.Riadok_Poc == riad:
                    obrazovka.blit(plocha, (StvorcVelk * pohyb.Stlpec_Konec, StvorcVelk * pohyb.Riadok_Konec))

def Vyobrazenie_sachovnice(obrazovka):
    global Mozne_Farby
    """Táto funkci je zodpovedaná za správne vykreslenie bielych a čierných štvorcov na šachovnici
    Vždicky ľavý horný roh musí byť biely - a list farieb udava index 0 pre bielu farbu a index 1 pre čiernu farbu.
    Potom (riadky + stlpce) % 2 nám da 0 alebo jedničku - Napr. riadok 0 a stlpec 0 nám da 0 - index bielej farby"""
    Mozne_Farby = [pg.Color("white"), pg.Color("brown")]
    for riadky in range(dim):
        for stlpce in range(dim):
            docasfarby = Mozne_Farby[(riadky + stlpce) % 2]
            pg.draw.rect(obrazovka, docasfarby, pg.Rect(stlpce*StvorcVelk, riadky*StvorcVelk, StvorcVelk, StvorcVelk))

def Vyobrazenie_figuriek(obrazovka,sachovnica):
    """Táto funkcia je zodpovedná za poukladanie obrázkov daných figuriek na správne miesta na šachovnici pomocou slovníka,
    do ktorého sme vo funkcií nacitanie_obrázkov dané obrázky figuriek uložili."""
    for riadky in range(dim):
        for stlpce in range(dim):
            figurkadocas = sachovnica[riadky][stlpce]
            if figurkadocas != "--":
                obrazovka.blit(Figurky_Obrazky[figurkadocas],pg.Rect(stlpce*StvorcVelk,riadky*StvorcVelk, StvorcVelk, StvorcVelk))



def Vyobrazenie_stavuHry(obrazovka, SH, Generator_phybov_neveducich_dosachu, nakliknuty_stvorec):
    Vyobrazenie_sachovnice(obrazovka)
    highlighting(obrazovka, SH, Generator_phybov_neveducich_dosachu, nakliknuty_stvorec)
    Vyobrazenie_figuriek(obrazovka, SH.sachovnica)

"""
Funkcia zodpovedná za animáciu pohybu figúrky
"""
def animacia(pohyb, obrazovka, sachovnica, hodinky):
    global Mozne_Farby
    dR = pohyb.Riadok_Konec - pohyb.Riadok_Poc
    dS = pohyb.Stlpec_Konec - pohyb.Stlpec_Poc
    FPS = 10 # rýchlost animácie
    Pocet_obraz = (abs(dS) + abs(dR)) * FPS # počet obrazov pre danú dlžku pohybu figúrky
    for obraz in range(Pocet_obraz):
        riad, stlp = pohyb.Riadok_Poc + dR*obraz/Pocet_obraz, pohyb.Stlpec_Poc + dS*obraz/Pocet_obraz
        Vyobrazenie_sachovnice(obrazovka)
        Vyobrazenie_figuriek(obrazovka, sachovnica)
        """ Pri pohybe figurky, je potrebné túto figurku po každom obraze v smyčke vymazať."""
        farb = Mozne_Farby[(pohyb.Stlpec_Konec + pohyb.Riadok_Konec) % 2]
        Stvorec_kon = pg.Rect(pohyb.Stlpec_Konec * StvorcVelk, pohyb.Riadok_Konec * StvorcVelk, StvorcVelk, StvorcVelk)
        pg.draw.rect(obrazovka, farb, Stvorec_kon)
        """Taktiež ak uživateľ vyhdzuje figúrku, je potrebné aby pri animácií myzla postupne"""
        if pohyb.Figurka_Na_Poziciu != '--':
            obrazovka.blit(Figurky_Obrazky[pohyb.Figurka_Na_Poziciu], Stvorec_kon)
        """Teraz nakreslíme našu hýbajúcu sa figurku, zvlášť pre každý obraz v cykle"""
        obrazovka.blit(Figurky_Obrazky[pohyb.Nakliknuta_Figurka], pg.Rect(stlp * StvorcVelk, riad * StvorcVelk, StvorcVelk, StvorcVelk))
        pg.display.flip()
        hodinky.tick(60)

def kreslenie(obrazovka, string):
    font = pg.font.SysFont('Helvitca', 32, True, False)
    """Nastavenie Fontu písma"""
    text = font.render(string, 0 ,pg.Color('Black'))
    poloha = pg.Rect(0, 0, sirka, vysk).move(sirka/2 - text.get_width()/2, vysk/2 - text.get_height()/2)
    """Nápis, o tom kto vyhral, bude posunutý do stredu obrazovky"""
    obrazovka.blit(text, poloha)


if __name__ == "__main__":
    main()







