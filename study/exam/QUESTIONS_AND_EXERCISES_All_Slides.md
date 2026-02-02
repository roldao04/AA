# COMPREHENSIVE QUESTIONS & EXERCISES STUDY GUIDE
**Advanced Algorithms - All Slides (01-13)**

**Study Focus**: This guide contains questions and exercises directly extracted from the course slides, with **priority on probability calculation problems** (coin tosses, dice rolls, probabilistic counters, Bloom filters). These are manual calculation exercises, not coding tasks.

---

## TABLE OF CONTENTS

### PART I: PROBABILITY CALCULATIONS (PRIORITY)
- **Section A**: Basic Probability & Statistical Experiments (Slides 06-07)
- **Section B**: Probabilistic Counters (Slide 09)
- **Section C**: Bloom Filters & AMQ Structures (Slide 10)

### PART II: ALGORITHM ANALYSIS & IMPLEMENTATION
- **Section D**: Data Stream Algorithms (Slides 11-13)
- **Section E**: Randomized Algorithms (Slide 08)
- **Section F**: Algorithm Design Strategies (Slides 01-05)

---

# PART I: PROBABILITY CALCULATIONS (PRIORITY)

---

## Section A: Basic Probability & Statistical Experiments

### A.1 COIN EXPERIMENTS (Slide 06)

#### Question A.1.1: Balanced Coin - 3 Tosses
**Source**: Slide 06, Lines 556-581
**Difficulty**: ⭐⭐ Medium

**Problem**: Toss a balanced coin 3 times.

**Tasks**:
1. Represent this experiment using:
   - Binary table
   - Binary tree
   - Directed Graph (order important)
2. Create a table showing the probability distribution for counting heads
3. What is the probability of getting:
   - Exactly 0 heads?
   - Exactly 1 head?
   - Exactly 2 heads?
   - Exactly 3 heads?

**Space for solution**:
```
Your work here...
```

---

#### Question A.1.2: Biased Coin - 3 Tosses
**Source**: Slide 06, Lines 597-612
**Difficulty**: ⭐⭐⭐ Hard

**Problem**: Toss a biased coin 3 times. The coin turns up heads only **45% of the time**.

**Tasks**:
1. What changes are needed in the representations from A.1.1?
2. Draw the binary tree with probabilities on each branch
3. Create a table showing the probability distribution for counting heads
4. Compare with the balanced coin case - what differences do you observe?

**Space for solution**:
```
Your work here...
```

---

#### Question A.1.3: Two Balanced Coins - n Tosses
**Source**: Slide 06, Lines 699-710
**Difficulty**: ⭐⭐ Medium

**Problem**: Toss **two balanced coins** n times simultaneously.

**Tasks**:
1. Record the total score (1 for heads, 0 for tails)
2. What do you expect for the distribution?
3. For n=1, what are the possible outcomes and their probabilities?

**Space for solution**:
```
Your work here...
```

---

### A.2 DIE EXPERIMENTS (Slide 06)

#### Question A.2.1: Balanced Die - 2 Throws
**Source**: Slide 06, Lines 641-653
**Difficulty**: ⭐⭐ Medium

**Problem**: Throw a standard 6-sided die 2 times.

**Tasks**:
1. Count the total number of "eyes" (dots)
2. Represent using:
   - 6-ary tree
   - Directed Graph
   - Table of probability distribution
3. What is the most probable sum?
4. What is the probability of getting a sum of 7?

**Space for solution**:
```
Your work here...
```

---

#### Question A.2.2: Biased Die - 2 Throws
**Source**: Slide 06, Lines 656-681
**Difficulty**: ⭐⭐⭐ Hard

**Problem**: Throw an unfair die 2 times, where **an ace (1) is twice as likely to turn up as any other face**.

**Tasks**:
1. First, determine the probability of each face (1, 2, 3, 4, 5, 6)
2. What are the needed changes in the representations?
3. Draw the 6-ary tree with probabilities
4. Create the probability distribution table for the sum

**Hint**: Let P(2) = P(3) = P(4) = P(5) = P(6) = p. Then P(1) = 2p. Use the fact that all probabilities sum to 1.

**Space for solution**:
```
Your work here...
```

---

#### Question A.2.3: Pair of Fair Dice - n Throws
**Source**: Slide 06, Lines 712-719
**Difficulty**: ⭐⭐ Medium

**Problem**: Throw a pair of fair dice n times.

**Tasks**:
1. Record the sum of the faces that turn up
2. What do you expect for the distribution?
3. For n=1, create the complete probability distribution

**Space for solution**:
```
Your work here...
```

---

### A.3 COMPOUND EXPERIMENTS (Slide 06)

#### Question A.3.1: Die-Coin Experiment
**Source**: Slide 06, Lines 737-762
**Difficulty**: ⭐⭐⭐ Hard

**Problem**: A standard die is thrown, and then a coin is tossed **the number of times shown on the die**.

**Tasks**:
1. Draw the tree representing this compound experiment
2. What is the probability of getting **6 heads**?
3. What is the probability of getting **0 heads**?
4. Create a complete table of probability distribution for the number of heads

**Space for solution**:
```
Your work here...
```

---

#### Question A.3.2: Coin-Dice Experiment
**Source**: Slide 06, Lines 764-790
**Difficulty**: ⭐⭐⭐ Hard

**Problem**: A coin is tossed. If heads: throw a **red die**. If tails: throw a **green die**.

**Tasks**:
1. Draw the tree representing this compound experiment
2. What is the probability of getting 6 eyes?
3. What is the probability of getting 6 **green** eyes?
4. Create a table of probability distribution (consider both color and score)

**Space for solution**:
```
Your work here...
```

---

### A.4 SIMPLE GAMES (Slide 06)

