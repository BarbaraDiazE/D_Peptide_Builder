import pandas as pd
import numpy as np
from decimal import Decimal

import sklearn
from sklearn import datasets, decomposition

import pickle

from bokeh.io import  show, output_file
from bokeh.models import ColumnDataSource, LassoSelectTool, ZoomInTool, ZoomOutTool, SaveTool, HoverTool,PanTool, Legend
from bokeh.plotting import figure
from bokeh.core.enums import LegendLocation

class GeneratePCA:

    def __init__(self, csv_name):
        self.csv_name = csv_name
        self.generated_csv = pd.read_csv(f'generated_csv/{csv_name}')
        self.bases_varias = pd.read_csv('apps/PCA/resources/bases_varias.csv')
        #self.librerias = self.bases_varias.LIBRARY.unique()
        self.LIN = self.read_smiles(f'smile_lin_{csv_name}.pkl')
        self.LIN_NM = self.read_smiles(f'smile_lin_nm_{csv_name}.pkl')
        self.CYC = self.read_smiles(f'smile_cyc_{csv_name}.pkl')
        self.CYC_NM = self.read_smiles(f'smile_cyc_nm_{csv_name}.pkl')
        
        Database = self.generated_csv
        Bibliotecas_varias = self.bases_varias

        smiles = list(list(Database["SMILES"]) + list(Bibliotecas_varias["SMILES"]))
        names = list(Database["NAME"]) + list(Bibliotecas_varias["NAME"])
        library = list(list(Database["LIBRARY"]) + list(Bibliotecas_varias["LIBRARY"]))
        HBA = list(Database["HBA"]) + list(Bibliotecas_varias["HBA"])
        HBD = list(Database["HBD"]) + list(Bibliotecas_varias["HBD"])
        RB = list(Database["RB"]) + list(Bibliotecas_varias["RB"])
        LOGP= list(Database["LogP"]) + list(Bibliotecas_varias["LogP"])
        TPSA = list(Database["TPSA"]) + list(Bibliotecas_varias["TPSA"])
        MW = list(Database["MW"]) + list(Bibliotecas_varias["MW"])
        columns = ["SMILES","NAME","LIBRARY","HBA", "HBD", "RB", "LogP", "TPSA", "MW"]
        idx = [(i) for i,x in enumerate (smiles,1)]
        data = [smiles,names,library,HBA, HBD, RB, LOGP, TPSA, MW]
        data = np.transpose(data, axes=None)
        self.Database = pd.DataFrame(
                                        data = data,
                                        index = idx,
                                        columns = columns)
        #elementos numericos
        feature_names = ["HBA", "HBD", "RB", "LogP","TPSA", "MW"]
        self.numerical_data = pd.DataFrame(self.Database[feature_names])
                
    
    def read_smiles(self, filename):
        with open('pickles/' + filename, 'rb') as fp:
            itemlist = pickle.load(fp)
        return itemlist

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

    def compute_pca(self):
        numerical_data = self.numerical_data
        # Calculate the principal components using scikit-learn
        sklearn_pca = sklearn.decomposition.PCA()
        sklearn_pca.fit(numerical_data)
        
        # Perform the PCA again retaining only the top 2 components
        sklearn_pca = sklearn.decomposition.PCA(n_components=6, svd_solver = "full", whiten = True)
        sklearn_pca.fit(numerical_data)
        pca_result = pd.DataFrame(sklearn_pca.transform(numerical_data), columns=['PC1','PC2',"PC3", 'PC4','PC5',"PC6"])
        pca_result["LIBRARY"] = self.Database.LIBRARY
        pca_result["TIPO"] = self.Database.LIBRARY
        pca_result["SMILES"] = self.Database.SMILES
        pca_result["NAME"] = self.Database.NAME
        self.pca_result = pca_result.set_index('TIPO')
        variance = list(sklearn_pca.explained_variance_ratio_)
        self.a = round(variance[0] * 100, 2)
        self.b = round(variance[1] * 100,2)

        return pca_result

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
        p = figure(title = "Chemical Space by PCA",
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
