import pandas as pd
import numpy as np
import statistics as st
import random
import pickle

from rdkit import Chem, DataStructs
from rdkit.Chem import AllChem, MACCSkeys, Descriptors
import itertools as it
from numpy import round

properties = ["SMILES","LIBRARY"]
lista = []
df = []

class StatHBD:

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

    def compute_HBD(self, L):
        ms = list()
        HBD = list()
        for i in L:
            ms.append(Chem.MolFromSmiles(i))
        for i in ms:
            HBD.append(Descriptors.NumHDonors(i))
        return HBD
   
    def compute_stats(self, S):
        HBD = self.compute_HBD(S)
        if len(HBD) > 0:
            stat = list()
            stat.append(round(min(HBD),2))
            stat.append(round(np.percentile(HBD, 25)))
            stat.append(round(st.median(HBD)))
            stat.append(round(st.mean(HBD),2))
            stat.append(round(np.percentile(HBD, 75),2)) 
            stat.append(max(HBD))
            stat.append(round(st.stdev(HBD),2))
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
        Database =  Database.rename_axis("HBD", axis="columns")
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






# import pandas as pd
# import numpy as np
# import statistics as st

# from numpy import round

# import pickle

# class StatHBD:
# #antes se llamaba GeneratePCA
#     def __init__(self, csv_name, 
#     #properties_list, libraries_list
#     ):
#         self.csv_name = csv_name
#         self.generated_csv = pd.read_csv(f'generated_csv/{csv_name}')
#         self.bases_varias = pd.read_csv('apps/PCA/resources/bases_varias.csv')
#         #self.properties_list = properties_list
#         #self.libraries_list = libraries_list

#     def set_smiles(self, smile_lin, smile_lin_nm, smile_cyc, smile_cyc_nm):
#         if len(smile_lin) > 0:
#             self.smile_lin = smile_lin
#         if len(smile_lin_nm) > 0:
#             self.smile_lin_nm = smile_lin_nm
#         if len(smile_cyc) > 0:
#             self.smile_cyc = smile_cyc
#         if len(smile_cyc_nm) > 0:
#             self.smile_cyc_nm = smile_cyc_nm

#     def read_smiles(self, filename):
#         with open('pickles/' + filename, 'rb') as fp:
#             itemlist = pickle.load(fp)
#         return itemlist

#     def compute(self):
#     #antes compute pca
#         Database = self.generated_csv
#         Bibliotecas_varias = self.bases_varias

#         smile_final_pca = list(list(Database["SMILES"]) + list(Bibliotecas_varias["SMILES"]))
#         names_final_pca = list(Database["NAME"]) + list(Bibliotecas_varias["NAME"])
#         libreria_pca = list(list(Database["LIBRARY"]) + list(Bibliotecas_varias["LIBRARY"]))
#         tipo_pca = list(Database["LIBRARY"]) + list(Bibliotecas_varias["LIBRARY"])
#         HBA_pca = list(Database["HBA"]) + list(Bibliotecas_varias["HBA"])
#         HBD_pca = list(Database["HBD"]) + list(Bibliotecas_varias["HBD"])
#         RB_pca = list(Database["RB"]) + list(Bibliotecas_varias["RB"])
#         LOGP_pca = list(Database["LogP"]) + list(Bibliotecas_varias["LogP"])
#         TPSA_pca = list(Database["TPSA"]) + list(Bibliotecas_varias["TPSA"])
#         MW_pca = list(Database["MW"]) + list(Bibliotecas_varias["MW"])

#         columns2 = ["SMILES","NAME","LIBRARY","HBA", "HBD", "RB", "LogP", "TPSA", "MW"]
#         idx2 = [(i) for i,x in enumerate (smile_final_pca,1)]
#         data2 = [smile_final_pca,names_final_pca,libreria_pca,HBA_pca, HBD_pca, RB_pca, LOGP_pca, TPSA_pca, MW_pca]
#         data2 = np.transpose(data2, axes=None)

#         Database2 = pd.DataFrame(
#                     data = data2,
#                     index = idx2,
#                     columns = columns2)
#         Datos=Database2
#         newcol = Datos["LIBRARY"]
#         Datos["LIBRERIA"]=newcol
#         Datos.set_index("LIBRERIA", inplace = True)

