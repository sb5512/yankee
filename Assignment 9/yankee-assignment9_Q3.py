import pandas as pd

# we get all paths from a given start node to the end node , it returns 
# the lists of path 
def get_all_path_from_start_end(start_node, end_node, graph_dict , path=[]):
    path = path + [start_node]
    try: 
        if start_node == end_node:
            return [path]
    except:
        return [path]
    if start_node not in graph_dict:
        return []
    
    paths = []    
    for outlink in graph_dict[start_node]:
        if outlink not in path:
            related_paths = get_all_path_from_start_end(outlink, 
                                                     end_node, graph_dict, 
                                                     path)
            for p in related_paths: 
                paths.append(p)
    return paths
        
# calculates the diameter of a graph i.e. the longest shortest path in the graph. 
def diameter_for_our_graph(graph_dict):       
    v = list(graph_dict.keys())
    pairs = {i+j :(v[i],v[j]) for i in range(len(v)-1) \
                                                   for j in range(i+1, len(v))}
    
    smallest_paths = []

    # This part is just to check for one pair i.e. for start and end vertex pair.    
    #singleExtractdict = {}
    #key , value = pairs.popitem()
    #singleExtractdict[key] = value
    # Testing

    for (start,end) in pairs.values(): #to be changed to pairs for singleExtractdict
        paths = get_all_path_from_start_end(start,end , graph_dict)
        
        if (len(paths) > 0):
            smallest = sorted(paths, key=len)[0]            
            smallest_paths.append(smallest)

    if len(smallest_paths) > 0:
        smallest_paths.sort(key=len)
        diameter = len(smallest_paths[-1]) - 1
        return diameter
    return 0        

# Helper function that changes particular list into numeric starting from 1.
def _changeToNumbers(toChangeListToNumber):
        changedList = []
        for value in toChangeListToNumber[0]:
            if value in newG:
                changedList.append(newG[value])
        return changedList
        
if __name__ == "__main__":
    store = pd.HDFStore("store.h5")#read .h5 file 
    df2=store['df2']    
       
    # Dictionary of article names and its associated article text in list form
    dict_df2 = df2.set_index('name').T.to_dict('list')
    articles_list_ofoutlinks = dict_df2
    
    # Here we convert each unique string into unique numbers and create the 
    # dictionary accordingly as numeric comaprisons are each computations.
    newG = {}
    for index, key in enumerate(articles_list_ofoutlinks):
        newG[key] = index    
        
    updatedGraph = {}
    for key, value in articles_list_ofoutlinks.items():
        newKey = newG[key]
        newValue = _changeToNumbers(value)
        updatedGraph[newKey] = newValue 
    
    print("The diameter of our graph is := " , \
                                          diameter_for_our_graph(updatedGraph))
    