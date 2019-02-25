import pandas as pd
import numpy as np
from decimal import Decimal

import sklearn
from sklearn import datasets, decomposition

import pickle

from rdkit import DataStructs, Chem
from rdkit.Chem.Fingerprints import FingerprintMols
from rdkit.DataManip.Metric.rdMetricMatrixCalc import GetTanimotoSimMat
from rdkit.DataManip.Metric.rdMetricMatrixCalc import GetTanimotoDistMat


from bokeh.models import ColumnDataSource, LassoSelectTool, ZoomInTool, ZoomOutTool, SaveTool, HoverTool, PanTool, Legend
from bokeh.io import  show, output_file
from bokeh.plotting import figure 
from bokeh.core.enums import LegendLocation

class GeneratePCA:

    def __init__(self, csv_name):
        self.csv_name = csv_name
        self.generated_csv = pd.read_csv(f'generated_csv/{csv_name}')
        self.generated_csv = self.generated_csv.sample(frac=0.3, replace=True, random_state=1992)
        self.bases_varias = pd.read_csv('apps/PCA/resources/sample_libraries_2.csv')
        self.LIN = self.read_smiles(f'smile_lin_{csv_name}.pkl')
        self.LIN_NM = self.read_smiles(f'smile_lin_nm_{csv_name}.pkl')
        self.CYC = self.read_smiles(f'smile_cyc_{csv_name}.pkl')
        self.CYC_NM = self.read_smiles(f'smile_cyc_nm_{csv_name}.pkl')

        Database = self.generated_csv
        Bibliotecas_varias = self.bases_varias

        smiles =  list( list(Database["SMILES"]) + list(Bibliotecas_varias["SMILES"]))
        names =   list( list(Database["NAME"])   + list(Bibliotecas_varias["NAME"]))
        library = list( list(Database["LIBRARY"])+ list(Bibliotecas_varias["LIBRARY"]))
        data = [smiles,names,library]
        data = np.transpose(data, axes=None)
        self.Database2 = pd.DataFrame(
                                        data = data,
                                        index = None,
                                        columns = ["SMILES","NAME","LIBRARY"]
                                    )
                    
    def read_smiles(self, filename):
        with open('pickles/' + filename, 'rb') as fp:
            itemlist = pickle.load(fp)
        return itemlist

    def compute_pca(self):
        Database = self.Database2
        smiles = list(Database.SMILES)
        smi = [Chem.MolFromSmiles(x) for x in smiles]
        fps=[FingerprintMols.FingerprintMol(x) for x in smi]

        tanimoto_sim_mat_lower_triangle=GetTanimotoSimMat(fps)
        n_mol = len(fps)
        similarity_matrix = np.ones([n_mol,n_mol])
        i_lower= np.tril_indices(n=n_mol,m=n_mol,k=-1)
        i_upper= np.triu_indices(n=n_mol,m=n_mol,k=1)
        similarity_matrix[i_lower] = tanimoto_sim_mat_lower_triangle
        similarity_matrix[i_upper] = similarity_matrix.T[i_upper] 



        sklearn_pca = sklearn.decomposition.PCA(n_components=2, svd_solver = "full", whiten = True)
        sklearn_pca.fit(similarity_matrix)
        variance = list(sklearn_pca.explained_variance_ratio_)
        a = round(variance[0] * 100, 2)
        b = round(variance[1] * 100,2)
        pca_result = pd.DataFrame(sklearn_pca.transform(similarity_matrix) , columns=['PC1','PC2'])
        pca_result["LIBRARY"] = Database.LIBRARY
        pca_result["TIPO"] = Database.LIBRARY
        pca_result["SMILES"] = Database.SMILES
        pca_result["NAME"] = Database.NAME
        self.pca_result = pca_result.set_index('TIPO')
        variance = list(sklearn_pca.explained_variance_ratio_)
        self.a = round(variance[0] * 100, 2)
        self.b = round(variance[1] * 100,2)

        return pca_result

    def existing_libraries(self):
        FDA = ["FDA"]
        FDA_PEP = ["FDA PEP"]
        MACRO = ["MACRO"]
        NP = ["NP"]
        PPI = ["PPI"]
        LIN = self.LIN
        LIN_NM = self.LIN_NM
        CYC = self.CYC
        CYC_NM = self.CYC_NM
        if len(self.LIN ) > 0:
            LIN = ["Linear"]
        if len(self.LIN_NM) > 0:
            LIN_NM = ["Linear Methylated"]
        if len(self.CYC) > 0:
            CYC = ["Cyclic"]
        if len(self.CYC_NM) > 0:
            CYC_NM = ["Cyclic Methylated"]
        
        return FDA, FDA_PEP, MACRO, NP, PPI, LIN, LIN_NM, CYC, CYC_NM

    def column_source(self, L):
        pca_result = self.pca_result
        df = []

        properties = ["PC1","PC2","LIBRARY","SMILES","NAME"]
        for col in properties:
            for row in L:
                df.append([col, row, pca_result.at[row, col]])
        if len(L) > 0:
            X = list(df[0][2])
            Y = list(df[1][2])
            N = list(df[4][2])
        else:
            X = list()
            Y = list()
            N = list()

        return ColumnDataSource(dict(x = X, y = Y, N = N))


    def plot(self,  source1, source2, source3, source4, source5, source6, source7, source8, source9):
        a = self.a
        b = self.b
        hover = HoverTool(tooltips = [
                                        ("PCA1","($x)"),
                                        ("PCA2","($y)"),
                                        ("NAME","(@N)"),
                                        ])
        p = figure( title = "CHEMICAL SPACE BY TOPOLOGICAL FP",
                x_axis_label = "PC 1 " + "("+str(a)+"%)", y_axis_label="PC 2 " + "("+str(b)+"%)",
                x_range = (-7,7), y_range = (-7,7), tools = [hover], plot_width = 1000, plot_height = 800)
        FDA_plot = p.circle(x = "x", y = "y", source = source1, color = "darkslateblue", size = 5)
        PPI_plot = p.circle(x = "x", y = "y", source = source2, color = "yellowgreen", size = 5)
        MACRO_plot = p.circle(x = "x", y = "y", source = source3, color ="lightsteelblue", size = 5)
        NP_plot = p.circle(x = "x", y = "y", source = source4, color = "olive", size = 5)
        PEP_FDA_plot = p.circle(x = "x", y = "y", source = source5, color ="darkslategray", size = 5)
        LIN_plot = p.circle(x = "x", y = "y", source = source6, color = "aquamarine", size = 5)
        LIN_NM_plot = p.circle(x = "x", y = "y", source = source7, color = "teal", size = 5)
        CYC_plot = p.circle(x = "x", y = "y", source = source8, color = "lightpink", size = 5)
        CYC_NM_plot = p.circle(x = "x", y = "y", source = source9, color = "mediumvioletred", size = 5)
        p.add_tools(LassoSelectTool(), ZoomInTool(), ZoomOutTool(), SaveTool(), PanTool())
        legend = Legend(items=[
                    ("FDA",     [FDA_plot]),
                    ("PPI",     [PPI_plot]),
                    ("MACRO",   [MACRO_plot]),
                    ("NP",      [NP_plot]),
                    ("PEP FDA", [PEP_FDA_plot]),
                    ("LIN",     [LIN_plot]),
                    ("LIN NM",  [LIN_NM_plot]),
                    ("CYC",     [CYC_plot]),
                    ("CYC NM",  [CYC_NM_plot]),
                    ], 
                location = "center", orientation = "vertical", click_policy = "hide"
            )
        p.add_layout(legend, place = 'right')
        p.xaxis.axis_label_text_font_size = "20pt"
        p.yaxis.axis_label_text_font_size = "20pt"
        p.xaxis.axis_label_text_color = "black"
        p.yaxis.axis_label_text_color = "black"
        p.xaxis.major_label_text_font_size = "18pt"
        p.yaxis.major_label_text_font_size = "18pt"
        p.title.text_font_size = "22pt"
        return p

    def resolve(self):
        self.compute_pca()
        FDA, FDA_PEP, MACRO, NP, PPI, LIN, LIN_NM, CYC, CYC_NM = self.existing_libraries()
        return self.plot(
            source1=self.column_source(FDA),
            source2=self.column_source(PPI),
            source3=self.column_source(MACRO),
            source4=self.column_source(NP),
            source5=self.column_source(FDA_PEP),
            source6=self.column_source(LIN),
            source7=self.column_source(LIN_NM),
            source8=self.column_source(CYC),
            source9=self.column_source(CYC_NM),
        )

