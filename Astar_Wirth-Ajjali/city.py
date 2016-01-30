# -*-coding:Latin-1-*
__author__ = "Wirth Jeremy & Wassim Ajjali"

class City:
	def __init__(self, name, x,y, parent):
		self.name = name
		self.x = x
		self.y = y
		self.parent = parent
		self.d = 0
		self.h = 0
		self.listConnection = []
		
	def __repr__(self):
		return self.name
		
	def addConnection(self, city):
		self.listConnection.append(city)
		
	def getConnection(self):
		return self.listConnection
		
	def __lt__(self, other):
		return self.h < other.h
		
	def __eq__(self, other):
		return self.name == other.name
		
	def parcours(self):
		listParent = [self]
		parent = self.parent
		result = ""
		while parent != None:
			listParent.append(parent)
			parent = parent.parent
		for city in reversed(listParent):
			result += city.name + " (" + str(city.d) +" km)\n"
		return result