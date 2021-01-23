""" Ukaldanie informácii o hry a bude kontrolovat ake su možne pohyby."""


class StavHry():

    def __init__(self):
        """ Šachovnica predstavuje hraciu plochu ktoúu v programe budeme reprezentovať ako 2D list (8x8), v ktorom
            b resp. w je označenie farby (black or white), a 'R' 'N' 'B' 'Q' 'K' 'p' - označujú jednotlivé figurky
            '--' označuje prázdne miesto na hracej ploche"""
        self.sachovnica = [["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                           ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                           ["--", "--", "--", "--", "--", "--", "--", "--"],
                           ["--", "--", "--", "--", "--", "--", "--", "--"],
                           ["--", "--", "--", "--", "--", "--", "--", "--"],
                           ["--", "--", "--", "--", "--", "--", "--", "--"],
                           ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                           ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.Bielytaha = True
        self.slovni_figuriek = {'p': self.pohyby_pesiaka, 'R': self.pohyby_veze, 'N': self.pohyby_Kona, 'B': self.pohyby_Strelca,
                                'Q': self.pohyby_Damy, 'K': self.pohyby_Krala}
        self.historia = []
        """Budem sledovať polohu oboch kraľov, kvôli kontrole možných pohybov a kvôli rošáde"""
        self.w_kingloc = (7, 4)
        self.b_kingloc = (0, 4)
        self.sach_mat = False
        self.mat = False
        """Na začiatku hry uživateľ neporušil zatiaľ žiadne pravidla rošády (napr. nepohol vežou alebo kráľom),
         takže rošada je možná - to neznamená že dovolená (napr. v ceste stoja  iné figúrky)"""
        self.sucasna_moznost_rosady = povolena_rosada(True, True, True, True)
        """Tento zoznam bude ukladať informáciu o tom, či je v danom pohybe splnená podmienka pre rošádu.
         Objekt však musíme skopírovat do zoznamu, inak pri ďalšom appendovaní, budeme mať iba rôzne referencie na ten istý objekt,
         ktorý sa bude pri každom pohybe aktualizovať"""
        self.historia_rosady = [povolena_rosada(self.sucasna_moznost_rosady.wks, self.sucasna_moznost_rosady.bks,
                                                self.sucasna_moznost_rosady.wqs, self.sucasna_moznost_rosady.bqs)]


    """Tátot funkcia vezme premennú pohyby a vykona daný pohyb"""
    def Tah_Figurkou(self, pohyby):
        self.sachovnica[pohyby.Riadok_Konec][pohyby.Stlpec_Konec] = pohyby.Nakliknuta_Figurka
        self.sachovnica[pohyby.Riadok_Poc][pohyby.Stlpec_Poc] = "--"
        """Miesto odkiaľ beriem figúrku ostane prázdne miesto na šachovnici"""
        self.historia.append(pohyby)
        self.Bielytaha = not self.Bielytaha

        """Ak uživateľ ťahá kráľom tak chceme aktualizovať jeho polohu"""
        if pohyby.Nakliknuta_Figurka == 'wK':
            self.w_kingloc = (pohyby.Riadok_Konec, pohyby.Stlpec_Konec)
        elif pohyby.Nakliknuta_Figurka == 'bK':
            self.b_kingloc = (pohyby.Riadok_Konec, pohyby.Stlpec_Konec)
        """Promocia pešiaka na dámu, ak hráč nevyberie inú figurku, tak pešiak bude povýšený na dámu"""
        if pohyby.promo_pesiaka == True:
            self.sachovnica[pohyby.Riadok_Konec][pohyby.Stlpec_Konec] = pohyby.Nakliknuta_Figurka[0] + 'Q'
        """Konečný pohyb rošády - kráľ sa už pohol na začiatku tejto funkcie,
        a teraz treba zabezpečiť aby sa pohla aj veža"""
        if pohyby.rosada:
            if pohyby.Stlpec_Konec - pohyby.Stlpec_Poc == 2:  # Rošáda na strane Krála
                self.sachovnica[pohyby.Riadok_Konec][pohyby.Stlpec_Konec - 1] = self.sachovnica[pohyby.Riadok_Konec][
                    pohyby.Stlpec_Konec + 1]
                # pohyb vežou na šachovnici
                self.sachovnica[pohyby.Riadok_Konec][pohyby.Stlpec_Konec + 1] = '--'
                # vymažeme vežu zo starého miesta na šachovnici
            elif pohyby.Stlpec_Konec - pohyby.Stlpec_Poc == - 2:  # Rošáda na strane dámy
                self.sachovnica[pohyby.Riadok_Konec][pohyby.Stlpec_Konec + 1] = self.sachovnica[pohyby.Riadok_Konec][
                    pohyby.Stlpec_Konec - 2]
                self.sachovnica[pohyby.Riadok_Konec][pohyby.Stlpec_Konec - 2] = '--'
        """Keď sa kráľ alebo veža pohne, musíme aktualizovať informáciu o tom, či je rošáda možná"""
        self.aktualizacia_moznej_rosady(pohyby)
        """Po tom čo aktualizujeme, tak appendujeme do historie_rošády"""
        self.historia_rosady.append(povolena_rosada(self.sucasna_moznost_rosady.wks, self.sucasna_moznost_rosady.bks,
                                                self.sucasna_moznost_rosady.wqs, self.sucasna_moznost_rosady.bqs))






    """Táto funkcia vráti posledný ťah"""
    def Undofunkcia(self):
        """Funkcia ktorá vyberie posladný ťah z historie - čo je vlastne objekt pohyb:
                     V tomto objekete su uložene počiatočne a konečne polohy figuriek daného ťahu.
                     Stačí teda prepísať naspäť tento stav na šachovnici do pôvodnej polohy"""
        if len(self.historia) != 0:
            pohyb = self.historia.pop()
            self.sachovnica[pohyb.Riadok_Konec][pohyb.Stlpec_Konec] = pohyb.Figurka_Na_Poziciu
            self.sachovnica[pohyb.Riadok_Poc][pohyb.Stlpec_Poc] = pohyb.Nakliknuta_Figurka
            self.Bielytaha = not self.Bielytaha
            """
            Ak vraciame pohyb s kráľom, tak chceme aktualizovat jeho polohu
            """
            if pohyb.Nakliknuta_Figurka == 'wK':
                self.w_kingloc = (pohyb.Riadok_Poc, pohyb.Stlpec_Poc)
            elif pohyb.Nakliknuta_Figurka == 'bK':
                self.b_kingloc = (pohyb.Riadok_Poc, pohyb.Stlpec_Poc)
            """
            Undo rošády
            """
            if pohyb.rosada:
                if pohyb.Stlpec_Konec - pohyb.Stlpec_Poc == 2:
                    self.sachovnica[pohyb.Riadok_Konec][pohyb.Stlpec_Konec + 1] = self.sachovnica[pohyb.Riadok_Konec][
                        pohyb.Stlpec_Konec - 1]
                    self.sachovnica[pohyb.Riadok_Konec][pohyb.Stlpec_Konec - 1] = '--'
                else:
                    self.sachovnica[pohyb.Riadok_Konec][pohyb.Stlpec_Konec - 2] = self.sachovnica[pohyb.Riadok_Konec][
                        pohyb.Stlpec_Konec + 1]
                    self.sachovnica[pohyb.Riadok_Konec][pohyb.Stlpec_Konec + 1] = '--'
            """
            Undo práv možnej rošady pre daný pohyb
            """
            self.historia_rosady.pop()   #vyhadzujeme poslednú zápis informácie o rošáde.
            self.sucasna_moznost_rosady = self.historia_rosady[-1] #Nastavujeme súčasnu informaciu o rošáde na poslednú z listu.









    """Funkcia ktorá v každom pohybe kontroluje pravidla rošády."""
    def aktualizacia_moznej_rosady(self, pohyb):
        """Ak sa pohne figúrka kráľa, tak rošáda už nieje možná"""
        if pohyb.Nakliknuta_Figurka == 'wK':
            self.sucasna_moznost_rosady.wks = False
            self.sucasna_moznost_rosady.wqs = False
        elif pohyb.Nakliknuta_Figurka == 'bK':
            self.sucasna_moznost_rosady.bks = False
            self.sucasna_moznost_rosady.bqs = False
            """Taktiež, ak sa pohne veža na danej strane, tak uživateľ stráca možnosť rošády na danej strane"""
        elif pohyb.Nakliknuta_Figurka == 'wR':
            if pohyb.Riadok_Poc == 7:
                """Prípad ľavej veže"""
                if pohyb.Stlpec_Poc == 0:
                    """Tak uživateľ stráca možnosť rošády na strane s dámou"""
                    self.sucasna_moznost_rosady.wqs = False
                    """Prípad pravej veže"""
                elif pohyb.Stlpec_Poc == 7:
                    """Tak uživateľ stráca možnosť rošády na strane s kráľom"""
                    self.sucasna_moznost_rosady.wks = False
        elif pohyb.Nakliknuta_Figurka == 'bR':
            """Podobný princíp pre čiernu stranu."""
            if pohyb.Riadok_Poc == 0:
                """Prípad ľavej veže"""
                if pohyb.Stlpec_Poc == 0:
                    self.sucasna_moznost_rosady.bqs = False
                    """Prípad pravej veže"""
                elif pohyb.Stlpec_Poc == 7:
                    self.sucasna_moznost_rosady.bks = False



    """Táto funkcia sa bude starať o to, aby uživateľ neurobil pohyb,
     ktorý automaticky vedie k šachovaniu nepriateľskou figúrkou"""
    def Generator_phybov_neveducich_dosachu(self):
        doc_moznost_rosady = povolena_rosada(self.sucasna_moznost_rosady.wks, self.sucasna_moznost_rosady.bks,
                                                self.sucasna_moznost_rosady.wqs, self.sucasna_moznost_rosady.bqs)
        """Kopia súčasných práv na rošádu, robíme to hlavne kvôli tomu že,
          generácia pohybov nám mení tieto práva, 
          lebo medzi generovanými pohybmi sú i pohyby v ktorých sa pohol kráľ alebo veža."""
        """Najprv dovolíme, aby boli povolené všetky možné pohyby."""
        pohyby = self.Generator_moznych_pohybov()
        """Rošáda:"""
        if self.Bielytaha:
            self.pohyby_rosady(self.w_kingloc[0], self.w_kingloc[1], pohyby)
        else:
            self.pohyby_rosady(self.b_kingloc[0], self.b_kingloc[1], pohyby)
        """Hráčovi povolíme urobiť daný pohyb"""
        for i in range(len(pohyby) - 1, -1, -1):
            self.Tah_Figurkou(pohyby[i])
            """Vygenerujem všetky možne súperové pohyby, a pre každý superov pohyb skontrolujeme, či sa kríži s kráľom.
                    Za túto kontrolu je zodpovedná funkcia - Sach."""
            """Ale najprv musíme prehodiť kola, pretože biely už ťahal (čierny je na ťahu),
             a ja robím kontrolu pre súperové (čierny hráč) ťahy"""
            self.Bielytaha = not self.Bielytaha
            if self.Sach():
                """Iterujeme od konca, aby pri posune indexov nedochádzalo k bugom"""
                pohyby.remove(pohyby[i])
            """ Ďalej prehodíme to, kto je na rade do pôvodného stavu"""
            self.Bielytaha = not self.Bielytaha
            """Vždy vrátime figurku na miesto, po tom čo sme skontrolovali jej ťahy"""
            self.Undofunkcia()
        """Ak nemáme žiadne dovolené pohyby, tak buď to znamená že kráľ je šachovaný, alebo šach-matovaný"""
        if len(pohyby) == 0:
            if self.Sach():
                self.sach_mat = True
            else:
                self.mat = True
        else:
            self.sach_mat = False
            self.mat = False
        self.sucasna_moznost_rosady = doc_moznost_rosady
        return pohyby


    """Táto funkcia bude zodpovedaná za kontrolu, či je hráč je po svojom ťahu v šachu"""
    def Sach(self):
        if self.Bielytaha:
            return self.Kral_utok(self.w_kingloc[0], self.w_kingloc[1])
        else:
            return self.Kral_utok(self.b_kingloc[0], self.b_kingloc[1])

    """Funkcia zodpovedná za kontrolu súperovho útoku na miesto (riad,stlp)"""
    def Kral_utok(self, riad, stlp):
        """Prehodíme ťah za superov ťah, aby sme mohli vygenerovať všetký možné  pohyby superovho kola"""
        self.Bielytaha = not self.Bielytaha
        sup_pohyby = self.Generator_moznych_pohybov()
        """Prehodíme to, kto je na ťahu do pôvodného stavu, po tom čo sme vygenereovali súperové pohyby."""
        self.Bielytaha = not self.Bielytaha
        for pohyb in sup_pohyby:
            if pohyb.Riadok_Konec == riad and pohyb.Stlpec_Konec == stlp:
                """Ak je splnená podmienak, že superová figúrka sa kríži s kráľom, tak vrátime True"""
                return True
        """Ak je splnená podmienak, že žiadna zo superových figúriek sa nekríži s kráľom, tak vrátime False"""
        return False


    """Táto funkcia bude generovať všetký možné pohyby figúriek,
     s ohľadom na pravidla ťahov v šachu pre daný stav šachovnice"""
    def Generator_moznych_pohybov(self):
        list_pohybov = []
        """Do tohto zozonamu budú ukladané pohyby ktoré splňaju pravidlá šachu."""
        """Všetky možné pohyby budeme musiet generovat pomocou prehľadávania šachovnice,
         a kontrolovania pohybov pre špecifické figurky"""
        for riadok in range(8):
            for stlpec in range(8):
                Farba_Figurky = self.sachovnica[riadok][stlpec][0]
                """pozicia 0 označuje 1. znak stringu na šachovnici - tento charakter označuje farbu figurky"""
                Figurka = self.sachovnica[riadok][stlpec][1]
                """pozicia 1 označuje 2.znak stringu na šachovnici - tento charakter označuje príslušnú figuku"""
                if (Farba_Figurky == 'w' and self.Bielytaha == True) or (Farba_Figurky == 'b' and self.Bielytaha == False):
                    self.slovni_figuriek[Figurka](riadok, stlpec, list_pohybov)
        return list_pohybov

    """Táto funcia kladie podmienky na pohyby pešiaka"""
    def pohyby_pesiaka(self, riad, stlp, lis):
        """Biely a čierny pešiaci sa pohybujú  oproti sebe - je potrebné vyriešit pohyby farieb zvlašť"""
        if self.Bielytaha:
           """Overovanie pohybu o jeden štvorec vpred pre bielych pešiakov"""
           if self.sachovnica[riad - 1][stlp] == '--':
               lis.append(Pohyby((riad, stlp), (riad - 1, stlp), self.sachovnica))
               """Overovanie pohybov bielych pešiakov o dva štvorce vpred (možné len ak pešiak stoji na riadku 6)"""
               if riad == 6 and self.sachovnica[riad - 2][stlp] == '--':
                   lis.append(Pohyby((riad, stlp), (riad - 2, stlp), self.sachovnica))
           if  stlp - 1 >= 0:
               """Overovanie možného vyhodenia čiernej figúrky smerom do ľava"""
               if self.sachovnica[riad - 1][stlp - 1][0] == 'b':
                   lis.append(Pohyby((riad, stlp), (riad - 1, stlp - 1), self.sachovnica))
           if  stlp + 1 <= 7:
               """Overovanie možného vyhodenia čiernej figúrky smerom do prava"""
               if self.sachovnica[riad - 1][stlp + 1][0] == 'b':
                   lis.append(Pohyby((riad, stlp), (riad - 1, stlp + 1), self.sachovnica))
        else:
            """Prípad, keď sú čierny pešiaci na ťahu"""
            if self.sachovnica[riad + 1][stlp] == '--':
                lis.append(Pohyby((riad, stlp), (riad + 1, stlp), self.sachovnica))
                """Overovanie pohybov čiernych pesiakov o dva štvorce vpred (možné, len ak pešiak stoji na riadku 1)"""
                if riad == 1 and self.sachovnica[riad + 2][stlp] == '--':
                    lis.append(Pohyby((riad, stlp), (riad + 2, stlp), self.sachovnica))
            if stlp - 1 >= 0:
                """Overovanie možného vyhodenia bielej figúrky smerom do ľava"""
                if self.sachovnica[riad + 1][stlp - 1][0] == 'w':
                    lis.append(Pohyby((riad, stlp), (riad + 1, stlp - 1), self.sachovnica))
            if stlp + 1 <= 7:
                """Overovanie možného vyhodenia bielej figúrky smerom do prava"""
                if self.sachovnica[riad + 1][stlp + 1][0] == 'w':
                    lis.append(Pohyby((riad, stlp), (riad + 1, stlp + 1), self.sachovnica))



    def pohyby_veze(self, riad, stlp, lis):
        Mozne_Stavy = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        """Veže sa môžu pohybovať buď len po riadkoch, alebo  po stlpcoch"""
        Farba = 'w' if self.Bielytaha else 'b'
        for Stav in Mozne_Stavy:
            for i in range(1, 8):
                Novy_Riadok = riad + Stav[0] * i
                Novy_Stlpec = stlp + Stav[1] * i
                if 0 <= Novy_Riadok <= 7 and 0 <= Novy_Stlpec <= 7:
                    if self.sachovnica[Novy_Riadok][Novy_Stlpec] == '--':
                        lis.append(Pohyby((riad, stlp), (Novy_Riadok, Novy_Stlpec), self.sachovnica))
                        """Ak je políčko prázdne - ťah je pridaný do generátoru možných ťahov"""
                    elif self.sachovnica[Novy_Riadok][Novy_Stlpec] != '--' and self.sachovnica[Novy_Riadok][Novy_Stlpec][0] != Farba:
                        lis.append(Pohyby((riad, stlp), (Novy_Riadok, Novy_Stlpec), self.sachovnica))
                        break
                        """Ak na poličku stojí nepriateľska figúrka - ťah je pridaný do generátoru možných ťahov"""
                    elif self.sachovnica[Novy_Riadok][Novy_Stlpec][0] == Farba:
                        break
                        """Inak je cyklus prerušený"""






    def pohyby_Strelca(self, riad, stlp, lis):
        Mozne_Stavy = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        """Strelec sa môže pohybovať po diagonálach"""
        if self.Bielytaha == True:
            Farba_na_Vyhodenie = 'b'
        else:
            Farba_na_Vyhodenie = 'w'
        for Stav in Mozne_Stavy:
            for i in range(1, 8):
                Novy_Riadok = riad + Stav[0] * i
                Novy_Stlpec = stlp + Stav[1] * i
                if 7 >= Novy_Riadok >= 0 and 7 >= Novy_Stlpec >= 0:
                    if self.sachovnica[Novy_Riadok][Novy_Stlpec] == '--':
                        lis.append(Pohyby((riad, stlp), (Novy_Riadok, Novy_Stlpec), self.sachovnica))
                        """Ak je políčko prázdne - ťah je pridaný do generátoru možných ťahov"""
                    elif self.sachovnica[Novy_Riadok][Novy_Stlpec][0] == Farba_na_Vyhodenie:
                        """Ak na poličku stojí súperová figúrka - ťah je pridaný do generátoru možných ťahov"""
                        lis.append(Pohyby((riad, stlp), (Novy_Riadok, Novy_Stlpec), self.sachovnica))
                        break
                    else:
                        break




    def pohyby_Damy(self, riad, stlp, lis):
        self.pohyby_veze(riad, stlp, lis)
        self.pohyby_Strelca(riad, stlp, lis)
        """Dáma sa može pohybovať ako veža a strelec , ktorých možné pohyby sme naimplementovali vyššie"""


    def pohyby_Krala(self, riad, stlp, lis):
        Mozne_Stavy = [(-1, 1), (-1, -1,), (1, -1), (1, 1), (1, 0), (-1, 0), (0, -1), (0, 1)]
        """Kráľ sa môže pohybovať o jedno poličko do všetkých strán"""
        Farba = 'w' if self.Bielytaha else 'b'
        for Stavy in Mozne_Stavy:
            Novy_Riadok = riad + Stavy[0]
            Novy_Stlpec = stlp + Stavy[1]
            if 7 >= Novy_Riadok >= 0 and 7 >= Novy_Stlpec >= 0:
                if self.sachovnica[Novy_Riadok][Novy_Stlpec][0] != Farba:
                    lis.append(Pohyby((riad, stlp), (Novy_Riadok, Novy_Stlpec), self.sachovnica))
                    """Ak je políčko prázdne - ťah je pridaný do generátoru možných ťahov"""
                    """Ak na poličku stojí súperová figúrka - ťah je pridaný do generátoru možných ťahov"""




    """
    Funkcia zodpovedná za generáciu povoelených pohybov rošády resp. pohybov kráľa na na pozicií (riad,stlp).
    """
    def pohyby_rosady(self, riad, stlp, pohyby):
        if self.Kral_utok(riad, stlp): #Ak je král pod útokom uživateľ nemôže robiť rošádu
            return
        if (self.Bielytaha and self.sucasna_moznost_rosady.wqs) or (not self.Bielytaha and self.sucasna_moznost_rosady.bqs):
            if self.sachovnica[riad][stlp - 1] == '--' and self.sachovnica[riad][stlp - 2] == '--' and self.sachovnica[riad][stlp - 3] == '--':
                if not self.Kral_utok(riad, stlp - 1) and not self.Kral_utok(riad, stlp - 2):
                    Farba = 'biela' if self.Bielytaha else 'čierna'
                    print("Rošáda možná na strane Dámy: ", Farba)
                    pohyby.append(Pohyby((riad, stlp), (riad, stlp - 2), self.sachovnica, rosada=True))
        if (self.Bielytaha and self.sucasna_moznost_rosady.wks) or (not self.Bielytaha and self.sucasna_moznost_rosady.bks):
            if self.sachovnica[riad][stlp + 1] == '--' and self.sachovnica[riad][stlp + 2] == '--':  # kontrola či su štvorce prázdne.
                if not self.Kral_utok(riad,stlp + 1) and not self.Kral_utok(riad,stlp + 2):  # kontrola, či dane polia niesú v šachu.
                    Farba = 'biela' if self.Bielytaha else 'čierna'
                    print("Rošáda možná na strane Kráľa: ", Farba)
                    pohyby.append(Pohyby((riad, stlp), (riad, stlp + 2), self.sachovnica, rosada=True))



    def pohyby_Kona(self, riad, stlp, lis):
        Mozne_Stavy = [(riad - 2, stlp - 1), (riad - 2, stlp + 1), (riad - 1, stlp - 2), (riad - 1, stlp + 2),
                       (riad + 2, stlp - 1), (riad + 2, stlp + 1), (riad + 1, stlp - 2), (riad + 1, stlp + 2)]
        """Kôn sa môže pohybovať po L-kách do všetkých strán od svojho miesta"""
        Farba_Na_Vyhodenie = 'b' if self.Bielytaha else 'w'
        for Stav in Mozne_Stavy:
            Novy_Riadok = Stav[0]
            Novy_Stlpec = Stav[1]
            if 7 >= Novy_Riadok >= 0 and 7 >= Novy_Stlpec >= 0:
                if self.sachovnica[Novy_Riadok][Novy_Stlpec] == '--':
                    lis.append(Pohyby((riad, stlp), (Novy_Riadok, Novy_Stlpec), self.sachovnica))
                    """Ak je políčko prázdne - ťah je pridaný do generátoru možných ťahov"""
                elif self.sachovnica[Novy_Riadok][Novy_Stlpec][0] == Farba_Na_Vyhodenie:
                    """Ak na poličku stojí súperová figúrka - ťah je pridaný do generátoru možných ťahov"""
                    lis.append(Pohyby((riad, stlp), (Novy_Riadok, Novy_Stlpec), self.sachovnica))



"""Trieda zodpovedná za kontrolovanie, či je rošáda možná resp. či sú splnené podmienky pre rošádu."""
class povolena_rosada():
    def __init__(self, wks, bks, wqs, bqs):
        """Inicializacie premenných triedy, kde napr. wks  - strana bieleho kráľa , bqs - strana čiernej dámy
        (rošada je možna na obe strany).Takže táto trieda zodpovedá za ukladanie informácií o tom, či je rošáda možná"""
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


class Pohyby():
    """ Zavedieme notáciu typickú pre šachové polia - pretože v terajšom prípade je napr. na poli (0,0) čierna veža.
    V šachovej terminologií to je však  8mi riadok  a stlpec A - preto použijem slovniky na mapovanie tejto notacie"""
    Preklad_notacie_do_riadkov = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    """Napríklad v šachovej notacií je "1" riadok, riadok s indexom 7 v súčasnom značení atd.."""
    Preklad_Riadkov_Do_Notacie = { Hodnota: Kluc for Kluc, Hodnota in Preklad_notacie_do_riadkov.items()}
    """ Slovník ktorý preklada notáciu z jazyka riadkov do šachovej notácie. A teda slovník opačný k predchádzajúcemu"""
    Preklad_notacie_do_stlpcov = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    """Slovník ktorý vraví že stlpec a,b,c ... je vlastne stlpec 0,1,2 v terajšej notácií"""
    Preklad_Stlpcov_do_notacie = {Hodnota: Kluc for Kluc, Hodnota in Preklad_notacie_do_stlpcov.items()}
    slovnik_figuriek = {'p': "pešiak", 'Q': "dáma", 'K': "král", 'N': "kôn", 'B': "strelec", 'R': "veža"}

    def __init__(self, Pociatocny_Stvorec, Konecny_Stvorec, sachovnica, rosada=False):
        """Inicializácia premenných v triede pohyby - ktorá je zodpovedná za premiestnovanie figúriek z počiatočnej polohy,
        na konečnú polohu."""
        self.Riadok_Poc = Pociatocny_Stvorec[0]
        self.Stlpec_Poc = Pociatocny_Stvorec[1]
        self.Riadok_Konec = Konecny_Stvorec[0]
        self.Stlpec_Konec = Konecny_Stvorec[1]
        self.Nakliknuta_Figurka = sachovnica[self.Riadok_Poc][self.Stlpec_Poc]
        self.Figurka_Na_Poziciu = sachovnica[self.Riadok_Konec][self.Stlpec_Konec]
        """Modifikácia triedy pohyby - kvôli uchovávaniu informácie či v danom pohybe ide o promociu pešiaka"""
        self.promo_pesiaka = False
        if (self.Nakliknuta_Figurka == 'wp' and self.Riadok_Konec == 0) or (self.Nakliknuta_Figurka == 'bp' and self.Riadok_Konec == 7):
            self.promo_pesiaka = True
            """Ak pešiak dôjde na koniec šachovnice, tak ide o promociu pešiaka, a 
            hráč si môže zvoliť figúrku, a ak si nezvolí, automaticky bude zvolená Dáma"""
        self.Identifikacne_Cislo_Tahu = self.Riadok_Poc * 1000 + self.Stlpec_Poc * 100 + self.Riadok_Konec * 10 + self.Stlpec_Konec
        """Táto premenna vytvára identifikačné číslo špecifické pre každý ťah - je potrebná aby sme vedeli porovnavať instancie.
        Napr. porovnat objekt Pohyby s objektom Generatorom_mozných_pohybov"""
        """rošáda"""
        self.rosada = rosada

    def __eq__(self, other):
        if isinstance(other, Pohyby):
            return other.Identifikacne_Cislo_Tahu == self.Identifikacne_Cislo_Tahu
        else:
            return False

    def Preklad_do_notacie_helper(self,riadok, stlpec):
        return self.Preklad_Riadkov_Do_Notacie[riadok] + self.Preklad_Stlpcov_do_notacie[stlpec] + " "

    def Preklad_do_notácie(self):
        if self.slovnik_figuriek[self.Nakliknuta_Figurka[1]][-1] == 'a':
            Farba = "Biela " if self.Nakliknuta_Figurka[0] == 'w' else "Čierna "
            Farba_op = "Čierna" if self.Nakliknuta_Figurka[0] == 'w' else "Biela "
        else:
            Farba = "Biely " if self.Nakliknuta_Figurka[0] == 'w' else "Čierny "
            Farba_op = "Čierny" if self.Nakliknuta_Figurka[0] == 'w' else "Biely "
        if self.Figurka_Na_Poziciu == '--':
            return Farba + self.slovnik_figuriek[self.Nakliknuta_Figurka[1]] + " z pozície " \
                   + self.Preklad_do_notacie_helper(self.Riadok_Poc, self.Stlpec_Poc) + \
                    " na pozíciu " + self.Preklad_do_notacie_helper(self.Riadok_Konec, self.Stlpec_Konec)
        else:
            return Farba + self.slovnik_figuriek[self.Nakliknuta_Figurka[1]] + " z pozície " \
                   + self.Preklad_do_notacie_helper(self.Riadok_Poc, self.Stlpec_Poc) + \
                   " vyhadzuje " + Farba_op + " " + self.slovnik_figuriek[self.Figurka_Na_Poziciu[1]]  \
                   + " na pzícií " + self.Preklad_do_notacie_helper(self.Riadok_Konec, self.Stlpec_Konec)
    """Funkcie triedy pohyby, ktoré nám budú zabzpečovat preklad do šachovej notácie pri nakliknutí figurky,
    a následnom položení figurky na dané miesto"""

