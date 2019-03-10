const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const Blockchain = require('./blockchain');
const paygrid = new Blockchain();
const uuid = require('uuid/v1');
const nodeAddress = uuid().split('-').join('');
const port = process.argv[2];
const rp = require('request-promise');

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false}));


app.get('/',function(req,res){
	res.send("Connection is working fine... Proceed to different API");
});

app.get('/blockchain',function(req,res){
	res.send(paygrid);
});


app.post('/transaction', function(req,res){
	const newTransaction= req.body;
	const blockIndex = paygrid.addTransactionToPendingTransactions(newTransaction);
	res.json({ note : `The transaction will be added to block number ${blockIndex}.`});
});


app.post('/transaction/broadcast', function(req,res){
	const newTransaction = paygrid.createNewTransaction(req.body.node, req.body.amount, req.body.sender, req.body.recipient);
	paygrid.addTransactionToPendingTransactions(newTransaction);

	const requestPromise = [];
	paygrid.networkNodes.forEach(networkNodeUrl =>{
		const requestOptions = {
			uri: networkNodeUrl + '/transaction',
			method: 'POST',
			body: newTransaction,
			json: true
		};

		requestPromise.push(rp(requestOptions));
	});

	Promise.all(requestPromise)
	.then(data =>{
		res.json({ note: "Transaction created and broadcast sucessfully." });
	});
});

app.get('/mine', function(req,res){
	const lastBlock = paygrid.getLastBlock();
	const previousBlockHash = lastBlock['hash'];

	const currentBlockData = {
		transactions: paygrid.pendingTransactions,
		index: lastBlock['index']+1
	};
	const nonce = paygrid.proofOfWork(previousBlockHash, currentBlockData);
	const blockHash = paygrid.hashBlock(previousBlockHash, currentBlockData, nonce);

	//paygrid.createNewTransaction(12.5,"00",nodeAddress);

	const newBlock = paygrid.createNewBlock(nonce, previousBlockHash, blockHash);

	const requestPromise = [];
	paygrid.networkNodes.forEach(networkNodeUrl =>{
		const requestOptions = {
			uri: networkNodeUrl + '/receive-new-block',
			method: 'POST',
			body: { newBlock: newBlock },
			json: true
		};

		requestPromise.push(rp(requestOptions));
	});

	Promise.all(requestPromise)
	.then(data => {
		const requestOptions = { 
			uri: paygrid.currentNodeUrl + '/transaction/broadcast',
			method: 'POST',
			body: {
				node: paygrid.currentNodeUrl,
				amount: 12.5,
				sender: "00",
				recipient: nodeAddress
			},
			json: true
		};

		return rp(requestOptions);
	})
	.then(data => {
		res.json({
		note: "New Block mined & broadcast sucessfully",
		block: newBlock
		});
	});
});


app.post('/receive-new-block', function(req,res){
	const newBlock = req.body.newBlock;
	const lastBlock = paygrid.getLastBlock();
	const correctHash = lastBlock.hash === newBlock.previousBlockHash;
	const correctIndex = lastBlock['index'] + 1 === newBlock['index'];

	if(correctIndex && correctHash){
		paygrid.chain.push(newBlock);
		paygrid.pendingTransactions = [];
		res.json({
			note: "New Block verified and accepted",
			newBlock: newBlock
		});
	} else {
		res.json({
			note: "New Block rejected",
			newBlock: newBlock
		});
	}
});

app.post('/register-and-broadcast-node', function(req,res){
	const newNodeUrl = req.body.newNodeUrl;
	if(paygrid.networkNodes.indexOf(newNodeUrl) == -1)
		paygrid.networkNodes.push(newNodeUrl);

	const regNodesPromises = [];
	paygrid.networkNodes.forEach(networkNodeUrl => {
		const requestOptions = {
			uri: networkNodeUrl + '/register-node',
			method: 'POST',
			body: { newNodeUrl: newNodeUrl},
			json: true
		};

		regNodesPromises.push(rp(requestOptions));
	});

	Promise.all(regNodesPromises)
	.then(data => {
		const bulkRegisterOptions = {
			uri: newNodeUrl + '/register-nodes-bulk',
			method: 'POST',
			body: { allNetworkNodes: [ ...paygrid.networkNodes, paygrid.currentNodeUrl ] },
			json: true
		};

		return rp(bulkRegisterOptions);
	})
	.then(data => {
		res.json({ note: 'New Node registered with network successfully.' });
	});
});



app.post('/register-node', function(req,res){
	const newNodeUrl = req.body.newNodeUrl;
	const nodeNotAlreadyPresent = paygrid.networkNodes.indexOf(newNodeUrl) == -1;
	const notCurrentNode = paygrid.currentNodeUrl !== newNodeUrl;
	if(nodeNotAlreadyPresent && notCurrentNode)
		paygrid.networkNodes.push(newNodeUrl);
	res.json({ note: 'New node registered successfully.' });
});

app.post('/register-nodes-bulk',function(req,res){
	const allNetworkNodes = req.body.allNetworkNodes;
	allNetworkNodes.forEach(networkNodeUrl =>{
		const nodeNotAlreadyPresent = paygrid.networkNodes.indexOf(networkNodeUrl) == -1;
		const notCurrentNode = paygrid.currentNodeUrl !== networkNodeUrl;
		if(nodeNotAlreadyPresent && notCurrentNode)
			paygrid.networkNodes.push(networkNodeUrl);
	});

	res.json({ note: 'Bulk registration successful.' });

});


app.get('/consensus', function(req,res){
	const requestPromise = [];
	paygrid.networkNodes.forEach(networkNodeUrl =>{
		const requestOptions = {
			uri: networkNodeUrl + '/blockchain',
			method: 'GET',
			json: true
		};

		requestPromise.push(rp(requestOptions));
	});

	Promise.all(requestPromise)
	.then(blockchains =>{
		const currentChainLength = paygrid.chain.length;
		let maxChainLength = currentChainLength;
		let newLongestChain = null;
		let newPendingTransactions = null;
		blockchains.forEach(blockchain =>{
			if(blockchain.chain.length > maxChainLength){
				maxChainLength =blockchain.chain.length;
				newLongestChain = blockchain.chain;
				newPendingTransactions = blockchain.pendingTransactions;
			};
		});

		if(!newLongestChain || (newLongestChain && !paygrid.chainIsValid(newLongestChain))){
			res.json({
				note: "Current chain has not been replaced.",
				chain: paygrid.chain
			});

		}else{
			paygrid.chain = newLongestChain;
			paygrid.pendingTransactions = newPendingTransactions;
			res.json({
				note: "This chain has been replaced.",
				chain: paygrid.chain
			});
		};
	});
});



app.get('/block/:blockHash', function(req,res){

	const blockHash = req.params.blockHash;
	const correctBlock = paygrid.getBlock(blockHash);
	res.json({
		block: correctBlock
	});
});


app.get('/transaction/:transaction', function(req,res){
	const transactionId = req.params.transaction;
	const transactionData = paygrid.getTransaction(transactionId);
	res.join({
		transaction: transactionData.transaction,
		block: transactionData.block
	});
});

app.get('/address/:address', function(req,res){
	const address = req.params.address;
	const addressData = paygrid.getAddressData(address);

	res.json({
		addressData: addressData
	});
});


app.get('/block-explorer', function(req,res){
	res.sendFile('./block-explorer/index.html', { root: __dirname });
});


app.listen(port ,function(){
	console.log(`Listening to port number ${port}...`);
});
