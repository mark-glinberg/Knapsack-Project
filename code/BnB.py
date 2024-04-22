#this file takes care of everything related to Branch and Bound including data parsing
from queue import PriorityQueue
import time 

#this function parses the input directory and returns Total Weight Allowed and Knapsack Items
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

#this class defined the Node object which as level, weight, profit and state as described in our paper
class Node:
    def __init__(self, level, weight, profit, state):
        self.level = level
        self.weight = weight
        self.profit = profit
        self.state = state
    #define a comparator so Priority Queue doesn't error
    def __lt__(self, other):
        return other.weight - self.weight

#this class calculates the upper bound of a node configuration
#arg1 node: current node configuration
#arg2 n: number of items in knapsack
#arg3 arr: array of items sorted via profit to weight ratio
#arg4 init: if true return approximation solution else return upper bound from fractional knapsack approach
def bound(node, n, W, arr, init=False):
    if node.weight >= W:
        return 0
 
    u_bound = node.profit
    j = node.level + 1
    t_w = node.weight
 
    while j < n and t_w + arr[j][1] <= W:
        u_bound += arr[j][0]
        t_w += arr[j][1]
        j += 1
    
    if init:
        return u_bound, j

    if j < n:
        u_bound += ((W - t_w) * arr[j][0] / arr[j][1])
 
    return u_bound

#This function solves the knapsack problem using Branch and Bound
#arg1 W: total allowable weight
#arg2 arr: array of knapsack items
#arg3 n: number of items
#arr4 maxTime: maximum time allowed in solving the question
def solution(W, arr, n, maxTime = float('inf')):
    start = time.time()
    #sort array via profit to weight ratio
    arr.sort(key=lambda x: x[0] / x[1], reverse=True)
     
    priority_queue = PriorityQueue()
    curr = Node(-1, 0, 0, []) #starting configuration where no items are considered
    #items in priority Queue are tuples of (-profit, Node) so the maximum profit is prioritized
    #Tested relying on defining the comparator in the Node definition itself but its buggy
    priority_queue.put((0, curr))
    
    #set a good max profit from approximation to allow more pruning
    max_profit, end = bound(curr, n, W, arr, init=True)
    res_state = [i for i in range(end)]
    traces = []
    is_optim = True
 
    while not priority_queue.empty():
        if time.time() - start > maxTime:
            is_optim = False
            break
        _, curr = priority_queue.get()
 
        if curr.level == -1:
            next = Node(0, 0, 0, [])
        elif curr.level == n - 1:
            continue
        else:
            next = Node(curr.level + 1, curr.weight, curr.profit, list(curr.state))

        #expand next state where item considered is chosen
        next.profit += arr[next.level][0]
        next.weight += arr[next.level][1]
        next.state.append(next.level)
        #update max if current partial solution is valid and better
        if next.weight <= W and next.profit > max_profit:
            max_profit = next.profit
            res_state = list(next.state)
            traces.append([round(time.time()-start,2), max_profit])
 
        next_bound = bound(next, n, W, arr)
        #prune if upperbound is less than current max profit
        if next_bound > max_profit:
            priority_queue.put((-next.profit, next))

        #expand next state where item considered is not chosen
        next = Node(curr.level + 1, curr.weight, curr.profit, list(curr.state))
        next_bound = bound(next, n, W, arr)
        #prune if upperbound is less than current max profit
        if next_bound > max_profit:
            priority_queue.put((-next.profit, next))
    ret_state = []
    for i in res_state:
        #append resultant state using the original index instead of sorted index
        ret_state.append(arr[i][2])
    ret_state.sort()

    return max_profit, ret_state, traces, is_optim

#this function gets the problem from a directory and generates the solution and trace where it needs to be
def BnB_knapsack(in_dir, cutoff=60):
    totcst, node_group = parse_input(in_dir)
    arr = [(node_group[i][0], node_group[i][1], i) for i in range(len(node_group))]
    n = len(arr)
    start = time.time()
    max_profit, state, traces, _ = solution(totcst, arr, n, cutoff)
    end = time.time()
    return max_profit, state, traces, end-start