#         librerias = Datos.LIBRARY.unique()
#         lista_librerias = []
#         for i in librerias:
#             lista_librerias.append(i)
        
#         data2 = []    
#         properties  = ["HBD"]  
#         for col in properties:
#                 for row in libreria_pca:
#                     data2.append([col, row, Datos.at[row, col]])
#         hbd_fda = []
#         hbd_ppi = []
#         hbd_np = []
#         hbd_pep_fda = []
#         hbd_macro = []
#         hbd_lin = []
#         hbd_lin_nm =[]
#         hbd_cyc= []
#         hbd_cyc_nm = []

#         for row in data2:
#             if 'HBD' in row[0] and 'Linear' in row[1]:
#                 hbd_lin= (row[2]).astype(float)
#         for row in data2:
#              if'HBD' in row[0] and 'Linear Methylated' in row[1]:
#                 hbd_lin_nm=(row[2]).astype(float)
#         for row in data2:
#             if 'HBD' in row[0] and 'Cyclic' in row[1]:
#                 hbd_cyc =(row[2]).astype(float)
#         for row in data2:
#             if 'HBD' in row[0] and 'Cyclic Methylated' in row[1]:
#                 hbd_cyc_nm = (row[2]).astype(float)
#         for row in data2:
#             if 'HBD' in row[0] and 'FDA' in row[1]:
#                 hbd_fda = (row[2]).astype(float)
#         for row in data2:
#             if 'HBD' in row[0] and 'FDA PEP' in row[1]:
#                 hbd_fda_pep =(row[2]).astype(float)
#         for row in data2:
#             if 'HBD' in row[0] and 'MACRO' in row[1]:
#                 hbd_macro =(row[2]).astype(float)
#         for row in data2:
#             if 'HBD' in row[0] and 'NP' in row[1]:
#                 hbd_np =(row[2]).astype(float)
#         for row in data2:
#             if 'HBD' in row[0] and 'PPI' in row[1]:
#                 hbd_ppi =(row[2]).astype(float)

        
                
#         # #Variables para csv
#         data_s = []    
#         stat_lin = [] 
#         stat_lin_nm = []
#         stat_cyc = []
#         stat_cyc_nm = []
#         stat_fda = []
#         stat_fda_pep = []
#         stat_macro = []
#         stat_np = []
#         stat_ppi = []

#         #Compute = StatHBD()
#         if len(hbd_lin)> 0:
#             stat_lin.append(round(min(hbd_lin),2))
#             stat_lin.append(round(np.percentile(hbd_lin, 25)))
#             stat_lin.append(round(st.median(hbd_lin)))
#             stat_lin.append(round(st.mean(hbd_lin),2))
#             stat_lin.append(round(np.percentile(hbd_lin, 75),2)) 
#             stat_lin.append(max(hbd_lin))
#             stat_lin.append(round(st.stdev(hbd_lin),2))
#             data_s.append(stat_lin)
        
              
#         if len(hbd_lin_nm)> 0:
#             stat_lin_nm.append(round(min(hbd_lin_nm),2))
#             stat_lin_nm.append(round(np.percentile(hbd_lin_nm, 25)))
#             stat_lin_nm.append(round(st.median(hbd_lin_nm)))
#             stat_lin_nm.append(round(st.mean(hbd_lin_nm),2))
#             stat_lin_nm.append(round(np.percentile(hbd_lin_nm, 75),2)) 
#             stat_lin_nm.append(max(hbd_lin_nm))
#             stat_lin_nm.append(round(st.stdev(hbd_lin_nm),2))
#             data_s.append(stat_lin)
        
#         if len(hbd_cyc)> 0:
#             stat_cyc.append(round(min(hbd_cyc),2))
#             stat_cyc.append(round(np.percentile(hbd_cyc, 25)))
#             stat_cyc.append(round(st.median(hbd_cyc)))
#             stat_cyc.append(round(st.mean(hbd_cyc),2))
#             stat_cyc.append(round(np.percentile(hbd_cyc, 75),2)) 
#             stat_cyc.append(max(hbd_cyc))
#             stat_cyc.append(round(st.stdev(hbd_cyc),2))
#             data_s.append(stat_cyc)
        
