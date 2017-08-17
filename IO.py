import numpy as np
import scipy.sparse
import sys
import matplotlib.pyplot as plt
'''
<< printer >>
Description ===================================================================
**** Purpose ****
print a data array in a PiLib standard format
**** Variables ****
[file]: 1x1, integer
<= the file object of the print out file 
[desc]: string
<= a string describes the content of the data
[A]: np.array, nxm, real/complex/sparse/string
<= the data array to be print out
**** Version ****
11/17/2016: first version
**** Comment ****
This function wiil atuomaically choose output type based on the data type.
'''
def printer(file,desc,A):

    A_dim=A.shape
    if (len(A_dim)==[1]):
        A_dim=[A.shape[0],1]
        
    file.write(' \n')
    def __row_print(print_format,A_row):
        for n in range(0,len(A_row)):
            file.write(print_format % (A_row[n]))
            
        file.write('\n') 
        return None
        
    if (A.dtype==np.int) & (scipy.sparse.issparse(A)==False): # integer
        order=0
        A=A*10**(-order)
        
        # print initial information
        file.write('============= PiLib Variable =============\n')
        file.write('%s\n' % desc)
        file.write('ORDER= %4d, SIZE=[%6d,%6d], TYPE=%s\n'% (order,A_dim[0],A_dim[1],'INTEGER'))
        file.write('\n')
        # print column index        
        file.write('      ')
        __row_print('  %6d',np.arange(0,A_dim[1]))   
        # print data matrix
        for n in range(0,A_dim[0]):
            file.write('%6d' % (n))
            __row_print('  %6d',A[n,:])
        
        return None 
        
    elif (A.dtype==np.float) & (scipy.sparse.issparse(A)==False): # real
        order=np.floor(np.log10(np.max(np.abs(A))))
        A=A*10**(-order)
        
        # print initial information
        file.write('============= PiLib Variable =============\n')
        file.write('%s\n' % desc)
        file.write('ORDER= %4d, SIZE=[%6d,%6d], TYPE=%s\n'% (order,A_dim[0],A_dim[1],'REAL'))
        file.write('\n')
        # print column index        
        file.write('      ')
        __row_print('  %10d',np.arange(0,A_dim[1]))   
        # print data matrix
        for n in range(0,A_dim[0]):
            file.write('%6d' % (n))
            __row_print('  %10.6f',A[n,:])
            
        return None
    elif (A.dtype==np.complex) & (scipy.sparse.issparse(A)==False): # complex
        order=np.floor(np.log10(np.max(np.abs(A))))
        A=A*10**(-order)
        B=np.zeros((A_dim[0],A_dim[1]*2))
        B[:,range(0,2*A_dim[1],2)]=A.real
        B[:,range(1,2*A_dim[1],2)]=A.imag
        
        # print initial information
        file.write('============= PiLib Variable =============\n')
        file.write('%s\n' % desc)
        file.write('ORDER= %4d, SIZE=[%6d,%6d], TYPE=%s\n'% (order,A_dim[0],A_dim[1],'COMPLEX'))
        file.write('\n')
        # print column index        
        file.write('        ')
        __row_print('%20d',np.arange(0,A_dim[1]))
        # print data matrix
        for n in range(0,A_dim[0]):
            file.write('%6d  ' % (n))
            __row_print('%10.6f',B[n,:])
            
        return None
    elif scipy.sparse.issparse(A):  # sparse
        A_nz=scipy.sparse.find(A)   
        A_out=np.zeros((len(A_nz[0])+1,3))*(1j)
        A_out[0,:]=[A.shape[0],A.shape[1],0]
        A_out[1:len(A_nz[0])+2,:]=np.transpose(A_nz)
        A=A_out        
            
        order=np.floor(np.log10(np.max(np.abs(A[:,2]))))         
        A[:,2]=A[:,2]*10**(-order)        
        
        # print initial information
        file.write('============= PiLib Variable =============\n')
        file.write('%s\n' % desc)
        file.write('ORDER= %4d, SIZE=[%6d,%6d], TYPE=%s\n'%\
        (order,len(A_nz[1]),3,'SPARSE'))
        file.write('\n')
        # print column index        
        file.write('  %6d  %6d  %20d\n' % (0,1,2))
        # print data matrix
        for n in range(0,len(A[:,0])-1):
            file.write('  %6d  %6d  %10.6f%10.6f\n' % (np.round(A[n,0].real)\
            ,np.round(A[n,1].real),A[n,2].real,A[n,2].imag))
            
        return None
    else :  # string
        order=0
        # print initial information
        file.write('============= PiLib Variable =============\n')
        file.write('%s\n' % desc)
        file.write('ORDER= %4d, SIZE=[%6d,%6d], TYPE=%s\n'
        % (order,A_dim[0],A_dim[1],'STRING'))
        file.write('\n\n')
        for n in range(0,A_dim[0]):
            for m in range(0,A_dim[1]):
                file.write('%s # ' % A[n,m])
            
            file.write('\n')
            
        return None

