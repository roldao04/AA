# Algorithm Design Strategies - Comprehensive Study Guide

## Table of Contents
1. [Introduction to Algorithm Design](#introduction)
2. [Divide and Conquer](#divide-and-conquer)
3. [Dynamic Programming](#dynamic-programming)
4. [Greedy Algorithms](#greedy-algorithms)
5. [Backtracking](#backtracking)
6. [Branch and Bound](#branch-and-bound)
7. [Other Important Strategies](#other-strategies)

---

## Introduction to Algorithm Design {#introduction}

### What is Algorithm Design?

Algorithm design is the process of creating step-by-step procedures to solve computational problems efficiently. The goal is not just to find *a* solution, but to find an *efficient* solution that minimizes resource usage (time and space).

### Why Study Design Strategies?

Rather than approaching each problem from scratch, we can use proven **design paradigms** - general strategies that work across many different problems. Understanding these paradigms allows you to:

- Recognize problem patterns quickly
- Apply known solutions to new problems
- Analyze and optimize existing algorithms
- Choose the right approach for each situation

### Key Complexity Classes

Before diving into strategies, recall these complexity classes:
- **O(1)**: Constant time - independent of input size
- **O(log n)**: Logarithmic - typically dividing the problem in half repeatedly
- **O(n)**: Linear - proportional to input size
- **O(n log n)**: Linearithmic - efficient sorting algorithms
- **O(n²)**: Quadratic - nested iterations
- **O(2ⁿ)**: Exponential - typically brute force approaches
- **O(n!)**: Factorial - permutation-based problems

---

## Divide and Conquer {#divide-and-conquer}

### Core Concept

Divide and Conquer is a problem-solving paradigm that works by:

1. **Divide**: Break the problem into smaller subproblems of the same type
2. **Conquer**: Solve the subproblems recursively (base case: solve directly when small enough)
3. **Combine**: Merge the subproblem solutions to create the solution to the original problem

### When to Use Divide and Conquer

This strategy works well when:
- The problem can be broken into independent subproblems
- Subproblems are similar to the original problem (recursive structure)
- Solutions to subproblems can be combined efficiently

### Classic Examples

#### 1. Merge Sort

**Problem**: Sort an array of n elements

**Algorithm**:
```
MergeSort(A, left, right):
    if left < right:
        mid = (left + right) / 2
        MergeSort(A, left, mid)      // Divide: sort left half
        MergeSort(A, mid+1, right)   // Divide: sort right half
        Merge(A, left, mid, right)   // Combine: merge sorted halves
```

**Key Insight**: If we can sort two halves, merging them is O(n). The divide step creates a balanced recursion tree.

**Complexity**:
- Time: O(n log n) - log n levels, n work per level
- Space: O(n) - for the merge operation

**Recurrence**: T(n) = 2T(n/2) + O(n)

#### 2. Quick Sort

**Problem**: Sort an array of n elements

**Algorithm**:
```
QuickSort(A, low, high):
    if low < high:
        pivot = Partition(A, low, high)  // Choose pivot, partition array
        QuickSort(A, low, pivot-1)       // Sort elements < pivot
        QuickSort(A, pivot+1, high)      // Sort elements > pivot
```

**Key Insight**: After partitioning around a pivot, the pivot is in its final position. The two subarrays can be sorted independently.

**Complexity**:
- Best/Average: O(n log n)
- Worst: O(n²) - when pivot choices are poor (already sorted array with bad pivot selection)
- Space: O(log n) - recursion stack

**Recurrence**:
- Average: T(n) = 2T(n/2) + O(n)
- Worst: T(n) = T(n-1) + O(n)

#### 3. Binary Search

**Problem**: Find an element in a sorted array

**Algorithm**:
```
BinarySearch(A, target, left, right):
    if left > right:
        return NOT_FOUND
    mid = (left + right) / 2
    if A[mid] == target:
        return mid
    if A[mid] > target:
        return BinarySearch(A, target, left, mid-1)
    else:
        return BinarySearch(A, target, mid+1, right)
```

**Key Insight**: In a sorted array, comparing with the middle element tells us which half contains the target (if it exists).

**Complexity**:
- Time: O(log n)
- Space: O(log n) for recursive version, O(1) for iterative

**Recurrence**: T(n) = T(n/2) + O(1)

#### 4. Maximum Subarray Problem (Divide & Conquer Approach)

**Problem**: Find the contiguous subarray with the largest sum

**Algorithm**: The maximum subarray is either:
- Entirely in the left half
- Entirely in the right half
- Crosses the midpoint

**Complexity**: O(n log n)

**Note**: This can be solved more efficiently with Dynamic Programming (Kadane's algorithm) in O(n).

### Master Theorem

The Master Theorem helps us solve recurrences of the form:
**T(n) = aT(n/b) + f(n)**

Where:
- a = number of subproblems
- n/b = size of each subproblem
- f(n) = cost of divide and combine steps

**Three Cases**:
1. If f(n) = O(n^c) where c < log_b(a): T(n) = Θ(n^(log_b(a)))
2. If f(n) = Θ(n^c) where c = log_b(a): T(n) = Θ(n^c log n)
3. If f(n) = Ω(n^c) where c > log_b(a): T(n) = Θ(f(n))

**Examples**:
- Merge Sort: T(n) = 2T(n/2) + O(n) → Case 2 → O(n log n)
- Binary Search: T(n) = T(n/2) + O(1) → Case 1 → O(log n)

### Key Takeaways

- Divide and Conquer naturally leads to recursive solutions
- Often achieves O(n log n) or O(log n) complexity
- The efficiency depends on balanced divisions and efficient combining
- Use the Master Theorem to analyze complexity

---

## Dynamic Programming {#dynamic-programming}

### Core Concept

Dynamic Programming (DP) is an optimization technique for solving problems by:

1. **Breaking down** the problem into overlapping subproblems
2. **Storing** solutions to subproblems to avoid redundant computation
3. **Building up** solutions from smaller to larger subproblems

**Key Difference from Divide & Conquer**: Subproblems overlap (same subproblem solved multiple times), so we **memoize** (cache) results.

### When to Use Dynamic Programming

DP is ideal when:
- The problem has **optimal substructure** (optimal solution contains optimal solutions to subproblems)
- There are **overlapping subproblems** (same subproblems appear multiple times)
- You can define a recurrence relation

### Two Approaches

1. **Top-Down (Memoization)**: Write recursive solution, cache results
2. **Bottom-Up (Tabulation)**: Fill a table iteratively from base cases up

### Classic Examples

#### 1. Fibonacci Numbers

**Problem**: Compute the nth Fibonacci number (F(n) = F(n-1) + F(n-2))

**Naive Recursion**: O(2ⁿ) - exponential due to repeated calculations

**DP Solution (Memoization)**:
```
Fib(n, memo):
    if n <= 1:
        return n
    if memo[n] is not computed:
        memo[n] = Fib(n-1, memo) + Fib(n-2, memo)
    return memo[n]
```

**DP Solution (Tabulation)**:
```
Fib(n):
    dp[0] = 0, dp[1] = 1
    for i from 2 to n:
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]
```

**Complexity**: O(n) time, O(n) space (can be optimized to O(1) space)

#### 2. 0/1 Knapsack Problem

**Problem**: Given items with weights and values, and a knapsack capacity W, maximize value without exceeding capacity.

**Recurrence**:
```
K(i, w) = maximum value using items 0..i with capacity w

K(i, w) = max(
    K(i-1, w),                    // don't take item i
    K(i-1, w - weight[i]) + value[i]  // take item i
)
```

**Base case**: K(0, w) = 0 (no items) or K(i, 0) = 0 (no capacity)

**Algorithm (Bottom-Up)**:
```
Knapsack(weights, values, W, n):
    dp[0..n][0..W] = 0
    for i from 1 to n:
        for w from 0 to W:
            if weights[i-1] <= w:
                dp[i][w] = max(
                    dp[i-1][w],
                    dp[i-1][w - weights[i-1]] + values[i-1]
                )
            else:
                dp[i][w] = dp[i-1][w]
    return dp[n][W]
```

**Complexity**: O(nW) time, O(nW) space (pseudo-polynomial - depends on W)

#### 3. Longest Common Subsequence (LCS)

**Problem**: Find the length of the longest subsequence common to two strings

**Recurrence**:
```
LCS(i, j) = LCS of X[0..i] and Y[0..j]

If X[i] == Y[j]:
    LCS(i, j) = LCS(i-1, j-1) + 1
Else:
    LCS(i, j) = max(LCS(i-1, j), LCS(i, j-1))
```

**Algorithm**:
```
LCS(X, Y):
    m = len(X), n = len(Y)
    dp[0..m][0..n] = 0
    for i from 1 to m:
        for j from 1 to n:
            if X[i-1] == Y[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]
```

**Complexity**: O(mn) time, O(mn) space

#### 4. Edit Distance (Levenshtein Distance)

**Problem**: Find minimum operations (insert, delete, substitute) to transform string X to Y

**Recurrence**:
```
If X[i] == Y[j]:
    ED(i, j) = ED(i-1, j-1)
Else:
    ED(i, j) = 1 + min(
        ED(i-1, j),     // delete from X
        ED(i, j-1),     // insert into X
        ED(i-1, j-1)    // substitute
    )
```

**Complexity**: O(mn) time, O(mn) space

#### 5. Matrix Chain Multiplication

**Problem**: Find optimal parenthesization to minimize scalar multiplications when multiplying a chain of matrices

**Key Insight**: The order matters! (A×B)×C may be cheaper than A×(B×C)

**Recurrence**:
```
M(i, j) = minimum multiplications to compute matrices i through j

M(i, j) = min over k in [i, j-1] of:
    M(i, k) + M(k+1, j) + cost of multiplying resulting matrices
```

**Complexity**: O(n³) time, O(n²) space

#### 6. Longest Increasing Subsequence (LIS)

**Problem**: Find the length of the longest strictly increasing subsequence in an array

**DP Approach 1** (O(n²)):
```
LIS(i) = length of longest increasing subsequence ending at index i

LIS(i) = 1 + max(LIS(j)) for all j < i where A[j] < A[i]
```

**DP Approach 2** (O(n log n)): Use binary search with auxiliary array

**Complexity**: O(n²) or O(n log n) depending on approach

#### 7. Coin Change Problem

**Problem**: Given coin denominations and an amount, find minimum coins needed (or number of ways)

**Minimum Coins Recurrence**:
```
MinCoins(amount) = 1 + min over all coins c of:
    MinCoins(amount - c)
```

**Number of Ways**:
```
Ways(amount, i) = Ways(amount, i-1) + Ways(amount - coin[i], i)
```

**Complexity**: O(n × amount) where n is number of coin types

### Identifying DP Problems

Ask yourself:
1. Can I break this into smaller subproblems?
2. Do subproblems overlap (get computed multiple times)?
3. Can I express the solution using a recurrence relation?
4. Is there an optimal substructure?

If yes to these, DP is likely a good approach.

### DP Design Process

1. **Define subproblems**: What does dp[i] or dp[i][j] represent?
2. **Find recurrence**: How does dp[i] relate to smaller subproblems?
3. **Identify base cases**: What are the smallest subproblems?
4. **Determine evaluation order**: What order ensures dependencies are met?
5. **Implement**: Top-down (memoization) or bottom-up (tabulation)

### Key Takeaways

- DP trades space for time by storing intermediate results
- Essential for optimization problems with overlapping subproblems
- Bottom-up often more efficient (no recursion overhead)
- Space can often be optimized (e.g., using rolling arrays)
- Pseudo-polynomial algorithms depend on numeric input values

---

## Greedy Algorithms {#greedy-algorithms}

### Core Concept

A greedy algorithm makes locally optimal choices at each step, hoping to find a global optimum. At each decision point, it:

1. Makes the choice that looks best **right now**
2. Never reconsiders that choice
3. Hopes this leads to a globally optimal solution

### When to Use Greedy Algorithms

Greedy works when the problem has:
- **Greedy choice property**: A global optimum can be reached by making locally optimal choices
- **Optimal substructure**: An optimal solution contains optimal solutions to subproblems

**Warning**: Greedy doesn't always work! You must **prove correctness** for each problem.

### Greedy vs Dynamic Programming

- **Greedy**: Makes one choice at each step, never looks back (faster, simpler)
- **DP**: Considers all options, stores results (guaranteed optimal if properly designed)

Some problems can be solved with either, but greedy is preferred when it works (more efficient).

### Classic Examples

#### 1. Activity Selection Problem

**Problem**: Given activities with start and finish times, select maximum number of non-overlapping activities

**Greedy Strategy**: Always pick the activity that finishes earliest (leaves most room for future activities)

**Algorithm**:
```
ActivitySelection(activities sorted by finish time):
    selected = [first activity]
    lastFinish = finish[0]
    for each activity i:
        if start[i] >= lastFinish:
            selected.append(i)
            lastFinish = finish[i]
    return selected
```

**Correctness**: Finishing early maximizes remaining time, so we can fit maximum activities

**Complexity**: O(n log n) for sorting, O(n) for selection

#### 2. Fractional Knapsack

**Problem**: Like 0/1 knapsack, but can take fractions of items

**Greedy Strategy**: Take items in order of value-to-weight ratio (value density)

**Algorithm**:
```
FractionalKnapsack(items, capacity):
    sort items by value/weight ratio (descending)
    totalValue = 0
    for each item:
        if capacity >= item.weight:
            take all of item
            capacity -= item.weight
            totalValue += item.value
        else:
            take fraction = capacity / item.weight
            totalValue += fraction × item.value
            break
    return totalValue
```

**Complexity**: O(n log n)

**Note**: The 0/1 version requires DP because we can't take fractions!

#### 3. Huffman Coding

**Problem**: Create optimal prefix-free binary encoding for characters based on frequencies

**Greedy Strategy**: Build tree bottom-up by repeatedly combining two nodes with smallest frequencies

**Algorithm**:
```
HuffmanCoding(frequencies):
    create leaf node for each character
    priority queue Q = all leaf nodes (by frequency)
    while Q.size() > 1:
        left = Q.extractMin()
        right = Q.extractMin()
        parent = new node with frequency = left.freq + right.freq
        parent.left = left, parent.right = right
        Q.insert(parent)
    return Q.top() as root
```

**Complexity**: O(n log n) using a heap

**Key Insight**: Least frequent characters should have longest codes

#### 4. Minimum Spanning Tree (MST)

**Problem**: Given weighted graph, find tree connecting all vertices with minimum total edge weight

##### Kruskal's Algorithm

**Greedy Strategy**: Add edges in order of increasing weight, skip if creates cycle

**Algorithm**:
```
Kruskal(G):
    sort edges by weight
    MST = empty
    for each edge (u,v) in sorted order:
        if u and v are in different components:
            add (u,v) to MST
            union components of u and v
    return MST
```

**Data Structure**: Union-Find for efficient component tracking

**Complexity**: O(E log E) where E is number of edges

##### Prim's Algorithm

**Greedy Strategy**: Grow tree from starting vertex by adding minimum weight edge to tree

**Algorithm**:
```
Prim(G, start):
    MST = empty
    visited = {start}
    priority queue Q = edges from start
    while Q not empty:
        edge (u,v) = Q.extractMin()
        if v not in visited:
            add (u,v) to MST
            visited.add(v)
            add all edges from v to Q
    return MST
```

**Complexity**: O(E log V) with binary heap, O(E + V log V) with Fibonacci heap

#### 5. Dijkstra's Shortest Path

**Problem**: Find shortest paths from source to all vertices in weighted graph (non-negative weights)

**Greedy Strategy**: Always extend the shortest known path

**Algorithm**:
```
Dijkstra(G, source):
    dist[source] = 0, dist[all others] = ∞
    priority queue Q = all vertices (by dist)
    while Q not empty:
        u = Q.extractMin()
        for each neighbor v of u:
            if dist[u] + weight(u,v) < dist[v]:
                dist[v] = dist[u] + weight(u,v)
                Q.decreaseKey(v)
    return dist
```

**Complexity**: O((V + E) log V) with binary heap

**Important**: Doesn't work with negative edge weights (use Bellman-Ford instead)

#### 6. Job Sequencing with Deadlines

**Problem**: Given jobs with deadlines and profits, schedule jobs to maximize profit

**Greedy Strategy**: Sort jobs by profit (descending), assign each to latest available slot before deadline

**Complexity**: O(n²) or O(n log n) with better data structures

### Proving Greedy Correctness

Common proof techniques:

1. **Exchange Argument**: Show that any solution can be transformed to greedy solution without losing optimality

2. **Staying Ahead**: Show greedy solution is always "ahead" of or "as good as" any other solution at each step

3. **Structural**: Prove the greedy choice property and optimal substructure

### When Greedy Fails

Examples where greedy doesn't work:
- **0/1 Knapsack**: Can't take fractions, need DP
- **Longest Path**: Greedy picks wrong initial choices
- **Coin Change** (certain denominations): Greedy may not find minimum coins

### Key Takeaways

- Greedy is fast and simple but requires proof of correctness
- Look for problems where local optimum leads to global optimum
- Often involves sorting and priority queues
- When greedy fails, consider Dynamic Programming
- Common in graph problems (MST, shortest paths) and scheduling

---

## Backtracking {#backtracking}

### Core Concept

Backtracking is a systematic way to search all possible solutions by:

1. **Building** a solution incrementally
2. **Abandoning** a partial solution as soon as it's determined to be invalid (pruning)
3. **Backtracking** to try other options

Think of it as exploring a decision tree with DFS (Depth-First Search), pruning branches that can't lead to valid solutions.

### When to Use Backtracking

Use backtracking for:
- **Constraint satisfaction problems** (CSPs)
- **Combinatorial search** (permutations, combinations)
- Problems where you need to find all solutions or one valid solution
- Problems with clear constraints that allow pruning

### General Template

```
Backtrack(solution):
    if solution is complete:
        process/store solution
        return

    for each candidate choice:
        if choice is valid (satisfies constraints):
            make choice (add to solution)
            Backtrack(updated solution)
            undo choice (backtrack)
```

### Classic Examples

#### 1. N-Queens Problem

**Problem**: Place N queens on N×N chessboard so no two queens attack each other

**Constraints**: No two queens in same row, column, or diagonal

**Algorithm**:
```
SolveNQueens(board, row):
    if row == N:
        found a solution, store it
        return

    for col from 0 to N-1:
        if safe to place queen at (row, col):
            place queen at (row, col)
            SolveNQueens(board, row + 1)
            remove queen from (row, col)  // backtrack
```

**Pruning**: Check diagonals and columns before placing queen

**Complexity**: O(N!) in worst case, much better with pruning

#### 2. Sudoku Solver

**Problem**: Fill 9×9 grid so each row, column, and 3×3 box contains digits 1-9

**Algorithm**:
```
SolveSudoku(board):
    find next empty cell (row, col)
    if no empty cell:
        return true  // solved

    for digit from 1 to 9:
        if valid to place digit at (row, col):
            place digit
            if SolveSudoku(board):
                return true
            remove digit  // backtrack

    return false  // trigger backtracking
```

**Complexity**: O(9^m) where m is number of empty cells (worst case)

#### 3. Graph Coloring

**Problem**: Color graph vertices so no adjacent vertices have same color, using minimum colors

**Algorithm**:
```
GraphColoring(vertex, colors):
    if all vertices colored:
        return true

    for each color:
        if color is safe for vertex:
            assign color to vertex
            if GraphColoring(next vertex, colors):
                return true
            remove color from vertex  // backtrack

    return false
```

**Complexity**: Exponential, but pruning helps significantly

#### 4. Subset Sum

**Problem**: Find if there's a subset of numbers that sums to target

**Algorithm**:
```
SubsetSum(numbers, index, currentSum, target):
    if currentSum == target:
        return true
    if index >= len(numbers) or currentSum > target:
        return false

    // Include current number
    if SubsetSum(numbers, index+1, currentSum + numbers[index], target):
        return true

    // Exclude current number
    return SubsetSum(numbers, index+1, currentSum, target)
```

**Complexity**: O(2ⁿ) without pruning

#### 5. Hamiltonian Path/Cycle

**Problem**: Find path visiting each vertex exactly once (cycle: return to start)

**Algorithm**:
```
HamiltonianPath(path, vertex):
    if path length == N:
        return true if valid

    for each unvisited neighbor of vertex:
        add neighbor to path
        mark as visited
        if HamiltonianPath(path, neighbor):
            return true
        remove neighbor from path  // backtrack
        mark as unvisited

    return false
```

**Complexity**: O(N!) in worst case

### Optimization Techniques

1. **Constraint Propagation**: After each choice, deduce implications to reduce search space

2. **Ordering Heuristics**:
   - **Most Constrained Variable**: Choose variable with fewest legal values first
   - **Least Constraining Value**: Choose value that rules out fewest options for other variables

3. **Early Termination**: Stop as soon as one solution is found (if that's all we need)

4. **Symmetry Breaking**: Avoid exploring symmetric configurations

### Backtracking vs Brute Force

- **Brute Force**: Generates all possible solutions, then checks validity
- **Backtracking**: Prunes invalid partial solutions early (much more efficient)

### Key Takeaways

- Backtracking is systematic exhaustive search with pruning
- Exponential time complexity but much better than brute force
- Critical to identify constraints for effective pruning
- Recursive implementation is natural and clean
- Used when other strategies (greedy, DP) don't apply

---

## Branch and Bound {#branch-and-bound}

### Core Concept

Branch and Bound is an optimization technique that:

1. **Branches**: Explores solution space systematically (like backtracking)
2. **Bounds**: Calculates bounds on the objective function to prune branches
3. **Prunes**: Eliminates branches that can't possibly lead to better solutions than the current best

It's used for **optimization problems** (finding best solution), whereas backtracking is for **constraint satisfaction** (finding any valid solution).

### When to Use Branch and Bound

Use when:
- You need an optimal solution, not just any valid solution
- You can compute bounds (lower/upper) on partial solutions
- The problem is NP-hard but instances are small enough
- You want exact solutions (not approximations)

### Key Components

1. **Bounding Function**: Estimates best possible objective value from current partial solution
   - **Lower bound** for minimization problems
   - **Upper bound** for maximization problems

2. **Branching Strategy**: How to explore the solution space (BFS, DFS, best-first)

3. **Selection Rule**: Which node to expand next

4. **Pruning Rule**: When to discard a branch

### General Algorithm

```
BranchAndBound():
    initialize queue with root node
    bestSolution = null
    bestValue = ∞ (for minimization)

    while queue not empty:
        node = select node from queue

        if node is complete solution:
            if node.value < bestValue:
                bestValue = node.value
                bestSolution = node
        else:
            bound = compute bound for node
            if bound < bestValue:  // promising
                branch: generate child nodes
                add children to queue
            // else: prune this branch

    return bestSolution
```

### Classic Examples

#### 1. 0/1 Knapsack (Branch and Bound)

**Problem**: Maximize value in knapsack without exceeding capacity (items are indivisible)

**Bounding Function**: Use fractional knapsack (greedy) as upper bound

**Algorithm**:
```
Sort items by value/weight ratio
Use priority queue (best-first search by bound)
For each node:
    Bound = current value + fractional knapsack on remaining items
    If bound > bestValue:
        Branch: include next item or exclude it
    Else:
        Prune
```

**Why it works**: Fractional solution provides optimistic upper bound; if even that isn't better than current best, no point exploring

**Complexity**: Exponential worst case, but often much faster than backtracking

#### 2. Traveling Salesman Problem (TSP)

**Problem**: Find shortest tour visiting all cities exactly once

**Bounding Function**: Use minimum spanning tree (MST) of unvisited cities + current path cost

**Algorithm**:
```
Start at root (empty tour)
For each partial tour:
    Lower bound = current tour cost + MST of unvisited cities
    If bound >= bestTourCost:
        Prune
    Else:
        Branch by adding each unvisited city
```

**Other bounds**: Minimum outgoing edges, linear relaxation

**Complexity**: O(N!) worst case, but effective pruning reduces this significantly

#### 3. Job Assignment Problem

**Problem**: Assign N jobs to N workers to minimize total cost

**Bounding Function**: Current assignment cost + minimum cost for remaining jobs (using greedy or relaxation)

**Hungarian Algorithm** solves this in polynomial time, but B&B shows the general approach

#### 4. Integer Linear Programming (ILP)

**Problem**: Optimize linear objective function with integer constraints

**Bounding Function**: Solve LP relaxation (allow fractional values)

**Algorithm**:
```
Solve LP relaxation
If solution is integer:
    Done
Else:
    Pick fractional variable x
    Branch: x ≤ ⌊x⌋ and x ≥ ⌈x⌉
    Solve LP for both branches
    Prune if bound worse than incumbent
```

This is the basis for **B&B solvers** used in commercial optimization software

### Search Strategies

1. **Breadth-First Search (BFS)**: Explore level by level (fair but memory-intensive)

2. **Depth-First Search (DFS)**: Explore deeply (less memory, may waste time on bad branches)

3. **Best-First Search**: Expand node with best bound (often most effective)

4. **Least-Cost Search**: Expand node with lowest cost so far

### Comparison with Other Methods

| Method | Goal | Pruning | Guarantee |
|--------|------|---------|-----------|
| Backtracking | Find valid solution | Constraint-based | First valid solution |
| Branch & Bound | Find optimal solution | Bound-based | Optimal solution |
| Greedy | Fast heuristic | None | No guarantee |
| Dynamic Programming | Optimal solution | None (all subproblems) | Optimal if applicable |

### Key Takeaways

- Branch and Bound guarantees optimal solution but is exponential
- Effective bounding function is crucial for performance
- Best-first search often outperforms BFS and DFS
- Used for NP-hard optimization problems where exact solution is needed
- Trade-off: Guaranteed optimality vs. computation time
- For large instances, may need to use heuristics or approximation algorithms instead

---

## Other Important Strategies {#other-strategies}

### 1. Transform and Conquer

**Concept**: Transform the problem into another form that's easier to solve

**Types**:
- **Instance simplification**: Preprocess data (e.g., sorting before searching)
- **Representation change**: Change data structure (e.g., tree to array)
- **Problem reduction**: Transform to a known problem

**Examples**:
- **Presorting**: Sort array before binary search, finding median, etc.
- **Balanced Search Trees**: AVL, Red-Black trees - transform to maintain balance
- **Gaussian Elimination**: Transform linear system to row-echelon form
- **Heap construction**: Transform array to heap structure

### 2. Space-Time Tradeoffs

**Concept**: Use extra space to save time (or vice versa)

**Techniques**:

**Hashing**:
- Trade space for O(1) average lookup time
- Hash tables, hash maps
- Applications: Caching, database indexing, symbol tables

**String Matching**:
- **Boyer-Moore**: Preprocess pattern to skip characters
- **Knuth-Morris-Pratt (KMP)**: Preprocess pattern to avoid backtracking
- Both use O(m) extra space to achieve O(n) time

**Dynamic Programming Tables**: Store subproblem solutions

**Precomputation**:
- Prefix sums: O(n) space for O(1) range sum queries
- Suffix arrays: O(n) space for efficient string operations

### 3. Decrease and Conquer

**Concept**: Reduce problem to smaller instance by a constant amount or factor

**Varieties**:

**Decrease by constant** (usually 1):
- **Insertion Sort**: Sort n-1 elements, insert nth element
- **Graph DFS/BFS**: Visit one vertex, recurse on remaining
- **Topological Sort**: Remove vertex with no incoming edges, repeat

**Decrease by constant factor** (usually half):
- **Binary Search**: Eliminate half the array each step
- **Exponentiation by Squaring**: Compute x^n in O(log n) by x^n = (x^(n/2))^2
- **Russian Peasant Multiplication**: Multiply in O(log n)

**Variable size decrease**:
- **Euclid's GCD**: GCD(a,b) = GCD(b, a mod b)
- **Nim Game**: Reduce by variable amount each turn

### 4. Randomized Algorithms

**Concept**: Use randomness to achieve good average-case performance

**Types**:

**Las Vegas algorithms**: Always correct, randomized runtime
- Example: Randomized QuickSort (random pivot selection)

**Monte Carlo algorithms**: Fixed runtime, probability of error
- Example: Primality testing (Miller-Rabin)

**Examples**:
- **Randomized QuickSort**: Expected O(n log n), avoids worst case
- **Randomized Selection**: Find kth smallest in expected O(n)
- **Skip Lists**: Randomized balanced search structure
- **Bloom Filters**: Probabilistic set membership

### 5. Approximation Algorithms

**Concept**: Find near-optimal solutions efficiently for NP-hard problems

**Performance Ratio**:
- Algorithm is ρ-approximation if solution ≤ ρ × optimal (minimization)

**Examples**:
- **Vertex Cover**: 2-approximation in polynomial time
- **TSP**: 2-approximation for metric TSP (triangle inequality)
- **Bin Packing**: First-fit is 2-approximation
- **Set Cover**: Greedy is O(log n)-approximation

**Trade-off**: Give up optimality for polynomial runtime

### 6. Online Algorithms

**Concept**: Make decisions without knowing future inputs

**Competitive Analysis**: Compare to optimal offline algorithm

**Examples**:
- **Caching**: LRU (Least Recently Used), LFU (Least Frequently Used)
- **Scheduling**: Makespan minimization
- **k-Server Problem**: Serve requests with k mobile servers

### 7. Parallel Algorithms

**Concept**: Divide work among multiple processors

**Models**:
- PRAM (Parallel Random Access Machine)
- Map-Reduce paradigm
- GPU computing

**Examples**:
- **Parallel Merge Sort**: Parallelize recursive calls
- **Parallel Matrix Multiplication**: Distribute computation
- **Map-Reduce**: Distributed data processing

**Metrics**: Speedup, efficiency, scalability

### 8. Bit Manipulation Techniques

**Concept**: Use bit-level operations for efficiency

**Applications**:
- **Set Operations**: Union, intersection using bitwise OR, AND
- **Subsets**: Iterate through all subsets using bit patterns
- **XOR Tricks**: Find single unique number, swap without temp variable
- **Brian Kernighan's Algorithm**: Count set bits efficiently
- **Power of Two**: Check if n is power of 2 using n & (n-1) == 0

### 9. Two Pointers Technique

**Concept**: Use two pointers to traverse data structure efficiently

**Applications**:
- **Two Sum (sorted array)**: O(n) with left and right pointers
- **Remove Duplicates**: In-place array modification
- **Palindrome Check**: Compare from both ends
- **Sliding Window**: Maintain window with two pointers
- **Merge Two Sorted Arrays**: O(n) merge

### 10. Sliding Window

**Concept**: Maintain a window of elements and slide it through array

**Types**:
- **Fixed Size**: Window size is constant
- **Variable Size**: Window size changes based on conditions

**Applications**:
- **Maximum Sum Subarray of Size K**: O(n) with sliding window
- **Longest Substring with K Distinct Characters**
- **Anagram Search**: Find all anagrams of pattern in text
- **Minimum Window Substring**

---

## Problem-Solving Framework

### Step 1: Understand the Problem
- What are inputs and outputs?
- What are the constraints?
- Are there edge cases?
- What's the expected scale (how large is n)?

### Step 2: Identify Problem Type
- **Optimization**: Minimize/maximize something → DP, Greedy, Branch & Bound
- **Search**: Find element/path → Divide & Conquer, Backtracking
- **Counting**: How many ways? → DP, Combinatorics
- **Decision**: Yes/No answer → Backtracking, Greedy
- **Construction**: Build a solution → Greedy, Backtracking

### Step 3: Choose Strategy
- Can you break into independent subproblems? → **Divide & Conquer**
- Are there overlapping subproblems? → **Dynamic Programming**
- Can you make locally optimal choices? → **Greedy** (prove it!)
- Need to explore all possibilities? → **Backtracking**
- Need optimal solution to NP-hard problem? → **Branch & Bound**
- Large input, need approximation? → **Approximation Algorithm**

### Step 4: Analyze Complexity
- Time complexity: O(?)
- Space complexity: O(?)
- Is it acceptable for the constraints?
- Can you optimize further?

### Step 5: Implement and Test
- Start with brute force if complex
- Optimize incrementally
- Test edge cases
- Verify correctness

---

## Complexity Cheat Sheet

| Algorithm/Strategy | Typical Complexity | Space |
|-------------------|-------------------|-------|
| Binary Search | O(log n) | O(1) |
| Merge Sort | O(n log n) | O(n) |
| Quick Sort (avg) | O(n log n) | O(log n) |
| Heap Sort | O(n log n) | O(1) |
| DFS/BFS | O(V + E) | O(V) |
| Dijkstra | O((V+E) log V) | O(V) |
| Bellman-Ford | O(VE) | O(V) |
| Floyd-Warshall | O(V³) | O(V²) |
| Kruskal's MST | O(E log E) | O(V) |
| Prim's MST | O(E log V) | O(V) |
| 0/1 Knapsack (DP) | O(nW) | O(nW) |
| LCS | O(mn) | O(mn) |
| Matrix Chain | O(n³) | O(n²) |
| Backtracking | O(b^d) where b=branching, d=depth | O(d) |

---

## Final Tips

1. **Practice Pattern Recognition**: Many problems are variations of classic problems

2. **Start Simple**: Begin with brute force, then optimize

3. **Draw it Out**: Visualize recursion trees, DP tables, graph structures

4. **Test Edge Cases**: Empty input, single element, duplicates, max constraints

5. **Analyze Trade-offs**: Time vs. space, optimality vs. speed

6. **Prove Correctness**: Especially for greedy algorithms, don't assume it works

7. **Master the Basics**: Sorting, searching, basic data structures - they're foundations

8. **Think Recursively**: Many strategies (DC, DP, Backtracking) are recursive in nature

9. **Optimize Space**: Often DP space can be reduced with rolling arrays

10. **Know When to Stop**: Sometimes polynomial approximation beats exponential exact solution

---

## Summary

This guide covered the major algorithm design strategies:

- **Divide and Conquer**: Break into independent subproblems, solve recursively, combine
- **Dynamic Programming**: Store overlapping subproblem solutions, build up to answer
- **Greedy**: Make locally optimal choices, hope for global optimum (prove it!)
- **Backtracking**: Systematically explore solution space with pruning
- **Branch and Bound**: Backtracking with bounds for optimization problems
- **Other Strategies**: Transform-and-conquer, space-time tradeoffs, approximation, etc.

Understanding these paradigms gives you a powerful toolkit for tackling algorithmic problems. The key is recognizing which strategy fits the problem structure, implementing it correctly, and analyzing its complexity.

Good luck with your studies!