###
###
###
# class GeneratePCA:

#     def __init__(self, csv_name):
#         self.csv_name = csv_name
#         self.generated_csv = pd.read_csv(f'generated_csv/{csv_name}')
#         self.bases_varias = pd.read_csv('apps/PCA/resources/sample_libraries_2.csv')

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
    
#     def compute_pca(self):
#         Database = self.generated_csv
#         Bibliotecas_varias = self.bases_varias

#         ms = list(list(Database["SMILES"]) + list(Bibliotecas_varias["SMILES"]))
#         labels = list(list(Database["LIBRARY"]) + list(Bibliotecas_varias["LIBRARY"]))
#         names_final_pca = list(Database["NAME"]) + list(Bibliotecas_varias["NAME"])
        
#         smi=[Chem.MolFromSmiles(x) for x in ms]
#         fps=[FingerprintMols.FingerprintMol(x) for x in smi]

#         tanimoto_sim_mat_lower_triangle=GetTanimotoSimMat(fps)
#         n_mol = len(fps)
#         similarity_matrix = np.ones([n_mol,n_mol])
#         i_lower= np.tril_indices(n=n_mol,m=n_mol,k=-1)
#         i_upper= np.triu_indices(n=n_mol,m=n_mol,k=1)
#         similarity_matrix[i_lower] = tanimoto_sim_mat_lower_triangle
#         similarity_matrix[i_upper] = similarity_matrix.T[i_upper] 