'''
<< scanner >>
Description ===================================================================
**** Purpose ****
read data from a file written in PiLib standard format
**** Variables ****
[file]: 1x1, file object
<= the file object of the print out file 
[mat]: np.array, nxm, int/real/complex/sparse
**** Version ****
11/17/2016: first version
**** Comment ****
This function wiil atuomaically choose generated data type based on read data.
'''

def scanner(file):
    def __head_scanner(file):
            file.readline()
            file.read(6)
            order=int(file.read(5))
            file.read(8)
            mat_size=[int(file.read(6))]
            file.read(1)
            mat_size.append(int(file.read(6)))
            file.read(8)
            mat_type=file.readline()[0:-1]
            header={'order':order,'size':mat_size,'type':mat_type}
            return(header)
    
    def __data_scanner(file,header):
        [file.readline() for n in range(0,2)]
        if header['type']=='REAL':
            mat=np.zeros(header['size'])
            for n in range(0,header['size'][0]):
                mat[n,:]=np.array([float(m) for m in file.readline().split()][1:])
            
            mat=mat*10**(header['order'])
            
        elif header['type']=='COMPLEX':
            mat=np.zeros(header['size'])*(0+0j)
            for n in range(0,header['size'][0]):
                line=np.array([float(m) for m in file.readline().split()][1:])
                mat[n,:]=line[0::2]+line[1::2]*1j
            
            mat=mat*10**(header['order'])

        elif header['type']=='INTEGER':
            mat=np.zeros(header['size'])
            for n in range(0,header['size'][0]):
                mat[n,:]=np.array([int(m) for m in file.readline().split()][1:])
                
            mat=mat*10**(header['order'])
            
        elif header['type']=='SPARSE':
            mat_size=[int(p) for p in [float(m) for m in file.readline().split()][0:2]]            
            mat=np.zeros(mat_size)*(0+0j)
            for n in range(1,header['size'][0]):
                line=np.array([float(m) for m in file.readline().split()])
                mat[int(line[0].real),int(line[1].real)]=line[2]+line[3]*1j
            
            mat=scipy.sparse.coo_matrix(mat*10**(header['order'])) 
            
        elif header['type']=='STRING':
            mat=np.zeros(header['size']).astype(str)
            for n in range(0,header['size'][0]):
                tmp=file.readline()
                beg=0
                text_mat=[]
                for m in range(0,header['size'][1]):
                    ind=tmp.find(' # ',beg)
                    text_mat=text_mat+[tmp[beg:ind]]
                    beg=ind+3
                    
                mat[n,:]=text_mat
            
        return mat
        
    # read a single PiLib Variable
    while True:
        line=file.readline()
        if line.find('PiLib Variable')!=-1:
            mat=__data_scanner(file,__head_scanner(file))
            return mat 
            break
        elif line=='':
            break
            return None

'''
<< str_restore >>
Description ===================================================================
**** Purpose ****
this function will restore the string matrix from PiLib format where each
string matrix element is separated b # to a list
**** Variables ****
[str_inp]: string, 1x1, a string with PiLib string matrix format
<= e.g. 'test1 # test2 #'
[str_out]: list, 1xn, 
=> a list of string
**** Version ****
12/7/2016: first version
**** Comment ****
'''
def str_restore(str_inp):
    tot_str=str_inp.count('#')
    if tot_str==0:
        sys.exit('Error: str_restore, number of # is zero!')
        
    hashtag_in=0
    str_out=[]
    for n in range(0,tot_str):        
        hashtag_out=str_inp.find('#',hashtag_in)
        str_out.append(str_inp[hashtag_in:hashtag_out-1])
        hashtag_in=hashtag_out+2
    
    return str_out    

