'''
This file tests all the functions in the IO module
'''

import numpy as np
import scipy.sparse
import PiLib.IO as PLBIO
import matplotlib.pyplot as plt

test_task='printer'
test_folder='/home/pipidog/Desktop/' 
#test_folder='C:/Users/pipidog/Desktop/'
if test_task=='printer':
    print('\n# test: printer ======================\n')
    file=open(test_folder+'test.txt','w')
    # integer
    A=(np.round(100*(np.random.rand(9,5)))).astype(int)
    PLBIO.printer(file,'this is a integer matrix',A)
    # real
    A=100*(np.random.rand(9,5))
    PLBIO.printer(file,'this is a real matrix',A)
    # complex
    A=100*(np.random.rand(9,5)+np.random.rand(9,5)*1j)
    PLBIO.printer(file,'this is a complex matrix',A)
    # sparse
    A=np.random.rand(3,3)+np.random.rand(3,3)*1j
    A=scipy.sparse.coo_matrix(A)    
    PLBIO.printer(file,'this is a sparse matrix',A)
    # string
    A=(np.random.rand(3, 3)).astype(str)    
    PLBIO.printer(file,'this is a string matrix',A)
    
    file.close()
elif test_task=='scanner':
    print('\n# test: scanner =======================\n')
    file=open(test_folder+'test.txt','r')
    var_name=['integer','real','complex','sparse','string']
    PLB_var={}
    for n in range(0,len(var_name)):
        print(var_name[n])
        PLB_var[var_name[n]]=PLBIO.scanner(file)
        print(PLB_var[var_name[n]])
    file.close()
elif test_task=='str_restore':
    print('\n# test: str_restore ====================\n')
    a='how # are # you # fine # thank # you #'
    b=PLBIO.str_restore(a)
    print(b)
elif test_task=='atom_label':
    print('\n# test: atom_label =====================\n')
    atom_input=['2*Sr','1*Re','1*Au','6*O']
    atom_output=PLBIO.atom_label(atom_input)
    print(atom_output)
elif test_task=='print_xsf':
    print('\n# test: print_xsf =====================\n')
    file=open(test_folder+'test.xsf','w')    
    atom_list=['2*Sr','1*Re','1*Au','6*O']
    atom_pos=np.random.rand(10,3)
    lat_vec=np.random.rand(3,3)
    PLBIO.print_xsf(file,lat_vec,atom_pos,atom_list)           
    file.close()
elif test_task=='print_xyz':
    print('\n# test: print_xyz =====================\n')
    file=open(test_folder+'test.xyz','w')
    atom_list=['2*Sr','1*Re','1*Au','6*O']
    atom_pos=np.random.rand(10,3)
    PLBIO.print_xyz(file,atom_pos,atom_list)           
    file.close()    
elif test_task=='dir_path':
    print('\n# test: dir_path ======================\n')
    work_dir='/home/pipidog'
    work_dir=PLBIO.dir_path(work_dir)
    print(work_dir)


