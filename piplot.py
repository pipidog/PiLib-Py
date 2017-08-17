import numpy as np
import sys, os
import matplotlib.pyplot as plt

'''
<< bicolormap >>
Description ===================================================================
**** Purpose ****
this function can generate a sequential bicolor colormap
**** Variables ****
[ini_rgb]: list, 1x3 
<= the initial RGB (for lower values) index specified by three real values.
   e.g: [1,0,0] => red, e.g: [0,0,0] => black, e.g: [1,1,1] => white
[final_rgb]: list, 1x3
<= the final RGB (for higher values) index specified by three real values.
   e.g: [1,0,0] => red, e.g: [0,0,0] => black, e.g: [1,1,1] => white
[cmap_test]: 1x1, string, 'on'/'off', default='off'
<= whether to output a figure shows the colormap. If 'on', a figure will 
   show up to demonstrate the colormap
**** Version ****
2/13/2017: first version
**** Comment ****
'''    

def bicolormap(ini_rgb,final_rgb,cmap_test='off'):
    import colormap 
    int_rgb=((np.array(ini_rgb)+np.array(final_rgb))/2).tolist()    
    color_var=(np.array([ini_rgb,int_rgb,final_rgb]).transpose()).tolist()
    
    c=colormap.Colormap()            
    mycmap = c.cmap( {'red':color_var[0], 'green':color_var[1], 'blue':color_var[2]})      
    if cmap_test=='on':    
        c.test_colormap(mycmap)
        
    return mycmap

'''
<<  >>
Description ===================================================================
**** Purpose ****
this function can generate a sequential bicolor colormap
**** Variables ****
[ini_rgb]: list, 1x3 
<= the initial RGB (for lower values) index specified by three real values.
   e.g: [1,0,0] => red, e.g: [0,0,0] => black, e.g: [1,1,1] => white
[final_rgb]: list, 1x3
<= the final RGB (for higher values) index specified by three real values.
   e.g: [1,0,0] => red, e.g: [0,0,0] => black, e.g: [1,1,1] => white
[cmap_test]: 1x1, string, 'on'/'off', default='off'
<= whether to output a figure shows the colormap. If 'on', a figure will 
   show up to demonstrate the colormap
**** Version ****
2/13/2017: first version
**** Comment ****
''' 
def fatband_plot(Ek,Ek_weight,Ef,k_div,state_grp,state_info,k_label=[],\
E_bound=[],desc='',ini_fig_num=0,marker_size=8,cmap_index='b'):

    # give input parameter default values
    if (k_label==[]):
       for n in range(0,len(k_div)):
           k_label.append('k'+str(n))
    
    if (E_bound==[]):
        E_bound=[np.min(Ek),np.max(Ek)]
           
    # load colormap for colorbar   
    PLBdir=__file__.replace("\\","/")[0:-9]
    PLBcmap=np.load(PLBdir+'database/PLBcmap.npz')['PLBcmap'].tolist()
      
    #organize data to scatter form
    x=np.tile(np.linspace(0,Ek.shape[1]-1,Ek.shape[1]),[1,Ek.shape[0]]).transpose()
    y=Ek.flatten()-Ef
    
    # screen out data out of E_bound
    
    for n in range(0,len(state_grp)+1):
        if (n<len(state_grp)):
            c=np.zeros(len(Ek_weight[:,:,0].flatten()))
    
            # sum over projected state group       
            for m in state_grp[n]:
                c=c+Ek_weight[:,:,m].flatten()
                
            # build colormap for band plotting
            c_int=np.linspace(min(c),max(c),32+1) 
    
            colors=np.zeros([32,4])     
            ini_rgb=[0.8,0.8,0.8]
            if cmap_index=='r':
                cmap=np.array([ini_rgb,[0.7,0.0,0.0]])
            elif cmap_index=='g':
                cmap=np.array([ini_rgb,[0.0,0.7,0.0]])
            elif cmap_index=='b':
                cmap=np.array([ini_rgb,[0.0,0.0,0.7]])
                
            
            for m in range(0,32):
                colors[m,0:3]=m*(cmap[1,:]-cmap[0,:])/31+cmap[0,:]       
            
            colors[:,3]=1   
            
    
            # prepare colorbar information 
            plt.figure(n+ini_fig_num+1)
            cbar_obj = plt.contourf([[0,0],[0,0]],\
            np.linspace(min(c),max(c),32), cmap=PLBcmap[cmap_index])    
            plt.clf()
            
            # plot colorbar        
            plt.colorbar(cbar_obj) 
    
            # plot fatband        
            plt.gca().set_color_cycle(colors)
            for m in range(0,32):
                ind=np.nonzero((c>=c_int[m]) & (c<c_int[m+1]))
                plt.plot(x[ind],y[ind],'o',lw=0,markeredgecolor='none',markersize=marker_size)
                
            # show fatband state info
            print('projected states in figure-%d:' % (n+1))
            print(state_info[state_grp[n]])
                
        else:
            # plot normal band structure            
            plt.figure(0)
            plt.plot(np.linspace(0,Ek.shape[1]-1,Ek.shape[1]),Ek.transpose(),'b',lw=2)

                
        # plot k divider    
        for m in k_div[1:-1]:
            plt.plot(m*np.ones(10),np.linspace(np.min(y),np.max(y),10),'k--')
        
        # plot Fermi level    
        plt.plot(np.linspace(0,np.max(x),10),np.zeros(10),'r--')

        # tweak figure
        plt.xlabel('k-path',fontsize=18)
        plt.xticks(k_div,k_label,fontsize=20)
        plt.yticks(fontsize=20)
        plt.ylabel('Energy (eV)',fontsize=18)
        plt.title(desc+' / band ',fontsize=18)
        plt.xlim(0,np.max(x))    
        plt.ylim( E_bound[0],E_bound[1])

    plt.show()   

        



