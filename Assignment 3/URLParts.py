# Class for URL to parts
class URLParts():
    def __init__(self):
        print ('-- You are now Using Team Yankees URL SPLITTER -- ')
        
    def splitURL(self, urlFromClient):
        
        url = urlFromClient # [:urlFromClient.find('\\r')]
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
        print (posPath)
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
                print (path)
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
            #path = domainSubPort + path
            domainSubPort = ''  
               
        if (domainSubPort.find(':') != -1):
            port = domainSubPort[domainSubPort.find(':'):].lstrip(':')
        else:
            port = 'None'
        
        if (domainSubPort.find(':') > 0):
            domainSub = domainSubPort[:domainSubPort.find(':')]
        else:
            domainSub = domainSubPort
        
        domain = [domainSub] 
        while domainSub.find('.') != -1 :
            domainSub = domainSub[domainSub.find('.'):].lstrip('.')
            domain.append(domainSub)
        
        # Removing last element in domain list as all subdomain are domains.
        subdomain = domain[:]
        subdomain.pop()
        domainString = ''
        for domainVal in domain :
            if domainVal != domain[-1]:
                 domainString = domainString + domainVal + ' & '
            else:
                domainString = domainString + domainVal
                
        subDomainString = ''
        for subDomainVal in subdomain :
            if subDomainVal != subdomain[-1]:
                subDomainString = subDomainString + subDomainVal + ' & '
            else:
                subDomainString = subDomainString + subDomainVal
                
        returnURLParts ={}
        returnURLParts['Protocol'] = protocol
        returnURLParts['Domain']= domainString
        returnURLParts['SubDomain']= subDomainString
        returnURLParts['Port']= port
        returnURLParts['Path']= path
        returnURLParts['Parameter']= parameter
        returnURLParts['Fragment']= fragment
        print (returnURLParts)
        return (returnURLParts)
        
urlpar = URLParts()
urlpar.splitURL("www.example.com/")