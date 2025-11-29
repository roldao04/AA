# Two-Day Master's Level Implementation Plan with Overnight Benchmarking

## Day 1: Algorithm Development + Formal Analysis (8-10 hours)

### Core Tasks (Must Complete)

**Morning (4 hours): Infrastructure + First Algorithms**

1. **Project setup** (30 min)
   - Create directory structure: `src/`, `experiments/`, `analysis/`, `data/`, `results/`, `overnight/`
   - Set up `requirements.txt`: networkx, numpy, pandas, matplotlib, seaborn, scipy
   - Download SNAP datasets: ego-Facebook, email-Eu-core, wiki-Vote, ca-GrQc, ca-HepTh
   - Create graph loading utilities with validation

2. **Exact baseline implementation** (45 min)
   - Implement matching-based exact algorithm using `nx.max_weight_matching()`
   - Add timing and operation counting with timeout protection
   - Write unit tests on small graphs (Karate, Dolphins)

3. **Israeli-Itai randomized matching** (1.5 hours)
   - Implement propose-accept mechanism with clear comments
   - **While coding, write formal analysis in parallel**: Create `theory.md` deriving expected O(log n) rounds
   - Add greedy extension for unmatched vertices
   - Test convergence behavior on small graphs

4. **Simulated Annealing** (1.25 hours)
   - Implement with three neighborhood operators: remove redundant, swap edge, add-then-remove
   - Include parameter logging (temperature, acceptance rate, iteration)
   - Write formal complexity analysis: worst-case polynomial, expected behavior

**Afternoon (4 hours): Statistical Framework + Additional Algorithms**

5. **Statistical experimental framework** (1 hour)
   - Create `ExperimentRunner` class with:
     - Multi-trial execution (configurable repetitions)
     - Mean, std, 95% confidence intervals
     - Wilcoxon signed-rank test utilities
     - Progress tracking and checkpointing for long runs
   - Set up structured logging to CSV/JSON with metadata

6. **Lazy Greedy 3/2-approximation** (1.5 hours)
   - Implement priority queue-based version
   - **Write approximation proof** in theory document (dual feasibility argument)
   - Add randomized tie-breaking variant for comparison

7. **Initial validation experiments** (1 hour)
   - Run all algorithms on small instances (n=30-100) with 20 repetitions
   - Verify correctness, optimality, approximation bounds
   - Generate initial convergence plots for SA
   - Debug any issues before overnight run

8. **Overnight experiment setup** (30 min)
   - Configure batch experiment script (see Overnight section below)
   - Set up error handling and intermediate result saving
   - Test script on 2-3 instances to verify it runs correctly
   - Schedule to start before sleep

### Stretch Tasks (Grade Boosters)

**Option A: Hybrid Algorithm** (2 hours)
- Implement 3 post-matching extension variants: random, min-degree, local-search
- Add to overnight benchmark suite
- **Contribution**: "Strategic Randomization in Edge Cover Extension"

**Option B: Graph Property Infrastructure** (2 hours)
- Compute graph metrics: density, clustering, degree distribution
- Generate synthetic graphs with controlled properties
- Add property-controlled instances to overnight run
- **Contribution**: "Structural Predictors of Randomized Performance"

**Option C: Enhanced Theoretical Analysis** (1.5 hours)
- Prove concentration bounds for Israeli-Itai using Chernoff
- Analyze worst-case graphs for each algorithm
- Add adversarial graph generation to overnight suite
- **Contribution**: Rigorous probabilistic analysis with formal proofs

---

## Overnight Benchmark Run (8-12 hours unattended)

### Automated Experiment Configuration

**Large-Scale Statistical Validation** (Priority 1)
```python
# Configuration for overnight_experiments.py
INSTANCES = [
    # Small-medium (validation)
    "karate", "dolphins", "football", "polbooks",
    # SNAP graphs
    "ego-Facebook", "email-Eu-core", "wiki-Vote", 
    "ca-GrQc", "ca-HepTh",
    # Synthetic controlled
    *generate_erdos_renyi(n=[100,200,500,1000], p=[0.1,0.25,0.5]),
    *generate_barabasi_albert(n=[100,200,500,1000], m=[2,5,10]),
]

ALGORITHMS = ["exact", "israeli_itai", "simulated_annealing", "lazy_greedy"]
REPETITIONS = 50  # High count for tight confidence intervals
TIMEOUT = 300  # 5 min per algorithm-instance pair
```

