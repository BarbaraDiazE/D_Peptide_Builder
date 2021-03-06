import pandas as pd
import numpy as np

import sklearn
from sklearn import datasets, decomposition
from sklearn.manifold import TSNE

import pickle

from rdkit import Chem, DataStructs
from rdkit.Chem import AllChem
from rdkit.Chem.Fingerprints import FingerprintMols
from rdkit.DataManip.Metric.rdMetricMatrixCalc import GetTanimotoSimMat, GetTanimotoDistMat

from bokeh.io import  show, output_file
from bokeh.models import ColumnDataSource, LassoSelectTool, ZoomInTool, ZoomOutTool, SaveTool, HoverTool,PanTool, Legend
from bokeh.plotting import figure
from bokeh.core.enums import LegendLocation

class GenerateTSNE:

    def __init__(self, csv_name, perplexity = 50):
        self.csv_name = csv_name
        self.generated_csv = pd.read_csv(f'generated_csv/{csv_name}')
        self.generated_csv = self.generated_csv.sample(frac=0.3, replace=True, random_state=1992)
        self.bases_varias = pd.read_csv('apps/PCA/resources/sample_libraries_2.csv')
        self.perplexity = perplexity
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

    def compute_tsne(self):
        Database = self.Database2
        smiles = list(Database["SMILES"])
        smi=[Chem.MolFromSmiles(x) for x in smiles]
        fps = [AllChem.GetMorganFingerprintAsBitVect(x,3) for x in smi]
        tanimoto_sim_mat_lower_triangle=GetTanimotoSimMat(fps)
        n_mol = len(fps)
        similarity_matrix = np.ones([n_mol,n_mol])
        i_lower= np.tril_indices(n=n_mol,m=n_mol,k=-1)
        i_upper= np.triu_indices(n=n_mol,m=n_mol,k=1)
        similarity_matrix[i_lower] = tanimoto_sim_mat_lower_triangle
        similarity_matrix[i_upper] = similarity_matrix.T[i_upper] 
        distance_matrix = np.subtract(1,similarity_matrix)


        TSNE_sim = TSNE(n_components=2,
                        init='pca',
                        random_state=1992, 
                        angle = 0.3,
                        perplexity=self.perplexity
                        ).fit_transform(distance_matrix)
        tsne_result = pd.DataFrame(data = TSNE_sim , 
                                columns=["PC1","PC2"]
                                )
        tsne_result["LIBRARY"] = list(Database.LIBRARY)
        tsne_result["TIPO"] = list(Database.LIBRARY)
        tsne_result["SMILES"] = list(Database.SMILES)
        tsne_result["NAME"] = list(Database.NAME)
        self.tsne_result = tsne_result.set_index('TIPO')
        
        
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
        tsne_result = self.tsne_result
        df = []

        properties = ["PC1","PC2","LIBRARY","SMILES","NAME"]
        for col in properties:
            for row in L:
                df.append([col, row, tsne_result.at[row, col]])
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
        hover = HoverTool(tooltips = [
                                        ("x","($x)"),
                                        ("y","($y)"),
                                        ("NAME","(@N)"),
                                        ])

        p = figure(title = "TSNE/Morgan 3 FP", x_range = (-7,7), y_range = (-7,7), tools = [hover], plot_width = 1000, plot_height = 800)
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
        self.compute_tsne()
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