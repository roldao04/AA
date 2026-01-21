# Probabilistic Counters and AMQ Filters - Comprehensive Study Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Probabilistic Counters](#probabilistic-counters)
3. [Cardinality Estimation](#cardinality-estimation)
4. [AMQ Filters - Introduction](#amq-introduction)
5. [Bloom Filters](#bloom-filters)
6. [Advanced AMQ Filters](#advanced-amq-filters)
7. [Analysis and Comparison](#analysis-comparison)
8. [Applications](#applications)
9. [Problem-Solving Framework](#problem-solving)
10. [Complexity Cheat Sheet](#complexity-cheat-sheet)

---

## Introduction {#introduction}

### The Space-Accuracy Trade-off

In many applications, we face a fundamental trade-off:
- **Exact algorithms**: Guaranteed correctness but high space/time cost
- **Approximate algorithms**: Small error probability but huge space/time savings

**Key Insight**: For many applications, approximate answers are sufficient if we can:
1. Bound the error probability
2. Save significant space/time
3. Handle much larger datasets

### Two Fundamental Problems

#### Problem 1: Counting with Limited Space

**Exact counting**: Requires O(log n) bits to count up to n
- For n = 1 billion: 30 bits needed
- What if we have millions of counters?
- Can we do better by accepting small error?

**Probabilistic counters**: Use O(log log n) bits with controlled error
- For n = 1 billion: 5 bits instead of 30!
- 6× space savings for each counter

#### Problem 2: Membership Testing with Limited Space

**Exact membership** (hash table): O(n) space for n elements
- Must store full elements or keys
- For large elements (URLs, documents), space expensive

**Approximate membership** (AMQ filters): O(n) bits with false positives
- Only need constant bits per element
- Accept small false positive rate
- 10-20× space savings typical

### When to Use Approximate Structures

Use approximate structures when:
1. **Space is limited**: Memory constraints, cache size, network bandwidth
2. **Scale is large**: Billions of elements, distributed systems
3. **Errors are acceptable**: False positives OK, false negatives not critical
4. **Speed is critical**: Faster operations with simpler structures
5. **Real-time processing**: Streaming data, online algorithms

**Examples**:
- Web cache: "Have we seen this URL?" (false positives → redundant fetch)
- Databases: "Is this value in the table?" (false positives → extra lookup)
- Network routers: "Is this IP blacklisted?" (false positives → block innocent IP)
- Analytics: "How many unique visitors?" (approximate count sufficient)

---

## Probabilistic Counters {#probabilistic-counters}

### 1. Morris Counter (1978)

#### The Problem

**Goal**: Count up to n using O(log log n) bits instead of O(log n) bits.

**Motivation**: If you have millions of counters (e.g., counting distinct words in documents), space adds up!

#### The Algorithm

**Key Idea**: Don't count every event; increment probabilistically!

**Representation**: Store X where the count estimate is 2^X

**Algorithm**:
```
Initialize: X = 0  (estimate = 2^0 = 1)

On each event:
    With probability 1/2^X:
        X = X + 1
```

**Estimating the count**: Return 2^X - 1 (or 2^X, depending on variant)

**Example execution**:
```
Event 1: X=0, prob=1/2^0=1    → X becomes 1 (estimate = 2)
Event 2: X=1, prob=1/2^1=0.5  → flip coin...
Event 3: X=1, prob=1/2^1=0.5  → flip coin...
...
After n events: X ≈ log₂(n)
```

#### Analysis

**Space**: X requires O(log log n) bits
- To count to n=1 billion: X ≤ 30, needs only 5 bits!

**Expectation**: E[2^X] ≈ n (can be shown by induction)

**Variance**: Var[2^X] ≈ n²/2
- Standard deviation ≈ n/√2
- Relative error: σ/μ ≈ 1/√2 ≈ 71%
- This is quite high!

**Accuracy**: The estimate can vary significantly (high variance)

#### Improved Morris Counter

**Problem**: Variance is too high (71% relative error)

**Solution**: Use multiple independent counters and average!

**Algorithm**:
```
Initialize: X₁, X₂, ..., Xₘ = 0

On each event:
    For i = 1 to m:
        With probability 1/2^(Xᵢ):
            Xᵢ = Xᵢ + 1

Estimate: (2^(X₁) + 2^(X₂) + ... + 2^(Xₘ)) / m
```

**Analysis**:
- Space: m × O(log log n) bits
- Variance reduced by factor of m
- Relative error: ≈ 1/√(2m)
- With m = 32 counters: relative error ≈ 12.5%

**Trade-off**: More space for better accuracy

#### Morris+ Variant

**Generalization**: Use base a instead of 2
```
Store X where estimate = a^X
Increment with probability 1/a^X
```

**Choice of a**:
- Larger a: Less frequent updates, more space-efficient
- Smaller a: More accurate estimates
- Common choice: a = 1.1 to 2

### 2. PCSA (Probabilistic Counting with Stochastic Averaging)

#### The Problem

**Distinct elements counting**: Given a stream of elements (with duplicates), estimate the number of distinct elements.

**Applications**:
- Unique visitors to a website
- Distinct words in documents
- Cardinality of database joins
- Network traffic analysis

**Challenge**: Exact counting requires O(n) space to store seen elements.

#### The Algorithm (Flajolet-Martin Basis)

**Key Idea**: Use hash function to generate "random" bit patterns; look at position of first 1-bit.

**Intuition**:
- Hash element to binary string
- Look at position of first 1-bit (rightmost)
- If we see first 1 at position k, likely about 2^k distinct elements
- Use multiple hash functions and average for accuracy

**Basic FM Algorithm**:
```
Initialize: bitmap B[0...L] = 0  (L = max log value)

For each element x:
    h = hash(x)  // binary string
    r = position of rightmost 1-bit in h
    B[r] = 1     // set bitmap at position r

Estimate: R = position of leftmost 0 in B
Return: 2^R / φ  where φ ≈ 0.77351
```

**Example**:
```
hash("alice") = ...010000  → r=4
hash("bob")   = ...000100  → r=2
hash("alice") = ...010000  → r=4 (duplicate, no change)
hash("carol") = ...001000  → r=3

Bitmap B: [1,0,1,1,1,0,0,...]
Leftmost 0 at position 1
Estimate: 2^1 / 0.77351 ≈ 2.6
```

#### PCSA Algorithm

**Improvement over basic FM**: Use multiple bitmaps for averaging

**Structure**:
- Use m bitmaps (e.g., m = 64)
- Use hash function to assign each element to one bitmap
- Compute estimate for each bitmap, then average

**Algorithm**:
```
Initialize: m bitmaps B₁[0...L], ..., Bₘ[0...L] = 0

For each element x:
    i = hash₁(x) mod m      // which bitmap?
    h = hash₂(x)            // pattern
    r = rightmost 1-bit position in h
    Bᵢ[r] = 1

For each bitmap i:
    Rᵢ = position of leftmost 0 in Bᵢ

Estimate: (2^(R₁) + ... + 2^(Rₘ)) / (m × φ)
```

**Key Properties**:
- **Stochastic averaging**: Using m bitmaps reduces variance
- **Hash independence**: Two different hash functions prevent correlation

#### Analysis

**Space**: m × L bits = m × O(log log n) bits
- For n = 1 billion, m = 64: ~640 bytes

**Accuracy**: Standard error ≈ 0.78/√m
- With m = 64: error ≈ 10%
- With m = 256: error ≈ 5%

**Time per element**: O(1) hash computations and bitmap updates

**Comparison to exact**:
- Exact: O(n) space to store all distinct elements
- PCSA: O(log log n) space with ~5-10% error

### 3. LogLog Counter

#### Motivation

**PCSA limitations**: Uses bitmaps, still O(log n) bits per bitmap

**Goal**: Reduce to truly O(log log n) bits per register

#### The Algorithm

**Key Innovation**: Instead of bitmap, store only the maximum r value seen!

**Structure**:
- m registers: R₁, R₂, ..., Rₘ
- Each register stores max r value (needs only log log n bits)

**Algorithm**:
```
Initialize: R₁, ..., Rₘ = 0

For each element x:
    i = hash₁(x) mod m           // which register?
    h = hash₂(x)                 // pattern
    r = position of leftmost 1-bit in h
    Rᵢ = max(Rᵢ, r)             // update maximum

Estimate: α_m × m × 2^(average of all Rᵢ)
```

Where α_m is a bias correction constant (≈ 0.39 for large m).

**Example**:
```
m = 4 registers
hash("alice") → register 2, r=3  →  R₂ = max(0,3) = 3
hash("bob")   → register 1, r=1  →  R₁ = max(0,1) = 1
hash("carol") → register 2, r=5  →  R₂ = max(3,5) = 5
hash("dave")  → register 3, r=2  →  R₃ = max(0,2) = 2

Registers: R₁=1, R₂=5, R₃=2, R₄=0
Average: (1+5+2+0)/4 = 2
Estimate: α₄ × 4 × 2^2 ≈ 6.2
```

#### Analysis

**Space**: m × log log n bits
- For n = 1 billion, m = 64, each register needs 5 bits = 320 bits = 40 bytes!
- Compare to exact: need to store up to 1B elements

**Accuracy**: Standard error ≈ 1.30/√m
- With m = 64: error ≈ 16%
- Slightly worse than PCSA but much less space

**Key Advantage**: Truly O(log log n) per register vs O(log n) for PCSA bitmaps

### 4. HyperLogLog Counter

#### The Innovation

**Problem with LogLog**: Taking average of exponentials is biased

**Solution**: Use **harmonic mean** instead of arithmetic mean!

#### The Algorithm

**Harmonic mean formula**:
```
HarmonicMean = m / (1/a₁ + 1/a₂ + ... + 1/aₘ)
             = m / Σ(1/aᵢ)
```

**HyperLogLog Algorithm**:
```
Initialize: R₁, ..., Rₘ = 0

For each element x:
    i = first p bits of hash(x)      // which register? (m = 2^p)
    remaining = rest of hash(x)       // pattern
    r = position of leftmost 1-bit in remaining + 1
    Rᵢ = max(Rᵢ, r)

Estimate: α_m × m² / Σ(2^(-Rᵢ))
```

**Key differences from LogLog**:
1. Use harmonic mean (dividing by sum of 2^(-Rᵢ))
2. Better bias correction with α_m
3. Small and large range corrections

**Bias Correction**:
- Small range (E < 2.5m): Use linear counting
- Large range (E > 2³²/30): Apply correction for hash collisions
- Medium range: Use raw estimate

#### Analysis

**Space**: m × log log n bits (same as LogLog)
- Typical: m = 2^14 = 16384 registers, 6 bits each = 12KB

**Accuracy**: Standard error ≈ 1.04/√m
- With m = 16384: error ≈ 0.81%!
- Better than LogLog (1.30/√m)
- Close to optimal (1/√m)

**Why harmonic mean?**
- Reduces impact of outlier large values
- Harmonic mean ≤ arithmetic mean
- More robust estimator for this problem

**Performance**:
- Time: O(1) per element
- Space: 12KB for 0.81% error regardless of n!
- Can count billions or trillions with same space

#### HyperLogLog++ (Google's Variant)

**Improvements**:
1. **Bias correction**: Empirical bias tables for small cardinalities
2. **Sparse representation**: Use sparse structure for small cardinalities
3. **Better hash function**: 64-bit hash for very large cardinalities

**Result**: Best practical cardinality estimator
- Used in Google BigQuery, Redis, Presto
- Can estimate cardinalities up to 2^64

### Comparison of Counting Methods

| Method | Space | Relative Error | Year | Notes |
|--------|-------|----------------|------|-------|
| Exact | O(n) | 0% | - | Store all distinct elements |
| Morris | O(log log n) | ~71% | 1978 | Simple counter |
| Morris+ (m counters) | m·log log n | ~1/√(2m) | - | Average m counters |
| PCSA | m·log n | ~0.78/√m | 1985 | Uses bitmaps |
| LogLog | m·log log n | ~1.30/√m | 2003 | Max per register |
| HyperLogLog | m·log log n | ~1.04/√m | 2007 | Harmonic mean |
| HyperLogLog++ | m·log log n | ~1.04/√m | 2013 | Bias correction |

**Example (n = 1 billion, target 1% error)**:
- Exact: 4-8 GB (storing 32-64 bit integers)
- HyperLogLog: 12 KB (m = 16384)
- Space reduction: ~500,000×!

---

## AMQ Filters - Introduction {#amq-introduction}

### What are AMQ Filters?

**AMQ** = **Approximate Membership Query**

**Definition**: Data structure supporting:
- **Insert(x)**: Add element x to the set
- **Query(x)**: Is x in the set?

**Approximation**:
- ✓ No false negatives (if x is in set, always return TRUE)
- ✗ Allow false positives (may return TRUE for x not in set)

**Trade-off**: Accept small error rate for massive space savings

### The Space Lower Bound

**Fundamental result**: Any AMQ filter with false positive rate ε requires:
```
Space ≥ n × log₂(1/ε) bits
```

**Example**: For n = 1M elements, ε = 1%:
```
Space ≥ 1M × log₂(100) ≈ 1M × 6.64 bits ≈ 830 KB
```

This is the **theoretical minimum** for any AMQ filter!

**Compare to exact**:
- Storing 1M 64-bit elements: 8 MB
- AMQ lower bound: 830 KB
- Space reduction: ~10×

### Types of AMQ Filters

1. **Bloom Filter**: Classic, simple, cache-unfriendly
2. **Counting Bloom Filter**: Supports deletions
3. **Quotient Filter**: Cache-friendly, supports deletions
4. **Cuckoo Filter**: Better performance, supports deletions
5. **Bloom Filter variants**: Compressed, Spectral, Scalable, etc.

We'll explore each in detail!

---

## Bloom Filters {#bloom-filters}

### Structure and Operations

#### Data Structure

**Components**:
- Bit array B of size m (all bits initially 0)
- k independent hash functions: h₁, h₂, ..., h_k
- Hash functions map elements to [0, m-1]

```
B: [0][0][0][0][0][0][0][0][0][0][0][0][0][0][0][0]
    0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
```

#### Insert Operation

```
Insert(x):
    for i = 1 to k:
        B[hᵢ(x)] = 1
```

Set k bits corresponding to k hash values.

**Example** (m=16, k=3):
```
Insert("cat"):
    h₁("cat") = 2  → B[2] = 1
    h₂("cat") = 7  → B[7] = 1
    h₃("cat") = 12 → B[12] = 1

B: [0][0][1][0][0][0][0][1][0][0][0][0][1][0][0][0]
```

#### Query Operation

```
Query(x):
    for i = 1 to k:
        if B[hᵢ(x)] == 0:
            return FALSE  // definitely not in set
    return TRUE           // probably in set
```

Check if all k bits are set.

**Example**:
```
Query("cat"):
    Check B[2]=1, B[7]=1, B[12]=1 → all set → return TRUE ✓

Query("dog"):
    Check B[5]=0 → return FALSE ✓ (definitely not inserted)

Query("bird"):
    h₁("bird")=2, h₂("bird")=7, h₃("bird")=14
    Check B[2]=1, B[7]=1, B[14]=0 → return FALSE ✓
```

#### False Positive Example

```
After inserting "cat" and "dog":
B: [0][0][1][0][0][1][0][1][0][0][0][0][1][0][1][0]

Query("fox"):
    h₁("fox") = 2  → B[2] = 1 ✓
    h₂("fox") = 7  → B[7] = 1 ✓
    h₃("fox") = 12 → B[12] = 1 ✓
    All set → return TRUE ✗ (false positive!)
```

The bits set by other elements cause false positive.

### Analysis

#### False Positive Probability

After inserting n elements:

**Probability a specific bit is still 0**:
```
P(bit is 0) = (1 - 1/m)^(kn) ≈ e^(-kn/m)
```

**Probability a specific bit is 1**:
```
P(bit is 1) = 1 - e^(-kn/m)
```

**False positive probability** (all k bits are 1 for non-member):
```
ε = (1 - e^(-kn/m))^k
```

Let α = n/m (load factor):
```
ε ≈ (1 - e^(-kα))^k
```

#### Optimal Number of Hash Functions

**Goal**: Minimize ε for given m and n

Taking derivative and setting to 0:
```
k* = (m/n) ln 2 ≈ 0.693 (m/n)
```

**Intuition**: k should be proportional to bits per element!

With optimal k:
```
ε = (1/2)^k = (1/2)^((m/n)ln 2) = (0.6185)^(m/n)
```

**Alternative form**:
```
m/n = -log₂(ε) / ln 2 ≈ 1.44 log₂(1/ε)
```

#### Space Analysis

For false positive rate ε:
```
m = -n ln(ε) / (ln 2)² ≈ 1.44 n log₂(1/ε) bits
```

**Examples**:

| n | ε | k* | m (bits) | m/n | Size |
|---|---|----|----------|-----|------|
| 1M | 1% | 7 | 9.6 Mb | 9.6 bits | 1.2 MB |
| 1M | 0.1% | 10 | 14.4 Mb | 14.4 bits | 1.8 MB |
| 1M | 0.01% | 13 | 19.2 Mb | 19.2 bits | 2.4 MB |
| 1B | 1% | 7 | 9.6 Gb | 9.6 bits | 1.2 GB |

**Key Insight**: Space is independent of element size! Only depends on n and ε.

**Compare to hash table**:
- 1M 64-bit elements: 8 MB
- Bloom filter (1% FP): 1.2 MB
- Space savings: ~6.7×

### Practical Considerations

#### Hash Function Implementation

**Challenge**: Need k independent hash functions

**Solution 1**: Use k different hash functions (expensive)

**Solution 2**: Double hashing (Kirsch-Mitzenmacher 2006)
```
hᵢ(x) = (h₁(x) + i × h₂(x)) mod m
```
Only need 2 hash functions to generate k!

**Solution 3**: Enhanced double hashing
```
hᵢ(x) = (h₁(x) + i × h₂(x) + i²) mod m
```

#### Insertion Without Resizing

**Problem**: Fixed size m means ε increases as n grows

**Solution 1**: Oversize initially
- Allocate for expected maximum n
- Waste space if actual n is smaller

**Solution 2**: Scalable Bloom Filters
- Create new Bloom filter when full
- Query all filters (more on this later)

#### Deletions Not Supported

**Problem**: Can't delete by unsetting bits - would affect other elements!

**Example**:
```
Insert("cat") → B[2]=1, B[7]=1, B[12]=1
Insert("dog") → B[2]=1, B[5]=1, B[7]=1  (overlaps at 2,7)

Delete("cat") by unsetting B[2], B[7], B[12]?
→ Would break "dog" query! (B[2] and B[7] needed for "dog")
```

**Solutions**:
1. Don't support deletions (original Bloom filter)
2. Use Counting Bloom Filter (next section)
3. Use Quotient or Cuckoo filters

### Bloom Filter Variants

#### 1. Counting Bloom Filter

**Idea**: Replace bits with counters

**Structure**:
- Array of c-bit counters (typically c=4)
- Increment on insert, decrement on delete

```
Insert(x):
    for i = 1 to k:
        Counter[hᵢ(x)]++

Delete(x):
    for i = 1 to k:
        Counter[hᵢ(x)]--

Query(x):
    for i = 1 to k:
        if Counter[hᵢ(x)] == 0:
            return FALSE
    return TRUE
```

**Space cost**: c × m bits (typically 4× standard Bloom filter)

**Counter overflow**: With 4-bit counters (max 15), overflow is rare in practice

#### 2. Compressed Bloom Filter

**Use case**: Send Bloom filter over network

**Idea**: Compress the bit array
- Many zeros → good compression ratio
- Optimal encoding (arithmetic coding)

**Space**: Can achieve near-optimal n log₂(1/ε) bits

**Trade-off**: Compression/decompression time

#### 3. Scalable Bloom Filter

**Problem**: Fixed-size Bloom filter degrades as n increases

**Solution**: Chain of Bloom filters with increasing sizes

**Structure**:
- Filters F₁, F₂, F₃, ... with error rates ε₁, ε₂, ε₃, ...
- Set ε_i = ε₀ × r^i where r < 1 (e.g., r = 0.5)

```
Insert(x):
    Insert into current filter
    If current filter full:
        Create next filter (double size, halve error rate)

Query(x):
    Check all filters (return TRUE if any returns TRUE)
```

**Total error rate**:
```
ε_total = ε₀(1 + r + r² + ...) = ε₀/(1-r)
```

With r=0.5: ε_total = 2ε₀

**Advantage**: Adapts to growing n without knowing it in advance

#### 4. Spectral Bloom Filter

**Extension**: Estimate element frequency (not just membership)

**Use counters** to approximate count for each element

**Applications**: Heavy hitters, frequency estimation

---

## Advanced AMQ Filters {#advanced-amq-filters}

### 1. Quotient Filter

#### Motivation

**Bloom filter limitations**:
1. Not cache-friendly (k random memory accesses)
2. No deletion support
3. Doesn't cluster related queries

**Quotient filter advantages**:
1. Better cache performance
2. Supports deletions
3. Can be merged
4. Can be resized

#### Structure

**Key idea**: Store fingerprints in hash table with remainder-quotient encoding

**Hash function decomposition**:
```
h(x) = quotient | remainder
       ← q bits →  ← r bits →
```

- **Quotient**: Table index (position)
- **Remainder**: Fingerprint stored at position

**Example** (q=4, r=4):
```
h("cat") = 01101001
Quotient = 0110 = 6 (position)
Remainder = 1001 = 9 (fingerprint)
```

**Table structure**:
- Size 2^q slots
- Each slot stores:
  - r-bit remainder
  - 3 metadata bits: is_occupied, is_continuation, is_shifted

#### Operations

**Insert(x)**:
1. Compute h(x), extract quotient q and remainder r
2. If slot q is empty, store r there
3. If slot q is occupied, insert r in run for q (may shift elements)

**Query(x)**:
1. Compute h(x), extract quotient q and remainder r
2. Find run for quotient q
3. Check if remainder r is in the run

**Delete(x)**:
1. Find fingerprint in table
2. Remove it and shift elements back

#### Run Organization

**Run**: Sequence of remainders with same quotient

**Challenge**: Runs can overflow to next slots (linear probing)

**Metadata bits**:
- **is_occupied**: Indicates quotient has elements
- **is_continuation**: Part of multi-element run
- **is_shifted**: Element displaced from home position

**Example**:
```
Quotient q=3 has 3 elements → run might be at positions 5,6,7
Use metadata to track start and end of runs
```

#### Analysis

**Space**: (r + 3) bits per slot, load factor α < 1
- For n elements: m = n/α slots
- Total: n(r+3)/α bits

**False positive rate**:
```
ε ≈ 1/2^r
```
(probability random element has matching remainder)

**Example**: r=8 gives ε ≈ 0.4%

**Time complexity**:
- Insert: O(1) expected
- Query: O(1) expected (with good load factor)
- Delete: O(1) expected

**Cache performance**:
- Runs stored contiguously → better locality
- Query typically accesses 1-2 cache lines

#### Comparison to Bloom Filter

**Advantages**:
- Deletions supported
- Better cache performance
- Can be merged efficiently
- Can be resized

**Disadvantages**:
- More complex implementation
- Higher space for same error rate (metadata overhead)
- Performance degrades with high load factor

### 2. Cuckoo Filter

#### Motivation

**Goals**: Combine best of Bloom and Quotient filters
1. Support deletions
2. Better cache performance than Bloom filter
3. Simpler than Quotient filter
4. Better space efficiency

#### Structure

**Key components**:
- Hash table with b buckets
- Each bucket holds k entries (typically k=4)
- Each entry stores r-bit fingerprint

**Total space**: b × k slots

**Two hash functions**:
```
h₁(x) = hash(x)
h₂(x) = h₁(x) ⊕ hash(fingerprint(x))
```

**Key property**: Given one position and fingerprint, can compute other position:
```
h₂(x) = h₁(x) ⊕ hash(f)
h₁(x) = h₂(x) ⊕ hash(f)
```

This is crucial for deletions!

#### Operations

**Insert(x)**:
1. Compute fingerprint f = fingerprint(x)
2. Compute h₁ = hash(x)
3. Compute h₂ = h₁ ⊕ hash(f)
4. If bucket h₁ or h₂ has empty slot, insert f
5. Otherwise, evict random entry and reinsert (cuckoo hashing)

**Cuckoo insertion with eviction**:
```
Insert(x):
    f = fingerprint(x)
    i = h₁(x)
    for attempt = 1 to MaxAttempts:
        if bucket[i] has empty slot:
            insert f into bucket[i]
            return SUCCESS
        else:
            randomly pick entry j from bucket[i]
            swap f with bucket[i][j]  // evict and insert
            i = i ⊕ hash(f)           // compute alternate location
    return FAILURE  // filter is full, need to rebuild
```

**Query(x)**:
```
Query(x):
    f = fingerprint(x)
    i₁ = h₁(x)
    i₂ = i₁ ⊕ hash(f)
    return (f in bucket[i₁]) OR (f in bucket[i₂])
```

Check both possible locations.

**Delete(x)**:
```
Delete(x):
    f = fingerprint(x)
    i₁ = h₁(x)
    i₂ = i₁ ⊕ hash(f)
    if f in bucket[i₁]:
        remove f from bucket[i₁]
        return SUCCESS
    else if f in bucket[i₂]:
        remove f from bucket[i₂]
        return SUCCESS
    return FAILURE  // not found
```

#### Analysis

**Load factor**: Can achieve α ≈ 95% with k=4 entries per bucket

**False positive rate**:
```
ε ≈ 2k/2^r
```

For r=8, k=4: ε ≈ 3.1%

**Space per element**:
```
Space = (r + ε) / α bits per element
```

Where ε accounts for empty slots.

**Example** (r=8, k=4, α=95%):
- Space per element ≈ 8.5 bits
- Compare to Bloom filter with same FP rate: ~9-10 bits
- **Cuckoo filter is more space-efficient!**

**Time complexity**:
- Query: O(k) = O(1) (check 2k slots)
- Insert: O(1) expected (with cuckoo hashing)
- Delete: O(k) = O(1)

#### Advantages over Bloom Filter

1. **Deletions supported**: Can remove fingerprints
2. **Better lookup performance**: Check only 2 buckets (2k slots) vs k random locations
3. **Better cache performance**: 2 cache lines vs k cache lines
4. **Better space**: For high false positive rates (ε > 3%)

#### Limitations

1. **False positives still exist**: From fingerprint collisions
2. **Need rebuilding**: If insert fails after max attempts
3. **Requires careful parameter tuning**: Bucket size k, fingerprint size r

### 3. Xor Filter

#### The Innovation (2019)

**Xor filter**: Even better space efficiency than Cuckoo filter!

**Key idea**:
- Use 3 hash functions h₁, h₂, h₃
- Store fingerprints such that: f(x) = T[h₁(x)] ⊕ T[h₂(x)] ⊕ T[h₃(x)]

**Space**: Can achieve ε ≈ 0.4% with only 9.84 bits per element
- Compare to theoretical optimum: 9.5 bits
- Only 3.5% overhead!

**Trade-off**:
- Cannot support deletions (static structure)
- Construction is more complex

**Use case**: Static sets where space is critical

### Comparison of AMQ Filters

| Filter | Space/elem | FP rate | Insert | Query | Delete | Cache | Merge |
|--------|-----------|---------|--------|-------|--------|-------|-------|
| Bloom | 9.6 bits | 1% | O(k) | O(k) | ✗ | Poor | ✗ |
| Counting Bloom | 38.4 bits | 1% | O(k) | O(k) | ✓ | Poor | ✗ |
| Quotient | 10-12 bits | 1% | O(1) | O(1) | ✓ | Good | ✓ |
| Cuckoo | 8-10 bits | 1% | O(1) | O(1) | ✓ | Better | ✗ |
| Xor | 9.84 bits | 0.4% | O(n) | O(1) | ✗ | Good | ✗ |

**Guidelines**:
- **Static set, optimize space**: Xor filter
- **Need deletions**: Cuckoo or Quotient filter
- **Simplicity**: Bloom filter
- **Cache performance critical**: Cuckoo or Quotient filter
- **Need merging**: Quotient filter

---

## Analysis and Comparison {#analysis-comparison}

### Theoretical Bounds

#### Information-Theoretic Lower Bound

For n elements with false positive rate ε:
```
Space ≥ n log₂(1/ε) bits
```

**Proof intuition**:
- Need to distinguish n elements from non-members
- Each element needs log₂(1/ε) bits to achieve error rate ε
- Cannot do better without additional assumptions

**Example** (n=1M, ε=1%):
```
Lower bound = 1M × log₂(100) ≈ 6.64M bits ≈ 830 KB
```

#### Practical Performance

Bloom filter achieves:
```
Space = n × 1.44 log₂(1/ε) bits ≈ 1.44 × lower bound
```

Only 44% overhead! Remarkably close to optimal.

### Space-Time Trade-offs

#### Bloom Filter Variants

**Standard Bloom**:
- Space: 1.44n log₂(1/ε)
- Query: k hash computations, k memory accesses
- k ≈ 0.7(m/n) ≈ log₂(1/ε)

**Blocked Bloom** (cache optimization):
- Divide into b blocks, hash selects block
- Query accesses only one block (one cache line)
- Slightly worse FP rate for same space

**Partitioned Bloom**:
- Divide bit array into k partitions
- Hash i uses partition i
- Worse FP rate but better cache performance

#### Cuckoo Filter Trade-offs

**Bucket size k**:
- Larger k → better load factor → less space
- Smaller k → faster queries
- Typical: k=4 (good compromise)

**Fingerprint size r**:
- Larger r → lower false positive rate
- Smaller r → less space
- Must have r ≥ log₂(2n/k) for good load factor

### Choosing the Right Structure

#### Decision Tree

```
Do you need deletions?
├─ No
│  ├─ Static set → Xor filter (best space)
│  └─ Dynamic → Bloom filter (simplest)
└─ Yes
   ├─ Cache performance critical?
   │  ├─ Yes → Cuckoo filter
   │  └─ No → Counting Bloom filter
   └─ Need merging? → Quotient filter
```

#### Application-Specific Considerations

**Web caching**:
- Bloom filter: Simple, effective
- False positives → extra fetch (acceptable)

**Databases**:
- Bloom filters on SSTables (LSM trees)
- Avoid disk reads for non-existent keys
- Used in: RocksDB, Cassandra, HBase

**Networks**:
- Bloom filters for route summarization
- Cuckoo filters in switches (cache-friendly)

**Spell checking**:
- Bloom filter for dictionary
- False positives → check full dictionary

**Distributed systems**:
- Quotient filters (mergeable)
- Synchronize filters across nodes

**Real-time analytics**:
- HyperLogLog for cardinality
- Count-Min sketch for frequencies
- Bloom filter for membership

---

## Applications {#applications}

### 1. Database Systems

#### LSM Trees (Log-Structured Merge Trees)

**Problem**: Frequent lookups in write-optimized storage

**Structure**:
- Multiple levels of SSTables (sorted string tables)
- Each SSTable is on disk

**Challenge**: Checking if key exists requires reading disk

**Solution**: Bloom filter per SSTable
```
Lookup(key):
    for each SSTable:
        if BloomFilter.Query(key) == FALSE:
            skip this SSTable  // definitely not here
        else:
            read SSTable from disk  // might be here
```

**Impact**:
- Eliminates ~99% of disk reads for non-existent keys
- Used in: LevelDB, RocksDB, Cassandra, HBase, ScyllaDB

**Space**: 10 bits per key (1% FP rate) → small overhead

#### Query Optimization

**Problem**: Expensive joins in distributed databases

**Solution**: Send Bloom filters to reduce data transfer
```
Node A: Build Bloom filter for join column
Node B: Filter rows using Bloom filter before sending
Result: Only send potentially matching rows
```

**Savings**: 90%+ reduction in network transfer for selective joins

### 2. Web Systems

#### Web Caching

**Problem**: Check if URL in cache without full lookup

**Solution**: Bloom filter as cache index
```
Fetch(url):
    if BloomFilter.Query(url) == FALSE:
        fetch from origin  // definitely not in cache
    else:
        check cache       // might be in cache
        if not in cache:  // false positive
            fetch from origin
```

**Benefits**:
- Avoid cache lookup for uncached URLs
- Small memory overhead (MB vs GB cache)

**Used by**: Squid, Varnish, CDNs

#### Malicious URL Detection

**Problem**: Check if URL is in blacklist (billions of URLs)

**Solution**: Bloom filter for blacklist
```
CheckURL(url):
    if BloomFilter.Query(url) == TRUE:
        return SUSPICIOUS  // might be malicious
    else:
        return SAFE       // definitely safe
```

**False positives**: Block safe URL (rare, acceptable)
**False negatives**: None (all malicious URLs caught)

**Used by**: Chrome Safe Browsing (used Bloom filters initially)

### 3. Network Systems

#### Route Summarization

**Problem**: Routers need compact route information

**Solution**: Bloom filters to summarize routes
- Instead of sending full routing table, send Bloom filter
- Query locally to determine if route might exist

**Trade-off**: False positives → extra routing hops

#### P2P Systems

**Problem**: Check which peers have which files

**Solution**: Each peer maintains Bloom filter of files
- Share filters with neighbors (small)
- Query filter before requesting file

**Examples**: BitTorrent, distributed hash tables

#### DDoS Mitigation

**Problem**: Detect repeated malicious IPs efficiently

**Solution**: Count-Min sketch or Counting Bloom filter
- Track IP access counts
- Identify high-frequency IPs (potential attackers)

### 4. Streaming and Big Data

#### Distinct Counting (HyperLogLog)

**Google**: Count unique search queries per day
- HyperLogLog: 1.5 KB per counter
- Can count billions with <1% error
- Used in: BigQuery, Analytics

**Redis**: PFADD and PFCOUNT commands
- HyperLogLog-based cardinality estimation
- 12 KB per key regardless of cardinality

**Twitter**: Count unique users per hashtag
- Real-time cardinality estimation
- Merge HyperLogLog across time windows

#### Real-Time Analytics

**Problem**: Track metrics for millions of entities

**Example - Web Analytics**:
```
Metric: Unique visitors per page
Store: HyperLogLog per page ID
Space: 12 KB per page (vs GB to store all visitor IDs)
```

**Example - IoT**:
```
Metric: Unique devices per sensor
Store: HyperLogLog per sensor
Merge: Combine HyperLogLog for sensor groups
```

### 5. Bioinformatics

#### Sequence Matching

**Problem**: Check if DNA k-mer seen before (billions of k-mers)

**Solution**: Bloom filter for k-mer presence
- 10-20 bits per k-mer vs 64+ bits to store
- False positives acceptable (verify with full check)

**Applications**:
- Genome assembly
- Read error correction
- Variant calling

**Examples**: Minia, Squeakr, Bifrost (genome assemblers)

### 6. Security and Privacy

#### Password Breach Detection

**Problem**: Check if password in breach database (billions of passwords)

**Solution**: Bloom filter of breached passwords
- Client downloads small filter
- Check locally without sending password
- False positives → warn user (safe side)

**Example**: haveibeenpwned.org uses Bloom filters

#### Privacy-Preserving Protocols

**Problem**: Set intersection without revealing sets

**Solution**: Exchange Bloom filters
- Compute approximate intersection
- No need to share actual elements

**Applications**: Private contact discovery, ad targeting

---

## Problem-Solving Framework {#problem-solving}

### When to Use Probabilistic Counters

#### Scenario Analysis

**Use probabilistic counters when**:
1. **Space is constrained**: Limited memory, cache, or bandwidth
2. **Exact count not critical**: Approximate sufficient (analytics, monitoring)
3. **Streaming data**: Cannot store all elements
4. **Scale is large**: Billions of elements or events
5. **Real-time requirement**: Must process fast

**Use exact counting when**:
1. **Accuracy critical**: Financial, legal, safety-critical systems
2. **Small scale**: Exact counting is cheap enough
3. **Debugging**: Need precise counts for troubleshooting

#### Choosing the Right Counter

| Scenario | Algorithm | Why |
|----------|-----------|-----|
| Count events (simple) | Morris Counter | Simplest, O(log log n) bits |
| Count events (accurate) | Morris+ (multiple) | Better accuracy with averaging |
| Count distinct elements | HyperLogLog | Best accuracy/space trade-off |
| Count distinct + merge | HyperLogLog | Supports merging |
| Very large cardinalities | HyperLogLog++ | Bias correction, up to 2^64 |
| Frequencies (not just counts) | Count-Min Sketch | Estimates per-element frequency |

### When to Use AMQ Filters

#### Scenario Analysis

**Use AMQ filters when**:
1. **Space critical**: Cannot store full elements
2. **False positives acceptable**: Can handle occasional errors
3. **Negative queries common**: Often checking non-members
4. **Element size large**: URLs, documents (space savings higher)
5. **Network transfer**: Compact representation for communication

**Use exact structures when**:
1. **False positives costly**: Critical to avoid errors
2. **Element size small**: Integers (AMQ overhead comparable)
3. **Updates frequent**: Deletions needed (unless using Cuckoo/Quotient)
4. **Small scale**: Hash table is affordable

#### Choosing the Right Filter

| Scenario | Filter | Why |
|----------|--------|-----|
| Simple membership, no deletes | Bloom Filter | Simplest, well-tested |
| Need deletions | Cuckoo Filter | Good performance + deletions |
| Cache performance critical | Quotient/Cuckoo | Better locality |
| Need merging | Quotient Filter | Only one that supports merging |
| Static set, optimize space | Xor Filter | Near-optimal space |
| Count frequencies | Count-Min Sketch | Frequency estimation |

### Design Process

#### Step 1: Define Requirements

```
Requirements Checklist:
□ What are we counting/checking?
□ How many elements (n)?
□ Acceptable error rate (ε)?
□ Need deletions?
□ Space constraints?
□ Latency requirements?
□ Static or dynamic?
```

#### Step 2: Calculate Space Budget

**For counters**:
```
HyperLogLog: m = (1.04/ε)² registers
Space = m × log log n bits
```

**For AMQ filters**:
```
Bloom: m = 1.44 n log₂(1/ε) bits
Cuckoo: m ≈ 1.05 n log₂(1/ε) bits (better)
```

**Example** (n=1M, ε=1%):
- HyperLogLog: 10,816 registers × 6 bits ≈ 8 KB
- Bloom: 1.2 MB
- Cuckoo: 1.0 MB

#### Step 3: Validate Performance

**Query throughput**:
- Bloom: k hash + k memory access
- Cuckoo: 2 hash + 2 bucket reads (typically faster)
- Quotient: 1 hash + few sequential reads

**Cache misses**:
- Bloom: Up to k cache misses
- Cuckoo: Up to 2 cache misses
- Quotient: Typically 1-2 cache misses

**Insert throughput**:
- Bloom: Same as query
- Cuckoo: May need evictions (occasional spike)

#### Step 4: Consider Trade-offs

**Space vs Accuracy**:
```
ε = 1%   → 9.6 bits/element
ε = 0.1% → 14.4 bits/element
ε = 0.01% → 19.2 bits/element
```

**Space vs Operations**:
- Standard Bloom: 9.6 bits, k≈7 ops
- Blocked Bloom: 11 bits, 1 cache line
- Trade 15% space for better locality

### Common Pitfalls

#### 1. Underestimating Growth

**Problem**: Set size exceeds capacity
```
Initial: n = 1M, ε = 1%
Actual: n = 10M, ε → 50%+ (filter saturated)
```

**Solutions**:
- Oversize initially (2-3× expected)
- Use Scalable Bloom Filter
- Monitor load factor, rebuild when needed

#### 2. Hash Function Quality

**Problem**: Poor hash function causes clustering
- Real false positive rate >> theoretical
- Performance degradation

**Solutions**:
- Use cryptographic hash (SHA, MurmurHash)
- Test hash distribution in practice
- Use double hashing carefully (need independence)

#### 3. Ignoring Cache Effects

**Problem**: Theoretical analysis assumes O(1) memory access
- Reality: Cache misses dominate

**Impact**:
```
Bloom (k=7): 7 random accesses → 7 cache misses
Cuckoo (k=4): 2 buckets → 2 cache misses
Speedup: 3-4× in practice
```

**Solutions**:
- Consider cache-optimized variants
- Measure real performance, not just complexity

#### 4. False Positive Cascades

**Problem**: Chaining probabilistic structures
```
Filter 1: ε₁ = 1%
Filter 2: ε₂ = 1%
Combined: ε ≈ ε₁ + ε₂ = 2%
```

Multiple filters compound errors!

**Solutions**:
- Account for cascading errors
- Use tighter error rates in pipeline
- Verify with exact check at end

---

## Complexity Cheat Sheet {#complexity-cheat-sheet}

### Probabilistic Counters

| Algorithm | Space (bits) | Relative Error | Update | Query | Merge |
|-----------|--------------|----------------|--------|-------|-------|
| Exact | log n | 0% | O(1) | O(1) | O(1) |
| Morris | log log n | ~71% | O(1) | O(1) | - |
| Morris+ (m) | m·log log n | ~1/√(2m) | O(m) | O(m) | - |
| PCSA | m·log n | ~0.78/√m | O(1) | O(m) | ✓ |
| LogLog | m·log log n | ~1.30/√m | O(1) | O(m) | ✓ |
| HyperLogLog | m·log log n | ~1.04/√m | O(1) | O(m) | ✓ |

**Typical values** (n = 10⁹, target 1% error):
- Exact: 30 bits
- HyperLogLog: m=10,816, space=8KB (2,700× saving)

### AMQ Filters

| Filter | Space/elem | FP Rate | Insert | Query | Delete | Merge |
|--------|-----------|---------|--------|-------|--------|-------|
| Hash Table | 64+ bits | 0% | O(1) | O(1) | ✓ | - |
| Bloom | ~10 bits | 1% | O(k) | O(k) | ✗ | ✗ |
| Counting Bloom | ~40 bits | 1% | O(k) | O(k) | ✓ | ✗ |
| Quotient | ~12 bits | 1% | O(1) | O(1) | ✓ | ✓ |
| Cuckoo | ~9 bits | 1% | O(1)* | O(1) | ✓ | ✗ |
| Xor | ~10 bits | 0.4% | O(n) | O(1) | ✗ | ✗ |

*Expected, may need rebuilding

**Space formula** (1% FP rate):
- Theoretical minimum: 6.64 bits/element
- Bloom filter: 9.6 bits/element (1.44× optimal)
- Cuckoo filter: ~8.5 bits/element (best practical)

### Parameter Selection

#### HyperLogLog

For target error ε:
```
m = (1.04/ε)² registers
Space = m × log₂(log₂(n)) bits
```

**Examples**:
- ε=1%: m=10,816, space≈8KB (for any n up to 2^64)
- ε=0.5%: m=43,264, space≈32KB

#### Bloom Filter

For false positive rate ε:
```
k = log₂(1/ε) hash functions
m = 1.44 × n × k bits
```

**Examples** (per million elements):
| ε | k | Space | Compare to Exact (64-bit) |
|---|---|-------|---------------------------|
| 10% | 3.3 | 0.5 MB | 8 MB (16× saving) |
| 1% | 6.6 | 1.2 MB | 8 MB (6.7× saving) |
| 0.1% | 10 | 1.8 MB | 8 MB (4.4× saving) |

#### Cuckoo Filter

For false positive rate ε and bucket size k:
```
r = ⌈log₂(1/ε) + log₂(2k)⌉ fingerprint bits
Load factor α ≈ 0.95 (for k=4)
Space ≈ r/α bits per element
```

**Example** (ε=1%, k=4):
- r=8 bits
- Space≈8.5 bits/element

---

## Summary and Final Tips {#summary}

### Key Takeaways

#### Probabilistic Counters

**Why they matter**:
- O(log log n) space instead of O(log n)
- Can count to billions with few KB
- Essential for streaming/big data

**Algorithm progression**:
1. Morris (1978): Simple but high variance
2. PCSA (1985): Multiple counters reduce variance
3. LogLog (2003): True O(log log n) per register
4. HyperLogLog (2007): Harmonic mean for best accuracy
5. HyperLogLog++ (2013): Production-ready with bias correction

**Practical winner**: HyperLogLog
- 1% error with ~8KB (for any cardinality up to 2^64!)
- Used in Redis, Presto, BigQuery, Druid

#### AMQ Filters

**Why they matter**:
- ~10 bits/element vs 64+ bits (hash table)
- Near-optimal space (1.44× theoretical minimum)
- Enable handling billions of elements

**Filter progression**:
1. Bloom (1970): Classic, simple, effective
2. Counting Bloom (1998): Support deletions
3. Quotient (2012): Cache-friendly, mergeable
4. Cuckoo (2014): Better performance + deletions
5. Xor (2019): Near-optimal space (static only)

**Practical winners**:
- General use: Bloom filter (battle-tested)
- Need deletions: Cuckoo filter (best performance)
- Optimize space: Xor filter (static sets only)

### Decision Framework

```
┌─── Need Counting? ────────────────────────────────────┐
│                                                        │
│  Simple counter? → Morris Counter                     │
│  Distinct elements? → HyperLogLog                     │
│  Need merging? → HyperLogLog (supports union)         │
│                                                        │
└────────────────────────────────────────────────────────┘

┌─── Need Membership Testing? ──────────────────────────┐
│                                                        │
│  Static set? → Bloom or Xor Filter                    │
│  Need deletions? → Cuckoo or Quotient Filter          │
│  Need merging? → Quotient Filter (only option)        │
│  Cache-critical? → Cuckoo or Quotient                 │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### Study Tips

1. **Understand the space savings**:
   - Counter: log log n vs log n
   - Filter: ~10 bits vs 64+ bits
   - These are exponential savings!

2. **Master the analysis**:
   - Bloom filter FP rate: (1 - e^(-kn/m))^k
   - Optimal k: (m/n) ln 2
   - HyperLogLog error: 1.04/√m

3. **Know the trade-offs**:
   - Space vs accuracy (tunable with parameters)
   - Simplicity vs features (deletions, merging)
   - Theory vs practice (cache effects matter!)

4. **Practice calculations**:
   - Given n and ε, compute m and k
   - Given space budget, find achievable ε
   - Compare exact vs approximate space

5. **Understand applications**:
   - Databases: Bloom filters in LSM trees
   - Web: Caching, malicious URL detection
   - Analytics: HyperLogLog for cardinality
   - Networks: Route summarization

### Common Exam Topics

1. **Bloom filter analysis**:
   - Derive FP probability
   - Compute optimal k
   - Calculate space for given ε

2. **HyperLogLog mechanics**:
   - Why harmonic mean?
   - Space complexity: m × log log n
   - Error rate: 1.04/√m

3. **Comparing structures**:
   - When to use each counter/filter
   - Space comparison table
   - Support for operations (delete, merge)

4. **Parameter selection**:
   - Given requirements, choose m, k, r
   - Trade-off analysis

5. **Applications**:
   - Why Bloom filters in databases?
   - How HyperLogLog enables real-time analytics?

### Implementation Tips

1. **Hash functions**:
   - Use good quality: MurmurHash3, xxHash
   - Double hashing for multiple hash functions
   - Test distribution in practice

2. **Parameter tuning**:
   - Start with theoretical values
   - Measure actual FP rate
   - Adjust based on workload

3. **Monitoring**:
   - Track filter load factor
   - Monitor FP rate in production
   - Rebuild when performance degrades

4. **Libraries** (don't reinvent):
   - Redis: HyperLogLog, Bloom filter
   - Guava (Java): BloomFilter
   - PyBloomFilter (Python)
   - pdatastructs (Rust)

### The Big Picture

**Probabilistic data structures enable**:
- Streaming algorithms (process unbounded data)
- Big data systems (handle billions of elements)
- Real-time analytics (fast approximate answers)
- Distributed systems (compact summaries)

**Core principle**:
> Trade perfect accuracy for massive space/time savings

**When to use**:
- Approximate answer sufficient
- Scale is large
- Space/time is constrained
- False positives acceptable

**When NOT to use**:
- Exact answer required
- Small scale (exact is cheap)
- False positives costly
- Debugging (need precision)

### Final Thoughts

Probabilistic counters and AMQ filters are among the most practical algorithms:
- Used in production at massive scale (Google, Facebook, Twitter, Redis)
- Enable features impossible with exact algorithms
- Near-optimal space (within 1.5× of theoretical minimum)
- Simple to implement and reason about

**Master these and you'll have powerful tools for building scalable systems!**

---

**Good luck with your studies!** May your bits be few and your false positives be rare! 🎲
