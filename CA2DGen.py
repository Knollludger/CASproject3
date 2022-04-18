from copy import copy, deepcopy
from msilib.schema import Binary
import random
from scipy import spatial
from deap import base
from deap import creator
from deap import tools
from sympy import false, true
import numpy as np
#1100000000011
#-1 is padding
#Here is where we'll put test cases
#Tests are of the form, init, desired, time
individualSize =  832 #2-d Case
#individualSize = 99
#individualSize = 56 
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
Tests.append((np.array([[-1,-1,-1,-1,-1],[-1,1,1,1,-1],[-1,1,1,1,-1],[-1,1,1,1,-1],[-1,-1,-1,-1,-1]]),3,3,3))
Tests.append((np.array([[-1,-1,-1,-1,-1],[-1,0,0,0,-1],[-1,0,0,0,-1],[-1,0,0,0,-1],[-1,-1,-1,-1,-1]]),3,3,3))
Tests.append((np.array([[-1,-1,-1,-1,-1],[-1,1,0,1,-1],[-1,0,0,0,-1],[-1,1,0,1,-1],[-1,-1,-1,-1,-1]]),50,3,3))
Tests.append((np.array([[-1,-1,-1,-1,-1],[-1,0,1,0,-1],[-1,0,1,0,-1],[-1,0,1,0,-1],[-1,-1,-1,-1,-1]]),50,3,3))
Tests.append((np.array([[-1,-1,-1,-1,-1],[-1,0,0,0,-1],[-1,0,0,0,-1],[-1,1,1,1,-1],[-1,-1,-1,-1,-1]]),50,3,3))
Tests.append((np.array([[-1,-1,-1,-1,-1],[-1,0,0,1,-1],[-1,0,0,1,-1],[-1,0,0,1,-1],[-1,-1,-1,-1,-1]]),50,3,3))
Tests.append((np.array([[-1,-1,-1,-1,-1],[-1,1,1,1,-1],[-1,0,0,0,-1],[-1,0,0,0,-1],[-1,-1,-1,-1,-1]]),50,3,3))
Tests.append((np.array([[-1,-1,-1,-1,-1],[-1,1,0,0,-1],[-1,0,0,0,-1],[-1,0,0,0,-1],[-1,-1,-1,-1,-1]]),50,3,3))
Tests.append((np.array([[-1,-1,-1,-1,-1,-1,-1],[-1,1,1,0,1,1,-1],[-1,1,1,0,1,1,-1],[-1,0,0,0,0,0,-1],[-1,1,1,0,1,1,-1],[-1,1,1,0,1,1,-1],[-1,-1,-1,-1,-1,-1,-1]]),300,5,5))
Tests.append((np.array([[-1,-1,-1,-1,-1,-1,-1],[-1,0,0,1,0,0,-1],[-1,0,0,1,0,0,-1],[-1,1,1,1,1,1,-1],[-1,0,0,1,0,0,-1],[-1,0,0,1,0,0,-1],[-1,-1,-1,-1,-1,-1,-1]]),300,5,5))
#end of basic tests
Tests.append((GenerateMatrix(5,5),300,5,5))
Tests.append((GenerateMatrix(5,5),300,5,5))
Tests.append((GenerateMatrix(5,5),300,5,5))
#Tests.append((GenerateMatrix(10,10),500,10,10))
#Tests.append((GenerateMatrix(20,20),1000,20,20))
#Tests.append((GenerateMatrix(30,30),5000,30,30))
#Tests.append((GenerateMatrix(100,100),100000,5,5))
#I should try reducing the bits, maybe 7 bits for the rules +  predefining the edges to allow it to focus.
#BestCurrent6 = [0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1]
#BestCurrent = [1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0]
BestCurrent2 = [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1]
BestCurrent3 = [ 0  ,    1,     1,     1,      0,      0,      0,      0,       0,         1,     1,     1,      1,     1,       1 ,   1,      0,     1,      1,      1,     1,       1,      1    ,   1,     0,        1,      1      , 1,      1,      1,     1,      1,                0,    1,       0,    0,   0,    1,    1,     1,   0,    1,     1,    1,   0,    1,   1,   1,              0,     1,   1,   1,  1,   1,   1,   1]
#               00000   00001  00010  00011   00100   00101   00110   00111   01000     01001    01010  01011   01100  01101  01110  01111    10000  10001   10010   10011  10100    10101    10110   10111   11000  11001    11010     11011   11100   11101  11110   11111 (end of 5) 0000    0001    0010  0011 0100  0101  0110  0111  1000 1001   1010  1011 1100 1101 1110 1111 (end of 4)  000   001   010  011  100  101  110  111
#best three works
def RunTwoDCA(Init,Rule,time, shouldPrint,printEnd, dim1, dim2):
    Current = Init
    if printEnd:
        print(Init)
    Next = deepcopy(Current)
    for i in range(0,time):
        for k in range(1,dim1+1):
            for j in range(1,dim2+1): #We'll need some gap to make it easier
                Next[k][j] = RunRule2d(createlistfrommatrix(k,j,Current),Rule)
        if shouldPrint:
            print(Next)
            print(i)
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
            return Rule[(2**4 + +2**5 + convert32ToRule(c))]
        elif c[7] == -1:
            return Rule[(2**5 +convert4ToRule(c))]
        else:
            return Rule[(convert5ToRule(c))]
    elif c[5] == -1: 
        return BestGuess[12 + convert2ToRule(c[3],c[4])]
    else:
        return BestGuess[4+convert3ToRule(c)]
            
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
        testTotal += RunTwoDCA(i[0],individual,i[1],False,False,i[2],i[3])
    
    return testTotal,

def endingProof(individual):
    testTotal = 0
    for i in Tests:
        testTotal += RunTwoDCA(i[0],individual,i[1],True,True,i[2],i[3])
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
    #endingProof(BestCurrent3)
    main()
    