import math

DEBUG = 0

def print_pol(p1):
    st = ""
    for i in xrange(0,len(p1)):
        if p1[i]:
            st = st + "x^"+str(i) + "+"
    if st.strip():
        st = st[:-1]
        print st
    else:
        print "0"


def max_degree(pol_1,pol_2):
    return max(len(pol_1), len(pol_2))

def mult(a, b):
    m = max(len(b), len(a))
    d = [0]*(2*m-1) #[0...2m-2]
    a_by_b = [[0 for x in range((2*m)-1)] for y in range((2*m)-1)]
    #print "polynom_multiplier: a:{0}, b:{1}, m:{2}".format(a,b,m)
    if DEBUG:
        print "polynom_multiplier: a:{0}, b:{1}, m:{2}".format(a,b,m)

    if(len(a) > 0 and len(b) > 0):
        #gen_ands:
        for k in xrange(0,m): # 0...m-1
            for i in xrange(0,k+1):#0...k
                if DEBUG:
                    print "k:{0}:a[{1}]:{2} b[{3}]:{4} a_by_b[{5}][{6}]:{7}".format(k,i,a[i],(k-i),b[k-i],k, i,(a[i] & b[k-i]))
                a_by_b[k][i] = a[i] & b[k-i]


        #gen_ands2:
        if DEBUG:
            print " "
        for k in xrange(m,(2*m)-1): # m...2*m-2
            for i in xrange(k, (2*m)-1):#k...2*m-2
                if DEBUG:
                    print "k:{0}:a[{1}]:{2} b[{3}]:{4} a_by_b[{5}][{6}]:{7}".format(k,(k-i+(m-1)),a[k-i+(m-1)],(i-(m-1)),b[i-(m-1)],k, i,(a[k-i+(m-1)] & b[i-(m-1)]))
                a_by_b[k][i] = a[k-i+(m-1)] & b[i-(m-1)]

        if DEBUG:
            print " "
        d[0] = a_by_b[0][0]

        for k in xrange(1,(2*m-1)):# 1...2*m-2
            aux = 0
            if(k < m):
                aux = a_by_b[k][0]
                for i in xrange(1,k+1): #1...k
                    if DEBUG:
                        print "aux:{0} ^ a_by_b[{1}][{2}]:{3}".format(aux, k,i,a_by_b[k][i])
                    aux = aux ^ a_by_b[k][i]
                    if DEBUG:
                        print "aux:{0}".format(aux)


            else:
                aux = a_by_b[k][k]
                for i in xrange(k+1,(2*m-1)):#k+1 ... 2m-2
                    if DEBUG:
                        print "aux:{0} ^ a_by_b[{1}][{2}]:{3}".format(aux, k,i,a_by_b[k][i])
                    aux = aux ^ a_by_b[k][i]
                    if DEBUG:
                        print "aux:{0}".format(aux)

            if DEBUG:
                print "d[{0}] = {1}".format(k,aux)
            d[k] = aux

        #print d
        return d


def sum_pol(p1, p2):
    if len(p1) == max(p1,p2):
        temp = [0]*(len(p2))
        for i in xrange(0,len(p2)):
            temp[i] = ((p1[i] + p2[i]) %2)
        temp = temp + p1[len(p2):]
        print "sum_pol:te{0}".format(temp)
        print "sum_pol:p1{0}".format(p1)
        return temp
    else:
        temp = [0]*(len(p1))
        for i in xrange(0,len(p1)):
            temp[i] = ((p1[i] + p2[i]) %2)
        temp = temp + p2[len(p1):]
        print "sum_pol:te{0}".format(temp)
        print "sum_pol:p2{0}".format(p2)
        return temp

def concat_pol(pol, m):
    #print m
    to_append = [0]*m
    return (to_append + pol)

def split_at(pol, m):
    #print pol
    return pol[m:], pol[:m]

def karatsuba(pol_1, pol_2):

    max_deg_p1_p2 = max_degree(pol_1,pol_2)
    if DEBUG:
        print "karatsuba: p1:{0}, p2:{1}".format(pol_1,pol_2)
    if (max_deg_p1_p2 < 3):
        return mult(pol_1, pol_2)

    m = int(math.floor(float(max_deg_p1_p2)/float(2)))
    #print "m = ", m
    pol_1_high, pol_1_low = split_at(pol_1, m)
    if DEBUG:
        print "karatsuba::pol_1_high:{0}, pol_1_low:{1}".format(pol_1_high,pol_1_low)
    pol_2_high, pol_2_low = split_at(pol_2, m)
    if DEBUG:
        print "karatsuba::pol_2_high:{0}, pol_2_low:{1}".format(pol_2_high,pol_2_low)

    z0 = karatsuba(pol_1_low, pol_2_low)
    if DEBUG:
        print "karatsuba::z0:{0}, pol_1_low:{1},pol_2_low:{2}".format(z0,pol_1_low,pol_2_low)
    temp_1 = sum_pol(pol_1_low, pol_1_high)
    temp_2 = sum_pol(pol_2_low, pol_2_high)
    z1 = karatsuba(temp_1, temp_2)
    if DEBUG:
        print "karatsuba::z1:{0}, temp_1:{1},temp_2:{2}".format(z1,temp_1,temp_2)
    z2 = karatsuba(pol_1_high, pol_2_high)
    if DEBUG:
        print "karatsuba::z2:{0}, pol_1_high:{1},pol_2_high:{2}".format(z2,pol_1_high,pol_2_high)
    #return (z2*10^(2*m2))+((z1-z2-z0)*10^(m2))+(z0)
    if DEBUG:
        print "karatsuba::z0:{0}".format(z0)
    temp_3 = sum_pol(z1,z2)
    if DEBUG:
        print "karatsuba::sum_pol(z1,z2):{0}, z1:{1}, z2:{2}".format(temp_3, z1,z2)
    temp_4 = sum_pol(temp_3, z0)
    if DEBUG:
        print "karatsuba::sum_pol(temp_3,z0):{0}, temp_3:{1}, z0:{2}".format(temp_4, temp_3,z0)
    if DEBUG:
        print "karatsuba::z0:{0}, temp_4:{1}, z2:{2}".format(z0, temp_4,z2)

    concat_1 = (concat_pol(temp_4, m))
    print "concat_1:{0}".format(concat_1)
    print_pol(concat_1)
    concat_2 = concat_pol(z2,(2*m))
    print "concat_2:{0}".format(concat_2)
    print_pol(concat_2)
    sum_1 = sum_pol(z0, concat_1)
    sum_2 = sum_pol(sum_1, concat_2)
    result  = z0 + temp_4 + z2
    return result

    #return (z0 +  (concat_pol(temp_4, m)) + concat_pol(z2,(2*m)))

pol_1 = [1,1,1,1]
print_pol(pol_1)
pol_2 = [1,1,1,0]
print_pol(pol_2)
result = karatsuba(pol_1, pol_2)
print_pol(result)
