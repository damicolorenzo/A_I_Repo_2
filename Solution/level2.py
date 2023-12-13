from agents import Environment
from level1 import Level1
from searchProblem import Search_problem_from_explicit_graph
from searchGeneric import AStarSearcher
from searchProblem import Arc
import matplotlib.pyplot as plt
import matplotlib as mplot
import networkx as nx


class Level2(Environment):
    def __init__ (self, level1):
        self.mat = level1.mat
        self.graph = level1.graph
        self.start_node = level1.start
        self.goal = level1.goal
        self.square_list = []
        self.solution = set()
        self.plotting_solution = []
    
    def plot_draw(self):
        self.square_list = []
        (M, N) = (len(self.mat), len(self.mat[0]))
        for i in range(M):
            for j in range(N):
                if self.mat[i][j] == 0:
                    self.square_list.append(mplot.patches.Rectangle((j*10, M*10-i*10), 10, -10, color='blue', fc = 'none',lw = 2))
                if self.mat[i][j] == 1:
                    self.square_list.append(mplot.patches.Rectangle((j*10, M*10-i*10), 10, -10, color='blue',lw = 2))
                if self.mat[i][j] == "s":
                    self.square_list.append(mplot.patches.Rectangle((j*10, M*10-i*10), 10, -10, color='green',lw = 2))
                if self.mat[i][j] == "g":
                    self.square_list.append(mplot.patches.Rectangle((j*10, M*10-i*10), 10, -10, color='red',lw = 2))
        return self.square_list
    
    def plot_draw_solution(self):
        list1 = []
        for en in self.solution.nodes():
            list1.append(en)
        list2 = reversed(list1)
        (M, N) = (len(self.mat), len(self.mat[0]))
        self.plotting_solution = list2
        return self.plotting_solution

    def control(self, visited, point, point1):
        x, y = point[0], point[1]
        x1, y1 = point1[0], point1[1]
        var = True
        for el in visited:
            if (el == (x, y) and visited[el] == (x1, y1)) or (el == (x1, y1) and visited[el] == (x, y)):
                var = False
        return var

    def graphToProblem(self):
        nodes = []
        for node in self.graph:
            nodes.append(node)
        arcs = []
        visited = {}
        for node in self.graph:
            dictionary = self.graph[node] 
            for element in dictionary:
                dictionary2 = dictionary[element] 
                for elem in dictionary2:
                    cost = dictionary2[elem]
                    if self.control(visited, node, element):
                        visited.update({node: element})
                        arcs.append(Arc(node, element, cost))
        start_node = self.start_node
        goal = self.goal
        self.problem = Search_problem_from_explicit_graph(nodes, arcs, start_node, goal)
        return self.problem

    def plot_run(self):
        self.problem = self.graphToProblem()
        s = AStarSearcher(self.problem)
        self.solution = s.search()
        self.plot_draw_solution()
        return self.plotting_solution


mat = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 'g', 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 's', 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

level1 = Level1(mat)
G = nx.DiGraph()
G = level1.createGraph()

pos = nx.nx_agraph.graphviz_layout(G,prog='neato')
nx.draw_networkx_nodes(G,pos,node_size=300)
edgeslist = [(u, v) for (u, v, d) in G.edges(data=True)]
nx.draw_networkx_labels(G, pos, font_size=8, font_family="sans-serif")
edge_labels = nx.get_edge_attributes(G, "cost")
nx.draw_networkx_edge_labels(G, pos, edge_labels)

level2 = Level2(level1)
fig = plt.figure()
ax = fig.add_subplot(111)

plt.xlim(0, len(level2.mat)*10)
plt.ylim(0, len(level2.mat)*10)
for el in level2.plot_draw():
    ax.add_patch(el)
plt.draw()

solution = level2.plot_run()
(M, N) = (len(mat), len(mat[0]))

for el in solution:
    i, j = el[0], el[1]
    node = mplot.patches.Rectangle((j*10, M*10-i*10), 10, -10, color='grey',lw = 1)
    ax.add_patch(node)
    plt.pause(0.5)
    plt.draw()
plt.show()

