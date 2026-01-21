# Data Stream Algorithms - Comprehensive Study Guide

## Table of Contents
1. [Introduction to Data Streams](#introduction)
2. [The Streaming Model](#streaming-model)
3. [Sampling from Streams](#sampling)
4. [Frequency Estimation](#frequency-estimation)
5. [Heavy Hitters and Top-K](#heavy-hitters)
6. [Quantiles and Order Statistics](#quantiles)
7. [Graph Streaming](#graph-streaming)
8. [Sliding Window Algorithms](#sliding-windows)
9. [Space Lower Bounds](#lower-bounds)
10. [Applications](#applications)
11. [Problem-Solving Framework](#problem-solving)
12. [Complexity Cheat Sheet](#complexity-cheat-sheet)

---

## Introduction to Data Streams {#introduction}

### What are Data Streams?

A **data stream** is a massive sequence of data items that arrive continuously over time, where:
- Data arrives at high rate (too fast to store everything)
- Data is too large to fit in memory
- Data can only be scanned once (or very few times)
- Must process in real-time or near real-time

**Examples**:
- Network traffic monitoring (packets, flows)
- Financial transactions (trades, quotes)
- Sensor data (IoT devices, telemetry)
- Web logs (clicks, page views)
- Social media feeds (tweets, posts)
- Database query logs

### The Challenge

**Traditional algorithms assume**:
- Random access to data
- Multiple passes over data
- Unlimited time and space

**Streaming reality**:
- Sequential access only
- Single pass (or very few passes)
- Limited memory (sublinear: o(n))
- Fast processing required
- Approximate answers acceptable

### Types of Data Streams

#### 1. Cash Register Model (Insertion Only)

**Stream**: Sequence of items from universe [n]
```
a₁, a₂, a₃, ..., aₘ
```

**Frequency vector**: f[i] = number of times item i appears

**Updates**: f[i]++ (only increments)

**Example**: Counting word frequencies in documents
```
Stream: "the", "cat", "sat", "on", "the", "mat"
f["the"] = 2, f["cat"] = 1, f["sat"] = 1, ...
```

#### 2. Turnstile Model (Insertions and Deletions)

**Updates**: f[i] += c where c can be positive or negative
- Positive: Insertion
- Negative: Deletion/decrements

**Constraint**: f[i] ≥ 0 always (non-negative frequencies)

**Example**: Network traffic (packets arrive and depart)

#### 3. Strict Turnstile Model

**Additional constraint**: f[i] ≥ 0 throughout (never goes negative)

**Example**: Bank account balances (can't go negative)

#### 4. General Turnstile Model

**No non-negativity constraint**: f[i] can be negative

**Example**: Net changes, deltas

### Key Metrics and Goals

#### Space Complexity

**Goal**: Use o(n) space (sublinear in universe size)

**Typical targets**:
- O(log n) - logarithmic (ideal)
- O(√n) - square root (acceptable)
- O(n^ε) for small ε - slightly sublinear

**Example**: n = 1 billion
- O(log n) ≈ 30 bits
- O(√n) ≈ 32K items
- O(n) = 1 billion items (not feasible)

#### Time Complexity

**Per-item processing**: O(1) or O(polylog n)

**Query time**: Should be fast (often O(1) or O(log n))

#### Accuracy

**ε-approximation**: Answer within (1±ε) of true value

**δ-failure probability**: Fails with probability at most δ

**Typical**: (ε,δ)-approximation
- ε = 0.01 (1% error)
- δ = 0.01 (1% failure probability)

### Why Streaming Algorithms?

**1. Scale**: Data too large for RAM
- Google processes 20+ PB per day
- Facebook handles 500+ TB of data daily
- Cannot store everything in memory

**2. Speed**: Real-time requirements
- Network intrusion detection (milliseconds)
- High-frequency trading (microseconds)
- Cannot afford slow algorithms

**3. Cost**: Memory is expensive
- RAM more expensive than disk per GB
- Want minimal hardware requirements
- Enable processing on edge devices

**4. Privacy**: Don't want to store raw data
- Streaming aggregates preserve privacy
- Comply with regulations (GDPR)
- Sketches don't reveal individual records

---

## The Streaming Model {#streaming-model}

### Formal Model

**Input**: Stream σ = (a₁, u₁), (a₂, u₂), ..., (aₘ, uₘ)
- aᵢ ∈ [n] - item identifier
- uᵢ - update value (typically +1 or -1)

**Frequency vector**: f = (f₁, f₂, ..., fₙ) where f[i] = Σ uⱼ for aⱼ = i

**Memory**: O(polylog(n,m)) space (sublinear)

**Time**: O(polylog(n,m)) per update

### Common Query Types

#### 1. Point Query

**Q**: What is f[i]? (frequency of item i)

**Example**: How many times did user 12345 appear?

#### 2. Range Query

**Q**: What is Σ f[i] for i ∈ [a,b]?

**Example**: How many items in price range [$10, $20]?

#### 3. Heavy Hitters (Top-K)

**Q**: Which items have f[i] > φn? (φ = threshold)

**Example**: Which users generated >1% of traffic?

#### 4. Quantiles

**Q**: What is the k-th smallest value?

**Example**: Median response time, 95th percentile latency

#### 5. Join Size

**Q**: Given two streams, what is |R ⋈ S|?

**Example**: How many users clicked both ads A and B?

#### 6. Graph Properties

**Q**: Number of triangles, connected components, etc.

**Example**: Detect communities in social network

### Fundamental Trade-offs

#### Space vs Accuracy

**Smaller space → Higher error**

**Example** (Count-Min Sketch):
- Space = O(1/ε · log(1/δ))
- Error = ε · ||f||₁ with probability 1-δ

Reducing ε by 2× doubles space requirement.

#### Space vs Time

**Smaller space → More computation per update**

**Example**:
- Exact counting: O(n) space, O(1) time
- Approximate: O(log n) space, O(log n) time

#### Passes vs Space

**More passes → Less space needed**

**Example** (Median):
- 1 pass: O(1/ε · log n) space
- 2 passes: O(√n) space
- ∞ passes: O(log n) space (sorting)

### Randomization in Streaming

**Why randomize?**
1. **Space lower bounds**: Many problems require Ω(n) space deterministically
2. **Simple algorithms**: Randomization often leads to simpler solutions
3. **High probability guarantees**: Can achieve low failure probability

**Analysis techniques**:
- Expectation and variance
- Concentration bounds (Chernoff, Markov)
- Union bound over multiple estimates

---

## Sampling from Streams {#sampling}

### 1. Uniform Random Sampling

#### Problem

**Goal**: Maintain a random sample of k items from stream of unknown length n

**Challenge**: Don't know n in advance!

**Applications**:
- Query optimization (sample-based statistics)
- Data exploration
- Visualization

#### Reservoir Sampling (Vitter 1985)

**Algorithm**:
```
ReservoirSample(stream, k):
    reservoir = [first k items from stream]

    for i = k+1 to n:
        j = Random(1, i)  // random integer in [1,i]
        if j ≤ k:
            reservoir[j] = stream[i]  // replace item j

    return reservoir
```

**Key insight**: After processing i items, each item has probability k/i of being in reservoir.

**Proof by induction**:
- Base (i=k): Each of first k items has probability k/k = 1 ✓
- Step: Assume true for i-1
  - Existing item stays with prob: (k/(i-1)) × (1 - 1/i + (i-k)/i × k/k) = k/i ✓
  - New item enters with prob: k/i ✓

**Complexity**:
- Space: O(k)
- Time per item: O(1)
- Final sample: Each item has probability k/n

**Example** (k=2, n=5):
```
Stream: a, b, c, d, e

After a,b: reservoir = [a,b]
After c: j=Random(1,3)=2 → reservoir = [a,c]
After d: j=Random(1,4)=4 → no change → [a,c]
After e: j=Random(1,5)=1 → reservoir = [e,c]

Each item has probability 2/5 of being in final sample
```

#### Weighted Reservoir Sampling

**Problem**: Sample with weights w[i]

**Algorithm A-Res (Efraimidis-Spirakis)**:
```
WeightedReservoirSample(stream, k):
    reservoir = empty heap (size k)

    for each item i with weight w[i]:
        key[i] = Random(0,1)^(1/w[i])  // random key
        if |reservoir| < k:
            reservoir.insert(i, key[i])
        else if key[i] > reservoir.min_key():
            reservoir.pop_min()
            reservoir.insert(i, key[i])

    return reservoir
```

**Property**: Item i selected with probability proportional to w[i]

**Complexity**:
- Space: O(k log k) (heap)
- Time per item: O(log k)

### 2. Distinct Sampling

#### Problem

**Goal**: Sample uniformly from distinct items (ignore duplicates)

**Challenge**: Can't store all distinct items (too many)

**Example**: Sample unique URLs from web crawl (billions of URLs, millions unique)

#### Distinct Sampling Algorithm

**Algorithm**:
```
DistinctSample(stream, k):
    hash_table = {}
    threshold = 0

    for each item x:
        if x not in hash_table:
            h = hash(x)  // uniform in [0,1]
            if h > threshold:
                hash_table[x] = h
                if |hash_table| > k:
                    remove item with smallest hash
                    threshold = min hash in table

    return items in hash_table
```

**Property**: Each distinct item selected with probability ≈ k/n_distinct

**Complexity**:
- Space: O(k)
- Time per item: O(1) expected (hash table)

### 3. Bernoulli Sampling

#### Problem

**Goal**: Include each item with probability p independently

**Algorithm**:
```
BernoulliSample(stream, p):
    sample = []

    for each item x:
        if Random() < p:
            sample.append(x)

    return sample
```

**Properties**:
- Each item included independently with probability p
- Expected sample size: p·n
- Actual size varies (binomial distribution)

**When to use**:
- Know sampling rate p in advance
- Don't need fixed sample size
- Want independence

**Example**: Sample 1% of web requests
```
p = 0.01
Expected sample size = 0.01 × total_requests
```

### 4. Sampling for Sum Estimation

#### Problem

**Goal**: Estimate Σ f[i] from sample

**Challenge**: Frequencies vary widely (some items very frequent)

#### Inverse Probability Weighting

**Algorithm**:
```
Sample items with probability p[i]
For sampled item i: estimate f[i] by f̃[i] = f[i]/p[i]
Estimate Σ f[i] by Σ f̃[i] over sampled items
```

**Analysis**: E[f̃[i]] = f[i] (unbiased)

**Variance reduction**: Sample high-frequency items with higher probability

#### Priority Sampling

**Optimal sampling for sum estimation**

**Algorithm**:
1. Assign priority τ[i] = f[i] / Random(0,1) to each item
2. Keep k items with highest priority
3. Threshold: τ_min = k-th highest priority

**Estimator**: Σ max(f[i], τ_min) / k

**Property**: Minimizes variance among all sampling schemes!

---

## Frequency Estimation {#frequency-estimation}

### The Problem

**Goal**: Estimate frequencies f[i] for all items i in stream

**Exact solution**: Hash table - O(n) space (too large!)

**Streaming solution**: Use sketch - O(log n) space with small error

### Count-Min Sketch (CM Sketch)

#### Structure

**Invented by**: Cormode & Muthukrishnan (2004)

**Data structure**:
- 2D array: Count[1..d, 1..w]
- d independent hash functions: h₁, h₂, ..., h_d
- Each hⱼ: [n] → [w]

```
       w columns
    ┌─────────────┐
  d │ □ □ □ □ □ □ │ h₁
    │ □ □ □ □ □ □ │ h₂
rows│ □ □ □ □ □ □ │ h₃
    │ □ □ □ □ □ □ │ h₄
    └─────────────┘
```

**Parameters**:
- w = ⌈e/ε⌉ (e ≈ 2.718)
- d = ⌈ln(1/δ)⌉

**Space**: O((1/ε) · log(1/δ)) = O((1/ε) · log n) typically

#### Operations

**Update(i, c)**: Increment frequency of item i by c
```
Update(i, c):
    for j = 1 to d:
        Count[j, hⱼ(i)] += c
```

**Query(i)**: Estimate frequency of item i
```
Query(i):
    return min_{j=1..d} Count[j, hⱼ(i)]
```

**Why minimum?** Each counter is an upper bound (collisions only add).

#### Example

Parameters: d=3, w=5, ε=0.4, δ≈0.05

```
Stream: a, b, c, a, b, a

After processing:
h₁(a)=2, h₂(a)=4, h₃(a)=1
h₁(b)=3, h₂(b)=2, h₃(b)=5
h₁(c)=2, h₂(c)=3, h₃(c)=4

        1   2   3   4   5
Row 1:  0  [3]  2   0   0  (a,c) → (b) → ()
Row 2:  0   1  [1]  3   0  () → (b,c) → () → (a)
Row 3: [3]  0   0   1   2  (a) → () → () → (c) → (b)

Query(a): min(3, 3, 3) = 3 ✓ (exact!)
Query(b): min(2, 1, 2) = 1 ✗ (true: 2, error from collision)
Query(c): min(3, 1, 1) = 1 ✓ (exact!)
```

#### Analysis

**Guarantee**: With probability ≥ 1-δ:
```
f[i] ≤ f̃[i] ≤ f[i] + ε·||f||₁
```

Where:
- f[i] = true frequency
- f̃[i] = estimated frequency
- ||f||₁ = Σ f[j] = total frequency

**Proof sketch**:
- Each Count[j, hⱼ(i)] = f[i] + Σ_{k: hⱼ(k)=hⱼ(i), k≠i} f[k]
- Expected collision: E[Σ f[k]] = ||f||₁/w ≈ ε·||f||₁
- By Markov: P(collisions > 2ε·||f||₁) < 1/2
- Taking minimum over d rows: P(all rows large) < δ

**Space complexity**: O((1/ε) · log(1/δ))

**Time complexity**:
- Update: O(d) = O(log(1/δ))
- Query: O(d) = O(log(1/δ))

#### Properties

**Advantages**:
1. **Small space**: O(1/ε · log(1/δ)) independent of n
2. **Fast updates**: O(log(1/δ)) per item
3. **Point queries**: Fast frequency estimation
4. **Range queries**: Sum adjacent cells
5. **Inner products**: Can estimate ⟨f,g⟩
6. **Mergeable**: Can combine multiple sketches

**Limitations**:
1. **Over-estimates**: Never under-estimates (due to collisions)
2. **Better for heavy items**: Error proportional to ||f||₁
3. **No deletions** (in basic version): Requires strictly non-negative updates

### Count Sketch (CS)

#### Motivation

**Count-Min Sketch problem**: Always over-estimates (collision only adds)

**Goal**: Unbiased estimator (can over or under-estimate)

#### Structure

**Similar to CM Sketch but adds sign**:
- 2D array: Count[1..d, 1..w]
- d hash functions: h₁, ..., h_d : [n] → [w]
- d sign functions: s₁, ..., s_d : [n] → {-1, +1}

#### Operations

**Update(i, c)**:
```
Update(i, c):
    for j = 1 to d:
        Count[j, hⱼ(i)] += sⱼ(i) × c
```

**Query(i)**:
```
Query(i):
    return median_{j=1..d} (sⱼ(i) × Count[j, hⱼ(i)])
```

**Why median?** Removes effect of large collisions (more robust)

#### Analysis

**Guarantee**: With probability ≥ 1-δ:
```
|f̃[i] - f[i]| ≤ ε·||f||₂
```

Where ||f||₂ = √(Σ f[j]²) is L₂ norm.

**Key difference**: Error in terms of ||f||₂ not ||f||₁
- ||f||₂ ≤ ||f||₁ always
- If frequencies skewed (few heavy hitters), ||f||₂ << ||f||₁
- **Count Sketch better for skewed distributions!**

**Parameters**:
- w = ⌈e/ε²⌉
- d = ⌈log(1/δ)⌉

**Space**: O(1/ε² · log(1/δ))

#### Comparison: Count-Min vs Count Sketch

| Aspect | Count-Min Sketch | Count Sketch |
|--------|------------------|--------------|
| **Error bound** | f[i] + ε·||f||₁ | ε·||f||₂ |
| **Bias** | Over-estimates | Unbiased |
| **Space** | O(1/ε · log(1/δ)) | O(1/ε² · log(1/δ)) |
| **Best for** | Heavy hitters, ||f||₁ | Skewed data, ||f||₂ small |
| **Aggregation** | min | median |
| **Deletions** | Not supported | Supported |

**Rule of thumb**:
- Use **Count-Min** for: Heavy hitters, non-negative updates, lower space
- Use **Count** for: Deletions, unbiased estimates, skewed distributions

### AMS Sketch (Alon-Matias-Szegedy)

#### Problem

**Goal**: Estimate F₂ = Σ f[i]² (second frequency moment)

**Why F₂?**
- Measures "surprise" or entropy
- Self-join size: |R ⋈ R|
- Gini index for inequality

#### Algorithm

**Key idea**: Use random ±1 variables

**Structure**:
- Array: Count[1..d]
- d 4-wise independent hash functions: s₁, ..., s_d : [n] → {-1, +1}

**Update(i, c)**:
```
Update(i, c):
    for j = 1 to d:
        Count[j] += sⱼ(i) × c
```

**Estimate F₂**:
```
EstimateF₂():
    return median_{j=1..d} (Count[j]²)
```

**Analysis**: E[Count[j]²] = F₂ (unbiased!)

**Guarantee**: With probability ≥ 1-δ:
```
|F̃₂ - F₂| ≤ ε·F₂
```

**Space**: O(1/ε² · log(1/δ))

**Applications**:
- Database self-join size
- Duplicate detection
- Data stream clustering

---

## Heavy Hitters and Top-K {#heavy-hitters}

### Problem Definition

**Heavy Hitters (φ-frequent items)**:
- Given threshold φ (e.g., 0.01 for 1%)
- Find all items i with f[i] ≥ φ·n

**Top-K**:
- Find K items with highest frequencies

**Applications**:
- Network monitoring: Heavy traffic sources
- Web analytics: Most visited pages
- Database query optimization: Frequently accessed data
- Fraud detection: Suspicious account activity

### 1. Misra-Gries Algorithm (1982)

#### The Algorithm

**Key idea**: Keep track of k-1 candidate items, decrement when see others

**Structure**:
- Hashtable: items → counts (at most k-1 entries)

**Algorithm**:
```
MisraGries(stream, k):
    counters = {}  // item → count

    for each item x in stream:
        if x in counters:
            counters[x] += 1
        else if |counters| < k-1:
            counters[x] = 1
        else:  // decrement all
            for each item y in counters:
                counters[y] -= 1
                if counters[y] == 0:
                    delete y from counters

    return counters
```

**Post-processing**: Second pass to verify actual frequencies (or use with sketch)

#### Example

k=3 (find items with frequency > n/3), n=10

```
Stream: a, b, c, a, b, a, c, d, e, a

Step 1: a → counters = {a:1}
Step 2: b → counters = {a:1, b:1}
Step 3: c → counters = {a:1, b:1, c:1} (full, k-1=2)
Step 4: a → counters = {a:2, b:1, c:1}
Step 5: b → counters = {a:2, b:2, c:1}
Step 6: a → counters = {a:3, b:2, c:1}
Step 7: c → counters = {a:3, b:2, c:2}
Step 8: d → counters = {a:2, b:1, c:1} (decremented all)
Step 9: e → counters = {a:1} (decremented all, b and c removed)
Step 10: a → counters = {a:2}

Result: a is candidate (true freq = 4, which is > 10/3)
```

#### Analysis

**Guarantee**:
- All items with f[i] > n/k are in output
- Output has at most k-1 items
- Stored count is ≤ actual count ≤ stored count + n/k

**Space**: O(k) items

**Time**: O(1) amortized per item

**Accuracy**: Error ≤ n/k for each item

**For φ-heavy hitters**: Set k = ⌈1/φ⌉
- Example: φ=0.01 (1%) → k=100

**Limitation**: Need second pass to get exact counts (or combine with Count-Min Sketch)

### 2. Space Saving Algorithm (Metwally et al. 2005)

#### Improvement over Misra-Gries

**Key insight**: Always keep k items (never delete all)

**Algorithm**:
```
SpaceSaving(stream, k):
    counters = {}  // item → count (exactly k entries after warmup)
    min_heap = MinHeap()  // track minimum count

    for each item x in stream:
        if x in counters:
            counters[x] += 1
            min_heap.update(x)
        else if |counters| < k:
            counters[x] = 1
            min_heap.insert(x, 1)
        else:  // replace minimum
            (y, min_count) = min_heap.pop_min()
            delete counters[y]
            counters[x] = min_count + 1  // inherit count!
            min_heap.insert(x, min_count + 1)

    return counters
```

**Key difference**: When replacing, new item inherits the old count (plus 1)

#### Example

k=2, stream: a, b, c, a, b, a, d

```
Step 1: a → counters = {a:1}
Step 2: b → counters = {a:1, b:1}
Step 3: c → replace min (a or b), say a → counters = {b:1, c:2}
Step 4: a → replace min (b) → counters = {c:2, a:2}
Step 5: b → replace min (c or a), say a → counters = {c:2, b:3}
Step 6: a → replace min (c) → counters = {b:3, a:3}
Step 7: d → replace min (b or a), say b → counters = {a:3, d:4}
```

#### Analysis

**Guarantee**:
- All items with f[i] > n/k are in output
- Better accuracy than Misra-Gries (tighter bounds)
- Error: true_count - stored_count ≤ n/k

**Space**: O(k)

**Time**: O(log k) per item (due to heap operations)

**Advantage**: Single pass, no need for verification (but overestimates)

### 3. Frequent Algorithm (Demaine et al. 2002)

#### Deterministic Algorithm for Heavy Hitters

**Algorithm**:
```
Frequent(stream, k):
    counters = {}  // item → count (at most k entries)

    for each item x in stream:
        if x in counters:
            counters[x] += 1
        else if |counters| < k:
            counters[x] = 1
        else:  // decrement all
            for each item y in counters:
                counters[y] -= 1
                if counters[y] == 0:
                    delete y

    // Output items with counter > 0
    return {x : counters[x] > 0}
```

**Similar to Misra-Gries but different parameter**: k items (not k-1)

#### Analysis

**Guarantee**: All items with f[i] > n/(k+1) are in output

**Space**: O(k)

**Time**: O(k) per item (may need to scan all counters)

### 4. Count-Min Sketch for Heavy Hitters

#### Combining Sketch with Thresholding

**Algorithm**:
```
HeavyHitters_CM(stream, φ, ε, δ):
    cms = CountMinSketch(ε, δ)

    for each item x in stream:
        cms.Update(x, 1)
        if cms.Query(x) ≥ φ·n:  // threshold check
            mark x as potential heavy hitter

    return potential heavy hitters
```

**Guarantee**:
- All items with f[i] ≥ φ·n are found
- False positives: f[i] ≥ (φ-ε)·n

**Space**: O(1/ε · log(1/δ))

**Advantage**: No need for second pass

**Disadvantage**: Need to know n (or estimate it)

### Comparison of Heavy Hitter Algorithms

| Algorithm | Space | Time/item | Passes | Guarantees |
|-----------|-------|-----------|--------|------------|
| Misra-Gries | O(k) | O(1) | 2 | Exact with second pass |
| Space Saving | O(k log k) | O(log k) | 1 | Overestimate ≤ n/k |
| Frequent | O(k) | O(k) | 1 | All items > n/(k+1) |
| CM Sketch | O(1/ε log(1/δ)) | O(log(1/δ)) | 1 | All items ≥ φ·n |

**Choice depends on**:
- Space budget (k vs 1/ε)
- Accuracy requirements
- Number of passes available
- Need for exact counts

---

## Quantiles and Order Statistics {#quantiles}

### Problem Definition

**Quantile**: Given φ ∈ [0,1], find element at rank ⌊φn⌋

**Examples**:
- Median: φ = 0.5
- 95th percentile: φ = 0.95
- Quartiles: φ = 0.25, 0.5, 0.75

**Applications**:
- Performance monitoring (latency percentiles)
- Quality of service (SLA: 95% requests < 100ms)
- Anomaly detection (values beyond 99th percentile)

**Challenge**: Can't store all values (too much space)

### ε-Approximate Quantile

**Definition**: Return element with rank in [(φ-ε)n, (φ+ε)n]

**Example**: For median (φ=0.5) with ε=0.01:
- Acceptable rank: [0.49n, 0.51n]
- Within 1% of true median

### 1. Sampling-Based Quantile

#### Random Sampling

**Algorithm**:
```
QuantileSampling(stream, φ, ε):
    sample = ReservoirSample(stream, k)
    sort(sample)
    return sample[⌊φk⌋]
```

**Analysis**: For ε-approximation, need k = O(1/ε² · log(1/δ))

**Space**: O(1/ε²)

**Advantage**: Simple, works for any distribution

**Disadvantage**: Large space for small ε

### 2. GK Algorithm (Greenwald-Khanna 2001)

#### Deterministic Quantile Algorithm

**Key idea**: Maintain summary of stream with bounded error

**Summary structure**: Sequence of tuples (v, g, Δ)
- v: value
- g: minimum rank gap
- Δ: maximum error

**Invariants**:
1. Values sorted: v₁ < v₂ < ... < vₛ
2. True rank in [r_min, r_max] where r_min = Σgᵢ, r_max = r_min + Δ
3. Maximum error: Δ ≤ 2εn

**Algorithm** (simplified):
```
GK_Quantile(stream, ε):
    summary = []  // list of (v, g, Δ) tuples

    for each value v in stream:
        insert (v, 1, ⌊2εn⌋) into summary (sorted position)

        if summary gets too large:
            compress summary by merging tuples
            maintain error bound 2εn

    Query(φ):
        find tuple with rank ≈ φn in summary
        return its value
```

**Compression**: Merge adjacent tuples if combined error within bounds

#### Analysis

**Guarantee**: ε-approximate quantile (deterministic)

**Space**: O(1/ε · log(εn))

**Time**:
- Insert: O(log(1/ε)) amortized
- Query: O(log(1/ε))

**Advantage**: Deterministic, works for multiple quantiles simultaneously

### 3. Q-Digest

#### Hierarchical Quantile Summary

**Structure**: Tree-based summary
- Leaves represent ranges [i, i]
- Internal nodes represent ranges [i, j]
- Node stores count for its range

**Compression rule**: Merge nodes if children's counts are small

**Space**: O(1/ε · log U) where U is universe size

**Operations**:
- Insert: O(log U)
- Query quantile: O(log U)
- Merge digests: O(1/ε · log U)

**Advantage**: Mergeable (useful for distributed systems)

### 4. t-Digest

#### Algorithm for Extreme Quantiles

**Motivation**: GK and Q-digest give uniform error; we want better accuracy at tails

**Key idea**: Variable resolution - more accuracy near 0 and 1 (extreme quantiles)

**Structure**: Clusters of points with centroid and weight

**Properties**:
- Better accuracy for extreme quantiles (p=0.01, 0.99)
- Mergeable
- Used in production (Elasticsearch, Prometheus)

**Space**: O(1/ε) with better constants than GK

---

## Graph Streaming {#graph-streaming}

### Problem Setting

**Graph stream**: Sequence of edge updates
```
(u₁, v₁), (u₂, v₂), ..., (uₘ, vₘ)
```

**Challenge**: Graph has n vertices, m edges where m >> n²

**Goal**: Compute graph properties using o(n²) space

**Examples**:
- Triangle counting
- Connected components
- Degree distribution
- Clustering coefficient

### 1. Triangle Counting

#### Problem

**Triangle**: Three vertices u, v, w with edges (u,v), (v,w), (u,w)

**Applications**:
- Social network analysis (community detection)
- Spam detection
- Recommendation systems

**Exact algorithm**: O(n³) or O(m^1.5) time, O(m) space (too expensive!)

#### Sampling-Based Triangle Counting

**Algorithm** (3-pass):
```
TriangleCounting(stream, k):
    # Pass 1: Count edges
    m = CountEdges(stream)

    # Pass 2: Sample k edges uniformly
    sample = ReservoirSample(stream, k)

    # Pass 3: Check triangles
    triangles_in_sample = 0
    for (u,v) in sample:
        for each edge (u,w) in stream:
            if (v,w) in stream:
                triangles_in_sample++

    # Estimate
    total_triples = C(m, 3)  // m choose 3
    sample_triples = C(k, 3)
    return triangles_in_sample × (total_triples / sample_triples)
```

**Analysis**:
- Space: O(k)
- Passes: 3
- Error: ε with probability 1-δ for k = O(1/ε² · 1/T) where T = #triangles

#### Single-Pass Triangle Counting

**Algorithm**: TRIÈST (De Stefani et al. 2016)

**Key idea**: Maintain random sample of edges, count triangles within sample, scale up

```
TRIÉST(stream, k):
    S = {}  // sample of edges (size ≤ k)
    t = 0   // time
    τ = 0   // triangle count

    for each edge (u,v) in stream:
        t++

        # Update triangle count
        τ += |neighbors(u) ∩ neighbors(v)| in S

        # Reservoir sampling
        if |S| < k:
            S.add((u,v))
        else with probability k/t:
            remove random edge from S
            S.add((u,v))

    # Estimate
    return τ × C(t,3) / C(k,3)
```

**Analysis**:
- Space: O(k)
- Passes: 1
- Time per edge: O(deg) where deg = average degree in sample
- Error: ε-approximation with k = O(m/T · 1/ε²)

### 2. Connected Components

#### Problem

**Goal**: Determine if graph is connected, or find number of components

**Exact algorithm**: DFS/BFS requires O(n+m) space (too much!)

#### Streaming Algorithm

**Challenge**: Very hard in single pass!

**Lower bound**: Ω(n) space required for exact answer in worst case

**Approximate approach**: Use sketching
- Assign random label to each vertex
- Propagate labels along edges
- Estimate components from label distribution

**Semi-streaming model**: O(n polylog n) space allowed
- Can store vertex info but not all edges
- Multiple passes allowed

**Algorithm** (semi-streaming):
```
ConnectedComponents(stream, passes):
    labels = {v: v for v in vertices}  // initially each vertex its own component

    for pass = 1 to log(n):
        for each edge (u,v) in stream:
            labels[u] = labels[v] = min(labels[u], labels[v])

    return |{labels[v] : v in vertices}|  // number of distinct labels
```

**Space**: O(n)

**Passes**: O(log n)

**Guarantee**: Exact number of components

### 3. Degree Distribution

#### Problem

**Goal**: Estimate distribution of vertex degrees

**Applications**:
- Network analysis (scale-free networks)
- Anomaly detection (unusually high degree)

#### Sampling-Based Estimation

**Algorithm**:
```
DegreeDistribution(stream, k):
    sample_vertices = random k vertices
    degrees = {v: 0 for v in sample_vertices}

    for each edge (u,v) in stream:
        if u in sample_vertices:
            degrees[u]++
        if v in sample_vertices:
            degrees[v]++

    return histogram of degrees
```

**Analysis**:
- Space: O(k)
- Each sampled vertex degree estimated from partial information

**Better approach**: Use graph sampling techniques (edge sampling, random walk sampling)

---

## Sliding Window Algorithms {#sliding-windows}

### Problem Setting

**Sliding window**: Consider only last W elements of stream

**Types**:
1. **Count-based window**: Last W items
2. **Time-based window**: Items from last T time units

**Applications**:
- Real-time monitoring (recent events matter)
- Anomaly detection (detect sudden changes)
- Trending topics (recent popularity)

**Challenge**: Can't store all W items (too much space)

### 1. Basic Statistics in Sliding Windows

#### Count in Window

**Problem**: How many items in last W elements?

**Exact solution**: Circular buffer - O(W) space

**Approximate solution**: Use decaying exponential histogram

#### Sum in Window

**Problem**: Sum of values in last W elements

**Exact solution**: Queue - O(W) space

**Space-efficient**: Use sampling or exponential histogram

### 2. Exponential Histograms

#### Problem

**Goal**: Count 1-bits in last W bits of stream

**Example**: Count clicks in last 1000 events

#### DGIM Algorithm (Datar-Gionis-Indyk-Motwani)

**Key idea**: Bucket recent 1-bits, merge old buckets

**Bucket**: (timestamp, size)
- timestamp: when bucket ends
- size: number of 1s in bucket (power of 2)

**Invariants**:
1. Bucket sizes are powers of 2
2. For each size, at most 2 buckets (except possibly smallest)
3. Buckets stored from newest to oldest

**Algorithm**:
```
ExponentialHistogram(W):
    buckets = []  // list of (timestamp, size)
    current_time = 0

    OnNewBit(bit):
        current_time++

        # Remove old buckets
        while buckets and buckets[-1].timestamp < current_time - W:
            buckets.pop()

        if bit == 1:
            # Add new bucket of size 1
            buckets.insert(0, (current_time, 1))

            # Merge buckets of same size
            i = 0
            while i < len(buckets) - 2:
                if buckets[i].size == buckets[i+1].size == buckets[i+2].size:
                    # Merge two oldest buckets of this size
                    new_bucket = (buckets[i+1].timestamp, buckets[i+1].size * 2)
                    buckets.pop(i+1)
                    buckets.pop(i+1)
                    buckets.insert(i+1, new_bucket)
                i++

    Count():
        if not buckets:
            return 0
        # Sum all bucket sizes except oldest (which might partially outside window)
        total = sum(b.size for b in buckets[:-1])
        total += buckets[-1].size // 2  // partial bucket
        return total
```

**Example** (W=10):
```
Stream: 0 0 1 0 1 1 0 1 1 0 1 1

After position 12:
Buckets: [(12,1), (11,1), (9,2), (7,1), (6,1), (4,1), (3,1)]
         └─────┘  └─────┘  └────┘
          size 1   size 1   size 2

Count: 1 + 1 + 2 + 1 + 1 + 1 + 0.5 = 7.5 ≈ 7 or 8
True count: 7
```

#### Analysis

**Space**: O(log W) buckets

**Error**: At most 1/2 of last bucket = O(1) error

**Relative error**: O(log W / #1s-in-window)
- Good when many 1s
- Large relative error when few 1s

**Update time**: O(log W) amortized

**Query time**: O(log W)

### 3. Sliding Window Heavy Hitters

#### Problem

**Goal**: Find frequent items in last W elements

**Challenges**:
1. Item frequencies change over time
2. Need to forget old occurrences
3. Limited space

#### Time-Decaying Count-Min Sketch

**Idea**: Age decay - old updates contribute less

**Algorithm**:
```
DecayingCMS(ε, δ, decay_rate):
    cms = CountMinSketch(ε, δ)
    current_time = 0

    Update(item):
        current_time++
        # Periodic decay
        if current_time % decay_period == 0:
            for all counters:
                counter *= decay_rate  // exponential decay

        cms.Update(item, 1)

    Query(item):
        return cms.Query(item)
```

**Decay rate**: λ ≈ 1 - 1/W (forget after ~W time steps)

**Analysis**:
- Recent items weighted more
- Smooth decay (no sharp cutoff)
- Space: same as regular CMS

#### Sliding Window with Explicit Timestamps

**Algorithm**: Store (item, timestamp) pairs with eviction

**Space-time tradeoff**: Store more pairs for accuracy vs space

---

## Space Lower Bounds {#lower-bounds}

### Communication Complexity Framework

**Key technique**: Reduce streaming problem to communication problem

**Setup**:
- Alice has first half of stream
- Bob has second half
- They want to compute some function
- Communication is expensive (lower bound on communication → lower bound on space)

### 1. Distinct Elements Lower Bound

**Problem**: Count distinct elements in stream

**Theorem**: Any streaming algorithm with ε-approximation requires Ω(1/ε² + log n) bits

**Proof sketch**:
- Reduce to Alice-Bob problem
- Alice has set A, Bob has set B
- Want to compute |A ∪ B|
- Information-theoretic argument: need Ω(min(|A|, |B|) + log n) bits

**Consequence**: HyperLogLog is nearly optimal!

### 2. Frequency Estimation Lower Bound

**Problem**: Estimate f[i] for any i

**Theorem**: Require Ω(1/ε) space for ε-approximation

**Consequence**: Count-Min Sketch is optimal in ε!

### 3. Quantiles Lower Bound

**Problem**: ε-approximate φ-quantile

**Theorem**: Require Ω(1/ε · log(εn)) space in comparison model

**Consequence**: GK algorithm is optimal!

### 4. Graph Problems

#### Triangle Counting

**Theorem**: Require Ω(1/ε² · min(n, m/T)) space for ε-approximation

Where T = number of triangles.

#### Connectivity

**Theorem**: Exact connectivity requires Ω(n) space in worst case (single pass)

**Implication**: Must use semi-streaming (multiple passes) or approximation

### General Lessons

**Trade-offs are inherent**:
1. Can't avoid space-accuracy tradeoff
2. Multiple passes can reduce space
3. Randomization often necessary

**Algorithm design goal**: Match lower bounds (up to log factors)

---

## Applications {#applications}

### 1. Network Monitoring

#### Traffic Analysis

**Problem**: Monitor network traffic in real-time
- Packet rates: billions per second
- Cannot store all packets

**Solutions**:
- **Count-Min Sketch**: Track per-flow byte/packet counts
- **Heavy Hitters**: Detect heavy flows (elephant flows)
- **Quantiles**: Monitor latency distributions (SLA violations)

**Example deployment**:
```
For each packet:
    cms.Update(src_ip, packet_size)
    cms.Update(dst_ip, packet_size)
    cms.Update((src_ip, dst_ip), packet_size)

Periodically:
    Find heavy hitters (flows > 1% total traffic)
    Report 95th percentile latency
```

**Impact**:
- Detect DDoS attacks (sudden heavy hitters)
- Capacity planning (traffic patterns)
- QoS enforcement (latency SLAs)

#### NetFlow/sFlow

**Standard protocols** for network monitoring using sampling
- Sample 1 in N packets
- Export sampled packet headers
- Reconstruct traffic statistics

**Enhancement with sketches**:
- Use sketches at router for better accuracy
- Coordinate sketches across routers
- Detect distributed attacks

### 2. Database Systems

#### Query Optimization

**Problem**: Estimate query result sizes for optimal query plans

**Statistics needed**:
- Cardinality: |R|, |S|
- Join sizes: |R ⋈ S|
- Distinct values: COUNT(DISTINCT col)

**Solutions**:
- **HyperLogLog**: Distinct count per column
- **Count-Min Sketch**: Frequency histograms
- **Sampling**: Sample rows for statistics

**Example (PostgreSQL)**:
```sql
-- Internal statistics maintained
HyperLogLog per column for COUNT(DISTINCT)
Histograms using sampling for value distributions
```

**Benefit**: Better query plans → faster queries

#### Stream Processing (Kafka, Flink)

**Scenario**: Process event streams in real-time

**Operations**:
- Windowed aggregations
- Join multiple streams
- Detect patterns

**Sketches used**:
- **Tumbling windows**: Reset counters periodically
- **Sliding windows**: Exponential histograms
- **Session windows**: Variable-length windows

**Example (Apache Flink)**:
```java
stream
    .keyBy(event -> event.userId)
    .window(SlidingEventTimeWindows.of(Time.minutes(10), Time.minutes(1)))
    .aggregate(new CountMinSketchAggregator())
```

### 3. Big Data Analytics

#### Large-Scale Log Analysis

**Problem**: Analyze logs from distributed systems (TB/day)

**Questions**:
- How many unique users? (HyperLogLog)
- Which pages are popular? (Heavy hitters)
- What's the median response time? (Quantiles)

**Architecture**:
```
Edge nodes: Maintain local sketches
Aggregator: Merge sketches periodically
Dashboard: Query merged sketches
```

**Example (Twitter)**:
- Track trending hashtags (heavy hitters)
- Count unique tweeters per topic (HyperLogLog)
- Monitor API latency (quantiles)

#### A/B Testing

**Problem**: Compare metrics between experiment groups

**Metrics**:
- Conversion rates
- Revenue per user
- Engagement (click-through rates)

**Sketches**:
- **HyperLogLog**: Unique users per variant
- **Count-Min**: Track events per user
- **Quantiles**: Distribution of values

**Benefit**: Real-time experiment monitoring without full data processing

### 4. IoT and Sensor Networks

#### Edge Computing

**Scenario**: Sensors with limited memory/bandwidth

**Constraints**:
- Limited battery (minimize computation)
- Limited bandwidth (compress data)
- Need aggregation (not raw readings)

**Solutions**:
- Local sketches at sensors
- Periodic sketch upload (compressed)
- Cloud aggregates sketches

**Example (Smart City)**:
```
Traffic sensors:
    - Count vehicles (HyperLogLog for unique vehicles)
    - Detect heavy users (toll collection)
    - Monitor patterns (time-series sketches)

Upload: 1KB sketch per hour vs 1MB raw data
Savings: 1000× bandwidth reduction
```

### 5. Security and Fraud Detection

#### Anomaly Detection

**Problem**: Detect unusual patterns in real-time

**Techniques**:
- **Heavy hitters**: Sudden traffic spike from IP
- **Quantiles**: Values beyond 99th percentile
- **Count-Min**: Track per-user activity

**Example (Credit Card Fraud)**:
```
For each transaction:
    cms.Update((card_id, merchant), amount)
    if cms.Query((card_id, merchant)) > threshold:
        flag_for_review()
```

**Patterns detected**:
- Multiple transactions in short time
- Unusual merchant for user
- Amount exceeding typical spending

#### Intrusion Detection

**Problem**: Detect network attacks

**Signatures**:
- Port scanning (many destinations from one source)
- DDoS (many sources to one destination)
- Data exfiltration (large outbound traffic)

**Monitoring**:
```
Count-Min Sketch: Track flows
Heavy Hitters: Detect anomalies
Time windows: Recent activity only
```

### 6. Machine Learning

#### Feature Engineering

**Problem**: Compute features from large-scale data

**Use cases**:
- **Categorical encoding**: Count of each category
- **User behavior**: Historical activity patterns
- **Temporal features**: Recent vs old events

**Sketches for features**:
```python
# Instead of storing all user history
user_sketch = CountMinSketch()
for event in user_events:
    user_sketch.update(event.type)

features['event_type_counts'] = user_sketch.query('purchase')
```

**Benefit**: Bounded memory per user, fast feature computation

#### Online Learning

**Scenario**: Train model on streaming data

**Challenges**:
- Can't store all training examples
- Distribution may shift (concept drift)

**Solutions**:
- Sample important examples (reservoir sampling)
- Weight recent examples more (decay)
- Track model performance (quantiles)

---

## Problem-Solving Framework {#problem-solving}

### Step 1: Identify Problem Type

#### Cardinality Problems

**Questions**:
- How many distinct ...?
- Unique count of ...?

**Algorithm**: HyperLogLog
- Space: O(1/ε² · log log n)
- Error: 1.04/√m

**Example**: "Count unique visitors to website"

#### Frequency Problems

**Questions**:
- How often does X appear?
- Distribution of frequencies?

**Algorithms**:
- Count-Min Sketch (over-estimates, lower space)
- Count Sketch (unbiased, more space)

**Example**: "How many times did user 12345 click?"

#### Heavy Hitter Problems

**Questions**:
- Which items are most frequent?
- Items above threshold φ?

**Algorithms**:
- Space Saving (top-k)
- Misra-Gries (above threshold)
- Count-Min + threshold

**Example**: "Find URLs with >1% of traffic"

#### Quantile Problems

**Questions**:
- What's the median/percentile?
- Distribution of values?

**Algorithms**:
- GK algorithm (exact quantiles)
- Q-digest (mergeable)
- t-digest (extreme quantiles)

**Example**: "What's 95th percentile latency?"

#### Sampling Problems

**Questions**:
- Get representative sample
- Estimate from sample

**Algorithms**:
- Reservoir sampling (uniform)
- Weighted sampling (non-uniform)

**Example**: "Sample 1000 random users"

### Step 2: Determine Constraints

#### Space Budget

**Question**: How much memory available?

**Implications**:
- Tight budget → More aggressive approximation
- Generous → Can use exact or less aggressive

**Example**:
- 1KB budget, 1M items → ~8 bits/item → Must approximate
- 1MB budget, 1K items → ~1KB/item → Can be exact

#### Accuracy Requirements

**Question**: How much error acceptable?

**Trade-off**: ε error requires O(1/ε) or O(1/ε²) space

**Example**:
- 10% error (ε=0.1): Small sketch
- 0.1% error (ε=0.001): 100× larger sketch

#### Time Constraints

**Question**: How fast must updates/queries be?

**Algorithms**:
- O(1) per update: Count-Min Sketch, HyperLogLog
- O(log k) per update: Space Saving (with heap)
- O(k) per update: Misra-Gries (scan all counters)

#### Number of Passes

**Question**: Can we scan stream multiple times?

**Implications**:
- 1 pass: Streaming algorithm required
- 2 passes: Can verify/refine estimates
- Multiple passes: Semi-streaming algorithms possible

**Example**: Triangle counting
- 1 pass: TRIÈST (space O(k))
- 3 passes: Sampling (space O(k), better accuracy)

### Step 3: Choose Algorithm

#### Decision Tree

```
What do you need to compute?

├─ Cardinality (distinct count)
│  └─ HyperLogLog
│      - Space: O(1/ε² · log log n)
│      - Error: 1%
│
├─ Frequencies
│  ├─ Non-negative updates only?
│  │  ├─ Yes → Count-Min Sketch
│  │  │   - Space: O(1/ε · log(1/δ))
│  │  │   - Over-estimates
│  │  └─ No → Count Sketch
│  │      - Space: O(1/ε² · log(1/δ))
│  │      - Unbiased
│  │
│  └─ Top-K items?
│      ├─ Space Saving (k counters)
│      └─ Count-Min + Heavy Hitters
│
├─ Quantiles
│  ├─ Single pass → GK algorithm
│  │   - Space: O(1/ε · log(εn))
│  ├─ Extreme quantiles → t-digest
│  └─ Mergeable → Q-digest
│
├─ Sampling
│  ├─ Uniform → Reservoir sampling
│  ├─ Weighted → Weighted reservoir
│  └─ Distinct → Distinct sampling
│
└─ Graph problems
   ├─ Triangles → TRIÈST / Sampling
   ├─ Components → Semi-streaming DFS
   └─ Degree dist → Sampling
```

### Step 4: Parameter Tuning

#### Count-Min Sketch

```
Given: Target error ε, failure probability δ

Parameters:
    w = ⌈e/ε⌉
    d = ⌈ln(1/δ)⌉

Space = w × d × size_of_counter

Example: ε=0.01, δ=0.01
    w = ⌈2.718/0.01⌉ = 272
    d = ⌈ln(100)⌉ = 5
    Space = 272 × 5 × 4 bytes = 5.3 KB
```

#### HyperLogLog

```
Given: Target error ε

Parameters:
    m = (1.04/ε)² registers

Space = m × log₂(log₂(n)) bits

Example: ε=0.01, n=10⁹
    m = (1.04/0.01)² = 10,816
    Each register: 5 bits (log₂(30))
    Space = 10,816 × 5 bits = 6.8 KB
```

#### Space Saving

```
Given: Threshold φ or top-k

Parameters:
    k = ⌈1/φ⌉ for φ-heavy hitters
    k = desired top items for top-k

Space = k × (item_size + counter_size)

Example: Top-100 items, 64-bit items, 32-bit counters
    Space = 100 × (8 + 4) = 1.2 KB
```

### Step 5: Implementation Considerations

#### Hash Functions

**Requirements**:
- Good distribution (avoid clustering)
- Fast computation
- Independence (for multiple hashes)

**Recommended**:
- MurmurHash3 (fast, good distribution)
- xxHash (very fast)
- CityHash (Google, optimized)

**For multiple hashes**: Use double hashing
```
hᵢ(x) = (h₁(x) + i × h₂(x)) mod m
```

#### Data Structures

**Arrays vs Hash Tables**:
- Arrays: Dense universe, fixed size
- Hash tables: Sparse universe, variable size

**Example**:
- Count-Min: Array (fixed w×d)
- Space Saving: Hash table + heap (dynamic k items)

#### Numerical Stability

**Issue**: Counters can overflow

**Solutions**:
- Use larger counters (64-bit)
- Periodic normalization (scale all counters)
- Saturating arithmetic (max out at limit)

**Example (Count-Min)**:
```cpp
// Instead of:
counter[j][h_j(x)]++;

// Use:
if (counter[j][h_j(x)] < MAX_COUNT) {
    counter[j][h_j(x)]++;
}
```

### Common Pitfalls

#### 1. Choosing Wrong Algorithm

**Mistake**: Using Count-Min for deletions

**Issue**: Count-Min assumes non-negative frequencies

**Solution**: Use Count Sketch (supports negative updates)

#### 2. Insufficient Space

**Mistake**: Setting ε too small for space budget

**Result**: Sketch doesn't fit in memory

**Solution**: Balance ε and space constraints

#### 3. Poor Hash Function

**Mistake**: Using simple hash (e.g., x mod m)

**Issue**: Bad distribution → clustering → high error

**Solution**: Use cryptographic or well-tested hash

#### 4. Ignoring Failure Probability

**Mistake**: Setting δ too large

**Result**: Frequent errors (e.g., δ=0.5 means 50% failure rate!)

**Solution**: Use δ ≤ 0.01 (1%) typically

#### 5. Not Validating Results

**Mistake**: Blindly trusting sketch results

**Solution**: Validate on sample of data, compare to ground truth

---

## Complexity Cheat Sheet {#complexity-cheat-sheet}

### Cardinality Estimation

| Algorithm | Space | Error | Update | Query | Merge |
|-----------|-------|-------|--------|-------|-------|
| Exact (hash set) | O(n) | 0% | O(1) | O(1) | O(n) |
| Morris Counter | O(log log n) | ~71% | O(1) | O(1) | ✗ |
| PCSA | O(m·log n) | 0.78/√m | O(1) | O(m) | ✓ |
| LogLog | O(m·log log n) | 1.30/√m | O(1) | O(m) | ✓ |
| HyperLogLog | O(m·log log n) | 1.04/√m | O(1) | O(m) | ✓ |

**Typical**: m = 1024-16384 for HyperLogLog (0.8%-3% error)

### Frequency Estimation

| Algorithm | Space | Error | Update | Query | Deletions |
|-----------|-------|-------|--------|-------|-----------|
| Exact (hash map) | O(d) | 0% | O(1) | O(1) | ✓ |
| Count-Min | O(1/ε·log(1/δ)) | ε·||f||₁ | O(log(1/δ)) | O(log(1/δ)) | ✗ |
| Count Sketch | O(1/ε²·log(1/δ)) | ε·||f||₂ | O(log(1/δ)) | O(log(1/δ)) | ✓ |
| AMS Sketch | O(1/ε²·log(1/δ)) | ε·F₂ | O(log(1/δ)) | O(log(1/δ)) | ✓ |

**Typical**: ε=0.01, δ=0.01 → w=272, d=5 for Count-Min

### Heavy Hitters

| Algorithm | Space | Error | Update | Query | Passes |
|-----------|-------|-------|--------|-------|--------|
| Exact | O(d) | 0% | O(1) | O(d) | 1 |
| Misra-Gries | O(k) | n/k | O(1) | O(k) | 2 |
| Space Saving | O(k·log k) | n/k | O(log k) | O(k) | 1 |
| Frequent | O(k) | n/(k+1) | O(k) | O(k) | 1 |
| CM + threshold | O(1/ε·log(1/δ)) | ε·||f||₁ | O(log(1/δ)) | O(log(1/δ)) | 1 |

**Typical**: k=100-1000 for top-k

### Quantiles

| Algorithm | Space | Error | Update | Query | Passes |
|-----------|-------|-------|--------|-------|--------|
| Exact (sort) | O(n) | 0% | O(1) | O(n log n) | ∞ |
| Sampling | O(1/ε²) | ε | O(1) | O(1/ε²·log(1/ε²)) | 1 |
| GK | O(1/ε·log(εn)) | ε | O(log(1/ε)) | O(log(1/ε)) | 1 |
| Q-digest | O(1/ε·log U) | ε | O(log U) | O(log U) | 1 |
| t-digest | O(1/ε) | ε | O(1) | O(1) | 1 |

**Typical**: ε=0.01 for 1% error

### Sampling

| Algorithm | Space | Property | Update | Sample |
|-----------|-------|----------|--------|--------|
| Reservoir | O(k) | Uniform k items | O(1) | O(k) |
| Weighted Reservoir | O(k·log k) | Weighted k items | O(log k) | O(k·log k) |
| Bernoulli | O(pn) | Independent prob p | O(1) | O(pn) |
| Distinct | O(k) | Uniform k distinct | O(1) | O(k) |

**Typical**: k=1000-10000

### Graph Streaming

| Problem | Space | Error | Update | Query | Passes |
|---------|-------|-------|--------|-------|--------|
| Triangle count (exact) | O(m) | 0% | O(1) | O(m^1.5) | 1 |
| Triangle (TRIÈST) | O(k) | ε | O(deg) | O(k) | 1 |
| Triangle (sampling) | O(k) | ε | O(1) | O(km) | 3 |
| Components (exact) | O(n+m) | 0% | O(1) | O(n+m) | 1 |
| Components (semi) | O(n) | 0% | O(1) | O(n log n) | O(log n) |

**Typical**: k = sample size (1000-10000)

### Space Lower Bounds (Information-Theoretic)

| Problem | Lower Bound | Achieved By |
|---------|-------------|-------------|
| Distinct elements | Ω(1/ε² + log n) | HyperLogLog: O(1/ε²·log log n) ✓ |
| Frequency (point) | Ω(1/ε) | Count-Min: O(1/ε·log(1/δ)) ✓ |
| Quantiles | Ω(1/ε·log(εn)) | GK: O(1/ε·log(εn)) ✓ |
| F₂ moment | Ω(1/ε²) | AMS: O(1/ε²·log(1/δ)) ✓ |
| Triangles | Ω(1/ε²·min(n, m/T)) | TRIÈST: O(k) where k=1/ε²·m/T ✓ |

**Note**: ✓ means algorithm is optimal (up to log factors)

---

## Summary and Final Tips {#summary}

### Key Concepts

#### The Streaming Model

**Constraints**:
- One pass (or few passes)
- Sublinear space: o(n)
- Fast processing: O(polylog n) per item

**Approximation**:
- ε-approximation: (1±ε) factor error
- δ-failure probability: Error with probability δ
- Trade-off: Space ∝ 1/ε or 1/ε²

#### Core Techniques

1. **Sampling**: Maintain representative subset
   - Reservoir sampling for uniform sample
   - Weighted sampling for non-uniform

2. **Sketching**: Random projections to compress
   - Hash functions for randomization
   - Multiple hash functions reduce error

3. **Counting**: Probabilistic counters
   - Morris: O(log log n) bits
   - HyperLogLog: Harmonic mean for cardinality

4. **Heavy hitters**: Find frequent items
   - Counter-based: Space Saving, Misra-Gries
   - Sketch-based: Count-Min with threshold

5. **Quantiles**: Order statistics
   - Summary-based: GK algorithm
   - Tree-based: Q-digest

6. **Windows**: Recent data only
   - Exponential histograms for counts
   - Decaying sketches for frequencies

### Algorithm Selection

**Decision factors**:
1. **Problem type**: Cardinality, frequency, quantile, etc.
2. **Space budget**: How much memory available?
3. **Accuracy needs**: Required ε and δ
4. **Update types**: Insert-only or deletions?
5. **Query types**: Point, range, heavy hitters?
6. **Passes**: Single pass or multiple?

**Quick reference**:
- Distinct count → HyperLogLog
- Frequency → Count-Min (or Count Sketch with deletions)
- Top-K → Space Saving
- Quantiles → GK or t-digest
- Sample → Reservoir sampling

### Study Tips

1. **Understand trade-offs**:
   - Space vs accuracy (fundamental)
   - Time vs space (some algorithms)
   - Passes vs space (multiple passes help)

2. **Master the analysis**:
   - Expectation and variance
   - Concentration bounds (Markov, Chernoff)
   - Error bounds (additive vs multiplicative)

3. **Practice parameter calculation**:
   - Given ε, δ → compute w, d
   - Given space budget → find achievable ε
   - Compare algorithms for same space

4. **Know the applications**:
   - Network monitoring (heavy hitters, quantiles)
   - Databases (cardinality for query optimization)
   - Analytics (real-time aggregations)

5. **Understand lower bounds**:
   - Why certain space is necessary
   - When algorithms are optimal
   - Inherent limits of streaming

### Common Exam Topics

1. **Reservoir sampling**:
   - Correctness proof
   - Extensions (weighted, distinct)

2. **Count-Min Sketch**:
   - Error analysis
   - Parameter selection
   - Comparison with Count Sketch

3. **HyperLogLog**:
   - Why harmonic mean?
   - Space complexity
   - Error analysis

4. **Heavy hitters algorithms**:
   - Misra-Gries invariants
   - Space Saving mechanics
   - Guarantees (what items found?)

5. **Quantile algorithms**:
   - GK summary structure
   - ε-approximation guarantee

6. **Lower bounds**:
   - Communication complexity reductions
   - Why Ω(1/ε) or Ω(1/ε²)?

### Implementation Tips

1. **Hash functions**:
   - Use quality hash (MurmurHash3, xxHash)
   - Test distribution on your data
   - Double hashing for multiple hashes

2. **Data structures**:
   - Arrays for fixed-size (Count-Min)
   - Hash tables for sparse (Space Saving)
   - Heaps for top-k (Space Saving)

3. **Numerical issues**:
   - Counter overflow (use 64-bit or saturation)
   - Floating point precision (t-digest)
   - Normalization (when needed)

4. **Testing**:
   - Validate on known data
   - Compare to exact algorithm
   - Measure actual error distribution

5. **Libraries** (don't reinvent):
   - Java: Clearspring stream-lib
   - Python: datasketch
   - C++: datasketches-cpp
   - Rust: pdatastructs

### The Big Picture

**Why streaming algorithms matter**:
- Enable processing at scale (billions of items)
- Real-time analytics (immediate insights)
- Resource efficiency (limited memory/bandwidth)
- Privacy-preserving (no raw data storage)

**Core principle**:
> Process unbounded data with bounded resources by accepting small error

**When to use**:
- Data too large for memory
- Real-time processing required
- Approximate answers sufficient
- Communication expensive (distributed)

**When NOT to use**:
- Small data (exact algorithms cheap)
- Exact answers required (critical systems)
- Can afford multiple passes and storage
- Debugging (need precise values)

### Final Thoughts

Data stream algorithms are fundamental to modern large-scale systems:
- **Google**: HyperLogLog in BigQuery for COUNT(DISTINCT)
- **Facebook**: Heavy hitters for feed ranking
- **Netflix**: Quantiles for video quality monitoring
- **Twitter**: Trending topics (heavy hitters on time windows)

**Key advantages**:
- Near-optimal space (within log factors of lower bounds)
- Fast processing (O(polylog n) per item)
- Provable guarantees (with probability 1-δ)
- Practical and deployed at scale

**Master these algorithms and you'll be equipped to build scalable analytics systems!**

---

**Good luck with your studies!** May your streams be bounded and your sketches be accurate! 🌊📊