**Parameter Sweep for Simulated Annealing** (Priority 2)
- Test 5 cooling schedules: exponential (α=[0.85,0.90,0.95,0.99]), linear
- Test 3 initial temperatures: T₀=[100, 500, 1000]
- Test 3 neighborhood structures
- Result: 45 configurations × 10 instances × 10 reps = 4,500 runs

**Graph Property Correlation Study** (Priority 3)
- Generate 50 graphs with systematic density variation (10%-90% in 10% steps)
- Generate 50 graphs with fixed density, varying clustering (watts_strogatz with k=[4,6,8,10])
- Measure: density, avg_clustering, degree_variance, diameter
- **Enables**: Correlation analysis between properties and algorithm performance

**Ablation Study for Unique Contribution** (Priority 4)
- If hybrid: Test all extension strategy combinations with 30 reps each
- If property-based: Generate additional controlled instances
- Save detailed traces for qualitative analysis

### Implementation Script Structure
```python
# overnight_experiments.py
import time, json, pickle
from datetime import datetime

def run_overnight_suite():
    results = []
    checkpoint_file = f"overnight/checkpoint_{datetime.now()}.pkl"
    
    for instance in INSTANCES:
        for algo in ALGORITHMS:
            for rep in range(REPETITIONS):
                try:
                    result = run_single_experiment(instance, algo, timeout=TIMEOUT)
                    results.append(result)
                    
                    # Checkpoint every 50 runs
                    if len(results) % 50 == 0:
                        save_checkpoint(results, checkpoint_file)
                except TimeoutError:
                    log_timeout(instance, algo, rep)
                except Exception as e:
                    log_error(instance, algo, rep, e)
    
    save_final_results(results, "overnight/final_results.json")
    generate_summary_statistics(results, "overnight/summary.csv")
```

### Expected Outcomes
- **50 repetitions** → confidence intervals with ±2-3% margin of error
- **5,000+ total runs** → robust statistical power for hypothesis testing
- **Parameter sweep results** → optimal SA configuration identified empirically
- **Property correlations** → quantitative predictors of algorithm suitability

---

## Day 2: Analysis + Visualization + Report (8-10 hours)

### Core Tasks (Must Complete)

**Morning (4 hours): Process Overnight Results + Unique Contribution**

1. **Load and validate overnight results** (30 min)
   - Verify completion rates, check for errors
   - Compute summary statistics per algorithm-instance pair
   - Identify any anomalies or failed runs

2. **Statistical analysis** (1.5 hours)
   - Compute confidence intervals for all randomized algorithms
   - Run pairwise Wilcoxon tests (Bonferroni correction for multiple comparisons)
   - Perform ANOVA to test if graph properties significantly affect performance
   - Create statistical summary tables with p-values

3. **Parameter optimization analysis** (45 min)
   - Identify best SA parameters from sweep results
   - Plot parameter sensitivity heatmaps
   - Re-run best configuration if needed

4. **Unique contribution deep-dive** (1.25 hours)
   - Detailed analysis of hybrid/property/theoretical contribution
   - Generate contribution-specific visualizations
   - Compute effect sizes and practical significance
   - Draft contribution subsection for paper

**Afternoon (5-6 hours): Visualization + Report Writing**

5. **Comprehensive visualization suite** (1.5 hours)
   - **Quality vs Runtime**: Scatter with 95% CI error bars, Pareto frontier
   - **Convergence Analysis**: SA mean ± std bands over iterations
   - **Distribution Plots**: Violin plots of solution quality across 50 trials
   - **Scalability**: Log-log plot with fitted complexity curves and R² values
   - **Statistical Comparison**: Box plots with significance brackets
   - **Parameter Sensitivity**: Heatmaps for SA parameter sweep
   - **Contribution-Specific**: Custom plots for unique angle
   - Use consistent color scheme, publication-quality formatting (300 DPI)

