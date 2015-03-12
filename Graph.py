class Directed_Graph(object):

	def __init__(self, list):
		''' Initializes a Graph object '''
		self.__graph_dict = {x:{} for x in list}

	def edges(self):
		''' returns the edges of a graph as a dictionary
			keys are ordered pairs (start, end)
			values are weight of edge between start and end
			{(start, end): weighted_edge}
		'''
		return self.__generate_edges()

	def add_vertex(self, vertex):
		if vertex not in self.__graph_dict.keys():
			self.__graph_dict[vertex] = []

	def add_edge(self, start, end):
		if start in self.__graph_dict.keys():
			if end not in self.__graph_dict[start].keys():
				self.__graph_dict[start][end] = 1
			else:
				self.__graph_dict[start][end] +=1

	def define_edge(self, start, end, value):
		if start in self.__graph_dict.keys():
			if end in self.__graph_dict[start].keys():
				self.__graph_dict[start][end] = value

	def __generate_edges(self):
		'''	A static method to generate edges. Edges are represented as dictionaries
			with ordered sets of two nodes as keys, and values of the edge's weight
		'''
		edges = {}
		for vertex in self.__graph_dict.keys():
			for neighbor in self.__graph_dict[vertex].keys():
				if (neighbor, vertex, self.__graph_dict[vertex][neighbor]) not in edges:
					edges[(vertex, neighbor)] = self.__graph_dict[vertex][neighbor]
		return edges


	def __str__(self):
		'''	Creates a printable string listing graph's vertices and edges.'''
		res = "vertices: "
		for k in self.__graph_dict:
			res += str(k) + " "
		res += "\nedges: "
		for edge in self.__generate_edges():
			res += str(edge) + " "
		return res


	def dijkstra(self, initial, end):
		''' When implemented, will traverse tree from 'initial' to 'end' in order
			to find the best segmentation for a word. Will replace need for
			morpho.scoreSegmentation(), which uses brute force approach
		'''
		return 