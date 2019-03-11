import urllib.request
#import connectionScript 
import json
import random
import os
from tkinter import messagebox
from tkinter import *

authenticNode = ""
master = Tk()
#w = Canvas(master, width=600, height=400) 
master.title('No Name Normies ')

connected_nodes = []
trust_values = {}


background_image=PhotoImage(file = "C:\\Users\\snaru\\Desktop\\nonamenormies\\pythonScripts\\logo1.png")
background_label = Label(master, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)



def checkConnectivity():
    nodes = ["http://192.168.43.117:3001/", "http://192.168.43.117:3002/", "http://192.168.43.117:3003/", "http://192.168.43.117:3004/", "http://192.168.43.117:3005/"]

    for node in nodes:
        response = os.system("curl -I " + node)

        if response == 0:
            #pingStatus = True
            connected_nodes.append(node[:-1])
        #else:
            #pingStatus = False

    #return pingStatus

#nodes = ["http://192.168.43.117:3001", "http://192.168.43.117:3002", "http://192.168.43.117:3003", "http://192.168.43.117:3004", "http://192.168.43.117:3005"]

checkConnectivity()
#trust_values = { i : 0 for i in connected_nodes }

w = Label(master, text="PayGrid: Payments made simpler", font=("Helvetica",16), fg="red").grid(column=1,pady=30)
#w.pack(fill=X,pady=30)


fields = ['Amount', 'Sender', 'Recipient']

textSender = Label(text='Sender', relief=RIDGE, width=15).grid(row=2,column=0)
sender=StringVar()
inputSender = Entry(master,relief=SUNKEN,width=100,textvariable=sender)
inputSender.grid(row=2,column=1,padx=30,pady=10)

textRecipient=Label(text='Recipient', relief=RIDGE, width=15).grid(row=3,column=0)
recipient=StringVar()
inputRecipient=Entry(master,relief=SUNKEN,width=100,textvariable=recipient)
inputRecipient.grid(row=3,column=1,padx=30,pady=10)

textAmount=Label(text='Amount', relief=RIDGE, width=15).grid(row=4,column=0)
amount=IntVar()
inputAmount=Entry(master,relief=SUNKEN,width=100,textvariable=amount)
inputAmount.grid(row=4,column=1,padx=30,pady=10)

"""
textAmount=Label(text='Amount', relief=RIDGE, width=15).grid(row=5,column=0)
amount=IntVar()
inputAmount=Entry(master,relief=SUNKEN,width=100,textvariable=amount)
inputAmount.grid(row=5,column=1,padx=30,pady=10)

textPrice=Label(master,text='Price', relief=RIDGE, width=15).grid(row=6,column=0)
price=IntVar()
inputPrice=Entry(master,relief=SUNKEN,width=100,textvariable=price)
inputPrice.grid(row=6,column=1,padx=30,pady=10)
"""

def Send():
    node = random.choice(connected_nodes)
    sender = inputSender.get()
    recipient= inputRecipient.get()
    amount=inputAmount.get()


    body = {'node':node,
            'sender': sender,
            'recipient': recipient,
            'amount': amount
            }

    #print (body)        
    myurl = node+"/transaction/broadcast"
    #authenticNode = node
    req = urllib.request.Request(myurl)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))

    #print (jsondataasbytes)
    response = urllib.request.urlopen(req, jsondataasbytes)
    if response.getcode() == 404:
        messagebox.showinfo("Msg", "Transaction not possible")
    elif response.getcode() == 200:
        messagebox.showinfo("Msg", "Transaction recorded")
    #print (response)
    #print (node + " \n" + name + " \n" + buyer + "\n" + seller + "\n" + amount + "\n" + price )
"""
shivam = "shivam"
def testHello():
    print (shivam)
"""

def Reset():
    inputSender.delete(0, END)
    inputRecipient.delete(0, END)
    inputAmount.delete(0,END)

def View():
    node = random.choice(connected_nodes)
    url = node + "/blockchain"   
    r = urllib.request.urlopen(url) 
    data = json.load(r)
    print (data['chain'])
    


    
send = Button(master, text = ("Make Transaction"), command = Send)
reset = Button(master, text = ("Reset Values"), command = Reset)
view = Button(master, text = ("View Blockchain"), command = View)
send.grid(row = 6, column=1,pady=5)
reset.grid(row =7, column =1,pady=5)
view.grid(row =8, column =1,pady=5)


#trustValue()
#trustRanking(103)
#buttons()
mainloop()