6. **Report writing** (3.5-4 hours - 8 pages IEEE/ACM format)

   **Section 1: Introduction** (1 page, 40 min)
   - Problem definition with real-world motivation
   - **Clear contribution statement** upfront
   - Related work (brief, 2-3 key papers)
   - Paper organization

   **Section 2: Theoretical Analysis** (2 pages, 1.5 hours)
   - **2.1 Exact Algorithm**: Gallai's theorem, O(n²√n) via Blossom
   - **2.2 Israeli-Itai Probabilistic Analysis**: 
     - Prove expected O(log n) rounds with derivation
     - Include Lemma on matching probability per round
     - Concentration bound (if stretch Option C completed)
   - **2.3 Approximation Guarantees**:
     - Lazy Greedy 3/2-approximation proof
     - SA expected complexity analysis
   - Use proper theorem/lemma/proof formatting

   **Section 3: Methodology** (1.5 pages, 45 min)
   - **3.1 Algorithm Implementations**: Brief pseudocode, optimizations
   - **3.2 Experimental Design**: 
     - Dataset descriptions with property tables
     - Statistical methodology: 50 trials, CI computation, Wilcoxon tests
     - Hardware specs
     - Overnight benchmark configuration details
   - **3.3 Evaluation Metrics**: Quality ratio, runtime, statistical significance

   **Section 4: Results** (2.5 pages, 1.5 hours)
   - **4.1 Performance Comparison**:
     - Statistical summary table (mean ± CI, p-values)
     - Quality-runtime tradeoff analysis
     - Scalability results with fitted curves
   - **4.2 [Your Unique Contribution]**:
     - Detailed results with interpretation
     - Statistical validation
     - Practical implications
   - **4.3 Parameter Sensitivity**: SA optimization results
   - **4.4 Graph Property Impact**: Correlation analysis (if completed)
   - Include 4-6 key figures referenced in text

   **Section 5: Discussion** (0.75 pages, 30 min)
   - Theoretical vs empirical reconciliation
   - When to use each algorithm (decision guide)
   - Limitations of study
   - Brief comparison with Project 1 insights

   **Section 6: Conclusion** (0.25 pages, 15 min)
   - Summary of findings
   - Contribution significance
   - Future work directions

7. **Polish and proofread** (30 min)
   - Check all references, citations
   - Verify figure numbers match text
   - Spell check, grammar review
   - Ensure all math notation consistent

### Stretch Tasks (Grade Boosters)

**Option D: Comparison with Published Baselines** (1 hour)
- Extract Ferdous et al. 2018 experimental parameters
- Compare your overnight results on equivalent graph sizes
- Add comparison table to results section
- **Impact**: Validates implementation quality

**Option E: Advanced Statistical Analysis** (1.5 hours)
- Multiple regression: predict algorithm performance from graph properties
- Cluster analysis: identify graph classes with similar algorithm behavior
- Add regression results table and cluster visualization
- **Impact**: Demonstrates statistical sophistication

**Option F: Supplementary Materials** (1 hour)
- Create supplementary PDF with:
  - Complete parameter sweep results
  - All 50-trial distributions
  - Extended theoretical proofs
  - Full experimental raw data tables
- **Impact**: Shows thoroughness, aids reproducibility

**Option G: Interactive Visualizations** (1.5 hours)
- Plotly interactive plots for parameter exploration
- Animation of SA convergence on example graphs
- Host on GitHub Pages
- **Impact**: Modern presentation, professional portfolio piece

---

## Execution Strategy

### Critical Path
1. **End Day 1 (8pm)**: Overnight script running error-free, validated on test instances
2. **Start Day 2 (8am)**: 5,000+ completed experiments, results loaded successfully
3. **12pm Day 2**: Statistical analysis complete, contribution finalized
4. **4pm Day 2**: All visualizations generated, report 80% drafted
5. **6pm Day 2**: Report complete, polished, ready for submission

### Contingency Plans
- **If overnight fails**: Use Day 1 validation data (20 reps), acknowledge as limitation
- **If time tight**: Cut Section 4.4, focus on core contribution results
- **If graphs too large**: Reduce to 30 repetitions, increase timeout

### Grade Impact Priority
1. **Rigorous theoretical analysis** (highest) - distinguishes master's work
2. **50+ repetitions with statistical tests** (very high) - shows methodological rigor
3. **Unique contribution** (very high) - demonstrates research capability
4. **Overnight benchmark scope** (high) - shows ambition and planning
5. **Publication-quality figures** (medium) - professionalism

### Quality Gates
- **Day 1 checkpoint**: Can you prove Israeli-Itai's O(log n) on paper?
- **Overnight success**: Did at least 90% of runs complete successfully?
- **Day 2 midpoint**: Do pairwise tests show p<0.05 for key comparisons?
- **Pre-submission**: Does contribution answer a question not explicitly addressed in literature?

This plan leverages overnight computing to achieve statistical rigor impossible within working hours alone, while maintaining focused implementation and analysis during active work sessions.