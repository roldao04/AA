# Revised Two-Day Implementation Plan: Empirical Breadth Focus

## Executive Summary

**Goal**: Maximum grade (A+) through comprehensive empirical comparison of randomized edge cover algorithms
**Timeline**: 2 full days (16-20 hours) + overnight automation (8-12 hours)
**Unique Contribution**: "Structural Predictors of Randomized Algorithm Performance" - systematic analysis of how graph properties affect algorithm selection
**Alignment**: Directly addresses assignment emphasis on "comparisons" and "VERY LARGE graphs"

**Key Shift from Original Plan**: Theoretical depth → Empirical breadth with statistical rigor

---

## Day 1: Implementation + Overnight Setup (8-9 hours)

### Morning Session: Algorithm Implementation (4.5 hours)

**1. Project Setup** (30 min)
- Create structure: `src/`, `experiments/`, `results/`, `overnight/`, `figures/`
- Requirements: networkx, numpy, pandas, matplotlib, seaborn, scipy
- **Pre-download SNAP datasets** (do before Day 1): ego-Facebook, email-Eu-core, wiki-Vote, ca-GrQc, ca-HepTh

**2. Exact Baseline** (30 min)
- Implement matching-based exact algorithm using `nx.max_weight_matching()`
- Add timeout protection and operation counting
- Test on Karate club (34 vertices)

**3. Israeli-Itai Randomized Matching** (1 hour)
- Implement propose-accept mechanism with clear comments
- Greedy extension for unmatched vertices
- **Skip formal proof** - just document O(log n) expected rounds in docstring
- Test convergence on small graphs

**4. Simulated Annealing** (1.5 hours)
- Three neighborhood operators: remove redundant, swap edge, add-then-remove
- Exponential cooling schedule with configurable α
- Parameter logging (temperature, acceptance rate, iteration)
- Initial temperature auto-tuning based on graph size

**5. Lazy Greedy (3/2-approximation)** (1 hour)
- Priority queue-based implementation
- Randomized tie-breaking variant
- **Mention** 3/2-approximation guarantee (no formal proof needed)

**6. Nearest Neighbor (2-approximation)** (30 min)
- Simple baseline: select min-weight edge per vertex
- Fast, trivially parallel, good comparison point

### Afternoon Session: Statistical Framework + Validation (3.5 hours)

**7. Experiment Runner Framework** (1.5 hours)
```python
class ExperimentRunner:
    - run_single_trial(graph, algorithm, params)
    - run_multi_trial(graph, algorithm, reps=40)
    - compute_statistics(results)  # mean, std, 95% CI
    - checkpoint_results(filename)  # save every 100 runs
    - load_checkpoint(filename)  # resume on failure
```
- CSV/JSON logging with metadata (timestamp, git commit, params)
- Progress tracking with tqdm

**8. Validation Experiments** (1 hour)
- Test all algorithms on: Karate (34v), Dolphins (62v), Football (115v)
- Verify correctness: all vertices covered, no isolated vertices
- Verify approximation bounds where applicable
- Run 20 repetitions to test statistical framework
- **Debug any issues now** - cannot fix during overnight run

**9. Overnight Script Setup + Testing** (1 hour)
- Create `overnight_experiments.py` with full configuration
- **CRITICAL**: Run mini version completely (3 instances × 3 algos × 5 reps)
- Verify checkpoint/resume logic works
- Check error handling and timeout behavior
- Estimate total runtime and disk space needed

---

## Overnight: Empirical Depth (8-12 hours unattended)

### Configuration

