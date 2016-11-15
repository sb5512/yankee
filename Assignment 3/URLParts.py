# Class for URL to parts
class URLParts():
    def __init__(self):
        print ('-- You are no Using Team Yankees URL SPLITTER -- ')
        
    def splitURL(self, urlFromClient):
        
        url = urlFromClient[:urlFromClient.find('\\r')]
        
        PROTOCOLCHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        protocol = port = domain = subdomain = path = parameter = fragment = ''
        
        protocolEnd = url.find(':/')
        if (protocolEnd > 0):
            for urlChar in url[:protocolEnd]:
                if urlChar not in PROTOCOLCHARS:
                    break
            else:
                protocol = url[:protocolEnd].lower()
                restUrl = url[protocolEnd:].lstrip(':/')
        
        if not protocol:
            restUrl = url
        
        posPath = restUrl.find('/')
        posParameter = restUrl.find('?')
        posFrag = restUrl.find('#')
        if posPath > 0:
            if posParameter > 0 and posFrag > 0:
                domainSubPort = restUrl[:posPath]
                path = restUrl[posPath:min(posParameter, posFrag)]
            elif posParameter > 0:
                if posParameter > posPath:
                    domainSubPort = restUrl[:posPath]
                    path = restUrl[posPath:posParameter]
                else:
                    domainSubPort = restUrl[:posParameter]
                    path = '' 
            elif posFrag > 0:
                domainSubPort = restUrl[:posPath]
                path = restUrl[posPath:posFrag]
            else:
                domainSubPort = restUrl[:posPath]
                path = restUrl[posPath:]
        else:
            if posParameter > 0:
                domainSubPort = restUrl[:posParameter]
            elif posFrag > 0:
                domainSubPort = restUrl[:posFrag]
            else:
                domainSubPort = restUrl   
        
        if posParameter > 0:
            if posFrag > 0:
                parameter = restUrl[posParameter+1:posFrag]
            else:
                parameter = restUrl[posParameter+1:]
        if posFrag > 0:
            fragment = restUrl[posFrag+1:]
        if not protocol:
            path = domainSubPort + path
            domainSubPort = ''  
               
        url[protocolEnd:].lstrip(':/')
        
        subdomain = domainSubPort[:domainSubPort.find('.')]
        domainPort = domainSubPort[domainSubPort.find('.'):].lstrip('.')
        domain = domainPort[:domainPort.find(':')]
        port = domainPort[domainPort.find(':'):].lstrip(':')
        
         
        returnURLParts ={}
        returnURLParts['Protocol']= protocol
        returnURLParts['Domain']= domain
        returnURLParts['SubDomain']= subdomain
        returnURLParts['Port']= port
        returnURLParts['Path']= path
        returnURLParts['Parameter']= parameter
        returnURLParts['Fragment']= fragment
        return (returnURLParts)