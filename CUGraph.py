#-*- coding: utf-8 -*-
import igraph
import igraph.vendor.texttable #needed for py2exe
import cairo
from unidecode import unidecode
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
		self.spritesNumber = len(spriteList)
		self.nameList.extend([cu.getName() for cu in self.CUCollection.getCollection()])

	def graphEdges(self,cuType,cuAsNode = False):
		"""
		graphEdges(self,cuType)
		returns list of tuples
		to be used for graphs
		"""
		
		edges = []
		if (cuAsNode):
			
			for cu in self.CUCollection.getCollection():
				#cuType filters the communication units
				#according to type
				if (cu.getCUType() == cuType):
					for aWriter in cu.getWriters():
						edges.append((self.nameList.index(aWriter),self.nameList.index(cu.getName())))
					for aReader in cu.getReaders():
						edges.append((self.nameList.index(cu.getName()),self.nameList.index(aReader)))
		else:
			for cu in self.CUCollection.getCollection():
				#cuType filters the communication units
				#according to the type
				if (cu.getCUType() == cuType):
					for aReader in cu.getReaders():
						for aWriter in cu.getWriters():
							#do not remove duplicates
							#if ((self.nameList.index(aReader),self.nameList.index(aWriter)) not in edges):
								edges.append((self.nameList.index(aWriter),self.nameList.index(aReader)))
		return edges
	
	def writeGraph(self,filename,cuType="all",cuAsNode = False):
		if (cuType == "all"):
			#allEdges is consists of edges from variables/messages/lists
			
			allEdges = self.graphEdges("variable",True)
			#REMOVE DUPLICATES
			#allEdges.extend([edge for edge in self.graphEdges("list") if edge not in allEdges])
			#allEdges.extend([edge for edge in self.graphEdges("message") if edge not in allEdges])
			#allEdges.extend([edge for edge in self.graphEdges("scene",True) if edge not in allEdges])
			allEdges.extend([edge for edge in self.graphEdges("list",True)])
			allEdges.extend([edge for edge in self.graphEdges("message",False)])
			allEdges.extend([edge for edge in self.graphEdges("scene",True)])
		else:
			allEdges = self.graphEdges(cuType,cuAsNode = cuAsNode)
		
		if (len(allEdges)>0):
			bbox = igraph.BoundingBox(800,600)
			surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,800,600)
			g = igraph.Graph(allEdges,directed = True)
			#multiple lines are depicted
			igraph.autocurve(g)

			#all sprites are depicted in the graph 
			#connected or not
			#labels converted to greeklish
			#only last 6 digits -> does not clutter graph with huge names
			g.vs["label"] = [unidecode(unicode(label))[-11:] for label in self.nameList]

			
			for i in range(1,len(g.vs)):
				g.vs[i]["color"]="blue"
			for i in range(1,min(self.spritesNumber,len(g.vs))):
				g.vs[i]["color"]="red"
			#remove isolated vertices
			verticesToRemove = []
			for vertex in g.vs:
				if (g.degree(vertex)<1):
					verticesToRemove.append(vertex)
			g.delete_vertices(verticesToRemove)
			#g.write_adjacency(filename + ".adj")
			#layout = g.layout("kk")
			#g.write_svg(filename + ".svg")#,layout = layout)
			plot = igraph.plot(g,surface,bounding_box = bbox)
			plot.background = None
			plot.redraw()
			print(filename)
			surface.write_to_png(filename + ".png")
		else:
			print("No edges for type: %s") % (cuType)

		


