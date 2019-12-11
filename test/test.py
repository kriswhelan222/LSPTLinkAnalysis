from linkAnalysis import insert, getRanking, getGraph
import networkx as nx

def test_insert():
	# G_test = nx.DiGraph()
	webURLs1 = {
			  "http://home.com/": 
			  	[
			      "http://index.com/",
			      "http://intro.com/",
			      "http://schools.com/"
			    ]
			  ,
			  "http://index.com/":  
			  	[
			      "http://home.com/"
			    ]
			  ,
			   "http://schools.com/": 
			    [
			      "http://home.com/"
			    ]
			}
	insert(webURLs1)
	webURLs2 = {
			  "http://schools.com/": 
			  	[
			      "http://cs.com/",
			      "http://ee.com/",
			      "http://art.com/",
			      "http://management.com"
			    ]
			  ,
			  "http://cs.com/":  
			  	[
			      "http://cs1.com/",
			      "http://ds.com/"

			    ]
			  ,
		  	  "http://intro.com/": 
			    [
			      "http://home.com/"
			    ]
			   ,
			}
	insert(webURLs2)
	G_test = getGraph()
	assert G_test.number_of_nodes() == 10
	assert len(list(G_test.neighbors("http://home.com/"))) == 3
	assert len(list(G_test.neighbors("http://schools.com/"))) == 5
	assert len(list(G_test.successors("http://cs.com/"))) == 2
	assert len(list(G_test.predecessors("http://cs.com/"))) == 1
	print('Pass all tests for "insert"')

def test_pageRank():
	G_test = getGraph()
	G_test.remove_node("http://cs1.com/")
	G_test.remove_node("http://ds.com/")
	assert len(list(G_test.successors("http://cs.com/"))) == 0
	assert len(list(G_test.predecessors("http://cs.com/"))) == 1
	rank = getRanking(["http://cs.com/", "http://ee.com/"])
	assert rank[0][1] == rank[1][1]
	rank = getRanking(["http://index.com/", "http://intro.com/", "http://schools.com/"])
	assert rank[0][1] == rank[1][1]
	assert rank[1][1] == rank[2][1]
	print('Pass all tests for "getRanking"')

if __name__ == '__main__':
	test_insert()
	test_pageRank()