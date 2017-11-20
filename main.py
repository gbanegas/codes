from karatsuba_pol import *

def main():
    kara = Karatsuba()
    pol_1 = [1,1,1]
    kara.print_pol(pol_1)
    pol_2 = [1,1,0]
    kara.print_pol(pol_2)
    result= kara.karatsuba(pol_1, pol_2)
    kara.print_pol(result)
    print "Degree: ", len(pol_1)
    print "XORS: ", kara.get_nr_xor()
    print "ANDs: ", kara.get_nr_and()

if __name__ == "__main__":
    main()
