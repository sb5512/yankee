from jsonSocket import Server
import json

host = 'localhost'
port = 8080

server = Server(host, port)  # Server Class is obtained from jsonSocket Library
server.accept()
#Receives data from client
data = server.recv()
data = json.loads(data.decode())

#Editing the obtained Json formatted data from client
formattedText = "\n"
formattedText = formattedText + 'Name' + " : " + data['Name'] +"\n" + 'Age'  +" : " + data['Age'] +"\n" + 'Matrikelnummer' + " : " + data['Matrikelnummer'] +"\n";

# Please note the following code could be done for hard coding removal. However
# with it the order was not achieved while printing

#formattedText = ""
#for key, value in data.items():
#     formattedText = formattedText + key + ":" + value +"\n";

# Now we encode the string and send to client for printing
server.send(formattedText.encode()).close()




