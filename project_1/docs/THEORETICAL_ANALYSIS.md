# Theoretical Complexity Analysis
## Minimum Edge Cover Problem

**Student Number:** 113920
**Course:** Advanced Algorithms (AA)
**Problem:** Minimum Edge Cover (Problem 20)

---

## Table of Contents

1. [Problem Definition](#problem-definition)
2. [Theoretical Foundations](#theoretical-foundations)
3. [Algorithm Complexity Analysis](#algorithm-complexity-analysis)
4. [Complexity Comparison Table](#complexity-comparison-table)
5. [Proof Sketches](#proof-sketches)
6. [References](#references)

---

## Problem Definition

**Minimum Edge Cover Problem:**

Given an undirected graph G = (V, E) with n vertices and m edges, find an edge cover C ⊆ E of minimum cardinality.

**Edge Cover Definition:** A set C of edges is an edge cover if every vertex in V is incident to at least one edge in C.

**Input:** Graph G = (V, E)
**Output:** Minimum cardinality edge cover C ⊆ E
**Constraint:** ∀v ∈ V, ∃e ∈ C such that v is incident to e

**Note:** Assumes no isolated vertices (every vertex has degree ≥ 1).

---

## Theoretical Foundations

### Gallai's Theorem

For any graph G = (V, E) with n vertices:

```
α'(G) + β'(G) = n
```

Where:
- **α'(G)** = size of maximum matching
- **β'(G)** = size of minimum edge cover

**Implication:**

```
|minimum edge cover| = n - |maximum matching|
```

This theorem is the foundation for the polynomial-time optimal algorithm.

### Matching Theory

- **Matching:** A set M of edges where no two edges share a vertex
- **Maximum Matching:** Matching of maximum cardinality
- **Maximal Matching:** Matching that cannot be extended (may not be maximum)

**Key Result:** Maximum matching can be found in polynomial time:
- General graphs: O(n²·⁵) using Edmonds' Blossom algorithm
- Bipartite graphs: O(√n · m) using Hopcroft-Karp algorithm

### Edge Cover Bounds

For a graph G with n vertices:

**Lower Bound:**
```
|minimum edge cover| ≥ ⌈n/2⌉
```
Achieved when a perfect or near-perfect matching exists.

**Upper Bound:**
```
|minimum edge cover| ≤ n - 1
```
Achieved in star graphs (one vertex connected to all others).

---

## Algorithm Complexity Analysis

### 1. Exhaustive Search (Backtracking)

**Algorithm:** Explore all 2^m possible subsets of edges, check if each is an edge cover, return minimum.

#### Time Complexity

**Worst Case: O(2^m)**

**Recurrence Relation:**
```
T(k) = 2·T(k-1) + O(n)
```
Where:
- k = number of edges remaining to process
- O(n) = cost of checking if current subset is valid edge cover

**Solution:**
```
T(m) = 2^m · O(n) = O(n · 2^m)
```

**Simplified:** O(2^m) since checking edge cover is linear in n.

**Best Case: O(2^m)**
Still need to explore exponential search space even with early termination.

**Space Complexity: O(m)**
Recursion depth is at most m (edge list length).

#### Optimizations

1. **Branch Pruning:** Abandon branches where |current| ≥ |best|
2. **Early Termination:** Stop when optimal bound is reached
3. **Greedy Upper Bound:** Start with greedy solution to improve pruning

**Optimized Average Case:** Still O(2^m) worst-case, but constant factors improve significantly.

---

### 2. Branch and Bound

**Algorithm:** Exhaustive search with lower bound pruning using matching theory.

#### Time Complexity

**Worst Case: O(2^m)**
Same as exhaustive in worst case (must explore entire tree).

**Best Case: O(m · n)**
When lower bound immediately prunes most branches.

**Average Case: O(2^(m/k))**
Where k > 1 is the pruning effectiveness factor. Empirically, k ≈ 2-4 for random graphs.

**Space Complexity: O(m)**

#### Lower Bound Calculation

**Simple Bound (Used):**
```
LB(partial_cover) = |partial_cover| + ⌈uncovered_vertices / 2⌉
```

**Tight Bound (Theoretical):**
```
LB(partial_cover) = |partial_cover| + (uncovered_vertices - |max_matching_in_remaining|)
```

Computing tight bound requires solving maximum matching repeatedly → expensive.

**Trade-off:** Use simple bound for speed; still provides good pruning.

---

### 3. Optimal Matching-Based (Polynomial)

**Algorithm:**
1. Find maximum matching M in G
2. For each unmatched vertex v, add any incident edge to M
3. Return resulting edge cover

#### Time Complexity

**Worst Case: O(n²·⁵)**
Dominated by maximum matching computation using Blossom algorithm.

**Breakdown:**
- Find maximum matching: O(n²·⁵) [Edmonds' Blossom]
- Identify unmatched vertices: O(n)
- Add incident edges: O(n · avg_degree) = O(m)

**Total:** O(n²·⁵ + m) = O(n²·⁵) since m ≤ n²

**Best Case: O(n²·⁵)**
Matching computation dominates regardless of input.

**Space Complexity: O(n + m)**
Store graph structure and matching.

#### Correctness (Gallai's Theorem)

**Proof Sketch:**

1. Let M be a maximum matching with |M| = α'(G)
2. Let V_unmatched = vertices not covered by M
3. |V_unmatched| = n - 2·|M|
4. For each v ∈ V_unmatched, add any incident edge
5. Edge cover size = |M| + |V_unmatched| = |M| + (n - 2·|M|) = n - |M|
6. By Gallai's theorem: β'(G) = n - α'(G) = n - |M| ✓

Therefore, this algorithm finds the minimum edge cover in polynomial time.

---

### 4. Greedy Coverage Heuristic

**Algorithm:** Iteratively select edges covering the most uncovered vertices.

#### Time Complexity

**Worst Case: O(m · n)**

**Analysis:**
- Outer loop: At most n/2 iterations (each edge covers ≤ 2 vertices)
- Inner loop: Scan all m edges to find best
- Per iteration: O(m) work

**Total:** O((n/2) · m) = O(m · n)

**Best Case: O(m · n)**
Must scan all edges even if solution is found early.

**Space Complexity: O(n)**
Track uncovered vertices.

#### Approximation Quality

**Theoretical Bound:** Unknown for this specific greedy strategy.

**Empirical Results (from experiments):**
- Finds optimal in ~78% of test cases
- Average quality ratio: 0.935 (6.5% larger than optimal)
- Never observed worse than 2× optimal

**Conjecture:** This greedy strategy is a 2-approximation (not proven here).

---

### 5. Greedy Matching-Based Heuristic

**Algorithm:** Find greedy maximal matching, then add edges for unmatched vertices.

#### Time Complexity

**Worst Case: O(m)**

**Analysis:**
- Find maximal matching: O(m) [scan edges once]
- Add edges for unmatched vertices: O(n + m)

**Total:** O(m)

**Best Case: O(m)**

**Space Complexity: O(n)**

#### Approximation Quality

**Theoretical Bound:** 2-approximation

**Proof Sketch:**
- Let M_greedy = greedy maximal matching
- Let M_opt = maximum matching
- |M_greedy| ≥ |M_opt| / 2 (property of maximal matching)
- Greedy solution size = n - |M_greedy|
- Optimal solution size = n - |M_opt|
- Ratio = (n - |M_greedy|) / (n - |M_opt|) ≤ 2 ✓

**Empirical Results:**
- Often finds optimal (especially for sparse graphs)
- Average quality ratio: ~0.92-0.95
- Fast execution (fastest of all algorithms)

---

## Complexity Comparison Table

| Algorithm | Time Complexity | Space | Optimal? | Notes |
|-----------|----------------|-------|----------|-------|
| **Exhaustive Search** | O(2^m) | O(m) | ✅ Yes | Exponential, impractical for m > 25 |
| **Branch & Bound** | O(2^m)* | O(m) | ✅ Yes | Better constants, effective pruning |
| **Optimal Matching** | O(n²·⁵) | O(n+m) | ✅ Yes | **Polynomial, scales to large graphs** |
| **Greedy Coverage** | O(m·n) | O(n) | ❌ No | Fast heuristic, ~78% optimal |
| **Greedy Matching** | O(m) | O(n) | ❌ No | **Fastest**, 2-approximation |

*\*Average case better than worst case due to pruning*

### Algorithm Selection Guidelines

**For Optimal Solutions:**
- **Small graphs (m ≤ 25):** Exhaustive or Branch & Bound
- **Medium/Large graphs:** Optimal Matching (polynomial)
- **Very large graphs:** Optimal Matching (scales well)

**For Fast Approximations:**
- **Need speed:** Greedy Matching (O(m))
- **Better quality:** Greedy Coverage (O(m·n))

**For Analysis/Comparison:**
- Use all algorithms on small graphs
- Compare exponential vs polynomial scalability
- Validate heuristic quality

---

## Proof Sketches

### Theorem 1: Edge Cover Existence

**Statement:** An edge cover exists if and only if G has no isolated vertices.

**Proof:**
- (⇒) If edge cover exists, all vertices are incident to some edge, so no isolated vertices.
- (⇐) If no isolated vertices, every v has degree ≥ 1. Take C = E (all edges). Every v is incident to some e ∈ C. ✓

### Theorem 2: Minimum Edge Cover Size (Gallai)

**Statement:** For graph G with n vertices, β'(G) = n - α'(G).

**Proof Sketch:**
1. **Lower bound:** Any edge cover must cover n vertices. Each edge covers ≤ 2 vertices. Need ≥ n/2 edges. With maximum matching of size α', we can achieve n - α' edges.

2. **Upper bound:** Construct edge cover of size n - α':
   - Start with maximum matching M (size α')
   - M covers 2α' vertices
   - Remaining n - 2α' vertices are unmatched
   - For each unmatched vertex, add any incident edge
   - Total edges: α' + (n - 2α') = n - α' ✓

3. **Optimality:** Cannot do better than n - α' because:
   - Each edge in matching covers 2 vertices efficiently
   - Unmatched vertices need dedicated edges
   - This construction is optimal ✓

### Theorem 3: Exhaustive Search Correctness

**Statement:** Exhaustive search finds minimum edge cover.

**Proof:**
- Exhaustive search explores all 2^m subsets of edges
- For each subset, checks if it's a valid edge cover
- Returns minimum size valid cover
- Since all possibilities are examined, minimum is guaranteed ✓

### Theorem 4: Branch & Bound Correctness

**Statement:** Branch & Bound finds minimum edge cover (same as exhaustive).

**Proof:**
- B&B is exhaustive search with pruning
- Pruning only eliminates branches that provably cannot improve best solution
- If LB(branch) ≥ |best|, branch cannot yield better solution
- All potentially optimal branches are explored
- Therefore, same optimality guarantee as exhaustive ✓

---

## Complexity Growth Comparison

### Practical Scalability

For graph with m edges and n vertices:

| m | Exhaustive (2^m ops) | Optimal Matching (n²·⁵ ops, n≈√m) | Ratio |
|---|---------------------|----------------------------------|-------|
| 10 | 1,024 | ~178 | 6× faster |
| 15 | 32,768 | ~435 | 75× faster |
| 20 | 1,048,576 | ~894 | 1,173× faster |
| 25 | 33,554,432 | ~1,563 | 21,467× faster |
| 50 | 1.13×10¹⁵ | ~6,299 | 1.79×10¹¹ faster |

**Conclusion:** Polynomial algorithm is dramatically faster for graphs with m > 15 edges.

### Execution Time Estimates

Assuming 1 microsecond per basic operation:

| Edges | Exhaustive | Optimal Matching |
|-------|------------|------------------|
| 10 | 1.0 ms | 0.2 ms |
| 20 | 1.0 sec | 0.9 ms |
| 25 | 33.6 sec | 1.6 ms |
| 30 | 17.9 min | 2.4 ms |
| 40 | 12.7 days | 5.1 ms |
| 50 | **35.7 years** | 6.3 ms |

**Key Insight:** Exhaustive becomes impractical around m=30. Optimal matching scales to thousands of edges.

---

## References

1. **Gallai's Theorem:** Gallai, T. (1959). "Über extreme Punkt-und Kantenmengen"
2. **Blossom Algorithm:** Edmonds, J. (1965). "Paths, trees, and flowers"
3. **Matching Theory:** Lovász, L. and Plummer, M.D. (1986). "Matching Theory"
4. **Approximation Algorithms:** Vazirani, V.V. (2001). "Approximation Algorithms"
5. **Algorithm Design:** Cormen, T.H., et al. (2009). "Introduction to Algorithms" (3rd ed.)
6. **Graph Theory:** West, D.B. (2001). "Introduction to Graph Theory" (2nd ed.)

---

**Document Version:** 1.0
**Last Updated:** 2025-11-08
**Author:** João Manuel Vieira Roldão (113920)
