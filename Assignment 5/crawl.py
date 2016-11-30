import re       
import socket    
import numpy as np  
import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt                                            
from urllib.parse import urlparse 
from urllib.parse import urljoin

ENCODING = 'utf-8'
url_to_process = {'http://141.26.208.82/articles/g/e/r/Germany.html' : 0}
url_visited = {}
url_external_internal = {}
url_totalLink = {}


#Helper function that handles socket connection and also gives response in bytes
def _clientConnectAndResponse(url, timeout=10, receive_buffer=8096):
    parsed = urlparse(url)                                                     
    try:                                                                       
        host, port = parsed.netloc.split(':')                                  
    except ValueError:                                                         
        host, port = parsed.netloc, 80                                         

    try: 
        clientSocket = socket.create_connection((host, port), timeout)
    except socket.timeout:
        raise
                        

    method  = 'GET %s HTTP/1.0\r\n\r\n' % parsed.path
    clientSocket.sendall(bytes(method, ENCODING))

    response = [clientSocket.recv(receive_buffer)]                                     
    while response[-1]:                                                        
        response.append(clientSocket.recv(receive_buffer))                             
    
    responseInBytes = b''.join(r for r in response)
    return responseInBytes

    
# Connects to the server and receives response. writes to a file, 
# returns filename , returns None if not 200 OK
def _downloadHTMLToFile(url,content_typeLength=14 ): 
    #Connecting to Server and obtaining responses in Byte format                       
    try:
        responseInBytes = _clientConnectAndResponse(url)
    except:
        return None
    
    headerBytes = responseInBytes[:responseInBytes.find(b'\r\n\r\n')]
    remainingBytes = responseInBytes[responseInBytes.find(b'\r\n\r\n'):]\
                                     .strip(b'\r\n\r\n')

    #Here we check if HTTP responses with 200 OK
    if (headerBytes.find(b'\r\n')) > 0 : 
        if headerBytes[:headerBytes.find(b'\r\n')].decode(ENCODING).lower()\
                       != "http/1.1 200 ok":        
            #print ("Cannot determine if HTTP 200 OK. Further Processing halts")
            return None
    
    # Check if url has a path. This is to extract filename for writing to file.        
    if (urlparse(url).path == ''):
        filename =  url.split('#')[-1]
    else:
        filename =  urlparse(url).path.split('/')[-1]
        
    # Write to a file with name given by filename variable
    try:
        with open(filename, 'wb') as htmlToFile:
            htmlToFile.write(remainingBytes)
            htmlToFile.close()
        return filename
    except IOError as e:
        return None
    

# Helper function used by parseHTMLForLinks to check if url is internal
def _is_internal(urlMain, urlToCheck):
  return urlparse(urlMain).scheme == urlparse(urlToCheck).scheme and\
                    urlparse(urlMain).netloc == urlparse(urlToCheck).netloc
 

# Helper function that returns the front part of the url that is to be 
# appeneded to relative urls for valid image construction
def _getPartToAppendToRelativeLinkURL(url):
    parsed = urlparse(url) 
    try:                                                                       
        host, port = parsed.netloc.split(':')                                  
    except ValueError:                                                         
        host = parsed.netloc
    return parsed.scheme +'://'+ host 
    
   
# obtaines a dictionary of internal and external links for a given url 
# Done by opening the file and extracting all links. Manages unique links
def _parseHTMLForLinks(filename , url, content_typeLength=14):
    externalLinks = set()
    internalLinks = set()
    allLinks = {}
   
    with open(filename , encoding = ENCODING) as html:
        try:
            content = html.read()
        except:
            allLinks['internal'] = internalLinks
            allLinks['external'] = externalLinks
            return allLinks
        pat = re.compile ('<a href="?\'?([^"\'>]*)')
        linksInAHref = pat.findall(content)
            
    toAppendRelativeLinkURL = _getPartToAppendToRelativeLinkURL(url)    
    for linkInAHref in linksInAHref:
        if(linkInAHref.find('://') < 0):
            
            #We have a relative link. So need to modify link
            link = urljoin(toAppendRelativeLinkURL, linkInAHref)
            
            internalLinks.update([link])
        else:
            if _is_internal(url,linkInAHref ):
                internalLinks.update([linkInAHref])
            else:
                externalLinks.update([linkInAHref])
    
    allLinks['internal'] = internalLinks
    allLinks['external'] = externalLinks
    return allLinks

