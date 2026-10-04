n, k=input().split()
n=int(n)
k=int(k)
fst=[]
scd=[]
for i in range(n+k):
    if(i<n):
        fst.append(input())
    else:
        scd.append(input())
def form(array):
    print(array)
    if((s.isdigit() for s in array[0:3]) and (array[4] == "a" or array[4] == "b" or array[4] == "c") and (array[5] == "-") and (s.islower() for s in array[6:8]) and (s.isdigit() for s in array[9:14]) and (array[len(array)-1]!=" ")):
        print("tr")
        return 1
    else:
        print("fals")
        return 0
PR=0
RC=0
TP=0
TPP=0
for i in range(n+k):
    if(i<n): 
        TPP+=form(fst[i])
        TP+=form(fst[i])
    else:
        TP+=form(scd[i-n])
PR=TPP/n
RC=(n)/(TP)
print("{:.4f} {:.4f}".format(PR, RC))
print(str(TPP)+" "+str(TP))
print(str(n)+" "+str(k))
#0023a-gps002300