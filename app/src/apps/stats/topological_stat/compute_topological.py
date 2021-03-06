import pandas as pd
import numpy as np
import statistics as st
import random
import pickle

from rdkit import Chem, DataStructs
from rdkit.Chem.Fingerprints import FingerprintMols
import itertools as it

properties = ["SMILES","LIBRARY"]
lista = []
df = []

class statTOPOLOGICAL:

    def __init__(self, csv_name):
        self.Data = pd.read_csv('apps/PCA/resources/sample_libraries.csv')
        self.Data['TIPO'] = self.Data['LIBRARY']
        self.Data = self.Data.set_index('TIPO')
        self.librerias = self.Data.LIBRARY.unique()
        self.LIN = self.read_smiles(f'smile_lin_{csv_name}.pkl')
        self.LIN_NM = self.read_smiles(f'smile_lin_nm_{csv_name}.pkl')
        self.CYC = self.read_smiles(f'smile_cyc_{csv_name}.pkl')
        self.CYC_NM = self.read_smiles(f'smile_cyc_nm_{csv_name}.pkl')
    
    def filtered(self):
        for col in properties:
            for row in self.librerias:
                df.append([col, row, self.Data.at[row, col]])
        FDA = list(df[0][2])
        FDA_PEP = list(df[1][2])
        MACRO = list(df[2][2])
        NP = list(df[3][2])
        PPI = list(df[4][2])
        return FDA, PPI, MACRO, NP, FDA_PEP
    
    def read_smiles(self, filename):
        with open('pickles/' + filename, 'rb') as fp:
            itemlist = pickle.load(fp)
        return itemlist
 
    def smiles(self):
        LIN = self.LIN
        LIN_NM = self.LIN_NM
        CYC = self.CYC
        CYC_NM = self.CYC_NM
        return LIN, LIN_NM, CYC, CYC_NM

    def column(self, LIN, LIN_NM, CYC, CYC_NM, ):
        column_name = ['FDA', 'PPI', 'MACRO', 'NP', 'FDA PEP']
        if len (LIN) > 0:
            column_name.append('LIN')
        if len (LIN_NM) > 0:
            column_name.append('LIN NM')
        if len (CYC) > 0:
            column_name.append('CYC')
        if len (CYC_NM) > 0:
            column_name.append('CYC NM')
        return column_name

    def compute_TOPOLOGICAL(self, L):
        ms = list()
        sim = list()
        random.seed(43)
        N = round(len(L)*.2)
        X = random.sample(L,N)
        ms=[Chem.MolFromSmiles(i) for i in X]
# 
        fps_Topological = [FingerprintMols.FingerprintMol(x) for x in ms]
        Topological = [DataStructs.FingerprintSimilarity(y,x) for x,y in it.combinations(fps_Topological,2)]
        Topological.sort()
        sim = Topological    #similitud
        return sim
    def compute_stats(self, S):
        sim = self.compute_TOPOLOGICAL(S)
        if len(sim) > 0:
            stat = list()
            stat.append(round(min(sim),2))
            stat.append(round(np.percentile(sim, 25)))
            stat.append(round(st.median(sim)))
            stat.append(round(st.mean(sim),2))
            stat.append(round(np.percentile(sim, 75),2)) 
            stat.append(max(sim))
            stat.append(round(st.stdev(sim),2))
            return stat
            
    def plot(self,  LIN, LIN_NM, CYC, CYC_NM, source1, source2, source3, source4, source5, source6=[],
                source7=[], source8=[], source9=[]):
        sources = [source1, source2, source3, source4, source5]
        if len(LIN) > 0:
            sources.append(source6)
        if len(LIN_NM) > 0:
            sources.append(source7)
        if len(CYC) > 0:
            sources.append(source8)
        if len(CYC_NM) > 0:
            sources.append(source9)
        data = np.matrix(sources)
        data = np.transpose(data, axes = None)
        idx = ["MIN", "1Q", "MEDIAN", "MEAN", "3Q", "MAX", "STD"]
        Database = pd.DataFrame(
                    data=data,
                    index=idx,
                    columns=self.column(LIN, LIN_NM, CYC, CYC_NM))
        Database =  Database.rename_axis(" Topological ", axis="columns")
        return Database.to_html()
    
    def resolve(self):
        FDA, PPI, MACRO, NP, FDA_PEP = self.filtered()
        LIN, LIN_NM, CYC, CYC_NM = self.smiles()
        return self.plot(
             LIN, LIN_NM, CYC, CYC_NM,
            source1=self.compute_stats(FDA),
            source2=self.compute_stats(PPI),
            source3=self.compute_stats(MACRO),
            source4=self.compute_stats(NP),
            source5=self.compute_stats(FDA_PEP),
            source6=self.compute_stats(LIN),
            source7=self.compute_stats(LIN_NM),
            source8=self.compute_stats(CYC),
            source9=self.compute_stats(CYC_NM),
        )