import re                                                          
from urllib.parse import urlparse 
from urllib.parse import urljoin
from yankee_http_client import downloadArbitaryFileWEB                             

ENCODING = 'utf-8'



def mainFunction(commandArguments , totalArg):
    if (totalArg > 1):
        parseHTML(commandArguments[1] , commandArguments[2])
    else:
        ## TESTINGGGGGGGGGGg
        #parseHTML(commandArguments[1] , commandArguments[2])
        parseHTML("index.html" , "http://west.uni-koblenz.de/en/studying/courses/ws1617/introduction-to-web-science")
        #print ("Please give valid arguments")
        return
        
def parseHTML(filename , url, content_typeLength=14):
    with open('index.php') as html:
        content = html.read()
        pat = re.compile (r'<img [^>]*src="([^"]+)')
        pat2 = re.compile (r'<link [^>]*href="([^"]+)')
         
        moreimages = pat2.findall(content)
        print (moreimages)
        moreimagesFiltered = list(filter(lambda x: x.find('.ico') > 0  or x.find('.png') > 0  or x.find('.jpeg') > 0  , moreimages))
        
        img = pat.findall(content)

    #print (moreimagesFiltered)
    allImagesURL = moreimagesFiltered + img 
    #print (allImagesURL)
    toAppendRelativeImageURL = getPartToAppendToRelativeImageURL(url)
    
    for imageurl in allImagesURL:
        if(imageurl.find('://') > 0):
            print ("oh yeah there it is")
            downloadArbitaryFileWEB(imageurl)
            #perform download for that url
        else:
            print ("nope")                                      
            link = urljoin(toAppendRelativeImageURL, imageurl)
            downloadArbitaryFileWEB(link)
            #perform download for that url
    #print(link)

def getPartToAppendToRelativeImageURL(url):
    parsed = urlparse(url) 
    try:                                                                       
        host, port = parsed.netloc.split(':')                                  
    except ValueError:                                                         
        host = parsed.netloc
    return parsed.scheme +'://'+ host 
    
mainFunction(" " , 0)