#         sklearn_pca = sklearn.decomposition.PCA(n_components=2, svd_solver = "full", whiten = True)
#         sklearn_pca.fit(similarity_matrix)
#         variance = list(sklearn_pca.explained_variance_ratio_)
#         a = round(variance[0] * 100, 2)
#         b = round(variance[1] * 100,2)
#         PCA_sim = pd.DataFrame(sklearn_pca.transform(similarity_matrix) , columns=['PC1','PC2'])
#         PCA_sim["LIBRARY"]=labels
#         PCA_sim['TIPO'] = labels
#         PCA_sim['SMILES']=ms
#         PCA_sim['NAME']=names_final_pca
#         PCA_sim = PCA_sim.set_index('TIPO')

#         smile_lin = self.read_smiles(f'smile_lin_{self.csv_name}.pkl')
#         smile_lin_nm = self.read_smiles(f'smile_lin_nm_{self.csv_name}.pkl')
#         smile_cyc = self.read_smiles(f'smile_cyc_{self.csv_name}.pkl')
#         smile_cyc_nm = self.read_smiles(f'smile_cyc_nm_{self.csv_name}.pkl')


#         #1 FDA
#         FDA = ["FDA",]
#         properties = ["PC1","PC2","LIBRARY","SMILES","NAME"]
#         df_FDA = []
#         for col in properties:
#             for row in FDA:
#                 df_FDA.append([col, row, PCA_sim.at[row, col]]) 

#         X_FDA = list(df_FDA[0][2])
#         Y_FDA = list(df_FDA[1][2])
#         S_FDA= list(df_FDA[3][2])
#         N_FDA= list(df_FDA[4][2])

#         #2 PPI
#         PPI = ["PPI",]
#         df_PPI = []
#         for col in properties:
#             for row in PPI:
#                 df_PPI.append([col, row, PCA_sim.at[row, col]]) 

#         X_PPI = list(df_PPI[0][2])
#         Y_PPI = list(df_PPI[1][2])
#         S_PPI= list(df_PPI[3][2])
#         N_PPI= list(df_PPI[4][2])

#         #3 MACRO
#         MACRO = ["MACRO",]
#         df_MACRO = []
#         for col in properties:
#             for row in MACRO:
#                 df_MACRO.append([col, row, PCA_sim.at[row, col]]) 

#         X_MACRO = list(df_MACRO[0][2])
#         Y_MACRO = list(df_MACRO[1][2])
#         S_MACRO= list(df_MACRO[3][2])
#         N_MACRO= list(df_MACRO[4][2])

#         #4 NP
#         NP = ["NP",]
#         df_NP = []
#         for col in properties:
#             for row in NP:
#                 df_NP.append([col, row, PCA_sim.at[row, col]]) 
#         X_NP = list(df_NP[0][2])
#         Y_NP = list(df_NP[1][2])
#         S_NP= list(df_NP[3][2])
#         N_NP= list(df_NP[4][2])
        