#### Question A.4.1: Two Dice Game - Red vs Green
**Source**: Slide 06, Lines 821-835
**Difficulty**: ⭐⭐ Medium

**Problem**: You pay 1 euro to roll two dice (one red, one green). You win 2 euros if there are more eyes on the red die than on the green die.

**Tasks**:
1. Calculate the probability of winning (red > green)
2. Calculate the probability of losing (red ≤ green)
3. What is your expected profit/loss per game?
4. **Should you play this game?** Justify mathematically.

**Space for solution**:
```
Your work here...
```

---

#### Question A.4.2: Guessing Game
**Source**: Slide 06, Lines 837-848
**Difficulty**: ⭐⭐⭐ Hard

**Problem**: You roll two dice and, beforehand, guess the sum: n eyes. If correct, you earn **n euros**. Otherwise, you **pay 1 euro**.

**Tasks**:
1. For each possible guess (2 through 12), calculate:
   - Probability of winning
   - Expected value of that guess
2. What is the optimal guess?
3. What is your expected profit/loss with optimal strategy?
4. **Should you play this game?** Justify.

**Space for solution**:
```
Your work here...
```

---

### A.5 BASIC PROBABILITY THEORY (Slide 07)

#### Question A.5.1: Fair Die - Basic Probabilities
**Source**: Slide 07, Lines 233-252
**Difficulty**: ⭐ Easy

**Problem**: Throwing a 6-sided fair die.

**Calculate**:
1. Probability of getting an **even number**
2. Probability of getting a number **larger than 2**
3. Probability of getting an even number **OR** a number larger than 2

**Hint**: Remember P(A ∪ B) = P(A) + P(B) - P(A ∩ B)

**Space for solution**:
```
Your work here...
```

---

#### Question A.5.2: Three Fair Coins
**Source**: Slide 07, Lines 256-276
**Difficulty**: ⭐⭐ Medium

**Problem**: Tossing three fair coins.

**Tasks**:
1. What is the sample space S₃?
2. What is the probability of getting **at least one head**?
3. What is the probability of getting **at least two heads**?

**Hints**:
- Consider the binary representation
- Use triangular representation with paths

**Space for solution**:
```
Your work here...
```

---

#### Question A.5.3: n Fair Coins - General Case
**Source**: Slide 07, Lines 278-298
**Difficulty**: ⭐⭐⭐ Hard

**Problem**: Tossing **n** fair coins.

**Calculate**:
1. Probability of getting "head" **exactly k times**
2. Probability of getting "head" **at least k times**

**Hint**: Use the binomial distribution formula.

**Space for solution**:
```
Your work here...
```

---

#### Question A.5.4: Binomial Distribution ⭐ KEY QUESTION
**Source**: Slide 07, Lines 317-332
**Difficulty**: ⭐⭐⭐ Hard

**Problem 1**: What is the probability of getting **6 heads in 15 tosses** of a **fair coin**?

**Tasks**:
1. Calculate using the binomial distribution formula
2. Verify your answer

**Problem 2**: Now consider that **P[heads] = 2 × P[tails]**

**Tasks**:
1. First, find P[heads] and P[tails] (they must sum to 1)
2. Calculate the probability of getting 6 heads in 15 tosses with this biased coin
3. Compare with the fair coin result

**Space for solution**:
```
Your work here...
```

---

### A.6 FAMOUS PROBABILITY PROBLEMS (Slide 07)

#### Question A.6.1: Problem 1 - Coin Until Second Repetition ⭐ KEY PROBLEM
**Source**: Slide 07, Lines 697-722
**Difficulty**: ⭐⭐⭐ Hard

**Problem**: A fair coin is tossed repeatedly until one of the faces appears **for the second time**.

**Examples of outcomes**:
- (H, T, H) → Y = 3 tosses
- (T, T) → Y = 2 tosses
- (H, H) → Y = 2 tosses
- (T, H, T) → Y = 3 tosses

**Tasks**:
1. Let Y = random variable representing the number of tosses needed
2. What are all possible values of Y?
3. Calculate P(Y = 2)
4. Calculate P(Y = 3)
5. Calculate P(Y = 4)
6. What is E[Y] (expected value)?

**Space for solution**:
```
Your work here...
```

---

#### Question A.6.2: Problem 2 - Die Until Second Repetition
**Source**: Slide 07, Lines 725-750
**Difficulty**: ⭐⭐⭐⭐ Very Hard

**Problem**: A fair die is thrown repeatedly until one of the faces appears **for the second time**.

**Examples of outcomes**:
- (3, 6, 2, 6) → Y = 4 throws
- (5, 5) → Y = 2 throws
- (1, 4, 3, 6, 2, 4) → Y = 6 throws

**Tasks**:
1. Let Y = random variable representing the number of throws needed
2. What are all possible values of Y?
3. Calculate P(Y = 2)
4. Calculate P(Y = 3)
5. Calculate P(Y = 7) (the maximum)
6. What is E[Y] (expected value)?

**Hint**: This is harder than the coin version because there are 6 faces instead of 2.

**Space for solution**:
```
Your work here...
```

---

#### Question A.6.3: Problem 3 - The Birthday Paradox ⭐ KEY PROBLEM
**Source**: Slide 07, Lines 753-775
**Difficulty**: ⭐⭐⭐⭐ Very Hard

**Problem**: In a party with **n people**, what is the probability of at least two of them celebrating their birthday on the same day?

**Tasks**:
1. Calculate this probability for n = 10, 20, 23, 30, 40, 50, 60
2. What is the **smallest n** that guarantees the probability is **above 50%**?
3. Why is this called a "paradox"?

**Assumptions**:
- Each birthday is equally likely (ignore leap years)
- 365 days in a year

**Hint**: It's easier to calculate the probability that NO two people share a birthday, then subtract from 1.

