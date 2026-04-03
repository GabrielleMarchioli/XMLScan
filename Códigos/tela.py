import tkinter as tk
from tkinter import filedialog
from xml_treatment import *

def test(path):
    # rodar em loop de acordo com o numero de notas
    cont = 0
    for i in path:
        caminho_nota = i #f'{caminho.split('Códigos')[0]}\\Notas\\Notas Novas\\{i}'
        # inicia a classe e pega os valores presentes na nota
        resultado = Xml_Treatment(caminho_nota)
        valores_notas = resultado.return_elements_taxes
        estado = resultado.state
        # chama a classe de calcular o tributo
        cal_trib = CalTributos(estado, valores_notas['BASE_CALC'])
        print(f'Valores da nota {cont + 1} do estado de {estado}: \n{valores_notas}\n\nValor dos impostos\n{cal_trib.calcular_json()}\n')
        cont +=1

def selecionar_arquivo():
    caminho = filedialog.askopenfilenames(
        title="Selecione um arquivo",
        filetypes=[("Arquivos XML", "*.xml"), ("Todos os arquivos", "*.*")]
    )
    
    if caminho:
        print('_'*50)
        test(caminho)
        print('_'*50)
    

def tela():
    janela = tk.Tk()
    janela.title("Tela NFE Test")
    janela.geometry("300x200")

    # Criando um rótulo (label)
    label_resultado = tk.Label(janela, text="Gerar Report")
    label_resultado.pack(pady=20)

    # Criando o botão
    botao = tk.Button(janela, text="Analisar Impostos", command=selecionar_arquivo)
    botao.pack(pady=10)

    # Iniciando a interface
    janela.mainloop()

if __name__ == '__main__':
    tela()