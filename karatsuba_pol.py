import math
DEBUG = 0
class Karatsuba():
    #DEBUG = 0

    def __init__(self):
        self.count_xor = 0
        self.count_and = 0

    def print_pol(self,p1):
        st = ""
        for i in xrange(0,len(p1)):
            if p1[i]:
                st = st + "x^"+str(i) + "+"
        if st.strip():
            st = st[:-1]
            print st
        else:
            print "0"


    def max_degree(self,pol_1,pol_2):
        return max(len(pol_1), len(pol_2))

    def mult(self, a, b):
        d = [0]*(max(len(a),len(b)))
        d[0] = a[0] & b[0]
        return d


    def sum_pol(self,p1, p2):
        if len(p1) == max(p1,p2):
            temp = [0]*(len(p2))
            for i in xrange(0,len(p2)):
                temp[i] = ((p1[i] + p2[i]) %2)

            temp = temp + p1[len(p2):]
            return temp
        else:
            temp = [0]*(len(p1))
            for i in xrange(0,len(p1)):
                temp[i] = ((p1[i] + p2[i]) %2)
            temp = temp + p2[len(p1):]
            return temp

    def concat_pol(self,pol, m):
        #print m
        to_append = [0]*m
        return (to_append + pol)

    def split_at(self,pol, m):
        #print pol
        return pol[m:], pol[:m]

    def karatsuba(self,pol_1, pol_2):
        max_deg_p1_p2 = self.max_degree(pol_1,pol_2)
        if DEBUG:
            print "karatsuba: p1:{0}, p2:{1}".format(pol_1,pol_2)
        if (max_deg_p1_p2 < 2):
            return self.mult(pol_1, pol_2)

        m = int(math.floor(float(max_deg_p1_p2)/float(2)))
        #print "m = ", m
        pol_1_high, pol_1_low = self.split_at(pol_1, m)
        if DEBUG:
            print "karatsuba::pol_1_high:{0}, pol_1_low:{1}".format(pol_1_high,pol_1_low)
        pol_2_high, pol_2_low = self.split_at(pol_2, m)
        if DEBUG:
            print "karatsuba::pol_2_high:{0}, pol_2_low:{1}".format(pol_2_high,pol_2_low)

        z0 = self.karatsuba(pol_1_low, pol_2_low)
        if DEBUG:
            print "karatsuba::z0:{0}, pol_1_low:{1},pol_2_low:{2}".format(z0,pol_1_low,pol_2_low)
        temp_1 = self.sum_pol(pol_1_low, pol_1_high)
        temp_2 = self.sum_pol(pol_2_low, pol_2_high)
        z1 = self.karatsuba(temp_1, temp_2)
        if DEBUG:
            print "karatsuba::z1:{0}, temp_1:{1},temp_2:{2}".format(z1,temp_1,temp_2)
        z2 = self.karatsuba(pol_1_high, pol_2_high)
        if DEBUG:
            print "karatsuba::z2:{0}, pol_1_high:{1},pol_2_high:{2}".format(z2,pol_1_high,pol_2_high)
        #return (z2*10^(2*m2))+((z1-z2-z0)*10^(m2))+(z0)
        if DEBUG:
            print "karatsuba::z0:{0}".format(z0)
        temp_3 = self.sum_pol(z1,z2)
        if DEBUG:
            print "karatsuba::sum_pol(z1,z2):{0}, z1:{1}, z2:{2}".format(temp_3, z1,z2)
        temp_4 = self.sum_pol(temp_3, z0)
        if DEBUG:
            print "karatsuba::sum_pol(temp_3,z0):{0}, temp_3:{1}, z0:{2}".format(temp_4, temp_3,z0)
        if DEBUG:
            print "karatsuba::z0:{0}, temp_4:{1}, z2:{2}".format(z0, temp_4,z2)

        concat_1 = (self.concat_pol(temp_4, m))
    #    print "concat_1:{0}".format(concat_1)
    #    print_pol(concat_1)
        concat_2 = self.concat_pol(z2,(2*m))
    #    print "concat_2:{0}".format(concat_2)
    #    print_pol(concat_2)
        sum_1 = self.sum_pol(z0, concat_1)
        sum_2 = self.sum_pol(sum_1, concat_2)

        return sum_2

        #return (z0 +  (concat_pol(temp_4, m)) + concat_pol(z2,(2*m)))