# Used by process_UrlBFS to obtain all the link for a given url. Uses 
# two helper function to download html to file and also parse html to get links
def getAllLinksForThisURL(url):
    #making sure all links obtained inside from the url is unique
    links = {'internal' : {} , 'external':{}}
    
    fileLocation = _downloadHTMLToFile(url)
    if fileLocation is not None:
        links = _parseHTMLForLinks(fileLocation,url)  
       
    return links
 
# Here we obtain the URL from global variable and start the URL crawling. 
def process_urlBFS():
    totalLinks = 0
    totalPages = 0
    while(url_to_process):
        key , value  = url_to_process.popitem()
        # Lets process the url to get more url links. 
        # Also download the html file for this url. Returns all link info
        receivedInternalExternalLinks = getAllLinksForThisURL(key)
        
        url_totalLink[key] = len(receivedInternalExternalLinks['internal']) +\
                                 len(receivedInternalExternalLinks['external'])
        
        #This will be used to calculate pages as we take 200 ok link as pages.
        url_visited[key] = url_totalLink[key]
        
        #key as url associated to values tuple i.e (internal, external)    
        url_external_internal[key] = (len(receivedInternalExternalLinks['internal'\
                                            ]),len(receivedInternalExternalLinks\
                                            ['external']))
        
        totalLinks = totalLinks + len(receivedInternalExternalLinks['internal'])\
                                          + len(receivedInternalExternalLinks\
                                          ['external'])
        allInternalReceivedURLLinks = receivedInternalExternalLinks['internal']
         
        
        for receivedURLLink in allInternalReceivedURLLinks:                
                # check if contains in url_visited. Add to process queue
                if (receivedURLLink not in url_visited): 
                    url_to_process[receivedURLLink] = 0

    totalPages = len([x for x in url_visited.values() if x != 0])
    #badPages404 = len([x for x in url_visited.values() if x == 0])
    print ("\nPhase I")
    print("\nTotal Number of webpages we found : " , totalPages)
    print("\nTotal Number of links we encountered :" , totalLinks)
   
    average = totalLinks / totalPages
    print("\nAverage number of links per web page : ", average )
    print ("\nMedian number of links per web page : ", \
                                               calculateMedian(url_totalLink))
    drawHistogram(url_totalLink)
    print ("\nPhase II")
    drawScatterDiagram(url_external_internal)
    
def calculateMedian(url_totalLink):
    medianValue = (np.median(list(url_totalLink.values())))
    return medianValue 

def drawHistogram(url_totalLink):
    x_1 = np.array(list(url_totalLink.values()))
    plt.figure(figsize=(7,5))
    plt.hist(x_1 , bins= range(min(x_1), 150, 5))
    plt.xlabel("Number of Links per page (Each bar i.e. 0-5, 5-10, ...)")
    plt.ylabel("Frequencies")    
    plt.show()

def drawScatterDiagram(url_external_internal):
    #preparing data for plotting
    tuple_internal_external = list(url_external_internal.values())
    internal = [x[0] for x in tuple_internal_external]
    external = [x[1] for x in tuple_internal_external]
    #print ("mero internal lsit : " , internal )
    #print ("mero external lsit : " , external )
    df1 = pd.DataFrame(index=range(len(internal)), columns=["URL" , \
                                           "Number Of Internal Links",\
                                           "Number Of External Links"])
    df1["URL"] = url_external_internal.keys()
    df1["Number Of Internal Links"] = internal
    df1["Number Of External Links"] = external
    print(df1)
    sns.lmplot(x="Number Of Internal Links", y="Number Of External Links"\
                                                   , data=df1, fit_reg=False)    
    
def mainFunction():
    process_urlBFS()
    print('done')


    
if __name__ == "__main__":
    mainFunction()
 