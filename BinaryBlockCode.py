import tkinter as tk
import math


class BinaryBlockCode(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # frame koji sadrzi pojedinu stranicu
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # konzola
        consoleFrame = tk.Frame(self)
        consoleFrame.pack(side="bottom", fill="both", expand=True)
        # scrollbar konzole
        scroll = tk.Scrollbar(consoleFrame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.console = tk.Text(consoleFrame, height=10, width=30)
        self.console.pack(side="left", fill="both", expand=True)
        scroll.config(command=self.console.yview)
        self.console.config(yscrollcommand=scroll.set)

        labelConsole = tk.Label(self, text="Console window")
        labelConsole.pack(side="bottom")

        # rjecnik svih stranica
        self.frames = {}
        # broj redaka generirajuce matrice
        self.rows = 0
        # broj stupaca generirajuce matrice
        self.columns = 0
        # lista svih generiranih polja za unos
        self.entries = []
        # generirajuca matrica
        self.genMat = []
        # abeceda koda
        self.alphabet = [0, 1]
        # vektorski prostor
        self.n = 0
        # dimenzija koda
        self.k = 0
        # sve kodne rijeci koda
        self.codeWords = []

        for F in (StartPage, InstructionsPage, GenMatPage, CodingPage):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        """funkcija za prikaz odredjenog frame-a"""

        frame = self.frames[cont]
        frame.tkraise()

    def saveRowsAndColumns(self):
        """ funkcija za spremanje broja unesenih redaka i stupaca generirajuce matrice
        :return:
        """

        if self.frames[GenMatPage].entryRows.get() != "":
            try:
                self.rows = int(self.frames[GenMatPage].entryRows.get())
                self.console.insert(tk.END, "broj redaka: " + str(self.rows) + "\n")
                self.console.see(tk.END)
            except ValueError:
                self.console.insert(tk.END, "[ERROR] broj redaka mora biti pozitivan broj\n")
                self.console.see(tk.END)

        else:
            self.console.insert(tk.END, "[WARNING] unesite ispravan broj redaka\n")
            self.console.see(tk.END)

        if self.frames[GenMatPage].entryColumns.get() != "":
            try:
                self.columns = int(self.frames[GenMatPage].entryColumns.get())
                self.console.insert(tk.END, "broj stupaca: " + str(self.columns) + "\n")
                self.console.see(tk.END)
            except ValueError:
                self.console.insert(tk.END, "[ERROR] broj stupaca mora biti pozitivan broj\n")
                self.console.see(tk.END)

        else:
            self.console.insert(tk.END, "[WARNING] unesite ispravan broj stupaca\n")
            self.console.see(tk.END)

    def makeEntries(self):
        """ Funkcija za generiranje polja za unos u frameu GenMatPage

        :return:
        """

        # gumbe nije moguce pritisnuti sve dok se ne stvori generirajuca matrica
        self.frames[GenMatPage].buttonCodingSpeed['state'] = 'disabled'
        self.frames[GenMatPage].buttonNormalize['state'] = 'disabled'
        self.frames[GenMatPage].buttonLin['state'] = 'disabled'
        self.frames[GenMatPage].buttonNK['state'] = 'disabled'
        self.frames[GenMatPage].buttonCode['state'] = 'disabled'

        # ako je prethodno postojalo polja za unos, unistavaju se
        for widget in self.frames[GenMatPage].entryFrame.winfo_children():
            widget.destroy()

        self.entries = []

        # stvaranje polja
        for i in range(self.rows):

            entryRow = tk.Frame(self.frames[GenMatPage].entryFrame)
            entryRow.pack()

            for j in range(self.columns):
                entry = tk.Entry(entryRow)
                entry.pack(side="left", padx=10, pady=10)
                self.entries.append(entry)

    def getGenMat(self):
        """ Funkcija za stvaranje generirajuce matrice
        Uzimaju se vrijednosti iz vec generiranih polja za unos

        :return:
        """
        self.genMat = []
        inputs = []

        try:
            for e in self.entries:
                if int(e.get()) == 1 or int(e.get()) == 0:
                    inputs.append(int(e.get()))
                else:
                    self.console.insert(tk.END, "[ERROR] sve vrijednosti moraju biti iz skupa [0, 1]\n")
                    self.console.see(tk.END)

            for i in range(self.rows):
                row = [0] * self.columns
                for j in range(self.columns):
                    row[j] = inputs[j + self.columns * i]
                self.genMat.append(row)

            # omogucavanje gumba posto je stvorena generirajuca matrica
            self.frames[GenMatPage].buttonCodingSpeed['state'] = 'normal'
            self.frames[GenMatPage].buttonNormalize['state'] = 'normal'
            self.frames[GenMatPage].buttonLin['state'] = 'normal'
            self.frames[GenMatPage].buttonNK['state'] = 'normal'
            self.frames[GenMatPage].buttonCode['state'] = 'normal'

            # vektorski prostor
            self.n = self.genMat[0].__len__()
            # dimenzija koda
            self.k = self.genMat.__len__()

        except ValueError:
            self.console.insert(tk.END, "[ERROR] sve vrijednosti moraju biti iz skupa [0, 1]\n")
            self.console.see(tk.END)

    def xor(self, row, patternRow, destinationIndex):
        """ Funkcija iskljucivo ili koja uzima redak row i redak gdje se nalazi pattern,
        napravi iskljucivo ili izmedju ta dva retka i zapise rezultat u destinationIndex redak
        generirajuce matrice

        :param row: prvi redak u operaciji
        :param patternRow: drugi redak u operaciji
        :param destinationIndex: redak za zapis rezultata
        :return:
        """

        v1 = self.genMat[row]
        v2 = self.genMat[patternRow]

        v3 = [0] * v1.__len__()

        for i in range(v3.__len__()):
            v3[i] = v1[i] ^ v2[i]

        self.genMat[destinationIndex] = v3

    def isGenMatStandardized(self):
        """ Funkcija za provjeru je li generirajuca matrica standardizirana, odnosno je li u standardnoj formi

        :return: true ako je matrica u standardnom obliku, false ako nije
        """

        #FIXME
        flag = True

        for i in range(self.k):

            if self.genMat[i][i] == 0:
                self.console.insert(tk.END, "generirajuca matrica nije u standardnom obliku\n")
                self.console.see(tk.END)
                flag = False
                break

            for j in range(self.k):
                if j == i:
                    continue
                if self.genMat[i][j] == 1:
                    print("generirajuca matrica nije standardizirana")
                    flag = False
                    break
        if flag:
            self.console.insert(tk.END, "generirajuca matrica je u standardnom obliku\n")
            self.console.see(tk.END)

    def swapRows(self, r1, r2):
        """ Funkcija za zamjenu dva retka generirajuce matrice
        :param r1: prvi redak
        :param r2: drugi redak
        :return:
        """

        temp = self.genMat[r1]
        self.genMat[r1] = self.genMat[r2]
        self.genMat[r2] = temp

    def swapColumns(self, c1, c2):
        """ Funkcija za zamjenu dva stupca generirajuce matrice
        :param c1: prvi stupac
        :param c2: drugi stupac
        :return:
        """

        for row in range(self.rows):
            temp = self.genMat[row][c1]
            self.genMat[row][c1] = self.genMat[row][c2]
            self.genMat[row][c2] = temp

    def getColumn(self, index):
        """ Funkcija za dohvat jednog stupca generirajuce matrice
        :param index: indeks stupca
        :return: stupac generirajuce matrice
        """

        numOfRows = self.genMat.__len__()

        result = [0] * numOfRows

        for row in range(numOfRows):
            result[row] = self.genMat[row][index]

        return result

    def containsColumn(self, index):
        """ Funkcija za provjeru sadrzi li generirajuca matrica stupac odredjenog izgleda.
        Npr. ako je broj redaka matrice 3, da bi matrica bila standardizirana prvi stupac mora izgledati
        [1, 0, 0](transponirano), drugi [0, 1, 0] itd. Ova funkcija provjerava je li stupac index upravo u ovom
        obliku koji naravno ovisi o dimenzionlanosti

        :param index: indeks stupca koji se provjerava
        :return: -1 -> ne postoji, index -> gdje se nalazi u matrici trazeni stupac
        """
        numOfRows = self.genMat.__len__()
        numOfColumns = self.genMat[0].__len__()

        # trazeni stupac koji ima na poziciji index jedinicu
        target = [0] * numOfRows
        target[index] = 1

        for column in range(numOfColumns):

            temp = self.getColumn(column)

            if temp == target:
                return column

        return -1

    def findPattern(self, currentColumn):
        """ Funkcija za pronalazak uzorka, npr. pocetak retka [0,0,1,...], ovisno o tome
        koji je trenutni indeks stupca

        Primjer:
            Da bi u matrici [1, 1, 0]
                            [0, 1, 0]
                            [0, 0, 1]
            razrjesili jedinicu na indeksu (1, 2) moramo pronaci redak [0, 1, ...] jer ce
            taj redak dati rezultantni redak mnozenja [1, 0, ...], a sto nam pomaze
            kod standardizacije matrice

            Ova funkcija upravo vrace indeks retka s tim potrebitim uzorkom.

        :param currentColumn: trenutni indeks stupca
        :return: broj retka s trazenim uzorkom
        """

        numOfRows = self.genMat.__len__()

        pattern = [0] * (currentColumn + 1)
        pattern[currentColumn] = 1

        for row in range(numOfRows):
            ok = True
            for i in range(pattern.__len__()):
                if self.genMat[row][i] != pattern[i]:
                    ok = False
                    break
            if ok:
                return row
        return -1

    def multiplyMod2(self, v):
        """ Funkcija za mnozenje kodne rijeci v i trenutne generirajuce matrice

        :param v: vektor koji mnozi generirajucu matricu
        :return: rezultantni vektor
        """

        result = [0] * self.columns

        for c in range(self.columns):

            column = self.getColumn(c)

            for i in range(self.rows):
                result[c] += v[i] * column[i]

        return [x % 2 for x in result]

    def generateCodeWords(self, dim):
        """ funkcija za stvaranje kodnih rijeci dimenzije :param dim
        :param dim: dimenzija pojedine kodne rijeci
        :return: lista kodnih rijeci
        """

        # lista kodnih rijeci
        codeWords = []

        # kodnih rijeci ima 2 na zeljenu duljinu, odnosno dim
        # prvo se generiraju binarne reprezentacije decimalnih brojeva
        for i in range(int(math.pow(2, dim))):

            tempCodeWord = [0] * dim

            # pretvaranje decimalne vrijednosti u binarnu
            binPart = bin(i).split("b")[1]
            # dodavanje prefiksnih nula do dimenzije dim
            while binPart.__len__() != dim:
                binPart = '0' + binPart

            for j in range(binPart.__len__()):
                tempCodeWord[j] = int(binPart[j])

            codeWords.append(tempCodeWord)

        # kodne rijeci se dobiju mnozenjem vec dobivenih binarnih brojeva
        # s generirajucom matricom
        for i in range(codeWords.__len__()):
            codeWords[i] = self.multiplyMod2(codeWords[i])

        return codeWords

    def normalize(self):
        """ Funkcija za svodjenje generirajuce matrica u strandardnu formu
        :return:
        """

        numOfRows = self.genMat.__len__()

        for column in range(numOfRows):

            for row in range(numOfRows):

                # ako smo na dijagonali gdje bi elementi trebali biti 1
                if row == column:

                    if self.genMat[row][column] != 1:

                        # probamo pronaci postoji li gotov stupac koji ima jedinicu
                        # na pravom mjestu a na ostalim mjestima nule
                        index = self.containsColumn(column)
                        if index != -1:
                            self.swapColumns(index, column)
                            break

                        index = self.findPattern(column)
                        if index != -1:
                            patternRow = index
                            self.xor(row, patternRow, row)
                            continue

                else:  # sve ostalo kad nismo na dijagonali

                    if self.genMat[row][column] == 0:
                        continue
                    else:

                        index = self.containsColumn(column)
                        if index != -1:
                            self.swapColumns(index, column)
                            break

                        index = self.findPattern(column)
                        if index != -1:
                            patternRow = index
                            self.xor(row, patternRow, row)
                            continue

        self.genMatPrint()

    def genMatPrint(self):
        """ Funkcija za ispis generirajuce matrice
        :return:
        """

        self.console.insert(tk.END, "ispis generirajuce matrice\n")
        self.console.see(tk.END)

        for row in self.genMat:
            self.console.insert(tk.END, str(row) + "\n")
            self.console.see(tk.END)

    def showNK(self):
        """ Funkcija za ispis n i k parametra blok koda
        :return:
        """

        self.console.insert(tk.END, "n generirajce matrice iznosi: " + str(self.n) + "\n")
        self.console.see(tk.END)
        self.console.insert(tk.END, "k generirajuce matrice iznosi: " + str(self.k) + "\n")
        self.console.see(tk.END)

    def linear(self):
        """ Fnkcija za provjeru je li blok kod linearan

        :return:
        """

        # generiraju se kodne rijeci pomocu trenutne generirajuce matrice
        self.codeWords = self.generateCodeWords(self.k)

        for i in range(self.rows):
            for j in range(self.rows):

                # iste kodne rijeci se preskacu
                if i == j:
                    continue

                # kodna rijec dobivena mnozenjem dvije kodne rijeci
                temp = [0] * self.columns
                for k in range(self.columns):
                    temp[k] = self.genMat[i][k] ^ self.genMat[j][k]

                # ako generirane kodne rijeci ne sadrze umnozak neke dvije kodne rijeci, kod nije linearan
                if not self.codeWords.__contains__(temp):
                    self.console.insert(tk.END, "kod nije linearan\n")
                    self.console.see(tk.END)
                    return

        self.console.insert(tk.END, "kod je linearan\n")
        self.console.see(tk.END)

    def codingSpeed(self):
        """ Funkcija za izracun i ispis kodne brzine
        :return:
        """

        cs = self.k / self.n

        self.console.insert(tk.END, "kodna brzina zastitnog koda je: " + str(cs) + "\n")
        self.console.see(tk.END)

    def setExample(self, num):
        """ Funkcija za postavljanje generirajuce matrice i ostalih parametara
        nakon klika na neki od gumba "Primjer"
        :param num: redni broj primjera
        :return:
        """

        if num == 1:
            self.genMat = [[0, 0, 1, 1, 1],
                           [1, 1, 0, 1, 1]]

        elif num == 2:
            self.genMat = [[1, 0, 1, 1, 0],
                           [1, 1, 0, 1, 0],
                           [0, 1, 0, 0, 1]]
        else:
            self.genMat = [[1, 0, 0, 1, 1, 1, 0],
                           [0, 1, 0, 1, 1, 0, 1],
                           [0, 0, 0, 1, 0, 1, 1],
                           [0, 0, 1, 1, 1, 0, 0]]

        self.rows = self.genMat.__len__()
        self.columns = self.genMat[0].__len__()

        self.makeEntries()

        values = []
        for row in self.genMat:
            for value in row:
                values.append(value)

        for e in range(self.entries.__len__()):
            text = values[e]
            self.entries[e].insert(0, text)

        self.frames[GenMatPage].buttonCodingSpeed['state'] = 'normal'
        self.frames[GenMatPage].buttonNormalize['state'] = 'normal'
        self.frames[GenMatPage].buttonLin['state'] = 'normal'
        self.frames[GenMatPage].buttonNK['state'] = 'normal'
        self.frames[GenMatPage].buttonCode['state'] = 'normal'

        self.frames[GenMatPage].entryRows.delete(0, tk.END)
        self.frames[GenMatPage].entryRows.insert(0, self.rows)
        self.frames[GenMatPage].entryColumns.delete(0, tk.END)
        self.frames[GenMatPage].entryColumns.insert(0, self.columns)

        # vektorski prostor
        self.n = self.genMat[0].__len__()
        # dimenzija koda
        self.k = self.genMat.__len__()

    def code(self):
        """ Funkcija za kodiranje unesene zeljene rijeci
        :return:
        """

        # unesena rijec koju treba kodirati
        inputString = self.frames[CodingPage].codeEntry.get()

        if inputString == "":
            self.console.insert(tk.END, "[WARNING] upisite nesto u polje za unos\n")
            self.console.see(tk.END)
        else:
            for i in range(inputString.__len__()):
                if inputString[i] != '1' and inputString[i] != '0':
                    self.console.insert(tk.END, "[ERROR] moguce je kodirati nizove koji se sastoje od simbola iz skupa: "  + str(self.alphabet) + "\n")
                    self.console.see(tk.END)
                    break

            inputCode = []
            for i in range(inputString.__len__()):
                inputCode.append(int(inputString[i]))

            # unesena rijec mora biti visekratnik retka generirajuce matrice, odnosno broja k
            if inputCode.__len__() % self.k != 0:
                self.console.insert(tk.END, "[ERROR] duljina rijeci za kodirati nije visekratnik broja " + str(self.k) + "\n")
                self.console.see(tk.END)
            else:
                coddedMessage = []
                for i in range(0, inputString.__len__(), self.k):
                    sub = []
                    for j in range(self.k):
                        sub.append(int(inputString[i + j]))
                    codedWord = self.multiplyMod2(sub)
                    coddedMessage.extend(codedWord)

                coddedMessageString = ""
                for i in coddedMessage:
                    coddedMessageString = coddedMessageString + str(i)

                self.console.insert(tk.END, "kodirana poruka: " + inputString + " je " + coddedMessageString + "\n")
                self.console.see(tk.END)


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        frame = tk.Frame(self)
        frame.place(in_=self, anchor="c", relx=.5, rely=.5)

        welcomeText = "Ovo je aplikacija za izracun standardnog\noblika generirajuce matrice i\nkodiranje proizvoljno unesene rijeci."
        label = tk.Label(frame, text=welcomeText)
        label.pack(padx=20, pady=20)

        buttonGenMat = tk.Button(frame, text="Unos generirajuce matrice", command=lambda: controller.show_frame(GenMatPage))
        buttonGenMat.pack(padx=10, pady=10)

        buttonSteps = tk.Button(frame, text="Upute za koristenje", command=lambda: controller.show_frame(InstructionsPage))
        buttonSteps.pack(padx=10, pady=10)


class InstructionsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        labelDescription = tk.Label(self, text="Ovdje se nalaze upute za koristenje aplikacije")
        labelDescription.pack(padx=10, pady=10)

        labelInstructions = tk.Label(self, text="Za stvaranje generirajuce matrice prvo je potrebno\n "
                                                "upisati broj redaka i stupaca same matrice i zatim pritisnuti na gumb \"unos\".\n\n"
                                                "Nakon toga se stvaraju polja za unos elemenata matrice.\n\n"
                                                "Za spremanje upisanih vrijednosti potrebno je pritisnuti gumb \"generiraj matricu\"\n "
                                                "nakon cega se stvara generirajuca matrica i omogucavaju ostali gumbi.\n\n"
                                                "Vec gotove primjere generirajucih matrica moguce je vidjeti pritiskom na neki gumb \"Primjer\".\n\n"
                                                "Za svođenje generirajuće matrice na standarnu formu, prvo je potrebno učitati primjer ili\n "
                                                "zadati neku proizvoljnu i zatim pritisnuti na gumb \"normaliziraj\" nakon čega se \n"
                                                "normalizirana matrica ispisuje u donjem dijelu prozora.\n\n"
                                                "Za kodiranje određene riječi potrebno je prvo stvoriti generirajuću matricu,\n"
                                                "zatim je normalizirati i nakon toga pritisnuti na gumb \"kodiraj\". Otvara se nova\n"
                                                "stranica s poljem za unos željene riječi koju treba kodirati. Nakon unosa riječi pritisnuti\n"
                                                "gumb \"kodiraj\" nakon čega se kodirana riječ pojavljuje u donjem dijelu prozora."
                                                )
        labelInstructions.pack(padx=10, pady=10)

        buttonBack = tk.Button(self, text="Nazad", command=lambda: controller.show_frame(StartPage))
        buttonBack.pack(padx=10, pady=10)


class GenMatPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # opis framea
        descriptionLabel = tk.Label(self, text="Unesite broj redaka i stupaca generirajuce matrice.")
        descriptionLabel.pack(padx=10, pady=20)

        # frame s unosom redaka i stupaca
        inputFrame = tk.Frame(self)
        inputFrame.pack()

        labelRows = tk.Label(inputFrame, text="Broj redaka: ")
        labelRows.pack(side="left", padx=10, pady=10)

        self.entryRows = tk.Entry(inputFrame)
        self.entryRows.pack(side="left", padx=5, pady=10)

        labelColumns = tk.Label(inputFrame, text="Broj stupaca: ")
        labelColumns.pack(side="left", padx=10, pady=10)

        self.entryColumns = tk.Entry(inputFrame)
        self.entryColumns.pack(side="left", padx=5, pady=10)

        # gumbi ----------------------------------------
        buttonFrame = tk.Frame(self)
        buttonFrame.pack()

        buttonInput = tk.Button(buttonFrame, text="unos", command=lambda: [controller.saveRowsAndColumns(),
                                                                           controller.makeEntries()])
        buttonInput.pack(side="left", padx=10, pady=10)

        buttonGenMat = tk.Button(buttonFrame, text="generiraj matricu",
                                 command=lambda: [controller.getGenMat(), controller.isGenMatStandardized()])
        buttonGenMat.pack(side="left", padx=10, pady=10)

        self.buttonNK = tk.Button(buttonFrame, text="n i k zadanog koda", state="disabled",
                                  command=lambda: controller.showNK())
        self.buttonNK.pack(side="left", padx=10, pady=10)

        self.buttonLin = tk.Button(buttonFrame, text="je li linearan?", state="disabled",
                                   command=lambda: controller.linear())
        self.buttonLin.pack(side="left", padx=10, pady=10)

        self.buttonNormalize = tk.Button(buttonFrame, text="normaliziraj", state="disabled",
                                         command=lambda: [controller.normalize(), controller.isGenMatStandardized()])
        self.buttonNormalize.pack(side="left", padx=10, pady=10)

        self.buttonCodingSpeed = tk.Button(buttonFrame, text="kodna brzina", state="disabled",
                                           command=lambda: controller.codingSpeed())
        self.buttonCodingSpeed.pack(side="left", padx=10, pady=10)

        self.buttonCode = tk.Button(buttonFrame, text="Kodiranje", state="disabled",
                                    command=lambda: controller.show_frame(CodingPage))
        self.buttonCode.pack(side="left", padx=10, pady=10)

        # frame s generiranim poljima za unos
        self.entryFrame = tk.Frame(self)
        self.entryFrame.pack(padx=10, pady=10)

        # farme s gumbima za gotov primjer generirajuce matrice
        examplesFrame = tk.Frame(self)
        examplesFrame.pack(padx=10, pady=10)

        button1 = tk.Button(examplesFrame, text="Primjer 1", command=lambda: controller.setExample(1))
        button1.pack(side="left", padx=10, pady=10)

        button2 = tk.Button(examplesFrame, text="Primjer 2", command=lambda: controller.setExample(2))
        button2.pack(side="left", padx=10, pady=10)

        button3 = tk.Button(examplesFrame, text="Primjer 3", command=lambda: controller.setExample(3))
        button3.pack(side="left", padx=10, pady=10)

        buttonBack = tk.Button(self, text="Nazad", command=lambda: controller.show_frame(StartPage))
        buttonBack.pack(padx=10, pady=10)


class CodingPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        descriptionLabel = tk.Label(self, text="Na ovoj stranici je moguce vidjeti izgled kodirane\n rijeci unesene u polje ispod.")
        descriptionLabel.pack(padx=10, pady=10)

        self.codeEntry = tk.Entry(self)
        self.codeEntry.pack(padx=10, pady=10)

        buttonCode = tk.Button(self, text="Kodiraj", command=lambda: controller.code())
        buttonCode.pack(padx=10, pady=10)

        buttonBack = tk.Button(self, text="Nazad", command=lambda: controller.show_frame(GenMatPage))
        buttonBack.pack(padx=10, pady=10)


if __name__ == "__main__":

    App = BinaryBlockCode()
    App.title("Zadatak 2 - grupa P02_6")
    # App.geometry("800x600")
    App.mainloop()