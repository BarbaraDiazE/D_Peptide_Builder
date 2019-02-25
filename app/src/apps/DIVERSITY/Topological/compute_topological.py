import pandas as pd
import numpy as np
import random
import pickle

from rdkit import Chem, DataStructs
from rdkit.Chem.Fingerprints import FingerprintMols
import itertools as it

from apps.core.functions import percentual_sample

from bokeh.io import  show, output_file
from bokeh.models import ColumnDataSource, LassoSelectTool, ZoomInTool, ZoomOutTool, SaveTool, HoverTool,PanTool, Legend
from bokeh.plotting import figure
from bokeh.core.enums import LegendLocation

properties = ["SMILES","LIBRARY"]
lista = []
df = []

class GenerateTopological:

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
        return FDA, FDA_PEP, MACRO, NP, PPI
    
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
    
    def compute_topological(self, L):
        ms = list()
        sim = list()
        y = list()
        random.seed(43)
        N =round(len(L)*.2)
        X = random.sample(L,N)
        ms =[Chem.MolFromSmiles(i) for i in X]
        fps_Topological = [FingerprintMols.FingerprintMol(x) for x in ms]
        Topological = [DataStructs.FingerprintSimilarity(y,x) for x,y in it.combinations(fps_Topological,2)]
        Topological.sort()
        sim = Topological    
        y = np.arange(1, len(sim) + 1)/len(sim) 
        return sim, y

    def column_source(self, column):
        sim, y = self.compute_topological(column)
        return ColumnDataSource(dict(x=sim, y=y))
    
    def plot(self, source1, source2, source3, source4, source5, source6, source7, source8, source9):
        hover = HoverTool(tooltips = [
            ("Similarity","($x)"),
            ("ECF","($y)"),
            ])
        p = figure(title = "TOPOLOGICAL FP/Tanimoto Similarity",
                x_axis_label = "Similarity", y_axis_label = "Cumulative Distribution Function",
                x_range = (0,1), y_range = (0,1), tools = [hover], plot_width = 1000, plot_height = 800)
        FDA_plot = p.line(x = "x", y = "y", source = source1, line_width = 3, color = "darkslateblue")
        PPI_plot = p.line(x = "x", y = "y", source = source2, line_width = 3, color = "yellowgreen")
        MACRO_plot = p.line(x = "x", y = "y", source = source3, line_width = 3, color = "lightsteelblue")
        NP_plot = p.line(x = "x", y = "y", source = source4, line_width = 3, color = "olive")
        PEP_FDA_plot = p.line(x = "x", y = "y", source = source5, line_width = 3, color = "darkslategray")
        LIN_plot = p.line(x = "x", y = "y", source = source6, line_width = 3, color = "aquamarine")
        LIN_NM_plot = p.line(x = "x", y = "y", source = source7, line_width = 3, color = "teal")
        CYC_plot = p.line(x = "x", y = "y", source = source8, line_width = 3, color = "lightpink")
        CYC_NM_plot = p.line(x = "x", y = "y", source = source9, line_width = 3, color = "mediumvioletred")
        p.add_tools(LassoSelectTool(), ZoomInTool(), ZoomOutTool(), SaveTool(), PanTool())
        legend = Legend(items=[
                    ("FDA", [FDA_plot]),
                    ("PPI", [PPI_plot]),
                    ("MACRO", [MACRO_plot]),
                    ("NP", [NP_plot]),
                    ("PEP FDA", [PEP_FDA_plot]),
                    ("LIN", [LIN_plot]),
                    ("LIN NM", [LIN_NM_plot]),
                    ("CYC", [CYC_plot]),
                    ("CYC NM", [CYC_NM_plot]),
                    ], location = "center", orientation = "vertical", click_policy = "hide")
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
        FDA, FDA_PEP, MACRO, NP, PPI = self.filtered()
        LIN, LIN_NM, CYC, CYC_NM = self.smiles()
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