#         if len(hbd_cyc_nm)>0:
#             stat_cyc_nm.append(round(min(hbd_cyc_nm),2))
#             stat_cyc_nm.append(round(np.percentile(hbd_cyc_nm, 25)))
#             stat_cyc_nm.append(round(st.median(hbd_cyc_nm)))
#             stat_cyc_nm.append(round(st.mean(hbd_cyc_nm),2))
#             stat_cyc_nm.append(round(np.percentile(hbd_cyc_nm, 75),2)) 
#             stat_cyc_nm.append(max(hbd_cyc_nm))
#             stat_cyc_nm.append(round(st.stdev(hbd_cyc_nm),2))
#             data_s.append(stat_cyc_nm)
        

#         if len(hbd_fda)> 0:
#             stat_fda.append(round(min(hbd_fda),2))
#             stat_fda.append(round(np.percentile(hbd_fda, 25)))
#             stat_fda.append(round(st.median(hbd_fda)))
#             stat_fda.append(round(st.mean(hbd_fda),2))
#             stat_fda.append(round(np.percentile(hbd_fda, 75),2)) 
#             stat_fda.append(max(hbd_fda))
#             stat_fda.append(round(st.stdev(hbd_fda),2))
#             data_s.append(stat_fda)
        
#         if len(hbd_fda_pep)> 0:
#             stat_fda_pep.append(round(min(hbd_fda_pep),2))
#             stat_fda_pep.append(round(np.percentile(hbd_fda_pep, 25)))
#             stat_fda_pep.append(round(st.median(hbd_fda_pep)))
#             stat_fda_pep.append(round(st.mean(hbd_fda_pep),2))
#             stat_fda_pep.append(round(np.percentile(hbd_fda_pep, 75),2)) 
#             stat_fda_pep.append(max(hbd_fda_pep))
#             stat_fda_pep.append(round(st.stdev(hbd_fda_pep),2))
#             data_s.append(stat_fda_pep)
        
        
#         if len(hbd_macro)> 0:
#             stat_macro.append(round(min(hbd_macro),2))
#             stat_macro.append(round(np.percentile(hbd_macro, 25)))
#             stat_macro.append(round(st.median(hbd_macro)))
#             stat_macro.append(round(st.mean(hbd_macro),2))
#             stat_macro.append(round(np.percentile(hbd_macro, 75),2)) 
#             stat_macro.append(max(hbd_macro))
#             stat_macro.append(round(st.stdev(hbd_macro),2))
#             data_s.append(stat_macro)
        
        
#         if len(hbd_np)> 0:
#             stat_np.append(round(min(hbd_np),2))
#             stat_np.append(round(np.percentile(hbd_np, 25)))
#             stat_np.append(round(st.median(hbd_np)))
#             stat_np.append(round(st.mean(hbd_np),2))
#             stat_np.append(round(np.percentile(hbd_np, 75),2)) 
#             stat_np.append(max(hbd_np))
#             stat_np.append(round(st.stdev(hbd_np),2))
#             data_s.append(stat_np)
        
        
        
#         if len(hbd_ppi)> 0:
#             stat_ppi.append(round(min(hbd_ppi),2))
#             stat_ppi.append(round(np.percentile(hbd_ppi, 25)))
#             stat_ppi.append(round(st.median(hbd_ppi)))
#             stat_ppi.append(round(st.mean(hbd_ppi),2))
#             stat_ppi.append(round(np.percentile(hbd_ppi, 75),2)) 
#             stat_ppi.append(max(hbd_ppi))
#             stat_ppi.append(round(st.stdev(hbd_ppi),2))
#             data_s.append(stat_ppi)   

#         #Dataframe por propiedad "HBD"
#         columns = lista_librerias
#         data = data_s
#         print(data)
#         data = np.transpose(data, axes = None)
#         idx = ["MIN", "1Q", "MEDIAN", "MEAN", "3Q", "MAX", "STD"]

#         Database_stat_hbd = pd.DataFrame(
#                      data = data,
#                      index = idx,
#                      columns = columns)

#         Database_stat_hbd =  Database_stat_hbd.rename_axis("HBD", axis="columns")

#         return Database_stat_hbd.to_html()
        
