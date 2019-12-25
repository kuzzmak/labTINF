import tkinter as tk


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

        self.entries = []

        self.genMat = []

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
            except ValueError:
                self.console.insert(tk.END, "[ERROR] broj stupaca mora biti pozitivan broj\n")
                self.console.see(tk.END)

        else:
            self.console.insert(tk.END, "[WARNING] unesite ispravan broj stupaca\n")
            self.console.see(tk.END)

    def makeEntries(self):

        for widget in self.frames[GenMatPage].entryFrame.winfo_children():
            widget.destroy()

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

        except ValueError:
            self.console.insert(tk.END, "[ERROR] sve vrijednosti moraju biti iz skupa [0, 1]\n")
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

        buttonFrame = tk.Frame(self)
        buttonFrame.pack()

        buttonGenMat = tk.Button(buttonFrame, text="Generiraj matricu", command=lambda: [controller.saveRowsAndColumns(),
                                                                                  controller.makeEntries()])
        buttonGenMat.pack(side="left", padx=10, pady=10)

        buttonPrintGenMat = tk.Button(buttonFrame, text="Napravi matricu", command=controller.getGenMat)
        buttonPrintGenMat.pack(side="right", padx=10, pady=10)

        self.entryFrame = tk.Frame(self)
        self.entryFrame.pack(padx=10, pady=10)





if __name__ == "__main__":

    App = BinaryBlockCode()
    App.title("Zadatak 2 - grupa P02_6")
    App.geometry("800x600")
    App.mainloop()