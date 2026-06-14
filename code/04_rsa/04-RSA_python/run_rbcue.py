import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
# heatmap
subject_id = ["001", "002", "003", "004", "006", "007", "009", "010", "011", "015", "017", "018",
              "019", "021", "022", "023", "024", "025", "026", "027", "028", "029", "030", "031"]

res=[]
for subj in subject_id:

        string = f"/home/medicaldata/LJData/SR_ana/analysis_res/rsa/rbCue/stats.{subj}_REML.nii"

        np.savetxt(f"/home/image030/{subj}_rdm.csv",np.random.random((3,3)))
        # res.append(string)

print(res)