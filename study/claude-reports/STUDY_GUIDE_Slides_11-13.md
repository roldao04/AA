# Comprehensive Study Guide - Data Stream Algorithms (Slides 11-13)
## Advanced Algorithms - University of Aveiro
### Professor: Joaquim Madeira
---

## Table of Contents
1. [Slide 11: Finding Frequent Items](#slide-11)
   - [Data Stream Model](#stream-model)
   - [MAJORITY Problem - Boyer & Moore](#majority)
   - [FREQUENT Problem - Misra & Gries](#misra-gries)
   - [Lossy-Counting Algorithm](#lossy-counting)
   - [Space-Saving Algorithm](#space-saving)
   - [Implementation Issues](#implementation)
2. [Slide 12: Sketch Algorithms](#slide-12)
   - [Synopses & Sketches](#synopses)
   - [Count-Min Sketch](#count-min)
   - [Finding Heavy-Hitters](#heavy-hitters)
   - [Count Sketch](#count-sketch)
3. [Slide 13: Distinct Elements](#slide-13)
   - [Direct Approaches](#direct-approaches)
   - [Flajolet-Martin Algorithm](#flajolet-martin)
   - [HyperLogLog Algorithm](#hyperloglog)
4. [Practice Problems](#practice-problems)
5. [Summary & Exam Tips](#summary)

---

# SLIDE 11: FINDING FREQUENT ITEMS <a name="slide-11"></a>

## The Data Stream Model <a name="stream-model"></a>

### Motivation

**Data streams** are everywhere in modern computing:
- Sequence of queries to Internet search engines
- Transactions across supermarket chains
- Network traffic monitoring (packets)
- Social media activity
- Sensor data from IoT devices

**Characteristics:**
- **Huge numbers** of simple data pieces
- Arriving at **enormous rates** (hundreds of GB/day or more!)
- Taken together, form a **complex whole**

### The Streaming Model Requirements

**Goal:** Compute function Φ(σ) of a massively long input stream σ

**Constraints:**
1. **One pass** over the data
2. **No random access** to data tokens
3. **Scan in given order** only
4. **Process on the fly** (as it happens)

**Resource requirements:**
```
Use space and time SUBLINEAR in the size of input!
```

**Why?** Total data too large to store or process traditionally.

### When to Produce Output?

**Four models:**
1. **At end of stream** - traditional batch processing
2. **When queried** on stream prefix observed so far
3. **Whenever stream updates** - continuous output
4. **On sliding window** of most recent updates

### Quality of Algorithm's Answer

**Most functions Φ(σ) are real-valued.**

We allow:
- **Computing estimates/approximations** (not exact!)
- **Using randomized algorithms**
- **Errors with small, controllable probability**

**Quality metric:** **(ε, δ)-approximation**

```
P[|Φ̂(σ) - Φ(σ)| ≤ ε × ||σ||] ≥ 1 - δ

where:
- Φ̂(σ) = estimated value
- Φ(σ) = true value
- ε = approximation error (relative)
- δ = failure probability
- ||σ|| = some norm of the stream (e.g., length)
```

**Example:** ε=0.01, δ=0.05 means:
- Error within 1% of stream size
- With 95% probability

---

## Finding Frequent Items - Overview

### The Heavy-Hitters Problem

**Problem statement:**
Given a sequence of items, identify those which occur **most frequently**.

**Formal definition:**
Find all items whose frequency exceeds a specified fraction of total items.

**Notation:**
- m = total number of items in stream
- n = number of distinct items
- f_i = frequency of item i
- Threshold: m/k for some parameter k

**Goal:** Find all items with f_i > m/k

### Applications

**1. Network packet monitoring:**
- Frequent items = heaviest bandwidth users
- Detect DDoS attacks
- Identify top talkers

**2. Search engine queries:**
- Frequent items = currently popular search terms
- Real-time trending topics
- Query optimization

**3. E-commerce:**
- Popular products
- Frequent buyers
- Trending categories

### Two Approaches

**1. Counter-based algorithms** (Slide 11):
- Track and maintain counts for subset of stream items
- **Examples:** Misra-Gries, Lossy-Counting, Space-Saving
- **Deterministic** algorithms

**2. Sketch algorithms** (Slide 12):
- Randomized approach
- Do NOT explicitly store stream elements
- **Examples:** Count-Min Sketch, Count Sketch
- **Probabilistic** guarantees

---

## THE MAJORITY PROBLEM <a name="majority"></a>

### Problem Definition

**MAJORITY element:**
An element that appears **more than m/2 times** in a sequence of m elements.

**Note:** At most ONE majority element can exist!

**Example:**
```
Sequence: [3, 1, 3, 3, 2, 3, 3]
Length m = 7
Majority threshold = 7/2 = 3.5

Element 3 appears 5 times > 3.5
→ Element 3 is the MAJORITY ✓
```

### Applications

**1. Elections:**
- Determine if candidate has majority of votes
- Avoid full count if possible

**2. Fault-tolerant computing:**
- Perform multiple redundant computations
- Check if majority of results agree
- Take majority as correct answer

**3. Distributed systems:**
- Consensus algorithms
- Replicated state machines

### Naive Algorithm (Sort-based)

**Algorithm:**
1. Sort the list: O(m log m)
2. If majority exists, it's the middle element
3. Verify by counting

**Why middle element?**
- If element appears > m/2 times
- It MUST occupy the middle position after sorting!

**Problems:**
- O(m log m) time
- Requires random access
- **NOT suitable for data streams!**

### Naive Algorithm (Counter-based)

**Algorithm:**
1. Create n frequency counters (one per distinct item)
2. **First pass:** Scan sequence, increment counters
3. **Second pass:** Find most frequent element
4. **Third pass:** Verify it's majority (count > m/2)

**Efficiency:**
- Time: O(m) per pass, 3 passes total
- Space: O(n) for counters

**Problems:**
- Space proportional to number of distinct items
- For large n, requires too much memory
- Still needs multiple passes

---

## Boyer & Moore's MJRTY Algorithm (1980) <a name="mjrty"></a>

### The Brilliant Idea

**Key insight:** Majority element (if exists) survives "pair annihilation"

**Intuition:**
- If we remove pairs of DIFFERENT elements
- Majority element will remain
- Think of it as a "voting battle"!

**Visual example:**
```
Stream: [3, 1, 3, 3, 2, 3, 3]

Pair off different elements:
(3,1) - cancel out
(3,2) - cancel out

Remaining: [3, 3, 3]
→ 3 is the candidate!
```

### Two-Pass Algorithm

**Pass 1:** Find majority candidate
**Pass 2:** Verify candidate is actually majority

**Why two passes?**
- Pass 1 finds candidate but doesn't guarantee it's majority
- Pass 2 confirms with actual count

### Algorithm - First Pass (Find Candidate)

**Pseudocode:**
```
MJRTY_FindCandidate(stream):
    candidate = null
    counter = 0

    for each element x in stream:
        if counter == 0:
            candidate = x
            counter = 1
        else if candidate == x:
            counter++
        else:
            counter--

    return candidate
```

**Invariant:** At any point, if we remove all paired elements, candidate appears counter more times than any other.

### Algorithm - Second Pass (Verify)

**Pseudocode:**
```
MJRTY_Verify(stream, candidate):
    counter = 0

    for each element x in stream:
        if candidate == x:
            counter++
        if counter >= (m/2 + 1):
            return TRUE  // Can stop early!

    return counter > m/2
```

**Optimization:** Can stop as soon as counter > m/2!

### Complete Algorithm

**Pseudocode:**
```
MJRTY(stream, m):
    // First pass
    candidate = MJRTY_FindCandidate(stream)

    // Second pass
    if MJRTY_Verify(stream, candidate):
        return candidate
    else:
        return null  // No majority element
```

### Visual Example - First Pass

**Stream:** [3, 1, 4, 1, 5, 9, 2, 6, 5]

```
Step | Element | Candidate | Counter | Action
-----|---------|-----------|---------|------------------
  1  |    3    |     3     |    1    | Set candidate
  2  |    1    |     3     |    0    | Different, decr
  3  |    4    |     4     |    1    | New candidate
  4  |    1    |     4     |    0    | Different, decr
  5  |    5    |     5     |    1    | New candidate
  6  |    9    |     5     |    0    | Different, decr
  7  |    2    |     2     |    1    | New candidate
  8  |    6    |     2     |    0    | Different, decr
  9  |    5    |     5     |    1    | New candidate

Candidate: 5
```

**Second pass:** Count occurrences of 5
- Frequency: 2 out of 9
- 2 < 9/2 = 4.5
- **Result:** No majority element ✗

### Another Example

**Stream:** [5, 5, 2, 5, 5, 2, 5]

```
Step | Element | Candidate | Counter | Action
-----|---------|-----------|---------|------------------
  1  |    5    |     5     |    1    | Set candidate
  2  |    5    |     5     |    2    | Same, incr
  3  |    2    |     5     |    1    | Different, decr
  4  |    5    |     5     |    2    | Same, incr
  5  |    5    |     5     |    3    | Same, incr
  6  |    2    |     5     |    2    | Different, decr
  7  |    5    |     5     |    3    | Same, incr

Candidate: 5
```

**Second pass:** Count occurrences of 5
- Frequency: 5 out of 7
- 5 > 7/2 = 3.5
- **Result:** 5 is the MAJORITY! ✓

### Why Second Pass is Necessary

**Counter-example:** Can we skip second pass?

**Stream:** [1, 2, 3, 4, 5]

```
First pass:
Step 1: candidate=1, counter=1
Step 2: candidate=1, counter=0
Step 3: candidate=3, counter=1
Step 4: candidate=3, counter=0
Step 5: candidate=5, counter=1

Candidate: 5
```

**But:** 5 appears only once (1/5 = 20%)
- NOT a majority!
- First pass can give false candidate

**Conclusion:** Second pass is **essential** for correctness!

### Complexity Analysis

**Time complexity:**
- First pass: O(m)
- Second pass: O(m) worst case, can stop early
- **Total: O(m)** ✓

**Space complexity:**
- candidate: 1 element
- counter: 1 integer
- **Total: O(1)** ✓ Constant space!

**Advantages:**
- Linear time
- Constant space
- Very practical!

**Limitation:**
- Requires TWO passes over data
- **Problem for streams:** Cannot go back!
- But: First pass gives "partial guarantee"

### Python Implementation

```python
def mjrty_find_candidate(stream):
    """
    First pass: Find majority candidate

    Args:
        stream: iterable of elements

    Returns:
        candidate element
    """
    candidate = None
    counter = 0

    for x in stream:
        if counter == 0:
            candidate = x
            counter = 1
        elif candidate == x:
            counter += 1
        else:
            counter -= 1

    return candidate

def mjrty_verify(stream, candidate):
    """
    Second pass: Verify candidate is majority

    Args:
        stream: iterable of elements
        candidate: element to verify

    Returns:
        True if candidate is majority, False otherwise
    """
    m = 0  # Total elements
    count = 0  # Candidate count

    for x in stream:
        m += 1
        if x == candidate:
            count += 1
        # Early termination optimization
        if count > m // 2:
            # Already more than half, can stop
            # But we don't know final m, so continue...
            pass

    return count > m // 2

def mjrty(stream):
    """
    Complete Boyer-Moore MJRTY algorithm

    Args:
        stream: list of elements (need to iterate twice)

    Returns:
        majority element if exists, None otherwise
    """
    # First pass
    candidate = mjrty_find_candidate(stream)

    # Second pass
    if candidate is not None and mjrty_verify(stream, candidate):
        return candidate
    else:
        return None

# Test examples
def test_mjrty():
    # Test 1: Has majority
    stream1 = [5, 5, 2, 5, 5, 2, 5]
    result1 = mjrty(stream1)
    print(f"Stream 1: {stream1}")
    print(f"Majority: {result1}")  # Should be 5
    print()

    # Test 2: No majority
    stream2 = [3, 1, 4, 1, 5, 9, 2, 6, 5]
    result2 = mjrty(stream2)
    print(f"Stream 2: {stream2}")
    print(f"Majority: {result2}")  # Should be None
    print()

    # Test 3: All same
    stream3 = [7, 7, 7, 7]
    result3 = mjrty(stream3)
    print(f"Stream 3: {stream3}")
    print(f"Majority: {result3}")  # Should be 7
    print()

    # Test 4: Exactly half (no majority)
    stream4 = [1, 1, 2, 2]
    result4 = mjrty(stream4)
    print(f"Stream 4: {stream4}")
    print(f"Majority: {result4}")  # Should be None (1 is not > 4/2)

test_mjrty()
```

### Tasks

**1. Implement naive algorithm**
- Compare running times with MJRTY

**2. Test with random strings**
- Generate random sequences over alphabet
- Vary sequence length and alphabet size
- Measure accuracy and speed

**3. Streaming analysis**
- For streams, only first pass is possible
- Track how often candidate from first pass is actual majority
- What percentage of time is "partial guarantee" correct?

---

## THE FREQUENT PROBLEM <a name="misra-gries"></a>

### Problem Definition

**Goal:** Find ALL items with frequency > m/k

**Comparison to MAJORITY:**
- MAJORITY: find item with freq > m/2 (k=2, at most 1 item)
- FREQUENT: find items with freq > m/k (at most k-1 items)

**Why "at most k-1 items"?**
- If k items each had frequency > m/k
- Total frequency > k × (m/k) = m
- Contradiction! (total = m)
- Therefore, at most k-1 items

**Example:**
```
Stream: [1, 2, 1, 3, 1, 2, 4, 1, 2]
m = 9 items
k = 3, threshold = m/k = 3

Frequencies:
Item 1: 4 times > 3 ✓
Item 2: 3 times = 3 (not >)
Item 3: 1 time
Item 4: 1 time

Heavy-hitters (freq > 3): {1}
```

### Applications

**1. Network traffic:**
- Find top-k bandwidth consumers
- Identify elephant flows

**2. Web analytics:**
- Most popular pages
- Top search terms
- Frequent user actions

**3. Database query optimization:**
- Frequent query patterns
- Hot data items

---

## Misra & Gries Algorithm (1982) <a name="frequency-estimation"></a>

### Key Idea

**Generalization of Boyer-Moore's MJRTY:**
- MJRTY: maintains 1 counter (k=2)
- Misra-Gries: maintains **at most (k-1) counters**

**Strategy:**
- Keep associative array: item → count
- Increment if item already tracked
- Add new item if space available
- Otherwise: **decrement ALL counters**

### The Algorithm

**Data structure:**
- Associative array A
- Keys: items seen in stream
- Values: counters
- **Size:** at most (k-1) entries

**Pseudocode:**
```
Misra_Gries(stream, k):
    A = empty associative array

    for each item j in stream:
        if j in keys(A):
            A[j] = A[j] + 1              // Increment
        else:
            if |keys(A)| < (k-1):
                A[j] = 1                 // Add new
            else:
                for each i in keys(A):
                    A[i] = A[i] - 1      // Decrement ALL
                    if A[i] == 0:
                        remove i from A  // Delete zeros

    return A
```

**Query frequency estimate for item a:**
```
if a in keys(A):
    return A[a]
else:
    return 0
```

### Visual Example

**Stream:** [3, 1, 3, 3, 2, 3, 4, 3, 2]
**Parameter:** k = 3 (find items with freq > m/3 = 3)
**Max counters:** k-1 = 2

```
Step | Item | Action         | Array A        | Comment
-----|------|----------------|----------------|------------------
  1  |  3   | Add            | {3: 1}         | First item
  2  |  1   | Add            | {3: 1, 1: 1}   | Second distinct
  3  |  3   | Increment      | {3: 2, 1: 1}   | Item exists
  4  |  3   | Increment      | {3: 3, 1: 1}   | Item exists
  5  |  2   | Decrement all  | {3: 2}         | Array full!
  6  |  3   | Increment      | {3: 3}         | Item exists
  7  |  4   | Add            | {3: 3, 4: 1}   | Space available
  8  |  3   | Increment      | {3: 4, 4: 1}   | Item exists
  9  |  2   | Decrement all  | {3: 3}         | Array full!

Final: {3: 3}
```

**True frequencies:**
- Item 3: 5 times
- Item 2: 2 times
- Item 1: 1 time
- Item 4: 1 time

**Estimated frequencies:**
- Item 3: 3 (underestimate by 2)
- Others: 0

**Heavy-hitters (freq > 3):**
- True: {3}
- Reported: {3} ✓ Correct!

### Key Properties

**1. No false negatives:**
```
If f_i > m/k, then item i is in A at the end
```

**Proof:**
- Suppose item i has frequency f_i > m/k
- Each decrement phase removes at most k items (including i once)
- Maximum decrements to i: < m/k (since others contribute < m - m/k)
- Final count for i: f_i - (decrements) > m/k - m/k = 0
- Therefore i survives in A

**2. Underestimates (never overestimates):**
```
Estimated frequency ≤ True frequency
```

**Proof:**
- Increment: happens exactly f_i times
- Decrement: can happen multiple times
- Net count ≤ f_i

**3. Error bound:**
```
|f̂_i - f_i| ≤ m/k

where f̂_i is estimated frequency
```

**Proof:**
- Each decrement phase processes k items
- At most m/k decrement phases total
- Each affects item i at most once per phase
- Maximum error: m/k

### Space and Time Complexity

**Space:**
- At most (k-1) counters
- Each counter: O(log m) bits
- **Total: O(k log m)**

**Time per item:**
- Lookup: depends on data structure
  - Hash table: O(1) expected
  - Balanced tree: O(log k)
- Decrement all: O(k) worst case

**Total time:**
- O(m) with hash table (amortized)
- O(m log k) with balanced tree

### Python Implementation

```python
class MisraGries:
    """
    Misra-Gries algorithm for finding frequent items

    Finds all items with frequency > m/k
    """

    def __init__(self, k):
        """
        Initialize algorithm

        Args:
            k: parameter (find items with freq > m/k)
        """
        self.k = k
        self.counters = {}  # Dictionary: item → count
        self.m = 0  # Total items processed

    def update(self, item):
        """
        Process one item from stream

        Args:
            item: the item to process
        """
        self.m += 1

        if item in self.counters:
            # Increment existing counter
            self.counters[item] += 1
        else:
            # Check if we have space
            if len(self.counters) < (self.k - 1):
                # Add new item
                self.counters[item] = 1
            else:
                # Decrement all counters
                to_remove = []
                for key in self.counters:
                    self.counters[key] -= 1
                    if self.counters[key] == 0:
                        to_remove.append(key)

                # Remove zeros
                for key in to_remove:
                    del self.counters[key]

    def query(self, item):
        """
        Get estimated frequency of item

        Args:
            item: item to query

        Returns:
            estimated frequency (lower bound)
        """
        return self.counters.get(item, 0)

    def get_heavy_hitters(self):
        """
        Get all items currently tracked

        These are candidates for freq > m/k

        Returns:
            dictionary of item → estimated count
        """
        return dict(self.counters)

# Test
def test_misra_gries():
    stream = [3, 1, 3, 3, 2, 3, 4, 3, 2]
    k = 3

    mg = MisraGries(k)

    print(f"Stream: {stream}")
    print(f"k = {k}, threshold = m/{k}")
    print()

    # Process stream
    for item in stream:
        mg.update(item)

    # Get results
    heavy_hitters = mg.get_heavy_hitters()
    print(f"Heavy-hitter candidates: {heavy_hitters}")
    print()

    # Verify with true counts
    from collections import Counter
    true_counts = Counter(stream)
    threshold = len(stream) / k

    print(f"True frequencies:")
    for item, count in sorted(true_counts.items()):
        estimated = mg.query(item)
        is_heavy = count > threshold
        print(f"  Item {item}: {count} (estimated: {estimated}) {'✓ HEAVY' if is_heavy else ''}")

test_misra_gries()
```

### Advanced Implementation - Optimized Decrement

**Problem:** Decrementing all counters is O(k)

**Solution:** Use linked list grouped by frequency counts

**Data structure:**
- Hash table: item → (count, pointer to list node)
- Linked lists: one per count value
- Track minimum count

**Decrement operation:**
1. Find list for minimum count
2. Decrement all items in that list (move to count-1 list)
3. Remove items that reach count 0
4. Update minimum

**Complexity:**
- Amortized O(1) per update
- Space overhead: O(k) for linked list structure

---

## Lossy-Counting Algorithm (2002) <a name="lossy-counting"></a>

### Manku & Motwani's Approach

**Variation of Misra-Gries** with explicit error tracking.

**Key differences:**
- Track "delta" value (implicit error bound)
- Delete items when count < delta
- Frequencies never underestimated by more than ε × m

### The Algorithm

**Parameters:**
- ε: error parameter (user-specified)

**Data structure:**
- Associative array: item → (count, delta)
- count: current count (lower bound on true count)
- delta: when item was first inserted (implicit)

**Conceptual buckets:**
- Divide stream into buckets of size w = ⌈1/ε⌉
- Current bucket number: b = ⌈m/w⌉

**Pseudocode:**
```
Lossy_Counting(stream, ε):
    w = ⌈1/ε⌉
    D = empty dictionary  // item → count
    m = 0  // items processed

    for each item in stream:
        m = m + 1

        if item in D:
            D[item] = D[item] + 1
        else:
            b_current = ⌈m/w⌉
            D[item] = 1 + (b_current - 1)  // count + delta

        // Bucket boundary?
        if m mod w == 0:
            // Delete items with count ≤ b_current
            b_current = m/w
            for each item in D:
                if D[item] ≤ b_current:
                    delete item from D

    return D
```

**Query:**
```
Items with freq > s × m (for support s):
    return {item : D[item] > (s - ε) × m}
```

### Key Properties

**1. Error guarantee:**
```
True_frequency(item) - ε × m ≤ Estimated_frequency(item) ≤ True_frequency(item)
```

**2. No false negatives:**
- Items with true freq > s × m are retained
- Reported if estimated > (s - ε) × m

**3. Space bound:**
- At most 1/ε items tracked

### Example

**Stream:** [a, b, a, c, a, b, d, a, b, c, a, d, b, a, c]
**ε = 0.2, w = ⌈1/0.2⌉ = 5**

```
Buckets:
1: [a, b, a, c, a]
2: [b, d, a, b, c]
3: [a, d, b, a, c]

Processing:
Bucket 1: Process 5 items
  - At end: D = {a:3, b:1, c:1}
  - Delete items with count ≤ 1: D = {a:3}

Bucket 2: Process next 5
  - Updates: a→4, b→1+1=2, d→1+1=2, c→1+1=2
  - At end: D = {a:4, b:2, d:2, c:2}
  - Delete items with count ≤ 2: keep items > 2
  - D = {a:4}

...
```

### Python Implementation

```python
import math

class LossyCounting:
    """Lossy-Counting algorithm"""

    def __init__(self, epsilon):
        """
        Args:
            epsilon: error parameter
        """
        self.epsilon = epsilon
        self.w = math.ceil(1 / epsilon)  # Bucket width
        self.D = {}  # item → count
        self.m = 0   # Items processed

    def update(self, item):
        """Process one item"""
        self.m += 1

        if item in self.D:
            self.D[item] += 1
        else:
            # Add with delta = current bucket - 1
            b_current = math.ceil(self.m / self.w)
            self.D[item] = 1 + (b_current - 1)

        # Bucket boundary? Prune items
        if self.m % self.w == 0:
            b_current = self.m // self.w
            to_delete = [item for item, count in self.D.items()
                        if count <= b_current]
            for item in to_delete:
                del self.D[item]

    def query(self, support):
        """
        Get items with frequency > support × m

        Args:
            support: threshold as fraction

        Returns:
            dictionary of heavy hitters
        """
        threshold = (support - self.epsilon) * self.m
        return {item: count for item, count in self.D.items()
                if count > threshold}

# Test
def test_lossy_counting():
    stream = list("abaacaabdabdabac")
    epsilon = 0.2

    lc = LossyCounting(epsilon)
    for item in stream:
        lc.update(item)

    print(f"Stream: {''.join(stream)}")
    print(f"ε = {epsilon}")
    print(f"Tracked items: {lc.D}")

    # Get heavy hitters for support 0.3 (30%)
    hh = lc.query(0.3)
    print(f"Heavy hitters (freq > 30%): {hh}")

test_lossy_counting()
```

---

## Space-Saving Algorithm (2005) <a name="space-saving"></a>

### Metwally et al.'s Approach

**Most space-efficient counter-based algorithm!**

**Key idea:**
- Keep exactly k = ⌈1/ε⌉ counters (not "at most")
- Replace item with **least count** when array is full
- Increment the replaced counter!

### The Algorithm

**Data structure:**
- Fixed-size array: k items and counts
- Track minimum counter

**Pseudocode:**
```
Space_Saving(stream, ε):
    k = ⌈1/ε⌉
    D = empty dictionary (max size k)
    min_count = 0

    for each item in stream:
        if item in D:
            D[item] = D[item] + 1
        else:
            if |D| < k:
                D[item] = 1
            else:
                // Find item with minimum count
                min_item = argmin_{i ∈ D} D[i]
                min_count = D[min_item]

                // Replace
                delete min_item from D
                D[item] = min_count + 1  // Inherit count!

        // Update min (can optimize with heap)
        min_count = min_{i ∈ D} D[i]

    return D
```

### Key Properties

**1. All counters sum to m:**
```
Σ D[item] = m
```

**2. Error bound:**
```
True_frequency(item) ≥ Estimated_frequency(item) ≥ True_frequency(item) - min_count
```

**3. Smallest count:**
```
min_count ≤ ε × m
```

**Proof:**
- Average count = m/k = m × ε
- Minimum ≤ Average

**4. Completeness:**
All items with true freq > ε × m are stored

### Advantages over Misra-Gries

**1. Space:** Exactly k items (predictable)

**2. Accuracy:** Often better in practice

**3. Simplicity:** No decrement-all operation

### Implementation with Min-Heap

**Optimization:** Use min-heap to find minimum count efficiently

**Data structure:**
- Hash table: item → (count, heap_index)
- Min-heap: (count, item) pairs

**Operations:**
- Find min: O(1)
- Update count: O(log k)
- Replace min: O(log k)

### Python Implementation

```python
import heapq

class SpaceSaving:
    """Space-Saving algorithm with min-heap"""

    def __init__(self, k):
        """
        Args:
            k: number of counters to maintain
        """
        self.k = k
        self.counters = {}  # item → count
        self.heap = []      # min-heap of (count, item)

    def update(self, item):
        """Process one item"""
        if item in self.counters:
            # Increment existing
            old_count = self.counters[item]
            self.counters[item] += 1

            # Update heap (lazy: push new, ignore old)
            heapq.heappush(self.heap, (self.counters[item], item))

        else:
            if len(self.counters) < self.k:
                # Add new item
                self.counters[item] = 1
                heapq.heappush(self.heap, (1, item))
            else:
                # Find and replace minimum
                while self.heap:
                    min_count, min_item = heapq.heappop(self.heap)
                    if min_item in self.counters and self.counters[min_item] == min_count:
                        # Valid minimum found
                        break

                # Replace min_item with new item
                del self.counters[min_item]
                self.counters[item] = min_count + 1
                heapq.heappush(self.heap, (min_count + 1, item))

    def get_top_k(self):
        """Get all tracked items sorted by count"""
        return sorted(self.counters.items(), key=lambda x: x[1], reverse=True)

# Test
def test_space_saving():
    stream = list("abaacaabdabdabac")
    k = 3

    ss = SpaceSaving(k)
    for item in stream:
        ss.update(item)

    print(f"Stream: {''.join(stream)}")
    print(f"k = {k}")
    print()
    print("Top items:")
    for item, count in ss.get_top_k():
        print(f"  {item}: {count}")

test_space_saving()
```

### Experimental Performance

**From Cormode & Hadjieleftheriou (2008-2009):**

**Space-Saving benefits:**
- **Very fast:** 20M - 30M updates per second
- **Accurate:** Lower error than Misra-Gries
- **Simple:** Easy to implement

**Implementation trade-offs:**
- **Heap:** Faster updates, slower queries
- **Linked lists:** Slower updates, faster queries (grouped by frequency)

---

## Implementation Issues <a name="implementation"></a>

### Dictionary Data Structures

**Choices for associative array:**

**1. Hash table:**
- Average case: O(1) lookup/insert/delete
- Worst case: O(k) (with chaining)
- Good for: Fast updates

**2. Balanced search tree:**
- Worst/average: O(log k)
- Good for: Guaranteed performance
- Examples: Red-black tree, AVL tree

**3. Python dict:**
- Implemented as hash table
- O(1) expected time
- Resize overhead amortized

### Decrement Operation Optimization

**Problem:** Misra-Gries decrement-all is O(k)
- Happens O(m/k) times
- Total: O(m) amortized, but slow in practice

**Solution: Linked lists grouped by frequency**

**Data structure:**
```
Hash table: item → (count, pointer to list node)

Linked lists: one list per count value
  count=1: [item_a, item_b, ...]
  count=2: [item_c, ...]
  count=3: [item_d, item_e, ...]
  ...

Min count tracker: pointer to minimum count list
```

**Decrement operation:**
1. Find list at minimum count
2. For each item in list:
   - Decrement count (move to count-1 list)
   - If count becomes 0, remove
3. Update minimum count pointer

**Complexity:**
- Amortized O(1) per item
- Extra space: O(k) for list structure

### Finding Minimum

**For Space-Saving:**

**Option 1: Linear scan**
- Time: O(k) per replacement
- Space: O(k) for counters
- Simple implementation

**Option 2: Min-heap**
- Time: O(log k) per update
- Space: O(k) for heap
- Better for large k

**Option 3: Sorted linked list**
- Time: O(k) update, O(1) min
- Space: O(k)
- Good if queries frequent

**Recommendation:** Min-heap for k > 100

---

# SLIDE 12: SKETCH ALGORITHMS <a name="slide-12"></a>

## Data Streams - Synopses <a name="synopses"></a>

### Motivation

**Challenge:**
- High-speed data streams / massive data
- Need fast, interactive response times
- Cannot process all data exactly

**Solution:** Compute lossy, compact **synopsis**
- Captures feature(s) of interest
- Execute queries on synopsis
- Get accurate estimates (not exact!)

### Types of Synopses

**1. Random samples:**
- Maintain random subset of stream
- Uniform or weighted sampling
- Good for: general queries

**2. Histograms:**
- Divide data into buckets
- Track bucket statistics
- Good for: range queries

**3. Wavelets:**
- Hierarchical representation
- Multi-resolution analysis
- Good for: signals, time series

**4. Sketches:**
- Linear transforms of input
- Hash-based data structures
- Good for: frequency, cardinality

### What are Sketches?

**Linear Sketches:**
Data structures representable as **linear transform** of input.

**Mathematical view:**
```
Sketch S = M × F

where:
- F = frequency vector (F[i] = frequency of item i)
- M = transformation matrix
- S = sketch vector (compressed representation)
```

**Properties:**
- **Fast:** Update independent of current state
- **Compact:** Sublinear space
- **Continuous:** Can handle updates
- **Parallelizable:** Sketches can be merged

### Frequency-Based Sketches

**Purpose:** Summarize frequency distribution

**Applications:**
- **Heavy-hitters:** Find most frequent items
- **Point queries:** Estimate frequency of specific item
- **Range queries:** Frequency in value range

**Guaranteed accuracy:** (ε, δ)-approximation

---

## THE COUNT-MIN SKETCH <a name="count-min"></a>

### Overview (Cormode & Muthukrishnan, 2003-2005)

**The Count-Min Sketch** is a probabilistic data structure for:
- Frequency estimation in data streams
- Sub-linear space
- Point queries and range queries

**Key properties:**
- **May over-estimate** frequencies
- **Never under-estimates**
- **Biased estimator** (one-sided error)
- Error bound with high probability

### Motivation: Simple Approach

**Idea 1:** Use hash table
- Problem: Can be very large (many distinct items)

**Idea 2:** Use array of counters + hash
- Problem: Collisions cause over-counting

**Idea 3:** Use MULTIPLE arrays with MULTIPLE hashes
- Take **MINIMUM** to reduce collision errors
- **This is Count-Min Sketch!**

### Structure

**2D array:**
```
     w columns
    ┌──────────────────┐
  d │ □ □ □ □ □ □ □ □ │  row 1, hash h₁
    │ □ □ □ □ □ □ □ □ │  row 2, hash h₂
rows│ □ □ □ □ □ □ □ □ │  row 3, hash h₃
  = │ □ □ □ □ □ □ □ □ │      ...
depth  ...............│      ...
    │ □ □ □ □ □ □ □ □ │  row d, hash hd
    └──────────────────┘
```

**Components:**
- **w:** width (number of columns)
- **d:** depth (number of rows)
- **d hash functions:** h₁, h₂, ..., h_d
- Each hash maps item to [0, w-1]

### Hash Functions

**For integer items:**
```
h_k(i) = ((a_k × i + b_k) mod p) mod w

where:
- p = large prime (e.g., 2³¹-1 or 2⁶¹-1)
- a_k, b_k = random values from [1, p-1]
- w = width of array
```

**Requirements:**
- **Pairwise independent** hash functions
- Different hash for each row
- Deterministic (same item → same hash)

**Don't need:**
- Cryptographic hash functions
- Perfect hash functions

### Operations

**1. Initialization:**
```
CountMinInit(w, d, p):
    // Create array
    C[1..d, 1..w] = 0

    // Generate hash functions
    for j = 1 to d:
        Pick a_j, b_j randomly from [1, p-1]

    N = 0  // Total items processed
```

**2. Update (process item i):**
```
CountMinUpdate(i):
    N = N + 1

    for j = 1 to d:
        h_j(i) = (a_j × i + b_j) mod p mod w
        C[j, h_j(i)] = C[j, h_j(i)] + 1
```

**Time:** O(d)

**3. Query (estimate frequency of item i):**
```
CountMinEstimate(i):
    est = ∞

    for j = 1 to d:
        h_j(i) = (a_j × i + b_j) mod p mod w
        est = min(est, C[j, h_j(i)])

    return est
```

**Time:** O(d)

### Visual Example

**Setup:** w=8, d=3

**Initial state:**
```
Row 1: [0, 0, 0, 0, 0, 0, 0, 0]
Row 2: [0, 0, 0, 0, 0, 0, 0, 0]
Row 3: [0, 0, 0, 0, 0, 0, 0, 0]
```

**Insert item 'a':**
- h₁('a') = 2 → C[1,2]++
- h₂('a') = 5 → C[2,5]++
- h₃('a') = 1 → C[3,1]++

```
Row 1: [0, 0, 1, 0, 0, 0, 0, 0]  ↑
Row 2: [0, 0, 0, 0, 0, 1, 0, 0]      ↑
Row 3: [0, 1, 0, 0, 0, 0, 0, 0]  ↑
```

**Insert item 'b':**
- h₁('b') = 5 → C[1,5]++
- h₂('b') = 2 → C[2,2]++
- h₃('b') = 6 → C[3,6]++

```
Row 1: [0, 0, 1, 0, 0, 1, 0, 0]
Row 2: [0, 0, 1, 0, 0, 1, 0, 0]
Row 3: [0, 1, 0, 0, 0, 0, 1, 0]
```

**Insert item 'a' again:**
```
Row 1: [0, 0, 2, 0, 0, 1, 0, 0]
Row 2: [0, 0, 1, 0, 0, 2, 0, 0]
Row 3: [0, 2, 0, 0, 0, 0, 1, 0]
```

**Query 'a':**
- C[1, 2] = 2
- C[2, 5] = 2
- C[3, 1] = 2
- **Estimate: min(2, 2, 2) = 2** ✓ (correct!)

**Insert item 'c' (collides with 'a' in row 1):**
- h₁('c') = 2 (collision!)
- h₂('c') = 7
- h₃('c') = 3

```
Row 1: [0, 0, 3, 0, 0, 1, 0, 0]  ← 'a' and 'c' collide
Row 2: [0, 0, 1, 0, 0, 2, 0, 1]
Row 3: [0, 2, 0, 1, 0, 0, 1, 0]
```

**Query 'a' now:**
- C[1, 2] = 3 (over-estimate due to collision)
- C[2, 5] = 2 (correct)
- C[3, 1] = 2 (correct)
- **Estimate: min(3, 2, 2) = 2** ✓ (still correct! minimum filters out collision)

### Parameter Selection

**Goal:** Error ≤ ε × N with probability ≥ (1 - δ)

**Formal guarantee:**
```
P[f̂_i ≤ f_i + ε × N] ≥ 1 - δ

where:
- f̂_i = estimated frequency
- f_i = true frequency
- N = total items processed
- ε = relative error
- δ = failure probability
```

**Parameters:**
```
d = ⌈log(1/δ)⌉           (depth/rows)

w = ⌈2/ε⌉ = ⌈e/ε⌉        (width/columns)
```

**Note:** Some papers use e/ε, some use 2/ε (constants differ slightly)

**Space complexity:**
```
S = w × d × bits_per_counter
  = O((1/ε) × log(1/δ)) counters
```

**Typical counter size:** 32 bits (4 bytes)

### Example Calculation

**Requirement:** Error ≤ 0.1% with 99.9% certainty

**Given:**
- ε = 0.001 (0.1%)
- δ = 0.001 (99.9% certainty)

**Calculate parameters:**
```
w = ⌈2/ε⌉ = ⌈2/0.001⌉ = ⌈2000⌉ = 2000

d = ⌈log(1/δ)⌉ = ⌈log(1/0.001)⌉
  = ⌈log(1000)⌉
  = ⌈9.97⌉ = 10
```

**Space required:**
```
Counters: 2000 × 10 = 20,000 counters
With 32-bit counters: 20,000 × 4 bytes = 80 KB
```

**Conclusion:** Only 80 KB to track frequencies with 0.1% error!

### Accuracy Analysis

**Why does taking minimum help?**

**Expected error for one row:**
- Collisions add extra counts
- Expected added weight: N/w
- By Markov inequality: P(error > 2N/w) ≤ 1/2

**For multiple independent rows:**
- Probability ALL d rows have large error: ≤ (1/2)^d
- Taking minimum: at least one row likely accurate

**Formal analysis:**

**Lemma:** For a single row j,
```
E[C[j, h_j(i)]] = f_i + N/w
```

**By Markov inequality:**
```
P[C[j, h_j(i)] > f_i + 2N/w] ≤ 1/2
```

**For d independent rows:**
```
P[min_j C[j, h_j(i)] > f_i + 2N/w] ≤ (1/2)^d
```

**Setting 2N/w = ε × N and (1/2)^d = δ:**
```
w = 2/ε
d = log(1/δ) / log(2) = log(1/δ)
```

### Properties

**1. One-sided error:**
- **Never under-estimates:** f̂_i ≥ f_i always
- May over-estimate due to collisions

**2. Error bound:**
```
f̂_i ≤ f_i + ε × N   with probability ≥ 1 - δ
```

**3. Relative error for high-frequency items:**
- For items with f_i >> ε × N, error is small relative to f_i
- For rare items, absolute error bounded but relative error can be large

**4. Mergeability:**
- Sketches with same w, d, hash functions can be merged
- Just add corresponding counters: C = C₁ + C₂

### Python Implementation

```python
import random

class CountMinSketch:
    """Count-Min Sketch for frequency estimation"""

    def __init__(self, epsilon, delta, prime=2**31-1):
        """
        Initialize Count-Min Sketch

        Args:
            epsilon: relative error
            delta: failure probability
            prime: prime for hash functions
        """
        self.epsilon = epsilon
        self.delta = delta
        self.w = int(2 / epsilon) + 1  # Width
        self.d = int(-1 * (1 / 2.718) * (delta / 2.718)) + 1  # Depth (approx log(1/delta))
        # Better: self.d = math.ceil(math.log(1/delta))

        self.p = prime
        self.counters = [[0] * self.w for _ in range(self.d)]

        # Generate hash function parameters
        self.a = [random.randint(1, self.p-1) for _ in range(self.d)]
        self.b = [random.randint(0, self.p-1) for _ in range(self.d)]

        self.N = 0  # Total items

        print(f"Count-Min Sketch created:")
        print(f"  w = {self.w} (width)")
        print(f"  d = {self.d} (depth)")
        print(f"  Space = {self.w * self.d * 4} bytes")

    def _hash(self, item, row):
        """Compute hash for item in given row"""
        # Convert item to integer if needed
        if isinstance(item, str):
            item = hash(item)

        return ((self.a[row] * item + self.b[row]) % self.p) % self.w

    def update(self, item, count=1):
        """
        Add item(s) to sketch

        Args:
            item: item to add
            count: number of times to add (default 1)
        """
        self.N += count

        for j in range(self.d):
            idx = self._hash(item, j)
            self.counters[j][idx] += count

    def estimate(self, item):
        """
        Estimate frequency of item

        Args:
            item: item to query

        Returns:
            estimated frequency (upper bound)
        """
        estimates = []
        for j in range(self.d):
            idx = self._hash(item, j)
            estimates.append(self.counters[j][idx])

        return min(estimates)

# Test
def test_count_min_sketch():
    # Create sketch
    cms = CountMinSketch(epsilon=0.01, delta=0.01)

    # Simulate stream
    stream = ['a'] * 100 + ['b'] * 50 + ['c'] * 25 + ['d'] * 10
    random.shuffle(stream)

    # Add other items with low frequency
    stream += ['e', 'f', 'g', 'h', 'i', 'j'] * 2

    # Process stream
    for item in stream:
        cms.update(item)

    # True frequencies
    from collections import Counter
    true_counts = Counter(stream)

    # Test queries
    print("\nFrequency estimates:")
    print(f"{'Item':<6} {'True':<6} {'Estimate':<10} {'Error':<8}")
    print("-" * 35)

    for item in sorted(true_counts.keys()):
        true_freq = true_counts[item]
        est_freq = cms.estimate(item)
        error = est_freq - true_freq

        print(f"{item:<6} {true_freq:<6} {est_freq:<10} {error:<8}")

    print(f"\nTotal items: {cms.N}")
    print(f"ε × N = {cms.epsilon * cms.N:.2f}")

test_count_min_sketch()
```

### Applications

**1. Natural Language Processing:**
- Track word frequencies
- N-gram statistics
- Vocabulary too large for exact counts

**2. Network monitoring:**
- Packet counts per source/destination
- Bandwidth usage per flow
- DDoS detection

**3. Database query optimization:**
- Cardinality estimation
- Join size estimation

**4. Web analytics:**
- Page view counts
- User action frequencies

---

## Finding Heavy-Hitters with Count-Min Sketch <a name="heavy-hitters"></a>

### Problem

**Goal:** Find all items with frequency > m/k

Using Count-Min Sketch for frequency estimation.

### Case 1: m Known in Advance

**Algorithm:**
```
FindHeavyHitters_Known(stream, k):
    ε = 1 / (2k)
    Initialize Count-Min Sketch with ε

    HH = empty set
    for each item i in stream:
        CountMinUpdate(i)
        est = CountMinEstimate(i)
        if est ≥ m/k:
            HH = HH ∪ {i}

    return HH
```

**Properties:**
- No false negatives (all heavy-hitters found)
- May have false positives (items with est > m/k but true < m/k)
- Space: O((k/ε) × log(1/δ)) = O(k log(1/δ))

### Case 2: m NOT Known in Advance

**Use MIN-HEAP to track heavy-hitter candidates!**

**Data structure:**
- Count-Min Sketch
- MIN-HEAP of (estimated_count, item) pairs

**Algorithm:**
```
FindHeavyHitters_Unknown(stream, k):
    ε = 1 / (2k)
    Initialize Count-Min Sketch with ε
    Initialize MIN-HEAP H (empty)
    n = 0  // Items processed

    for each item i in stream:
        n = n + 1
        CountMinUpdate(i)

        est = CountMinEstimate(i)

        if est ≥ n/k:
            if i in H:
                Update H with new estimate for i
            else:
                Insert (est, i) into H

        // Prune heap
        while H not empty and H.min().count < n/k:
            H.deleteMin()

    return items in H
```

**Complexity:**
- Update: O(d) for CM-Sketch + O(log |H|) for heap
- Space: O(w×d + k)

### Python Implementation

```python
import heapq

class HeavyHittersFinder:
    """Find heavy-hitters using Count-Min Sketch + Heap"""

    def __init__(self, k, epsilon=None, delta=0.01):
        """
        Args:
            k: find items with freq > m/k
            epsilon: CM-Sketch error (default 1/(2k))
            delta: CM-Sketch failure probability
        """
        self.k = k
        if epsilon is None:
            epsilon = 1 / (2 * k)

        self.cms = CountMinSketch(epsilon, delta)
        self.heap = []  # min-heap of (count, item)
        self.heap_set = set()  # items in heap
        self.n = 0  # items processed

    def update(self, item):
        """Process one item"""
        self.n += 1
        self.cms.update(item)

        est = self.cms.estimate(item)
        threshold = self.n / self.k

        if est >= threshold:
            if item in self.heap_set:
                # Update: remove old, add new
                # (Heap doesn't support decrease-key, so we add duplicate)
                heapq.heappush(self.heap, (est, item))
            else:
                heapq.heappush(self.heap, (est, item))
                self.heap_set.add(item)

        # Prune heap
        while self.heap and self.heap[0][0] < threshold:
            _, item = heapq.heappop(self.heap)
            self.heap_set.discard(item)

    def get_heavy_hitters(self):
        """Get current heavy-hitter candidates"""
        # Return unique items with current estimates
        result = {}
        for item in self.heap_set:
            result[item] = self.cms.estimate(item)
        return result

# Test
def test_heavy_hitters():
    stream = ['a'] * 100 + ['b'] * 50 + ['c'] * 25 + ['d'] * 10
    stream += ['e', 'f', 'g'] * 2
    random.shuffle(stream)

    k = 5  # Find items with freq > m/5
    hhf = HeavyHittersFinder(k)

    for item in stream:
        hhf.update(item)

    hh = hhf.get_heavy_hitters()

    print(f"Heavy-hitters (freq > {hhf.n}/{k} = {hhf.n/k:.1f}):")
    for item, est in sorted(hh.items(), key=lambda x: x[1], reverse=True):
        print(f"  {item}: {est}")

    # Verify
    from collections import Counter
    true = Counter(stream)
    print("\nTrue frequencies:")
    for item, freq in sorted(true.items(), key=lambda x: x[1], reverse=True):
        is_hh = freq > hhf.n / k
        print(f"  {item}: {freq} {'✓ HH' if is_hh else ''}")

test_heavy_hitters()
```

---

## THE COUNT SKETCH <a name="count-sketch"></a>

### Overview (Charikar et al., 2004)

**Alternative to Count-Min Sketch** with different properties.

**Key differences:**
1. Uses **signed updates** (+1 or -1)
2. Takes **MEDIAN** instead of minimum
3. **Unbiased estimator**
4. Different error guarantee

### Structure

**Same 2D array: w × d**

But now **TWO hash functions per row:**
```
h_j(i): maps item to [0, w-1]         (which column?)
g_j(i): maps item to {-1, +1}         (sign?)
```

**Update:** Add g_j(i) to C[j, h_j(i)]
- If g_j(i) = +1: increment
- If g_j(i) = -1: decrement

### Operations

**1. Initialization:**
```
CountSketchInit(w, d):
    C[1..d, 1..w] = 0

    for j = 1 to d:
        Generate h_j (maps to [w])
        Generate g_j (maps to {-1, +1})
```

**2. Update:**
```
CountSketchUpdate(i):
    for j = 1 to d:
        col = h_j(i)
        sign = g_j(i)
        C[j, col] = C[j, col] + sign
```

**3. Query:**
```
CountSketchEstimate(i):
    estimates = []

    for j = 1 to d:
        col = h_j(i)
        sign = g_j(i)
        est_j = sign × C[j, col]
        estimates.append(est_j)

    return median(estimates)
```

**Key difference:** MEDIAN instead of MIN!

### Why Signed Updates?

**Idea:** Cancellation of errors

**For item i in row j:**
```
C[j, h_j(i)] = g_j(i) × f_i + Σ(collision noise)
```

**Multiplying by g_j(i):**
```
g_j(i) × C[j, h_j(i)] = f_i + Σ(signed noise)
```

**Noise cancels out in expectation!**
- Items colliding with i have random signs
- Expected contribution: 0
- Unbiased estimator!

### Unbiased Estimator

**For each row j:**
```
E[g_j(i) × C[j, h_j(i)]] = f_i
```

**Proof:**
- g_j(i) × g_j(i) = 1 (same item)
- E[g_j(i) × g_j(k)] = 0 (different items, independent)
- Only f_i survives in expectation

**Count-Min comparison:**
- Count-Min: E[estimate] = f_i + collision_weight (biased)
- Count Sketch: E[estimate] = f_i (unbiased!)

### Error Guarantee

**Different from Count-Min!**

**Count-Min:** Error ≤ ε × N
**Count Sketch:** Error ≤ ε × ||F||₂

where ||F||₂ = √(Σ f_i²) is the **second frequency moment**

**For skewed distributions:** ||F||₂ << N
→ Count Sketch can have better error!

### Parameter Selection

**Goal:** Error ≤ ε × ||F||₂ with probability ≥ (1 - δ)

**Parameters:**
```
d = ⌈log(4/δ)⌉

w = ⌈e/ε²⌉ = O(1/ε²)
```

**Note: w = O(1/ε²)** vs Count-Min's w = O(1/ε)
- Count Sketch needs more columns!

**Space:**
```
S = O((1/ε²) × log(1/δ))
```

**Comparison:**
- Count-Min: O((1/ε) × log(1/δ))
- Count Sketch: O((1/ε²) × log(1/δ)) - **quadratic** in 1/ε!

### When to Use Count Sketch?

**Advantages:**
- Unbiased estimator
- Better for skewed distributions (small ||F||₂)
- Can handle deletions (negative updates)

**Disadvantages:**
- More space (quadratic in 1/ε)
- More complex (median vs min)

**Rule of thumb:**
- **Uniform distribution:** Count-Min better
- **Highly skewed:** Count Sketch better (if ||F||₂ << N)

### Relationship to Count-Min

**Count-Min is special case of Count Sketch!**

**If we set g_j(i) = +1 for all items:**
- Signed updates become regular increments
- Median becomes minimum (no negative values)
- Count Sketch reduces to Count-Min!

### Python Implementation

```python
import random
import statistics

class CountSketch:
    """Count Sketch with signed updates"""

    def __init__(self, epsilon, delta, prime=2**31-1):
        """
        Args:
            epsilon: relative error
            delta: failure probability
        """
        self.epsilon = epsilon
        self.delta = delta
        self.w = int(2.718 / (epsilon ** 2)) + 1
        self.d = int(0.693 * 4 / delta) + 1  # approx log(4/delta)

        self.p = prime
        self.counters = [[0] * self.w for _ in range(self.d)]

        # Hash functions for column
        self.a_h = [random.randint(1, self.p-1) for _ in range(self.d)]
        self.b_h = [random.randint(0, self.p-1) for _ in range(self.d)]

        # Hash functions for sign
        self.a_g = [random.randint(1, self.p-1) for _ in range(self.d)]
        self.b_g = [random.randint(0, self.p-1) for _ in range(self.d)]

        print(f"Count Sketch created:")
        print(f"  w = {self.w} (width)")
        print(f"  d = {self.d} (depth)")

    def _hash_column(self, item, row):
        """Hash to column [0, w-1]"""
        if isinstance(item, str):
            item = hash(item)
        return ((self.a_h[row] * item + self.b_h[row]) % self.p) % self.w

    def _hash_sign(self, item, row):
        """Hash to sign {-1, +1}"""
        if isinstance(item, str):
            item = hash(item)
        val = ((self.a_g[row] * item + self.b_g[row]) % self.p) % 2
        return 1 if val == 0 else -1

    def update(self, item, count=1):
        """Add item with signed updates"""
        for j in range(self.d):
            col = self._hash_column(item, j)
            sign = self._hash_sign(item, j)
            self.counters[j][col] += sign * count

    def estimate(self, item):
        """Estimate frequency using median"""
        estimates = []
        for j in range(self.d):
            col = self._hash_column(item, j)
            sign = self._hash_sign(item, j)
            est = sign * self.counters[j][col]
            estimates.append(est)

        return statistics.median(estimates)

# Test
def test_count_sketch():
    cs = CountSketch(epsilon=0.01, delta=0.01)

    stream = ['a'] * 100 + ['b'] * 50 + ['c'] * 25
    random.shuffle(stream)

    for item in stream:
        cs.update(item)

    from collections import Counter
    true_counts = Counter(stream)

    print("\nCount Sketch estimates:")
    for item in sorted(true_counts.keys()):
        true_freq = true_counts[item]
        est_freq = cs.estimate(item)
        error = abs(est_freq - true_freq)

        print(f"{item}: true={true_freq}, est={est_freq:.1f}, error={error:.1f}")

test_count_sketch()
```

---

## Recent Advances in Sketches

**2016 - Augmented Sketch:**
- Combines heavy-hitters with sketch
- Better accuracy for frequent items

**2018 - Elastic Sketch:**
- Adaptive allocation between heavy and light parts
- Better space utilization

**2018 - CountMax Sketch:**
- Uses maximum instead of minimum
- Different error characteristics

**2021 - Clock-Sketch:**
- Time-aware frequency estimation
- Sliding window support

**2022 - LU-Sketch:**
- Learned updates
- Machine learning integration

---

# SLIDE 13: DISTINCT ELEMENTS <a name="slide-13"></a>

## The DISTINCT-ELEMENTS Problem

### Problem Definition

**Given stream:** σ = [a₁, a₂, ..., a_m]

**Set of distinct items:**
```
D = {j : f_j > 0}

where f_j = frequency of item j
```

**Goal:** Estimate **#D = |D|** (cardinality)

**Output:** (ε, δ)-approximation of #D

### Why It's Hard

**Theorem:** Impossible to solve in sublinear space using:
- Deterministic algorithm (δ = 0), OR
- Exact algorithm (ε = 0)

**Therefore:** Must use **randomized approximation**!

### Applications

**1. Website analytics:**
- Unique users per month
- Distinct IP addresses

**2. E-commerce:**
- Distinct products sold
- Unique customers

**3. Search engines:**
- Unique queries
- Distinct words in crawled pages

**4. Network monitoring:**
- Distinct flows
- Unique sources/destinations

---

## Direct (Exact) Approaches <a name="direct-approaches"></a>

### 1. Bitmap and Bit Counting

**Idea:** Use bitmap of size N (universe size)

**Algorithm:**
```
Bitmap(stream, N):
    B = array of N bits, all 0

    for each item i in stream:
        B[i] = 1

    return count_ones(B)
```

**Complexity:**
- Space: O(N) bits
- Time: O(m) for stream + O(N) for counting

**Problem:** N can be HUGE!
- IP addresses: N = 2³² (4 billion)
- URLs: N is unbounded!

### 2. Sorting and Eliminating Duplicates

**Algorithm:**
```
Sort_Unique(stream):
    A = array of m items from stream
    Sort A
    Count distinct elements (adjacent duplicates)
```

**Linux command:**
```bash
sort -u file.txt | wc -l
```

**Complexity:**
- Space: O(m)
- Time: O(m log m)

**Problem:** Impractical for huge data sets!

### 3. Hashing and Counting

**Algorithm:**
```
Hash_Count(stream):
    H = empty hash table

    for each item i in stream:
        if i not in H:
            H.insert(i)

    return |H|
```

**Complexity:**
- Space: O(n) where n = #distinct
- Time: O(m) expected

**Problems:**
- Hash table must fit in memory
- Load factor considerations
- n can be very large!

### Approximate Method: Hash Without Collision Handling

**Idea:** Don't resolve collisions!

**Algorithm:**
```
Hash_NoCollision(stream, table_size):
    B = array of table_size bits, all 0
    count = 0

    for each item i in stream:
        h = hash(i)
        if B[h] == 0:
            B[h] = 1
            count++

    return count  // or count × correction_factor
```

**Properties:**
- Underestimates (collisions not inserted)
- Can add statistical correction factor
- Space: O(table_size) bits

### Bloom Filter for Cardinality

**Algorithm:**
```
BF_Cardinality(stream, m, k):
    BF = Bloom Filter with m bits, k hash functions
    count = 0

    for each item i in stream:
        if i NOT in BF:
            BF.insert(i)
            count++

    return count
```

**Properties:**
- Cannot over-estimate (no false negatives!)
- Can underestimate (false positives prevent insertion)
- Can add correction factor

---

## Flajolet-Martin Algorithm (1985) <a name="flajolet-martin"></a>

### The Brilliant Idea

**Key insight:** Count trailing zeros in hash values!

**Intuition:**
- About 50% of numbers end in 0 (binary)
- About 25% end in 00
- About 12.5% end in 000
- ...

**If we see r trailing zeros:**
- Probably seen about 2^r distinct elements!

### The Algorithm

**Step 1:** Choose hash function
```
h: items → bit strings of length ≥ log₂(n)

Requirements:
- Deterministic (same input → same output)
- 2-universal
- At least log₂(n) bits output
```

**Step 2:** Define trailing zeros function
```
zeros(a) = max{i : 2^i divides h(a)}
        = number of trailing zeros in binary representation of h(a)
        = position of rightmost 1-bit

Examples:
h(a) = ...1000 → zeros(a) = 3
h(a) = ...0001 → zeros(a) = 0
h(a) = ...0110 → zeros(a) = 1
```

**Step 3:** Track maximum
```
R = max{zeros(a_k)} for all items in stream
```

**Step 4:** Estimate cardinality
```
Estimate = 2^R  (or 2^R + 1/2 with correction)
```

### Why It Works

**Probability analysis:**

**For random hash values:**
```
P(zeros(a) ≥ r) = P(binary ends in r or more zeros)
                = P(divisible by 2^r)
                = 1 / 2^r
```

**Expected behavior:**
- If we've seen k distinct elements
- Expected max trailing zeros ≈ log₂(k)
- Therefore 2^(max) ≈ k

**Formal statement:**
```
If k distinct elements:
- P(R ≥ r) → 1   if k >> 2^r  (very likely to see r zeros)
- P(R ≥ r) → 0   if k << 2^r  (very unlikely)

Therefore: 2^R will be around k
```

### Worked Example

**Stream:** σ = [3, 1, 4, 1, 5, 9, 2, 6, 5]

**Hash function (for example):**
```
h₁(x) = (2x + 1) mod 32
Represent as 5-bit binary
```

**Compute hash and trailing zeros:**

```
Item | Hash h₁(x) | Binary  | Trailing 0s
-----|------------|---------|------------
  3  |     7      | 00111   |     0
  1  |     3      | 00011   |     0
  4  |     9      | 01001   |     0
  1  |     3      | 00011   |     0  (duplicate)
  5  |    11      | 01011   |     0
  9  |    19      | 10011   |     0
  2  |     5      | 00101   |     0
  6  |    13      | 01101   |     0
  5  |    11      | 01011   |     0  (duplicate)

Max trailing zeros: R = 0
Estimate: 2^0 = 1
```

**Actual distinct:** 7 items

**Problem:** This hash function is bad! (odd × 2 + 1 always gives odd number)

**Better hash:**
```
h₂(x) = (3x + 7) mod 32

Item | Hash h₂(x) | Binary  | Trailing 0s
-----|------------|---------|------------
  3  |    16      | 10000   |     4  ★
  1  |    10      | 01010   |     1
  4  |    19      | 10011   |     0
  1  |    10      | 01010   |     1  (dup)
  5  |    22      | 10110   |     1
  9  |     2      | 00010   |     1
  2  |    13      | 01101   |     0
  6  |    25      | 11001   |     0
  5  |    22      | 10110   |     1  (dup)

Max trailing zeros: R = 4
Estimate: 2^4 = 16
```

**Actual:** 7, **Estimate:** 16 (overestimate, but in right ballpark!)

### Improving Accuracy: Multiple Hash Functions

**Problem:** Single hash gives high variance

**Solution:** Use **many hash functions** h₁, h₂, ..., h_m

**For each hash:**
```
R_i = max{zeros_i(a)} using hash h_i
Estimate_i = 2^{R_i}
```

**Combining estimates:**

**Bad:** Simple average
- Problem: One outlier can skew result

**Bad:** Median
- Problem: All estimates are powers of 2
- Median might not be close if #distinct between powers

**GOOD:** Average of medians (grouping)
1. Partition m hash functions into g groups
2. Compute average within each group
3. Take median of the g averages

**Example:** 90 hash functions
- Split into 9 groups of 10
- Average within each group → 9 values
- Median of 9 values → final estimate

### Space Complexity

**Per hash function:**
- Store R: O(log log n) bits
  - R ≤ log₂(n)
  - Storing R needs log₂(log₂(n)) bits

**Total with m hash functions:**
```
Space = m × O(log log n)
```

**Incredibly small!**

**Example:** n = 1 billion
- log₂(10⁹) ≈ 30
- log₂(30) ≈ 5 bits per hash
- 1000 hash functions → 5000 bits ≈ 625 bytes!

### Time Complexity

**Per item:**
- Compute hash: O(1)
- Count trailing zeros: O(log n) worst case
- Update max: O(1)

**Total:** O(m) items × O(m_hash × log n)

**Limitation:** Computing many hash functions is slow!

### Python Implementation

```python
import random
import statistics

def trailing_zeros(n):
    """Count trailing zeros in binary representation"""
    if n == 0:
        return 0
    count = 0
    while (n & 1) == 0:
        count += 1
        n >>= 1
    return count

class FlajoletMartin:
    """Flajolet-Martin algorithm for cardinality estimation"""

    def __init__(self, num_hashes=32, prime=2**31-1):
        """
        Args:
            num_hashes: number of hash functions
            prime: prime for hash functions
        """
        self.m = num_hashes
        self.p = prime

        # Generate hash functions
        self.a = [random.randint(1, prime-1) for _ in range(num_hashes)]
        self.b = [random.randint(0, prime-1) for _ in range(num_hashes)]

        # Track max trailing zeros for each hash
        self.R = [0] * num_hashes

    def _hash(self, item, idx):
        """Compute hash value"""
        if isinstance(item, str):
            item = hash(item)
        return (self.a[idx] * item + self.b[idx]) % self.p

    def add(self, item):
        """Add item to stream"""
        for i in range(self.m):
            h_val = self._hash(item, i)
            zeros = trailing_zeros(h_val)
            self.R[i] = max(self.R[i], zeros)

    def estimate(self):
        """Estimate cardinality"""
        # Simple estimate: average of 2^R_i
        estimates = [2 ** r for r in self.R]
        return statistics.mean(estimates)

    def estimate_grouped(self, groups=None):
        """Estimate using grouped median-of-averages"""
        if groups is None:
            groups = max(1, self.m // 10)  # Default: 10 per group

        group_size = self.m // groups
        group_estimates = []

        for g in range(groups):
            start = g * group_size
            end = start + group_size
            group_R = self.R[start:end]
            avg = statistics.mean([2 ** r for r in group_R])
            group_estimates.append(avg)

        return statistics.median(group_estimates)

# Test
def test_flajolet_martin():
    # Create estimator
    fm = FlajoletMartin(num_hashes=90)

    # Generate stream with known distinct count
    distinct_items = list(range(1000))
    stream = distinct_items * 3  # Each item appears 3 times
    random.shuffle(stream)

    # Process stream
    for item in stream:
        fm.add(item)

    # Estimate
    est_simple = fm.estimate()
    est_grouped = fm.estimate_grouped(groups=9)

    print(f"True distinct count: {len(distinct_items)}")
    print(f"Estimate (average): {est_simple:.0f}")
    print(f"Estimate (grouped): {est_grouped:.0f}")
    print(f"Error (average): {abs(est_simple - len(distinct_items)) / len(distinct_items) * 100:.1f}%")
    print(f"Error (grouped): {abs(est_grouped - len(distinct_items)) / len(distinct_items) * 100:.1f}%")

test_flajolet_martin()
```

---

## HyperLogLog Algorithm (2007) <a name="hyperloglog"></a>

### Overview

**Authors:** Flajolet, Fusy, Gandouet, Meunier (2007)

**Key idea:** Near-optimal probabilistic algorithm for cardinality estimation

**Refinement of Flajolet-Martin:**
- Better accuracy
- Better use of hash bits
- Stochastic averaging

### The Algorithm (Practical Variant)

**Step 1: Hash and split**
```
For each item:
- Compute hash h(item) → bit string
- First p bits: bucket index (2^p buckets)
- Remaining bits: count trailing zeros
```

**Step 2: Update buckets**
```
M[1..2^p] = array of max trailing zeros per bucket

For each item x:
    j = first p bits of h(x)         // bucket
    w = remaining bits of h(x)
    M[j] = max(M[j], zeros(w) + 1)
```

**Step 3: Estimate cardinality**
```
Harmonic mean of 2^{M[j]}:

E = α_m × m² × (Σ 2^{-M[j]})^{-1}

where:
- m = 2^p (number of buckets)
- α_m = correction constant ≈ 0.7213/(1 + 1.079/m)
```

### Why Harmonic Mean?

**Arithmetic mean:** Sensitive to outliers
- One large value skews result up

**Harmonic mean:** Robust to outliers
- Weighted toward smaller values
- Better for averaging rates/ratios

**Formula:**
```
HM = n / (Σ 1/x_i)
```

For powers of 2:
```
HM = m / (Σ 2^{-M[j]})
```

### Parameters

**Precision parameter p:**
- Determines number of buckets: m = 2^p
- Typical: p = 10 to 16
  - p = 10 → 1024 buckets
  - p = 14 → 16384 buckets

**Space:**
- Each bucket: log₂(log₂(n)) bits
- Total: 2^p × log₂(log₂(n)) bits

**Example:** p = 14, n = 10⁹
- Buckets: 16384
- Bits per bucket: log₂(30) ≈ 5
- Total: 16384 × 5 bits ≈ 10 KB

**Accuracy:**
- Standard error ≈ 1.04 / √m
- p = 14 (m = 16384) → error ≈ 0.81%

### HyperLogLog++ (Google, 2013)

**Improvements:**
1. **64-bit hash codes** (not 32-bit)
   - Can estimate > 1 billion distinct items

2. **Bias correction** for small cardinalities
   - Near-exact for small counts

3. **Sparse representation** for small sets
   - Use less memory when few distinct items

4. **Improved estimation** formula

**Used in production at Google!**
- Count distinct queries over time
- Unique user tracking
- Large-scale analytics

### Requirements at Google

**1. Accuracy:**
- Accurate estimates for fixed memory
- Near-exact for small cardinalities

**2. Memory efficiency:**
- Efficient use of space
- Adaptive to actual cardinality

**3. Large cardinalities:**
- Handle > 1 billion distinct items
- Reasonable accuracy

**4. Practicality:**
- Implementable and maintainable
- Not overly complex

**HyperLogLog++ meets all requirements!**

### Comparison: Theoretical vs Practical

**Kane et al. (2010):**
- Optimal space complexity
- Meets theoretical lower bound
- BUT: Too complex for practical implementation

**HyperLogLog++:**
- Near-optimal (within constant factor)
- Practical and maintainable
- Actually used in production!

**Lesson:** Sometimes "good enough" > "optimal"

### Recent Advances

**2017 - UltraLogLog:**
- Even better accuracy
- Further optimizations

**2019 - Deep Cardinality Estimation:**
- Machine learning approaches
- Learned estimators

**2022 - Learned Cardinality Estimation:**
- Neural networks for estimation
- Data-dependent optimization

### Python Implementation (Simplified HyperLogLog)

```python
import math
import mmh3  # MurmurHash3 (install: pip install mmh3)

class HyperLogLog:
    """Simplified HyperLogLog implementation"""

    def __init__(self, p=14):
        """
        Args:
            p: precision parameter (4 <= p <= 16)
        """
        self.p = p
        self.m = 1 << p  # 2^p buckets
        self.M = [0] * self.m  # Bucket max values

        # Correction constant
        if self.m >= 128:
            self.alpha = 0.7213 / (1 + 1.079 / self.m)
        elif self.m >= 64:
            self.alpha = 0.709
        elif self.m >= 32:
            self.alpha = 0.697
        else:
            self.alpha = 0.673

    def _hash(self, item):
        """Compute 32-bit hash"""
        if isinstance(item, str):
            item = item.encode('utf-8')
        return mmh3.hash(item, signed=False)

    def add(self, item):
        """Add item to stream"""
        # Get 32-bit hash
        h = self._hash(item)

        # Split into bucket index and trailing zero count
        j = h & ((1 << self.p) - 1)  # First p bits
        w = h >> self.p  # Remaining bits

        # Count leading zeros in w (equivalent to trailing in original FM)
        # Python: use bit_length to find position of leftmost 1
        leading_zeros = 32 - self.p - w.bit_length() + 1 if w > 0 else 32 - self.p

        # Update bucket maximum
        self.M[j] = max(self.M[j], leading_zeros)

    def estimate(self):
        """Estimate cardinality"""
        # Raw estimate using harmonic mean
        raw_estimate = self.alpha * (self.m ** 2) / sum(2 ** (-x) for x in self.M)

        # Small range correction
        if raw_estimate <= 2.5 * self.m:
            # Count zero buckets
            zeros = self.M.count(0)
            if zeros != 0:
                return self.m * math.log(self.m / zeros)

        # No correction for intermediate range

        # Large range correction
        if raw_estimate > (1/30) * (1 << 32):
            return -(1 << 32) * math.log(1 - raw_estimate / (1 << 32))

        return raw_estimate

# Test
def test_hyperloglog():
    hll = HyperLogLog(p=14)

    # Generate stream
    distinct_count = 10000
    stream = list(range(distinct_count)) * 5  # Each item 5 times
    random.shuffle(stream)

    # Add to HLL
    for item in stream:
        hll.add(item)

    # Estimate
    estimate = hll.estimate()
    error = abs(estimate - distinct_count) / distinct_count * 100

    print(f"HyperLogLog (p={hll.p}, {hll.m} buckets)")
    print(f"True distinct: {distinct_count}")
    print(f"Estimate: {estimate:.0f}")
    print(f"Error: {error:.2f}%")
    print(f"Expected error: ~{104/math.sqrt(hll.m):.2f}%")

test_hyperloglog()
```

---

# PRACTICE PROBLEMS <a name="practice-problems"></a>

## EASY

**1. Boyer-Moore MJRTY**
```
Stream: [1, 2, 1, 1, 3, 1, 2, 1]

a) Run first pass. What is the candidate?
b) Run second pass. Is there a majority?
c) What is the final counter value after first pass?

Solution:
a) Candidate = 1
b) Yes, 1 appears 5 times > 8/2
c) Counter = 3 (final state)
```

**2. Misra-Gries with k=2**
```
Stream: [a, b, a, c, a, b, a]
k = 2, threshold = 7/2 = 3.5

Run the algorithm. What items are tracked?

Solution:
Since k=2, this reduces to Boyer-Moore!
Final: {a: counter_value}
a appears 4 times > 3.5 → Heavy-hitter
```

**3. Count-Min Sketch Parameters**
```
Requirement: Error ≤ 1% with 95% certainty

Calculate:
a) ε = ?
b) δ = ?
c) w = ?
d) d = ?

Solution:
a) ε = 0.01
b) δ = 0.05
c) w = ⌈2/0.01⌉ = 200
d) d = ⌈log(1/0.05)⌉ = ⌈log(20)⌉ = ⌈4.32⌉ = 5
```

## MEDIUM

**4. Misra-Gries Step-by-Step**
```
Stream: [3, 1, 3, 2, 3, 4, 3]
k = 3, max counters = 2

Complete the execution trace.

Solution:
Step 1: {3:1}
Step 2: {3:1, 1:1}
Step 3: {3:2, 1:1}
Step 4: Decrement all → {3:1}
Step 5: {3:2}
Step 6: {3:2, 4:1}
Step 7: {3:3, 4:1}

Final: {3:3, 4:1}
True: 3 appears 4 times, 4 appears 1 time
```

**5. Count-Min Sketch Query**
```
CMS with w=5, d=3, N=20

Counter values after processing:
Row 1: [2, 5, 3, 4, 2]
Row 2: [3, 2, 6, 2, 3]
Row 3: [4, 3, 2, 5, 1]

Item x hashes to:
h₁(x)=1, h₂(x)=2, h₃(x)=3

a) What is estimated frequency?
b) What is error bound?

Solution:
a) Counters: C[1,1]=2, C[2,2]=6, C[3,3]=5
   Estimate = min(2, 6, 5) = 2

b) Error bound = ε × N (need ε from initialization)
   If ε = 2/w = 2/5 = 0.4
   Error ≤ 0.4 × 20 = 8
```

**6. Flajolet-Martin Example**
```
Hash function: h(x) = (3x) mod 16

Stream: [2, 5, 7, 2, 9]

a) Compute hash and trailing zeros for each item
b) What is R (max trailing zeros)?
c) Estimate of distinct count?
d) True distinct count?

Solution:
a) 2: h=6=0110 (1 zero)
   5: h=15=1111 (0 zeros)
   7: h=5=0101 (0 zeros)
   9: h=11=1011 (0 zeros)

b) R = max(1, 0, 0, 0) = 1

c) Estimate = 2^1 = 2

d) True: 4 distinct items {2, 5, 7, 9}
```

## HARD

**7. Space-Saving Replacement**
```
Stream: [a, b, c, d, a, e, b]
k = 3

Trace execution including which item gets replaced.

Solution:
Step 1: a → {a:1}
Step 2: b → {a:1, b:1}
Step 3: c → {a:1, b:1, c:1}
Step 4: d → min is a/b/c (pick a), replace → {d:2, b:1, c:1}
Step 5: a → min is b/c, replace b → {d:2, a:2, c:1}
Step 6: e → min is c, replace → {d:2, a:2, e:2}
Step 7: b → min is d/a/e, replace d → {b:3, a:2, e:2}

Final: {b:3, a:2, e:2}
```

**8. Count-Min vs Count Sketch**
```
For stream with N=10000 items:
- Uniform: each of 100 items appears 100 times
- Skewed: 1 item appears 9000 times, 100 others appear 10 times each

a) Calculate ||F||₂ for each
b) Which sketch is better for each distribution?

Solution:
a) Uniform: ||F||₂ = √(100 × 100²) = √(10⁶) = 1000
   Skewed: ||F||₂ = √(9000² + 100×10²) ≈ √(81×10⁶) ≈ 9000

b) Count-Min error: ε × N
   Count Sketch error: ε × ||F||₂

   Uniform: ||F||₂/N = 1000/10000 = 0.1
   → Count Sketch error 10× smaller!

   Skewed: ||F||₂/N = 9000/10000 = 0.9
   → Count Sketch error only slightly smaller
```

**9. HyperLogLog Buckets**
```
p = 4 (16 buckets)

Hash values (first 4 bits | remaining):
- Item a: 0011 | 01000... (zeros(remaining) = 3)
- Item b: 0011 | 00010... (zeros = 4)
- Item c: 1010 | 10000... (zeros = 0)

a) Update bucket values
b) If all other buckets remain 0, estimate cardinality

Solution:
a) Bucket 3 (binary 0011): M[3] = max(0, 3+1, 4+1) = 5
   Bucket 10 (binary 1010): M[10] = 0+1 = 1
   Others: M[i] = 0

b) Raw = α₁₆ × 16² × (Σ 2^{-M[i]})^{-1}
   ≈ 0.673 × 256 × (14×1 + 2^{-5} + 2^{-1})^{-1}
   ≈ 0.673 × 256 × (14.53)^{-1}
   ≈ 11.9

   True distinct: 3
   (Small counts need correction!)
```

## CHALLENGE

**10. Implement and Compare**
```
Task: Implement Misra-Gries, Lossy-Counting, and Space-Saving.

Generate stream with Zipfian distribution:
- 100 distinct items
- Item i has frequency ∝ 1/i
- Total m = 10000 items

a) Compare accuracy for k=10
b) Measure running time
c) Which is best?

(No solution provided - implement yourself!)
```

---

# SUMMARY & EXAM TIPS <a name="summary"></a>

## Key Algorithms Summary

### Finding Frequent Items

| Algorithm | Space | Time/item | Guarantees |
|-----------|-------|-----------|------------|
| Boyer-Moore MJRTY | O(1) | O(1) | Finds majority (freq > m/2) |
| Misra-Gries | O(k log m) | O(log k) avg | Finds freq > m/k, no false neg |
| Lossy-Counting | O(1/ε log m) | O(1) amort | Error ≤ ε×m |
| Space-Saving | O(k log m) | O(log k) | All freq > ε×m found |

### Sketch Algorithms

| Algorithm | Space | Update | Query | Error |
|-----------|-------|--------|-------|-------|
| Count-Min | O(1/ε × log 1/δ) | O(log 1/δ) | O(log 1/δ) | ≤ ε×N w.p. ≥ 1-δ |
| Count | O(1/ε² × log 1/δ) | O(log 1/δ) | O(log 1/δ) | ≤ ε×||F||₂ w.p. ≥ 1-δ |

### Cardinality Estimation

| Algorithm | Space | Error | Notes |
|-----------|-------|-------|-------|
| Flajolet-Martin | O(m log log n) | High variance | Use many hashes |
| HyperLogLog | O(2^p log log n) | ~1.04/√(2^p) | Near-optimal |
| HyperLogLog++ | O(2^p log log n) | Better | Google's version |

## Key Formulas

### Count-Min Sketch
```
w = ⌈2/ε⌉
d = ⌈log(1/δ)⌉
Space = O(1/ε × log 1/δ)
Error: f̂_i ≤ f_i + ε×N with prob ≥ 1-δ
```

### Count Sketch
```
w = O(1/ε²)
d = ⌈log(4/δ)⌉
Space = O(1/ε² × log 1/δ)
Error: |f̂_i - f_i| ≤ ε×||F||₂ with prob ≥ 1-δ
```

### Flajolet-Martin
```
R = max{zeros(h(a_i))}
Estimate = 2^R
Space = m × O(log log n) for m hash functions
```

### HyperLogLog
```
m = 2^p buckets
E = α_m × m² / (Σ 2^{-M[j]})
Standard error ≈ 1.04 / √m
Space = m × log log n bits
```

## Important Concepts

**1. Data Stream Model:**
- One pass only
- No random access
- Sublinear space
- (ε, δ)-approximation

**2. Heavy-Hitters:**
- Items with freq > m/k
- At most k-1 such items
- No false negatives (key property!)

**3. One-sided vs Two-sided Error:**
- One-sided: only over-estimate OR only under-estimate
- Two-sided: can err in both directions
- Count-Min: one-sided (over-estimates)
- Count Sketch: two-sided (unbiased)

**4. Sketches:**
- Linear transforms
- Hash-based
- Mergeability
- Fast updates

**5. Cardinality:**
- Trailing zeros ≈ log₂(count)
- Harmonic mean for averaging
- Small space: log log n

## Common Exam Questions

**1. Run algorithm step-by-step:**
- Boyer-Moore on sequence
- Misra-Gries with given k
- Space-Saving replacements

**2. Calculate parameters:**
- Count-Min: given ε, δ → find w, d
- Space requirements
- Error bounds

**3. Analyze complexity:**
- Time per operation
- Space usage
- Compare algorithms

**4. Probability calculations:**
- Trailing zeros probability
- Hash collision analysis
- Error probability

**5. Choose right algorithm:**
- When to use Count-Min vs Count Sketch?
- Exact vs approximate methods
- Trade-offs in practice

## Study Tips

**1. Master the fundamentals:**
- Understand WHY each algorithm works
- Don't just memorize pseudocode
- Practice examples by hand

**2. Key insights:**
- MJRTY: pair annihilation
- Misra-Gries: decrement all
- Count-Min: minimum over hashes
- Count Sketch: signed updates, median
- Flajolet-Martin: trailing zeros ~ log

**3. Parameter calculations:**
- Practice computing w, d from ε, δ
- Understand space/accuracy trade-offs
- Know when to use each formula

**4. Implementations:**
- Code at least one from each category
- Understand data structure choices
- Hash functions, heaps, dictionaries

**5. Comparisons:**
- Know when each algorithm is best
- Understand error types
- Space vs time trade-offs

## Quick Reference

**Boyer-Moore (MJRTY):**
```python
candidate = None; counter = 0
for x in stream:
    if counter == 0: candidate = x; counter = 1
    elif x == candidate: counter += 1
    else: counter -= 1
# Verify candidate in second pass
```

**Misra-Gries:**
```python
# Max k-1 counters
if item in A: A[item] += 1
elif len(A) < k-1: A[item] = 1
else: decrement_all(); remove_zeros()
```

**Count-Min Sketch:**
```python
# Update
for j in 1..d:
    C[j][h_j(item)] += 1

# Query
return min(C[j][h_j(item)] for j in 1..d)
```

**Flajolet-Martin:**
```python
R = max(trailing_zeros(hash(item)) for item in stream)
estimate = 2 ** R
```

## Final Advice

**Before exam:**
1. Review all algorithms
2. Practice calculations
3. Code key algorithms
4. Understand trade-offs
5. Sleep well!

**During exam:**
1. Read carefully
2. Identify algorithm needed
3. Show all work
4. Check units (m vs n vs k)
5. Verify answers make sense

**Good luck! 🎓**

---

## References

### Finding Frequent Items

- R. Boyer & J. Moore, "MJRTY – A fast majority vote algorithm," Automated Reasoning: Essays in Honor of Woody Bledsoe, Springer, 1991

- J. Misra & D. Gries, "Finding repeated elements," Science of Computer Programming, Vol. 2, 1982

- G. Cormode & M. Hadjieleftheriou, "Finding the frequent items in streams of data," Communications of the ACM, Vol. 52, N. 10, 2009

### Sketch Algorithms

- G. Cormode & S. Muthukrishnan, "An improved data stream summary: the count-min sketch and its applications," Journal of Algorithms, 2005

- M. Charikar et al., "Finding frequent items in data streams," Theoretical Computer Science, 2004

- G. Cormode et al., "Synopses for Massive Data: Samples, Histograms, Wavelets, Sketches," Foundations and Trends in Databases, Vol. 4, 2012

### Cardinality Estimation

- P. Flajolet & G. Martin, "Probabilistic counting algorithms for data base applications," Journal of Computer and System Sciences, 1985

- P. Flajolet et al., "HyperLogLog: the analysis of a near-optimal cardinality estimation algorithm," 2007

- S. Heule et al., "HyperLogLog in Practice: Algorithmic Engineering of a State of The Art Cardinality Estimation Algorithm," Google Inc., 2013

### General

- J. Leskovec, A. Rajaraman & J. Ullman, "Mining of Massive Datasets," 2nd Ed., Cambridge University Press, 2014

---

*End of Study Guide*
