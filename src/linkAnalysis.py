import networkx as nx

#Global variable to represent the graph
G = nx.DiGraph()

"""Return the PageRank of the nodes in the graph. 

PageRank computes a ranking of the nodes in the graph G based on 
the structure of the incoming links. It was originally designed as 
an algorithm to rank web pages. 

Parameters 
---------- 
G : graph 
	A NetworkX graph.  Undirected graphs will be converted to a directed 
	graph with two directed edges for each undirected edge. 

alpha : float, optional 
	Damping parameter for PageRank, default=0.85. 

personalization: dict, optional 
	The "personalization vector" consisting of a dictionary with a 
	key for every graph node and nonzero personalization value for each node. 
	By default, a uniform distribution is used. 

max_iter : integer, optional 
	Maximum number of iterations in power method eigenvalue solver. 

tol : float, optional 
	Error tolerance used to check convergence in power method solver. 

nstart : dictionary, optional 
	Starting value of PageRank iteration for each node. 

weight : key, optional 
	Edge data key to use as weight.  If None weights are set to 1. 

dangling: dict, optional 
	The outedges to be assigned to any "dangling" nodes, i.e., nodes without 
	any outedges. The dict key is the node the outedge points to and the dict 
	value is the weight of that outedge. By default, dangling nodes are given 
	outedges according to the personalization vector (uniform if not 
	specified). This must be selected to result in an irreducible transition 
	matrix (see notes under google_matrix). It may be common to have the 
	dangling dict to be the same as the personalization dict. 

Returns 
------- 
pagerank : dictionary 
	 Dictionary of nodes with PageRank as value 

Notes 
----- 
The eigenvector calculation is done by the power iteration method 
and has no guarantee of convergence.  The iteration will stop 
after max_iter iterations or an error tolerance of 
number_of_nodes(G)*tol has been reached. 

The PageRank algorithm was designed for directed graphs but this 
algorithm does not check if the input graph is directed and will 
execute on undirected graphs by converting each edge in the 
directed graph to two edges. 

	
"""
def pagerank(G, alpha=0.85, personalization=None, 
						 max_iter=100, tol=1.0e-6, nstart=None, weight='weight', 
						 dangling=None): 
	
	if len(G) == 0: 
		return {} 

	if not G.is_directed(): 
		D = G.to_directed() 
	else: 
		D = G 

	# Create a copy in (right) stochastic form 
	W = nx.stochastic_graph(D, weight=weight) 
	N = W.number_of_nodes() 

	# Choose fixed starting vector if not given 
	if nstart is None: 
		x = dict.fromkeys(W, 1.0 / N) 
	else: 
		# Normalized nstart vector 
		s = float(sum(nstart.values())) 
		x = dict((k, v / s) for k, v in nstart.items()) 

	if personalization is None: 

		# Assign uniform personalization vector if not given 
		p = dict.fromkeys(W, 1.0 / N) 
	else: 
		missing = set(G) - set(personalization) 
		if missing: 
				raise NetworkXError('Personalization dictionary '
														'must have a value for every node. '
														'Missing nodes %s' % missing) 
		s = float(sum(personalization.values())) 
		p = dict((k, v / s) for k, v in personalization.items()) 

	if dangling is None: 

		# Use personalization vector if dangling vector not specified 
		dangling_weights = p 
	else: 
		missing = set(G) - set(dangling) 
		if missing: 
				raise NetworkXError('Dangling node dictionary '
														'must have a value for every node. '
														'Missing nodes %s' % missing) 
		s = float(sum(dangling.values())) 
		dangling_weights = dict((k, v/s) for k, v in dangling.items()) 
	dangling_nodes = [n for n in W if W.out_degree(n, weight=weight) == 0.0] 

	# power iteration: make up to max_iter iterations 
	for _ in range(max_iter): 
		xlast = x 
		x = dict.fromkeys(xlast.keys(), 0) 
		danglesum = alpha * sum(xlast[n] for n in dangling_nodes) 
		for n in x: 

			# this matrix multiply looks odd because it is 
			# doing a left multiply x^T=xlast^T*W 
			for nbr in W[n]: 
					x[nbr] += alpha * xlast[n] * W[n][nbr][weight] 
			x[n] += danglesum * dangling_weights[n] + (1.0 - alpha) * p[n] 

		# check convergence, l1 norm 
		err = sum([abs(x[n] - xlast[n]) for n in x]) 
		if err < N*tol: 
				return x 
	raise NetworkXError('pagerank: power iteration failed to converge '
											'in %d iterations.' % max_iter)


"""
Inert the given input dictionary into the web graph

Parameters 
---------- 
webURLs: dictionary
	A dictionary with key as links and value as all outlinks.

"""

def insert(webURLs):
	# loop through all the input
	for URL1, outlinks in webURLs.items():
		# if the given URL is not in the graph, add it
		if URL1 not in G.nodes:
			G.add_node(URL1)
		# check if all connected URLs are still connected
		else: 
			for curr_outlink in G.successors(URL1):
				if curr_outlink not in outlinks:
					G.remove_edge(URL1, curr_outlink)
		# Loop though all the outlinks from the given URL1
		for URL2 in outlinks:
			# If the connected outlink is not in the graph
			if URL2 not in G.nodes:
					G.add_node(URL2)
			G.add_edge(URL1, URL2)
	print("Everything is successfully inserted in the WebGraph.")


"""
Delete the given input list of URLs into the web graph

Parameters 
---------- 
URLList: list
	A list of URLids which no longer valid in the graph

"""

def delete(URLList):
	for URL in URLList:
		if URL in G.nodes:
			# Remove all connected edges from and to this URL
			for from_URL in G.predecessors(URL):
				G.remove_edge(from_URL, URL)
			for to_URL in G.successors(URL):
				G.remove_edge(URL, to_URL)
			G.remove_node(URL)

	print("All URLs are successfully removed from the WebGraph")



"""
Run the pageRank algorithm and get results

Parameters 
---------- 
URLlist : list of URLs 
	A list which user will input and get the sorted dictionary of the lists
	Default set as all nodes in the graph

Returns
-------
result : list
	A sorted dictionary with (URLID, rank score) pair

"""
def getRanking(URLlist=G.nodes):
		pr = pagerank(G,0.4)
		
		results = dict()
		# Get all the rankings of the given URL list
		for URL in URLlist:
			# if the link is in the graph, provide the rank score
			if URL in pr.keys():
				results[URL] = pr[URL]
			#  if the link is not in the graph, provide 0
			else:
				results[URL] = 0
		# make a sorted array based on dictionary values. Descending order
		# Currently returns all nodes in the graph
		return sorted(results.items(), key=lambda results: results[1], reverse = True)

def getGraph():
	return G
