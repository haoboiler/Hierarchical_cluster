import numpy

lang_dict = {'aao':'UD_Arabic-NYUAD', 'cop':'UD_Coptic-Scriptorium', 
'heb':'UD_Hebrew-HTB', 'bxr':'UD_Buryat-BDT', 'eus':'UD_Basque-BDT', 
'afr':'UD_Afrikaans-AfriBooms', 'dan':'UD_Danish-DDT', 'deu':'UD_German-GSD', 
'eng':'UD_English-EWT', 'got':'UD_Gothic-PROIEL', 'nob':'UD_Norwegian-Bokmaal', 
'nld':'UD_Dutch-Alpino', 'nno':'UD_Norwegian-Nynorsk', 'swe':'UD_Swedish-Talbanken', 
'bel':'UD_Belarusian-HSE', 'bul':'UD_Bulgarian-BTB', 'ces':'UD_Czech-PDT', 
'chu':'UD_Old_Church_Slavonic-PROIEL', 'hrv':'UD_Croatian-SET', 'hsb':'UD_Upper_Sorbian-UFAL', 
'lit':'UD_Lithuanian-HSE', 'lav':'UD_Latvian-LVTB', 'pol':'UD_Polish-LFG', 
'rus':'UD_Russian-SynTagRus', 'slk':'UD_Slovak-SNK', 'slv':'UD_Slovenian-SSJ', 
'srp':'UD_Serbian-SET', 'ukr':'UD_Ukrainian-IU', 'cat':'UD_Catalan-AnCora', 'spa':'UD_Spanish-AnCora', 
'fra':'UD_French-GSD', 'fro':'UD_Old_French-SRCMF', 'glg':'UD_Galician-TreeGal', 'ita':'UD_Italian-ISDT', 
'lat':'UD_Latin-PROIEL', 'por':'UD_Portuguese-Bosque', 'ron':'UD_Romanian-RRT', 'fas':'UD_Persian-Seraji', 
'hin':'UD_Hindi-HDTB', 'kmr':'UD_Kurmanji-MG', 'mar':'UD_Marathi-UFAL', 'urd':'UD_Urdu-UDTB', 
'ell':'UD_Greek-GDT', 'grc':'UD_Ancient_Greek-PROIEL', 'gle':'UD_Irish-IDT', 'hye':'UD_Armenian-ArmTDP', 
'ind':'UD_Indonesian-GSD', 'jpn':'UD_Japanese-GSD', 'kor':'UD_Korean-Kaist', 'kaz':'UD_Kazakh-KTB', 
'tur':'UD_Turkish-IMST', 'uig':'UD_Uyghur-UDT', 'est':'UD_Estonian-EDT', 'fin':'UD_Finnish-FTB', 
'hun':'UD_Hungarian-Szeged', 'sme':'UD_North_Sami-Giella', 'tam':'UD_Tamil-TTB', 'tel':'UD_Telugu-MTG', 
'vie':'UD_Vietnamese-VTB', 'zho':'UD_Chinese-GSD'}

class cluster:
    def __init__(self, vector, cluster_list = None, id = None):
        self.clist = cluster_list
        self.vector = vector 
        self.id = id     

    def __str__(self, level = 0):
        ret = "\t"*level + lang_dict[self.id]+"\n"
        for child in self.clist:
            ret += child.__str__(level+1)
        return ret

def get_distance(vector_a, vector_b):
    '''
    Input: 2 vectors
    Output: Distance(Euclidean) between two vector
    '''

    distance = numpy.linalg.norm(vector_a - vector_b)
    return distance

def get_vector(node_list):
    '''
    Input: list of nodes
    Output: average vector
    '''
    new_vector = node_list[0].vector
    
    length = len(node_list)
    for i in range(length-1):
        new_vector += node_list[i+1].vector
    new_vector = new_vector/length
    
    return new_vector

def merge_cluster(cluster_list, threshold = 1):
    '''
    Merge some cluster to one
    '''
    min_distance = 100000
    cluster_node = []
    for node in cluster_list:
        for other_node in cluster_list:
            if node != other_node:
                dis = get_distance(node.vector, other_node.vector)
                if dis < min_distance:
                    min_distance = dis
                    cluster_node = [node, other_node]
    
    new_vector = get_vector(cluster_node)
    new_cluster_list = []
    flag = 0
    for node in cluster_list:
        if node not in cluster_node:
            dis = get_distance(node.vector, new_vector)
            if dis < threshold:
                cluster_node.append(node)
                flag += 1
            else:
                new_cluster_list.append(node)

    new_vector = get_vector(cluster_node)
    new_node = cluster(new_vector, cluster_node, cluster_node[0].id)

    new_cluster_list.append(new_node)
    print('merge ' + str(flag)+' nodes')
    return new_cluster_list


def get_nodes(file_path):
    '''
    Input the file path
    Ouput: 17, 17**2, 17**3 length vector
    '''
    file = open(file_path, 'r')
    file_list = []
    line = file.readline()
    while(line):
        line = line.split(':')
        key = line[0]
        vector = line[1]
        vector = vector[:-1].split(', ')
        for i in range(len(vector)):
            vector[i] = float(vector[i])
        vector = numpy.array(vector)
        #file_dict[key] = vector
        cluster_node = cluster(vector,[],key)
        file_list.append(cluster_node)
        line = file.readline()
    return file_list



def main():
    cluster_list = get_nodes('lang_vector.txt')
    print(len(cluster_list))
    threshold = 0.3
    while(len(cluster_list)>1):
        cluster_list = merge_cluster(cluster_list,threshold)
        threshold = threshold + 0.3
        print(len(cluster_list))
    str(cluster_list[0])
    print(cluster_list[0])


if __name__ == '__main__':
    main()