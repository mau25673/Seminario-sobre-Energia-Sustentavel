import math
import numpy as np
#classes
class Termeletrica:
    def __init__(self, potencia, identificacao, combustivel, producaoco2, tipo, custodeoperacao):
        self.identificacao=identificacao
        self.potencia=potencia
        self.combustivel=combustivel
        self.producaoco2=producaoco2
        self.tipo=tipo
        self.custodeoperacao=custodeoperacao
    def __str__(self):
        return f'Identificação: {self.identificacao} | Eletricidade gerada: {self.potencia} MWh | Produção de CO2: {self.producaoco2} Toneladas | Tipo: {self.tipo} | Custo de operação: US${self.custodeoperacao}/h'

class Eolica:
    def __init__(self, identificacaoEolica, potenciaEolica, custo, numeroTorres, tipoEolica, eficienciaEolica, matrizEolica):
        self.identificacaoEolica=identificacaoEolica
        self.potenciaEolica=potenciaEolica 
        self.custo=custo
        self.numeroTorres=numeroTorres
        self.tipoEolica=tipoEolica
        self.eficienciaEolica=eficienciaEolica
        self.matrizEolica=matrizEolica
    def __str__(self):
        return f'Identificação: {self.identificacaoEolica} | Eletricidade gerada: {self.potenciaEolica} MWh | Custo: R$ {"%.2f" % self.custo} | Torres: {self.numeroTorres} | Tipo: {self.tipoEolica}\nMapa: \n{self.matrizEolica}\nCada 1 simboliza uma torre, produzindo 6 MWh.'
#listas
lista_usinas = []
lista_eolicas = []
#menu principal
def menu_principal():
    print('Seja bem vindo(a) ao calculador de transferência entre termelétricas e parques eólicos!\n')
    try:
        while True:
            escolha=int(input('Escolha a opção que deseja a seguir:\n1. Registrar termelétrica\n2. Listar termelétricas\n3. Converter termelétrica para parque eólico\n4. Listar parques eólicos\n5. Comparar termelétrica com eólica\n6. Sair\n'))
            if escolha == 1:
                registrar_usina()
            elif escolha == 2:
                listar_termeletricas()
            elif escolha == 3:
                conversor()
            elif escolha == 4:
                listar_eolicas()
            elif escolha == 5:
                comparador()
            elif escolha == 6:
                print("Saindo...")
                break
            else:
                print('Opção inválida.')
    except ValueError:
        print('Valor inválido, digite um número listado nas opções.')
        menu_principal()
#registro
def registrar_usina():
    try:
        identificacao = input("Insira o nome da usina termelétrica: ")
        for usina in lista_usinas:
            if identificacao == usina.identificacao:
                print('Nome em uso, tente novamente.')
                registrar_usina()
        identificacao = identificacao.lower()
        tipo = int(input("Insira o tipo de usina termelétrica, baseado na lista abaixo:\n1. Carvão\n2. Gás natural\n3. Diesel\n"))
        if tipo < 1 or tipo > 3:
            print('Valor inválido, digite um número que está na lista.')
            tipo = int(input("Insira o tipo de usina termelétrica, baseado na lista abaixo:\n1. Carvão\n2. Gás natural\n3. Diesel\n"))
        combustivel = float(input("Insira a quantidade de combustível consumido em toneladas (ou metros cúbicos caso seja um gás) ao longo de uma hora de operação: "))
        eficiencia = float(input("Insira a eficiência da usina termelétrica em decimal (0.4 para 40%, 1 para 100%, etc): "))
        #calculo de potencia e produção de gas carbonico
        if tipo == 1:
            producaoco2 = combustivel * 1.892
            potencia = (((combustivel * 1000)*24)/3600) * eficiencia
            custodeoperacao = 102.70 * combustivel
        elif tipo == 2:
            producaoco2 = combustivel * 0.001932
            potencia = (combustivel * 0.01) * eficiencia
            custodeoperacao = 0.12 * combustivel
        elif tipo == 3:
            producaoco2 = combustivel * 3.130
            potencia = (((combustivel * 1000)*42.5)/3600) * eficiencia 
            custodeoperacao = 1967 * combustivel
        #adicionando na lista
        usina = Termeletrica(potencia, identificacao, combustivel, producaoco2, tipo,custodeoperacao)
        print(f'Usina registrada com sucesso!:\n{usina}')
        lista_usinas.append(usina)
    except ValueError:
        print("Valor inválido, digite um número listado.")
        registrar_usina()
