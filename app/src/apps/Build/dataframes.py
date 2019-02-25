import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------------
# Dataset amino_first
# ---------------------------------------------------------------------------------
amino_first_dataframe = pd.DataFrame(
    {
        "NAME":  "L-ALA              L-CYS               L-ASP                  L-GLU                   L-PHE                      L-HIS                        L-ILE                         L-LYS                   L-LEU                    L-MET                   L-ASN                   L-PRO            L-GLN                    L-ARG                       L-SER               L-THR                      L-VAL                  L-TRP                              L-TYR                         GLY".split(),
        "LIN":   "N[C@@H](C)C        N[C@@H](CS)C        N[C@H](C(O)O)CC        N[C@H](C(O)O)CCC        N[C@@H](Cc3ccccc3)C        N[C@@H](Cc4[nH]cnc4)C        N[C@@H]([C@@H](C)CC)C         N[C@@H](CCCCN)C         N[C@@H](CC(C)C)C         N[C@@H](CCSC)C          N[C@@H](CC(N)O)C        N1CCC[C@H]1C     N[C@@H](CCC(N)O)C        N[C@@H](CCCNC(N)N)C         N[C@@H](CO)C        N[C@@H]([C@H](O)C)C        N[C@@H](C(C)C)C        N[C@@H](Cc5c[nH]c6c5cccc6)C        N[C@@H](Cc7ccc(O)cc7)C        NCC".split(),
        "LIN NM":"N(C)(C)[C@@H](C)C  N(C)(C)[C@@H](CS)C  N(C)(C)[C@H](C(O)O)CC  N(C)(C)[C@H](C(O)O)CCC  N(C)(C)[C@@H](Cc3ccccc3)C  N(C)(C)[C@@H](Cc4[nH]cnc4)C  N(C)(C)[C@@H]([C@@H](C)CC)C   N(C)(C)[C@@H](CCCCN)C   N(C)(C)[C@@H](CC(C)C)C   N(C)(C)[C@@H](CCSC)C    N(C)(C)[C@@H](CC(N)O)C  N1(C)CCC[C@H]1C  N(C)(C)[C@@H](CCC(N)O)C  N(C)(C)[C@@H](CCCNC(N)N)C   N(C)(C)[C@@H](CO)C  N(C)(C)[C@@H]([C@H](O)C)C  N(C)(C)[C@@H](C(C)C)C  N(C)(C)[C@@H](Cc5c[nH]c6c5cccc6)C  N(C)(C)[C@@H](Cc7ccc(O)cc7)C  N(C)(C)CC".split(),
        "CYC NM":"N%99(C)[C@@H](C)C  N%99(C)[C@@H](CS)C  N%99(C)[C@H](C(O)O)CC  N%99(C)[C@H](C(O)O)CCC  N%99(C)[C@@H](Cc3ccccc3)C  N%99(C)[C@@H](Cc4[nH]cnc4)C  N%99(C)[C@@H]([C@@H](C)CC)C   N%99(C)[C@@H](CCCCN)C   N%99(C)[C@@H](CC(C)C)C   N%99(C)[C@@H](CCSC)C    N%99(C)[C@@H](CC(N)O)C  N1%99CCC[C@H]1C  N%99(C)[C@@H](CCC(N)O)C  N%99(C)[C@@H](CCCNC(N)N)C   N%99(C)[C@@H](CO)C  N%99(C)[C@@H]([C@H](O)C)C  N%99(C)[C@@H](C(C)C)C  N%99(C)[C@@H](Cc5c[nH]c6c5cccc6)C  N%99(C)[C@@H](Cc7ccc(O)cc7)C  N%99(C)CC".split(),
        "CYC":   "N%99[C@@H](C)C     N%99[C@@H](CS)C     N%99[C@H](C(O)O)CC     N%99[C@H](C(O)O)CCC     N%99[C@@H](Cc3ccccc3)C     N%99[C@@H](Cc4[nH]cnc4)C     N%99[C@@H]([C@@H](C)CC)C      N%99[C@@H](CCCCN)C      N%99[C@@H](CC(C)C)C      N%99[C@@H](CCSC)C       N%99[C@@H](CC(N)O)C     N1%99CCC[C@H]1C  N%99[C@@H](CCC(N)O)C     N%99[C@@H](CCCNC(N)N)C      N%99[C@@H](CO)C     N%99[C@@H]([C@H](O)C)C     N%99[C@@H](C(C)C)C     N%99[C@@H](Cc5c[nH]c6c5cccc6)C     N%99[C@@H](Cc7ccc(O)cc7)C     N%99CC".split(),
    }
)
amino_first_dataframe = amino_first_dataframe.set_index('NAME')

