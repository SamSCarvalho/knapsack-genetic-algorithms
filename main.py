import csv
import random
from item import Item

GEN_MAXIMO = 20000
POPULACAO_INICIAL_QUANT = 10
CAPACIDADE_MOCHILA = 22

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
			totalValor += itens[index].valor
			totalPeso += itens[index].peso
		index += 1
	if totalPeso > CAPACIDADE_MOCHILA:
		return totalValor - (totalPeso - CAPACIDADE_MOCHILA)
	else:
		return totalValor # ESTA OKAY
	
def pegarValorIndividuo(individuo, itens):
	index = 0
	totalValor = 0
	for i in individuo:
		if index >= len(itens):
			break
		if (i == 1):
			totalValor += itens[index].valor
		index += 1
	return totalValor

def pegarPesoIndividuo(individuo, itens):
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
	max = sum(fitness(ind, itens) for ind in populacao)
	pick = random.uniform(0, max)
	current = 0
	for ind in populacao:
			current += fitness(ind, itens)
			if current > pick:
					return ind

def returnMatches(a,b):
       return list(set(a) & set(b))

def selecao(populacao, itens):
	mutation_chance = 0.08
	filhos = []
	for x in range(0,POPULACAO_INICIAL_QUANT/2):
		individuo1 = roulleteWheel(populacao, itens)
		individuo2 = roulleteWheel(populacao, itens)
		while individuo1 == individuo2:
			individuo2 = roulleteWheel(populacao, itens)
		meio = len(individuo1)/2
		filho = individuo1[:meio] + individuo2[meio:]
		if mutation_chance > random.random():
			filho = mutacao(filho)
		filhos.append(filho)
		filho2 = individuo2[:meio] + individuo1[meio:]
		if mutation_chance > random.random():
			filho2 = mutacao(filho2)
		filhos.append(filho2)
	eleito = eletismo(populacao, itens)
	filhos.append(eleito)
	return filhos

def mutacao(individuo):
	r = random.randint(0,len(individuo)-1)
	if individuo[r] == 1:
			individuo[r] = 0
	else:
			individuo[r] = 1
	return individuo
	

def eletismo(populacao, itens):
	eleito = None
	valorEleito = 0
	for ind in populacao:
		if fitness(ind, itens) > valorEleito:
			eleito = ind
			valorEleito = fitness(ind, itens)
	return eleito

def calcularMedPop(populacao, itens):
	total = 0
	quantidade = 0
	for ind in populacao:
		total += fitness(ind, itens)
		quantidade += 1
	return total/quantidade

def verificarPadronizacao(mediaGeracoes):
	# for med in expression_list:
		# pass
	if (len(mediaGeracoes) >= 5):
		mediaGeracoes = mediaGeracoes[:5]
		if mediaGeracoes[1:] == mediaGeracoes[:-1]:
			return True
	return False


def main():
	geracao = 0
	itens = gerarItens() # gerar itens de acordo com o CSV
	populacao = gerarPopulacaoInicial(itens) # gerar a populacao inicial
	mediaGeracoes = []
	for g in range(0, GEN_MAXIMO):
		if verificarPadronizacao(mediaGeracoes): break
		geracao += 1
		print(" --- Geracao %s ---" % str(geracao))
		populacao = selecao(populacao, itens)
		for ind in populacao:
			print("%s, VALOR: [ %s ] PESO: [ %s ] FITNESS: [ %s ]" % (
				str(ind),
				pegarValorIndividuo(ind, itens),
				pegarPesoIndividuo(ind, itens),
				fitness(ind, itens))
			)
		mediaGeracoes.append(calcularMedPop(populacao, itens))
		print("MEDIA POPULACAO: [ %s ]" % (calcularMedPop(populacao, itens)))

if __name__ == "__main__":
  main()