#-*- coding: utf-8 -*-
import igraph
from Sprites import *


class CUGraph():
	"""
	class CUGraph is a class
	that is used to create
	graph of communication units
	"""
	def __init__(self,CUCollection,spriteList):
		self.CUCollection = CUCollection
		#nameList is a list of the names of the sprites
		#it is used to get a consistent index of a sprite
		self.nameList = [sp.name for sp in spriteList]

	def graphEdges(self,cuType):
		"""
		graphEdges(self,cuType)
		returns list of tuples
		to be used for graphs
		"""
		
		edges = []
		for cu in self.CUCollection.getCollection():
			#cuType filters the communication units
			#according to the type
			if (cu.getCUType() == cuType):
				for aReader in cu.getReaders():
					for aWriter in cu.getWriters():
						if ((self.nameList.index(aReader),self.nameList.index(aWriter)) not in edges):
							edges.append((self.nameList.index(aWriter),self.nameList.index(aReader)))
		return edges
	
	def writeGraph(self,filename,cuType="all"):
		if (cuType == "all"):
			#allEdges is consists of edges from variables/messages/lists
			#if two sprites are connected with two or more CUs 
			#only one line is drawn
			allEdges = self.graphEdges("variable")
			allEdges.extend([edge for edge in self.graphEdges("list") if edge not in allEdges])
			allEdges.extend([edge for edge in self.graphEdges("message") if edge not in allEdges])
		else:
			allEdges = self.graphEdges(cuType)
		if (len(allEdges)>0):
			g = igraph.Graph(allEdges,directed = True)
			#all sprites are depicted in the graph 
			#connected or not
			g.vs["label"] = self.nameList
			layout = g.layout("kk")
			g.write_svg(filename + ".svg",layout = layout)
		else:
			print("No edges for type: %s") % (cuType)
		
