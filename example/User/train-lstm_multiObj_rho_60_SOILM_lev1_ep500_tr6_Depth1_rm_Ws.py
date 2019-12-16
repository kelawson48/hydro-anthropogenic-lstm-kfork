from hydroDL import wrapMaster, train
from app.common import default
import os

cDir = os.path.dirname(os.path.abspath(__file__))
cDir = r'/mnt/sdc/SUR_VIC/'

# define training options
optData = default.update(
    default.optDataSMAP,
    rootDB='/mnt/sdc/SUR_VIC/input_VIC/',
    varT=[
    'APCP_FORA', 'DLWRF_FORA', 'DSWRF_FORA', 'TMP_2_FORA', 'SPFH_2_FORA',
    'VGRD_10_FORA', 'UGRD_10_FORA', 'PEVAP_FORA', 'PRES_FORA'
],
    varC=[
    'DEPTH_1', 'Ds', 'Ds_MAX', 'EXPT_1', 'INFILT'
],
    # target=['SOILM_0-100_VIC', 'SSRUN_VIC','EVP_VIC'],
    target='SOILM_lev1_VIC',
    subset='CONUS_VICv16f1',
    tRange=[20100401, 20160401])
optModel = default.optLstm
optLoss = default.optLossRMSE
optTrain = default.update(default.optTrainSMAP, miniBatch=[100, 60], nEpoch=500)
out = os.path.join(cDir, 'output_VIC/CONUS_v16f1_SOILM_lev1_rho60_ep500_tr6_Depth1_rm_Ws')
masterDict = wrapMaster(out, optData, optModel, optLoss, optTrain)

# train
train(masterDict)
# runTrain(masterDict, cudaID=2, screen='LSTM-multi')