# ChessByKarol
Po stiahnutí súboru Chess.zip(v ktorom sú Images.zip, ChessEngine, ChessMain), je potrebné súbory vložiť do jedného priečinku (ChessEngine a ChessMain spolu s rozbaleným súborom Images.zip).
Chess main vyžaduje balíček pygame. 
Výstupom tohto programu je klasická šachová partia medzi dvojicou hráčou.
Šach spustíme kliknutím na zelenú šipku (Štart - klasicke spúštanie programu Python) v pravom hornom rohu.
Po kliknutí na šipku, sa zobrazí šachová hracia plocha.

UI - User interface:

Kliknutím ľavým tlačidlom myše na príslušnú figúrku, a následným kliknutím na požadované políčko,
na ktoré sa má fígrka presunúť,dôjde k príslušnému ťahu figúrkou.

Dvojnásobným kliknutím ľavým tlačidlom myše na príslušnú figúrku po sebe, dôjde k odznačeniu príslušnej figúrky. 
Ak uživateľ klikne na figúrku a rozmyslí si svoj ťah, tak jednoduchým prekliknutím na inú figúrku program spozná, 
že uživateľ chce urobiť ťah inou figúrkou.

Klávesa - r - reset hry

Klávesa - z - Undo - pohybu (krok -späť)

Ak je hráč dôjde pešiakom na koniec šachovnice, tak automaticky dôje k promocií na dámu. Ak by hráč chcel povýšiť pešiaka
na inú figúrku - tak v dolnom okne sa zobrazia klávesové skratky pre výber jednotlivých figuriek:
q - Dáma, n - kôň, b - Strelec, v - Veža

Ak sú splnené podmienky pre rošádu na danej strane (biely hráč resp. čierny hráč),
tak jednoduchým klknutím na kráľa, a následným kliknutím na políčko,
ktoré je vzdialené dva polia do prava resp. do ľava (záleží na ktorej strane sú splenené podmienky pre rošádu),
dôjde k rošáde (kráľ sa posunie o dva polia do prava resp. do ľava a príslušným spôsobom sa presunie i veža).

Taktiež sa dá všimnúť, že nakliknutím na príslušnú figurku dochádza k zvýrazneniu možných políčok, 
vrámci ktorých sa daná figúrka môže presúvať.
V dolnom textovom okne programu PyCharm, budú príslušné ťahy vypisované v šachovej notácií
Taktiež ak je hráč šachovaný v dolnom textovom okne programu PyCharm, bude šach vypísaný.
