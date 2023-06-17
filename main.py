import tkinter as tk
from extract import Extracao

def submit():

    name = arquivoInput.get()
    data = dataInput.get().split("/")
    dia = int(data[0])
    mes = int(data[1])
    ano = int(data[2])
    etx = Extracao(name, ano, mes, dia)
    etx.executar_extracao()


janela = tk.Tk(screenName=None, baseName=None, className='Python APP', useTk=True)
janela.geometry("450x400")

arquivoLabel = tk.Label(janela, text = 'Nome do Arquivo', anchor="e", width=15)
arquivoLabel.grid(row= 0, column = 0, padx = 5, pady =5)

dataLabel = tk.Label(janela, text = 'Até a Data', width=15, anchor="e")
dataLabel.grid(row= 1, column = 0, padx = 5, pady =5)

arquivoInput = tk.Entry(janela, width= 30, cursor="hand2")
arquivoInput.grid(row= 0, column = 1, padx = 5, pady =5)

dataInput = tk.Entry(janela, width= 30, cursor="hand2")
dataInput.grid(row= 1, column = 1, padx = 5, pady =5)

enterButton = tk.Button(janela, text = 'PRINT', command=submit)
enterButton.grid(row= 2, column = 1, padx = 5, pady =5)


janela.mainloop()