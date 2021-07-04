# import

import pandas as pd
import copy
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm
import difflib as dl
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from util.config import *


class SyllabusKG:

    def __init__(self, syllabus, subject, total_marks=120):
        self.syllabus = syllabus
        self.subject = subject
        self.total_marks = total_marks

        self.dataframe = self.createDataFrame()


    def createDataFrame(self):
        file = open(self.syllabus,'r')
        text = file.read()
        text = text.replace('\xad', ' ')
        l = text.split("\n")
        syl = pd.DataFrame(l)
        csyl = copy.deepcopy(syl)
        
        for i in range(len(syl)):
            csyl[0][i] = csyl[0][i].split(",")
            syl[0][i] = csyl[0][i][0]
        time = []
        for i in range(len(syl)):
            csyl[0][i].pop(0)
            time.append(csyl[0][i].pop(len(csyl[0][i])-1))

        syl[1] = csyl[0]
        temp = pd.DataFrame(time)
        syl[2] = temp[0]

        syl.rename(columns={0:'Module',1:'Topic',2:'Weightage'}, inplace=True)
        syl['Weightage'] = syl['Weightage'].astype(int)
        syl['Weightage'] = syl['Weightage']*self.total_marks/syl['Weightage'].sum()

        for i in range(len(syl)):
            for j in range(len(syl['Topic'][i])):
                syl['Topic'][i][j] = syl['Topic'][i][j].split("+")
        
        self.dataframe = syl


    def buildKnowledgeGraph(self):
        self.G = nx.DiGraph(edge_attr = True)
        self.G.add_node(self.subject, node_bucket= 0, 
            overflow_bucket= 0, max_marks = self.total_marks) 

        for i in range(len(self.dataframe)):
            self.G.add_node(self.dataframe['Module'][i], node_bucket= 0, 
                overflow_bucket= 0, max_marks = int(self.dataframe['Weightage'][i]))
            self.G.add_edge(subject, self.dataframe['Module'][i])


        for i in range(len(self.dataframe)):
            for j in range(len(self.dataframe['Topic'][i])):
                for k in range(len(self.dataframe['Topic'][i][j])):
                    self.G.add_node(self.dataframe['Topic'][i][j][k], 
                        node_bucket= 0, overflow_bucket= 0, max_marks = 10)
                    self.G.add_edge(self.dataframe['Topic'][i][j][0], 
                        self.dataframe['Topic'][i][j][k])
                    self.G.add_edge(self.dataframe['Module'][i], 
                        self.dataframe['Topic'][i][j][0])

        self.G.remove_edges_from(nx.selfloop_edges(self.G))
        
        return self.G


    # Plot Graph
    def plotGraph(self):
        options = {
            'node_color': 'orange',
            'node_size': 1000,
            'width': 0.5,
            'arrowstyle': '-|>',
            'arrowsize': 5,
        }

        plt.figure(figsize=(15,10))

        pos = nx.planar_layout(self.G)
        nx.draw(self.G, pos, arrows=True, with_labels = True, **options)
        plt.show()


    def exportGraph(self):
        nx.write_gpickle(self.G, self.subject+'_graph.gpickle')

        
    # Import graph from Pickle
    def importGraph(self):
        self.G = nx.read_gpickle(self.subject+'_graph.gpickle')
        return self.G
        

    def setPredAndSucc(self):
        self.pred = dict(nx.bfs_predecessors(self.G, self.subject))
        self.succ = dict(nx.bfs_successors(self.G, self.subject))
        

    def handleOverflow(self, node, child=False):
        
        if node == self.subject:
            layer1= list(self.G.successors(node))
            self.G.nodes[node]['overflow_bucket'] = 0
            self.G.nodes[node]['node_bucket'] = 0
            
            for x in layer1:
                self.G.nodes[node]['overflow_bucket'] += (self.G.nodes[x]['overflow_bucket'])
                self.G.nodes[node]['node_bucket'] += (self.G.nodes[x]['node_bucket'])
                
            return
        
        if child:
            self.G.nodes[node]['node_bucket'] += (
                self.G.nodes[child]['node_bucket'] + self.G.nodes[child]['overflow_bucket'])
        
        if self.G.nodes[node]['node_bucket'] > self.G.nodes[node]['max_marks']:
            self.G.nodes[node]['overflow_bucket'] += (
                G.nodes[node]['node_bucket'] - self.G.nodes[node]['max_marks'])
            self.G.nodes[node]['node_bucket'] = self.G.nodes[node]['max_marks']

        self.handle_overflow(self.pred[node], node)
        

    def parse(self, question_paper_df, threshold=70):
        
        self.set_pred_succ()
        
        identified_node = []
        
        for i in range(len(question_paper_df['Extracted Keywords'])):
            fsim=0
            
            for j in list(self.G.nodes):
                s = dl.SequenceMatcher(None, question_paper_df['Extracted Keywords'][i], j)
                sim3 = s.ratio()*100
                sim1 = fuzz.token_sort_ratio(question_paper_df['Extracted Keywords'][i], j) 
                sim2 = fuzz.partial_ratio(question_paper_df['Extracted Keywords'][i], j)
                sim = max(sim1,sim2,sim3)
                
                if sim>fsim:
                    fsim=sim
                    fnode=j
            
            if fsim > threshold:
                identified_node.append(fnode)
                self.G.nodes[fnode]['node_bucket'] = question_paper_df['Marks'][i]
                self.handle_overflow(fnode)
            
            else:
                identified_node.append('None')
        
        question_paper_df['Identified Node'] = identified_node

        return question_paper_df


    def display(self):
        for i in list(self.G.nodes):
            print(i, self.G.nodes[i]['max_marks'], 
                self.G.nodes[i]['node_bucket'], 
                self.G.nodes[i]['overflow_bucket'])


    def getResult(self):
        return round(self.G.nodes[self.subject]['node_bucket']/self.G.nodes[self.subject]['max_marks']*100 , 2)
