def kthFactor (n, k):
        counter = 1
        print(n)
        while(counter <= (n / 2) and k >= 0):
            if(n % counter == 0):
                k -= 1
                if(k == 0):
                    return counter
            counter += 1
        return -1
        
print(kthFactor(46,3))
print(kthFactor(267,3))
print(kthFactor(4141,3))
print(kthFactor(414,3))