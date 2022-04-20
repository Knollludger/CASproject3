from copy import copy, deepcopy
from msilib.schema import Binary
import random
from scipy import spatial
from deap import base
from deap import creator
from deap import tools
from sympy import false, true
import numpy as np
import sys
#1100000000011
#-1 is padding
#Here is where we'll put test cases
#Tests are of the form, init, desired, time
#individualSize =  832 #2-d Case
#individualSize = 99
#individualSize = 56 
#individualSize = 248
individualSize = 128
def GenerateMatrix(dim1,dim2):
    gen = np.zeros((dim1+2,dim2+2),np.int8)
    for i in range(0,dim1+2):
        for j in range(0,dim2+2):
            if i == 0 or j == 0 or i == dim1 + 1 or j == dim2 + 1:
                gen[i][j] = -1
            else:
                 gen[i][j] = random.randint(0,1)
    return gen

Tests=[]
#Tests.append((np.array([[-1,-1,-1,-1,-1],[-1,1,1,1,-1],[-1,1,1,1,-1],[-1,1,1,1,-1],[-1,-1,-1,-1,-1]]),3,3,3))
#Tests.append((np.array([[-1,-1,-1,-1,-1],[-1,0,0,0,-1],[-1,0,0,0,-1],[-1,0,0,0,-1],[-1,-1,-1,-1,-1]]),3,3,3))
#Tests.append((np.array([[-1,-1,-1,-1,-1],[-1,1,0,1,-1],[-1,0,0,0,-1],[-1,1,0,1,-1],[-1,-1,-1,-1,-1]]),50,3,3))
#Tests.append((np.array([[-1,-1,-1,-1,-1],[-1,0,1,0,-1],[-1,0,1,0,-1],[-1,0,1,0,-1],[-1,-1,-1,-1,-1]]),50,3,3))
#Tests.append((np.array([[-1,-1,-1,-1,-1],[-1,0,0,0,-1],[-1,0,0,0,-1],[-1,1,1,1,-1],[-1,-1,-1,-1,-1]]),50,3,3))
#Tests.append((np.array([[-1,-1,-1,-1,-1],[-1,0,0,1,-1],[-1,0,0,1,-1],[-1,0,0,1,-1],[-1,-1,-1,-1,-1]]),50,3,3))
#Tests.append((np.array([[-1,-1,-1,-1,-1],[-1,1,1,1,-1],[-1,0,0,0,-1],[-1,0,0,0,-1],[-1,-1,-1,-1,-1]]),50,3,3))
#Tests.append((np.array([[-1,-1,-1,-1,-1],[-1,1,0,0,-1],[-1,0,0,0,-1],[-1,0,0,0,-1],[-1,-1,-1,-1,-1]]),50,3,3))
Tests.append((np.array([[-1,-1,-1,-1,-1,-1,-1],[-1,1,1,0,1,1,-1],[-1,1,1,0,1,1,-1],[-1,0,0,0,0,0,-1],[-1,1,1,0,1,1,-1],[-1,1,1,0,1,1,-1],[-1,-1,-1,-1,-1,-1,-1]]),300,5,5))
Tests.append((np.array([[-1,-1,-1,-1,-1,-1,-1],[-1,0,0,1,0,0,-1],[-1,0,0,1,0,0,-1],[-1,1,1,1,1,1,-1],[-1,0,0,1,0,0,-1],[-1,0,0,1,0,0,-1],[-1,-1,-1,-1,-1,-1,-1]]),300,5,5))
#end of basic tests
#Tests.append((GenerateMatrix(5,5),300,5,5))
#Tests.append((GenerateMatrix(5,5),300,5,5))
#Tests.append((GenerateMatrix(5,5),300,5,5))
Tests.append((GenerateMatrix(10,10),500,10,10))
Tests.append((GenerateMatrix(20,20),1000,20,20))
Tests.append((GenerateMatrix(100,100),5000,100,100))

#Tests.append((GenerateMatrix(50,50),100000,50,50))
#I should try reducing the bits, maybe 7 bits for the rules +  predefining the edges to allow it to focus.
#BestCurrent6 = [0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1]
#BestCurrent = [1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0]
BestCurrent2 = [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1]

#best three works
#BestCut = [0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0]
BestCurrent5 = [0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1]
#Apparently works (doesn't)
BestCurrent6 = [0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1]
#######

