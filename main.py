# -*- coding: utf-8 -*-
import csv
import random
import matplotlib.pyplot
from item import Item

GEN_MAXIMO = 200000
POPULACAO_INICIAL_QUANT = 100
CAPACIDADE_MOCHILA = 22
MEDIA_QUALIDADE_NUMBER = 5

def gerarGrafico(mediaGeracoes):
	geracoes = []
	valores = []
	for i in range(len(mediaGeracoes)):
		valores.append(mediaGeracoes[i])
		geracoes.append(i+1)
	matplotlib.pyplot.title('Media do fitness das geracoes durante o algoritmo genetico')
	matplotlib.pyplot.xlabel('Geracoes')
	matplotlib.pyplot.ylabel('Fitness')
	matplotlib.pyplot.plot(geracoes, valores)
	matplotlib.pyplot.show()

def gerarItens():
	arquivo = open('itens.csv')
	linhas = csv.reader(arquivo)
	return [Item(int(linha[0]), int(linha[1])) for linha in linhas]

def gerarPopulacaoInicial(itens):
	print(' -- Gerando populacao inicial -- ')
	return [gerarIndividuo(itens) for x in range (0,POPULACAO_INICIAL_QUANT)]

def gerarIndividuo(itens):
	return [random.randint(0,1) for x in range (0,len(itens))]

def fitness(individuo, itens):
	totalValor = 0
	totalPeso = 0
	index = 0
	penalidade = 0
	for i in individuo:
		if index >= len(itens):
			break
		if (i == 1):
			totalValor += itens[index].valor # Somar todos os valores dentro do individuo
			totalPeso += itens[index].peso # Somar todos os pesos dentro do individuo
		index += 1
	if totalPeso > CAPACIDADE_MOCHILA: # Verificar se peso excede a capacidade da mochila
		return 0
	else:
		return totalValor # Retornar soma dos valores quando peso não exceder
	
def pegarValorIndividuo(individuo, itens): # Função para retornar valor de um individuo
	index = 0
	totalValor = 0
	for i in individuo:
		if index >= len(itens):
			break
		if (i == 1):
			totalValor += itens[index].valor
		index += 1
	return totalValor

def pegarPesoIndividuo(individuo, itens): # Função para retornar peso de um individuo
	index = 0
	totalPeso = 0
	for i in individuo:
		if index >= len(itens):
			break
		if (i == 1):
			totalPeso += itens[index].peso
		index += 1
	return totalPeso

def roulleteWheel(populacao, itens):
	max = sum(fitness(ind, itens) for ind in populacao) # Realizar a soma dos fitness de uma populacao
	pick = random.uniform(0, max) # randomizar um numero em cima da soma
	current = 0
	for ind in populacao:
		current += fitness(ind, itens)
		if current > pick: # Se valor alcançado for maior que o escolhido de forma relatória
				return ind # Retornar individuo

def gerarCortes(individuo):
	cortes = []
	corte1 = random.randint(0,len(individuo)-1) # Randomizar onde será realizado o corte para geração de filhos
	while (corte1 == len(individuo)-1):
		corte1 = random.randint(0,len(individuo)-1)
	corte2 = random.randint(0,len(individuo)-1)
	while(corte2 <= corte1):
		corte2 = random.randint(0,len(individuo)-1)
	cortes.append(corte1)
	cortes.append(corte2)
	return cortes

