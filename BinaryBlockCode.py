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

        for F in (StartPage, GenMatPage):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        """funkcija za prikaz odredjenog frame-a"""

        frame = self.frames[cont]
        frame.tkraise()

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

        buttonGenMat = tk.Button(self, text="Generiraj matricu")
        buttonGenMat.pack(padx=10, pady=10)







if __name__ == "__main__":

    App = BinaryBlockCode()
    App.title("Zadatak 2 - grupa P02_6")
    App.geometry("800x600")
    App.mainloop()