**Space for solution**:
```
Your work here...
```

---

#### Question A.6.4: Problem 4 - Collision Problem
**Source**: Slide 07, Lines 820-867
**Difficulty**: ⭐⭐⭐ Hard

**Problem**: Consider **n = 4000**.

**Experiment**:
1. Generate random numbers in the domain [n] = {0, 1, 2, ..., 3999}
2. Keep generating until **two numbers have the same value** (collision)
3. Let k = number of random trials needed

**Tasks (Theoretical)**:
1. What is the expected value of k?
2. What is the probability of collision after √n ≈ 63 trials?
3. What is the probability of collision after 2√n ≈ 126 trials?

**Hint**: This is related to the Birthday Paradox.

**Space for solution**:
```
Your work here...
```

---

#### Question A.6.5: Problem 5 - Coin Until All Faces ⭐ Coupon Collector
**Source**: Slide 07, Lines 870-895
**Difficulty**: ⭐⭐ Medium

**Problem**: A fair coin is tossed repeatedly until **each face has appeared at least once**.

**Examples of outcomes**:
- (H, T) → Y = 2 tosses
- (T, T, H) → Y = 3 tosses
- (H, H, H, T) → Y = 4 tosses

**Tasks**:
1. Let Y = random variable representing the number of tosses needed
2. What is the minimum value of Y?
3. Calculate P(Y = 2)
4. Calculate P(Y = 3)
5. Calculate P(Y = 4)
6. What is E[Y] (expected value)?

**Space for solution**:
```
Your work here...
```

---

#### Question A.6.6: Problem 6 - Die Until All Faces ⭐ Coupon Collector
**Source**: Slide 07, Lines 898-924
**Difficulty**: ⭐⭐⭐ Hard

**Problem**: A fair die is thrown repeatedly until **each face has appeared at least once**.

**Examples of outcomes**:
- (1, 2, 4, 5, 3, 6) → Y = 6 throws
- (1, 2, 1, 4, 3, 5, 3, 6) → Y = 8 throws

**Tasks**:
1. Let Y = random variable representing the number of throws needed
2. What is the minimum value of Y?
3. Calculate P(Y = 6)
4. What is E[Y] (expected value)?

**Hint**: This is the classic **Coupon Collector Problem**. The expected value has a known formula: E[Y] = n × H_n, where H_n = 1 + 1/2 + 1/3 + ... + 1/n

**Space for solution**:
```
Your work here...
```

---

#### Question A.6.7: Problem 7 - Coupon Collector General Case
**Source**: Slide 07, Lines 926-971
**Difficulty**: ⭐⭐⭐⭐ Very Hard

**Problem**: Consider **n = 200**.

**Experiment**:
1. Generate random numbers in the domain [n] = {0, 1, ..., 199}
2. Keep generating until **every value i in [n] has appeared at least once**
3. Let k = number of random trials needed