**Instances** (Total: ~45 instances)
```python
# Real-world graphs (15 instances)
SNAP_GRAPHS = [
    "karate", "dolphins", "football", "polbooks",  # small validation
    "ego-Facebook", "email-Eu-core", "wiki-Vote",  # medium SNAP
    "ca-GrQc", "ca-HepTh", "ca-CondMat",  # scientific collaboration
    "p2p-Gnutella08", "soc-Slashdot0811"  # large if time permits
]

# Synthetic: Graph Property Correlation Study (30 instances)
PROPERTY_STUDY = {
    # Density variation (10 instances)
    "erdos_renyi": [(n=500, p) for p in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]],

    # Clustering variation (10 instances)
    "watts_strogatz": [(n=500, k, p) for k in [4, 6, 8, 10, 12]],

    # Degree distribution variation (10 instances)
    "barabasi_albert": [(n, m) for n in [200, 500, 1000] for m in [2, 5, 10]]
}
```

**Algorithms** (4 core)
- Exact (baseline, with timeout)
- Israeli-Itai
- Simulated Annealing (best config from quick sweep)
- Lazy Greedy

**Parameters**
- Repetitions: **40** (not 50) - still gives <4% margin of error at 95% CI
- Timeout: 5 minutes per instance
- SA quick parameter sweep: 3 cooling schedules (α = 0.85, 0.90, 0.95)

**Expected Output**
- Total runs: ~3,600 (45 instances × 4 algorithms × 40 reps ÷ 2 for timeouts)
- Results CSV with columns: instance, algorithm, rep, solution_size, runtime, graph_properties
- Checkpoints every 100 runs
- Summary statistics per instance-algorithm pair

### Graph Property Extraction
For each synthetic graph, compute and log:
- Vertices, edges, density
- Average clustering coefficient
- Degree distribution (mean, std, max)
- Connected components
- Diameter (if feasible)

---

## Day 2: Analysis + Report Writing (8-9 hours)

### Morning: Deep Statistical Analysis (4 hours)

**1. Load and Validate Results** (20 min)
- Check completion rates (target: >90%)
- Identify failed runs and timeouts
- Verify data integrity