def writestepToFile(Next,dim1,dim2):
    f = open("runMatrix" + str(dim1) + "x" + str(dim2) + ".txt",'a')
    for k in range(1,dim1+1):
        for j in range(1,dim2+1):
            if Next[k,j]:
                f.write("B")
            else: f.write("W")
            if not j == dim2:
                f.write(",")
        if  not k == dim1: f.write("\n")
    f.write(":\n")
    f.close()



def RunTwoDCA(Init,Rule,time, shouldPrint,printEnd, dim1, dim2,write2File):
    Current = Init
    if printEnd:
        print(Init)
    Next = deepcopy(Current)
    for i in range(0,time):
        for k in range(1,dim1+1):
            for j in range(1,dim2+1): #We'll need some gap to make it easier
                Next[k][j] = RestrictedRunRule2D2(createlistfrommatrix(k,j,Current),Rule)
        if shouldPrint:
            print(Next)
            print(i)
            #checker(deepcopy(Init),deepcopy(Next),dim1,dim2)
        if write2File:
            writestepToFile(Current,dim1,dim2)
        if np.array_equal(Next,Current):
            break
        else:
            Current = deepcopy(Next)
    
    if printEnd:
        print(Next)
    return -(not checker(Init,Next,dim1,dim2))

def createlistfrommatrix(i,j,Current):
    returner = []
    #print((i,j))
    for m in range(-1,2):
        for k in range(-1,2):
            returner.append(Current[i+m][j+k])
    #print(returner)
    return returner

BestGuess = [0   ,   1,   1,    1,   0,   1,     0,    0,    0,    1,   1,    1,    0,    0,    0  ,  1] #Timms Rule
#           00       01    10   11   000  001    010   011   100  101  110    111   00    01    10    11
def RunRule(c1,c2,c3,Rule):
    #print(c1,c2,c3)
    if c1 == -1:
        return Rule[(2*c2 + c3)]
    elif c3 == -1:
        return Rule[(len(Rule) - 4 + 2*c1 + c2)]
    else:
        return Rule[(4 + c1*4 + c2*2 + c3)]

def RunRule2d(c,Rule):
    if c[1] == -1:
        if c[3] == -1:
            return Rule[(2**9 + convertcelltodecimal(c))]
        elif c[5] == -1:
            return Rule[(2**9 +2**4 + convertcelltodecimal(c))]
        else: 
            return Rule[(2**9 +2**4 + 2**4 +convertcelltodecimal(c))]
    elif c[7] == -1:
            if c[5] == -1:
                return Rule[(2**9 +2**4 + 2**4 + 2**6 +convertcelltodecimal(c))]
            elif c[3] == -1:
                return Rule[(2**9 +2**4 + 2**4 + 2**6 + 2**4 +convertcelltodecimal(c))]
            else:
                return Rule[(2**9 +2**4 + 2**4 + 2**6 + 2**4 + 2**4 + convertcelltodecimal(c))]
    elif c[5] == -1:
        return Rule[(2**9 +2**4 + 2**4 + 2**6 + 2**4 + 2**4 + 2**6 + convertcelltodecimal(c))]
    elif c[3] == -1:
        return Rule[(2**9 +2**4 + 2**4 + 2**6 + 2**4 + 2**4 + 2**6 + 2**6 +convertcelltodecimal(c))]
    else:
        return Rule[convertcelltodecimal(c)]

def RestrictedRunRule2D(c,Rule):
    #print(c)
    if c[3] == -1:
        if c[1] == -1:
            return Rule[(48 + convert32ToRule(c))]
        elif c[7] == -1:
            return Rule[(32 +convert4ToRule(c))]
        else:
            return Rule[(convert5ToRule(c))]
    elif c[5] == -1: 
        return BestGuess[12 + convert2ToRule(c[3],c[4])]
    else:
        return BestGuess[4+convert3ToRule(c)]

