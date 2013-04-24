import random
from time import *
import cProfile
 
def zero(m,n):
    # Create zero matrix
    new_matrix = [[0 for row in range(n)] for col in range(m)]
    return new_matrix
 
def rand(m,n):
    # Create random matrix
    new_matrix = [[random.randint(-1,3) for row in range(n)] for col in range(m)]
    return new_matrix
 
def show(matrix):
    # Print out matrix
    for col in matrix:
        print col 

'''
    convert string to number matrix
'''
def str_to_matrix(str_matrix):
     
    lines = str_matrix.split('\n')
    matrix = []
    i = 0
    for line in lines:
        matrix.append([])
        str_nums = line.split()
        for str_num in str_nums:
            matrix[i].append(float(str_num))
        i += 1
    return matrix
        
'''
    Convert number matrix to a string
'''
def matrix_to_str(matrix):   
    
    str_ret = ""
    for row in matrix:
        for elem in row:
            str_ret = str_ret + "" + str(elem) + " "
        str_ret = str_ret + "\n" 
    return str_ret


    
def mult(matrix1,matrix2):
    '''
    # Matrix multiplication
    if len(matrix1[0]) != len(matrix2):
        # Check matrix dimensions
        print 'Matrices must be m*n and n*p to multiply!'
        print len(matrix1[0])
        print len(matrix2)
    else:
        # Multiply if correct dimensions
    '''
    new_matrix = zero(len(matrix1)-1,len(matrix2[0]))
    for i in range(len(matrix1)-1):
        for j in range(len(matrix2[0])):
            for k in range(len(matrix2)-1):
                new_matrix[i][j] += matrix1[i][k]*matrix2[k][j]
    return new_matrix

def mult2(matrix1,matrix2):
    '''
    # Matrix multiplication
    if len(matrix1[0]) != len(matrix2):
        # Check matrix dimensions
        print 'Matrices must be m*n and n*p to multiply!'
        print len(matrix1[0])
        print len(matrix2)
    else:
        # Multiply if correct dimensions
    '''
    new_matrix = zero(len(matrix1),len(matrix2[0]))
    for i in range(len(matrix1)):
        for j in range(len(matrix2[0])):
            for k in range(len(matrix2)):
                new_matrix[i][j] += matrix1[i][k]*matrix2[k][j]
    return new_matrix

def matrix_mult(matrix1,matrix2):
    '''
    # Matrix multiplication
    if len(matrix1[0]) != len(matrix2):
        # Check matrix dimensions
        print 'Matrices must be m*n and n*p to multiply!'
        print len(matrix1[0])
        print len(matrix2)
    else:
        # Multiply if correct dimensions
    '''
    new_matrix = zero(len(matrix2[0]),len(matrix2[0]))
    for i in range(len(matrix2[0])):
        for j in range(len(matrix2[0])):
            for k in range(len(matrix2[0])):
                new_matrix[i][j] += matrix1[i][k]*matrix2[k][j]
    return new_matrix
 
def main():
    
    f = open('test.txt','w')
    f.write(matrix_to_str(rand(3,3)))
    f.close()
    '''
    print str_mat
    mat = str_to_matrix(str_mat)
    mat = mult(mat,mat)
    print mat
    #f.write(matrix_to_str(mat))
    #f.close()
    '''

if __name__ == "__main__":
    main()
    
def time_mult(matrix1,matrix2):
    # Clock the time matrix multiplication takes
    start = clock()
    new_matrix = mult(matrix1,matrix2)
    end = clock()
    print 'Multiplication took ',end-start,' seconds'
 
def profile_mult(matrix1,matrix2):
    # A more detailed timing with process information
    # Arguments must be strings for this function
    # eg. profile_mult('a','b')
    cProfile.run('matrix.mult(' + matrix1 + ',' + matrix2 + ')')