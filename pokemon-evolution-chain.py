# coding=utf-8

from urllib.request import Request, urlopen
import json
import re

def getJson(url):
	global data

	requestData = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	openData = urlopen(requestData).read()

	data = json.loads(openData)

	return data

pokemonInput = input("Pokemon ID eller navn: ")

pokemonData = getJson('https://pokeapi.co/api/v2/pokemon-species/' + pokemonInput) # Henter all data om spesifikk Pokemon

evoChainUrl = pokemonData["evolution_chain"]["url"] # Henter URL for evolution chain for spesifikk Pokemon fra Pokemon data
evoData = getJson(evoChainUrl)["chain"] # Henter data fra evolution chain

print ("Evolution chain for #" + str(pokemonData["id"]) + " - " + pokemonData["name"].title() + ":")

evoChain = []

rePattern = '/\d+/' # RegEx mønster for å hente ut Pokemon ID fra url

evoChain.append([re.findall(rePattern, str(evoData["species"]["url"]))[0].replace('/', ''), evoData["species"]["name"]]) # Legger til første Pokemon

while (evoData["evolves_to"]):
	reResult = re.findall(rePattern, str(evoData["evolves_to"][0]["species"]["url"]))

	evoChain.append([reResult[0].replace('/', ''), evoData["evolves_to"][0]["species"]["name"]]) # Legger til Pokemon ID og navn

	evoData = evoData["evolves_to"][0]  # Går videre til neste Pokemon i evolution chain

	# if not evoData["evolves_to"]: # Hvis det ikke finnes flere Pokemons i evolution chain
		# print ("Finished")

for pokemon in evoChain:
	print ("#" + pokemon[0] + " - " + pokemon[1].title())
