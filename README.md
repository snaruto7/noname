# nonamenormies


This is Blockchain based fintech application with python GUI

In Blockchain folder and developer folder:
  **blockchain.js** file is to make own blockchain from scratch
  **networkNodes.js** file is to create miner nodes for the blockchain network
  
  
  
  Currently we have made this for 5 nodes, which are separated by 5 different ports 
  To run the blockchain server:
      
   Go inside blockchain folder and run **npm run node_1** and similarly upto **node_5**
   after running 5 different nodes run **connectionScript.py** in pythonScripts folder to synchronise the blockchain network
  We have implemented Trust based ranking method which will enable to build trust in decentralized environment preventing Sybil Attack
  This is infinite running script named as **trustBuilding.py** which will monitor and calculate each and every nodes

For Users end:

  Python GUI is been created named as **paygridApp.py**, it will launch a GUI for user and allow them to make transaction seamlessly.
