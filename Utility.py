import numpy as np
import scipy.sparse
import sys
'''
<< spmat >>
Description ===================================================================
**** Purpose ****
convert a matrix to PiLab sparse format and vice versa
**** Variables ****
[A]: nxn / nx3
<= input matrix, can be full or sparse 
[A_out]: nxn / nx3
=> output matrix, can be full or sparse
if A is in PiLab sparse format, A_out is full. A_out is full matrix.
if A is full matrix, A_out is sparse.
**** Version ****
11/17/2016: first version
**** Common ****
'''
def spmat(A):
    if (A.shape[1]==3) & \
    (np.sum((np.abs(A[:,0:1]-np.round(A[:,0:1]))))==0) &\
    (A[0,2]==0) &\
    (len(np.nonzero(A[1:,0].real>=A[0,0].real)[0])==0) &\
    (len(np.nonzero(A[1:,1].real>=A[0,1].real)[0])==0):
        inp_type='sp'
    else:
        inp_type='full'
          
    if inp_type=='full':
        A_nz=scipy.sparse.find(A)   
        A_out=np.zeros((len(A_nz[0])+1,3))*(1j)
        A_out[0,:]=[A.shape[0],A.shape[1],0]
        A_out[1:len(A_nz[0])+2,:]=np.transpose(A_nz)
        
        return A_out
    elif inp_type=='sp':
        A_out=np.zeros((np.round(A[0,0:1+1].real)))*(1j)    
        for n in range(1,A.shape[0]):           
            A_out[np.round(A[n,0].real),np.round(A[n,1].real)]=A[n,2]
            
        return A_out
 
 
def clear_all():
    """Clears all the variables from the workspace of the spyder application."""
    gl = globals().copy()
    for var in gl:
        if var[0] == '_': continue
        if 'func' in str(globals()[var]): continue
        if 'module' in str(globals()[var]): continue

        del globals()[var]
    
    if __name__ == "__main__":
        clear_all()
        
''' 
search for the line number where a particular keyword appears in a file
obtained by file.readlines()
'''

def grep(file_line,key_str):
    key_line=[]
    for n in range(0,len(file_line)):
        if file_line[n].find(key_str)!=-1:
            key_line.append(n)

    return key_line