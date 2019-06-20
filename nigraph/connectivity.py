### imports ###
import numpy as np
import pandas as pd
from typing import Tuple, Union
import random
from collections import defaultdict
from scipy.stats.stats import pearsonr

###


def look_around(point, parc):
    around = []
    [x, y, z] = point
    for i in range(max(0, x - 1), min(np.shape(parc)[0], x + 2)):
        for j in range(max(0, y - 1), min(np.shape(parc)[1], y + 2)):
            for k in range(max(0, z - 1), min(np.shape(parc)[2], z + 2)):
                label = parc[i, j, k]
                around.append(label)
    d = defaultdict(set)
    {d[around.count(i)].add(i) for i in around}
    return random.choice(list(d[max(d.keys())]))


def connectivity_matrix_diffusion(tract_data: np.ndarray, meta: pd.DataFrame, parc: np.ndarray) -> np.ndarray:
    labels = meta.index
    cm = np.zeros((len(labels), len(labels)))
    print("computing end connectivity matrix")
    for tract in tract_data:
        start = [tract[0].astype(int)[0], tract[0].astype(int)[1], tract[0].astype(int)[2]]
        end = [tract[-1].astype(int)[0], tract[-1].astype(int)[1], tract[-1].astype(int)[2]]

        if parc[start[0], start[1], start[2]] not in labels:
            start = look_around(start, parc)
        else:
            start = parc[start[0], start[1], start[2]]

        if not parc[end[0], end[1], end[2]] in labels:
            end = look_around(end, parc)
        else:
            end = parc[end[0], end[1], end[2]]

        if (start in labels) and (end in labels):
            cm[labels.index(start), labels.index(end)] += 1

    return cm


def connectivity_matrix_fmri(data: np.ndarray, meta: pd.DataFrame, parc: np.ndarray):
    tpoints = data.shape[0]
    parcels = len(meta)
    if len(parc.shape) > 1:
        parc = parc[:, 0]
    parcelated_dtseries = np.zeros((parcels, tpoints))
    if not len(parc) == data.shape[1]:
        data = data[:, :len(parc)]

    for area in range(len(meta.index)):
        area_dtseries = np.mean(data[:, parc == int(meta.index[area])], axis=1)
        parcelated_dtseries[area, :] = area_dtseries
    corr_mat = np.corrcoef(parcelated_dtseries)
    return corr_mat


def seed_map(roi, data: np.ndarray):
    roi_vals = np.mean(data[:, roi > 0], axis=1)
    s_map = np.apply_along_axis(lambda x: pearsonr(roi_vals, x), axis=0, arr=data)
    return s_map