#         #5 FDA_PEP
#         FDA_PEP = ["FDA PEP",]
#         df_FDA_PEP = []
#         for col in properties:
#             for row in FDA_PEP:
#                 df_FDA_PEP.append([col, row, PCA_sim.at[row, col]]) 
#         X_FDA_PEP = list(df_FDA_PEP[0][2])
#         Y_FDA_PEP = list(df_FDA_PEP[1][2])
#         S_FDA_PEP= list(df_FDA_PEP[3][2])
#         N_FDA_PEP= list(df_FDA_PEP[4][2])

#         #6 LINEAR
#         Linear = ["Linear",]
#         df_LIN = list()

#         if len(smile_lin)> 0:
#             for col in properties:
#                 for row in Linear:
#                     df_LIN.append([col, row, PCA_sim.at[row, col]]) 
#         if len(df_LIN) > 0:
#             X_LIN = list(df_LIN[0][2])
#             Y_LIN = list(df_LIN[1][2])
#             S_LIN= list(df_LIN[3][2])
#             N_LIN= list(df_LIN[4][2])
                    
#         #7 LINAR NM
#         Linear_NM = ["Linear Methylated"]
#         df_LIN_NM = list()

            
#         if len(smile_lin_nm) > 0:
#             for col in properties:
#                 for row in Linear_NM:
#                     df_LIN_NM.append([col, row, PCA_sim.at[row, col]])
#         if len(df_LIN_NM) > 0: 
#             #df_LIN_NM = df_LIN_NM.astype(str)         
#             X_LIN_NM =  list(df_LIN_NM[0][2])
#             Y_LIN_NM = list(df_LIN_NM[1][2])
#             S_LIN_NM= list(df_LIN_NM[3][2])
#             N_LIN_NM= list(df_LIN_NM[4][2])
            

#         #8 CYCLIC
#         Cyclic = ["Cyclic",]
#         df_CYC = list()
#         if len(smile_cyc) > 0:
#             for col in properties:
#                 for row in Cyclic:
#                     df_CYC.append([col, row, PCA_sim.at[row, col]])  
#         if len(df_CYC) > 0:
#             X_CYC = list(df_CYC[0][2])
#             Y_CYC = list(df_CYC[1][2])
#             S_CYC= list(df_CYC[3][2])
#             N_CYC= list(df_CYC[4][2])
            
#         #9 CYC NM
#         Cyclic_NM = ["Cyclic Methylated",]
#         df_CYC_NM = list()
#         if len(smile_cyc_nm) > 0:
#             for col in properties:
#                 for row in Cyclic_NM:
#                     df_CYC_NM.append([col, row, PCA_sim.at[row, col]])  
#         if len(df_CYC_NM) > 0:
#             X_CYC_NM = list(df_CYC_NM[0][2])
#             Y_CYC_NM = list(df_CYC_NM[1][2])
#             S_CYC_NM= list(df_CYC_NM[3][2])
#             N_CYC_NM= list(df_CYC_NM[4][2])

#         X_10 = list()
#         Y_10 = list()
#         N_10 = list()
        
#         #1. FDA
#         source1 = ColumnDataSource(dict(x = X_FDA, y = Y_FDA, N = N_FDA))        
#         #2. PPI
#         source2 = ColumnDataSource(dict(x = X_PPI, y = Y_PPI, N = N_PPI)) 
#         #3. MACRO
#         source3 = ColumnDataSource(dict(x = X_MACRO, y = Y_MACRO, N = N_MACRO)) 
#         #4. NP
#         source4 = ColumnDataSource(dict(x = X_NP, y = Y_NP, N = N_NP)) 
#         #5 FDA PEP
#         source5 = ColumnDataSource(dict(x = X_FDA_PEP,y = Y_FDA_PEP, N = N_FDA_PEP))         
#         #6 LINEAR
#         if len(smile_lin) > 0:
#             source6 = ColumnDataSource(dict(x = X_LIN, y = Y_LIN, N = N_LIN)) 
#         #7 LINAR NM
#         if len(smile_lin_nm) > 0:
#             source7 = ColumnDataSource(dict(x = X_LIN_NM, y = Y_LIN_NM, N = N_LIN_NM)) 
#         #8 CYCLIC
#         if len(smile_cyc) > 0:
#             source8 = ColumnDataSource(dict(x = X_CYC, y = Y_CYC, N = N_CYC)) 
#         #9 CYC NM
#         if len(smile_cyc_nm) > 0:
#             source9 = ColumnDataSource(dict(x = X_CYC_NM, y = Y_CYC_NM, N = N_CYC_NM)) 


