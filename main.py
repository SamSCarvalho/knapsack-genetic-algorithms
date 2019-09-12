import csv
import random
from item import Item

GEN_MAXIMO = 200
POPULACAO_INICIAL_QUANT = 9
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
	for i in individuo:
		if index >= len(itens):
			break
		if (i == 1):
			totalValor += itens[index].valor
			totalPeso += itens[index].peso
		index += 1

	# return totalPeso <= CAPACIDADE_MOCHILA
	if totalPeso > CAPACIDADE_MOCHILA:
		return False # INDIVIDUO COM PESO MAIOR QUE CAPACIDADE :(
	else:
		return individuo # ESTA OKAY
	
def main():
	itens = gerarItens() # gerar itens de acordo com o CSV
	populacao = gerarPopulacaoInicial(itens) # gerar a populacao inicial
	print(populacao)
	for g in range(0, GEN_MAXIMO):
		populacao = filter(lambda x: fitness(x, itens), populacao)
		print(" -- Populacao selecionada -- ")
		print(populacao)

if __name__ == "__main__":
  main()