# Randomized Algorithms - Comprehensive Study Guide

## Table of Contents
1. [Introduction to Randomized Algorithms](#introduction)
2. [Fundamental Concepts](#fundamental-concepts)
3. [Classic Randomized Algorithms](#classic-algorithms)
4. [Randomized Data Structures](#randomized-data-structures)
5. [Analysis Techniques](#analysis-techniques)
6. [Applications and Examples](#applications)
7. [Problem-Solving Framework](#problem-solving)
8. [Complexity Cheat Sheet](#complexity-cheat-sheet)

---

## Introduction to Randomized Algorithms {#introduction}

### What are Randomized Algorithms?

A **randomized algorithm** is an algorithm that uses random numbers to influence its execution path or decisions. Unlike deterministic algorithms that always produce the same output for a given input, randomized algorithms may produce different outputs or take different execution paths across multiple runs with the same input.

### Why Use Randomness?

Randomization in algorithms offers several key advantages:

1. **Simplicity**: Often simpler to design and implement than deterministic counterparts
2. **Efficiency**: Can achieve better average-case performance
3. **Avoiding Worst Cases**: Randomization can make worst-case inputs unlikely
4. **Breaking Symmetry**: Useful in distributed systems and networking
5. **Approximation**: Sometimes the only practical approach for hard problems

### Two Classes of Randomized Algorithms

#### Las Vegas Algorithms

**Definition**: Always produce the **correct answer**, but the **running time is random**.

**Characteristics**:
- Correctness is guaranteed
- Running time varies between executions
- We analyze **expected running time**
- Can be stopped at any time with correct result (if finished)

**Examples**:
- Randomized QuickSort
- Randomized QuickSelect
- Randomized incremental algorithms

**Example**: Randomized QuickSort always sorts correctly, but may take different amounts of time depending on pivot choices.

#### Monte Carlo Algorithms

**Definition**: Have **fixed running time**, but the answer may be **incorrect with some probability**.

**Characteristics**:
- Running time is deterministic or bounded
- May produce wrong answer with some probability
- Often can reduce error probability by repeated runs
- Trade accuracy for speed

**Examples**:
- Randomized primality testing (Miller-Rabin)
- Approximate counting algorithms
- Pattern matching with fingerprinting
- Bloom filters (membership testing)

**Example**: Miller-Rabin primality test runs in fixed time but has a small probability of incorrectly identifying a composite number as prime.

### Key Differences

| Aspect | Las Vegas | Monte Carlo |
|--------|-----------|-------------|
| **Correctness** | Always correct | May be incorrect |
| **Running Time** | Random | Fixed/Bounded |
| **Analysis Focus** | Expected time | Error probability |
| **When to Use** | Correctness critical | Speed critical, some error acceptable |
| **Improvement** | Hard to guarantee time | Run multiple times to reduce error |

### Expected vs Worst-Case Complexity

**Worst-Case Complexity**: Maximum resources (time/space) over all possible inputs and random choices
- Guarantees performance bound
- Can be pessimistic for randomized algorithms

**Expected Complexity**: Average resources over all random choices for a given input
- More realistic measure for randomized algorithms
- Analysis uses probability theory

**Example**: Randomized QuickSort
- Worst-case: O(n²) (very unlikely with random pivots)
- Expected: O(n log n) (over all random choices)

---

## Fundamental Concepts {#fundamental-concepts}

### Probability Basics for Algorithm Analysis

#### Sample Space and Events

- **Sample Space (Ω)**: Set of all possible outcomes
- **Event**: Subset of the sample space
- **Probability P(E)**: Measure of likelihood, 0 ≤ P(E) ≤ 1

#### Key Probability Rules

1. **Complement**: P(Ā) = 1 - P(A)
2. **Union**: P(A ∪ B) = P(A) + P(B) - P(A ∩ B)
3. **Independence**: P(A ∩ B) = P(A) × P(B) if A and B are independent
4. **Conditional**: P(A|B) = P(A ∩ B) / P(B)

#### Random Variables

A **random variable** X is a function from the sample space to real numbers.

**Expected Value (Expectation)**:
```
E[X] = Σ x · P(X = x)
```

The expected value represents the average outcome over many trials.

**Key Properties**:
1. **Linearity of Expectation**: E[X + Y] = E[X] + E[Y] (even if X and Y are dependent!)
2. **Scaling**: E[cX] = c · E[X]
3. **Independence**: E[XY] = E[X] · E[Y] if X and Y are independent

#### Indicator Random Variables

An **indicator random variable** I_A for event A:
```
I_A = 1 if event A occurs
I_A = 0 if event A does not occur
```

**Key Property**: E[I_A] = P(A)

This is extremely useful for analysis! Convert counting problems to sums of indicators.

### Analyzing Randomized Algorithms

#### Expected Running Time

For a randomized algorithm, we analyze the **expected number of operations** over all possible random choices.

**General approach**:
1. Identify random choices made by the algorithm
2. Express running time as a function of these choices
3. Compute expected value

**Example**: Expected number of coin flips to get heads
```
E[# flips] = 1/2 · 1 + 1/4 · 2 + 1/8 · 3 + ... = 2
```

#### Worst-Case Expected Time

The **expected running time** is still the worst over all inputs:
```
E[T(n)] = max over inputs of size n { E[running time on that input] }
```

This is different from worst-case deterministic time!

### Randomness in Algorithm Design

**Where randomness is used**:
1. **Random pivot selection**: QuickSort, QuickSelect
2. **Random sampling**: Skip lists, sampling algorithms
3. **Random hash functions**: Hash tables, Bloom filters
4. **Random ordering**: Randomized incremental algorithms
5. **Random bits**: Fingerprinting, load balancing

---

## Classic Randomized Algorithms {#classic-algorithms}

### 1. Randomized QuickSort

#### The Algorithm

**Key Idea**: Choose pivot randomly instead of deterministically (e.g., always first element)

```
RandomizedQuickSort(A, left, right):
    if left < right:
        pivot_index = RandomPartition(A, left, right)
        RandomizedQuickSort(A, left, pivot_index - 1)
        RandomizedQuickSort(A, pivot_index + 1, right)

RandomPartition(A, left, right):
    i = Random(left, right)  // Random index in [left, right]
    swap A[i] with A[right]  // Move random element to end
    return Partition(A, left, right)  // Standard partition
```

#### Why Randomize?

**Deterministic QuickSort problems**:
- Worst-case O(n²) on already sorted arrays (if always picking first/last as pivot)
- An adversary could construct worst-case inputs
- Performance depends on input ordering

**Randomized QuickSort advantages**:
- Worst-case O(n²) still exists but is **extremely unlikely**
- Expected O(n log n) on **any input**
- No input distribution assumptions needed
- Adversary cannot predict which pivots will be chosen

#### Analysis

**Key insight**: Use indicator random variables for comparisons.

Let X = total number of comparisons
Let z₁, z₂, ..., zₙ be elements in sorted order

Define indicator: X_{ij} = 1 if zᵢ is compared with z_j, 0 otherwise

Total comparisons:
```
X = Σ_{i=1}^{n-1} Σ_{j=i+1}^{n} X_{ij}
```

By linearity of expectation:
```
E[X] = Σ_{i=1}^{n-1} Σ_{j=i+1}^{n} E[X_{ij}]
     = Σ_{i=1}^{n-1} Σ_{j=i+1}^{n} P(zᵢ compared with z_j)
```

**When are zᵢ and z_j compared?**
- They're compared if one is chosen as pivot before any element between them
- The first pivot chosen from {zᵢ, z_{i+1}, ..., z_j} determines if they're compared
- If zᵢ or z_j chosen first: they're compared (probability 2/(j-i+1))
- Otherwise: they're separated and never compared

Therefore:
```
P(zᵢ compared with z_j) = 2 / (j - i + 1)
```

Computing the expectation:
```
E[X] = Σ_{i=1}^{n-1} Σ_{j=i+1}^{n} 2/(j-i+1)
     = Σ_{i=1}^{n-1} Σ_{k=1}^{n-i} 2/k  (substituting k = j-i)
     ≤ Σ_{i=1}^{n-1} 2 Σ_{k=1}^{n} 1/k
     ≤ 2n · H_n
     = O(n log n)
```

Where H_n is the nth harmonic number ≈ ln(n).

**Complexity**:
- **Expected time**: O(n log n)
- **Worst-case time**: O(n²) (extremely unlikely)
- **Space**: O(log n) expected recursion depth
- **In-place**: Yes (with small extra space)

**Key Takeaway**: Random pivot selection achieves expected O(n log n) on **any input**, eliminating the dependency on input distribution.

### 2. Randomized QuickSelect

#### The Problem

Find the kth smallest element in an unsorted array (also called the **selection problem**).

**Applications**:
- Finding median (k = n/2)
- Finding percentiles
- Top-k problems

#### The Algorithm

Similar to QuickSort but only recurse on one side:

```
RandomizedQuickSelect(A, left, right, k):
    if left == right:
        return A[left]

    pivot_index = RandomPartition(A, left, right)
    pivot_rank = pivot_index - left + 1

    if k == pivot_rank:
        return A[pivot_index]
    else if k < pivot_rank:
        return RandomizedQuickSelect(A, left, pivot_index - 1, k)
    else:
        return RandomizedQuickSelect(A, pivot_index + 1, right, k - pivot_rank)
```

#### Analysis

**Intuition**: Each good pivot reduces problem size significantly.

A pivot is "good" if it falls in the middle 50% of elements. The probability of choosing a good pivot is 1/2.

**Expected recursion depth**: O(log n)
- With probability 1/2, we get a good pivot
- Good pivot reduces problem to at most 3n/4 size
- Expected number of trials to get good pivot: 2
- Depth: log₄/₃(n) = O(log n)

**More detailed analysis** using recurrence:

```
E[T(n)] ≤ E[T(partition size)] + O(n)
```

Best pivot: splits 50-50, giving T(n/2)
Worst pivot: splits 0-100, giving T(n-1)

Average over all possible pivots:
```
E[T(n)] ≤ (1/n) Σ_{i=1}^{n} T(i) + O(n)
```

This resolves to:
```
E[T(n)] = O(n)
```

**Complexity**:
- **Expected time**: O(n) - linear!
- **Worst-case time**: O(n²) (extremely unlikely)
- **Space**: O(log n) expected

**Key Insight**: Unlike sorting (which requires O(n log n)), selection can be done in expected linear time with randomization!

**Note**: There exists a deterministic O(n) algorithm (median-of-medians), but it's more complex and has larger constants.

### 3. Randomized Min-Cut (Karger's Algorithm)

#### The Problem

Given an undirected graph G = (V, E), find a **minimum cut**: the smallest set of edges whose removal disconnects the graph.

**Applications**:
- Network reliability
- Image segmentation
- Clustering

#### The Algorithm: Random Contraction

**Key Idea**: Repeatedly contract random edges until only 2 vertices remain. The remaining edges form a cut.

```
KargerMinCut(G):
    while |V| > 2:
        pick edge (u,v) uniformly at random from E
        contract edge (u,v):
            - merge u and v into single vertex
            - remove self-loops
            - keep parallel edges
    return remaining edges as the cut
```

**Edge Contraction**: Merge two vertices into one, combining all incident edges.

#### Analysis

**Key Question**: What's the probability this finds the min-cut?

Let C be a min-cut of size k (k edges).

**Probability analysis**:

**First contraction**:
- For algorithm to succeed, we must NOT pick an edge from C
- How many edges are there? At least kn/2 (each vertex has degree ≥ k)
- P(don't pick edge from C) ≥ 1 - k/(kn/2) = 1 - 2/n

**Second contraction** (given first succeeded):
- Now (n-1) vertices
- P(success) ≥ 1 - 2/(n-1)

**Continuing**:
```
P(algorithm finds min-cut) ≥ (1 - 2/n)(1 - 2/(n-1))...(1 - 2/3)
                            = (n-2)/n · (n-3)/(n-1) · ... · 1/3
                            = 2/(n(n-1))
                            = Ω(1/n²)
```

**Improving success probability**:
- Run algorithm n² times independently
- Return minimum cut found

P(all runs fail) ≤ (1 - 1/n²)^(n²) ≈ 1/e ≈ 0.37

Running O(n² ln n) times gives success probability ≥ 1 - 1/n.

**Complexity**:
- **Single run**: O(n²) time
- **For high success probability**: O(n⁴ log n) time
- **Better implementations** (Karger-Stein): O(n² log³ n)

**Key Insight**: Simple randomized algorithm for a problem where no efficient deterministic algorithm was known!

### 4. Randomized Incremental Construction

#### General Paradigm

**Approach**:
1. Add objects (points, lines, etc.) in random order
2. Maintain solution incrementally
3. Analyze expected complexity over random orderings

**Examples**:
- Convex hull construction
- Delaunay triangulation
- Trapezoidal decomposition

#### Example: Convex Hull

**Standard approach**: Graham scan in O(n log n)

**Randomized incremental**:
1. Shuffle points randomly
2. Add points one by one, updating convex hull
3. Expected O(n log n) with good practical performance

**Key advantage**: Simpler to implement, better constants in practice.

---

## Randomized Data Structures {#randomized-data-structures}

### 1. Skip Lists

#### The Problem

Maintain a sorted set supporting:
- Search: O(log n)
- Insert: O(log n)
- Delete: O(log n)

**Classic solutions**: Balanced trees (AVL, Red-Black) - complex to implement

#### Skip List Structure

A **skip list** is a probabilistic alternative to balanced trees.

**Structure**:
- Multiple levels of linked lists
- Level 0: all elements in sorted order
- Level i: approximately half the elements of level i-1
- Each element has random height (number of levels it appears in)

```
Level 3:  1 -------------------------> 13
Level 2:  1 --------> 7 ------------> 13 --------> 17
Level 1:  1 --> 3 --> 7 --> 9 -----> 13 --> 15 --> 17 --> 19
Level 0:  1 --> 3 --> 7 --> 9 --> 11 --> 13 --> 15 --> 17 --> 19
```

#### Element Height

Each element's height is determined randomly:
- Height 1 with probability 1/2
- Height 2 with probability 1/4
- Height k with probability 1/2^k

**Method**: Flip coin; heads = increase height, tails = stop.

```
RandomHeight():
    height = 1
    while Random() < 0.5:  // Coin flip
        height++
    return min(height, MaxLevel)
```

Expected height of an element: 2

#### Operations

**Search for x**:
```
Search(x):
    current = head
    for level from MaxLevel down to 0:
        while current.next[level].key < x:
            current = current.next[level]
    current = current.next[0]
    return current if current.key == x
```

**Strategy**:
- Start at top level (sparsest)
- Move right as far as possible without exceeding x
- Drop down one level
- Repeat until level 0

**Insert(x)**:
1. Search for x to find insertion point
2. Generate random height h
3. Insert x at levels 0 through h-1
4. Update pointers at each level

**Delete(x)**:
1. Search for x
2. Remove from all levels it appears in
3. Update pointers

#### Analysis

**Expected number of levels**: O(log n)
- Level i has approximately n/2^i elements
- Top level when n/2^k ≈ 1, so k ≈ log n

**Search time analysis**:
- At each level, expected number of steps: 2 (geometric distribution)
- Number of levels: O(log n)
- Expected search time: O(log n)

**Detailed analysis**:
Working backwards from target:
- At level 0, we're at the target
- At level i, we're within 2 steps of target in expectation
- Climbing from level 0 to level O(log n): O(log n) steps

**Complexity**:
- **Search**: O(log n) expected
- **Insert**: O(log n) expected
- **Delete**: O(log n) expected
- **Space**: O(n) expected

**Advantages over balanced trees**:
- Simpler to implement
- No complex rotations
- Good cache performance (forward pointers)
- Easy to make concurrent

**Disadvantages**:
- Probabilistic guarantees (not worst-case)
- Extra space for pointers
- Not cache-optimal (vertical traversal)

### 2. Hash Tables with Random Hash Functions

#### The Problem

Store a set of elements supporting:
- Insert: O(1)
- Delete: O(1)
- Search: O(1)

**Challenge**: Hash collisions

#### Universal Hashing

A family H of hash functions is **universal** if:
```
For any two keys x ≠ y: P(h(x) = h(y)) ≤ 1/m
```
where h is chosen uniformly at random from H, and m is the table size.

**Benefit**: No fixed hash function means adversary cannot construct bad inputs.

#### Example: Polynomial Hash Family

```
h(x) = ((ax + b) mod p) mod m
```
where:
- p is a large prime
- a, b are random values in [0, p-1]
- m is the table size

This family is universal!

#### Analysis with Universal Hashing

For any set S of n keys and query key x:
```
E[# collisions with x] ≤ n/m = α (load factor)
```

**Consequence**: Expected search time is O(1 + α).

With α = O(1) (table size proportional to number of elements), operations are O(1) expected.

#### Perfect Hashing

For **static** sets (no insertions/deletions), can achieve O(1) **worst-case** lookup:

**Two-level scheme**:
1. First hash table of size n with universal hash function
2. For each bucket with k elements, second hash table of size k²
3. Choose hash functions to avoid collisions in second level

**Result**: O(n) space, O(1) worst-case lookup!

### 3. Bloom Filters

#### The Problem

**Set membership testing** with:
- Very space-efficient storage
- Fast queries
- Allow false positives (acceptable for some applications)

**Applications**:
- Web caching (avoid storing URLs)
- Database query optimization
- Network routers (blacklist checking)
- Spell checkers

#### Structure

A **Bloom filter** for n elements:
- Bit array of size m
- k independent hash functions h₁, h₂, ..., h_k
- All bits initially 0

```
[0][0][0][0][0][0][0][0][0][0][0][0][0][0][0][0]
```

#### Operations

**Insert(x)**:
```
for i = 1 to k:
    set bit[h_i(x)] = 1
```

**Query(x)**:
```
for i = 1 to k:
    if bit[h_i(x)] == 0:
        return FALSE  // definitely not in set
return TRUE  // probably in set
```

#### Example

Let m = 16, k = 3, n = 2

Insert "cat":
- h₁("cat") = 2, h₂("cat") = 7, h₃("cat") = 12
```
[0][0][1][0][0][0][0][1][0][0][0][0][1][0][0][0]
```

Insert "dog":
- h₁("dog") = 5, h₂("dog") = 7, h₃("dog") = 14
```
[0][0][1][0][0][1][0][1][0][0][0][0][1][0][1][0]
```

Query "cat": Check bits 2, 7, 12 → all 1 → return TRUE ✓

Query "bird":
- h₁("bird") = 3, h₂("bird") = 7, h₃("bird") = 10
- Bit 3 is 0 → return FALSE ✓

Query "fox":
- h₁("fox") = 2, h₂("fox") = 7, h₃("fox") = 14
- All are 1 → return TRUE ✗ (false positive!)

#### Analysis

**False negatives**: Impossible! If x was inserted, all k bits are definitely set.

**False positives**: Possible. Another combination of elements might set the same bits.

**Probability of false positive**:

After inserting n elements:
- Probability a specific bit is still 0: (1 - 1/m)^(kn)
- Approximately e^(-kn/m)

Probability of false positive:
```
P(false positive) ≈ (1 - e^(-kn/m))^k
```

**Optimal k**:
```
k* = (m/n) ln 2 ≈ 0.693 m/n
```

With optimal k:
```
P(false positive) ≈ (1/2)^k ≈ 0.6185^(m/n)
```

**Example**: With m = 10n and k = 7:
- False positive rate ≈ 0.8%
- Space: only 10 bits per element (vs. storing full elements!)

**Space efficiency**:
- Traditional hash table: O(n) elements, each requiring O(log U) bits
- Bloom filter: O(n) bits total!
- Trade-off: Accept small false positive rate for huge space savings

**Properties**:
- **No false negatives**: If returns FALSE, element definitely not in set
- **False positives possible**: If returns TRUE, element probably in set
- **Cannot delete**: Setting bit to 0 might affect other elements
- **Very space efficient**: Constant bits per element regardless of element size

**Counting Bloom Filters**: Use counters instead of bits to support deletions.

---

## Analysis Techniques {#analysis-techniques}

### 1. Indicator Random Variables

#### The Technique

**Idea**: Convert counting problems into sums of indicator random variables.

**Definition**: For event A, indicator I_A:
```
I_A = 1 if A occurs
I_A = 0 if A does not occur
```

**Key property**: E[I_A] = P(A)

**Why useful**: Linearity of expectation applies to indicators!

#### Example: Expected Number of Comparisons

Problem: Count expected comparisons in randomized algorithm.

**Approach**:
1. Define X_{ij} = indicator that elements i and j are compared
2. Total comparisons: X = Σ X_{ij}
3. E[X] = Σ E[X_{ij}] = Σ P(i and j compared)

This avoids complex probability calculations!

#### Example: Birthday Paradox

Problem: What's the expected number of pairs sharing a birthday in a room of n people?

**Solution**:
```
X_{ij} = indicator that person i and j share birthday
E[X_{ij}] = P(same birthday) = 1/365
Total pairs: C(n,2) = n(n-1)/2
E[# pairs with same birthday] = n(n-1)/(2·365)
```

For n = 23: E ≈ 0.69 (so by pigeonhole, high probability of at least one pair!)

### 2. Linearity of Expectation

#### The Property

**For any random variables X and Y** (even dependent!):
```
E[X + Y] = E[X] + E[Y]
```

More generally:
```
E[Σ X_i] = Σ E[X_i]
```

**Crucial**: This holds even if the X_i are **dependent**!

#### Why So Powerful

- Don't need to calculate joint probability distributions
- Don't need independence assumptions
- Simplifies many analyses dramatically

#### Example: Coupon Collector Problem

**Problem**: How many random draws (with replacement) to collect all n types of coupons?

**Analysis**:
- Let X_i = number of draws to get the i-th new coupon (after having i-1)
- Total draws: X = X₁ + X₂ + ... + X_n
- P(get new coupon when have i-1) = (n-i+1)/n
- E[X_i] = n/(n-i+1) (geometric distribution)

By linearity:
```
E[X] = Σ_{i=1}^n E[X_i]
     = Σ_{i=1}^n n/(n-i+1)
     = n · Σ_{i=1}^n 1/i
     = n · H_n
     ≈ n ln n
```

**Result**: Expected O(n log n) draws to collect all n coupons.

### 3. Probabilistic Method

#### The Technique

**Idea**: Prove existence by showing positive probability.

**Logic**:
1. Define a probability space
2. Show expected value of random variable < k (or > k)
3. Conclude: Some outcome must have value < k (or > k)

**"If average is good, best must be even better!"**

#### Example: MAX-CUT

**Problem**: Given graph G = (V, E), partition V into two sets to maximize edges crossing the partition.

**Claim**: There exists a cut with at least m/2 edges (where m = |E|).

**Proof**:
- Randomly assign each vertex to set A or B (probability 1/2 each)
- For each edge (u,v), P(edge crosses cut) = 1/2
- E[# edges in cut] = Σ P(edge crosses) = m/2
- Therefore, some assignment achieves ≥ m/2 edges!

This gives a **randomized 2-approximation algorithm** for MAX-CUT (NP-hard problem).

### 4. Union Bound (Boole's Inequality)

#### The Inequality

For events A₁, A₂, ..., A_n:
```
P(A₁ ∪ A₂ ∪ ... ∪ A_n) ≤ P(A₁) + P(A₂) + ... + P(A_n)
```

Or equivalently:
```
P(at least one event occurs) ≤ Σ P(A_i)
```

**Useful for**: Bounding probability of failure when multiple bad things could happen.

#### Example: Avoiding All Bad Events

If each of n bad events has probability ≤ 1/(2n):
```
P(some bad event) ≤ n · 1/(2n) = 1/2
P(no bad event) ≥ 1/2
```

So there's a good outcome with probability ≥ 1/2!

### 5. Markov's Inequality

#### The Inequality

For **non-negative** random variable X:
```
P(X ≥ a) ≤ E[X] / a
```

**Interpretation**: Probability of being much above average is small.

#### Example

If expected algorithm runtime is E[T] = 10 seconds:
```
P(T ≥ 100 sec) ≤ 10/100 = 0.1
```

At most 10% probability of taking ≥ 100 seconds.

**Limitation**: Often gives loose bounds (only uses expectation).

### 6. Chebyshev's Inequality

#### The Inequality

For random variable X with mean μ and variance σ²:
```
P(|X - μ| ≥ k) ≤ σ² / k²
```

**Interpretation**: Probability of being far from mean is bounded by variance.

#### Example: Coin Flips

Flip n fair coins. X = number of heads.
- E[X] = n/2
- Var(X) = n/4
- P(|X - n/2| ≥ √n) ≤ (n/4) / n = 1/4

So with probability ≥ 3/4, number of heads is within √n of n/2.

**Better than Markov**: Uses both mean and variance.

### 7. Chernoff Bounds

#### The Bounds

For sum of independent random variables, **much tighter** bounds than Chebyshev.

**Setup**: X₁, ..., X_n independent random variables in [0,1], X = Σ X_i, μ = E[X]

**Chernoff bound** (multiplicative form):
```
P(X ≥ (1+δ)μ) ≤ e^(-δ²μ/3)  for 0 < δ ≤ 1
P(X ≤ (1-δ)μ) ≤ e^(-δ²μ/2)  for 0 < δ ≤ 1
```

**Interpretation**: Exponentially unlikely to deviate far from mean!

#### Example: Coin Flips

Flip n fair coins, X = number of heads.
- μ = n/2
- P(X ≥ 3n/4) = P(X ≥ (1+1/2)μ)
              ≤ e^(-n/48)

For n = 100: probability < 10⁻⁹ (vs. Chebyshev: ≈ 0.04)

**Conclusion**: Concentration is exponentially strong!

---

## Applications and Examples {#applications}

### Load Balancing

**Problem**: Assign n jobs to m machines to minimize maximum load.

**Deterministic**: Assign to least-loaded machine → max load ≤ n/m + (n-1)

**Randomized**: Assign each job to random machine
- Expected load on each machine: n/m
- By Chernoff bound: with high probability, max load ≈ n/m + O(√(n log m / m))

**Better randomized** (power of two choices):
- For each job, pick 2 random machines, assign to less loaded
- Max load ≈ n/m + O(log log m) with high probability!
- Exponentially better than pure random!

### Randomized Rounding

**Technique**: Solve LP relaxation, randomly round fractional solutions.

**Example: Set Cover**:
1. Solve LP to get fractional solution x_i ∈ [0,1]
2. Include set i with probability x_i
3. Repeat O(log n) times to ensure coverage

**Result**: O(log n)-approximation in expectation.

### Hashing Applications

**Robin Hood Hashing**:
- On collision, evict element farther from home position
- Randomized insertion order
- Expected probe length: O(1) with high probability

**Cuckoo Hashing**:
- Two hash tables, two hash functions
- Element can be in one of two positions
- On insert, if both positions full, evict one and rehash
- O(1) worst-case lookup!
- O(1) expected insertion

### Monte Carlo Simulation

**Integration**: Estimate integral by random sampling
```
∫[a,b] f(x) dx ≈ (b-a) · (1/n) Σ f(x_i)
```
where x_i are random points in [a,b].

Error decreases as O(1/√n) by central limit theorem.

### Randomized Rounding in Approximation

Many NP-hard optimization problems:
1. Formulate as integer linear program
2. Solve LP relaxation (polynomial time)
3. Randomly round fractional solution
4. Analyze expected approximation ratio

**Examples**:
- MAX-SAT
- Vertex Cover
- Set Cover
- MAX-CUT

---

## Problem-Solving Framework {#problem-solving}

### When to Use Randomization

Consider randomization when:

1. **Avoiding worst cases**: Deterministic algorithm has bad worst-case on some inputs
   - Example: QuickSort with random pivots

2. **Simplicity**: Randomized algorithm much simpler than deterministic
   - Example: Skip lists vs. balanced trees

3. **Breaking symmetry**: Need to break ties or symmetry
   - Example: Distributed algorithms, leader election

4. **No good deterministic algorithm known**: Problem seems hard
   - Example: Min-cut, primality testing

5. **Approximation acceptable**: Fast approximate answer better than slow exact
   - Example: Monte Carlo methods, Bloom filters

6. **Average-case performance critical**: Expected time more important than worst-case
   - Example: Hash tables, randomized incremental algorithms

### Design Patterns

#### Pattern 1: Random Sampling
- **Idea**: Sample random elements to make decisions
- **Examples**: Random pivots, randomized incremental construction
- **Analysis**: Show sample is representative with high probability

#### Pattern 2: Random Ordering
- **Idea**: Process input in random order
- **Examples**: Randomized QuickSort, incremental algorithms
- **Analysis**: Show expected performance over all orderings

#### Pattern 3: Random Choices
- **Idea**: Make random decisions at each step
- **Examples**: Skip lists (random height), randomized rounding
- **Analysis**: Show expected structure has good properties

#### Pattern 4: Randomized Relaxation
- **Idea**: Solve relaxed problem, randomly round solution
- **Examples**: LP-rounding for approximation algorithms
- **Analysis**: Bound approximation ratio in expectation

#### Pattern 5: Random Hashing
- **Idea**: Use random hash function from universal family
- **Examples**: Hash tables, Bloom filters, fingerprinting
- **Analysis**: Show low collision probability

### Analysis Strategy

**Step 1**: Identify random choices
- What random bits are used?
- What is the sample space?

**Step 2**: Define random variables
- What are we trying to count/measure?
- Use indicators when possible!

**Step 3**: Apply linearity of expectation
- Express target as sum of simpler random variables
- Compute expectations of components

**Step 4**: Handle dependencies (if needed)
- Are variables independent?
- If dependent, use conditional probability or other techniques

**Step 5**: Apply concentration bounds (if needed)
- Need to bound probability of deviation from expectation?
- Use Markov, Chebyshev, or Chernoff depending on strength needed

**Step 6**: Amplify success probability (if needed)
- Run algorithm multiple times
- Take best/majority result

### Common Pitfalls

1. **Forgetting worst-case still exists**: Expected O(n) doesn't mean worst-case O(n)!

2. **Assuming independence**: Linearity of expectation works regardless, but other properties may require independence

3. **Wrong probability space**: Carefully define what's random (inputs vs. algorithm choices)

4. **Not using indicators**: Makes analysis much harder

5. **Loose concentration bounds**: Use strongest applicable bound (Chernoff > Chebyshev > Markov)

### Comparing Alternatives

| Approach | Pros | Cons | When to Use |
|----------|------|------|-------------|
| **Deterministic** | Worst-case guarantee, predictable | May be complex, input-dependent | Need guarantees, critical systems |
| **Las Vegas** | Always correct, simple | Random runtime, no guarantee | Correctness critical, time flexible |
| **Monte Carlo** | Fast, bounded time | May be wrong, need verification | Speed critical, errors acceptable |
| **Approximation** | Polynomial time, bounded quality | Not optimal | NP-hard problems, large scale |

---

## Complexity Cheat Sheet {#complexity-cheat-sheet}

### Randomized Algorithms

| Algorithm | Expected Time | Worst-Case Time | Space | Type |
|-----------|---------------|-----------------|-------|------|
| Randomized QuickSort | O(n log n) | O(n²) | O(log n) | Las Vegas |
| Randomized QuickSelect | O(n) | O(n²) | O(log n) | Las Vegas |
| Karger Min-Cut | O(n²) per run | O(n²) | O(n+m) | Monte Carlo |
| Randomized Incremental | Varies | Varies | Varies | Las Vegas |

### Randomized Data Structures

| Data Structure | Search | Insert | Delete | Space | Notes |
|----------------|--------|--------|--------|-------|-------|
| Skip List | O(log n) exp | O(log n) exp | O(log n) exp | O(n) exp | Simple alternative to trees |
| Hash Table (universal) | O(1) exp | O(1) exp | O(1) exp | O(n) | With O(1) load factor |
| Bloom Filter | O(k) | O(k) | - | O(m) bits | False positives, k = # hashes |
| Treap | O(log n) exp | O(log n) exp | O(log n) exp | O(n) | BST with random priorities |

### Complexity Class Notes

- **exp** = expected/average over random choices
- **w.h.p.** = with high probability (≥ 1 - 1/n^c for constant c)
- **amortized** = average over sequence of operations
- All worst-case times assume adversarial input but random algorithm choices

### Probability Tool Complexity

| Technique | Strength | Requirements | Typical Use |
|-----------|----------|--------------|-------------|
| Markov | Weak (1/a bound) | Non-negative RV | First-order bound |
| Chebyshev | Medium (1/k² bound) | Mean + Variance | Deviation from mean |
| Chernoff | Strong (exponential) | Independence | Tight concentration |
| Union Bound | Additive | None | Multiple events |
| Linearity of Exp | Exact | None (works always!) | Counting, indicators |

---

## Final Tips and Summary {#tips-summary}

### Study Tips

1. **Master indicator random variables**: This technique appears everywhere in analysis

2. **Practice linearity of expectation**: It's the most powerful tool - works even with dependencies!

3. **Understand probability vs. expectation**: Expected O(n) ≠ O(n) with high probability

4. **Know your concentration bounds**:
   - Markov: Weak but general
   - Chebyshev: Needs variance
   - Chernoff: Strong but needs independence

5. **Recognize Las Vegas vs. Monte Carlo**: Correctness vs. time guarantees

6. **Compare with deterministic**: Randomized often simpler and faster in expectation

7. **Draw probability trees**: Visualize sample space and events

8. **Work through examples**: Calculate small cases by hand to build intuition

### Common Exam Topics

1. **Analysis of randomized QuickSort**: Using indicator random variables

2. **Skip list operations**: Understanding the structure and analysis

3. **Bloom filter calculations**: False positive rate, optimal k

4. **Expected running time**: Computing E[T(n)] for various algorithms

5. **Probability calculations**: Basic probability for algorithm analysis

6. **Comparing approaches**: When to use randomization vs. deterministic

7. **Concentration bounds**: Applying Markov, Chebyshev, Chernoff

### Key Takeaways

**Why Randomization?**
- Simplicity: Often easier to design and implement
- Efficiency: Better expected performance
- Robustness: No worst-case inputs (with good random choices)
- Novel solutions: Enables algorithms for problems without good deterministic approaches

**Core Techniques**:
- Random sampling (pivots, elements)
- Random ordering (shuffle input)
- Random choices (skip list heights)
- Random hashing (universal hash functions)

**Analysis Tools**:
- Indicator random variables → count using expectation
- Linearity of expectation → sum expectations even with dependence
- Concentration bounds → high probability statements

**Trade-offs**:
- Expected vs. worst-case time
- Correctness vs. speed (Las Vegas vs. Monte Carlo)
- Space vs. accuracy (Bloom filters)
- Optimality vs. approximation

**Design Principles**:
1. Identify what to randomize (input order, choices, samples)
2. Prove correctness (if Las Vegas) or bound error (if Monte Carlo)
3. Analyze expected performance using probability tools
4. Apply concentration bounds for high-probability statements
5. Amplify success by repetition if needed

### Common Mistakes to Avoid

1. **Confusing expected value with high probability**: E[X] = n doesn't mean X ≈ n always

2. **Assuming independence without justification**: Check carefully before using independence

3. **Using wrong concentration bound**: Match bound strength to what you need

4. **Ignoring worst case**: Randomized doesn't eliminate worst case, just makes it unlikely

5. **Forgetting to seed properly**: Implementation needs good random number generator

6. **Overcomplicated analysis**: Often indicators and linearity are enough

### Practice Problems

To master randomized algorithms, practice:

1. **QuickSort analysis**: Derive E[T(n)] = O(n log n) from scratch

2. **Hash table analysis**: Compute expected chain length with universal hashing

3. **Skip list probability**: Calculate probability of various heights and search times

4. **Bloom filter design**: Given n, m, find optimal k and false positive rate

5. **Coupon collector**: Derive E[T] = O(n log n)

6. **Birthday paradox**: Calculate collision probabilities

7. **Random walk**: Analyze expected time to reach boundary

8. **Balls and bins**: Expected maximum load when throwing n balls into m bins

---

## Summary

### The Big Picture

Randomized algorithms represent a powerful paradigm shift: **using randomness as a computational resource**. By making random choices during execution, we can often achieve:

- Simpler algorithms
- Better expected performance
- Robustness against adversarial inputs
- Solutions to problems without efficient deterministic approaches

### The Three Pillars

1. **Las Vegas Algorithms**: Always correct, random time
   - QuickSort, QuickSelect, skip lists
   - Analyze expected running time

2. **Monte Carlo Algorithms**: Fixed time, may err
   - Primality testing, Bloom filters
   - Analyze error probability

3. **Randomized Data Structures**: Use randomness in construction
   - Skip lists, hash tables, Bloom filters
   - Analyze expected performance

### Essential Analysis Tools

1. **Indicator Random Variables**: Convert counting to expectation
2. **Linearity of Expectation**: Sum expectations even with dependence!
3. **Concentration Bounds**: Prove high-probability guarantees
4. **Probabilistic Method**: Existence by positive probability

### When to Use

- Input-dependent worst cases → random pivots/ordering
- Complex balanced structures → simpler randomized structures
- NP-hard problems → randomized approximation
- Space constraints → probabilistic structures (Bloom filters)
- Distributed systems → symmetry breaking

### The Bottom Line

Randomized algorithms are not just theoretical curiosities - they're practical tools widely used in:
- Database systems (query optimization)
- Networks (load balancing, routing)
- Machine learning (stochastic gradient descent)
- Cryptography (key generation)
- Web services (caching, filtering)

Master the analysis techniques, understand the trade-offs, and recognize when randomization can simplify your solutions!

---

**Good luck with your studies!** Remember: randomness is a feature, not a bug!