def RestrictedRunRule2D2(c,Rule):
    #print(len(Rule))
    #print(c)
    if c[3] == -1:
        if c[1] == -1:
            return BestCurrent3[(48 + convert32ToRule(c))]
        elif c[7] == -1:
            return BestCurrent3[(32 +convert4ToRule(c))]
        else:
            return BestCurrent3[(convert5ToRule(c))]
    elif c[5] == -1: 
        if c[7] == -1:
            return BottomRightRule[convert33ToRule(c)]
        elif c[1] == -1:
            return TopRightRule[convert44ToRule(c)]
        else:
            return RightEdgeRule[convert55ToRule(c)]
    elif c[7] == -1:
        return BottomEdgeRule[convert52ToRule(c)]
    elif c[1] == -1:
        return TopEdgeRule[convert54ToRule(c)]
    else:
        #print(str(c[1]) +"" + str(c[2]) + "" + str(c[3]) + "" + str(c[4]) + "" + str(c[5]) +""+  str(c[6]) + ""+ str(c[7]))
        #print(Rule[convert7ToRule(c)])
        return Rule[convert7ToRule(c)]

BestCurrent3 = [ 0  ,    1,     1,     1,      0,      0,      0,      0,       0,         1,     1,     1,      1,     1,       1 ,   1,      0,     1,      1,      1,     1,       1,      1    ,   1,     0,        1,      1      , 1,      1,      1,     1,      1,                0,    1,       0,    0,   0,    1,    1,     1,   0,    1,     1,    1,   0,    1,   1,   1,              0,     1,   1,   1,  1,   1,   1,   1]
#               00000   00001  00010  00011   00100   00101   00110   00111   01000     01001    01010  01011   01100  01101  01110  01111    10000  10001   10010   10011  10100    10101    10110   10111   11000  11001    11010     11011   11100   11101  11110   11111 (end of 5) 0000    0001    0010  0011 0100  0101  0110  0111  1000 1001   1010  1011 1100 1101 1110 1111 (end of 4)  000   001   010  011  100  101  110  111

def convert3ToRule(c):
    return c[3] * 4 + c[4] * 2 + c[5] * 1

def convert2ToRule(c1,c2):
    return c1*2 + c2
def convert4ToRule(c):
    return c[1]*8 + c[2] * 4 + c[4] * 2 + c[5] * 1

def convert32ToRule(c):
    return c[4]*4 + c[5] * 2 + c[7]

def convert5ToRule(c):
    return c[1]*16 + c[2] * 8 + c[4] * 4 + c[5] * 2 + c[7]

#restriced 2 rules

def convert33ToRule(c):
    return c[1] * 4 + c[3]*2 + c[4]
BottomRightRule = [0,  0,  0   ,  0 ,  0  , 0   ,0 ,1]
###               000 001  010   011 100  101   110 111


def convert52ToRule(c):
    return c[1]*16 + c[2] * 8 + c[3]* 4 + c[4]*2 + c[5]
BottomEdgeRule = [0  ,    1   ,  0,      0   , 0,     1  ,    0        ,0,       0,    1,     0,      0   ,  0   ,  1,     1,   1,     0,    1     , 0,     0     ,  0,    1,     1,      1,     0,     1,   0,       0  ,   0,    1,    1,    1]
#####          00000  00001   00010   00011 00100  00101     00110    00111  01000   01001  01010  01011   01100  01101 01110  01111 10000  10001   10010  10011   10100  10101  10110   10111  11000 11001 11010   11011   11100 11101 11110  11111                                       
def convert54ToRule(c):
    return c[3]*16 + c[4] * 8 + c[5]* 4 + c[6]*2 + c[7]
TopEdgeRule = [0  ,    0   ,  0,        1   , 1,     1  ,      1        ,1,       0,    0,     0,      0   ,  0   ,  0,     0,     0,     0,      0     , 0,     1     ,  1,    1,     1,      1,     1,     1,   1,       1  ,    1,    1,    1,    1]
#####          00000  00001   00010   00011 00100  00101     00110    00111    01000   01001  01010  01011   01100  01101 01110  01111   10000  10001   10010  10011   10100  10101  10110   10111  11000 11001 11010   11011   11100 11101 11110  11111                                       
def convert55ToRule(c):
    return c[1]*16 + c[3] * 8 + c[4]* 4 + c[6]*2 + c[7]
RightEdgeRule = [0  ,    0   ,  0,      1   , 0,     0  ,    0        ,0,       0,    0,     0,      1   ,  0   ,  0,      0,   0,     0,    0     , 0,     1     ,  0,    0,     0,      0,     0,     0,   0,       1  ,   1,    1,    1,    1]
#####          00000  00001   00010   00011 00100  00101     00110    00111  01000   01001  01010  01011   01100  01101 01110  01111 10000  10001   10010  10011   10100  10101  10110   10111  11000 11001 11010   11011   11100 11101 11110  11111                                       
def convert42ToRule(c):
    return c[1]*8  + c[2]*4 + c[4] * 2 + c[7]



