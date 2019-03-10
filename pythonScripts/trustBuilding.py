import urllib.request
import random
import json
import os
from time import sleep

#print(authenticNode)
connected_nodes = []   #nodes present in the network
banned_nodes = {}    # banned nodes
trust_values = {}    # trust values of each and every node
trust_ranking = {}   # ranking based on trust value (visible)
def checkConnectivity():    #checking connectivity of nodes in network
    nodes = ["http://192.168.43.117:3001/", "http://192.168.43.117:3002/", "http://192.168.43.117:3003/", "http://192.168.43.117:3004/", "http://192.168.43.117:3005/"]

    for node in nodes:
        response = os.system("curl -I " + node)

        if response == 0:
            #pingStatus = True
            connected_nodes.append(node[:-1])
        #else:
            #pingStatus = False

    #return pingStatus
checkConnectivity()
trust_values = { i : 0 for i in connected_nodes }


def connectionPersists(node):   #persistance of connection of nodes in network
    response = os.system("curl -I " + node + "/")
    if response == 0:
        return True
    return False

#checkConnectivity()
#print (connected_nodes)


#print (trust_values)


def authentication():   #validation phase of transaction
    node = random.choice(connected_nodes)
    url = node + "/blockchain"
    open_url = urllib.request.urlopen(url)
    data = json.load(open_url)

    if not 'pendingTransactions' in data or len(data['pendingTransactions']) != 0:
        for txn in data['pendingTransactions']:
            value = trust_values[txn['node']]
            value =  value + 1
            trust_values[txn['node']] = value 
    else:
        print ("No pending transaction to process")

#authentication()
#print (trust_values)
"""
nodes = ["http://192.168.43.119:3001", "http://192.168.43.119:3002", "http://192.168.43.119:3003", "http://192.168.43.119:3004", "http://192.168.43.119:3005"]
trust = {nodes[0]:0,nodes[1]:0, nodes[2]:0, nodes[3]:0, nodes[4]:0}
list_node=[]

def authentication():
    node = random.choice(nodes)
    url = node + "/blockchain"   
    r = urllib.request.urlopen(url) 
    data = json.load(r)
    for txn in data['pendingTransactions']:
         #print(txn['transactionId'])
         list_node.append(txn['nodeName'])

#authentication()
#print (list_node)

def dosprevention():
    #checkConnectivity()

    if (checkConnectivity()):
        sleep(60)
        if (checkConnectivity()):
            value = trust[dos_prevented]
            value = value +8
            trust[dos_prevented] = value
        else:
            value = trust[dos_prevented]
            value = value - 8
            trust[dos_prevented] = value

    else:
        print ("Network node not connected")        

def mine():
    a = authentication()
    if len(list_node) !=0:
        for node in list_node:
            value = trust[node]
            #print(value)
            value = value + 1
            trust[node]=value
            #print ("ignore")
        list_node = []
            
    miner_node = random.choice(nodes)
    url = miner_node + "/mine"
    r = urllib.request.urlopen(url)
    data = json.load(r)

    value = trust[miner_node]
    value = value +8
    trust[miner_node]=value

    
def scalable():
    print ("scaling")



def trustvalue():
    authentication(node)
    mine(node)
    dosPrevention()
    #majorityApproval(node)
"""

def timeMeasure():   #time based incentives for nodes

    for node in connected_nodes:
        if connectionPersists(node):
            value = trust_values[node]
            value = value + 1
            trust_values[node] = value
    
def blockMiner():   #mining rewards for nodes which also includes points
    authentication()
    miner_node = random.choice(connected_nodes)
    url = miner_node + "/mine"

    mined = urllib.request.urlopen(url)
    data = json.load(mined)

    value = trust_values[miner_node]
    value = value + 8
    trust_values[miner_node] = value
    

def banned(node, value):   #trace of banned nodes
    banned_nodes.update({node, value})
    
def trustRanking(trust_value):   #trust ranking based on points in network

    for node in trust_value:

        if trust_value[node] < -10:
            banned(node, trust_value[node])
            
        elif -10<= trust_value[node] <0:
            value = "NA"
            trust_ranking[node]=value
        
        elif 0<= trust_value[node] <=10:
            value = "Silver 1"
            trust_ranking[node]=value
            #node + "has Silver 1 ranking"
        elif 11 < trust_value[node] <=18:
            value = "Silver 2"
            trust_ranking[node]=value
        elif 19 < trust_value[node] <=32:
            value = "Silver 3"
            trust_ranking[node]=value
        elif 33 < trust_value[node] <=40:
            value = "Silver 4"
            trust_ranking[node]=value
        elif 41 < trust_value[node] <=52:
            value = "Silver 5"
            trust_ranking[node]=value
        elif 53 < trust_value[node]  <=60:
            value = "Silver 6"
            trust_ranking[node]=value
        elif 61 <trust_value[node]  <=75:
            value = "Silver 7"
            trust_ranking[node]=value
        elif 76 < trust_value[node]  <=82:
            value = "Silver 8"
            trust_ranking[node]=value
        elif 83 < trust_value[node]  <=99:
            value = "Silver 9"
            trust_ranking[node]=value
        elif 100 <trust_value[node]  <=120:
            value = "Silver 10"
            trust_ranking[node]=value
        elif 121 < trust_value[node] <=180:
            value = "Gold 1"
            trust_ranking[node]=value
        elif 181 < trust_value[node]  <=300:
            value = "Gold 2"
            trust_ranking[node]=value
        elif 301 < trust_value[node]:
            value = "Gold 3"
            trust_ranking[node]=value

#print (trust_values)
#blockMiner()
#print (trust_values)
#trustRanking(trust_values)
#print (trust_values)



def buildingTrust():   #infinite running and monitoring function which will keep track of ranks of nodes
    while True:
        blockMiner()
        #print ("After Block")
        #print (trust_values)
        timeMeasure()
        #print ("After Time")
        #print (trust_values)
        trustRanking(trust_values)
        print (trust_ranking)
        sleep(100)


buildingTrust()
"""
while True:
    mine()
    print (trust)
    sleep(100)

#print (trust)
"""