#         source10 = ColumnDataSource(dict(x = X_10, y = Y_10, N = N_10))
#         hover = HoverTool(tooltips = [
#             ("PCA1","($x)"),
#             ("PCA2","($y)"),
#             ("NAME","(@N)"),
#             ])
#         p = figure(title = "PCA Topological FP",
#                 x_axis_label = "PC 1 " + "("+str(a)+"%)", y_axis_label="PC 2 " + "("+str(b)+"%)",
#                 x_range = (-7,7), y_range = (-7,7), tools = [hover],   plot_width = 1000, plot_height = 800)
#         FDA_plot = p.circle(x = "x", y = "y", source = source1, color="darkslateblue", size = 5,  )
#         PPI_plot = p.circle(x = "x", y = "y", source = source2, color="yellowgreen", size = 5)
#         MACRO_plot = p.circle(x = "x", y = "y", source = source3, color="lightsteelblue", size = 5)
#         NP_plot = p.circle(x = "x", y = "y", source = source4, color="olive", size = 5,)
#         PEP_FDA_plot = p.circle(x = "x", y = "y", source = source5, color="darkslategray", size = 5, )
#         if len(smile_lin) > 0:
#             LIN_plot = p.circle(x = "x", y = "y", source = source6, color="aquamarine", size = 5, )
#         if len(smile_lin_nm) > 0:            
#             LIN_NM_plot = p.circle(x = "x", y = "y", source = source7, color="teal", size = 5,)
#         if len(smile_cyc) > 0:
#             CYC_plot = p.circle(x = "x", y = "y", source = source8, color="lightpink", size = 5)
#         if len(smile_cyc_nm) > 0:
#             CYC_NM_plot = p.circle(x = "x", y = "y", source = source9, color="mediumvioletred", size = 5,)
#         p.add_tools(LassoSelectTool(), ZoomInTool(), ZoomOutTool(), SaveTool(), PanTool())
#         if len(smile_lin) > 0:
#             LIN_plot = p.circle(x = "x", y = "y", source = source6, color = "aquamarine", size = 5)
#         else:
#             LIN_plot = p.circle(x = "x", y = "y", source = source10, color = "aquamarine", size = 5)
#         if len(smile_lin_nm) > 0:            
#             LIN_NM_plot = p.circle(x = "x", y = "y", source = source7, color = "teal", size = 5)
#         else:
#             LIN_NM_plot = p.circle(x = "x", y = "y", source = source10, color = "teal", size = 5)
#         if len(smile_cyc) > 0:
#             CYC_plot = p.circle(x = "x", y = "y", source = source8, color = "lightpink", size = 5)
#         else:
#             CYC_plot = p.circle(x = "x", y = "y", source = source10, color = "lightpink", size = 5)
#         if len(smile_cyc_nm) > 0:
#             CYC_NM_plot = p.circle(x = "x", y = "y", source = source9, color = "mediumvioletred", size = 5)
#         else:
#             CYC_NM_plot = p.circle(x = "x", y = "y", source = source10, color = "mediumvioletred", size = 5)
#         p.add_tools(LassoSelectTool(), ZoomInTool(), ZoomOutTool(), SaveTool(), PanTool())
#         legend = Legend(items=[
#                     ("FDA",     [FDA_plot]),
#                     ("PPI",     [PPI_plot]),
#                     ("MACRO",   [MACRO_plot]),
#                     ("NP",      [NP_plot]),
#                     ("PEP FDA", [PEP_FDA_plot]),
#                     ("LIN",     [LIN_plot]),
#                     ("LIN NM",  [LIN_NM_plot]),
#                     ("CYC",     [CYC_plot]),
#                     ("CYC NM",  [CYC_NM_plot]),
#                     ], 
#                 location = "center", orientation = "vertical", click_policy = "hide"
#             )
#         p.add_layout(legend, place = 'right')
#         p.xaxis.axis_label_text_font_size = "20pt"
#         p.yaxis.axis_label_text_font_size = "20pt"
#         p.xaxis.axis_label_text_color = "black"
#         p.yaxis.axis_label_text_color = "black"
#         p.xaxis.major_label_text_font_size = "18pt"
#         p.yaxis.major_label_text_font_size = "18pt"
#         p.title.text_font_size = "22pt"
#         return p