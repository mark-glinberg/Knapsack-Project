from queue import PriorityQueue
import time 

def parse_input(indir):
    items = []
    ret = []
    with open(indir, 'r') as file:
        for i in file:
            items.append(i.replace('\n', ''))
    n = int(items[0].split(" ")[0])
    cnt = int(items[0].split(" ")[1])
    items = items[1:n+1]
    for item in items:
        spt = item.split(" ")
        ret.append([float(spt[0]), float(spt[1])])
    return cnt, ret
 
class Node:
    def __init__(self, level, weight, profit, state):
        self.level = level
        self.profit = profit
        self.weight = weight
        self.state = state
 
    def __lt__(self, other):
        return other.weight - self.weight

def bound(node, n, W, arr):
    if node.weight >= W:
        return 0
 
    u_bound = node.profit
    j = node.level + 1
    t_w = node.weight
 
    while j < n and t_w + arr[j][1] <= W:
        u_bound += arr[j][0]
        t_w += arr[j][1]
        j += 1

    if j < n:
        u_bound += ((W - t_w) * arr[j][0] / arr[j][1])
 
    return u_bound
 
def solution(W, arr, n, maxTime = float('inf')):
    start = time.time()
    arr.sort(key=lambda x: x[0] / x[1], reverse=True)
     
    priority_queue = PriorityQueue()
    curr = Node(-1, 0, 0, [])
    priority_queue.put(curr)
 
    max_profit = 0
    res_state = None
    traces = []
    is_optim = True
 
    while not priority_queue.empty():
        if time.time() - start > maxTime:
            is_optim = False
            break
        curr = priority_queue.get()
 
        if curr.level == -1:
            next = Node(0, 0, 0, [])
        elif curr.level == n - 1:
            continue
        else:
            next = Node(curr.level + 1, curr.weight, curr.profit, list(curr.state))

        next.profit += arr[next.level][0]
        next.weight += arr[next.level][1]
        next.state.append(next.level)
        if next.weight <= W and next.profit > max_profit:
            max_profit = next.profit
            res_state = list(next.state)
            traces.append([round(time.time()-start,2), max_profit])
 
        next_bound = bound(next, n, W, arr)
        if next_bound > max_profit:
            priority_queue.put(next)
 
        next = Node(curr.level + 1, curr.weight, curr.profit, list(curr.state))
        next_bound = bound(next, n, W, arr)
        if next_bound > max_profit:
            priority_queue.put(next)
    ret_state = []
    for i in res_state:
        ret_state.append(arr[i][2])
    ret_state.sort()

    return max_profit, ret_state, traces, is_optim

def BnB_knapsack(in_dir, cutoff=60, dir_solution="", dir_trace=""):
    in_dir = in_dir.replace('\\', '/')
    dir_solution = dir_solution.replace('\\', '/')
    dir_trace = dir_trace.replace('\\', '/')
    if dir_solution != "":
        dir_solution += '/'
    if dir_trace != "":
        dir_trace += '/'
    totcst, node_group = parse_input(in_dir)

    arr = [(node_group[i][0], node_group[i][1], i) for i in range(len(node_group))]
    n = len(arr)
    
    max_profit, state, traces, _ = solution(totcst, arr, n, cutoff)
    return max_profit, state, traces
