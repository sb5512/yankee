from jsonSocket import Server
import json
from URLParts import URLParts 

host = 'localhost'
port = 8080

server = Server(host, port)  # Server Class is obtained from jsonSocket Library
server.accept()

#Receives data from client
data = server.recv()
data = json.loads(data.decode())

print ('Received URL : ' , data['URL'])

#Here we use our URLParts class to use the function splitURL to get split data
urlToParts = URLParts()
dataURLParts = urlToParts.splitURL(data['URL'])

#Editing the obtained Json formatted data from client
formattedText = "\n"
formattedText = formattedText + \
        'Protocol' + " : " + dataURLParts['Protocol'] +"\n" + \
        'Domain'  +" : " + dataURLParts['Domain'] +"\n" + \
        'SubDomain' + " : " + dataURLParts['SubDomain'] +"\n" + \
        'Port'  +" : " + dataURLParts['Port'] +"\n" + \
        'Path' + " : " + dataURLParts['Path'] +"\n" + \
        'Parameter'  +" : " + dataURLParts['Parameter'] +"\n" + \
        'Fragment' + " : " + dataURLParts['Fragment'] +"\n";

# Please note the following code could be done to omit hard coding. However
# with the below code the order was not achieved while printing

#formattedText = ""
#for key, value in data.items():
#     formattedText = formattedText + key + ":" + value +"\n";

# Now we encode the string and send to client for printing
server.send(formattedText.encode()).close()

