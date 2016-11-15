from jsonSocket import Client
import json

host = 'localhost'
port = 8080

# Client code:
client = Client()  # Client Class is obtained from jsonSocket Library
data ={}
url = input("Please Enter your URL :")
data['URL']= url

#collects data and converts to Json and sends to the Server
client.connect(host, port).send(json.dumps(data).encode())

#Gets response from server
response = client.recv()

print ("\n \n Received from Server \n \n" , response.decode())
client.close()