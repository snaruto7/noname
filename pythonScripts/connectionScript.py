import urllib.request
import json      
import random

node1 = "http://192.168.43.117:3001"
node2 = "http://192.168.43.117:3002"
node3 = "http://192.168.43.117:3003"
node4 = "http://192.168.43.117:3004"

nodes = [node1, node2, node3, node4]

def registerAll():
    for i in range(len(nodes)):
        body = {'newNodeUrl': nodes[i] }  
        myurl = "http://192.168.43.117:3005/register-and-broadcast-node"
        req = urllib.request.Request(myurl)
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        jsondata = json.dumps(body)
        jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
        req.add_header('Content-Length', len(jsondataasbytes))

        #print (jsondataasbytes)
        response = urllib.request.urlopen(req, jsondataasbytes)
        if response.getcode() == 200:
            print ("Nodes registered to the network successfully")
        else:
            print ("Cannnot connect to network")


registerAll()
def scaling(string):
    node=random.choice(nodes)
    body = { 'newNodeUrl': string }
    myurl = node+"/register-and-broadcast-node"
    req = urllib.request.Request(myurl)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))

    #print (jsondataasbytes)
    response = urllib.request.urlopen(req, jsondataasbytes)
    if response.getcode() == 200:
        print ("new node" + string + " Successfully registered in the network")
    else:
        print ("Error registering node to the network")


