# -*-coding:Latin-1-*
__author__ = "Wirth Jeremy & Wassim Ajjali"

from city import City
from math import sqrt

# QUESTIONS
# Quelles sont les heuristique admissible :
# - Vol d'oiseau et manhattan car se sont les 2 seules à prendre en compte les 2 composantes x et y
# Les differentes heuristiques ont-elles une influence sur le nombre de visite :
# - Oui cela depend des villes A et B, certain parcours comme Warsaw -> Lisbon me donne un nombre de villes constant (19) mais pour un parcours Warsaw -> Paris, le nombre varie fortement (7,6,15,17)
# Dans un cas reelle ? :
# - distance a vol d'oiseau

cityConnection = {}
cityDic = {}

""" PARSING - ville """
def positionParse(positions):
	lines = positions.split("\n")
	for line in lines:
		word = line.split(" ")
		city = City(word[0], word[1], word[2], None)
		cityDic[word[0]] = city

""" PARSING - connexion entre les villes """	
def connectionParse(connections):
	lines = connections.split("\n")
	for line in lines:
		word = line.split(" ")
		if(word[0] in cityConnection) and (word[1] in cityConnection):
			cityConnection[word[0]].update({word[1] : word[2]})
			cityConnection[word[1]].update({word[0] : word[2]})
		else:
			if word[0] in cityConnection:
				cityConnection[word[0]].update({word[1] : word[2]})
			else:
				cityConnection[word[0]] = {word[1] : word[2]}
			if word[1] in cityConnection :
				cityConnection[word[1]].update({word[0] : word[2]})
			else:
				cityConnection[word[1]] = {word[0] : word[2]}

""" HEURISTIQUE """
def h_0(c1, c2):
	return 0
def h_distX(c1, c2):
	return abs(int(c2.x) - int(c1.x))
def h_distY(c1,c2):
	return abs(int(c2.y) - int(c1.y))
def h_volOiseau(c1,c2):
	return sqrt((int(c2.x) - int(c1.x))**2 + (int(c2.y) - int(c1.y))**2)
def h_manhattan(c1,c2):
	return h_distX(c1,c2) + h_distY(c1,c2)

""" Creation des listes de connexion entre les villes """
def createConnection():
	for cName in cityConnection.keys():
		city = cityDic[cName]
		for cConn in cityConnection[cName]:
			city.addConnection(cityDic[cConn])

def astar(departure, destination, heuristic, nameHeuristic):
	cityStart = cityDic[departure]
	cityEnd = cityDic[destination]
	
	result = str(nameHeuristic) + "\n------------------------\n"
	frontiere = []
	history = []
	
	frontiere.append(cityStart)
	
	while len(frontiere) > 0:
		result += "front : " + str(frontiere) + "\n"
		city = frontiere.pop(0)
		history.append(city.name)
		result += "hist : " + str(history) + "\n"
		
		if city.name == cityEnd.name:
			result += "\nNombre de ville visiter: " + str(len(history))+ "\ndistance parcouru : " + str(city.d) + " km\n" +"\nChemin :\n" + city.parcours() + "\n"
			return result

		nextCities = city.getConnection()
		
		for c in nextCities:
			newCity = City(c.name, c.x, c.y, city)
			newCity.d = city.d + int(cityConnection[city.name][newCity.name])
			
			newCity.h += heuristic(city, newCity)
			newCity.listConnection = cityDic[c.name].listConnection
			if (newCity not in frontiere) and (c.name not in history):
				frontiere.append(newCity)
				
		frontiere.sort()
		
	result += str(nameHeuristic) + "\n------------------------\nNo solution"
	return result
	
if __name__ == "__main__":
	
	fileConnections = open("data/connections.txt", "r")
	filePositions = open("data/positions.txt", "r")
	
	connectionParse(fileConnections.read())
	positionParse(filePositions.read())
	createConnection()
	
	departure = "Warsaw"
	destination = "Lisbon"

	result = astar(departure, destination, h_0, "heuristic_0")
	result += astar(departure, destination, h_distX, "heuristic_distance_x")
	result += astar(departure, destination, h_distY, "heuristic_distance_y")
	result += astar(departure, destination, h_volOiseau, "heuristic_vol_oiseau")
	result += astar(departure, destination, h_manhattan, "heuristic_manhattan")
	
	print result
	text_file = open("Output.txt", "w")
	text_file.write("%s" % result)
	text_file.close()
	
		
	