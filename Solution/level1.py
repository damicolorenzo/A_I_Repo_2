import networkx as nx
from agents import Environment
from queue import PriorityQueue

class Level1(Environment):
	def __init__(self, mat):
		self.row = [0, 1, 0, -1]
		self.col = [1, 0, -1, 0]
		self.graph = nx.DiGraph()
		self.goal = []
		self.start = ()
		self.mat = mat
		#self.visiting = True

	def isSafe(self, x, y):
		return (x >= 0 and x < len(self.mat)) and (y >= 0 and y < len(self.mat[0])) and (self.mat[x][y] == 0 or self.mat[x][y] == 'g' or self.mat[x][y] == 's')

	def manDistance(self, point1, point2):
		x1, y1 = point1[0], point1[1]
		x2, y2 = point2[0], point2[1]
		return abs(x1-x2) + abs(y1-y2)
		
	def BestFSVisit(self, que):
		history = []
		graphHistoryNode = []
		while que.qsize() != 0:
			lista = []
			obj = que.get()
			node = obj[1]
			x, y = node[0], node[1]
			if self.mat[x][y] != 'g':
				history.append(node)
				for k in range(len(self.row)):
					if self.isSafe(x + self.row[k], y + self.col[k]) and (x + self.row[k], y + self.col[k]) not in history:
						self.graph.add_edge((x, y), (x + self.row[k], y + self.col[k]), cost=self.manDistance((x + self.row[k], y + self.col[k]), self.goal[0]))	
						if ((x + self.row[k], y + self.col[k])) not in graphHistoryNode:
							lista.append((self.manDistance((x + self.row[k], y + self.col[k]), self.goal[0]),  (x + self.row[k], y + self.col[k])))
							que.put((self.manDistance((x + self.row[k], y + self.col[k]), self.goal[0]),  (x + self.row[k], y + self.col[k])))
						if self.mat[x + self.row[k]][y + self.col[k]] != 'g':
							graphHistoryNode.append((x + self.row[k], y + self.col[k]))
		return self.graph

	def createGraph(self):
		if not self.mat or not len(self.mat):
			return 0
		
		(M, N) = (len(self.mat), len(self.mat[0]))

		self.processed = [[False for x in range(N)] for y in range(M)]
	
		for i in range(M):
			for j in range(N):
				if self.mat[i][j] == 's':
					self.start = (i, j)
				if self.mat[i][j] == 'g':
					self.goal.append((i, j))
					
		que = PriorityQueue()
		que.put((0, self.start))
		self.BestFSVisit(que)

		""" nearToNear = {}
		self.DFSvisit(nearToNear, self.start) """
		
		return self.graph
	
	""" #Can be a partial solution for point 1 
	def oldOnes(sef, point, list):
		(x, y) = point
		if (x, y) in list:
			return False
		else:
			return True
		
	def DFSvisit(self, nearToNear, near):
		self.row = [-1, 0, 0, 1]
		self.col = [0, -1, 1, 0]
		x, y = near[0], near[1]
		count = 0
		for k in range(len(self.row)):
			count += 1
			if self.isSafe(x + self.row[k], y + self.col[k]) and self.oldOnes((x + self.row[k], y + self.col[k]), nearToNear):
				if not self.mat[x][y] == 'g' and self.visiting:
					print((x, y), (x + self.row[k], y + self.col[k]))
					self.graph.add_edge((x, y), (x + self.row[k], y + self.col[k]), cost=self.manDistance((x + self.row[k], y + self.col[k]), self.goal[0]))
					nearToNear.update({(x, y):count})
					self.DFSvisit(nearToNear, (x + self.row[k], y + self.col[k]))
				else:
					self.visiting = False
					return self.graph """

