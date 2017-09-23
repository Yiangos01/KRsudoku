import time
import pycosat
import numpy as np
import csv
import sys

posible_numbers=[0,1,2,3,4,5,6,7,8]

def  create_array_names():
    puzzle=np.zeros((9,9,9))
    for i in range(9):
        for j in range(9):
            for k in range(9):
                puzzle[i][j][k] = i * 81 + j * 9 + k +1
    return puzzle

def encode_at_least_one(puzzle):

    #for each box contain have a number
    clause_box=[]
    clause_columns=[]
    clause_rows=[]
    for i in range(len(puzzle[:])):
        for j in range(len(puzzle[0,:])):
            clause_box.append([puzzle[i,j,x] for x in posible_numbers])
            clause_columns.append([puzzle[i,x,j] for x in posible_numbers])
            clause_rows.append([puzzle[x,i,j] for x in posible_numbers])

    return clause_box+clause_columns+clause_rows

def encode_at_most_one(puzzle):

    for i in range(9):
        for j in range(9):
            arr = [-1*names[i], -1*names[j]]
            encode.insert(0, arr)
    return encode

def readSudoku(csvfile):
    #print (csvfile)
    csvfile = open(csvfile, "rt")
    reader = csv.reader(csvfile)
    puzzle=np.zeros((9,9))
    for row in reader:
        puzz=row[0]

    i=0
    j=0
    for digit in list(puzz):
        if digit=='.':
            puzzle[i][j%9]=0
        else :
            puzzle[i][j%9]=digit
        j+=1
        if j%9==0:
            i+=1

    return puzzle

def main():

    puzzle=readSudoku(sys.argv[1])
    encoding=create_array_names()
    #print (encoding)

    cnf = encode_at_least_one(encoding)
    print (len(cnf))

if __name__ == '__main__':
    main()
