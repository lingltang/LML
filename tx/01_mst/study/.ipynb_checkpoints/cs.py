import pandas as pd
import numpy as np

dic = {'Ling':99, 'Mo':27, 'Yu':32}
pdarr2 = pd.Series(data=dic, dtype=float)
pdarr2.reindex(index=['Np', 'Wsl', 'Hlh'])

pdarr4 = pd.DataFrame([[2,4,8],[3,5,9]])
pdarr4