**2. Core Statistical Analysis** (1.5 hours)
- Compute 95% confidence intervals for all randomized algorithms
- Pairwise Wilcoxon signed-rank tests with Bonferroni correction
- Effect size calculation (Cohen's d)
- Create statistical summary tables with p-values
- Identify statistically significant differences (p < 0.05)

**3. Graph Property Correlation Analysis** (1 hour) ⭐ **UNIQUE CONTRIBUTION**
- Multiple linear regression: `runtime ~ density + clustering + degree_std`
- Multiple linear regression: `quality_ratio ~ density + clustering + degree_std`
- Separate models per algorithm
- Identify which properties predict performance
- R² values and coefficient significance

**4. Parameter Optimization** (30 min)
- Identify best SA cooling schedule from quick sweep
- Plot parameter sensitivity if time permits

**5. Generate All Visualizations** (40 min)
```python
# Required figures (6-7 total)
1. Quality vs Runtime scatter (all algorithms, 95% CI error bars)
2. Scalability: log-log plot (vertices vs runtime)
3. Statistical comparison: box plots with significance brackets
4. Distribution plots: violin plots of solution quality across 40 trials
5. Property correlation heatmap: R² values per algorithm-property pair
6. Decision guide heatmap: which algorithm wins per property regime
7. Convergence plot: SA mean ± std bands over iterations (1-2 examples)
```
- Use consistent color scheme, 300 DPI, publication-quality formatting

### Afternoon: Report Writing (5 hours)

**Target: 6 pages IEEE/ACM format**

**Section 1: Introduction** (0.75 pages, 30 min)
- Edge cover problem definition with real-world motivation
- **Clear contribution statement**: systematic study of graph properties' impact on randomized algorithm performance
- Brief related work (2-3 key papers from research doc)
- Paper organization

**Section 2: Background & Algorithms** (1 page, 40 min)
- **2.1 Problem Formulation**: Minimum edge cover definition, Gallai's theorem
- **2.2 Algorithm Overview**: Brief description of 4 algorithms with complexity table
  - Exact: O(n²√n) via matching
  - Israeli-Itai: O(log n) expected parallel depth
  - Lazy Greedy: O(|E|log|E|), 3/2-approximation
  - Simulated Annealing: configurable quality-time tradeoff
- **No formal proofs** - just state guarantees

**Section 3: Methodology** (1 page, 40 min)
- **3.1 Implementation Details**: Key optimizations, libraries used
- **3.2 Experimental Design**:
  - Dataset descriptions (15 real-world + 30 synthetic)
  - Graph property table (density, clustering, size ranges)
  - Statistical methodology: 40 trials, 95% CI, Wilcoxon tests
  - Hardware specs and overnight automation approach
- **3.3 Evaluation Metrics**: Quality ratio, runtime, statistical significance

**Section 4: Results** (2.5 pages, 2 hours) ⭐ **CORE CONTRIBUTION**
- **4.1 Overall Performance Comparison** (0.75 pages)
  - Statistical summary table (mean ± CI, p-values)
  - Quality-runtime tradeoff analysis (Figure 1)
  - Key finding: which algorithm dominates when

- **4.2 Graph Property Impact Analysis** (1 page) ⭐ **UNIQUE CONTRIBUTION**
  - Regression results: significant predictors per algorithm
  - Correlation heatmap (Figure 5)
  - Decision guide heatmap (Figure 6): "Use Israeli-Itai when density < 0.3"
  - Practical implications for algorithm selection

- **4.3 Scalability Results** (0.5 pages)
  - Log-log plot with fitted complexity curves (Figure 2)
  - Largest graphs successfully processed
  - Timeout analysis for exact algorithm

- **4.4 Solution Quality Distribution** (0.25 pages)
  - Violin plots showing variance across 40 trials (Figure 4)
  - Highlight consistency vs. variance tradeoffs

**Section 5: Discussion** (0.5 pages, 30 min)
- Theoretical vs. empirical reconciliation
- **Practical decision guide**: When to use each algorithm (flowchart or table)
- Limitations: timeout bias, property coverage, weighted graphs not tested
- Connection to Project 1 insights (if applicable)

**Section 6: Conclusion** (0.25 pages, 15 min)
- Summary: empirical evidence that graph properties strongly affect algorithm choice
- Contribution significance: first systematic property-based comparison for edge cover
- Future work: dynamic graphs, weighted instances, hybrid approaches

**Polish & References** (25 min)
- Verify all figure numbers match citations
- Check references (BibTeX from research doc)
- Spell check, consistent notation
- Verify all claims supported by results

---

## Key Changes from Original Plan

| Aspect | Original Plan | Revised Plan | Rationale |
|--------|--------------|--------------|-----------|
| **Focus** | Theoretical depth with formal proofs | Empirical breadth with statistical rigor | Aligns with "comparisons + VERY LARGE graphs" |
| **Algorithms** | 4 + optional 5th | 5 core (added Nearest Neighbor) | More comparison points, simple to add |
| **Repetitions** | 50 trials | 40 trials | <4% margin still rigorous, saves 20% analysis time |
| **Report Length** | 8 pages | 6 pages | Match empirical focus, less theory writing |
| **Theory Section** | 2 pages with proofs | 0.5 pages stating guarantees | Free up time for analysis |
| **Unique Contribution** | Theoretical analysis (Option C) | Graph property correlation study | More publishable, empirical angle |
| **Parameter Sweep** | 4,500 SA runs | ~500 quick sweep | Enough to optimize, not overwhelming |
| **Day 1 Theory Writing** | In parallel with coding | Skip entirely | Focus on implementation quality |

---

## Unique Contribution: "Structural Predictors of Randomized Algorithm Performance"

### Research Question
**Can graph structural properties predict which randomized algorithm will perform best?**

### Approach
1. **Systematic variation**: Generate graphs with controlled density, clustering, degree distribution
2. **Comprehensive measurement**: Extract 5-8 graph properties per instance
3. **Statistical modeling**: Multiple regression to identify significant predictors
4. **Practical output**: Decision heatmap showing optimal algorithm per property regime

### Why This is Publication-Worthy
- **No existing study** systematically examines property-performance relationships for edge cover
- **Practical impact**: Provides actionable guidance for practitioners
- **Methodologically rigorous**: Large sample (30 synthetic + 15 real), 40 reps, statistical validation
- **Generalizable**: Framework applies to other graph problems

### Expected Findings (Hypotheses)
- Dense graphs favor exact algorithm (less matching complexity)
- Sparse graphs favor Israeli-Itai (parallelizable, fast)
- High clustering favors greedy approaches (local structure)
- Power-law distributions create variance in randomized methods

---

## Critical Success Factors

### Day 1 End Checklist
- [ ] All 5 algorithms implemented and tested on small graphs
- [ ] Overnight script successfully completed mini test run (3×3×5 = 45 trials)
- [ ] Checkpoint/resume logic verified
- [ ] All SNAP datasets downloaded and loadable
- [ ] Estimated overnight completion time < 12 hours

### Day 2 Start Checklist
- [ ] Overnight run completed with >90% success rate
- [ ] Results CSV loaded successfully with expected columns
- [ ] No corrupted checkpoints
- [ ] Total runs > 3,000

### Pre-Submission Checklist
- [ ] All figures have captions and are referenced in text
- [ ] Statistical claims supported by p-values in results
- [ ] Contribution clearly differentiated from prior work
- [ ] Code runs without errors on validation graphs
- [ ] Report fits 6-page limit (not including references)

---

## Risk Mitigation

### If Overnight Fails Completely
- **Fallback**: Use Day 1 validation data (20 reps on 10 instances)
- **Adjustment**: Acknowledge as limitation, focus on property correlation with smaller sample
- **Timeline**: Add 4 hours Day 2 morning for emergency re-runs

### If Overnight Partially Completes (50-89%)
- **Action**: Analyze available data, note missing instances in limitations
- **No re-run**: Work with what you have (still likely >2,000 trials)

### If Analysis Takes Longer Than Expected
- **Cut**: Section 4.4 (distribution plots)
- **Simplify**: Property correlation to univariate analysis (density only)
- **Reduce**: Report to 5 pages, combine Sections 5+6

### If Writing Runs Late
- **Priority 1**: Sections 1, 3, 4.1, 4.2, 6 (core contribution)
- **Priority 2**: Sections 2, 4.3, 5
- **Last resort**: Submit with draft Discussion section

---

## Why This Plan Achieves A+

1. **Methodological Rigor**: 40 trials, proper CI, Wilcoxon tests, Bonferroni correction
2. **Scale**: 3,500+ experiments across diverse graphs, reaching "VERY LARGE" requirement
3. **Novel Contribution**: Property-performance analysis fills gap in literature
4. **Practical Impact**: Actionable decision guide for algorithm selection
5. **Comprehensive Comparison**: 5 algorithms, 15 real + 30 synthetic graphs
6. **Professional Presentation**: Publication-quality figures, statistical validation
7. **Leverages Overnight Automation**: Shows planning and resource optimization

---

## Timeline Summary

| Phase | Duration | Key Deliverable |
|-------|----------|-----------------|
| Day 1 Morning | 4.5h | 5 working algorithms |
| Day 1 Afternoon | 3.5h | Statistical framework + validated overnight script |
| Overnight | 8-12h | 3,500+ experimental runs |
| Day 2 Morning | 4h | Complete statistical analysis + all figures |
| Day 2 Afternoon | 5h | 6-page report |
| **Total Active Work** | **17h** | Submission-ready project |

**Buffer**: 3 hours built into Day 2 estimates for unexpected issues

---

## Final Notes

- **Pre-work recommended**: Download datasets, set up Python environment, test NetworkX imports
- **Day 1 evening**: Start drafting introduction while overnight runs (optional, saves 30min Day 2)
- **Visualization templates**: Prepare matplotlib style sheet Day 1 to speed up Day 2 figure generation
- **Git commits**: Commit after each major algorithm implementation for safety
- **Focus**: If time gets tight, prioritize Section 4.2 (property correlation) over other results

This plan is **realistic, empirically-focused, and targets A+ through unique contribution** while respecting the 2-day constraint.