def selecao(populacao, itens):
	# mutation_chance = 0.08
	filhos = []
	for x in range(0,POPULACAO_INICIAL_QUANT/2):
		individuo1 = roulleteWheel(populacao, itens) # Utilizar algoritmo do RoulleteWheel para selecionar individuo
		individuo2 = roulleteWheel(populacao, itens) # Utilizar algoritmo do RoulleteWheel para selecionar o segundo individuo
		while individuo1 == individuo2: # Enquanto individuo 1 for igual ao individuo 2 continuar realizando algoritmo do RoulleteWheel
			individuo2 = roulleteWheel(populacao, itens)
		cortes = gerarCortes(individuo1) # Gerar os dois cortes para o cruzamento em dois pontos
		filho = individuo1[:cortes[0]] + individuo2[cortes[0]:cortes[1]] + individuo1[cortes[1]:] # Criação do primeiro filho
		filhos.append(filho)
		filho2 = individuo2[:cortes[0]] + individuo1[cortes[0]:cortes[1]] + individuo2[cortes[1]:] # Criação do segundo filho
		filhos.append(filho2)
	filhoParaMutacao = random.randint(0,POPULACAO_INICIAL_QUANT-1); # Selecionar indice do filho para mutacao de forma aleatoria
	filhos[filhoParaMutacao] = mutacao(filhos[filhoParaMutacao]) # Realizar mutacao
	eleito = eletismo(populacao, itens) # Selecionar o melhor individuo da geração passada
	filhos.append(eleito) # Adicionar individuo selecionado para nova geração
	return filhos # Retornar nova geração

def mutacao(individuo):
	r = random.randint(0,len(individuo)-1) # Randomizar a posição em que vai haver a alteração no individuo
	if individuo[r] == 1:
			individuo[r] = 0
	else:
			individuo[r] = 1
	return individuo
	

def eletismo(populacao, itens):
	eleito = None
	valorEleito = 0
	for ind in populacao:
		if fitness(ind, itens) > valorEleito: # Verificar sempre o individuo com melhor fitness para poder retornar
			eleito = ind
			valorEleito = fitness(ind, itens)
	return eleito

def calcularMedPop(populacao, itens): # Calcular média de FITNESS em uma geração
	total = 0
	quantidade = 0
	for ind in populacao:
		total += fitness(ind, itens)
		quantidade += 1
	return total/quantidade

def verificarPadronizacao(mediaGeracoes): # Verificar padronização da média para poder para o algoritmo
	# for med in expression_list:
		# pass
	if (len(mediaGeracoes) >= MEDIA_QUALIDADE_NUMBER):
		mediaGeracoes = mediaGeracoes[-MEDIA_QUALIDADE_NUMBER:]
		if mediaGeracoes[1:] == mediaGeracoes[:-1]:
			return True
	return False

def retornarMelhorDaPopulacao(populacao, itens):
	melhor = eletismo(populacao, itens)
	print("\n ---- O MELHOR RESULTADO ENCONTRADO -----")
	print("\n ESTRUTURA = %s" % (str(melhor)))
	print("\n VALOR = %s" % (pegarValorIndividuo(melhor,itens)))
	print("\n PESO = %s" % (pegarPesoIndividuo(melhor,itens)))
	print("\n FITNESS = %s" % (fitness(melhor,itens)))

def main():
	geracao = 0
	itens = gerarItens() # Gerar itens de acordo com o CSV
	populacao = gerarPopulacaoInicial(itens) # Gerar a populacao inicial
	mediaGeracoes = [] # Lista para armazenar a media de fitness das gerações
	for g in range(0, GEN_MAXIMO):
		populacao = sorted(populacao, key=lambda x: fitness(x, itens), reverse=True) # Ordenar de forma reversa pelo fitness dos individuos
		if verificarPadronizacao(mediaGeracoes):
			retornarMelhorDaPopulacao(populacao,itens)
			gerarGrafico(mediaGeracoes)
			break
		geracao += 1
		print(" --- Geracao %s ---" % str(geracao))
		populacao = selecao(populacao, itens)
		# for ind in populacao:
		# 	print("%s, VALOR: [ %s ] PESO: [ %s ] FITNESS: [ %s ]" % (
		# 		str(ind),
		# 		pegarValorIndividuo(ind, itens),
		# 		pegarPesoIndividuo(ind, itens),
		# 		fitness(ind, itens))
		# 	)
		mediaGeracoes.append(calcularMedPop(populacao, itens)) # Adicionar media da população na lista
		print("MEDIA POPULACAO: [ %s ]" % (calcularMedPop(populacao, itens)))

if __name__ == "__main__":
  main()