'''
<< atom_label >>
Description ===================================================================
**** Purpose ****
using PiLab atom species input format, this function will convert to normal
string list. 
**** Variables ****
[atom_input]: list, 1xn, strings, 
<= input of the atoms using PiLib standard format
   e.g: ['2*Sr','1*Re','1*Au','6*O']
[atom_output]: list, 1xn, strings
=> output of the atom labels in standard list format
   e.g: ['Sr', 'Sr', 'Re', 'Au', 'O', 'O', 'O', 'O', 'O', 'O']
**** Version ****
12/8/2016: first version
**** Comment ****
'''
def atom_label(atom_input):
    atom_output=[]    
    for atom in atom_input:
        sub_atom_tot=atom[0:atom.find('*')]
        sub_atom_type=atom[atom.find('*')+1:]
        atom_output.extend([sub_atom_type]*int(sub_atom_tot))
        
    return atom_output
            
'''
<< print_xsf >>
Description ===================================================================
**** Purpose ****
print xsf structure file based on input data
**** Variables ****
[file]: 1x1, file object
<= the file object of the print out file 
[lat_vec]: np.array, 3x3, real
<= lattice row vectors 
[atom_pos]: np.array, nx3, real
<= atom positions in cartisian
[atom_list]: list, nx1, string
<= atom label in PiLib format, e.g.:['2*Sr','1*Re','1*Au','6*O']
**** Version ****
12/08/2016: first version
**** Comment ****
'''
def print_xsf(file,lat_vec,atom_pos,atom_list):
    atom_list=atom_label(atom_list)  
    file.write('%s\n' % 'CRYSTAL')
    file.write('  %s\n' % 'PRIMITIVE')
    [file.write('    %9.5f  %9.5f  %9.5f\n' % tuple(row)) for row in lat_vec.tolist()]
    file.write('  %s\n' % 'PRIMCOORD')
    file.write('    %d\n' % len(atom_list))
    for n in range(0,len(atom_list)):
        row=atom_pos[n].tolist()
        row.insert(0,atom_list[n])
        file.write('    %2s  %9.5f  %9.5f  %9.5f\n' % tuple(row))
           
    file.close()
    return None
    
'''
<< print_xyz >>
Description ===================================================================
**** Purpose ****
print xyz moleculear structure file based on input data
**** Variables ****
[file]: 1x1, file object
<= the file object of the print out file 
[atom_pos]: np.array, nx3, real
<= atom positions in cartisian
[atom_list]: list, nx1, string
<= atom label in PiLib format, e.g.:['2*Sr','1*Re','1*Au','6*O']
**** Version ****
12/12/2016: first version
**** Comment ****
'''
def print_xyz(file,atom_pos,atom_list):
    atom_list=atom_label(atom_list) 
    file.write('%d\n' % len(atom_list))
    file.write('%s\n' % 'comment line')
    for n in range(0,len(atom_list)):
        row=atom_pos[n].tolist()
        row.insert(0,atom_list[n])
        file.write('    %2s  %9.5f  %9.5f  %9.5f\n' % tuple(row))
           
    file.close()
    return None    
    
'''
<< dir_path >>
Description ===================================================================
**** Purpose ****
add '/' to the directory path
**** Variables ****
[path]: string, 1x1, 
<= the directory of the path 
**** Version ****
12/12/2016: first version
**** Comment ****
'''    
def dir_path(path):
    if (path[-1]!='/') & (path[-1]!='\\') :
        path=path+'/'
        
    return path
    

'''
<< stdout_file >>
Description ===================================================================
**** Purpose ****
this function directs the stdout to a particular file
**** Variables ****
[filename]: string, 1x1 
<= the file name of the output file (including the path)
[command]: string, 1x1
<= the command to execute in console 
[Output file]: 
=> An output file will be shown contains the stdout of executing the command
**** Version ****
2/12/2017: first version
**** Comment ****
'''    
def stdout_file(filename,command):
    __console__=sys.stdout   # backup original stdout 
    file=open(filename,'w')    
    sys.stdout=file  
    for command_line in command:
        exec(command_line)
        
    file.close()    
    sys.stdoud=__console__
    
    return None
    