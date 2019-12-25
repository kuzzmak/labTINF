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

        self.console = tk.Text(consoleFrame, height=5, width=30)
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


        for F in (StartPage, InstructionsPage, GenMatPage):

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
                self.console.insert(tk.END, "[INFO] broj redaka: " + str(self.rows) + "\n")
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
                self.console.insert(tk.END, "[INFO] broj stupaca: " + str(self.columns) + "\n")
                self.console.see(tk.END)
            except ValueError:
                self.console.insert(tk.END, "[ERROR] broj stupaca mora biti pozitivan broj\n")
                self.console.see(tk.END)

        else:
            self.console.insert(tk.END, "[WARNING] unesite ispravan broj stupaca\n")
            self.console.see(tk.END)

    def makeEntries(self):

        self.frames[GenMatPage].buttonCodingSpeed['state'] = 'disabled'
        self.frames[GenMatPage].buttonNormalize['state'] = 'disabled'
        self.frames[GenMatPage].buttonLin['state'] = 'disabled'
        self.frames[GenMatPage].buttonNK['state'] = 'disabled'

        for widget in self.frames[GenMatPage].entryFrame.winfo_children():
            widget.destroy()

        self.entries = []

        for i in range(self.rows):

            entryRow = tk.Frame(self.frames[GenMatPage].entryFrame)
            entryRow.pack()

            for j in range(self.columns):
                entry = tk.Entry(entryRow)
                entry.pack(side="left", padx=10, pady=10)
                self.entries.append(entry)

    def getGenMat(self):

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

            self.frames[GenMatPage].buttonCodingSpeed['state'] = 'normal'
            self.frames[GenMatPage].buttonNormalize['state'] = 'normal'
            self.frames[GenMatPage].buttonLin['state'] = 'normal'
            self.frames[GenMatPage].buttonNK['state'] = 'normal'

        except ValueError:
            self.console.insert(tk.END, "[ERROR] sve vrijednosti moraju biti iz skupa [0, 1]\n")
            self.console.see(tk.END)

    def xor(self, row, patternRow, destinationIndex):

        v1 = self.genMat[row]
        v2 = self.genMat[patternRow]

        v3 = [0] * v1.__len__()

        for i in range(v3.__len__()):
            v3[i] = v1[i] ^ v2[i]

        self.genMat[destinationIndex] = v3

    def isGenMatStandardized(self):
        #FIXME
        flag = True

        for i in range(self.k):

            if self.genMat[i][i] == 0:
                print("generirajuca matrica nije standardizirana")
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
            print("generirajuca matrica je standardizirana")

    def swapRows(self, r1, r2):

        temp = self.genMat[r1]
        self.genMat[r1] = self.genMat[r2]
        self.genMat[r2] = temp

    def swapColumns(self, c1, c2):

        numOfRows = self.genMat.__len__()

        for row in range(numOfRows):
            temp = self.genMat[row][c1]
            self.genMat[row][c1] = self.genMat[row][c2]
            self.genMat[row][c2] = temp

    def getColumn(self, index):

        numOfRows = self.genMat.__len__()

        result = [0] * numOfRows

        for row in range(numOfRows):
            result[row] = self.genMat[row][index]

        return result

    def containsColumn(self, index):

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

        numOfRows = self.genMat.__len__()
        numOfColumns = self.genMat[0].__len__()

        result = [0] * numOfColumns

        for c in range(numOfColumns):

            column = self.getColumn(c)

            for i in range(numOfRows):
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

        return codeWords

    def normalize(self):

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

        self.console.insert(tk.END, "[INFO] ispis generirajuce matrice\n")
        self.console.see(tk.END)

        for row in self.genMat:
            self.console.insert(tk.END, str(row) + "\n")
            self.console.see(tk.END)

    def showNK(self):
        pass #TODO

    def linear(self):
        pass  #TODO

    def codingSpeed(self):
        pass #TODO


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

        labelInstructions = tk.Label(self, text="")
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

        buttonGenMat = tk.Button(buttonFrame, text="generiraj matricu", command=controller.getGenMat)
        buttonGenMat.pack(side="left", padx=10, pady=10)

        self.buttonNK = tk.Button(buttonFrame, text="n i k zadanog koda", state="disabled", command=lambda: controller.showNK())
        self.buttonNK.pack(side="left", padx=10, pady=10)

        self.buttonLin = tk.Button(buttonFrame, text="je li linearan?", state="disabled", command=lambda: controller.linear())
        self.buttonLin.pack(side="left", padx=10, pady=10)

        self.buttonNormalize = tk.Button(buttonFrame, text="normaliziraj", state="disabled", command=lambda: controller.normalize())
        self.buttonNormalize.pack(side="left", padx=10, pady=10)

        self.buttonCodingSpeed = tk.Button(buttonFrame, text="kodna brzina", state="disabled", command=lambda: controller.codingSpeed())
        self.buttonCodingSpeed.pack(side="left", padx=10, pady=10)

        # frame s generiranim poljima za unos
        self.entryFrame = tk.Frame(self)
        self.entryFrame.pack(padx=10, pady=10)


if __name__ == "__main__":

    App = BinaryBlockCode()
    App.title("Zadatak 2 - grupa P02_6")
    App.geometry("800x600")
    App.mainloop()