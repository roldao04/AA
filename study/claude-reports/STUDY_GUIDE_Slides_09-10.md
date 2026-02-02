# Comprehensive Study Guide - Probabilistic Counters & AMQ Filters (Slides 09-10)
## Advanced Algorithms - University of Aveiro
### Professor: Joaquim Madeira
---

## Table of Contents
1. [Slide 09: Probabilistic Counters](#slide-09)
   - [Motivation & Big Data](#motivation)
   - [Summary Statistics](#summary-statistics)
   - [Counting with Probability 1/2](#counting-p-half)
   - [Counting with Probability 1/2^k](#counting-p-power)
   - [Morris Counter - Binary Base](#morris-binary)
   - [Morris Counter - Arbitrary Base](#morris-arbitrary)
   - [Csurös' Floating-Point Counter](#csuros-counter)
2. [Slide 10: AMQ Filters](#slide-10)
   - [Hash Tables & Functions](#hash-tables)
   - [Bloom Filters](#bloom-filters)
   - [Counting Bloom Filters](#counting-bloom)
   - [Quotient Filter](#quotient-filter)
   - [Recent AMQ Approaches](#recent-amq)
3. [Practice Problems](#practice-problems)
4. [Summary & Exam Tips](#summary)

---

# SLIDE 09: PROBABILISTIC COUNTERS <a name="slide-09"></a>

## Motivation & Big Data Applications <a name="motivation"></a>

### The Problem
**Can we use a small counter to keep approximate counts of large numbers?**

Traditional approach:
- n-bit counter → counts up to 2^n events
- Example: 8-bit counter → counts up to 256 events

But what if we need to count millions or billions of events?
- Use many counters simultaneously
- Track different events in Big Data applications

### Why Probabilistic Counters? (Morris, 1978)

Even though memory is cheaper now, probabilistic counters are **still relevant** because:
- **Massive data volumes** require fast and memory-efficient processing
- **Big Data applications:**
  - Online social networks
  - Large-scale scientific experiments
  - Search engines
  - Online content delivery
  - Product and consumer tracking
  - Medical data (genetic sequences, time series)
  - GPS location tracking
  - Business data (customer behavior)

### Scale Up vs Downsize

**Scale Up (Expensive):**
- Replicate cheap hardware/devices
- Build massive DBMSs and warehouses
- High equipment and energy costs

**Downsize the Data (Smart):**
- Compact representations of large data sets
- Approximate answers
- **Probabilistic methods** ✓

### Data Streaming Context

Data arrives in a **streaming fashion:**
- Must be processed **on the fly**
- Examples: network packets, web queries
- **Requirements:**
  - Make just **one pass** over the data
  - Use memory that is **sublinear** on the amount of data

### Application: System Performance Monitoring

**Statistics counters:**
- Count events that occur with **high frequency**
- Counter values are read **infrequently**
- Detecting excessively high rates of various system events

---

## Summary Statistics <a name="summary-statistics"></a>

### Why Summary Statistics?

Provide a summary of essential features of a dataset to answer:
- What are typical values?
- How much variation is in the data?
- Are there outliers?

### Mean Value (Average)

**Formula:**
```
μ(X) = (1/n) × Σ(xᵢ) for i=1 to n
```

**Python:**
```python
def mean(X):
    return sum(X) / len(X)
```

**Interpretation:**
- If xᵢ values are close together → mean is a good representation of a typical sample
- Sensitive to outliers

### Deviation Measures

#### 1. Maximal Deviation
```
maxdev(X) = max|xᵢ - μ| for i=1,2,...,n
```

Shows the largest distance from the mean.

#### 2. Mean Absolute Deviation (MAD)
```
mad(X) = (1/n) × Σ|xᵢ - μ| for i=1 to n
```

Average of absolute distances from mean.

#### 3. Standard Deviation
```
stddev(X) = √[(1/n) × Σ(xᵢ - μ)²] for i=1 to n
```

**Relationship:**
```
mad(X) ≤ stddev(X) ≤ maxdev(X)
```

**Important:** Outliers heavily affect these deviation measures!

---

## Counting with Probability 1/2 <a name="counting-p-half"></a>

### The Basic Idea

**Method:** For each event, increment the counter with probability **1/2**
- Intuition: Only incrementing for **half** of the events
- Like tossing a coin for each event!

### How Many Events Can We Count?

With n bits:
- Traditional counter: counts up to 2^n
- **Probabilistic counter (p=1/2): counts up to 2^(n+1)** 🎯

But is this what actually happens? Let's analyze!

### State Diagram & Binary Tree

**Binary Tree Structure:**
- Root = counter value 0
- Each event creates two branches:
  - Left branch (probability 1/2): counter **not** incremented
  - Right branch (probability 1/2): counter incremented
- After k events: 2^k possible paths

**Example for 4 events:**
```
Event 1:     0 -----> 1
           1/2  \   /  1/2
Event 2:        0   1   2
           paths...
```

### Random Variable Analysis

#### Expected Value (Mean)

Let Xᵢ represent the i-th increment:
- Xᵢ = 1: counter is incremented
- Xᵢ = 0: counter is not incremented
- P[Xᵢ = 0] = P[Xᵢ = 1] = 1/2

**Calculate E[Xᵢ]:**
```
E[Xᵢ] = 0 × P[Xᵢ=0] + 1 × P[Xᵢ=1]
      = 0 × (1/2) + 1 × (1/2)
      = 1/2
```

**Counter value after k events:**
```
S = Σ Xᵢ  (sum of all increments)

E[S] = E[Σ Xᵢ] = Σ E[Xᵢ] = k × (1/2) = k/2
```

**Estimate number of events:**
```
n ≈ 2 × S  (where S is the counter value)
```

#### Variance & Standard Deviation

**Calculate σ²(Xᵢ):**
```
E[Xᵢ²] = 0² × P[Xᵢ=0] + 1² × P[Xᵢ=1]
       = 0 + 1 × (1/2) = 1/2

σ²(Xᵢ) = E[Xᵢ²] - (E[Xᵢ])²
       = 1/2 - (1/2)²
       = 1/2 - 1/4 = 1/4
```

**For sum S after k events:**
```
σ²(S) = σ²(Σ Xᵢ) = Σ σ²(Xᵢ) = k × (1/4) = k/4

σ(S) = √(k/4) = √k / 2
```

**Summary for p = 1/2:**
- **Expected value:** E[S] = k/2
- **Variance:** σ²(S) = k/4
- **Standard deviation:** σ(S) = √k/2

### Probability Distribution

**Question:** After n events, what is the probability of the counter value being k?

**Notation:** p(n, k) = probability of counter = k after n events

**Analysis using binary tree:**
- After n events: 2^n possible paths
- Each path has probability (1/2)^n
- Number of paths leading to counter = k follows **binomial distribution**

**Formula:**
```
p(n, k) = C(n, k) × (1/2)^k × (1/2)^(n-k)
        = C(n, k) × (1/2)^n
        = C(n, k) / 2^n

where C(n, k) = n! / (k! × (n-k)!)
```

This is the **binomial coefficient** (Pascal's triangle)!

### Pascal-Like Triangle for p = 1/2

```
n=0:                    1
n=1:                  1   1
n=2:                1   2   1
n=3:              1   3   3   1
n=4:            1   4   6   4   1
n=5:          1   5  10  10   5   1
```

Each entry C(n,k) = number of ways to get counter = k after n events.

**Probability:** p(n, k) = C(n, k) / 2^n

**Example: n = 4 events**
```
p(4, 0) = 1/16   (counter stays at 0)
p(4, 1) = 4/16 = 1/4
p(4, 2) = 6/16 = 3/8  ← most probable!
p(4, 3) = 4/16 = 1/4
p(4, 4) = 1/16
```

### Computing Bernstein Polynomials (Efficient Method)

Instead of computing factorials, use **recurrence relations:**

```
B₀,₀(t) = 1

Bₙ,₀(t) = (1-t) × Bₙ₋₁,₀(t)
Bₙ,ₙ(t) = t × Bₙ₋₁,ₙ₋₁(t)
Bₙ,ⱼ(t) = (1-t) × Bₙ₋₁,ⱼ(t) + t × Bₙ₋₁,ⱼ₋₁(t)   for j=1,2,...,n-1
```

For probability with p = 1/2, use **t = 1/2**.

**Python implementation:**
```python
def compute_prob_distribution(n, p=0.5):
    """Compute probability distribution for n events with probability p"""
    # Use dynamic programming
    dp = [[0.0] * (n+2) for _ in range(n+2)]
    dp[0][0] = 1.0

    for events in range(1, n+1):
        for counter in range(events+1):
            # Not incremented (probability 1-p)
            dp[events][counter] += (1-p) * dp[events-1][counter]
            # Incremented (probability p)
            if counter > 0:
                dp[events][counter] += p * dp[events-1][counter-1]

    return [dp[n][k] for k in range(n+1)]

# Example: 100 events
probs = compute_prob_distribution(100, p=0.5)
mean = sum(k * probs[k] for k in range(101))
print(f"Mean: {mean}")  # Should be ≈ 50
```

### Experimental Analysis Tasks

**Task 1:** Simulate counter for 10, 100, 1000, 10000 events
```python
import random

def simulate_counter_p_half(n_events):
    """Simulate probabilistic counter with p=1/2"""
    counter = 0
    for _ in range(n_events):
        if random.random() < 0.5:  # Increment with probability 1/2
            counter += 1
    return counter

# Run many trials
def run_trials(n_events, n_trials=10000):
    results = [simulate_counter_p_half(n_events) for _ in range(n_trials)]

    mean = sum(results) / n_trials
    variance = sum((x - mean)**2 for x in results) / n_trials
    stddev = variance ** 0.5

    print(f"Events: {n_events}")
    print(f"Mean: {mean:.2f} (expected: {n_events/2:.2f})")
    print(f"Variance: {variance:.2f} (expected: {n_events/4:.2f})")
    print(f"Std Dev: {stddev:.2f} (expected: {(n_events**0.5)/2:.2f})")
    print()

# Test for different event counts
for n in [10, 100, 1000, 10000]:
    run_trials(n)
```

**Task 2:** Compute accuracy ratio
```python
def accuracy_ratio(exact, approximate):
    """Relative error"""
    return abs(exact - approximate) / exact

def estimate_from_counter(counter_value):
    """Estimate number of events from counter"""
    return 2 * counter_value
```

**Expected results for 100 events, 10000 trials:**
- Mean counter value: ≈ 50
- Variance: ≈ 25
- Standard deviation: ≈ 5

---

## Counting with Probability 1/2^k <a name="counting-p-power"></a>

### Generalization: Use Smaller Probability

**Goal:** Count more events with the same number of bits!

**Method:** Increment counter with probability **1/2^k** where k ≥ 1

**Examples:**
- k = 1: p = 1/2 (previous method)
- k = 2: p = 1/4
- k = 3: p = 1/8
- k = 5: p = 1/32
- k = 6: p = 1/64

### Capacity Improvement

With n bits:
- Traditional: counts up to 2^n
- With p = 1/2^k: **counts up to 2^(n+k)** 🎯

**Example:** 8-bit counter with k=5 (p=1/32)
- Traditional: 256 events
- Probabilistic: 2^13 = 8192 events!

### Expected Value & Variance (General Formula)

Let **p = probability of incrementing** and **q = 1-p**

After n events:
```
E[S] = n × p

σ²(S) = n × p × q

σ(S) = √(n × p × q)
```

**For p = 1/2^k:**
```
E[S] = n / 2^k

σ²(S) = n × (1/2^k) × (1 - 1/2^k)

Estimate: n ≈ 2^k × S
```

**Example: p = 1/32 (k=5)**
```
After 100 events:
E[S] = 100 / 32 = 3.125
σ²(S) = 100 × (1/32) × (31/32) ≈ 3.027
σ(S) ≈ 1.74

Estimate from counter: n ≈ 32 × counter_value
```

### Probability Distribution

Still follows **binomial distribution:**
```
p(n, k) = C(n, k) × p^k × (1-p)^(n-k)

where p = 1/2^k
```

**Pascal-like triangle structure:**
- More weight on smaller counter values
- Distribution is more "stretched" horizontally

### Python Implementation

```python
def simulate_counter_fixed_prob(n_events, k):
    """
    Simulate counter with probability p = 1/2^k

    Args:
        n_events: number of events to count
        k: exponent (probability = 1/2^k)

    Returns:
        counter value
    """
    counter = 0
    p = 1.0 / (2 ** k)

    for _ in range(n_events):
        if random.random() < p:
            counter += 1

    return counter

def estimate_events_fixed_prob(counter_value, k):
    """Estimate number of events from counter value"""
    return (2 ** k) * counter_value

# Example: k=5 (p = 1/32)
def test_fixed_prob():
    k = 5  # p = 1/32
    n_events = 10000
    n_trials = 10000

    results = [simulate_counter_fixed_prob(n_events, k) for _ in range(n_trials)]

    mean = sum(results) / n_trials
    variance = sum((x - mean)**2 for x in results) / n_trials

    # Theoretical values
    p = 1.0 / (2**k)
    expected_mean = n_events * p
    expected_var = n_events * p * (1 - p)

    print(f"k = {k}, p = 1/{2**k}")
    print(f"Events: {n_events}")
    print(f"Mean: {mean:.2f} (expected: {expected_mean:.2f})")
    print(f"Variance: {variance:.2f} (expected: {expected_var:.2f})")

    # Test estimation
    estimates = [estimate_events_fixed_prob(c, k) for c in results]
    avg_estimate = sum(estimates) / len(estimates)
    print(f"Average estimate: {avg_estimate:.2f} (actual: {n_events})")

test_fixed_prob()
```

### Experimental Tasks

**Task 1:** Set p = 1/32 and simulate for 10, 100, 1000, 10000 events
- Compare experimental vs theoretical results
- Observe that variance grows linearly with n

**Task 2:** Compute probability distributions for n = 10, 100, 1000
```python
def compute_prob_binomial(n, k, p):
    """Compute P(counter = k | n events, probability p)"""
    from math import comb
    return comb(n, k) * (p ** k) * ((1-p) ** (n-k))

# For p = 1/32, n = 100
p = 1/32
n = 100
for k in range(10):
    prob = compute_prob_binomial(n, k, p)
    print(f"p({n}, {k}) = {prob:.6f}")
```

### Issues with Fixed Probability

**Problem 1:** Counting small numbers with small probability
- If p = 1/32 and n = 10 events
- E[S] = 10/32 ≈ 0.3
- Counter is likely to be 0 or 1!
- Very poor accuracy for small counts

**Problem 2:** Counting very large numbers
- Can we be more economical?
- Fixed probability wastes bits for very large counts

**Solution:** Use **decreasing probability** as counter increases! ➡️

---

## Morris Counter - Decreasing Probability (Binary Base) <a name="morris-binary"></a>

### The Big Idea (Morris, 1978)

**Key insight:** As the counter value increases, increment it with **lesser probability**

**Algorithm:**
```
If counter has value k:
- Increment with probability 1/2^k
- Do NOT increment with probability (1 - 1/2^k)
```

**State Diagram:**
```
     1           1/2          1/4          1/8
0 ------> 1 ----------> 2 ----------> 3 ----------> 4 ...
  (100%)     (50%)        (25%)       (12.5%)
```

From counter value k:
- Probability to increment to k+1: **1/2^k**
- Probability to stay at k: **1 - 1/2^k**

### Expected Number of Events

**Question:** On average, how many events needed to reach counter value k?

**Analysis:** Let n(k) = expected number of events to reach counter = k

**Recurrence:**
```
n(0) = 0
n(1) = 1  (first event always increments 0→1 with p=1)
n(2) = n(1) + expected events to go from 1→2
     = 1 + 1/(1/2) = 1 + 2 = 3
n(3) = n(2) + 1/(1/4) = 3 + 4 = 7
n(4) = n(3) + 1/(1/8) = 7 + 8 = 15
...
n(k) = n(k-1) + 2^(k-1)
```

**Pattern:**
```
Counter value k | Expected events n(k)
----------------|--------------------
      0         |         0
      1         |         1
      2         |         3
      3         |         7
      4         |        15
      5         |        31
      k         |      2^k - 1
```

**Closed Formula:**
```
n(k) = 2^k - 1
```

### Logarithmic Counter!

From n(k) = 2^k - 1, we can solve for k:
```
2^k = n + 1
k = log₂(n + 1)

For large n:
k ≈ log₂(n)
```

**Therefore:**
- After n events, expected counter value ≈ **log₂(n)**
- This is a **logarithmic counter**!
- For larger values, it counts "slower"

### Space Efficiency (AMAZING!)

**After n probabilistic updates:**
- Counter contains approximation of **log n**
- Counter value is stored in **log log n bits**!!

**Example:**
- n = 1,000,000 events
- Counter value ≈ log₂(1,000,000) ≈ 20
- Need only log₂(20) ≈ 5 bits!

**Compare:**
- Traditional counter for 1M events: 20 bits
- Morris counter for 1M events: ~5 bits
- **4× space savings!**

### Estimation Formula

**Given counter value k, estimate number of events:**
```
n ≈ 2^k - 1
```

**Evaluation:**
- Compare estimated n with ⌊log₂(n+1)⌋

### Capacity with Fixed Bits

**What's the largest value we can count with n bits?**

Traditional: 2^n
Morris (binary): **2^(2^n) - 1**

**Examples:**
```
4-bit counter:
- Traditional: 16
- Morris: 2^16 - 1 = 65,535

8-bit counter:
- Traditional: 256
- Morris: 2^256 - 1 ≈ 10^77 (HUGE!)

16-bit counter:
- Traditional: 65,536
- Morris: 2^65536 - 1 ≈ 10^19728 (astronomical!)
```

### Expected Value Analysis

Let Xᵢ represent the i-th increment:
```
P[Xᵢ = 1] = 1/2^(i-1)
P[Xᵢ = 0] = 1 - 1/2^(i-1)

E[Xᵢ] = 1 × P[Xᵢ=1] = 1/2^(i-1)
```

**Counter value after n events:**
```
S = Σ Xᵢ

E[S] = Σ E[Xᵢ] = Σ (1/2^(i-1))

This is a geometric series that approximates log₂(n)
```

But we only store **integer values**!

```
Events n | E[S]                    | Expected counter
---------|-------------------------|------------------
    1    | 1                       | 1
    3    | 1 + 1/2 + 1/2          | 2
    7    | 1 + 2×(1/2) + 4×(1/4) | 3
   15    | 1 + 2×(1/2) + 4×(1/4) + 8×(1/8) | 4
  2^k-1  | complicated...          | k
```

**General formula:**
```
After n = 2^k - 1 events:
Expected counter value = k = log₂(n+1)
```

### Probability Distribution

**Question:** After n events, what is P(counter = k)?

**Notation:** p(n, k) = probability of counter = k after n events

**Recurrence relations:**
```
p(1, 1) = 1
p(1, 0) = 0  (impossible to have 0 after 1 event)

p(n, 1) = (1/2) × p(n-1, 1)

p(n, n) = (1/2^(n-1)) × p(n-1, n-1)

p(n, k) = (1/2^(k-1)) × p(n-1, k-1)          [increment from k-1]
        + (1 - 1/2^k) × p(n-1, k)            [stay at k]
```

**Pascal-like triangle structure** (but NOT symmetric!)

### Python Implementation

```python
class MorrisCounter:
    """Morris approximate counter (binary base)"""

    def __init__(self):
        self.counter = 0

    def increment(self):
        """Process one event"""
        if self.counter == 0:
            self.counter = 1  # First event always increments
        else:
            # Increment with probability 1/2^counter
            prob = 1.0 / (2 ** self.counter)
            if random.random() < prob:
                self.counter += 1

    def estimate(self):
        """Estimate the actual count"""
        return (2 ** self.counter) - 1

    def get_counter(self):
        return self.counter

# Simulation
def simulate_morris(n_events):
    """Simulate Morris counter for n events"""
    mc = MorrisCounter()
    for _ in range(n_events):
        mc.increment()
    return mc.get_counter(), mc.estimate()

# Test with multiple trials
def test_morris():
    event_counts = [10, 50, 100, 500, 1000, 10000]
    n_trials = 10000

    for n_events in event_counts:
        counters = []
        estimates = []

        for _ in range(n_trials):
            counter, estimate = simulate_morris(n_events)
            counters.append(counter)
            estimates.append(estimate)

        mean_counter = sum(counters) / n_trials
        mean_estimate = sum(estimates) / n_trials
        variance = sum((x - mean_counter)**2 for x in counters) / n_trials
        stddev = variance ** 0.5

        expected_counter = math.log2(n_events + 1)

        print(f"Events: {n_events}")
        print(f"  Mean counter: {mean_counter:.2f} (expected: {expected_counter:.2f})")
        print(f"  Mean estimate: {mean_estimate:.2f} (actual: {n_events})")
        print(f"  Std dev: {stddev:.2f}")
        print(f"  Accuracy: {(mean_estimate/n_events)*100:.1f}%")
        print()

test_morris()
```

### Computing Probability Distribution

```python
def compute_morris_prob_distribution(n_max):
    """
    Compute probability distribution for Morris counter

    Returns: p[n][k] = probability of counter=k after n events
    """
    # Maximum possible counter value
    k_max = int(math.log2(n_max)) + 5

    # Initialize probability table
    p = [[0.0] * (k_max + 1) for _ in range(n_max + 1)]

    # Base cases
    p[1][1] = 1.0  # After 1 event, counter = 1

    # Fill table using recurrence
    for n in range(2, n_max + 1):
        for k in range(1, k_max + 1):
            # Probability of staying at k
            if k <= n-1:
                stay_prob = 1 - (1 / (2 ** k))
                p[n][k] += stay_prob * p[n-1][k]

            # Probability of incrementing from k-1 to k
            if k > 1 and k-1 <= n-1:
                inc_prob = 1 / (2 ** (k-1))
                p[n][k] += inc_prob * p[n-1][k-1]

    return p

# Example: probabilities after 100 events
probs = compute_morris_prob_distribution(100)
print("P(counter = k | 100 events):")
for k in range(1, 10):
    print(f"  k={k}: {probs[100][k]:.6f}")
```

### Experimental Tasks

**Task 1:** Simulate for 10, 50, 100, 500, 1000, 10000 events
- Repeat many times (e.g., 10000 trials)
- Compute mean, variance, standard deviation
- Compare with theoretical log₂(n)

**Task 2:** Analyze accuracy
```python
def analyze_morris_accuracy(n_events, n_trials=10000):
    errors = []
    relative_errors = []

    for _ in range(n_trials):
        counter, estimate = simulate_morris(n_events)
        error = abs(n_events - estimate)
        rel_error = error / n_events
        errors.append(error)
        relative_errors.append(rel_error)

    print(f"Events: {n_events}")
    print(f"  Mean absolute error: {sum(errors)/n_trials:.2f}")
    print(f"  Mean relative error: {sum(relative_errors)/n_trials:.4f}")
```

**Expected result for 10000 events, 10000 trials:**
- Mean counter value: ≈ 13-14 (log₂(10000) ≈ 13.3)
- Mean estimate: close to 10000 but with variance
- Standard deviation: several counter values

---

## Morris Counter - Arbitrary Base <a name="morris-arbitrary"></a>

### Motivation

For some applications, the expected error of binary Morris counter might be **too large**.

**How to improve counter performance?**
- Use a different base **a** instead of 2

### The Algorithm

**If counter has value k:**
- Increment with probability **1/a^k**
- Do NOT increment with probability **(1 - 1/a^k)**

**Base a is now the counter base** (not fixed at 2)

### Better Accuracy with a < 2

**Key insight:** Take a < 2

Examples:
- a = 2^(1/2) = √2 ≈ 1.414
- a = 2^(1/4) ≈ 1.189
- a = 1.5
- a = 1.1

**Result:** Counter value after m increments will be **larger** than with binary base
→ Giving **better accuracy**!

### Estimation Formula

**Given counter value k, estimate number of events:**
```
n ≈ (a^k - a + 1) / (a - 1)
```

**Compare with binary base (a=2):**
```
Binary: n ≈ 2^k - 1
Arbitrary: n ≈ (a^k - a + 1) / (a - 1)
```

### Example: a = √2

```python
import math

a = 2 ** 0.5  # √2 ≈ 1.414

def estimate_events_arbitrary(counter, a):
    """Estimate events from counter value with base a"""
    return (a ** counter - a + 1) / (a - 1)

# Examples
for k in range(1, 10):
    estimate = estimate_events_arbitrary(k, a)
    print(f"Counter={k} → Estimate={estimate:.2f} events")

# Output:
# Counter=1 → Estimate=1.00 events
# Counter=2 → Estimate=3.41 events
# Counter=3 → Estimate=8.24 events
# Counter=4 → Estimate=17.66 events
# Counter=5 → Estimate=35.91 events
# ...
```

### Capacity with Fixed Bits

With n bits and base a:
```
Maximum count ≈ (a^(2^n) - a + 1) / (a - 1)
```

**4-bit counter examples:**
```
a = 2:     2^16 - 1 ≈ 65,535
a = √2:    smaller capacity but better accuracy for moderate values
a = 1.5:   even smaller but excellent accuracy
```

**Trade-off:**
- Smaller a → better accuracy for moderate counts
- Larger a → can count to larger values
- Choose a based on application needs!

### Implementation Notes

**Probabilities can be stored in a table:**
- No need to recompute a^k every time!
- Pre-compute probabilities for k = 0, 1, 2, ..., max_counter

```python
class MorrisCounterArbitrary:
    """Morris counter with arbitrary base a"""

    def __init__(self, a=1.414):
        self.counter = 0
        self.a = a
        # Pre-compute probabilities for efficiency
        self.max_counter = 100
        self.probs = [1.0 / (a ** k) if k > 0 else 1.0
                      for k in range(self.max_counter)]

    def increment(self):
        """Process one event"""
        if self.counter == 0:
            self.counter = 1
        elif self.counter < self.max_counter:
            prob = self.probs[self.counter]
            if random.random() < prob:
                self.counter += 1

    def estimate(self):
        """Estimate actual count"""
        a = self.a
        k = self.counter
        return (a ** k - a + 1) / (a - 1)

# Test different bases
def compare_bases():
    n_events = 10000
    n_trials = 1000
    bases = [2.0, 1.414, 1.189, 1.5]

    for a in bases:
        estimates = []
        for _ in range(n_trials):
            mc = MorrisCounterArbitrary(a)
            for _ in range(n_events):
                mc.increment()
            estimates.append(mc.estimate())

        mean_est = sum(estimates) / n_trials
        variance = sum((e - mean_est)**2 for e in estimates) / n_trials
        rel_error = abs(mean_est - n_events) / n_events

        print(f"Base a = {a:.3f}:")
        print(f"  Mean estimate: {mean_est:.2f}")
        print(f"  Variance: {variance:.2f}")
        print(f"  Relative error: {rel_error:.4f}")
        print()

compare_bases()
```

### Experimental Tasks

**Task 1:** Simulate counter with a = 2^(1/2) for 10, 50, 100, 500, 1000, 10000 events
- Repeat experiments many times
- Compare mean, variance, stddev with binary base

**Task 2:** Compare different bases
- Test a = 2, √2, 2^(1/4), 1.5, 1.3
- Analyze accuracy vs capacity trade-off

**Expected observation:**
- Smaller a gives better accuracy for moderate counts
- a = √2 is a good practical choice

---

## Csurös' Floating-Point Counter (2010) <a name="csuros-counter"></a>

### Motivation

Combine the best of both worlds:
- **Accurate count** for smaller values (deterministic)
- **Logarithmic approximation** for larger values (probabilistic)

### Structure

**Binary floating-point counter:**
- **d-bit significand** (mantissa)
- **Binary exponent**
- Total space: **d + log log n** bits

**Key feature:** First M = 2^d steps are **deterministic** (not probabilistic)!

### The Algorithm

**Parameters:**
- M = 2^d (where d is a non-negative integer)
- Counter X, initialized to X = 0

**Counter representation:**
```
X = 2^d × t + u

where:
- t = exponent (number of times we've "overflowed")
- u = significand (lower d bits)
```

**Increment procedure:**
```
1. If X < M:
   - Increment X deterministically: X = X + 1

2. If X ≥ M:
   - Split X into: X = M × t + u
   - Increment with probability 1/(M × 2^t)
   - If incremented: X = X + 1
```

### Estimation Formula

**Given counter value X = 2^d × t + u:**
```
Estimate = (M + u) × 2^t - M
```

where:
- M = 2^d
- u = lower d bits of X
- t = X >> d (X divided by 2^d, integer division)

### Examples

**Example 1: d = 0 (M = 1)**
- No significand bits
- This reduces to **Morris' counter**!
- First 1 step is deterministic

**Example 2: d = 3 (M = 8)**
- First 8 increments are deterministic
- Counter accurately counts 0, 1, 2, 3, 4, 5, 6, 7
- After that, probabilistic behavior starts

**Example 3: d = 8 (M = 256)**
- First 256 increments are deterministic
- Perfect accuracy for small counts!
- Then switches to logarithmic approximation

### Why This Works

**Benefits:**
1. **Small counts:** Perfect accuracy (deterministic)
2. **Large counts:** Space-efficient (logarithmic)
3. **Tunable:** Choose d based on application
   - Large d → more accuracy, more space
   - Small d → more approximation, less space

**Probability of increment after M:**
```
When X = M × t + u (X ≥ M):
P(increment) = 1 / (M × 2^t)
```

This maintains the logarithmic approximation property!

### Python Implementation

```python
import random
import math

class CsurosCounter:
    """Csurös' floating-point approximate counter"""

    def __init__(self, d=4):
        """
        Initialize counter

        Args:
            d: number of significand bits (M = 2^d)
        """
        self.d = d
        self.M = 2 ** d
        self.counter = 0

    def increment(self):
        """Process one event"""
        if self.counter < self.M:
            # Deterministic phase
            self.counter += 1
        else:
            # Probabilistic phase
            t = self.counter >> self.d  # Exponent (X / M)
            prob = 1.0 / (self.M * (2 ** t))

            if random.random() < prob:
                self.counter += 1

    def estimate(self):
        """Estimate the actual count"""
        if self.counter < self.M:
            return self.counter  # Exact during deterministic phase

        t = self.counter >> self.d  # Exponent
        u = self.counter & ((1 << self.d) - 1)  # Lower d bits

        return (self.M + u) * (2 ** t) - self.M

    def get_counter_value(self):
        return self.counter

# Test function
def test_csuros(d_values=[0, 2, 4, 8]):
    """Test Csurös counter with different d values"""
    event_counts = [10, 50, 100, 500, 1000, 10000]
    n_trials = 1000

    for d in d_values:
        print(f"\n{'='*50}")
        print(f"Testing with d = {d} (M = {2**d})")
        print(f"{'='*50}")

        for n_events in event_counts:
            estimates = []

            for _ in range(n_trials):
                counter = CsurosCounter(d)
                for _ in range(n_events):
                    counter.increment()
                estimates.append(counter.estimate())

            mean_est = sum(estimates) / n_trials
            variance = sum((e - mean_est)**2 for e in estimates) / n_trials
            stddev = variance ** 0.5
            rel_error = abs(mean_est - n_events) / n_events

            print(f"Events: {n_events:6d} | "
                  f"Est: {mean_est:8.1f} | "
                  f"StdDev: {stddev:6.1f} | "
                  f"RelErr: {rel_error:.4f}")

# Run tests
test_csuros()
```

### Comparison: Morris vs Csurös

| Feature | Morris (d=0) | Csurös (d=4) | Csurös (d=8) |
|---------|--------------|--------------|--------------|
| Deterministic phase | 1 event | 16 events | 256 events |
| Accuracy (small n) | Poor | Good | Excellent |
| Space (bits) | log log n | 4 + log log n | 8 + log log n |
| Max capacity | 2^(2^b) | Slightly less | Significantly less |

**Recommendation:**
- For very large counts: Morris (d=0)
- For balanced accuracy: Csurös with d=4 or d=8
- For small count accuracy: Csurös with d=8 or more

### Experimental Tasks

**Task 1:** Simulate Csurös counter for various d values
- d = 0, 2, 4, 6, 8
- Events: 10, 50, 100, 500, 1000, 10000
- Compare accuracy in deterministic vs probabilistic phases

**Task 2:** Analyze space-accuracy trade-off
```python
def analyze_space_accuracy_tradeoff():
    """Compare different d values"""
    n_events = 1000
    n_trials = 10000
    d_values = range(0, 10)

    results = []
    for d in d_values:
        estimates = []
        for _ in range(n_trials):
            counter = CsurosCounter(d)
            for _ in range(n_events):
                counter.increment()
            estimates.append(counter.estimate())

        mean_est = sum(estimates) / n_trials
        rel_error = abs(mean_est - n_events) / n_events
        space_bits = d + math.ceil(math.log2(math.log2(n_events + 1)))

        results.append((d, 2**d, rel_error, space_bits))

    print("d  | M    | RelError | Space")
    print("---|------|----------|------")
    for d, M, err, space in results:
        print(f"{d:2d} | {M:4d} | {err:.6f} | {space:2d} bits")

analyze_space_accuracy_tradeoff()
```

---

## Other Approaches

### Flajolet & Martin (1985)

**Approximate counting of different elements in a multi-set**
- Analyze the **tail bits** of hash values
- Count trailing zeros in binary representation
- Used for estimating cardinality (distinct elements)

**Key idea:**
- If you hash n distinct elements uniformly
- Average position of rightmost 1-bit ≈ log₂(n)

This is related to but different from Morris counters!

---

## Summary: Probabilistic Counters

| Method | Probability | Capacity (n bits) | Space for count n | Accuracy |
|--------|-------------|-------------------|-------------------|----------|
| Traditional | - | 2^n | n | Perfect |
| Fixed p=1/2 | 1/2 | 2^(n+1) | n | Good |
| Fixed p=1/2^k | 1/2^k | 2^(n+k) | n | Moderate |
| Morris (binary) | 1/2^counter | 2^(2^n) | log log n | Lower |
| Morris (arbitrary) | 1/a^counter | Depends on a | log log n | Better |
| Csurös (d bits) | Complex | Large | d + log log n | Tunable |

**Key takeaways:**
1. **Fixed probability:** Simple, good for known ranges
2. **Morris (binary):** Maximum space efficiency, lower accuracy
3. **Morris (arbitrary):** Better accuracy with a < 2
4. **Csurös:** Best of both worlds - accurate for small, efficient for large

**When to use:**
- **Known moderate range:** Fixed probability counters
- **Very large unknown range:** Morris counter
- **Need small-count accuracy:** Csurös counter
- **Multiple counters:** Probabilistic (save memory across many counters)

---

# SLIDE 10: AMQ FILTERS <a name="slide-10"></a>

## Introduction to AMQ

### Set Membership Problem

**Given:**
- An arbitrary sized string s
- A set S = {x₁, x₂, ..., xₙ}

**Question:** Does s belong to S?

**"Easy" for small sets:**
- Linear search: O(n)
- Binary search (if sorted): O(log n)
- Hash table: O(1) average

**"Difficult" for huge sets:**
- Big Data applications
- Billions of elements
- Cannot fit in memory
- Need fast answers

### Approximate Membership Queries (AMQ)

**Key idea:** Trade perfect accuracy for speed and space!

**Data structure should be:**
- **FAST:** Faster than searching through S
- **SMALL:** Smaller than explicit representation of S

**How?** Allow some **probability of error**

### Types of Errors

**1. False Positives:**
- Reality: y ∉ S
- Report: y ∈ S
- "Claim element is in set when it's not"

**2. False Negatives:**
- Reality: y ∈ S
- Report: y ∉ S
- "Claim element is not in set when it is"

**Which is worse?** Depends on application!
- Bloom filters: No false negatives, only false positives
- Some other filters: Allow both types

---

## Hash Tables & Hash Functions <a name="hash-tables"></a>

### Quick Review: Hash Tables

**Data structure for storing key-value pairs:**
- No ordering requirement
- **Fast access:** O(1) average case
- **No duplicate keys**

**Main operations:**
1. **Insert (put):** Add key-value pair
   - If key exists, update value
2. **Search (get):** Find value for given key
3. **Additional:** contains(key), delete(key), is_empty(), keys()

### Hash Functions

**Purpose:** Transform search keys into array indices
- Perform **arithmetic operations**
- Fast computation
- Ideally: different keys → different indices

**Reality:** Collisions DO occur!
- Distinct keys Kᵢ ≠ Kⱼ may have h(Kᵢ) = h(Kⱼ)

### Time Complexity

Best case: **O(1)**
- Direct access to correct entry

Worst case: **O(N)**
- All distinct keys collide: h(K₁) = h(K₂) = ... = h(Kₙ)
- Must search entire table
- Very rare with good hash function!

### Simple Hash Functions

**1. Division Method:**
```
h(k) = k mod m

where:
- m is a prime number
- m should not be close to a power of 2
```

**Problem:** Works badly for many patterns in input data

**2. Knuth's Variant:**
```
h(k) = k(k+3) mod m
```

Supposedly works much better!

**3. String Hashing (Simple):**
```python
def hash_string_simple(s, m):
    """Hash string by summing character codes"""
    return sum(ord(c) for c in s) % m
```

**Problem:** Anagrams get same hash value!
- "listen" and "silent" → same hash

**4. DJB31MA (Better for strings):**
```python
def djb31ma(s):
    """Dan Bernstein's hash function"""
    h = 5381
    for c in s:
        h = ((h << 5) + h) + ord(c)  # h * 33 + c
    return h & 0xFFFFFFFF  # Keep 32 bits
```

### Non-Cryptographic Hash Functions

**Suitable for hash tables but NOT for security:**

**1. FNV (Fowler-Noll-Vo):**
```python
def fnv1a_32(data):
    """FNV-1a 32-bit hash"""
    FNV_32_PRIME = 0x01000193
    FNV1_32A_INIT = 0x811c9dc5

    hash_value = FNV1_32A_INIT
    for byte in data:
        hash_value ^= byte
        hash_value = (hash_value * FNV_32_PRIME) & 0xFFFFFFFF

    return hash_value
```

**2. MurmurHash:**
- Fast computation
- Good distribution
- "Multiply and rotate" operations
- Widely used in practice

### Universal Hashing

**Problem:** For any fixed hash function, there exist keys that collide

**Solution:** Use a **set of hash functions** H

**Definition:** H is **universal** if:
```
For all keys 0 ≤ i < j < M:
P(h(i) = h(j)) ≤ 1/M

where h is randomly selected from H
```

**Benefit:** No input pattern can cause systematic collisions

---

## Bloom Filters <a name="bloom-filters"></a>

### Introduction (B.H. Bloom, 1970)

**Bloom Filter:**
- Use **hash functions** to determine approximate set membership
- Allow **fast set membership tests** on very large data sets
- **Space-efficient** probabilistic data structure

**Key property:**
- **No false negatives**
- **Some false positives** (tunable probability)

### Applications

**1. Spell-Checking / Text Analysis:**
- Determine if candidate words are in dictionary
- Filter should be large enough for user-added words

**2. Web-Caching:**
- WWW caching proxy servers
- Quickly check if page is in cache before expensive disk access

**3. Email Spam Detection:**
- Database of 1 billion "good" email addresses
- If email comes from one of these → NOT spam
- Fast pre-filter before expensive checks

**4. Text Similarity:**
- Find related passages in different reports
- Create Bloom filter for words in each passage
- Compute normalized dot product of filter pairs
- Result = similarity measure

**5. Network Monitoring:**
- Track packets, connections, flows
- Detect duplicates or anomalies

**6. Database Systems:**
- Speed up join operations
- Filter rows before expensive operations

### How Bloom Filters Work

**Structure:**
- **Bit array** of size m (all initialized to 0)
- **k independent hash functions:** h₁, h₂, ..., hₖ
- Each hash maps element to range [0, m-1]

**Initialization:**
```
Create bit array B[0..m-1]
Set all bits to 0: B[i] = 0 for all i
```

### Basic Operations

**1. Insertion (Add element x):**
```
For i = 1 to k:
    index = hᵢ(x)
    B[index] = 1
```

**Complexity:** O(k) - constant time!

**2. Membership Test (Query element x):**
```
For i = 1 to k:
    index = hᵢ(x)
    If B[index] == 0:
        Return "x is NOT in S" (DEFINITE!)

If all k bits are 1:
    Return "x is PROBABLY in S"
```

**Complexity:** O(k) - constant time!

**Note:** Elements are never removed (standard Bloom filter)

### Visual Example

```
Initial state (m=16, k=3):
Index: 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15
Bits:  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0

Insert "alice":
h₁("alice") = 3  → Set B[3] = 1
h₂("alice") = 7  → Set B[7] = 1
h₃("alice") = 12 → Set B[12] = 1

Bits:  0  0  0  1  0  0  0  1  0  0  0  0  1  0  0  0

Insert "bob":
h₁("bob") = 2   → Set B[2] = 1
h₂("bob") = 7   → Set B[7] = 1 (already 1!)
h₃("bob") = 14  → Set B[14] = 1

Bits:  0  0  1  1  0  0  0  1  0  0  0  0  1  0  1  0

Query "charlie":
h₁("charlie") = 5  → B[5] = 0  ✗
Return: "charlie is NOT in set" (correct!)

Query "alice":
h₁("alice") = 3   → B[3] = 1  ✓
h₂("alice") = 7   → B[7] = 1  ✓
h₃("alice") = 12  → B[12] = 1 ✓
Return: "alice is PROBABLY in set" (correct!)

Query "dave":
h₁("dave") = 3   → B[3] = 1  ✓
h₂("dave") = 7   → B[7] = 1  ✓
h₃("dave") = 12  → B[12] = 1 ✓
Return: "dave is PROBABLY in set" (FALSE POSITIVE!)
```

### Important Properties

**1. No False Negatives:**
- If Bloom filter says "NOT in set" → definitely NOT in set
- If element was inserted, all k bits were set to 1
- They will still be 1 (bits never cleared)

**2. Possible False Positives:**
- If Bloom filter says "probably in set" → maybe not!
- k bits might be set to 1 by other elements
- Collision in hash space

**3. Cannot Delete:**
- Clearing a bit might affect other elements
- Would introduce false negatives!
- Solution: Counting Bloom Filters (later)

---

## Bloom Filter Parameters & Probability Analysis <a name="bloom-parameters"></a>

### Four Key Parameters

1. **n:** Number of elements inserted
2. **m:** Number of bits in array (m = c × n often)
3. **k:** Number of hash functions
4. **f:** Fraction of bits set to 1

**Question:** How to choose m and k optimally?

### Probability Analysis - After 1 Insertion

**Initially:** All bits are 0

**Insert one element using hash function h₁:**

**Q:** What is P(bᵢ = 1) after using first hash function?
```
A: P(bᵢ = 1) = 1/m  (equal probability for any cell)
   P(bᵢ = 0) = 1 - 1/m
```

**After computing k hash functions:**
```
P(bᵢ = 0) = (1 - 1/m)^k

P(bᵢ = 1) = 1 - (1 - 1/m)^k
```

### Probability Analysis - After n Insertions

**After inserting all n elements:**

Each element uses k hash functions, total k×n hash operations.

**Assuming independence:**
```
P(bᵢ = 0) = (1 - 1/m)^(kn)

P(bᵢ = 1) = 1 - (1 - 1/m)^(kn)
```

**Approximation using e:**
```
Let a = (1 - 1/m)^n

For large m: a ≈ e^(-n/m)

Therefore:
P(bᵢ = 0) ≈ e^(-kn/m)
P(bᵢ = 1) ≈ 1 - e^(-kn/m)
```

### False Positive Probability

**Definition:** Testing membership of item NOT in S returns positive

**This happens when:** All k bits are set to 1 by other elements

**Probability:**
```
p = P(all k bits are 1)
  = (P(one bit is 1))^k
  = (1 - a)^k

where a = (1 - 1/m)^(kn)

Using approximation:
p ≈ (1 - e^(-kn/m))^k
```

**This is the FALSE POSITIVE RATE!**

### Numerical Example

**Setup:** n = 1 billion items, m = 8 billion bits (8 GB)

**Ratio:** m/n = 8 bits per element

**Test different k values:**

```
k = 1:
p ≈ (1 - e^(-1/8))^1 ≈ 0.1175 = 11.75%

k = 2:
p ≈ (1 - e^(-2/8))^2 ≈ 0.0493 = 4.93%

k = 3:
p ≈ (1 - e^(-3/8))^3 ≈ 0.0268 = 2.68%

k = 4:
p ≈ (1 - e^(-4/8))^4 ≈ 0.0177 = 1.77%

k = 5:
p ≈ (1 - e^(-5/8))^5 ≈ 0.0133 = 1.33%

k = 6:
p ≈ (1 - e^(-6/8))^6 ≈ 0.0108 = 1.08% ← optimal!

k = 7:
p ≈ (1 - e^(-7/8))^7 ≈ 0.0096 = 0.96%

k = 8:
p ≈ (1 - e^(-8/8))^8 ≈ 0.0092 = 0.92%

k = 10:
p ≈ (1 - e^(-10/8))^10 ≈ 0.0099 = 0.99%
```

**Observation:** False positive rate first decreases, then increases!
- Too few hash functions → bits set randomly
- Too many hash functions → too many bits set to 1

There's an **optimal k value**!

### Optimal Number of Hash Functions

**To minimize false positive probability p:**

Minimize log(p) (more tractable):
```
log(p) = k × log(1 - e^(-kn/m))
```

**Taking derivative and setting to 0:**
```
d/dk [k × log(1 - e^(-kn/m))] = 0
```

**Solution:**
```
k_opt = (m/n) × ln(2)
     ≈ 0.693 × (m/n)
```

**Use the closest integer to k_opt**

**For our example:** m/n = 8
```
k_opt ≈ 0.693 × 8 ≈ 5.54 → Use k = 6
```

**With optimal k, false positive rate:**
```
p ≈ (1/2)^k_opt = 0.5^k_opt
```

### Choosing Parameters

**Given requirements:**

**Option 1:** Fix false positive rate p and set size n
```
m = -n × ln(p) / (ln(2))²
  ≈ -1.44 × n × ln(p)

k = -log₂(p)
```

**Example:** n = 1 million, p = 0.01 (1%)
```
m ≈ -1.44 × 10⁶ × ln(0.01)
  ≈ -1.44 × 10⁶ × (-4.605)
  ≈ 6.63 million bits ≈ 830 KB

k ≈ -log₂(0.01) ≈ 6.64 → Use k = 7
```

**Option 2:** Fix space m and set size n
```
k = (m/n) × ln(2)

p ≈ (0.5)^k
```

### Python Implementation

```python
import hashlib
import math

class BloomFilter:
    """Simple Bloom Filter implementation"""

    def __init__(self, n_items, false_pos_rate=0.01):
        """
        Initialize Bloom Filter

        Args:
            n_items: expected number of items
            false_pos_rate: desired false positive rate
        """
        # Calculate optimal m and k
        self.n = n_items
        self.p = false_pos_rate

        # m = -n × ln(p) / (ln(2))²
        self.m = math.ceil(-n_items * math.log(false_pos_rate) / (math.log(2)**2))

        # k = m/n × ln(2)
        self.k = round(self.m / n_items * math.log(2))
        self.k = max(1, self.k)  # At least 1

        # Bit array
        self.bits = [0] * self.m
        self.count = 0

        print(f"Bloom Filter created:")
        print(f"  m = {self.m} bits ({self.m/8:.0f} bytes)")
        print(f"  k = {self.k} hash functions")
        print(f"  Expected p ≈ {self.expected_fpr():.6f}")

    def _hash(self, item, seed):
        """Generate hash value for item with given seed"""
        h = hashlib.md5(f"{item}{seed}".encode())
        return int(h.hexdigest(), 16) % self.m

    def add(self, item):
        """Add item to the filter"""
        for i in range(self.k):
            index = self._hash(item, i)
            self.bits[index] = 1
        self.count += 1

    def contains(self, item):
        """
        Check if item might be in the filter

        Returns:
            True if item might be in filter (or false positive)
            False if item is definitely NOT in filter
        """
        for i in range(self.k):
            index = self._hash(item, i)
            if self.bits[index] == 0:
                return False  # Definitely not in set
        return True  # Probably in set

    def expected_fpr(self):
        """Calculate expected false positive rate"""
        if self.count == 0:
            return 0.0
        return (1 - math.exp(-self.k * self.count / self.m)) ** self.k

    def actual_fpr(self):
        """Calculate actual false positive rate from bit array"""
        ones = sum(self.bits)
        return (ones / self.m) ** self.k

# Test Bloom Filter
def test_bloom_filter():
    # Create filter for 1000 items with 1% false positive rate
    bf = BloomFilter(n_items=1000, false_pos_rate=0.01)

    # Add some items
    items_to_add = [f"item{i}" for i in range(1000)]
    for item in items_to_add:
        bf.add(item)

    # Test items that were added
    true_positives = sum(bf.contains(item) for item in items_to_add)
    print(f"\nTrue positives: {true_positives}/{len(items_to_add)} = {true_positives/len(items_to_add)*100:.1f}%")

    # Test items that were NOT added
    items_not_added = [f"notitem{i}" for i in range(1000)]
    false_positives = sum(bf.contains(item) for item in items_not_added)
    print(f"False positives: {false_positives}/{len(items_not_added)} = {false_positives/len(items_not_added)*100:.2f}%")
    print(f"Expected FPR: {bf.expected_fpr()*100:.2f}%")
    print(f"Actual FPR: {bf.actual_fpr()*100:.2f}%")

test_bloom_filter()
```

### Which Hash Functions to Use?

**Good news:** No need for cryptographic hash functions!

**Technique:** Simulate k hash functions using just **2 hash functions**
- Kirsch and Mitzenmacher (2006)

**Method:**
```
Compute h₁(x) and h₂(x)

For i = 0, 1, 2, ..., k-1:
    hᵢ(x) = (h₁(x) + i × h₂(x)) mod m
```

**Alternative:** Use single 64-bit hash
```
Compute one hash on 64-bit numbers
Split into upper and lower 32 bits
Use these as two independent hash values
```

### Experimental Tasks

**Task 1:** Create Bloom filter with different parameters
```python
def experiment_parameters():
    """Test different m, n, k combinations"""
    n = 1000
    test_items = [f"test{i}" for i in range(n)]
    false_items = [f"false{i}" for i in range(n)]

    configs = [
        (8*n, 5),   # 8 bits per item, k=5
        (8*n, 6),   # 8 bits per item, k=6
        (10*n, 7),  # 10 bits per item, k=7
        (12*n, 8),  # 12 bits per item, k=8
    ]

    for m, k in configs:
        bf = BloomFilter.__new__(BloomFilter)
        bf.m = m
        bf.k = k
        bf.bits = [0] * m
        bf.count = 0

        # Add items
        for item in test_items:
            bf.add(item)

        # Test false positive rate
        fps = sum(bf.contains(item) for item in false_items)
        fpr = fps / len(false_items)
        expected = bf.expected_fpr()

        print(f"m={m}, k={k}: FPR={fpr:.4f}, Expected={expected:.4f}")

experiment_parameters()
```

**Task 2:** Analyze percentage of false positives

**Task 3:** Compare space usage: Bloom filter vs hash table

---

## Counting Bloom Filters <a name="counting-bloom"></a>

### Motivation

**Standard Bloom Filter limitations:**
1. Cannot represent **multi-sets** (sets with repeated elements)
2. Cannot query **multiplicity** of an item (how many times it appears)
3. **Cannot delete** an item

**Solution:** Counting Bloom Filters!

### Structure

Instead of bits, use **w-bit counters:**
```
Standard:  [0, 1, 0, 1, 1, ...]  (1 bit each)
Counting:  [0, 3, 0, 1, 5, ...]  (w bits each, e.g., w=4)
```

**Typical:** w = 4 bits (counts 0-15) is enough for most applications

**Space:** w × m bits instead of m bits
- Factor of w increase
- Usually w = 4, so 4× space

### Operations

**1. Initialize:**
```
Set all counters to 0
```

**2. Insert element x:**
```
For i = 1 to k:
    index = hᵢ(x)
    counter[index] = counter[index] + 1
```

**3. Membership test for x:**
```
For i = 1 to k:
    index = hᵢ(x)
    If counter[index] == 0:
        Return "x is NOT in set"

If all k counters are non-zero:
    Return "x is PROBABLY in set"
```

**4. Delete element x:**
```
For i = 1 to k:
    index = hᵢ(x)
    counter[index] = counter[index] - 1
```

**5. Count occurrences of x (frequency estimation):**
```
For i = 1 to k:
    index = hᵢ(x)
    counts[i] = counter[index]

Return min(counts)  # Minimum as estimate
```

**Why minimum?** Counters might be inflated by other elements. The minimum is the most conservative estimate.

### Visual Example

```
Initial (m=10, k=3, w=4):
Index:     0  1  2  3  4  5  6  7  8  9
Counters: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

Insert "alice":
h₁("alice")=2, h₂("alice")=5, h₃("alice")=7
Counters: [0, 0, 1, 0, 0, 1, 0, 1, 0, 0]

Insert "alice" again:
Counters: [0, 0, 2, 0, 0, 2, 0, 2, 0, 0]

Insert "bob":
h₁("bob")=2, h₂("bob")=4, h₃("bob")=8
Counters: [0, 0, 3, 0, 1, 2, 0, 2, 1, 0]

Count("alice"):
counters at [2, 5, 7] = [3, 2, 2]
min = 2 ✓ (correct, inserted twice)

Count("bob"):
counters at [2, 4, 8] = [3, 1, 1]
min = 1 ✓ (correct, inserted once)

Delete "alice":
Counters: [0, 0, 2, 0, 1, 1, 0, 1, 1, 0]

Count("alice"):
counters at [2, 5, 7] = [2, 1, 1]
min = 1 ✓ (one copy remains)
```

### Issues & Trade-offs

**1. Counter Overflow:**
- Counters have maximum value 2^w - 1
- If counter reaches max, stop incrementing (saturate)
- This creates **undercounts**!

**Example:** w=4, max=15
```
If counter = 15 and we insert:
- Cannot increment (would overflow)
- Counter stays at 15
- Undercount the actual frequency
```

**2. False Negatives from Deletion:**
- If we delete item that was never inserted
- Decrement counters that might be used by other items
- This can cause false negatives!

**Example:**
```
Counters: [0, 3, 0, 2, 1]

Delete "fake" (never inserted):
h₁("fake")=1, h₂("fake")=3
Decrements: [0, 2, 0, 1, 1]

Now if real item has h(...) ∈ {1, 3}:
- Might hit counter=0 somewhere
- False negative!
```

**3. Choice of Counter Width w:**
```
Large w:
  + No overflow risk
  - Wastes space (many zeros)
  - Larger memory footprint

Small w:
  + Space efficient
  - Quick overflow
  - More undercounts

Trade-off: Usually w=4 is good balance
```

### Python Implementation

```python
class CountingBloomFilter:
    """Counting Bloom Filter with deletion support"""

    def __init__(self, n_items, false_pos_rate=0.01, counter_width=4):
        """
        Initialize Counting Bloom Filter

        Args:
            n_items: expected number of items
            false_pos_rate: desired false positive rate
            counter_width: bits per counter (default 4)
        """
        self.w = counter_width
        self.max_count = (2 ** counter_width) - 1

        # Calculate optimal m and k (same as Bloom filter)
        self.m = math.ceil(-n_items * math.log(false_pos_rate) / (math.log(2)**2))
        self.k = round(self.m / n_items * math.log(2))
        self.k = max(1, self.k)

        # Counter array
        self.counters = [0] * self.m

        print(f"Counting Bloom Filter created:")
        print(f"  m = {self.m} counters")
        print(f"  k = {self.k} hash functions")
        print(f"  w = {self.w} bits per counter")
        print(f"  Space = {self.m * self.w} bits ({self.m * self.w / 8:.0f} bytes)")

    def _hash(self, item, seed):
        """Generate hash value"""
        h = hashlib.md5(f"{item}{seed}".encode())
        return int(h.hexdigest(), 16) % self.m

    def add(self, item):
        """Add item (increment counters)"""
        for i in range(self.k):
            index = self._hash(item, i)
            if self.counters[index] < self.max_count:
                self.counters[index] += 1

    def remove(self, item):
        """
        Remove item (decrement counters)
        WARNING: May introduce false negatives if item wasn't in filter!
        """
        for i in range(self.k):
            index = self._hash(item, i)
            if self.counters[index] > 0:
                self.counters[index] -= 1

    def contains(self, item):
        """Check if item might be in filter"""
        for i in range(self.k):
            index = self._hash(item, i)
            if self.counters[index] == 0:
                return False
        return True

    def count(self, item):
        """
        Estimate frequency of item

        Returns minimum counter value as conservative estimate
        """
        counts = []
        for i in range(self.k):
            index = self._hash(item, i)
            counts.append(self.counters[index])
        return min(counts)

# Test
def test_counting_bloom():
    cbf = CountingBloomFilter(n_items=1000, false_pos_rate=0.01)

    # Add items with different frequencies
    items = {
        "alice": 5,
        "bob": 3,
        "charlie": 1,
        "dave": 10,
    }

    for item, freq in items.items():
        for _ in range(freq):
            cbf.add(item)

    # Check counts
    print("\nEstimated counts:")
    for item, true_count in items.items():
        est_count = cbf.count(item)
        print(f"  {item}: {est_count} (actual: {true_count})")

    # Test deletion
    print("\nAfter deleting 'alice' 2 times:")
    cbf.remove("alice")
    cbf.remove("alice")
    est_count = cbf.count("alice")
    print(f"  alice: {est_count} (should be ~3)")

    # Test item not in filter
    print(f"\nItem 'eve' (not added): count = {cbf.count('eve')}")

test_counting_bloom()
```

### Practical Usage Pattern

**In network devices:**

If insertions/deletions are **rare** compared to lookups:
1. Keep **CBF in off-chip memory** (slower, larger)
2. Keep **BF in on-chip memory** (fast, smaller)
3. Update BF whenever CBF changes

**Benefits:**
- Fast lookups (use BF)
- Can handle deletions (use CBF)
- Space-efficient for frequent reads

---

## Quotient Filter <a name="quotient-filter"></a>

### Motivation: Bloom Filter Limitation

**Problem:** What if filter is **too big to fit in main memory**?

**Traditional approach:**
- Store some parts in HDD or SSD
- But random accesses are slower in disk
- **Significantly bad performance!**

**Bloom filter requires:**
- k random accesses per operation
- If k=5 and each access is to disk → very slow!

**Ideas for improvement:**
1. Random access only **once**
2. Store each element's data **really close** together

**Challenge:**
- Using just 1 hash function → high collision probability
- Need to handle collisions efficiently

**Solution:** Quotient Filter!

### The Quotient Filter (2011)

**By:** Michael Bender et al.

**Properties:**
- Space-efficient probabilistic data structure for AMQ
- Supports 4 operations:
  1. Add element
  2. Delete element
  3. Test if element is member
  4. Test if element is NOT member

**Key features:**
- Uses **one hash function** (not k!)
- Stores **p-bit fingerprint** for each element
- **Compact open hash table** with m = 2^q buckets

### Quotienting Technique

**Fingerprint partitioning:**
```
Hash element → p-bit fingerprint f

Split f into two parts:
- Quotient f_q: q most significant bits (MSBs)
- Remainder f_r: r least significant bits (LSBs)

where p = q + r
```

**Division interpretation:**
```
f_q = f / 2^r   (quotient)
f_r = f mod 2^r  (remainder)
```

**Usage:**
- **Quotient f_q:** indexes a table bucket (which bucket?)
- **Remainder f_r:** stored IN that bucket (what's stored?)

### Example

**Parameters:** p=16 bits, q=10, r=6

```
Element "alice":
Hash → fingerprint f = 0b1101001011001110 (16 bits)

Split:
f_q = upper 10 bits = 0b1101001011 = 843 (quotient)
f_r = lower 6 bits  = 0b001110 = 14 (remainder)

Store remainder 14 in bucket 843
```

### Collision Handling: Runs

**Soft collision:** Different fingerprints with same quotient
```
f_q = f*_q  but  f ≠ f*
```

**Solution:** Store all remainders with same quotient **contiguously** in a **run**
- Run = sequence of remainders with same quotient
- Stored in sorted order!

**If necessary:**
- Remainder is **shifted forward** from its original location
- Stored in a subsequent bucket
- **Wrapping around** at end of table

### Three Auxiliary Bits Per Bucket

**To track collisions and shifts, each bucket has 3 bits:**

**1. is_occupied (bit):**
- Set if f_q = j for some stored fingerprint
- j is the **canonical bucket** (where it "wants" to be)

**2. is_continuation (bit):**
- Bucket is occupied
- But NOT by the first remainder in a run
- Marks continuation of a run

**3. is_shifted (bit):**
- Remainder in bucket is NOT in its canonical bucket
- It has been shifted forward due to collision

**Initially:** All three bits are 0

```
Bucket structure:
[is_occupied | is_continuation | is_shifted | remainder (r bits)]
      1 bit         1 bit             1 bit       r bits
```

### Membership Testing Algorithm

**Given:** Element x to search

**Steps:**
1. Compute fingerprint f = hash(x)
2. Compute quotient f_q and remainder f_r
3. **Check bucket f_q:**
   - If **not occupied** → item **definitely NOT** in filter! ✓
   - If **occupied** → continue to step 4

4. **Locate the run for quotient f_q:**
   a. Scan **left** from bucket f_q until find bucket with is_shifted = 0
      (This finds the start of all runs in this cluster)
   b. Scan **right**, counting runs, until reach run for quotient f_q
      (Use is_occupied and is_continuation to count runs)

5. **Search within the run:**
   - Compare f_r with each remainder in the run
   - If **found** → element is **(probably) in filter** (might be false positive)
   - If **not found** → element is **definitely NOT in filter** ✓

**Complexity:**
- Average: O(1)
- Worst: O(run length)

### Adding an Element Algorithm

**Given:** Element x to add

**Steps:**
1. Compute fingerprint f = hash(x)
2. Compute quotient f_q and remainder f_r
3. Follow membership testing procedure to:
   - Check if already in filter (if yes, done!)
   - Locate the run for f_q

4. **Insert remainder f_r into the run:**
   - Find correct position to maintain **sorted order**
   - Shift all remainders at or after the insertion point **forward**
   - Update auxiliary bits:
     - Set is_occupied for bucket f_q
     - Set is_shifted for shifted remainders
     - Set is_continuation for non-first remainders in run

**Complexity:** O(run length + shift distance)

### Visual Example

**Parameters:** q=3 (8 buckets), r=5 (5-bit remainders)

**Use 32-bit signed MurmurHash3**

**Add "alice":**
```
hash("alice") → fingerprint = 0b10110001 (simplified)
f_q = 0b101 = 5 (bucket index)
f_r = 0b00001 = 1 (remainder)

Bucket 5 is empty:
Bucket:  [0][1][2][3][4][5][6][7]
Occ:      0  0  0  0  0  1  0  0
Cont:     0  0  0  0  0  0  0  0
Shift:    0  0  0  0  0  0  0  0
Rem:      -  -  -  -  -  1  -  -
                        ↑ "alice" stored here
```

**Add "bob":**
```
hash("bob") → f_q = 3, f_r = 15

Bucket:  [0][1][2][3][4][5][6][7]
Occ:      0  0  0  1  0  1  0  0
Cont:     0  0  0  0  0  0  0  0
Shift:    0  0  0  0  0  0  0  0
Rem:      -  -  - 15  -  1  -  -
                  ↑ "bob"    ↑ "alice"
```

**Add "charlie":**
```
hash("charlie") → f_q = 3, f_r = 7 (collision with "bob"!)

Run for bucket 3 already has remainder 15
Insert 7 (sorted order: 7 < 15)
Shift 15 forward:

Bucket:  [0][1][2][3][4][5][6][7]
Occ:      0  0  0  1  0  1  0  0
Cont:     0  0  0  0  1  0  0  0  ← bucket 4 is continuation
Shift:    0  0  0  0  1  0  0  0  ← bucket 4 is shifted
Rem:      -  -  -  7 15  1  -  -
                  ↑ ↑     ↑
              "charlie" (shifted) "alice"
                "bob"
```

**Test membership of "alice":**
```
hash("alice") → f_q = 5, f_r = 1

1. Bucket 5: is_occupied = 1 ✓
2. Scan left: bucket 3 has is_shifted = 0 (run start)
3. Scan right counting runs:
   - Bucket 3: run #1 (is_occupied=1, is_cont=0)
   - Bucket 4: still run #1 (is_occupied=0, is_cont=1)
   - Bucket 5: run #2 (is_occupied=1, is_cont=0) ← this is our run!
4. Search run: remainder at bucket 5 is 1
5. f_r = 1 matches! → "alice" is PROBABLY in filter ✓
```

### Quotient Filter Properties

**Advantages:**
1. **False positives possible** (but low probability)
2. **False positives tunable** (choose p based on desired rate)
3. **No false negatives**
4. **Supports deletion!** (can remove remainders)
5. **Faster than Bloom filter** (single hash function)
6. **Better for disk** (one random access, then sequential)

**Hash function requirements:**
- Must generate **uniformly distributed** fingerprints
- Non-cryptographic is fine (e.g., MurmurHash)

**Run length analysis:**
- Most runs have length **O(1)**
- Probable that most runs have length **O(log m)**
- Efficient for large number of elements

### Comparison: Quotient vs Bloom

| Feature | Bloom Filter | Quotient Filter |
|---------|--------------|-----------------|
| Space | m bits | m × (r + 3) bits (≈20% bigger) |
| Hash functions | k (typically 5-10) | 1 |
| Lookup speed | Evaluate k hashes | Evaluate 1 hash + scan |
| Deletion | No | Yes ✓ |
| Disk performance | Poor (k random I/Os) | Good (1 random + sequential) |
| False positives | Yes (tunable) | Yes (tunable) |
| False negatives | No | No |

**Bottom line:**
- Quotient filters are about **20% bigger**
- But **faster** (single hash)
- Support **deletion**
- Better for **disk-based** systems

---

## Recent AMQ Approaches <a name="recent-amq"></a>

### 2014 - Cuckoo Filters

**Authors:** Fan, Andersen, Kaminsky, Mitzenmacher

**Key ideas:**
- Based on cuckoo hashing
- Support deletion like quotient filters
- Better space efficiency than Bloom filters
- Fast lookups and insertions

**Properties:**
- Uses 2 hash functions and 2 candidate buckets per item
- Stores fingerprints in buckets
- If both buckets full, "kick out" existing item and relocate

**Advantages:**
- Deletion support
- Better space than Bloom for same false positive rate
- Fast operations

### 2017 - Counting Quotient Filters

**Extension of quotient filters with counting support**
- Track multiplicity of elements
- Space-efficient frequency estimation
- Maintains quotient filter benefits (deletion, single hash)

### 2018 - Morton Filters

**Idea:** Improve cache efficiency
- Better memory layout
- Faster in practice due to cache locality
- Combines ideas from Bloom and quotient filters

### 2020 - Xor Filters

**Authors:** Graf, Lemire

**Key innovation:**
- Uses XOR operations
- **Static** filter (no insertion after construction)
- Very space-efficient
- Fast queries

**Properties:**
- Smaller than Bloom filters
- Faster construction
- Good for static datasets

### 2022 - Binary Fuse Filters

**Further improvement on Xor filters:**
- Even more space-efficient
- Faster construction
- Better for modern CPUs

### 2023 - Adaptive Cuckoo Filters

**Adapt to workload:**
- Adjust parameters based on access patterns
- Optimize for specific use cases

### Aug 2024 - Bloom Filter Variants

**Recent research:**
- Learned Bloom filters (use machine learning)
- Compressed Bloom filters
- Hardware-accelerated implementations

### Sept 2024 - Adaptive Quotient Filters

**Latest development:**
- Quotient filters that adapt to data
- Balance space and performance dynamically

---

## Practice Problems <a name="practice-problems"></a>

### Probabilistic Counters

**EASY:**

**1. Fixed Probability Counter (p=1/2)**
```
Given: Counter with p=1/2, n=100 events
Questions:
a) What is E[counter value]?
b) What is σ²(counter value)?
c) What is the estimate of n from counter value 48?

Solutions:
a) E[S] = n × p = 100 × 0.5 = 50
b) σ²(S) = n × p × (1-p) = 100 × 0.5 × 0.5 = 25
c) Estimate = 2 × 48 = 96 (actual: 100, error: 4%)
```

**2. Fixed Probability Counter (p=1/32)**
```
Given: Counter with p=1/32, n=1000 events
Questions:
a) What is E[counter value]?
b) How do you estimate n from counter value k?
c) If counter = 30, estimate n.

Solutions:
a) E[S] = 1000 × (1/32) = 31.25
b) Estimate = 32 × k
c) Estimate = 32 × 30 = 960 (actual: 1000, error: 4%)
```

**3. Morris Counter - Capacity**
```
Question: How many events can a 5-bit Morris counter (binary base) represent?

Solution:
With b=5 bits:
Maximum counter value = 2^5 = 32
Maximum events ≈ 2^32 - 1 ≈ 4.3 billion

Compare to traditional: 2^5 = 32 events
Improvement: >100 million times!
```

**MEDIUM:**

**4. Probability Distribution**
```
For counter with p=1/2, n=4 events:
Calculate probability distribution p(4, k) for k=0,1,2,3,4

Solution:
p(4, 0) = C(4,0) × (1/2)^4 = 1/16 = 0.0625
p(4, 1) = C(4,1) × (1/2)^4 = 4/16 = 0.25
p(4, 2) = C(4,2) × (1/2)^4 = 6/16 = 0.375 ← most probable
p(4, 3) = C(4,3) × (1/2)^4 = 4/16 = 0.25
p(4, 4) = C(4,4) × (1/2)^4 = 1/16 = 0.0625

Verify: sum = 1.0 ✓
```

**5. Morris Counter - Expected Value**
```
Question: After how many events does Morris counter (binary)
reach expected value of 10?

Solution:
E[counter] = log₂(n+1)
10 = log₂(n+1)
2^10 = n+1
n = 1023 events
```

**6. Csurös Counter - Comparison**
```
Compare Csurös counter with d=0, d=4, d=8 for n=1000 events.
Estimate space and accuracy.

Solution:
d=0 (Morris):
- Space: log₂(log₂(1000)) ≈ 3.3 bits
- Deterministic: 1 event
- Accuracy: Lower

d=4:
- Space: 4 + 3.3 ≈ 7.3 bits
- Deterministic: 16 events
- Accuracy: Medium

d=8:
- Space: 8 + 3.3 ≈ 11.3 bits
- Deterministic: 256 events
- Accuracy: High (perfect for first 256!)
```

**HARD:**

**7. Morris Counter - Arbitrary Base**
```
Given: Morris counter with base a = √2
Question: After counter reaches value 15, estimate number of events.

Solution:
Estimate = (a^k - a + 1) / (a - 1)
         = ((√2)^15 - √2 + 1) / (√2 - 1)
         = (181.02 - 1.414 + 1) / 0.414
         = 180.6 / 0.414
         ≈ 436 events
```

**8. Probability Analysis**
```
For Morris counter (binary), compute p(7, 3) - probability
that counter = 3 after 7 events.

Solution:
Use recurrence:
p(n, k) = (1/2^(k-1)) × p(n-1, k-1) + (1 - 1/2^k) × p(n-1, k)

Build table... (complex calculation)
Answer: p(7, 3) ≈ 0.2734
```

### Bloom Filters

**EASY:**

**9. Basic Bloom Filter**
```
Given: n = 1000 items, m = 8000 bits, k = 6 hash functions
Question: Estimate false positive rate.

Solution:
p ≈ (1 - e^(-kn/m))^k
  ≈ (1 - e^(-6×1000/8000))^6
  ≈ (1 - e^(-0.75))^6
  ≈ (1 - 0.472)^6
  ≈ (0.528)^6
  ≈ 0.0195 = 1.95%
```

**10. Optimal k**
```
Given: m/n = 10 bits per element
Question: What is optimal k?

Solution:
k_opt = (m/n) × ln(2)
      = 10 × 0.693
      = 6.93
      ≈ 7 hash functions
```

**11. Space Calculation**
```
Given: Need n = 1 million items with p = 0.01 (1% false positives)
Question: How much space needed?

Solution:
m = -n × ln(p) / (ln(2))²
  = -10^6 × ln(0.01) / (0.693)²
  = -10^6 × (-4.605) / 0.48
  = 9,593,750 bits
  ≈ 1.2 MB
```

**MEDIUM:**

**12. Comparison: Bloom vs Hash Table**
```
Compare space for storing 1 billion URLs:
a) Hash table (8 bytes per pointer + 100 bytes per URL average)
b) Bloom filter (1% false positive rate)

Solution:
a) Hash table: 10^9 × 108 bytes = 108 GB

b) Bloom filter:
   m = -10^9 × ln(0.01) / (ln(2))² ≈ 9.6 billion bits ≈ 1.2 GB

Bloom filter is 90× smaller!
```

**13. Multiple Hash Functions**
```
Given: Two hash functions h₁ and h₂
Show how to simulate k=5 hash functions.

Solution:
For i = 0, 1, 2, 3, 4:
   hᵢ(x) = (h₁(x) + i × h₂(x)) mod m

Example with h₁(x)=100, h₂(x)=23, m=1000:
h₀(x) = (100 + 0×23) mod 1000 = 100
h₁(x) = (100 + 1×23) mod 1000 = 123
h₂(x) = (100 + 2×23) mod 1000 = 146
h₃(x) = (100 + 3×23) mod 1000 = 169
h₄(x) = (100 + 4×23) mod 1000 = 192
```

**14. Counting Bloom Filter**
```
Given: CBF with w=4 bits, k=3
After insertions, counters at positions [5, 12, 18] are [3, 7, 5]
Question: What is estimated frequency?

Solution:
Frequency estimate = min(3, 7, 5) = 3
(Conservative estimate using minimum)
```

**HARD:**

**15. Quotient Filter**
```
Given: p=12 bits, q=8, r=4
Element hash to fingerprint f = 0b101101110011

Questions:
a) What is quotient f_q?
b) What is remainder f_r?
c) In which bucket is remainder stored (assuming no collisions)?

Solution:
a) f_q = upper 8 bits = 0b10110111 = 183
b) f_r = lower 4 bits = 0b0011 = 3
c) Stored in bucket 183 (canonical bucket)
```

**CHALLENGE:**

**16. Implement Morris Counter Simulator**
```
Task: Write Python code to:
- Simulate Morris counter for n events
- Run 10000 trials
- Compare experimental vs theoretical results
- Plot probability distribution

(See implementation section for solution)
```

**17. Bloom Filter Analysis**
```
Given: Bloom filter with n=10^6, m=10^7, k=7
After all insertions, count that 6,321,205 bits are set to 1.

Questions:
a) What is actual fraction f of bits set?
b) What is actual false positive rate?
c) Compare with theoretical FPR.

Solution:
a) f = 6,321,205 / 10^7 = 0.6321

b) Actual FPR = f^k = (0.6321)^7 ≈ 0.0155 = 1.55%

c) Theoretical:
   p ≈ (1 - e^(-7×10^6/10^7))^7
     ≈ (1 - e^(-0.7))^7
     ≈ (0.5034)^7
     ≈ 0.0078 = 0.78%

   Actual is higher! Possibly:
   - More items inserted than expected
   - Hash functions not perfectly independent
```

---

## Summary & Exam Tips <a name="summary"></a>

### Probabilistic Counters - Key Concepts

**1. Fixed Probability Counters:**
- **p = 1/2:** E[S] = n/2, σ²(S) = n/4, estimate = 2×counter
- **p = 1/2^k:** E[S] = n/2^k, estimate = 2^k × counter
- **General p:** E[S] = n×p, σ²(S) = n×p×(1-p)
- **Distribution:** Binomial with parameters (n, p)

**2. Morris Counter (Binary Base):**
- **Algorithm:** Increment with probability 1/2^(counter value)
- **Expected events for counter=k:** n(k) = 2^k - 1
- **Estimation:** n ≈ 2^counter - 1
- **Space:** log log n bits (amazing!)
- **Capacity (b bits):** 2^(2^b) - 1

**3. Morris Counter (Arbitrary Base a):**
- **Algorithm:** Increment with probability 1/a^(counter value)
- **Estimation:** n ≈ (a^counter - a + 1) / (a - 1)
- **Better accuracy:** Use a < 2 (e.g., √2)

**4. Csurös Counter:**
- **Structure:** d-bit significand + exponent
- **First M = 2^d steps:** Deterministic (exact!)
- **Estimation:** (M + u) × 2^t - M
- **Trade-off:** Larger d → better accuracy, more space

### Bloom Filters - Key Formulas

**1. Parameters:**
- **n:** number of items
- **m:** number of bits
- **k:** number of hash functions
- **p:** false positive rate

**2. Optimal k:**
```
k_opt = (m/n) × ln(2) ≈ 0.693 × (m/n)
```

**3. False Positive Rate:**
```
p ≈ (1 - e^(-kn/m))^k
```

**4. Space Required:**
```
m = -n × ln(p) / (ln(2))²  ≈ -1.44 × n × ln(p)
```

**5. No false negatives!**

**6. Cannot delete (standard BF)**

### Counting Bloom Filters

**1. Use w-bit counters (typically w=4)**

**2. Space:** w × m bits (w× overhead)

**3. Operations:**
- **Insert:** increment k counters
- **Delete:** decrement k counters (may cause false negatives!)
- **Count:** min of k counters

**4. Issues:**
- Counter overflow (undercount)
- False negatives from deletion

### Quotient Filters

**1. Structure:**
- Fingerprint = quotient + remainder
- Store remainder in bucket indexed by quotient
- 3 auxiliary bits: is_occupied, is_continuation, is_shifted

**2. Advantages:**
- Single hash function (faster!)
- Supports deletion
- Better for disk (sequential access)

**3. Trade-offs:**
- About 20% larger than Bloom filter
- More complex implementation

### Common Exam Questions

**1. Calculate Expected Value & Variance:**
- Know formulas for different counter types
- Practice with various values of n, p, k

**2. Estimate Events from Counter:**
- Fixed prob: n ≈ (1/p) × counter
- Morris binary: n ≈ 2^counter - 1
- Morris arbitrary: n ≈ (a^counter - a + 1) / (a - 1)
- Csurös: (M + u) × 2^t - M

**3. Bloom Filter Design:**
- Given n and p, calculate m and k
- Given m and n, find optimal k
- Calculate false positive rate

**4. Probability Distributions:**
- Binomial distribution for fixed probability
- Recurrence relations for Morris counter
- Pascal-like triangles

**5. Space Analysis:**
- Compare traditional vs probabilistic counters
- Bloom filter vs hash table
- Counting Bloom vs standard Bloom

**6. Implementation:**
- Write pseudocode or Python for counters
- Implement Bloom filter operations
- Understand hash function simulation

### Important Insights

**1. Probabilistic Counters:**
- **Trade-off:** Accuracy vs space
- **Use case:** Massive data, many counters
- **Key insight:** Logarithmic growth is powerful!

**2. Bloom Filters:**
- **Trade-off:** Space vs false positive rate
- **Use case:** Membership testing, pre-filtering
- **Key insight:** k hash functions create redundancy

**3. General Principles:**
- **Approximate answers** can be good enough
- **Probabilistic methods** save massive space
- **No free lunch:** Always trade-offs to consider

### Study Strategy

**1. Master the formulas:**
- Write them on flashcards
- Practice calculations by hand
- Understand derivations (at least intuitively)

**2. Code implementations:**
- Write Morris counter from scratch
- Implement Bloom filter
- Run experiments and verify against theory

**3. Solve practice problems:**
- Work through all problems in this guide
- Time yourself (exam conditions)
- Check your answers carefully

**4. Understand trade-offs:**
- When to use each method?
- What are the pros/cons?
- Real-world applications?

**5. Draw diagrams:**
- Binary trees for probability paths
- Pascal-like triangles
- State diagrams
- Bloom filter bit arrays

### Quick Reference Table

| Data Structure | Space | Insert | Query | Delete | False+ | False- |
|----------------|-------|--------|-------|--------|--------|--------|
| Hash Table | O(n) | O(1) | O(1) | O(1) | No | No |
| Bloom Filter | O(m) | O(k) | O(k) | No | Yes | No |
| Counting Bloom | O(wm) | O(k) | O(k) | O(k) | Yes | Yes* |
| Quotient Filter | O(m) | O(1)† | O(1)† | O(1)† | Yes | No |

†Amortized time

*Only if delete item not in filter

### Final Tips

**Before the exam:**
1. Review all formulas (write them out)
2. Solve practice problems (all of them!)
3. Understand conceptual questions
4. Know when to use each method
5. Get good sleep!

**During the exam:**
1. Read questions carefully (twice!)
2. Identify what's given, what's asked
3. Write down relevant formulas first
4. Show your work (partial credit!)
5. Double-check calculations
6. Manage your time wisely

**Good luck! 🍀**

---

## References

### Probabilistic Counters

- R. Morris, "Counting Large Numbers of Events in Small Registers," Communications of the ACM, Vol. 21, N. 10, October 1978

- P. Flajolet, "Approximate Counting: A Detailed Analysis," BIT, Vol. 25, 1985

- M. Csurös, "Approximate counting with a floating-point counter," COCOON, LNCS vol. 6196, p. 358-367, Springer, 2010

### Bloom Filters & AMQ

- B. H. Bloom, "Space/Time Trade-offs in Hash Coding with Allowable Errors," Communications of the ACM, July 1970

- J. Blustein and A. El-Maazaw, "Bloom Filters – A Tutorial, Analysis, and Survey," TR CS 2002-10, Dalhousie University, 2002

- A. Broder and M. Mitzenmacher, "Network Applications of Bloom Filters: A Survey," Internet Mathematics, Vol. 1, N. 4, 2004

- Michael A. Bender et al., "Don't Thrash: How to Cache Your Hash on Flash," VLDB 2012

### General Resources

- J. Leskovec, A. Rajaraman and J. D. Ullman, "Mining of Massive Datasets," 2014 – Chapter 4

- M. Mitzenmacher, "Bloom Filters and Such," 2014 Summer School on Hashing, Copenhagen

- A. Gakhov, "Probabilistic Data Structures and Algorithms for Big Data Applications," 2019

---

*End of Study Guide*
