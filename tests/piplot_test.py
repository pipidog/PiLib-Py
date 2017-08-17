
'''
This file tests all the functions in the piplot module
'''
import PiLib as PLB
import numpy as np
import PiLib.piplot as PLBplt
import matplotlib.pyplot as plt

PLBdir=PLB.getdir()
test_task='fatband_plot'
test_folder='/home/pipidog/Desktop/' 
#test_folder='C:/Users/pipidog/Desktop/'
if test_task=='bicolormap':
    print('\n# test: bicolormap ======================\n')    
    PLBcmap={}    
    plt.figure(0)        
    PLBcmap['r']=PLBplt.bicolormap([0.8,0.8,0.8],[0.7,0.0,0.0],cmap_test='on')

    plt.figure(1)    
    PLBcmap['g']=PLBplt.bicolormap([0.8,0.8,0.8],[0.0,0.7,0.0],cmap_test='on')
    
    plt.figure(2)    
    PLBcmap['b']=PLBplt.bicolormap([0.8,0.8,0.8],[0.0,0.0,0.7],cmap_test='on')
    np.savez(PLBdir+'database/PLBcmap.npz',PLBcmap=PLBcmap)
elif test_task=='fatband_plot':
    print('\n# test: fatband_plot ======================\n')
    # set initial parameters 
    E_bound=[-4.5,+4.5]
    Ef=0
    state_grp=[[0],list(range(1,4)),list(range(4,9)),list(range(9,16))]
    k_label=['$\Gamma$','H','N','$\Gamma$','P','H']    
    cmap_index='b'
    desc='Eu-NM-SOC'
    # load fatband data (Eu-metal via abinit, state_info index should -1)
    # also, k_loc should also -1 because data are from scilab
    fatband=np.load(PLBdir+'tests/fatband.npz')
    PLBplt.fatband_plot(fatband['Ek'],fatband['Ek_weight'],0,fatband['kloc']-1,\
    state_grp,fatband['state_info'],k_label,E_bound,desc=desc,cmap_index=cmap_index) 
