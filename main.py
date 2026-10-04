def cUp(ar, x, y):
    for i in range(y):
        if(ar[i][x]==1): return 1
    return 0
def cDown(ar, x, y, n):
    for i in range(y+1, n):
        if(ar[i][x]==1): return 1
    return 0
def cLeft(ar, x, y):
    for i in range(x):
        if(ar[y][i]==1): return 1
    return 0
def cRight(ar, x, y, m):
    for i in range(x+1, m):
        if(ar[y][i]==1): return 1
    return 0
def Sides(ar, x, y, n, m):
    return cUp(ar, x, y)+cDown(ar, x, y, n)+cLeft(ar, x, y)+cRight(ar, x, y, m)
def O(ar, x, y):
    return not(ar[y][x])
def Count(ar, n, m):
    count=0
    for y in range(n):
        for x in range(m):
            if O(ar, x, y): count+=Sides(ar, x, y, n, m)
    return count

n, m=[int(v) for v in input().split()]
ar = []
for j in range(n):
    N=[int(v) for v in input().split()]
    ar.append(N)

print(Count(ar, n, m))