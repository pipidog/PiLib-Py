'''
core module of DFTPPT
Currently, DFTPPT supports the following code and functions
1. quantum espresso
    1). band structure plot
    2). fatband structure plot
    3). PDOS plot with respect to a series of selected atoms
    4). PDOS plot with respect to all suborbitals of a particular atom
2. abinit
    1). band structure plot
3. wien2k

4. elk

5. Wannier Tools

'''
import sys, os
import PiLib as PLB
import numpy as np

class dftppt:
    def __init__(self,wdir):
        self.wdir=wdir
    
    # abinit methods ---------------------------
    def getabt(task,dset):
		if task=='band':
			flist=os.listdir(self.wdir)
         for fname in flist:
             if fname.find('DS'+str(dset)+'_EIG')!=-1:
                 # read band data
                 break
			
		elif task=='fatband':
			
		elif task=='pdos'
        
        
    def outabt(task,dset):
        
    def plotabt(task,dset):
    
    
    
    # quantum espresso methods -------------------   
    def getqe(task):

    # wien2k methods -----------------------------
    def getw2k(task):
    
    # Wannier tools methods ----------------------
    def getwt(task):

    # elk methods --------------------------------
    def getelk(task):
        
    
        
        
    
