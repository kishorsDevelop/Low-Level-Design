from collections import defaultdict
def simplify(transactions):
    map = {}
    for trans in transactions:
        map[trans[0]] = map.get(trans[0], 0) - trans[2]
        map[trans[1]] = map.get(trans[1], 0) + trans[2]

    balance = []
    for val in map.values():
        if val != 0:
           balance.append(val)
    return dfs(balance, 0)

def dfs(balance, ind):
    
    if balance[ind] == 0:
        return ind
    
    while ind < len(balance) and balance[ind] == 0:
        ind += 1
    
    res = float('inf')
    for i in range(ind+1, len(balance)):
        if balance[i] * balance[ind] < 0:
            balance[i] += balance[ind]
            res = min(res, 1 + dfs(balance, ind+1))
            balance[i] -= balance[ind]
    
    return res