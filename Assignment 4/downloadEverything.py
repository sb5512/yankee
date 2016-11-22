import re 
import sys                                                         
from urllib.parse import urlparse 
from urllib.parse import urljoin
from yankee_http_client import downloadArbitaryFileWEB                             

ENCODING = 'utf-8'

def mainDownloadEverythingFunction(commandArguments , totalArg):
    if (totalArg > 1):
        parseHTML(commandArguments[1] , commandArguments[2])
    else:
        print ("Please give valid arguments")
        return
        
def parseHTML(filename , url, content_typeLength=14):
    with open(filename , 'r') as html:
        content = html.read()
        pat = re.compile (r'<img [^>]*src="([^"]+)')
        pat2 = re.compile (r'<link [^>]*href="([^"]+)') # Here we also check from <link href and images inside them
        
        moreimages = pat2.findall(content) 
        moreimagesFiltered = list(filter(lambda x: x.find('.ico') > 0  or x.find('.png') > 0  or x.find('.jpeg') > 0  , moreimages))
        
        img = pat.findall(content)

    allImagesURL = moreimagesFiltered + img 
    toAppendRelativeImageURL = _getPartToAppendToRelativeImageURL(url)
    
    for imageurl in allImagesURL:
        if(imageurl.find('://') > 0):
            downloadArbitaryFileWEB(imageurl)
            #perform download for that url
        else:                                      
            link = urljoin(toAppendRelativeImageURL, imageurl)
            downloadArbitaryFileWEB(link) #perform download for that url
            

# Helper function that returns the front part of the url that is to be appened to relative urls for valid image construction
def _getPartToAppendToRelativeImageURL(url):
    parsed = urlparse(url) 
    try:                                                                       
        host, port = parsed.netloc.split(':')                                  
    except ValueError:                                                         
        host = parsed.netloc
    return parsed.scheme +'://'+ host 
    

#Main Function call alongside command line Argument Handling
totalArg = len(sys.argv) 
commandArguments = sys.argv # Get the arguments list
mainDownloadEverythingFunction(commandArguments , totalArg)