def convert7ToRule(c):
   
    return c[1]*64 + c[2]*32 + c[3] * 16 + c[4] * 8 + c[5] * 4 + c[6] *2 + c[7] 
BestCurrent6 = [0,          0,     0  ,         1,        1,          1,          1,        1,               0,             0,       0,         0,          0,     0,           0,        0,      0,      0,       0,           1,        1,      1,        1,      1,       0,       0 ,       0       , 0    ,    0,        0,        0,        0,         0 ,      0,        0,       1,           1,      1,         1,        1,      0,        0,          0,       0,        0,       0,       0,        0,         0 ,        0,      0,        1,       1,       1,       1,          1,         1,        1,     1,        1,          1,         1,        1 ,        1,        0,         0,            0,            1,         1,          1,         1,           1 ,         0,         0,        0,        0,          0,          0,          0,            0,       0,        0,       0,            1,       1,       1,      1 ,        1,          1,       1,       1,          1,       1,         1,         1,        1,          0,       0,             0,          1,           1,          1,         1,           1 ,      0,       0,         0,            0,        0,         0,            0,           0,        0,        0,           0,            1,      1,       1,          1 ,        1,          1,          1,            1,          1,       1,            1,          1,         1]
#######       0000000   0000001  0000010     0000011    0000100     0000101  0000110       0000111       0001000         0001001  0001010    0001011     0001100  0001101    0001110  0001111  0010000  0010001   0010010    0010011  0010100  0010101   0010110  0010111  0011000 0011001  0011010    0011011   0011100   0011101   0011110   0011111   0100000  0100001    0100010   0100011     0100100  0100101  0100110    0100111 0101000   0101001     0101010 0101011   0101100  0101101    0101110  0101111    0110000   0110001  0110010   0110011  0110100   0110101   0110110     0110111  0111000 0111001    0111010   0111011    0111100   0111101   0111110    0111111     1000000    1000001       1000010    1000011      1000100   1000101    1000110      1000111    1001000    1001001    1001010    1001011   1001100      1001101       1001110     1001111   1010000   1010001    1010010      1010011 1010100  1010101   1010110    1010111    1011000   1011001   1011010    1011011   1011100   1011101   1011110   1011111    1100000    1100001       1100010    1100011      1100100   1100101    1100110      1100111    1101000    1101001    1101010    1101011   1101100      1101101       1101110     1101111   1110000   1110001       1110010      1110011 1110100  1110101      1110110    1110111    1111000      1111001     1111010    1111011     1111100     1111101      1111110   1111111
def convert44ToRule(c):
    return c[3] * 8 + c[4]*4 +c[6]*2 + c[7]

TopRightRule = [0 ,   0,       0 ,   1    , 0   ,   0,     0,    0,       0   ,  0    ,0  , 1  ,  1,      1   ,     1 ,   1 ]
####           0000  0001   0010   0011    0100    0101   0110  0111    1000   1001  1010   1011   1100  1101    1110   1111

#end
def mazeSearch(matrix,x,y,value,newvalue):
    #print(matrix)
    #print(x,y)
    #print(value)
    total = 0
    if matrix[x-1,y] == value:
        matrix[x-1,y] = newvalue
        total += 1
        total += mazeSearch(matrix,x-1,y,value,newvalue)
    if matrix[x,y+1] == value:
        matrix[x,y+1] = newvalue
        total += 1
        total += mazeSearch(matrix,x,y+1,value,newvalue)
    if matrix[x,y-1] == value:
        matrix[x,y-1] = newvalue
        total += 1
        total += mazeSearch(matrix,x,y-1,value,newvalue)
    if matrix[x+1,y] == value:
        matrix[x+1,y] = newvalue
        total += 1
        total += mazeSearch(matrix,x+1,y,value,newvalue)
    return total