#lista as termeletricas registradas
def listar_termeletricas():
    print("Listando termelétricas registradas:")
    for usina in lista_usinas:
        print(usina)
#lista as eolicas registradas
def listar_eolicas():
    print("Listando eólicas registradas:")
    for eolica in lista_eolicas:
        print(eolica)
#cria o mapa pro parque eolico
def mapa(numeroTorres):
    linhas = math.sqrt(numeroTorres)
    linhas=int(linhas)
    colunas = linhas
    if linhas * colunas < numeroTorres:
        colunas+=1
    contadorTorres=numeroTorres
    matrizEolica=np.zeros((linhas, colunas), dtype=int)
    for i in range(linhas):
        for j in range(colunas):
            if matrizEolica[i,j] == 0 and contadorTorres > 0:
                matrizEolica[i,j] = 1
                contadorTorres-=1
    return matrizEolica
#converte uma termeletrica pra uma eolica
def conversor():
    i = 0
    print('Conversor de termoelétrica para parque eólico: \n')
    listar_termeletricas()
    try:
        usinaescolhida=str(input("Qual usina deseja converter?: "))
        usinaescolhida = usinaescolhida.lower()
        for i in range (len(lista_usinas)):
            if lista_usinas[i].identificacao == usinaescolhida:
                identificacaoEolica = str(input('Digite a identificação do parque eólico a ser criado: '))
                potenciaEolica = lista_usinas[i].potencia
                tipoEolica = int(input('Escolha a opção que desejar:\n1. Onshore\n2. Offshore\n'))
                if tipoEolica == 1:
                    custo = potenciaEolica * 7000000
                elif tipoEolica == 2:
                    custo = potenciaEolica * 14300000
                numeroTorres = math.ceil(potenciaEolica / 6)
                eficienciaEolica=0.45
                matrizEolica=mapa(numeroTorres)
                eolica = Eolica(identificacaoEolica, potenciaEolica, custo, numeroTorres, tipoEolica, eficienciaEolica, matrizEolica)
                lista_eolicas.append(eolica)
                break
            else:
                print('Usina não encontrada.')
    except ValueError:
        print('Valor inválido.')
#compara uma usina termeletrica com um parque eolico
def comparador():
    listar_termeletricas()
    escolhatermeletrica=str(input("Escolha uma das termelétricas para comparar os dados (Por identificação): "))
    listar_eolicas()
    try:
        escolhaeolica=str(input("Escolha um dos parques eólicos para comparar os dados (Por identificação): "))
        for usina in lista_usinas:
            if usina.identificacao == escolhatermeletrica:
                print(usina)
                custoUmAno=(usina.custodeoperacao*24)*365
                co2Salvo=(usina.producaoco2*24)*365
                break
        for eolica in lista_eolicas:
            if eolica.identificacaoEolica == escolhaeolica:
                print(eolica)
                break
        else:
            print('Opção inválida. Tente novamente.')
            comparador()
        print(f"Ao trocar para uma eólica, serão salvos US${"%.2f" % custoUmAno} por ano em combustível, não contando manutenção ou pessoal.\nSerão {co2Salvo} toneladas de CO2 a menos soltas na atmosfera ao longo de um ano.")
    except ValueError:
        print('Opção inválida. Tente novamente.')
        comparador()

#roda o código inteiro
menu_principal()