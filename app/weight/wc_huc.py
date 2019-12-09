import os
import numpy as np
import matplotlib.pyplot as plt
import refine
import imp
imp.reload(refine)
refine.reload()


hucStrLst = ['13', '15', '03']  # [ref, close, far]
hucLst = np.asarray(hucStrLst, dtype=int)-1

out = 'CONUSv4f1_y15_Forcing'

saveFolder = os.path.join(
    refine.kPath['dirResult'], 'weight', 'wc_huc')
rootOut = refine.kPath['OutSigma_L3_NA']
rootDB = refine.kPath['DB_L3_NA']
nCase = len(hucStrLst)
caseStr = ['train', 'close', 'far']

doOpt = []
# doOpt.append('plotMap')
doOpt.append('plotBox')
doOpt.append('plotVS')

#################################################
# plot box
if 'plotBox' in doOpt:
    dataBox = []
    for k in range(0, nCase):
        testName = 'hucn1_'+str(hucLst[k]+1).zfill(2)+'_v2f1'
        trainName = 'hucn1_'+str(hucLst[0]+1).zfill(2)+'_v2f1'
        out = trainName+'_y15_Forcing'
        syr = 2016
        eyr = 2017
        cX, cH = refine.funWeight.readWeightCancel(
            rootOut=rootOut, out=out, test=testName, syr=syr, eyr=eyr)
        rX = cX.sum(axis=2)/cX.shape[2]
        rH = cH.sum(axis=2)/cH.shape[2]
        dataBox.append([rX.mean(axis=0), rH.mean(axis=0)])

    fig = refine.funPost.plotBox(
        dataBox, title='box of weight cancellation',
        labelC=['train-'+hucStrLst[0], 'close-' +
                hucStrLst[1], 'far-'+hucStrLst[2]],
        labelS=['input->hidden', 'hidden->hidden'])
    saveFile = os.path.join(saveFolder, 'boxPlot'+str().join(hucStrLst))
    fig.savefig(saveFile)


#################################################
# plot MC dropout vs weight cancellation rate
if 'plotVS' in doOpt:
    fig, axes = plt.subplots(nCase, 2, figsize=(8, 10))
    for k in range(0, nCase):
        testName = 'hucn1_'+str(hucLst[k]+1).zfill(2)+'_v2f1'
        trainName = 'hucn1_'+str(hucLst[0]+1).zfill(2)+'_v2f1'
        out = trainName+'_y15_Forcing'
        syr = 2016
        eyr = 2017
        cX, cH = refine.funWeight.readWeightCancel(
            rootOut=rootOut, out=out, test=testName, syr=syr, eyr=eyr)
        rX = (cX.sum(axis=2)/cX.shape[2]).transpose()
        rH = (cH.sum(axis=2)/cH.shape[2]).transpose()

        ds = refine.classDB.DatasetPost(
            rootDB=rootDB, subsetName=testName, yrLst=range(syr, eyr+1))
        ds.readData(var='SMAP_AM', field='SMAP')
        ds.readPred(rootOut=rootOut, out=out, drMC=100,
                    field='LSTM', testBatch=100)
        statErr = ds.statCalError(predField='LSTM', targetField='SMAP')
        statSigma = ds.statCalSigma(field='LSTM')

        refine.funPost.plotVS(rX.mean(axis=1), statSigma.sigmaMC,
                              ax=axes[k, 0], plot121=False, title=caseStr[k])
        refine.funPost.plotVS(rH.mean(axis=1), statSigma.sigmaMC,
                              ax=axes[k, 1], plot121=False, title=caseStr[k])

        axes[k, 0].set_ylabel('sigmaMC')
        if k == nCase-1:
            axes[k, 0].set_xlabel('WCR input')
            axes[k, 1].set_xlabel('WCR hidden')
    fig.show()
    saveFile = os.path.join(saveFolder, 'WCRvsSigmaMC'+str().join(hucStrLst))
    fig.savefig(saveFile)
