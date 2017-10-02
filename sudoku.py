import time
import pycosat
import numpy as np
import pandas as pd
import csv
import sys
import pycosat

posible_numbers=[0,1,2,3,4,5,6,7,8]

def  create_array_names():
    puzzle=np.zeros((9,9,9))
    for i in range(9):
        for j in range(9):
            for k in range(9):
                puzzle[i][j][k] = i * 81 + j * 9 + k +1
    return puzzle

def encode_at_least_one(puzzle):
    clauses_box=[]
    clauses_columns=[]
    clauses_rows=[]
    clauses_block=[]
    for i in range(len(puzzle[:])):
        for j in range(len(puzzle[0,:])):
            clauses_box.append([int(puzzle[i,j,x]) for x in posible_numbers]) #at least a number in a box
            clauses_columns.append([int(puzzle[i,x,j]) for x in posible_numbers]) #at least
            clauses_rows.append([int(puzzle[x,i,j]) for x in posible_numbers])
            if(i%3==0 and j%3==0):
                for x in posible_numbers:
                    block=[]
                    for block_i in range(i,i+3):
                        for block_j in range(j,j+3):
                            block+=[int(puzzle[block_i,block_j,x])]
                    clauses_block.append(block)

    return clauses_box+clauses_columns+clauses_rows+clauses_block

def encode_at_most_one(puzzle):
    clauses_box=[]
    clauses_columns=[]
    clauses_rows=[]
    clauses_block=[]
    for i in range(len(puzzle[:])):
        for j in range(len(puzzle[0,:])):
            for x in posible_numbers:
                clauses_box += [[-1*int(puzzle[i,j,x]), -1*int(puzzle[i,j,k])] for k in range(x+1,9)]
                clauses_columns += [[-1*int(puzzle[i,x,j]), -1*int(puzzle[i,k,j])] for k in range(x+1,9)]
                clauses_rows +=[[-1*int(puzzle[x,i,j]), -1*int(puzzle[k,i,j])] for k in range(x+1,9)]
                if(i%3==0 and j%3==0):
                    for block_i in range(i,i+3):
                        for block_j in range(j,j+3):
                            block=[]
                            for x in posible_numbers:
                                for bl_i in range(block_i,i+3):
                                    for bl_j in range(block_j,j+3):
                                        if bl_i!=block_i or bl_j!=block_j:
                                            block=[-1*int(puzzle[block_i,block_j,x]),-1*int(puzzle[bl_i,bl_j,x])]
                                        #print (block)
                                        if len(block)!=0:
                                            clauses_block.append(block)
                                        block=[]

    return clauses_box+clauses_columns+clauses_rows+clauses_block

def encode_X_wing(puzzle):


    clauses_hieuristic=[]
    clauses=[]
    for x in posible_numbers:
        for i in [1,3,5,7]:
            for j in [0,2,4,6,8]:
                for i2 in  range(i,len(puzzle[:]),2):
                    for ji in range(1,len(puzzle[:]),2):
                        clauses=[]
                        for j2 in range(j,len(puzzle[:]),2):
                            for jj in range(0,len(puzzle[:]),2):
                                clauses+=[-1*int(puzzle[i,j,x]),int(puzzle[i2,ji,x]),-1*int(puzzle[jj,j2,x])]
                        clauses_hieuristic.append(clauses)

    #clauses=[]
    #for x in posible_numbers:
    #    for j in [0,2,4,6,8]:
    #        for i in [1,3,5,7]:
    #            for j2 in  range(j,len(puzzle[:]),2):
    #                clauses=[]
    #                for i2 in range(i,len(puzzle[:]),2):
    #                    #print(str(i)+str(j)+" "+str(i)+str(i2)+" "+str(j2)+str(j))
    #                    for i3 in range(i2,len(puzzle[:]),2):
    #                        for ij in range(j2,len(puzzle[0,:]),2):
    #                           clauses+=[-1*int(puzzle[i,j,x]),int(puzzle[j3,j2,x]),-1*int(puzzle[i2,i3,x])]
    #                clauses_hieuristic.append(clauses)

    return clauses_hieuristic



def readSudoku(sud_file):

    puzzle=np.zeros((9,9))
    i=0
    j=0
    for digit in sud_file:
        if digit=='.':
            puzzle[i][j%9]=0
        else :
            puzzle[i][j%9]=digit
        j+=1
        if j%9==0:
            i+=1

    return puzzle

def encode_givens(puzzle,encoding):

    cnf=[]
    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
                if puzzle[i][j]!=0:
                    cnf.append([int(encoding[i,j,int(puzzle[i][j])-1])])

    return cnf

def create_solution(result_list,encoding):
    puzzle=np.zeros((9,9))
    list_r=[]
    for r in result_list:
        if r>0 :
            list_r.append(r)

    counter=0
    i=0
    j=0
    for i in range(9):
        for j in range(9):
            puzzle[i][j]=list_r[counter]-81*i-9*j
            counter+=1
    print(puzzle)

def main():

    encoding=create_array_names()
    #sudokus=readSudoku(sys.argv[1])
    sudokus=pd.read_csv(sys.argv[1])
    #print(sudokus)
    average=0
    average1 = 0

    average=[]
    average1=[]
    for index ,sudoku_info in sudokus.iterrows():
        puzzle=readSudoku(sudoku_info[0])

        cnf1 = encode_at_least_one(encoding)
        cnf2 = encode_at_most_one(encoding)
        cnf3 = encode_X_wing(encoding)
        cnf4 = encode_givens(puzzle ,encoding)
        cnf_hieuristics=cnf1+cnf2+cnf3+cnf4

        start = time.clock()
        result_list = pycosat.solve(cnf_hieuristics)
        end = time.clock()
        average.append(end-start)

        if result_list=='UNSAT':
            print ("error")

        #print (result_list)
        create_solution(result_list,encoding)
        #average1+=end1-start1
    print ('Average time with hieuristics: '+str(sum(average)/len(sudokus)))
    #print ('Average time without hieuristics: '+str(average1/len(sudokus)))

if __name__ == '__main__':
    main()