# ---------------------------------------------------------------------------------
# Dataset
# ---------------------------------------------------------------------------------
df = pd.DataFrame(
    {
        "NAME":  "L-ALA           L-CYS            L-ASP               L-GLU                L-PHE                   L-HIS                     L-ILE                     L-LYS               L-LEU                L-MET              L-ASN                L-PRO         L-GLN                 L-ARG                    L-SER            L-THR                   L-VAL               L-TRP                           L-TYR                      GLY".split(),
        "LIN":   "(N[C@@H](C)C    (N[C@@H](CS)C    (N[C@H](C(O)O)CC    (N[C@H](C(O)O)CCC    (N[C@@H](Cc3ccccc3)C    (N[C@@H](Cc4[nH]cnc4)C    (N[C@@H]([C@@H](C)CC)C    (N[C@@H](CCCCN)C    (N[C@@H](CC(C)C)C    (N[C@@H](CCSC)C    (N[C@@H](CC(N)O)C    (N1CCC[C@H]1C (N[C@@H](CCC(N)O)C    (N[C@@H](CCCNC(N)N)C     (N[C@@H](CO)C    (N[C@@H]([C@H](O)C)C    (N[C@@H](C(C)C)C    (N[C@@H](Cc5c[nH]c6c5cccc6)C    (N[C@@H](Cc7ccc(O)cc7)C    (NCC" .split(),
        "LIN NM":"(N(C)[C@@H](C)C (N(C)[C@@H](CS)C (N(C)[C@H](C(O)O)CC (N(C)[C@H](C(O)O)CCC (N(C)[C@@H](Cc3ccccc3)C (N(C)[C@@H](Cc4[nH]cnc4)C (N(C)[C@@H]([C@@H](C)CC)C (N(C)[C@@H](CCCCN)C (N(C)[C@@H](CC(C)C)C (N(C)[C@@H](CCSC)C (N(C)[C@@H](CC(N)O)C (N1CCC[C@H]1C (N(C)[C@@H](CCC(N)O)C (N(C)[C@@H](CCCNC(N)N)C  (N(C)[C@@H](CO)C (N(C)[C@@H]([C@H](O)C)C (N(C)[C@@H](C(C)C)C (N(C)[C@@H](Cc5c[nH]c6c5cccc6)C (N(C)[C@@H](Cc7ccc(O)cc7)C (N(C)CC".split(),
        "CYC NM":"(N(C)[C@@H](C)C (N(C)[C@@H](CS)C (N(C)[C@H](C(O)O)CC (N(C)[C@H](C(O)O)CCC (N(C)[C@@H](Cc3ccccc3)C (N(C)[C@@H](Cc4[nH]cnc4)C (N(C)[C@@H]([C@@H](C)CC)C (N(C)[C@@H](CCCCN)C (N(C)[C@@H](CC(C)C)C (N(C)[C@@H](CCSC)C (N(C)[C@@H](CC(N)O)C (N1CCC[C@H]1C (N(C)[C@@H](CCC(N)O)C (N(C)[C@@H](CCCNC(N)N)C  (N(C)[C@@H](CO)C (N(C)[C@@H]([C@H](O)C)C (N(C)[C@@H](C(C)C)C (N(C)[C@@H](Cc5c[nH]c6c5cccc6)C (N(C)[C@@H](Cc7ccc(O)cc7)C (N(C)CC".split(),
        "CYC":   "(N[C@@H](C)C    (N[C@@H](CS)C    (N[C@H](C(O)O)CC    (N[C@H](C(O)O)CCC    (N[C@@H](Cc3ccccc3)C    (N[C@@H](Cc4[nH]cnc4)C    (N[C@@H]([C@@H](C)CC)C    (N[C@@H](CCCCN)C    (N[C@@H](CC(C)C)C    (N[C@@H](CCSC)C    (N[C@@H](CC(N)O)C    (N1CCC[C@H]1C (N[C@@H](CCC(N)O)C    (N[C@@H](CCCNC(N)N)C     (N[C@@H](CO)C    (N[C@@H]([C@H](O)C)C    (N[C@@H](C(C)C)C    (N[C@@H](Cc5c[nH]c6c5cccc6)C    (N[C@@H](Cc7ccc(O)cc7)C    (NCC" .split(),
    }
)
df = df.set_index('NAME')

# ---------------------------------------------------------------------------------
# Dataset oxigen
# ---------------------------------------------------------------------------------
oxigen = pd.DataFrame(
    {
        "NAME":  "  2         3          4             5              6".split(),
        "LIN":   "  (O)=O)=O   (O)=O)=O)=O  (O)=O)=O)=O)=O   (O)=O)=O)=O)=O)=O  (O)=O)=O)=O)=O)=O)=O" .split(),
        "LIN NM":"  (O)=O)=O   (O)=O)=O)=O  (O)=O)=O)=O)=O   (O)=O)=O)=O)=O)=O  (O)=O)=O)=O)=O)=O)=O".split(),
        "CYC NM":"  %99=O)=O    %99=O)=O)=O %99=O)=O)=O)=O   %99=O)=O)=O)=O)=O  %99=O)=O)=O)=O)=O)=O".split(),
        "CYC":   "  %99=O)=O    %99=O)=O)=O %99=O)=O)=O)=O   %99=O)=O)=O)=O)=O  %99=O)=O)=O)=O)=O)=O" .split(),
    }
)
oxigen = oxigen.set_index('NAME')
