
class Reduction():

    def __init__(self, m, b,c):
        self.m = m
        self.b = b
        self.c = c


    def reduction(self, d):
        T1 = [0]*(self.b-2)
        D_red = [0]*self.m

        for i in xrange(0,self.b-1):
            T1[i] = (d[i + 2*self.b + 1] + d[i + 3*self.b + (2*self.c)])%2;

        for i in xrange(0,c):
            D_red[i] = (d[i] + T1[i]) %2

        
