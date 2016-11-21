import socket   
import sys                                                               
from urllib.parse import urlparse                                       

ENCODING = 'utf-8'

def mainFunction(commandArguments , totalArg):
    if (totalArg > 1):
        downloadArbitaryFileWEB(commandArguments[1])
    else:
        print ("\n Invaild URL -- Default URL shown below will be used : " + "\n http://west.uni-koblenz.de/en/studying/courses/ws1617/introduction-to-web-science \n\n")
        downloadArbitaryFileWEB("http://west.uni-koblenz.de/en/studying/courses/ws1617/introduction-to-web-science")
        #downloadArbitaryFileWEB("http://west.uni-koblenz.de/sites/default/files/styles/personen_bild/public/_IMG0076-Bearbeitet_03.jpg")
        #downloadArbitaryFileWEB("http://west.uni-koblenz.de/sites/default/files/styles/personen_bild/public/aboutus/team/persons/korok-sengupta.jpg?itok=O4OB0OyU")

def downloadArbitaryFileWEB(url , content_typeLength=14):
    #Connecting to Server and obtaining responses in Byte format                        
    responseInBytes = _clientConnectAndResponse(url)
    
    headerBytes = responseInBytes[:responseInBytes.find(b'\r\n\r\n')]
    remainingBytes = responseInBytes[responseInBytes.find(b'\r\n\r\n'):].strip(b'\r\n\r\n')
    print (headerBytes)
    #print (remainingBytes)
    #Here we check if HTTP responses with 200 OK
    if (headerBytes.find(b'\r\n')) > 0 : 
        if headerBytes[:headerBytes.find(b'\r\n')].decode(ENCODING).lower() != "http/1.1 200 ok":        
            print ("Cannot determine if HTTP 200 OK. Further Processing wont occur")
            return
    
    #Display Header
    print (headerBytes.decode(ENCODING)) 
    
    #checking if the URL is for an image
    isImage = _checkIfImage(headerBytes , content_typeLength)
    headerFile = open('index.php.header' , 'w', newline='\n')
    headerFile.write(headerBytes.decode(ENCODING))
    
    if isImage:
        imageToFile = open(urlparse(url).path.split('/')[-1], 'wb')
        imageToFile.write(remainingBytes)
        imageToFile.close()
    else:
        htmlToFile = open('index.php', 'wb')
        htmlToFile.write(remainingBytes)
        htmlToFile.close()
    


def _clientConnectAndResponse(url, timeout=10, receive_buffer=8096):
    parsed = urlparse(url)                                                     
    try:                                                                       
        host, port = parsed.netloc.split(':')                                  
    except ValueError:                                                         
        host, port = parsed.netloc, 80                                         

    clientSocket = socket.create_connection((host, port), timeout)                     

    method  = 'GET %s HTTP/1.0\r\n\r\n' % parsed.path
    clientSocket.sendall(bytes(method, ENCODING))

    response = [clientSocket.recv(receive_buffer)]                                     
    while response[-1]:                                                        
        response.append(clientSocket.recv(receive_buffer))                             
    
    responseInBytes = b''.join(r for r in response)
    return responseInBytes

    
def _checkIfImage (headerBytes, content_typeLength):
    if (headerBytes.find(b'Content-Type:') >= 0):
        headerBytesAfterContentType = headerBytes[headerBytes.find(b'Content-Type:'):]
    else:
        print ("DOESNOT HAVE A CONTENT TYPE")
        raise ValueError('No Content Type in header File')
    if (headerBytesAfterContentType.find(b';') >= 0):
        fileFormat = headerBytesAfterContentType[:headerBytesAfterContentType.find(b';')]
    else:
        fileFormat = headerBytesAfterContentType
    #print (fileFormat.decode(ENCODING))
    fileFormatStrip = fileFormat.decode(ENCODING)[content_typeLength:]
    #print (fileFormatStrip)
    if fileFormatStrip.lower() in ('image/png', 'image/jpeg', 'image/gif'):
        return True
    return False

    
#Argument Handling
totalArg = len(sys.argv)
# Get the arguments list 
commandArguments = str(sys.argv)
# Print arguments
print ("The total numbers of args passed to the script: %d " % totalArg)
print ("Args list: %s " % commandArguments)

mainFunction(commandArguments , totalArg)

#geturl('http://west.uni-koblenz.de/en/studying/courses/ws1617/introduction-to-web-science')
#geturl('http://west.uni-koblenz.de/sites/default/files/styles/personen_bild/public/_IMG0076-Bearbeitet_03.jpg')