import numpy as np
import matplotlib.pyplot as plt
import utils as u
import evaluator.utils as eu

# data
gt_select = "gt"
traj_select = "sim__freq1_err3_user3"
gt = np.loadtxt(f"assets/groundtruth/{gt_select}.csv", skiprows=1)
traj = np.loadtxt(f"assets/trajectories/{traj_select}.csv", skiprows=1)
# interpolation
interpolations = eu.interpolation(gt, [traj])
# cdf
cdf = eu.normCDF(interpolations[0][0], interpolations[0][1])

cdf = cdf[cdf[:, 0].argsort()]
print(cdf)

