# LSPTLinkAnalysis
Large scale programming and testing: link analysis team as part of an RPI-based search engine

##  Team Members
- Kris Whelan
- Yazhi Wang
- Jinyi Xie
- Troy Ferrazzano

## hostname: 
lspt-link1.cs.rpi.edu

## Interact with other teams

### Crawling
#### start()
- Send a list of rpi.edu related URL to the Crawling team to start the system
- Not implemented yet

### Document Data Store
#### insert(webURLs)
- When Crawling get links and related outlinks, they are expected to send to DDS and DDS will send us the relationship using URLid to replace the URL link
- Our webgraph will be updated and send a message to DDS

### Ranking
#### getRanking(URLList)
- When Ranking wants a ranking of list of URLs, they will send us the list of URLids
- Our webgraph will get the output from pagerank algorithm and send a sorted list of (URLid, score) pair to Ranking
- By default, URLList assumes all nodes in the graph
