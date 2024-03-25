import numpy as np


def vector_distance(w1,w2):     # finding distance between two word vectors
    q=(w1-w2)**2
    w=np.sum(q)
    return(np.squeeze(w))       # returns a float value from 0 to infinity


def sigmoid(v) :
    A1=1/(1+np.exp(-1*v))
    return(A1)


def load_parameters() :
    f1=open("W1.txt")
    W1=np.zeros((2,3))
    f2=open("B1.txt")
    B1=np.zeros((1,2))
    f3=open("W2.txt")
    W2=np.zeros((1,2))
    f4=open("B2.txt")
    B2=0

    r,c=(0,0)
    for line in f1 :
        s=line.strip().split(",")
        c=0
        for val in s :
            W1[r][c]=float(val)
            c=c+1
        r=r+1

    r,c=(0,0)
    s=f2.read().strip().split(",")
    for val in s :
        B1[0][r]=float(val)
        r=r+1

    r=0
    s=f3.read().strip().split(",")
    for val in s :
        W2[0][c]=float(val)
        c=c+1

    c=0

    B2=float(f4.read().strip())
    return (W1,B1.T,W2,B2)


def predict_matching(vector) :
    W1,B1,W2,B2=load_parameters()
    A1=np.tanh(np.dot(W1,vector)+B1)
    A2=sigmoid(np.dot(W2,A1)+B2)
    return (np.squeeze(A2))
