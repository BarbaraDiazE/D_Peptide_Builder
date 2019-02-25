from rdkit import Chem
from rdkit.Chem.Draw import IPythonConsole
from rdkit.Chem import Draw, Descriptors

import numpy as np
import pandas as pd


from .dataframes import (
    amino_first_dataframe, df, oxigen
)

from .generators import (
    generate_sequence, generate_names
)

class ComputeSequence:
    def __init__(self, amino_first, dataset, peptide_type, peptide_length):
        self.amino_first = amino_first
        self.dataset = dataset
        self.peptide_type = peptide_type
        self.peptide_length = peptide_length

    def df_amino_first(self):
        df_list = []
        for col in self.peptide_type:
            for row in self.amino_first:
                df_list.append([col, row, amino_first_dataframe.at[row, col]])
        return df_list

    def df_data(self):
        df_list = []
        for col in self.peptide_type:
            for row in self.dataset:
                df_list.append([col, row, df.at[row, col]])
        return df_list

    def df_oxigen(self):
        df_list = []
        for col in self.peptide_type:
            for row in [self.peptide_length]:
                df_list.append([col, row, oxigen.at[row, col]])
        return df_list

    def data_first(self):
        data_first_1 = list(filter(lambda item: item[0] == 'LIN', self.df_amino_first() ))
        data_first_2 = list(filter(lambda item: item[0] == 'LIN NM', self.df_amino_first() ))
        data_first_3 = list(filter(lambda item: item[0] == 'CYC', self.df_amino_first() ))
        data_first_4 = list(filter(lambda item: item[0] == 'CYC NM', self.df_amino_first() ))
        return data_first_1, data_first_2, data_first_3, data_first_4

    def data_num(self):
        data_1 = list(filter(lambda item: item[0] == 'LIN', self.df_data()))
        data_2 = list(filter(lambda item: item[0] == 'LIN NM', self.df_data()))
        data_3 = list(filter(lambda item: item[0] == 'CYC', self.df_data()))
        data_4 = list(filter(lambda item: item[0] == 'CYC NM', self.df_data()))
        return data_1, data_2, data_3, data_4

    def data_oxigen(self):
        data_oxigeno_1 = list(filter(lambda item: item[0] == 'LIN', self.df_oxigen()))
        data_oxigeno_2 = list(filter(lambda item: item[0] == 'LIN NM', self.df_oxigen()))
        data_oxigeno_3 = list(filter(lambda item: item[0] == 'CYC', self.df_oxigen()))
        data_oxigeno_4 = list(filter(lambda item: item[0] == 'CYC NM', self.df_oxigen()))
        return data_oxigeno_1, data_oxigeno_2, data_oxigeno_3, data_oxigeno_4

    def generate_smiles_and_names(self):
        data_first_1, data_first_2, data_first_3, data_first_4 = self.data_first()
        data_1, data_2, data_3, data_4 = self.data_num()
        data_oxigeno_1, data_oxigeno_2, data_oxigeno_3, data_oxigeno_4 = self.data_oxigen()
        if len(data_1) > 0:
            smile_lin = generate_sequence(data_first_1, data_1, self.peptide_length)
            names_lin = generate_names(data_first_1, data_1, self.peptide_length)
        elif len(data_1) == 0:
            smile_lin = list()
            names_lin = list()
        if len(data_2) > 0:
            smile_lin_nm = generate_sequence(data_first_2, data_2, self.peptide_length)
            names_lin_nm= generate_names(data_first_2, data_2, self.peptide_length)
        elif len(data_2) == 0:
            smile_lin_nm = list()
            names_lin_nm = list()
        if len(data_3) > 0:
            smile_cyc = generate_sequence(data_first_3, data_3, self.peptide_length)
            names_cyc = generate_names(data_first_3, data_3, self.peptide_length)
        elif len(data_3) == 0:
            smile_cyc = list()
            names_cyc = list()
        if len(data_4) > 0:
            smile_cyc_nm = generate_sequence(data_first_4, data_4, self.peptide_length)
            names_cyc_nm = generate_names(data_first_4, data_4, self.peptide_length)
        elif len(data_4) == 0:
            smile_cyc_nm = list()
            names_cyc_nm = list()
        
        smile_lin = list(map(lambda item: item + data_oxigeno_1[0][2], smile_lin))
        smile_lin_nm =list(map(lambda item: item + data_oxigeno_2[0][2], smile_lin_nm))
        smile_cyc = list(map(lambda item: item + data_oxigeno_3[0][2], smile_cyc))
        smile_cyc_nm = list(map(lambda item: item + data_oxigeno_4[0][2], smile_cyc_nm))

        self.smile_lin = smile_lin
        self.smile_lin_nm = smile_lin_nm
        self.smile_cyc = smile_cyc
        self.smile_cyc_nm = smile_cyc_nm

        libreria_lin = []
        if len(smile_lin) > 0:
            for i in smile_lin:
                libreria_lin.append("Linear")    

        libreria_lin_nm =[]
        if len(smile_lin_nm) > 0:
            for i in smile_lin_nm:
                    libreria_lin_nm.append("Linear Methylated")

        libreria_cyc =[]
        if len(smile_cyc) > 0:
            for i in smile_cyc:
                    libreria_cyc.append("Cyclic")

        libreria_cyc_nm =[]
        if len(smile_cyc_nm) > 0:
            for i in smile_cyc_nm:
                    libreria_cyc_nm.append("Cyclic Methylated")
        
        smile_final = smile_lin + smile_lin_nm + smile_cyc + smile_cyc_nm
        names_final = names_lin + names_lin_nm + names_cyc + names_cyc_nm
        libreria_final = libreria_lin + libreria_lin_nm + libreria_cyc + libreria_cyc_nm

        return smile_final, names_final, libreria_final

    def get_smiles(self):
        return self.smile_lin, self.smile_lin_nm, self.smile_cyc, self.smile_cyc_nm

    def generate_dataframe(self):

        smile_final, names_final, libreria_final = self.generate_smiles_and_names()
        
        #Descriptors.NumHAcceptors
        smiles = [ ]
        HBA = [ ]
        HBD = [ ]
        RB = [ ]
        LOGP = [ ]
        TPSA = [ ]
        MW = [ ] 

        for i in smile_final:
            smiles.append(Chem.MolFromSmiles(i))
            
        for i in smiles:
            HBA.append(Descriptors.NumHAcceptors(i))
            HBD.append(Descriptors.NumHDonors(i))
            RB.append(Descriptors.NumRotatableBonds(i))
            LOGP.append(Descriptors.MolLogP(i))
            TPSA.append(Descriptors.TPSA(i))
            MW.append(Descriptors.MolWt(i))

        columns = ["SMILES","NAME","LIBRARY", "HBA", "HBD", "RB", "LogP", "TPSA", "MW"]
        idx = [(i) for i,x in enumerate (smile_final,1)]
        data = [smile_final,names_final,libreria_final, HBA, HBD, RB, LOGP, TPSA, MW]
        data = np.transpose(data, axes=None)

        Database = pd.DataFrame(
                    data = data,
                    index = idx,
                    columns = columns)
        return Database
        