def checker(Init,output,dim1,dim2):
    aliveX = 0
    alivey = 0
    deadx =0
    deady = 0
    firstalive = False
    firstDead = False
    totalinit = 0
    totaloutput = 0
    for i in range(1,dim1+1):
        noZeros = True
        for j in range(1,dim2+1):
            totalinit += Init[i][j]
            totaloutput += output[i][j]
            if output[i][j] == 1 and firstalive == False:
                firstalive = True
                aliveX = i
                alivey = j
            if output[i][j] == 0 and firstDead == False:
                firstDead = True
                deadx = i
                deady = j
    if totalinit != totaloutput:
        #print("here")
        #print((totalinit,totaloutput))
        #sys.exit(0)
        return False
    else:
        #print("here2")
        mz1 = 0
        if firstalive:
            output[aliveX,alivey] = 3
            mz1 = mazeSearch(output,aliveX,alivey,1,3) + 1
        #print(mz1,totalinit)
        mz2 = 0
        if firstDead:
            output[deadx,deady] = 2
            mz2 = mazeSearch(output,deadx,deady,0,2) + 1
        #print(mz2,dim1*dim2-totalinit)
        return mz1==totalinit and mz2 ==dim1*dim2-totalinit




def convertcelltodecimal(c):
    multiplier = 1
    total = 0
    for i in c:
        if i == -1:
            continue
        else: 
            total += multiplier*i
            multiplier *= 2
    return total

def mut3(ca,indp):
    if random.random() < indp:
        ca = random.randint(0,2)


creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# Attribute generator 
#                      define 'attr_bool' to be an attribute ('gene')
#                      which corresponds to integers sampled uniformly
#                      from the range [0,1] (i.e. 0 or 1 with equal
#                      probability)
toolbox.register("attr_bool", random.randint, 0, 1)

toolbox.register("individual", tools.initRepeat, creator.Individual, 
    toolbox.attr_bool, individualSize) #264 is our rule size, 256 for 3, 8 for the edges.

# define the population to be a list of individuals
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# the goal ('fitness') function to be maximized
def evalOneMax(individual):
    testTotal = 0
    for i in Tests:
        testTotal += RunTwoDCA(i[0],individual,i[1],False,False,i[2],i[3],False)
    
    return testTotal,

def endingProof(individual):
    testTotal = 0
    for i in Tests:
        testTotal += RunTwoDCA(i[0],individual,i[1],True,True,i[2],i[3],True)
        if not testTotal == 0:
            break
        
    print(testTotal)
    return testTotal,


#----------
# Operator registration
#----------
# register the goal / fitness function
toolbox.register("evaluate", evalOneMax)

# register the crossover operator
toolbox.register("mate", tools.cxTwoPoint)

# register a mutation operator with a probability to
# flip each attribute/gene of 0.05
toolbox.register("mutate", tools.mutUniformInt,low=0,up=1, indpb=0.05)

# operator for selecting individuals for breeding the next
# generation: each individual of the current generation
# is replaced by the 'fittest' (best) of three individuals
# drawn randomly from the current generation.
toolbox.register("select", tools.selTournament, tournsize=3)

#----------

def main():
    random.seed(64)

    # create an initial population of 300 individuals (where
    # each individual is a list of integers)
    pop = toolbox.population(n=300)
    # CXPB  is the probability with which two individuals
    #       are crossed
    #
    # MUTPB is the probability for mutating an individual
    CXPB, MUTPB = 0.5, 0.2

    print("Start of evolution")

    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    print("  Evaluated %i individuals" % len(pop))

    # Extracting all the fitnesses of 
    fits = [ind.fitness.values[0] for ind in pop]

    # Variable keeping track of the number of generations
    g = 0

    # Begin the evolution
    while max(fits) < 0 and g < 1000:
        # A new generation
        g = g + 1
        print("-- Generation %i --" % g)

        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):

            # cross two individuals with probability CXPB
            if random.random() < CXPB:
                toolbox.mate(child1, child2)

                # fitness values of the children
                # must be recalculated later
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:

            # mutate an individual with probability MUTPB
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        print("  Evaluated %i individuals" % len(invalid_ind))

        # The population is entirely replaced by the offspring
        pop[:] = offspring

        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]

        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5

        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))
        print("  Avg %s" % mean)
        print("  Std %s" % std)
        best_ind = tools.selBest(pop, 1)[0]
        print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))
    print("-- End of (successful) evolution --")

    best_ind = tools.selBest(pop, 1)[0]
    print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))
    evalOneMax(best_ind)
    endingProof(best_ind)
if __name__ == "__main__":
    np.set_printoptions(threshold=sys.maxsize,linewidth=100*100)
    sys.setrecursionlimit(101*101)
    endingProof(BestCurrent6)
    
    #main()
    