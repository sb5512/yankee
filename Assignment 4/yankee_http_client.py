import socket   
import sys                                                               
from urllib.parse import urlparse                                       

ENCODING = 'utf-8'

#takes command line arguments and performs downloading files
def mainFunction(commandArguments , totalArg):
    if (totalArg > 1):
        downloadArbitaryFileWEB(commandArguments[1])
    else:
        print ("\n Invaild URL -- Default URL shown below will be used : " +  
        "\n http://west.uni-koblenz.de/en/studying/courses/ws1617/" + 
        "introduction-to-web-science \n\n")
        downloadArbitaryFileWEB("http://west.uni-koblenz.de/en/studying/" +
        "courses/ws1617/introduction-to-web-science")
        
        
#Connects to the server and receives response. writes to a file 
def downloadArbitaryFileWEB(url , content_typeLength=14):
    #Connecting to Server and obtaining responses in Byte format                       
    responseInBytes = _clientConnectAndResponse(url)
    
    headerBytes = responseInBytes[:responseInBytes.find(b'\r\n\r\n')]
    remainingBytes = responseInBytes[responseInBytes.find(b'\r\n\r\n'):]\
                                     .strip(b'\r\n\r\n')

    #Here we check if HTTP responses with 200 OK
    if (headerBytes.find(b'\r\n')) > 0 : 
        if headerBytes[:headerBytes.find(b'\r\n')].decode(ENCODING).lower()\
                       != "http/1.1 200 ok":        
            print ("Cannot determine if HTTP 200 OK. Further Processing halts")
            return
    
    #Display Header
    print('\n')
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
    

#Helper function that handles socket connection and also gives response in bytes
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

#Takes headerBytes and checks if response from server was an image file or not
def _checkIfImage (headerBytes, content_typeLength):
    if (headerBytes.find(b'Content-Type:') >= 0):
        headerBytesAfterContentType = headerBytes[headerBytes.find\
                                                  (b'Content-Type:'):]
    else:
        print ("DOESNOT HAVE A CONTENT TYPE")
        raise ValueError('No Content Type in header File')
    if (headerBytesAfterContentType.find(b';') >= 0):
        fileFormat = headerBytesAfterContentType[:headerBytesAfterContentType\
                                                 .find(b';')]
    else:
        fileFormat = headerBytesAfterContentType
    #print (fileFormat.decode(ENCODING))
    fileFormatStrip = fileFormat.decode(ENCODING)[content_typeLength:]
   
    if fileFormatStrip.lower().find('image/') >= 0:  
        return True
    return False

if __name__ == "__main__":
     #Main Function call alongside command line Argument Handling
     totalArg = len(sys.argv) 
     commandArguments = sys.argv # Get the arguments list
     mainFunction(commandArguments , totalArg)