**Tasks (Theoretical)**:
1. What is E[k] (expected number of trials)?
2. Calculate using the formula: E[k] = n × (1 + 1/2 + 1/3 + ... + 1/n)
3. Approximate E[k] ≈ n × ln(n) + n × γ, where γ ≈ 0.5772 (Euler's constant)

**Space for solution**:
```
Your work here...
```

---

#### Question A.6.8: Problem 8 - Blind-Folded Darts (Extra)
**Source**: Slide 07, Lines 984-1001
**Difficulty**: ⭐⭐⭐ Hard

**Problem**: In a blind-folded game of darts:
- **n darts** are thrown to **m targets**
- Each dart reaches one and only one target

**Tasks**:
1. What is the probability of **no target being hit more than once**?
2. What is the probability of **at least one target being hit at least twice**?

**Hint**: These two probabilities are complementary.

**Space for solution**:
```
Your work here...
```

---

### A.7 MONTE CARLO METHODS (Slide 08)

#### Question A.7.1: Birth Rate Probability
**Source**: Slide 08, Lines 125-136
**Difficulty**: ⭐⭐ Medium

**Problem**: The birth rate ratio of boys to girls is **51 to 49**.

**Task**: What is the probability of having **two children who are both girls**?

**Assumptions**:
- Births are independent events
- Each birth follows the 51:49 ratio

**Space for solution**:
```
Your work here...
```

---

## Section B: Probabilistic Counters (Slide 09)

---

### B.1 FIXED PROBABILITY COUNTERS - p = 1/2

#### Question B.1.1: State Diagram and Binary Tree
**Source**: Slide 09, Lines 167-211
**Difficulty**: ⭐⭐ Medium

**Problem**: For each event, increment the counter with probability **1/2** (coin toss).

**Tasks**:
1. Draw the **state diagram** for counter values 0, 1, 2, 3
2. Draw the **binary tree diagram** showing all possible paths for 4 events
3. Label each branch with its probability

**Space for solution**:
```
Your work here...
```

---

#### Question B.1.2: Expected Value - p = 1/2 ⭐ KEY CALCULATION
**Source**: Slide 09, Lines 336-366
**Difficulty**: ⭐⭐⭐ Hard

**Problem**: Counter increments with probability p = 1/2.

**Given**:
- X_i represents the i-th increment
- X_i = 1 (counter incremented) with probability 1/2
- X_i = 0 (not incremented) with probability 1/2
- After k events, S = ∑ X_i

**Tasks**:
1. Calculate E[X_i]
2. Calculate E[S] after k events
3. How can you estimate the number of events from counter value S?

**Space for solution**:
```
Your work here...
```

---

#### Question B.1.3: Variance - p = 1/2 ⭐ KEY CALCULATION
**Source**: Slide 09, Lines 369-382
**Difficulty**: ⭐⭐⭐ Hard

**Problem**: Continue from B.1.2.

**Tasks**:
1. Calculate E[X_i²]
2. Calculate σ²(X_i) = E[X_i²] - {E[X_i]}²
3. Calculate σ²(S) after k events
4. Calculate σ(S) (standard deviation)

**Space for solution**:
```
Your work here...
```

---

#### Question B.1.4: Probability Distribution - p = 1/2 ⭐ KEY QUESTION
**Source**: Slide 09, Lines 423-462
**Difficulty**: ⭐⭐⭐⭐ Very Hard

**Problem**: After **n events**, what is the probability of the counter value being **k**?

Let **p(n, k)** denote this probability.

**Example for n = 4**:
1. What are the more probable counter values?
2. What are the less probable counter values?
3. Calculate p(4, 0), p(4, 1), p(4, 2), p(4, 3), p(4, 4)

**Tasks**:
1. Draw the binary tree diagram for n = 4
2. Draw the Pascal-like triangle
3. Identify the pattern
4. What distribution does this follow?

**Space for solution**:
```
Your work here...
```

---

### B.2 FIXED PROBABILITY COUNTERS - p = 1/2^k

#### Question B.2.1: State Diagram and Binary Tree - p = 1/2^k
**Source**: Slide 09, Lines 528-562
**Difficulty**: ⭐⭐⭐ Hard

**Problem**: For each event, increment the counter with probability **p = 1/2^k** (e.g., k=2 gives p=1/4, k=3 gives p=1/8).

**Tasks**:
1. Draw the state diagram for p = 1/4
2. Draw the binary tree diagram
3. Draw the Pascal-like triangle

**Space for solution**:
```
Your work here...
```

---

#### Question B.2.2: Mean and Variance - General p ⭐ KEY FORMULA
**Source**: Slide 09, Lines 564-593
**Difficulty**: ⭐⭐⭐ Hard

**Problem**: Incrementing with probability **p**, where q = (1 - p).

**Derive**:
1. E[S] after n events (in terms of n and p)
2. σ²(S) after n events (in terms of n, p, and q)

**Verify for specific cases**:
- p = 1/2: Should match B.1.2 and B.1.3
- p = 1/32: Calculate E[S] and σ²(S) for n = 100 events

**Space for solution**:
```
Your work here...
```

---

#### Question B.2.3: Probability Distribution - p = 1/32
**Source**: Slide 09, Lines 628-653
**Difficulty**: ⭐⭐⭐⭐ Very Hard

**Problem**: For **p = 1/32** and various values of n (10, 100, 1000, ...).

**Tasks**:
1. Compute the probability distributions for possible counter values
2. Compute the mean and variance from the distribution
3. Compare with the theoretical values from B.2.2

**Space for solution**:
```
Your work here...
```

---

### B.3 MORRIS COUNTER (Binary Base - Decreasing Probability)

#### Question B.3.1: State Diagram - Morris Counter
**Source**: Slide 09, Lines 705-735
**Difficulty**: ⭐⭐ Medium

**Problem**: Morris counter (1978) - Binary base with decreasing probability.

**Rule**: If counter has value k, increment it with probability **1/2^k**.

**Tasks**:
1. Draw the state diagram for counter values 0, 1, 2, 3, 4
2. Label each transition with its probability
3. Draw the tree-like diagram

**Space for solution**:
```
Your work here...
```

---

#### Question B.3.2: Events to Reach Counter Value k ⭐ KEY ANALYSIS
**Source**: Slide 09, Lines 737-768
**Difficulty**: ⭐⭐⭐⭐ Very Hard

**Problem**: On average, how many events **n** are needed to reach a counter value of **k**?

**Tasks**:
1. Set up the table:

| Counter value | Number of events needed to increment |
|---------------|--------------------------------------|
| 0 → 1         | X₁                                   |
| 1 → 2         | X₂                                   |
| 2 → 3         | X₃                                   |
| ...           | ...                                  |
| k-1 → k       | X_k                                  |

2. What is E[X₁]? (Expected events to go from 0 to 1)
3. What is E[X₂]? (Expected events to go from 1 to 2)
4. What is E[X_k]? (Expected events to go from k-1 to k)
5. Total expected events: E[Total] = ?

**Hint**: If probability of increment is p, expected events = 1/p.

**Space for solution**:
```
Your work here...
```

---

#### Question B.3.3: Expected Counter Value After n Events ⭐ KEY RESULT
**Source**: Slide 09, Lines 772-848
**Difficulty**: ⭐⭐⭐⭐ Very Hard

**Problem**: After **n** probabilistic updates, what is the expected counter value?

**Given from previous question**:
- To reach counter value k, need approximately 2^k - 1 events

**Tasks**:
1. Invert the relationship: If n events occurred, expected counter value ≈ ?
2. Complete the table:

| Number of events (n) | E[S] Expected counter value | Formula verification |
|----------------------|----------------------------|----------------------|
| 1                    | 1                          | floor(log₂(1+1))     |
| 3                    | 2                          | floor(log₂(3+1))     |
| 7                    | 3                          | floor(log₂(7+1))     |
| 15                   | 4                          | floor(log₂(15+1))    |
| n                    | ?                          | ?                    |

3. Why is this called a "logarithmic counter"?
4. How many bits are needed to store this counter?

**Space for solution**:
```
Your work here...
```

---

#### Question B.3.4: Estimating Events from Counter Value
**Source**: Slide 09, Lines 882-897
**Difficulty**: ⭐⭐⭐ Hard

**Problem**: Given a Morris counter with value **k**, estimate the number of events **n**.

**Tasks**:
1. What is the estimation formula? (n ≈ ?)
2. Calculate estimates for k = 5, 10, 16
3. What is the largest value you can count with:
   - A 4-bit counter?
   - An 8-bit counter?
   - A 16-bit counter?

**Space for solution**:
```
Your work here...
```

---

#### Question B.3.5: Probability Distribution - Morris Counter ⭐ ADVANCED
**Source**: Slide 09, Lines 925-973
**Difficulty**: ⭐⭐⭐⭐⭐ Expert

**Problem**: After **n** events, what is the probability of the Morris counter value being **k**?

**Recurrence relations given**:
- p(1, 1) = 1 and p(1, 0) = 0
- p(n, 1) = (1/2) × p(n-1, 1)
- p(n, n) = (1/2^(n-1)) × p(n-1, n-1)
- p(n, k) = (1/2^(k-1)) × p(n-1, k-1) + (1 - 1/2^k) × p(n-1, k)

**Example for n = 4**:
1. Calculate p(3, k) for all valid k
2. Calculate p(4, k) for all valid k
3. Draw the Pascal-like triangle

**Tasks**:
1. Set up the recursive table
2. Calculate values for n = 1, 2, 3, 4
3. What is the most probable counter value for n = 4?

**Space for solution**:
```
Your work here...
```

---

### B.4 ARBITRARY BASE COUNTERS

#### Question B.4.1: Counter with Base a = 2^(1/2)
**Source**: Slide 09, Lines 995-1062
**Difficulty**: ⭐⭐⭐⭐ Very Hard

**Problem**: Counter with arbitrary base **a**.

**Rule**: If counter has value k, increment with probability **1/a^k**.

**For a = 2^(1/2) ≈ 1.414**:

**Tasks**:
1. Why does taking a < 2 improve accuracy?
2. How do you estimate the number of events from counter value k?
   - Formula: n ≈ (a^k - a + 1) / (a - 1)
3. Calculate the estimate for k = 10, a = 2^(1/2)
4. What is the largest value countable with:
   - A 4-bit counter?
   - An 8-bit counter?
5. Compare with Morris counter (a = 2)

**Space for solution**:
```
Your work here...
```

---

### B.5 CSURÖS' FLOATING-POINT COUNTER

#### Question B.5.1: Understanding Csurös' Counter
**Source**: Slide 09, Lines 1079-1134
**Difficulty**: ⭐⭐⭐⭐ Very Hard

**Problem**: Csurös (2010) - Binary floating-point counter.

**Structure**:
- d-bit significand
- Binary exponent
- Total: d + log log n bits
- M = 2^d (first M steps are deterministic)

**Counter representation**: X = 2^d × t + u
- t = exponent
- u = lower d bits (significand)

**Estimate**: (M + u) × 2^t - M

**Tasks**:
1. For d = 0, show this reduces to Morris counter
2. For d = 3 (M = 8):
   - Counter value X = 19. Calculate t and u.
   - What is the estimated count?
3. Why are the first M steps deterministic?
4. What advantage does this provide?

**Space for solution**:
```
Your work here...
```

---

## Section C: Bloom Filters & AMQ Structures (Slide 10)

---

### C.1 BLOOM FILTER PROBABILITY CALCULATIONS

#### Question C.1.1: Probability After 1 Insertion ⭐ KEY CALCULATION
**Source**: Slide 10, Lines 499-519
**Difficulty**: ⭐⭐⭐ Hard

**Problem**: A Bloom filter has **m** cells (bits), initially all zero. We use **k** hash functions.

**After inserting ONE element**:

**Tasks**:
1. What is the probability that a specific bit b_i = 1 after using the **first** hash function?
   - P(b_i = 1) = ?
   - P(b_i = 0) = ?

2. After computing all **k** hash functions and setting k cells:
   - P(b_i = 0) = ?

**Assumption**: Hash functions distribute uniformly and independently.

**Space for solution**:
```
Your work here...
```

---

#### Question C.1.2: Probability After n Insertions ⭐ KEY FORMULA
**Source**: Slide 10, Lines 535-571
**Difficulty**: ⭐⭐⭐⭐ Very Hard

**Problem**: After inserting **n** elements into the Bloom filter.

**Tasks**:
1. Calculate P(b_i = 0) after n insertions
   - Formula: P(b_i = 0) = (1 - 1/m)^(k×n)

2. Calculate P(b_i = 1) after n insertions
   - Let a = (1 - 1/m)^n
   - Then P(b_i = 1) = 1 - a^k

3. **Approximation**: Show that a ≈ e^(-n/m)
   - Hint: Use the limit: lim_{m→∞} (1 - 1/m)^m = e^(-1)

**Space for solution**:
```
Your work here...
```

---

#### Question C.1.3: False Positive Probability ⭐ CRITICAL FORMULA
**Source**: Slide 10, Lines 573-594
**Difficulty**: ⭐⭐⭐⭐ Very Hard

**Problem**: Calculate the probability of a **false positive**.

**Definition**: Testing membership of an item **not in S** gives a positive answer.

**Tasks**:
1. For a false positive, all k bits corresponding to the item must be set to 1
2. Calculate: p = P(false positive) = (1 - a)^k
3. Using approximation from C.1.2: p ≈ (1 - e^(-kn/m))^k

**Space for solution**:
```
Your work here...
```

---

#### Question C.1.4: Numerical Example - 1 Billion Items ⭐ KEY EXAMPLE
**Source**: Slide 10, Lines 596-613
**Difficulty**: ⭐⭐⭐⭐ Very Hard

**Problem**: A Bloom filter with:
- **n = 1 billion items** (1,000,000,000)
- **m = 8 billion bits** (8,000,000,000)
- Calculate for different values of k

**Tasks**:
1. For **k = 1**:
   - Calculate p ≈ 1 - e^(-1/8)
   - Evaluate numerically

2. For **k = 2**:
   - Calculate p ≈ (1 - e^(-2/8))^2
   - Evaluate numerically

3. For **k = 3, 4, 5, 6, 7, 8**:
   - Calculate p for each
   - Which k gives the minimum false positive rate?

4. Plot p vs k to visualize the behavior

**Space for solution**:
```
Your work here...
```

---

### C.2 OPTIMAL PARAMETER SELECTION

#### Question C.2.1: Optimal Value of k ⭐ CRITICAL FORMULA
**Source**: Slide 10, Lines 615-638
**Difficulty**: ⭐⭐⭐⭐⭐ Expert

**Problem**: Determine the value of **k** that minimizes the false positive probability p.

**Given**: p ≈ (1 - e^(-kn/m))^k

**Method**: Minimize log(p) which is more tractable.

**Tasks**:
1. Write: log(p) = k × log(1 - e^(-kn/m))
2. Take derivative with respect to k and set to 0
3. Show that the optimal k is:
   - k_opt ≈ (m/n) × ln(2)
   - k_opt ≈ 0.693 × (m/n)

4. For the example in C.1.4 (m/n = 8):
   - Calculate k_opt
   - Round to nearest integer
   - Calculate the minimum false positive rate

**Space for solution**:
```
Your work here...
```

---

#### Question C.2.2: Designing a Bloom Filter
**Source**: Slide 10, Lines 473-495
**Difficulty**: ⭐⭐⭐⭐ Very Hard

**Problem**: You need to design a Bloom filter for a spell-checker application.

**Requirements**:
- Dictionary has n = 500,000 words
- Acceptable false positive rate: p ≤ 0.01 (1%)

**Tasks**:
1. Determine the required number of bits m
   - Use: m ≈ -n × ln(p) / (ln(2))^2
2. Calculate k_opt = 0.693 × (m/n)
3. Round k to nearest integer
4. Verify that the false positive rate is below 1%
5. How much memory is needed (in MB)?

**Space for solution**:
```
Your work here...
```

---

### C.3 COUNTING BLOOM FILTERS

#### Question C.3.1: Understanding Counting Bloom Filters
**Source**: Slide 10, Lines 736-788
**Difficulty**: ⭐⭐⭐ Hard

**Problem**: Counting Bloom Filter with **w-bit counters** instead of single bits.

**Tasks**:
1. Why do we need counters instead of bits?
2. How does insertion work?
3. How does deletion work?
4. Why can deletions introduce **false negatives**? Explain with an example.
5. How do you retrieve the count of an element?

**Typical value**: w = 4 bits per counter

**Space for solution**:
```
Your work here...
```

---

#### Question C.3.2: Counter Overflow Analysis
**Source**: Slide 10, Lines 806-823
**Difficulty**: ⭐⭐⭐ Hard

**Problem**: Counting Bloom Filter with w-bit counters.

**Issues**:
1. What happens when a counter reaches 2^w - 1?
2. For w = 4, what is the maximum counter value?
3. Why does overflow lead to undercounts?
4. Trade-off analysis:
   - Large w → ?
   - Small w → ?

**Space for solution**:
```
Your work here...
```

---

# PART II: ALGORITHM ANALYSIS & IMPLEMENTATION

---

## Section D: Data Stream Algorithms

---

### D.1 FINDING FREQUENT ITEMS (Slide 11)

#### Question D.1.1: MAJORITY Problem - Understanding
**Source**: Slide 11, Lines 243-257
**Difficulty**: ⭐⭐ Medium

**Problem**: The MAJORITY problem seeks an element that appears **more than m/2 times** in a sequence of m elements.

**Tasks**:
1. Given sequence: [A, B, A, A, B, A, A]
   - Is there a majority element?
   - Which one and what is its frequency?

2. Given sequence: [A, B, C, A, B, C]
   - Is there a majority element?

3. Why is sorting not useful for data streams?

**Space for solution**:
```
Your work here...
```

---

#### Question D.1.2: Boyer-Moore MJRTY Algorithm - Trace
**Source**: Slide 11, Lines 300-349
**Difficulty**: ⭐⭐⭐ Hard

**Problem**: Trace the Boyer-Moore majority vote algorithm.

**Algorithm**:
```
candidate = null; counter = 0;
while (not end of sequence)
    x = current_token();
    if (counter == 0)
        candidate = x; counter = 1;
    else if (candidate == x)
        counter++;
    else
        counter--;
```

**Task**: Execute this algorithm on the following sequences:

1. Sequence: [A, B, A, A, B, A, A]
   - Show candidate and counter at each step
   - Final candidate?
   - Is second pass needed?

2. Sequence: [A, B, C, A, B, A]
   - Show candidate and counter at each step
   - Final candidate?
   - Would second pass confirm majority?

**Space for solution**:
```
Your work here...
```

---

#### Question D.1.3: FREQUENT Problem - Misra & Gries Algorithm
**Source**: Slide 11, Lines 413-501
**Difficulty**: ⭐⭐⭐⭐ Very Hard

**Problem**: Find all items occurring more than **m/k** times. Algorithm keeps **(k-1) counters**.

**Algorithm outline**:
```
A = empty associative array;
while (not end of sequence)
    j = current_token();
    if (j in keys(A))
        A[j] = A[j] + 1;
    else
        if (|keys(A)| < (k-1))
            A[j] = 1;
        else
            for each i in keys(A)
                A[i] = A[i] - 1;
                if (A[i] == 0) remove i from A;
```

**Task**: Execute with k = 3 on sequence: [A, B, C, A, D, A, B, A]

**Space for solution**:
```
Your work here...
```

---

### D.2 DISTINCT ELEMENTS PROBLEM (Slide 13)

#### Question D.2.1: Understanding Flajolet-Martin Algorithm
**Source**: Slide 13, Lines 368-437
**Difficulty**: ⭐⭐⭐⭐ Very Hard

**Problem**: Estimate the number of distinct elements using hash tail lengths.

**Concept**:
- Hash each element to binary string
- Count trailing zeros (tail length)
- Track maximum tail length R
- Estimate: # distinct ≈ 2^R

**Why it works**:
- About 1/2^r elements have tail length r
- If max tail R = 3, probably saw about 2^3 = 8 distinct elements

**Tasks**:
1. Why is the probability of r trailing zeros approximately 1/2^r?
2. If stream has 100 distinct elements, what is the expected maximum tail length?
3. What are the limitations of using a single hash function?

**Space for solution**:
```
Your work here...
```

---

#### Question D.2.2: Flajolet-Martin Example ⭐ KEY EXERCISE
**Source**: Slide 13, Lines 566-585
**Difficulty**: ⭐⭐⭐⭐ Very Hard

**Problem**: σ = [3, 1, 4, 1, 5, 9, 2, 6, 5]

**Hash functions** (represent results as 5-bit binary):
- h₁(x) = (2x + 1) mod 32
- h₂(x) = (3x + 7) mod 32
- h₃(x) = 4x mod 32

**Tasks**:
1. For each element in σ, compute h₁, h₂, h₃
2. Convert each result to 5-bit binary
3. Count trailing zeros for each
4. Determine tail length for each stream element
5. For each hash function, track maximum tail length R
6. Estimate number of distinct elements using each hash function
7. Combine the three estimates (average? median?)
8. Compare with actual count of distinct elements

**Space for solution**:
```
Your work here...
```

---

#### Question D.2.3: Hash Function Quality Analysis
**Source**: Slide 13, Lines 586-597
**Difficulty**: ⭐⭐⭐ Hard

**Problem**: Analyze the hash functions from D.2.2.

**Questions**:
1. Do you see any problems with these hash functions?
2. For h₃(x) = 4x mod 32, what pattern do you notice in the binary representations?
3. For hash functions of the form h(x) = ax + b mod 2^k:
   - When is the result always even?
   - What advice would you give?
4. Why should we avoid even values of a?

**Space for solution**:
```
Your work here...
```

---

#### Question D.2.4: HyperLogLog Understanding
**Source**: Slide 13, Lines 615-676
**Difficulty**: ⭐⭐⭐⭐⭐ Expert

**Problem**: HyperLogLog (2007) - Near-optimal cardinality estimation.

**Key improvements over Flajolet-Martin**:
- Uses stochastic averaging
- Partitions hash space into m buckets
- Maintains maximum tail length per bucket
- Combines estimates using harmonic mean

**Tasks**:
1. Why is harmonic mean better than arithmetic mean for this application?
2. With m = 256 buckets and 6-bit tail counters:
   - How much memory is needed?
   - What cardinalities can be estimated?
3. What is the typical error rate?

**Space for solution**:
```
Your work here...
```

---

## Section E: Randomized Algorithms (Slide 08)

---

### E.1 PRIMALITY TESTING

#### Question E.1.1: Fermat's Primality Test - Understanding
**Source**: Slide 08, Lines 444-517
**Difficulty**: ⭐⭐⭐ Hard

**Problem**: Fermat's Little Theorem states:
If **p is prime** and **1 < a < p**, then **a^(p-1) ≡ 1 (mod p)**

**Fermat's Test**:
```
boolean fermat_test(P)  // P > 3
    a = rand_int(2, P-2);
    if (power(a, P-1) % P != 1)
        return false;  // Composite!
    return true;  // Probably prime
```

**Tasks**:
1. Test p = 15 with a = 2
   - Calculate 2^14 mod 15
   - Is 15 prime or composite?
   - Is 2 a Fermat-witness or Fermat-liar for 15?

2. Test p = 341 with a = 3
   - Calculate 3^340 mod 341
   - Is 341 prime or composite? (Note: 341 = 11 × 31)
   - Is 3 a Fermat-witness or Fermat-liar for 341?

3. Test p = 341 with a = 2
   - Calculate 2^340 mod 341
   - Is 2 a Fermat-witness or Fermat-liar for 341?

**Space for solution**:
```
Your work here...
```

---

#### Question E.1.2: Error Probability Analysis
**Source**: Slide 08, Lines 519-560
**Difficulty**: ⭐⭐⭐ Hard

**Problem**: Iterated Fermat's test with k repetitions.

**Theorem**: If p is composite, at most **half** of the integers a (where 1 < a < p) satisfy the Fermat equation.

**Tasks**:
1. For 1 test: Error probability ≤ ?
2. For 2 independent tests: Error probability ≤ ?
3. For k independent tests: Error probability ≤ ?
4. For k = 10: Calculate error probability
5. For k = 20: Calculate error probability
6. Is k = 10 sufficient for "negligible" error?

**Space for solution**:
```
Your work here...
```

---

#### Question E.1.3: Carmichael Numbers
**Source**: Slide 08, Lines 570-597
**Difficulty**: ⭐⭐⭐⭐ Very Hard

**Problem**: Carmichael numbers are composite numbers that satisfy:
**b^(n-1) ≡ 1 (mod n)** for all b relatively prime to n.

**Examples**: 561, 1105, 1729, 2465, 2821, 6601

**Tasks**:
1. For n = 561, test with several values of b:
   - b = 2, 3, 4, 5, 7
   - Calculate b^560 mod 561 for each
2. Why does Fermat's test always fail for Carmichael numbers?
3. What alternative primality tests handle Carmichael numbers?
   - Miller-Rabin (1980)
   - Baillie-PSW (1980)

**Space for solution**:
```
Your work here...
```

---

## Section F: Algorithm Design Strategies (Slides 01-05)

---

### F.1 COMPLEXITY ANALYSIS

#### Question F.1.1: Big-O Comparisons
**Difficulty**: ⭐⭐ Medium

**Problem**: Order these complexities from best to worst for n = 1,000,000:

1. O(n)
2. O(n log n)
3. O(n²)
4. O(2^n)
5. O(log n)
6. O(n!)
7. O(1)
8. O(n³)
9. O(√n)
10. O(n log² n)

**Tasks**:
1. Order them
2. Calculate approximate number of operations for n = 1,000,000
3. Which are polynomial? Which are exponential?

**Space for solution**:
```
Your work here...
```

---

#### Question F.1.2: Recurrence Relations
**Difficulty**: ⭐⭐⭐ Hard

**Problem**: Solve these recurrence relations:

1. T(n) = 2T(n/2) + n
   - Master Theorem case?
   - Solution?

2. T(n) = T(n-1) + n
   - Pattern?
   - Solution?

3. T(n) = T(n/2) + 1
   - Master Theorem case?
   - Solution?

**Space for solution**:
```
Your work here...
```

---

### F.2 DIVIDE & CONQUER

#### Question F.2.1: Binary Search Analysis
**Difficulty**: ⭐⭐ Medium

**Problem**: Binary search in a sorted array of n elements.

**Tasks**:
1. Write the recurrence relation
2. Solve for time complexity
3. Why is it better than linear search?
4. Worst-case comparisons for n = 1,024?

**Space for solution**:
```
Your work here...
```

---

#### Question F.2.2: Merge Sort Analysis
**Difficulty**: ⭐⭐⭐ Hard

**Problem**: Merge sort recursively divides, sorts, and merges.

**Tasks**:
1. Recurrence: T(n) = 2T(n/2) + O(n)
2. Apply Master Theorem
3. Time complexity?
4. Space complexity?
5. Compare with Quick Sort

**Space for solution**:
```
Your work here...
```

---

### F.3 DYNAMIC PROGRAMMING

#### Question F.3.1: Fibonacci - Naive vs DP
**Difficulty**: ⭐⭐ Medium

**Problem**: Calculate Fibonacci numbers.

**Naive recursive**:
```
fib(n):
    if n ≤ 1: return n
    return fib(n-1) + fib(n-2)
```

**Tasks**:
1. Time complexity of naive version?
2. Why is it inefficient?
3. How does memoization help?
4. Time complexity with DP?

**Space for solution**:
```
Your work here...
```

---

#### Question F.3.2: Longest Common Subsequence
**Difficulty**: ⭐⭐⭐ Hard

**Problem**: Find LCS of two strings.

**Strings**: X = "ABCDGH", Y = "AEDFHR"

**Tasks**:
1. Define subproblem structure
2. Write recurrence relation
3. Build DP table
4. Find LCS length
5. Reconstruct the LCS

**Space for solution**:
```
Your work here...
```

---

### F.4 GREEDY ALGORITHMS

#### Question F.4.1: Activity Selection
**Difficulty**: ⭐⭐ Medium

**Problem**: Select maximum number of non-overlapping activities.

**Activities**: [(start, finish)]
- A1: (1, 4)
- A2: (3, 5)
- A3: (0, 6)
- A4: (5, 7)
- A5: (3, 9)
- A6: (5, 9)
- A7: (6, 10)
- A8: (8, 11)

**Tasks**:
1. Apply greedy selection (earliest finish time)
2. Which activities are selected?
3. Is this optimal?
4. Prove greedy choice property

**Space for solution**:
```
Your work here...
```

---

#### Question F.4.2: Huffman Coding
**Difficulty**: ⭐⭐⭐⭐ Very Hard

**Problem**: Create optimal prefix-free code.

**Character frequencies**:
- A: 45
- B: 13
- C: 12
- D: 16
- E: 9
- F: 5

**Tasks**:
1. Build Huffman tree (show steps)
2. Assign codes to each character
3. Calculate average code length
4. Compare with fixed-length encoding

**Space for solution**:
```
Your work here...
```

---

## ADDITIONAL STUDY RESOURCES

### Recommended Practice Order

1. **Start with Basic Probability** (Section A)
   - Build foundation with coin and die problems
   - Master binomial distribution

2. **Move to Famous Problems** (Section A.6)
   - Birthday Paradox
   - Coupon Collector
   - These connect to advanced topics

3. **Tackle Probabilistic Counters** (Section B)
   - Fixed probability counters
   - Morris counter analysis
   - Build intuition for probabilistic algorithms

4. **Master Bloom Filters** (Section C)
   - Probability calculations are crucial
   - Understand parameter optimization
   - Practice numerical examples

5. **Study Data Stream Algorithms** (Section D)
   - Apply probability knowledge
   - Understand approximation algorithms

### Key Formulas to Memorize

#### Probability
- Binomial: P(X=k) = C(n,k) × p^k × (1-p)^(n-k)
- Expected value: E[X] = Σ x_i × P(X=x_i)
- Variance: Var(X) = E[X²] - (E[X])²

#### Probabilistic Counters
- Fixed probability p: E[S] = n × p, Var(S) = n × p × (1-p)
- Morris counter: E[S] ≈ floor(log₂(n+1))
- Estimate from counter: n ≈ 2^k - 1 (binary base)

#### Bloom Filters
- After n insertions: P(bit=0) = (1 - 1/m)^(kn)
- False positive: p ≈ (1 - e^(-kn/m))^k
- Optimal k: k_opt ≈ 0.693 × (m/n)

### Exam Preparation Tips

1. **Practice calculations** without a calculator
2. **Understand derivations**, don't just memorize
3. **Draw diagrams** for probability problems
4. **Trace algorithms** on small examples
5. **Know when approximations are valid**

---

**END OF STUDY GUIDE**

*This guide contains all questions and exercises directly extracted from course slides 01-13, with priority focus on probability calculations as requested.*
