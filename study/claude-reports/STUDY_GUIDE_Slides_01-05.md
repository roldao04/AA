# Comprehensive Study Guide - Algorithm Design Strategies (Slides 01-05)

## Advanced Algorithms - University of Aveiro
### Professor: Joaquim Madeira

---

## Table of Contents
1. [Slide 01: Python 3 & Algorithm Efficiency](#slide-01)
2. [Slide 02: Algorithm Design Techniques & Complexity](#slide-02)
3. [Slide 03: Dynamic Programming Introduction](#slide-03)
4. [Slide 04: Advanced Dynamic Programming & Optimization](#slide-04)
5. [Slide 05: Greedy Algorithms & Graph Problems](#slide-05)
6. [Summary of Key Concepts](#summary)
7. [Practice Problems](#practice)

---

<a name="slide-01"></a>
# SLIDE 01: Python 3 & Algorithm Efficiency

## 1.1 Python 3 Overview

### Main Features
- **Dynamic typing**: Types associated with objects, not variables
- **Simple, consistent syntax**: Uses indentation for code blocks
- **Multiplatform**: Runs on Windows, Linux, macOS
- **Highly modular**: Easy to organize code into modules
- **Extensive standard library**: "Batteries included" philosophy

### Pros
1. **Easy to learn/use**: Familiar constructs, simple rules
2. **Expressive**: Fewer lines of code compared to other languages
   ```python
   var2, var1 = var1, var2  # Easy swap without temp variable
   ```
3. **Readable**: Mandatory indentation enforces clean code
4. **Complete**: Rich standard library
5. **Cross-platform**: Write once, run anywhere

### Cons
1. **Not the fastest**: Interpreted, semicompiled to bytecode
2. **Fewer libraries than Java**: But easy to extend
3. **No compile-time type checking**: Type mismatches found at runtime

### Python Data Types

#### Numbers
```python
# Integers (unlimited precision)
1, -3, 42, 888888888888888

# Floats
3.0, 31e12, -6e-4

# Complex numbers
3+2j, -4-2j, 4.2+6.3j

# Booleans
True, False
```

#### Collections
- **Lists**: Mutable, ordered sequences `[1, 2, 3]`
- **Tuples**: Immutable sequences `(1, 2, 3)`
- **Dictionaries**: Key-value pairs `{'a': 1, 'b': 2}`
- **Sets**: Unordered collections of unique items `{1, 2, 3}`
- **Strings**: Immutable text sequences `"hello"`

---

## 1.2 Computational Efficiency

### Why Analyze Efficiency?

Running time depends on:
- Speed of the computer
- Programming language
- Quality of implementation
- Compiler optimizations

**Solution**: Count "basic operations" independent of hardware/software

### Formal Analysis (Pencil and Paper)

#### For Iterative Algorithms:
1. **Identify loops**: How many iterations?
2. **Count basic operations**: Additions, multiplications, comparisons
3. **Set up summations**: Express total operations as a sum
4. **Find closed formula**: Simplify to a mathematical expression

#### For Recursive Algorithms:
1. **Count recursive calls**
2. **Establish recurrence relations**
3. **Solve recurrences** to get closed formulas
4. **Use tools** like WolframAlpha to verify

---

## 1.3 TASK 1: Iterative Algorithms

### Exercise: Analyze these functions

```c
// Function f1
int f1(int n) {
    int i, r=0;
    for(i = 1; i <= n; i++)
        r += i;
    return r;
}

// Function f2
int f2(int n) {
    int i, j, r=0;
    for(i = 1; i <= n; i++)
        for(j = 1; j <= n; j++)
            r += 1;
    return r;
}

// Function f3
int f3(int n) {
    int i, j, r=0;
    for(i = 1; i <= n; i++)
        for(j = i; j <= n; j++)
            r += 1;
    return r;
}

// Function f4
int f4(int n) {
    int i, j, r=0;
    for(i = 1; i <= n; i++)
        for(j = 1; j <= i; j++)
            r += j;
    return r;
}
```

### Solutions:

#### f1(n) - Sum of first n integers
- **Return value**: `f1(n) = n(n+1)/2`
- **Number of iterations**: `n`
- **Operations count**: `n` additions

#### f2(n) - Nested loops (square)
- **Return value**: `f2(n) = n²`
- **Number of iterations**: `n²`
- **Operations count**: `n²` additions

#### f3(n) - Triangular nested loops
- **Return value**: `f3(n) = n(n+1)/2`
- **Number of iterations**:
  ```
  ∑(i=1 to n) (n-i+1) = n + (n-1) + ... + 1 = n(n+1)/2
  ```
- **Operations count**: `n(n+1)/2` additions

#### f4(n) - Nested loops with variable bounds
- **Return value**: `f4(n) = n(n+1)(n+2)/6`
- **Number of iterations**: `n(n+1)/2`
- **Operations count**:
  ```
  ∑(i=1 to n) ∑(j=1 to i) j = ∑(i=1 to n) i(i+1)/2 = n(n+1)(n+2)/6
  ```

**Tip**: Use WolframAlpha to verify summations!

---

## 1.4 TASK 2: Recursive Algorithms

### Exercise: Analyze these recursive functions

```c
// Function r1
unsigned int r1(unsigned int n) {
    if(n == 0) return 0;
    return 1 + r1(n - 1);
}

// Function r2
unsigned int r2(unsigned int n) {
    if(n == 0) return 0;
    if(n == 1) return 1;
    return n + r2(n - 2);
}

// Function r3
unsigned int r3(unsigned int n) {
    if(n == 0) return 0;
    return 1 + 2 * r3(n - 1);
}

// Function r4
unsigned int r4(unsigned int n) {
    if(n == 0) return 0;
    return 1 + r4(n - 1) + r4(n - 1);
}
```

### Solutions:

#### r1(n) - Linear recursion
- **Return value**: `r1(n) = n`
- **Recurrence**: `R(n) = 1 + R(n-1)`, `R(0) = 0`
- **Number of calls**: `n`
- **Closed formula**: `R(n) = n`

#### r2(n) - Decreasing by 2
- **Return value**:
  - If n is even: `r2(n) = n(n+2)/4`
  - If n is odd: `r2(n) = 1 + (n-1)(n+3)/4`
- **Number of calls**: `floor(n/2)`

#### r3(n) - Exponential growth
- **Return value**: `r3(n) = 2^n - 1`
- **Number of calls**: `n`
- **Note**: Result grows exponentially, but calls grow linearly

#### r4(n) - Binary recursion
- **Return value**: `r4(n) = 2^n - 1` (same as r3!)
- **Number of calls**: `2 × (2^n - 1) = 2^(n+1) - 2`
- **⚠️ Critical difference**: r4 makes EXPONENTIAL calls while r3 makes LINEAR calls
- **Both compute the same result, but r4 is MUCH slower**

**Important lesson**: Same result ≠ Same efficiency!

---

<a name="slide-02"></a>
# SLIDE 02: Algorithm Design Techniques & Complexity Analysis

## 2.1 Deterministic vs Non-Deterministic Algorithms

### Deterministic Algorithms
- **Definition**: Always returns the same answer for the same input
- Takes the same steps every time
- Most common type of algorithm

### Non-Deterministic Algorithms
- **Definition**: Can exhibit different behavior on different runs with same input
- Factors causing non-determinism:
  - Random number generation
  - User input
  - Timer values
  - Timing-sensitive operations (multi-threading)
  - Hardware errors
- Often used for:
  - Approximate solutions
  - When exact solutions are too costly

---

## 2.2 Problem Types

### Common Problem Categories

1. **Searching**
   - Sequential search, binary search
   - In arrays, lists, trees
   - Ordered vs. non-ordered data

2. **Sorting**
   - Selection sort, bubble sort, merge sort, quicksort
   - In-place vs. extra space
   - Stable vs. unstable

3. **String Processing**
   - Pattern matching
   - Longest common substring
   - Edit distance

4. **Graph/Network Problems**
   - Traversals (DFS, BFS)
   - Shortest paths
   - Minimum spanning tree
   - Traveling salesman

5. **Combinatorial Problems**
   - Finding permutations, combinations, subsets
   - Often the most difficult (NP-complete)
   - Knapsack, N-Queens, TSP

---

## 2.3 Algorithm Design Techniques

### 1. Brute-Force
- **Approach**: Direct, straightforward solution
- **Examples**: Selection sort, sequential search, exhaustive search
- **Pros**: Simple, works for small problems
- **Cons**: Can be very slow for large inputs

### 2. Divide-and-Conquer
- **Approach**: Break into smaller similar sub-problems, solve all, combine
- **Recurrence**: Usually splits into 2+ sub-problems
- **Examples**: Mergesort, quicksort, binary search
- **Formula**: `T(n) = aT(n/b) + f(n)` (Master Theorem)

### 3. Decrease-and-Conquer
- **Approach**: Reduce to ONE smaller sub-problem
- **Difference from D&C**: Only one recursive call
- **Examples**: Binary search, insertion sort
- **Usually more efficient** than divide-and-conquer

### 4. Transform-and-Conquer
- **Approach**: Transform problem, solve transformed version
- **Examples**: Heapsort, AVL trees, 2-3 trees

### 5. Dynamic Programming
- **Approach**: Break into overlapping sub-problems, solve bottom-up, store results
- **Key**: Reuse previously computed results
- **Examples**: Fibonacci, binomial coefficients, Knapsack

### 6. Greedy Algorithms
- **Approach**: Make locally optimal choice at each step
- **Choices are**: Feasible, locally optimal, irrevocable
- **Examples**: Coin changing, Dijkstra's algorithm, Prim's algorithm
- **⚠️ Warning**: Not always optimal!

---

## 2.4 Algorithm Efficiency Analysis

### Orders of Growth

| n | log₂ n | n | n log₂ n | n² | n³ | 2ⁿ | n! |
|---|--------|---|----------|----|----|-----|-----|
| 10 | 3.3 | 10 | 33 | 100 | 1,000 | 1,024 | 3.6×10⁶ |
| 100 | 6.6 | 100 | 660 | 10,000 | 1,000,000 | 1.3×10³⁰ | 9.3×10¹⁵⁷ |
| 1,000 | 10 | 1,000 | 10,000 | 1,000,000 | 10⁹ | ∞ | ∞ |

### Asymptotic Notations

#### Big-O (O) - Upper Bound
- `t(n) ∈ O(g(n))` if `t(n) ≤ c·g(n)` for all `n ≥ n₀`
- **Meaning**: t(n) grows no faster than g(n)

#### Big-Omega (Ω) - Lower Bound
- `t(n) ∈ Ω(g(n))` if `t(n) ≥ c·g(n)` for all `n ≥ n₀`
- **Meaning**: t(n) grows at least as fast as g(n)

#### Big-Theta (Θ) - Tight Bound
- `t(n) ∈ Θ(g(n))` if `t(n) ∈ O(g(n))` AND `t(n) ∈ Ω(g(n))`
- **Meaning**: t(n) grows exactly like g(n)

### Example:
```
T(n) = 10n² + 100n - 23

T(n) = O(n²)      ✓
T(n) = O(n³)      ✓ (looser bound)
T(n) ≠ O(n)       ✗

T(n) = Ω(n²)      ✓
T(n) = Ω(n)       ✓ (looser bound)
T(n) ≠ Ω(n³)      ✗

T(n) = Θ(n²)      ✓ (best answer)
T(n) ≠ Θ(n)       ✗
T(n) ≠ Θ(n³)      ✗
```

### Efficiency Classes

1. **O(1)** - Constant: Array access, hash table lookup
2. **O(log n)** - Logarithmic: Binary search
3. **O(n)** - Linear: Sequential search, simple loops
4. **O(n log n)** - N-log-N: Merge sort, heap sort
5. **O(n²)** - Quadratic: Bubble sort, selection sort
6. **O(n³)** - Cubic: Matrix multiplication
7. **O(2ⁿ)** - Exponential: Generating all subsets
8. **O(n!)** - Factorial: Generating all permutations

---

## 2.5 Worst, Best, and Average Cases

### Sequential Search Example

#### Best Case: B(n) = O(1)
- Element found at first position
- 1 comparison

#### Worst Case: W(n) = O(n)
- Element not in array OR at last position
- n comparisons

#### Average Case: A(n) = O(n)
- **Assumptions**:
  - Element is in array
  - Equal probability at each position
- **Formula**: `A(n) = (1 + 2 + ... + n)/n = (n+1)/2 ≈ n/2`
- Still O(n), but better constant

---

## 2.6 EXAMPLE: Computing Powers a^b

### Strategy 1: Brute-Force (Iterative)
```python
def power_brute_force(a, b):
    result = 1
    for i in range(b):
        result *= a
    return result
```
- **Multiplications**: `b`
- **Complexity**: `O(b)`

### Strategy 2: Brute-Force (Recursive)
```python
def power_recursive(a, b):
    if b == 0:
        return 1
    return a * power_recursive(a, b-1)
```
- **Recurrence**: `M(b) = 1 + M(b-1)`, `M(0) = 0`
- **Multiplications**: `b`
- **Complexity**: `O(b)`
- **No improvement** over iterative!

### Strategy 3: Divide-and-Conquer
```python
def power_divide_conquer(a, b):
    if b == 0:
        return 1
    left = power_divide_conquer(a, b // 2)
    right = power_divide_conquer(a, (b+1) // 2)
    return left * right
```
- **Recurrence**: `M(n) = M(n/2) + M((n+1)/2) + 1`
- For `n = 2^k`: `M(n) = 2M(n/2) + 1 = 2n - 1`
- **Multiplications**: `2n - 1`
- **Complexity**: `O(n)` - Still linear!

### Strategy 4: Decrease-and-Conquer ⭐ BEST
```python
def power_decrease_conquer(a, b):
    if b == 0:
        return 1
    if b == 1:
        return a

    half = power_decrease_conquer(a, b // 2)

    if b % 2 == 0:
        return half * half  # Even
    else:
        return a * half * half  # Odd
```
- **Recurrence**:
  - Even: `M(n) = M(n/2) + 1`
  - Odd: `M(n) = M((n-1)/2) + 2`
- **Best case** (all even powers): `M(n) = log₂(n)`
- **Worst case** (all odd powers): `M(n) = 2·log₂(n)`
- **Complexity**: `O(log b)` ⭐ **LOGARITHMIC!**

### Comparison Table

| b | Brute-Force | Div & Conq | Dec & Conq |
|---|-------------|------------|------------|
| 8 | 8 | 15 | 3 |
| 16 | 16 | 31 | 4 |
| 32 | 32 | 63 | 5 |
| 64 | 64 | 127 | 6 |
| 1024 | 1024 | 2047 | 10 |

**Lesson**: Decrease-and-Conquer is MUCH better!

---

## 2.7 Empirical Analysis

### Process:
1. **Run algorithm** on sample test inputs
2. **Record**: Operation counts and/or running times
3. **Analyze data**: Create tables, plots
4. **Identify** complexity class

### Example Table

| n | M(n) |
|---|------|
| 1 | 1 |
| 2 | 3 |
| 4 | 10 |
| 8 | 36 |
| 16 | 136 |
| 32 | 528 |

**Question**: What's the complexity order?

Looking at ratios: Each doubling of n multiplies M(n) by ~4
→ Suggests `O(n²)`

---

<a name="slide-03"></a>
# SLIDE 03: Dynamic Programming Introduction

## 3.1 What is Dynamic Programming?

### Key Concepts

**Dynamic Programming (DP)** is used when:
1. Problem can be broken into **overlapping sub-problems**
2. Optimal solution has **optimal substructure**
3. We can **store** intermediate results to avoid recomputation

### Top-Down vs. Bottom-Up

#### Top-Down (Recursive)
- Start from main problem
- Break into sub-problems recursively
- **Problem**: May solve same sub-problem many times
- **Complexity**: Often exponential

#### Bottom-Up (DP)
- Start from simplest/smallest sub-problems
- Build up to main problem
- **Store results** in table/array
- **Complexity**: Polynomial

---

## 3.2 EXAMPLE: Fibonacci Numbers

### Recursive Definition
```
F(0) = 0
F(1) = 1
F(n) = F(n-1) + F(n-2)  for n ≥ 2
```

### Version 1: Naive Recursion ❌
```python
def fib_recursive(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib_recursive(n-1) + fib_recursive(n-2)
```

**Problem**: Exponential time!

#### Analysis:
- **Number of additions**: `A(n) = F(n+1) - 1`
- **Growth rate**: Exponential! `F(n) ≈ φⁿ` where `φ = (1+√5)/2 ≈ 1.618` (golden ratio)
- **Complexity**: `O(φⁿ) ≈ O(1.618ⁿ)` - VERY SLOW!

| n | F(n) | A(n) | Ratio |
|---|------|------|-------|
| 10 | 55 | 54 | - |
| 15 | 610 | 609 | 1.618 |
| 20 | 6765 | 6764 | 1.618 |
| 30 | 832040 | 832039 | 1.618 |

**Why so slow?** Massive overlapping sub-problems!

```
F(5) calls:
    F(4) calls:
        F(3) calls:
            F(2), F(1)
        F(2) calls:  ← DUPLICATE!
            F(1), F(0)
    F(3) calls:  ← DUPLICATE!
        F(2), F(1)
```

### Version 2: Dynamic Programming (Array) ✓
```python
def fib_dp_array(n):
    if n == 0:
        return 0
    if n == 1:
        return 1

    f = [0] * (n + 1)
    f[0] = 0
    f[1] = 1

    for i in range(2, n + 1):
        f[i] = f[i-1] + f[i-2]

    return f[n]
```
- **Additions**: `n - 1`
- **Complexity**: `O(n)` - Linear! ⭐
- **Space**: `O(n)`

### Version 3: Optimized (3 Variables) ⭐
```python
def fib_dp_optimized(n):
    if n == 0:
        return 0
    if n == 1:
        return 1

    prev2 = 0  # F(i-2)
    prev1 = 1  # F(i-1)

    for i in range(2, n + 1):
        current = prev1 + prev2
        prev2 = prev1
        prev1 = current

    return prev1
```
- **Additions**: `n - 1`
- **Complexity**: `O(n)` - Linear!
- **Space**: `O(1)` - Constant! ⭐⭐

### Version 4: Memoization
```python
from functools import cache

@cache
def fib_memo(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib_memo(n-1) + fib_memo(n-2)
```
- **Complexity**: `O(n)` - Each F(i) computed once
- **Space**: `O(n)` - Cache storage
- **Advantage**: Keeps recursive structure, gets DP speed

---

## 3.3 EXAMPLE: Linear Robot

### Problem:
Robot can move forward by **1, 2, or 3 meters**. How many ways can it move exactly **n meters**?

### Recurrence:
```
R(0) = 1  (one way: don't move)
R(1) = 1  (only 1-meter step)
R(2) = 2  (1+1 or 2)
R(3) = 4  (1+1+1, 1+2, 2+1, or 3)

R(n) = R(n-1) + R(n-2) + R(n-3)  for n ≥ 3
```

### Solution V1: Recursive ❌
```python
def robot_recursive(n):
    if n == 0:
        return 1
    if n == 1:
        return 1
    if n == 2:
        return 2
    return robot_recursive(n-1) + robot_recursive(n-2) + robot_recursive(n-3)
```
- **Complexity**: Exponential!

### Solution V2: DP Array ✓
```python
def robot_dp_array(n):
    if n == 0:
        return 1
    if n == 1:
        return 1
    if n == 2:
        return 2

    r = [0] * (n + 1)
    r[0] = 1
    r[1] = 1
    r[2] = 2

    for i in range(3, n + 1):
        r[i] = r[i-1] + r[i-2] + r[i-3]

    return r[n]
```
- **Complexity**: `O(n)`
- **Space**: `O(n)`

### Solution V3: Optimized (4 Variables) ⭐
```python
def robot_dp_optimized(n):
    if n == 0:
        return 1
    if n == 1:
        return 1
    if n == 2:
        return 2

    prev3 = 1  # R(i-3)
    prev2 = 1  # R(i-2)
    prev1 = 2  # R(i-1)

    for i in range(3, n + 1):
        current = prev1 + prev2 + prev3
        prev3 = prev2
        prev2 = prev1
        prev1 = current

    return prev1
```
- **Complexity**: `O(n)`
- **Space**: `O(1)` ⭐

---

## 3.4 EXAMPLE: Binomial Coefficients (Pascal's Triangle)

### Definition:
The binomial coefficient C(n, k) represents:
- Number of ways to choose k items from n items
- Entry in Pascal's triangle at row n, position k

### Recurrence:
```
C(n, 0) = 1  for all n
C(n, n) = 1  for all n
C(n, k) = C(n-1, k) + C(n-1, k-1)  for 0 < k < n
```

### Pascal's Triangle:
```
         1
       1   1
      1   2   1
    1   3   3   1
   1  4   6   4   1
  1  5  10  10  5   1
```

### Solution V1: Recursive ❌
```python
def binomial_recursive(n, k):
    if k == 0 or k == n:
        return 1
    return binomial_recursive(n-1, k) + binomial_recursive(n-1, k-1)
```
- **Complexity**: Exponential!
- Many overlapping sub-problems

### Solution V2: DP 2D Array ✓
```python
def binomial_dp_2d(n, k):
    c = [[0] * (k + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        c[i][0] = 1  # C(i, 0) = 1

    for i in range(1, n + 1):
        for j in range(1, min(i, k) + 1):
            c[i][j] = c[i-1][j] + c[i-1][j-1]

    return c[n][k]
```
- **Complexity**: `O(n × k)`
- **Space**: `O(n × k)`

### Solution V3: DP 1D Array ⭐
```python
def binomial_dp_1d(n, k):
    c = [0] * (k + 1)
    c[0] = 1

    for i in range(1, n + 1):
        # Update from right to left to avoid overwriting
        for j in range(min(i, k), 0, -1):
            c[j] = c[j] + c[j-1]

    return c[k]
```
- **Complexity**: `O(n × k)`
- **Space**: `O(k)` ⭐

---

## 3.5 The Higher-Lower Game

### Game Rules:
1. Person A picks a number in [1, 100]
2. Person B guesses
3. Person A says: "Correct", "Too high", or "Too low"
4. Repeat until correct

### Strategies:

#### Naive Strategy:
- Guess 1, 2, 3, 4, ...
- **Best case**: 1 guess
- **Worst case**: 100 guesses
- **Average**: 50.5 guesses

#### Smart Strategy (Binary Search):
- Always guess the middle of remaining range
- **Best case**: 1 guess
- **Worst case**: ⌈log₂(100)⌉ = 7 guesses
- **Average**: ~6 guesses
- **Complexity**: `O(log n)` ⭐

### Implementation:
```python
def higher_lower_binary(target, low=1, high=100):
    guesses = 0
    while low <= high:
        guess = (low + high) // 2
        guesses += 1

        if guess == target:
            return guesses
        elif guess < target:
            low = guess + 1
        else:
            high = guess - 1

    return guesses
```

---

## 3.6 Memoization

### Concept:
**Memoization** = Remember previously computed results

### Implementation Pattern:
```python
# Initialize cache
cache = {}

def memoized_function(n):
    # Check if already computed
    if n in cache:
        return cache[n]

    # Base cases
    if n == 0:
        result = base_value
    else:
        # Recursive computation
        result = compute_result(n)

    # Store in cache
    cache[n] = result
    return result
```

### Python's Built-in Memoization:
```python
from functools import cache

@cache
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

### Time vs. Space Trade-off:
- **Time**: Much faster (avoid recomputation)
- **Space**: Uses memory to store results
- **When to use**: When function called repeatedly with same inputs

---

<a name="slide-04"></a>
# SLIDE 04: Advanced Dynamic Programming & Optimization Problems

## 4.1 Delannoy Numbers D(i,j)

### Problem:
Count paths on a rectangular grid from (0,0) to (i,j) where:
- You can move: **North (↑)**, **East (→)**, or **NorthEast (↗)**

### Recurrence:
```
D(0, j) = 1  for all j ≥ 0  (only move East)
D(i, 0) = 1  for all i ≥ 0  (only move North)
D(i, j) = D(i-1, j) + D(i, j-1) + D(i-1, j-1)  for i,j > 0
```

### Intuition:
To reach (i,j), you must have come from:
- (i-1, j) - came from South, moved North
- (i, j-1) - came from West, moved East
- (i-1, j-1) - came diagonally, moved NorthEast

### Central Delannoy Numbers: D(n,n)

| n | D(n,n) |
|---|--------|
| 0 | 1 |
| 1 | 3 |
| 2 | 13 |
| 3 | 63 |
| 4 | 321 |
| 5 | 1683 |

**Growth rate**: Exponential, approximately `3ⁿ`

### Solution V1: Recursive ❌
```python
def delannoy_recursive(i, j):
    if i == 0 or j == 0:
        return 1
    return (delannoy_recursive(i-1, j) +
            delannoy_recursive(i, j-1) +
            delannoy_recursive(i-1, j-1))
```
- **Complexity**: Exponential - TOO SLOW!

### Solution V2: DP 2D Array ✓
```python
def delannoy_dp_2d(m, n):
    d = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases
    for i in range(m + 1):
        d[i][0] = 1
    for j in range(n + 1):
        d[0][j] = 1

    # Fill table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            d[i][j] = d[i-1][j] + d[i][j-1] + d[i-1][j-1]

    return d[m][n]
```
- **Complexity**: `O(m × n)`
- **Space**: `O(m × n)`

### Solution V3: DP Two 1D Arrays ⭐
```python
def delannoy_dp_1d(m, n):
    prev = [1] * (n + 1)  # Previous row
    curr = [1] * (n + 1)  # Current row

    for i in range(1, m + 1):
        curr[0] = 1
        for j in range(1, n + 1):
            curr[j] = prev[j] + curr[j-1] + prev[j-1]
        prev, curr = curr, prev  # Swap

    return prev[n]
```
- **Complexity**: `O(m × n)`
- **Space**: `O(n)` ⭐

### Solution V4: Memoization
```python
from functools import cache

@cache
def delannoy_memo(i, j):
    if i == 0 or j == 0:
        return 1
    return delannoy_memo(i-1, j) + delannoy_memo(i, j-1) + delannoy_memo(i-1, j-1)
```
- **Complexity**: `O(m × n)`
- **Space**: `O(m × n)`

---

## 4.2 Bernstein Polynomials B(n,j)(t)

### Definition:
Bernstein polynomials are used in:
- Bezier curves (computer graphics)
- Numerical analysis
- Approximation theory

### Recurrence:
```
B(0,0)(t) = 1

B(n,0)(t) = (1-t) × B(n-1,0)(t)  for n ≥ 1
B(n,n)(t) = t × B(n-1,n-1)(t)    for n ≥ 1

B(n,j)(t) = (1-t) × B(n-1,j)(t) + t × B(n-1,j-1)(t)
            for 1 ≤ j ≤ n-1
```

where `t ∈ [0, 1]`

### Similar to Pascal's Triangle!
But each entry is a polynomial, not a number.

### Solution V1: Recursive ❌
```python
def bernstein_recursive(n, j, t):
    if n == 0 and j == 0:
        return 1.0
    if j == 0:
        return (1 - t) * bernstein_recursive(n-1, 0, t)
    if j == n:
        return t * bernstein_recursive(n-1, n-1, t)
    return ((1 - t) * bernstein_recursive(n-1, j, t) +
            t * bernstein_recursive(n-1, j-1, t))
```
- **Complexity**: Exponential!

### Solution V2: DP 2D Array ✓
```python
def bernstein_dp_2d(n, j, t):
    b = [[0.0] * (n + 1) for _ in range(n + 1)]

    b[0][0] = 1.0

    for i in range(1, n + 1):
        b[i][0] = (1 - t) * b[i-1][0]
        b[i][i] = t * b[i-1][i-1]

        for k in range(1, i):
            b[i][k] = (1 - t) * b[i-1][k] + t * b[i-1][k-1]

    return b[n][j]
```
- **Complexity**: `O(n²)`
- **Space**: `O(n²)`

### Solution V3: DP 1D Array ⭐
```python
def bernstein_dp_1d(n, j, t):
    b = [0.0] * (n + 1)
    b[0] = 1.0

    for i in range(1, n + 1):
        # Update from right to left
        for k in range(i, 0, -1):
            b[k] = (1 - t) * b[k] + t * b[k-1]
        b[0] = (1 - t) * b[0]

    return b[j]
```
- **Complexity**: `O(n²)`
- **Space**: `O(n)` ⭐

---

## 4.3 The Coin Row Problem

### Problem:
- Row of n coins with values `c₁, c₂, ..., cₙ`
- **Goal**: Pick up maximum total value
- **Constraint**: Cannot pick two adjacent coins

### Example:
```
Coins: [5, 1, 2, 10, 6, 2]
```

**Possible selections**:
- `[5, 2, 6]` = 13
- `[5, 10, 2]` = 17 ⭐ Optimal
- `[1, 10, 2]` = 13

### Recurrence:
```
F(0) = 0  (no coins)
F(1) = c₁  (just take first coin)

F(n) = max(cₙ + F(n-2), F(n-1))  for n > 1
```

**Intuition**: For the nth coin, either:
- **Take it**: Get `cₙ` + best from first `n-2` coins
- **Skip it**: Get best from first `n-1` coins

### Solution V1: Recursive ❌
```python
def coin_row_recursive(coins):
    def f(n):
        if n == 0:
            return 0
        if n == 1:
            return coins[0]
        return max(coins[n-1] + f(n-2), f(n-1))

    return f(len(coins))
```
- **Complexity**: Exponential!

### Solution V2: DP Array ✓
```python
def coin_row_dp(coins):
    n = len(coins)
    if n == 0:
        return 0
    if n == 1:
        return coins[0]

    f = [0] * (n + 1)
    f[0] = 0
    f[1] = coins[0]

    for i in range(2, n + 1):
        f[i] = max(coins[i-1] + f[i-2], f[i-1])

    return f[n]
```
- **Complexity**: `O(n)`
- **Space**: `O(n)`

### Solution V3: Track Solution ⭐
```python
def coin_row_dp_track(coins):
    n = len(coins)
    if n == 0:
        return 0, []
    if n == 1:
        return coins[0], [0]

    f = [0] * (n + 1)
    f[0] = 0
    f[1] = coins[0]

    choice = [False] * (n + 1)  # Did we take coin i?
    choice[1] = True

    for i in range(2, n + 1):
        if coins[i-1] + f[i-2] > f[i-1]:
            f[i] = coins[i-1] + f[i-2]
            choice[i] = True
        else:
            f[i] = f[i-1]
            choice[i] = False

    # Reconstruct solution
    selected = []
    i = n
    while i > 0:
        if choice[i]:
            selected.append(i-1)  # Coin index
            i -= 2
        else:
            i -= 1

    selected.reverse()
    return f[n], selected
```
- **Complexity**: `O(n)`
- **Space**: `O(n)`

---

## 4.4 The 0-1 Knapsack Problem

### Problem Formulation:
- **Given**: n items, each with weight `wᵢ` and value `vᵢ`
- **Given**: Knapsack capacity `W`
- **Goal**: Select subset of items with:
  - Maximum total value
  - Total weight ≤ W
  - Each item either taken (1) or not taken (0)

### Mathematical Formulation:
```
Maximize:   ∑ xᵢ × vᵢ
Subject to: ∑ xᵢ × wᵢ ≤ W
Where:      xᵢ ∈ {0, 1}
```

---

### 4.4.1 Exhaustive Search Approach

#### Algorithm:
1. Generate all 2ⁿ subsets
2. For each subset:
   - Check if total weight ≤ W
   - If feasible, compute total value
3. Return subset with maximum value

#### Example:
```
Capacity W = 10
Items:
  Item 1: w=7, v=$42
  Item 2: w=3, v=$12
  Item 3: w=4, v=$40
  Item 4: w=5, v=$25
```

**Optimal solution**: Items 3 & 4 → $65

#### Implementation:
```python
def knapsack_exhaustive(weights, values, W):
    n = len(weights)
    best_value = 0
    best_subset = []

    # Try all 2^n subsets
    for mask in range(1 << n):
        subset_weight = 0
        subset_value = 0
        subset = []

        for i in range(n):
            if mask & (1 << i):
                subset_weight += weights[i]
                subset_value += values[i]
                subset.append(i)

        # Check if feasible and better
        if subset_weight <= W and subset_value > best_value:
            best_value = subset_value
            best_subset = subset

    return best_value, best_subset
```
- **Complexity**: `O(2ⁿ)` - EXPONENTIAL!
- **Only usable for small n** (n ≤ 20)

---

### 4.4.2 Heuristic Approaches

#### Heuristic 1: Largest Value First
- Sort by value (decreasing)
- Take items while they fit
- **Not optimal!**

#### Heuristic 2: Smallest Weight First
- Sort by weight (increasing)
- Take items while they fit
- **Not optimal!**

#### Heuristic 3: Best Value-to-Weight Ratio (Greedy)
```python
def knapsack_greedy(weights, values, W):
    n = len(weights)

    # Compute ratios and sort
    items = [(values[i]/weights[i], weights[i], values[i], i)
             for i in range(n)]
    items.sort(reverse=True)  # Highest ratio first

    total_weight = 0
    total_value = 0
    selected = []

    for ratio, w, v, i in items:
        if total_weight + w <= W:
            total_weight += w
            total_value += v
            selected.append(i)

    return total_value, selected
```

**Example where it FAILS**:
```
Capacity W = 50
Items:
  Item 1: w=10, v=$60  → ratio = 6
  Item 2: w=20, v=$100 → ratio = 5
  Item 3: w=30, v=$120 → ratio = 4

Greedy chooses: Items 1 & 2 → $160
Optimal: Items 2 & 3 → $220 ⭐
```

**⚠️ Greedy is NOT optimal for 0-1 Knapsack!**

---

### 4.4.3 Dynamic Programming Solution ⭐

#### Subproblem Definition:
`V[i, j]` = Maximum value using first `i` items with capacity `j`

#### Recurrence:
```
V[0, j] = 0  for all j  (no items)
V[i, 0] = 0  for all i  (no capacity)

V[i, j] = V[i-1, j]  if wᵢ > j  (item doesn't fit)

V[i, j] = max(V[i-1, j], vᵢ + V[i-1, j-wᵢ])  if wᵢ ≤ j
          └─ don't take    └─ take item i
```

#### Implementation:
```python
def knapsack_dp(weights, values, W):
    n = len(weights)

    # Create DP table
    V = [[0] * (W + 1) for _ in range(n + 1)]

    # Fill table
    for i in range(1, n + 1):
        for j in range(W + 1):
            # Option 1: Don't take item i
            V[i][j] = V[i-1][j]

            # Option 2: Take item i (if it fits)
            if weights[i-1] <= j:
                V[i][j] = max(V[i][j],
                             values[i-1] + V[i-1][j - weights[i-1]])

    return V[n][W]
```
- **Complexity**: `O(n × W)` - **Pseudo-polynomial!**
- **Space**: `O(n × W)`

#### Complexity Discussion:
- Complexity is `O(n × W)`, which depends on the **value** of W
- This is called **pseudo-polynomial**
- True polynomial complexity would be `O(n × log W)` (depends on # of bits to represent W)
- For reasonable values of W, this is very practical!

#### Reconstructing the Solution:
```python
def knapsack_dp_solution(weights, values, W):
    n = len(weights)
    V = [[0] * (W + 1) for _ in range(n + 1)]

    # Fill table (same as before)
    for i in range(1, n + 1):
        for j in range(W + 1):
            V[i][j] = V[i-1][j]
            if weights[i-1] <= j:
                V[i][j] = max(V[i][j],
                             values[i-1] + V[i-1][j - weights[i-1]])

    # Backtrack to find items
    selected = []
    i, j = n, W
    while i > 0 and j > 0:
        # Was item i selected?
        if V[i][j] != V[i-1][j]:
            selected.append(i-1)
            j -= weights[i-1]
        i -= 1

    selected.reverse()
    return V[n][W], selected
```

#### Example Execution:
```
Capacity W = 10
Items:
  0: w=7, v=$42
  1: w=3, v=$12
  2: w=4, v=$40
  3: w=5, v=$25

DP Table V[i][j]:
    j→  0   1   2   3   4   5   6   7   8   9   10
i=0     0   0   0   0   0   0   0   0   0   0   0
i=1     0   0   0   0   0   0   0  42  42  42  42
i=2     0   0   0  12  12  12  12  42  42  42  54
i=3     0   0   0  12  40  40  40  52  52  52  82
i=4     0   0   0  12  40  40  40  52  65  65  65

Answer: V[4][10] = $65
Selected items: [2, 3] (Items 3 & 4)
```

---

<a name="slide-05"></a>
# SLIDE 05: Greedy Algorithms & Graph Problems

## 5.1 Fractional/Continuous Knapsack Problem

### Difference from 0-1 Knapsack:
- **0-1**: Each item is either taken completely or not taken
- **Fractional**: Can take any fraction of an item (0 ≤ xᵢ ≤ 1)

### Mathematical Formulation:
```
Maximize:   ∑ xᵢ × vᵢ
Subject to: ∑ xᵢ × wᵢ ≤ W
Where:      0 ≤ xᵢ ≤ 1
```

### Greedy Algorithm ⭐ (OPTIMAL for Fractional!)
```python
def fractional_knapsack(weights, values, W):
    n = len(weights)

    # Create items with value/weight ratios
    items = [(values[i]/weights[i], weights[i], values[i], i)
             for i in range(n)]
    items.sort(reverse=True)  # Sort by ratio (decreasing)

    total_value = 0.0
    remaining_capacity = W
    selected = []  # (item_index, fraction)

    for ratio, w, v, i in items:
        if remaining_capacity == 0:
            break

        if w <= remaining_capacity:
            # Take whole item
            selected.append((i, 1.0))
            total_value += v
            remaining_capacity -= w
        else:
            # Take fraction
            fraction = remaining_capacity / w
            selected.append((i, fraction))
            total_value += v * fraction
            remaining_capacity = 0

    return total_value, selected
```

#### Example:
```
Capacity W = 50
Items:
  Item 1: w=10, v=$60  → ratio = 6
  Item 2: w=20, v=$100 → ratio = 5
  Item 3: w=30, v=$120 → ratio = 4

Greedy solution:
1. Take all of Item 1: 10 kg, $60
2. Take all of Item 2: 20 kg, $100
3. Take 2/3 of Item 3: 20 kg, $80
Total: $240 ⭐ OPTIMAL!
```

- **Complexity**: `O(n log n)` (for sorting)
- **✓ Always optimal** for fractional knapsack!
- **✗ NOT optimal** for 0-1 knapsack!

---

## 5.2 Greedy Algorithms

### Key Characteristics:
1. **Feasible**: Satisfies problem constraints
2. **Locally Optimal**: Best choice at current step
3. **Irrevocable**: Cannot undo choices

### When do Greedy Algorithms Work?
- **Greedy Choice Property**: Locally optimal choices lead to globally optimal solution
- **Optimal Substructure**: Optimal solution contains optimal solutions to sub-problems

### ⚠️ Warning:
Greedy algorithms don't always work! Must prove correctness for each problem.

---

## 5.3 The Coin-Changing Problem

### Problem:
Make change for amount `A` using:
- Available denominations: `d₁ > d₂ > ... > dₙ = 1`
- **Goal**: Use fewest number of coins
- Assume unlimited coins of each denomination

### Mathematical Formulation:
```
Minimize:   ∑ xᵢ
Subject to: ∑ xᵢ × dᵢ = A
Where:      xᵢ ∈ {0, 1, 2, ...}
```

### Greedy Algorithm:
```python
def coin_change_greedy(denominations, amount):
    coins_used = []
    remaining = amount

    for denom in denominations:  # Assume sorted descending
        if remaining == 0:
            break

        count = remaining // denom
        if count > 0:
            coins_used.append((denom, count))
            remaining -= count * denom

    return coins_used
```

#### Example 1 (Works):
```
Amount A = 48
Denominations: [25, 10, 5, 1]  (US coins)

Greedy solution:
- 1 × 25¢ = 25¢
- 2 × 10¢ = 20¢
- 0 × 5¢ = 0¢
- 3 × 1¢ = 3¢
Total: 6 coins ⭐ OPTIMAL
```

#### Example 2 (FAILS!):
```
Amount A = 10
Denominations: [7, 5, 1]

Greedy solution:
- 1 × 7 = 7
- 0 × 5 = 0
- 3 × 1 = 3
Total: 4 coins ✗

Optimal solution:
- 2 × 5 = 10
Total: 2 coins ⭐
```

**⚠️ Greedy NOT always optimal!** Depends on denominations.

### When is Greedy Optimal?
- For "canonical" coin systems (like US/Euro coins)
- Dynamic programming gives optimal solution for ANY denominations

---

## 5.4 The Activity Selection Problem

### Problem:
- Set of activities with start time `sᵢ` and finish time `fᵢ`
- **Goal**: Select maximum number of non-overlapping activities

### Example:
```
Activity  Start  Finish
   A        1      3
   B        2      5
   C        4      7
   D        6      9
   E        8     10
```

### Greedy Strategies (Which Works?)

#### Strategy 1: Earliest Start Time ✗
- Choose activities that start earliest
- **Counter-example**:
  ```
  A: [1, 10]
  B: [2, 3]
  C: [4, 5]

  Greedy picks: A (1 activity)
  Optimal: B, C (2 activities)
  ```

#### Strategy 2: Shortest Duration ✗
- Choose activities with shortest duration
- **Counter-example**:
  ```
  A: [1, 2]
  B: [1, 10]
  C: [9, 10]

  Greedy picks: A (then nothing fits)
  Optimal: B (or A+C for 2 activities)
  ```

#### Strategy 3: Fewest Conflicts ✗
- Choose activity conflicting with fewest others
- **Counter-example**: Complex, but can be constructed

#### Strategy 4: Earliest Finish Time ✓ ⭐
- **Always choose** activity that finishes earliest
- **This works!** Optimal for activity selection

### Greedy Algorithm (Earliest Finish):
```python
def activity_selection(start_times, finish_times):
    n = len(start_times)

    # Create activities and sort by finish time
    activities = list(zip(start_times, finish_times, range(n)))
    activities.sort(key=lambda x: x[1])  # Sort by finish time

    selected = []
    last_finish = 0

    for s, f, i in activities:
        if s >= last_finish:  # No overlap
            selected.append(i)
            last_finish = f

    return selected
```

- **Complexity**: `O(n log n)` (sorting) + `O(n)` (selection) = `O(n log n)`
- **✓ Always optimal!**

#### Why Does This Work?
**Proof idea**:
- Let A be greedy solution, O be optimal solution
- If they differ, we can swap first activity in O with first activity in A
- This doesn't decrease number of activities
- By induction, greedy is optimal

---

## 5.5 Graph Algorithms

### 5.5.1 Minimum Spanning Tree (MST)

**Problem**: Given weighted connected graph, find tree connecting all vertices with minimum total edge weight.

#### Algorithm 1: Kruskal's Algorithm ⭐
**Idea**: Start with forest of single vertices, add cheapest edge that doesn't create cycle

```python
def kruskal_mst(graph):
    # graph = list of (weight, u, v) edges
    edges = sorted(graph)  # Sort by weight

    parent = {}  # For Union-Find
    def find(v):
        if v not in parent:
            parent[v] = v
        if parent[v] != v:
            parent[v] = find(parent[v])
        return parent[v]

    def union(u, v):
        parent[find(u)] = find(v)

    mst = []
    total_weight = 0

    for weight, u, v in edges:
        if find(u) != find(v):  # No cycle
            mst.append((u, v, weight))
            total_weight += weight
            union(u, v)

    return mst, total_weight
```

- **Complexity**: `O(E log E)` where E = number of edges
- **✓ Always optimal!**

#### Algorithm 2: Prim's Algorithm ⭐
**Idea**: Start with one vertex, always add cheapest edge to a new vertex

```python
import heapq

def prim_mst(graph, start):
    # graph = adjacency list {v: [(neighbor, weight), ...]}
    mst = []
    visited = set([start])
    edges = [(weight, start, neighbor)
             for neighbor, weight in graph[start]]
    heapq.heapify(edges)

    while edges:
        weight, u, v = heapq.heappop(edges)
        if v not in visited:
            visited.add(v)
            mst.append((u, v, weight))

            for neighbor, w in graph[v]:
                if neighbor not in visited:
                    heapq.heappush(edges, (w, v, neighbor))

    return mst
```

- **Complexity**: `O(E log V)` with binary heap
- **✓ Always optimal!**

#### When to Use Which?
- **Kruskal's**: Better for sparse graphs (few edges)
- **Prim's**: Better for dense graphs (many edges)

---

### 5.5.2 Single-Source Shortest Paths (SSSP)

**Problem**: Given weighted graph and source vertex s, find shortest paths from s to all other vertices.

#### Dijkstra's Algorithm ⭐
**Requirements**: All edge weights must be **non-negative**

**Idea**: Maintain set of vertices with known shortest distances, always extend to closest unvisited vertex

```python
import heapq

def dijkstra(graph, source):
    # graph = adjacency list {v: [(neighbor, weight), ...]}
    distances = {source: 0}
    previous = {}
    pq = [(0, source)]  # (distance, vertex)
    visited = set()

    while pq:
        dist, u = heapq.heappop(pq)

        if u in visited:
            continue
        visited.add(u)

        for v, weight in graph[u]:
            new_dist = dist + weight
            if v not in distances or new_dist < distances[v]:
                distances[v] = new_dist
                previous[v] = u
                heapq.heappush(pq, (new_dist, v))

    return distances, previous
```

- **Complexity**: `O((V + E) log V)` with binary heap
- **✓ Always optimal** (for non-negative weights!)

#### Reconstructing Path:
```python
def reconstruct_path(previous, source, target):
    path = []
    current = target
    while current != source:
        path.append(current)
        if current not in previous:
            return None  # No path exists
        current = previous[current]
    path.append(source)
    path.reverse()
    return path
```

---

## 5.6 The Traveling Salesman Problem (TSP)

### Problem:
- Given n cities and distances between them
- **Goal**: Find shortest tour visiting each city exactly once and returning to start

### Formulation:
- Find shortest Hamiltonian cycle in complete weighted graph
- **NP-Complete** problem!

### Exhaustive Search:
```python
from itertools import permutations

def tsp_exhaustive(distances):
    n = len(distances)
    cities = list(range(n))

    # Fix starting city (say 0)
    other_cities = cities[1:]

    min_cost = float('inf')
    best_tour = None

    # Try all (n-1)! permutations
    for perm in permutations(other_cities):
        tour = [0] + list(perm) + [0]

        # Calculate tour cost
        cost = 0
        for i in range(len(tour) - 1):
            cost += distances[tour[i]][tour[i+1]]

        if cost < min_cost:
            min_cost = cost
            best_tour = tour

    return min_cost, best_tour
```

- **Complexity**: `O(n!)` - EXTREMELY SLOW!
- Only practical for n ≤ 12

---

### 5.6.1 TSP Approximation Algorithms

#### Heuristic 1: Nearest Neighbor ⭐
**Idea**: Always go to nearest unvisited city

```python
def tsp_nearest_neighbor(distances, start=0):
    n = len(distances)
    unvisited = set(range(n))
    tour = [start]
    unvisited.remove(start)

    current = start
    total_cost = 0

    while unvisited:
        # Find nearest unvisited city
        nearest = min(unvisited, key=lambda city: distances[current][city])
        tour.append(nearest)
        total_cost += distances[current][nearest]
        unvisited.remove(nearest)
        current = nearest

    # Return to start
    tour.append(start)
    total_cost += distances[current][start]

    return total_cost, tour
```

- **Complexity**: `O(n²)`
- **Fast** but solution quality varies
- **Performance ratio**: Can be arbitrarily bad! (RA = ∞)

#### Heuristic 2: Shortest Edge
**Idea**: Add shortest edges that don't create a cycle (until have Hamiltonian cycle)

```python
def tsp_shortest_edge(distances):
    n = len(distances)

    # Create list of all edges
    edges = []
    for i in range(n):
        for j in range(i+1, n):
            edges.append((distances[i][j], i, j))

    edges.sort()  # Sort by distance

    # Track degree of each vertex
    degree = [0] * n
    tour_edges = []

    for dist, u, v in edges:
        # Can add edge if:
        # 1. Both vertices have degree < 2
        # 2. Doesn't create premature cycle
        if degree[u] < 2 and degree[v] < 2:
            if not creates_cycle(tour_edges, u, v, n):
                tour_edges.append((u, v, dist))
                degree[u] += 1
                degree[v] += 1

                if len(tour_edges) == n:
                    break

    # Reconstruct tour from edges
    return reconstruct_tour(tour_edges)
```

#### Performance Ratio:
**Definition**: For minimization problem:
```
RA = max over all instances (Approx_Solution / Optimal_Solution)
```

- **Nearest Neighbor**: RA = ∞ (can be arbitrarily bad)
- **Better heuristics exist** (2-approximation algorithms for metric TSP)

---

<a name="summary"></a>
# Summary of Key Concepts

## Algorithm Design Paradigms

| Strategy | Key Idea | When to Use | Examples |
|----------|----------|-------------|----------|
| **Brute-Force** | Try all possibilities | Small inputs, simple problems | Exhaustive search, selection sort |
| **Divide & Conquer** | Split into multiple sub-problems | Recursive structure, independent sub-problems | Merge sort, quicksort |
| **Decrease & Conquer** | Reduce to ONE smaller problem | Binary search-like problems | Binary search, computing powers |
| **Transform & Conquer** | Transform then solve | Can convert to easier problem | Heapsort, balanced trees |
| **Dynamic Programming** | Solve overlapping sub-problems bottom-up | Optimization, overlapping sub-problems | Fibonacci, Knapsack, coin row |
| **Greedy** | Make locally optimal choices | Greedy choice property holds | MST, SSSP, activity selection |

## Complexity Classes (Best to Worst)

1. **O(1)** - Constant
2. **O(log n)** - Logarithmic (decrease-and-conquer)
3. **O(n)** - Linear
4. **O(n log n)** - Linearithmic (good sorting algorithms)
5. **O(n²)** - Quadratic (nested loops)
6. **O(n³)** - Cubic
7. **O(2ⁿ)** - Exponential (very slow!)
8. **O(n!)** - Factorial (extremely slow!)

## When Greedy Works

| Problem | Greedy Works? | Why? |
|---------|---------------|------|
| Fractional Knapsack | ✓ YES | Can split items |
| 0-1 Knapsack | ✗ NO | Must take whole items |
| Coin Changing | ⚠️ DEPENDS | Only for canonical systems |
| Activity Selection | ✓ YES | Earliest finish time |
| MST | ✓ YES | Both Kruskal's and Prim's |
| SSSP | ✓ YES | Dijkstra's (non-negative weights) |
| TSP | ✗ NO | NP-complete |

## Dynamic Programming Checklist

To apply DP, check:
1. ✓ Can break into sub-problems?
2. ✓ Sub-problems overlap?
3. ✓ Optimal substructure?
4. ✓ Can define recurrence?
5. ✓ Know base cases?

Then:
- Define state/subproblem
- Write recurrence relation
- Identify base cases
- Choose storage (2D array, 1D array, few variables)
- Implement bottom-up
- Optionally: Reconstruct solution

---

<a name="practice"></a>
# Practice Problems

## Easy Problems

### 1. Array Sum
Write iterative and recursive functions to sum array elements. Analyze complexity.

### 2. Factorial
Implement factorial three ways: iterative, recursive, tail-recursive. Compare.

### 3. Maximum Element
Find maximum element in array using divide-and-conquer. Analyze complexity.

## Medium Problems

### 4. Fibonacci Variants
Implement Fibonacci using:
- Naive recursion
- DP with array
- DP with 3 variables
- Memoization
Compare performance for n=30.

### 5. Longest Increasing Subsequence
Given array, find length of longest increasing subsequence.
Example: [10, 9, 2, 5, 3, 7, 101, 18] → 4 (subsequence: [2, 3, 7, 101])

### 6. Coin Change (Minimum Coins)
Given coin denominations and amount, find minimum number of coins.
Use DP to solve optimally.

### 7. Edit Distance
Given two strings, find minimum number of operations (insert, delete, replace) to convert one to other.

## Hard Problems

### 8. Matrix Chain Multiplication
Given dimensions of matrices, find optimal way to multiply them (minimize total multiplications).

### 9. Subset Sum
Given set of integers and target sum, determine if any subset sums to target.

### 10. Partition Problem
Given set of integers, can you partition into two subsets with equal sum?

## Challenge Problems

### 11. TSP Small Instance
Implement exhaustive search for TSP with 8 cities. Generate random distances.

### 12. Knapsack Comparison
Implement all three approaches for 0-1 Knapsack:
- Exhaustive search
- Greedy (ratio-based)
- Dynamic programming
Compare results on various test cases.

### 13. Activity Selection Variants
Implement activity selection with weights (maximize total weight of selected activities).

---

## Tips for Exam Preparation

### 1. Complexity Analysis
- **Practice** finding closed formulas for summations
- **Use** WolframAlpha to verify
- **Remember** common summations:
  - ∑(i=1 to n) i = n(n+1)/2
  - ∑(i=1 to n) i² = n(n+1)(2n+1)/6
  - ∑(i=1 to n) i³ = [n(n+1)/2]²

### 2. Recurrence Relations
- **Master Theorem** for divide-and-conquer:
  ```
  T(n) = aT(n/b) + f(n)

  Case 1: If f(n) = O(n^(log_b(a) - ε)), then T(n) = Θ(n^log_b(a))
  Case 2: If f(n) = Θ(n^log_b(a)), then T(n) = Θ(n^log_b(a) × log n)
  Case 3: If f(n) = Ω(n^(log_b(a) + ε)), then T(n) = Θ(f(n))
  ```

### 3. DP Problem Solving Steps
1. Define subproblem
2. Write recurrence
3. Identify base cases
4. Determine computation order
5. Implement bottom-up
6. Optimize space if possible

### 4. Greedy Algorithm Questions
- **Always ask**: "Does greedy work for this problem?"
- **Prove** or **find counter-example**
- **Remember**: Greedy ≠ Optimal (usually)

### 5. Common Mistakes
- **Confusing** 0-1 vs. fractional knapsack
- **Forgetting** base cases in DP
- **Wrong** complexity analysis (confusing polynomial vs. exponential)
- **Using** greedy when DP is needed

---

## Additional Resources

### Books Referenced:
1. **Levitin** - Introduction to the Design and Analysis of Algorithms, 3rd Ed.
2. **Cormen et al.** - Introduction to Algorithms, 3rd Ed.
3. **Johnsonbaugh & Schaefer** - Algorithms

### Online Tools:
- **WolframAlpha**: For verifying mathematical formulas
- **Python timeit**: For performance measurement
- **Python cProfile**: For code profiling

### Python Profiling Example:
```python
import cProfile
import pstats

# Profile a function
cProfile.run('fibonacci(30)', 'profile_stats')

# Analyze results
stats = pstats.Stats('profile_stats')
stats.sort_stats('cumulative')
stats.print_stats(10)
```

---

## Good Luck with Your Studies! 🎓

Remember:
- **Practice** is key
- **Understand** don't memorize
- **Test** your implementations
- **Analyze** complexity carefully
- **Compare** different approaches

**Most Important**: Focus on **WHY** each technique works, not just HOW to implement it!

---

**End of Study Guide**

*Generated for Advanced Algorithms course*
*University of Aveiro*
*Slides 01-05*
