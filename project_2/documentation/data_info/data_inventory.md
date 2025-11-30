# Data Inventory: Complete Graph Dataset Analysis

**Date:** November 30, 2025
**Status:** Comprehensive inventory of all available graph datasets
**Purpose:** Guide graph selection for testing, benchmarking, and experiments

---

## Executive Summary

### Total Available Resources

| Category | Count | Size Range | Status |
|----------|-------|------------|--------|
| **SW Graphs** | 11 | 13v to 10,000v | 3 tested, 8 untested |
| **SNAP Main Graphs** | 5 | 1,005v to 12,008v | All untested |
| **Facebook Ego Networks** | 10 | 52v to 1,034v | All untested |
| **DIMACS Benchmarks** | 3 | 1,000v to 4,000v (DENSE!) | All untested |
| **NetworkX Built-ins** | 3 | 34v to 115v | 2 tested (karate, football) |
| **IMPRACTICAL (Too Large)** | 6+ | >65k to 1.8B edges | Do NOT use |
| **TOTAL USABLE** | **32 graphs** | 13v to 12,008v | **29 untested** |

### Key Insights

- **Excellent size diversity**: 13 vertices to 12,000 vertices
- **Density spectrum**: Sparse social networks (0.001) to ultra-dense random (0.9)
- **Domain diversity**: Social, collaboration, ego networks, random benchmarks
- **Unique opportunity**: DIMACS dense graphs provide stress testing (450k-1.8M edges!)
- **Critical warning**: 6+ graphs are IMPRACTICAL (Friendster: 31GB file, 1.8 billion edges!)

### Recommended Strategy

**For Testing (Quick Validation):**
- 5-8 graphs: SWtiny*, ego-698, ego-414, karate, florentine

**For Benchmarking (Diverse Sample):**
- 20-25 graphs spanning all size categories and densities

**For "Very Large" Proof:**
- **Primary**: SW10000EWD (10,000 vertices, 2.5MB)
- **Alternative**: CA-HepPh (12,008 vertices, 237k edges)

**AVOID Completely:**
- Friendster (31GB, impractical)
- YouTube, LiveJournal, Orkut (all compressed .gz > 1GB)
- SWlargeG (100MB, optional stretch only)

---

## 1. Sedgewick & Wayne (SW) Graphs

**Location:** `data/SW_ALGUNS_GRAFOS/`
**Format:** Custom SW format (4-line header + edge list)
**Total:** 11 graphs
**Status:** 3 tested, 8 ready to test

### Complete Inventory

| File | Vertices | Edges | Density | Size | Type | Status |
|------|----------|-------|---------|------|------|--------|
| **SWtinyG.txt** | 13 | 13 | 0.167 | 67 B | Undirected | ✅ TESTED |
| **SWtinyEWD.txt** | ~15 | ~20 | ~0.19 | 144 B | Weighted | 🔄 Ready |
| **SWtinyDG.txt** | ~15 | ~20 | ~0.19 | 142 B | Directed | 🔄 Ready |
| **SWtinyDAG.txt** | ~10 | ~12 | ~0.13 | 93 B | DAG | 🔄 Ready |
| **SWmediumG.txt** | 250 | 1,273 | 0.041 | 8.9 KB | Undirected | ✅ TESTED |
| **SWmediumEWD.txt** | ~250 | ~2,000 | ~0.06 | 40 KB | Weighted | 🔄 Ready |
| **SWmediumDG.txt** | ~250 | ~500 | ~0.02 | 894 B | Directed | 🔄 Ready |
| **SW1000EWD.txt** | 1,000 | 8,433 | 0.017 | 313 KB | Weighted | ✅ TESTED |
| **SW10000EWD.txt** | **10,000** | **~80,000** | **~0.002** | **2.5 MB** | **Weighted** | **⭐ CRITICAL** |
| **SWlargeG.txt** | **~100,000+** | **~1M+** | **~0.0002** | **100 MB** | **Undirected** | **⚠️ STRETCH** |

### Format Specification

```
Line 1: 0/1 (undirected/directed)
Line 2: 0/1 (unweighted/weighted)
Line 3: number_of_vertices
Line 4: number_of_edges
Lines 5+: vertex_from vertex_to [weight]
```

### Loader Implementation

**Status:** ✅ Implemented in `src/utils/graph_loader.py::load_sw_graph()`

**Features:**
- Automatic directed → undirected conversion
- Self-loop removal
- Isolated vertex cleanup
- Weight ignoring (not needed for edge cover)

### Testing Status

**Completed (3 graphs):**
- ✅ SWtinyG.txt: All algorithms tested, valid covers
- ✅ SWmediumG.txt: Lazy Greedy wins (1.064x optimal, 3ms)
- ✅ SW1000EWD.txt: Lazy Greedy dominates (1.034x optimal, 27ms)

**Priority Testing (8 graphs):**
1. **SW10000EWD.txt** (10,000v) - HIGHEST PRIORITY for "very large" requirement
2. SWtinyEWD, SWtinyDG, SWtinyDAG - Quick validation (< 5 min total)
3. SWmediumEWD, SWmediumDG - Additional medium-scale diversity
4. SWlargeG.txt - Optional stretch goal (may timeout/fail)

### Recommendations

**Use for benchmarking:**
- SWtinyG (validation baseline)
- SWmediumG (250v, moderate density)
- SW1000EWD (1k vertices, proven scalability)
- **SW10000EWD** (10k vertices, CRITICAL for "very large" claim)

**Skip:**
- SWlargeG unless attempting extreme scale demonstration (high risk of failure)

---

## 2. SNAP Datasets (Stanford Large Network Dataset Collection)

**Location:** `data/SNAP/`
**Format:** Edge list with comment headers
**Total:** 18+ graphs (5 main + 10 ego networks + 3 impractical)

### 2.1 Main Collaboration & Social Networks

| Graph | Vertices | Edges | Density | Size | Domain | Priority |
|-------|----------|-------|---------|------|--------|----------|
| **CA-GrQc** | 5,242 | 28,980 | 0.002 | 344 KB | Arxiv collab | ⭐ HIGH |
| **CA-HepPh** | 12,008 | 237,010 | 0.003 | 2.9 MB | Physics collab | ⭐ HIGH |
| **email-Eu-core** | 1,005 | 25,571 | 0.051 | 192 KB | Email network | ✅ MEDIUM |
| **Wiki-Vote** | 7,115 | 103,689 | 0.004 | 1.1 MB | Wikipedia voting | ⭐ HIGH |
| **facebook_combined** | 4,039 | 88,234 | 0.011 | 836 KB | Social network | ✅ MEDIUM |

**Format Example (CA-GrQc.txt):**
```
# Directed graph (each unordered pair of nodes is saved once): CA-GrQc.txt
# Collaboration network of Arxiv General Relativity category
# Nodes: 5242 Edges: 28980
# FromNodeId	ToNodeId
3466	937
3466	5233
...
```

**Loader Status:** 🔄 Needs implementation (simple edge list, skip # comments)

**Why These Matter:**
- **CA-HepPh**: Largest SNAP graph we can reasonably test (**12k vertices!**)
- **CA-GrQc**: Good 5k vertex benchmark
- **Wiki-Vote**: 7k vertices with directed→undirected conversion test
- **Sparse graphs**: Real-world social networks (density < 0.01)

### 2.2 Facebook Ego Networks

**Location:** `data/SNAP/facebook/facebook/*.edges`
**Format:** Simple edge list (space-separated, no headers)
**Total:** 10 ego networks
**Status:** All untested

| Ego ID | Nodes | Edges | Density | Use Case |
|--------|-------|-------|---------|----------|
| **ego-698** | 61 | 540 | 0.295 | Tiny benchmark |
| **ego-3980** | 52 | 292 | 0.220 | Tiny benchmark |
| **ego-414** | 150 | 3,386 | 0.303 | Small, dense |
| **ego-686** | 168 | 3,312 | 0.236 | Small, dense |
| **ego-348** | 224 | 6,384 | 0.255 | Small, dense |
| **ego-0** | 333 | 5,038 | 0.091 | Medium |
| **ego-3437** | 534 | 9,626 | 0.068 | Medium |
| **ego-1684** | 786 | 28,048 | 0.091 | Medium-large |
| **ego-1912** | 747 | 60,050 | 0.215 | Large, very dense! |
| **ego-107** | 1,034 | 53,498 | 0.100 | Large, 1k+ nodes |

**Format (*.edges files):**
```
236 186
438 169
541 378
...
```

**Loader Status:** 🔄 Needs implementation

**Why These Matter:**
- **Size diversity**: 52 to 1,034 vertices (perfect spectrum!)
- **Density range**: 0.07 to 0.30 (sparse to moderately dense)
- **Ego network structure**: Different from random/collaboration graphs
- **Quick to load**: Small file sizes, easy testing
- **ego-107**: Crosses 1,000-vertex threshold
- **ego-1912**: Stress test with 60k edges in 747 vertices!

**Recommended for Benchmarking:**
- ego-698 (tiny, 61v)
- ego-414 (small, 150v)
- ego-0 (medium, 333v)
- ego-3437 (medium, 534v)
- ego-1684 (medium-large, 786v)
- ego-107 (large, 1,034v)

### 2.3 IMPRACTICAL Graphs (DO NOT USE!)

| Graph | File Size | Estimated Nodes/Edges | Why Impractical |
|-------|-----------|----------------------|-----------------|
| **friendster ungraph** | **31 GB** | **~65M nodes, 1.8B edges** | File too large to load in memory |
| youtube ungraph | 1.3 GB (gzipped) | ~1.1M nodes, 3M edges | Too large for testing |
| livejournal ungraph | 1.7 GB (gzipped) | ~4M nodes, 34M edges | Too large |
| orkut ungraph | 2.3 GB (gzipped) | ~3M nodes, 117M edges | Too large |
| Community files | Large (gzipped) | N/A | Not graph structure |

**CRITICAL WARNING:**
- **Friendster** file alone is **31 GB uncompressed**
- Even if algorithms could handle it, loading would take hours
- Would require distributed computing or external memory algorithms
- **DO NOT ATTEMPT** unless specifically targeting extreme-scale research

**Alternative for Large-Scale Claims:**
- CA-HepPh (12k vertices) is largest practical SNAP graph
- SW10000EWD (10k vertices) from SW collection
- These are sufficient for "very large graph" claims

---

## 3. DIMACS Benchmark Graphs

**Location:** `data/DIMACS/`
**Format:** DIMACS CLIQUE format (custom header + 'e' edge lines)
**Total:** 3 graphs
**Status:** All untested

### Complete Inventory

| Graph | Vertices | Edges | Edge Prob | Density | Size | Challenge |
|-------|----------|-------|-----------|---------|------|-----------|
| **C1000.9** | 1,000 | **450,079** | p=0.9 | **0.900** | 4.3 MB | Ultra-dense! |
| **C2000.9** | 2,000 | **1,799,532** | p=0.9 | **0.900** | 19 MB | Extreme density! |
| **C4000.5** | 4,000 | **~4M** | p=0.5 | **0.500** | 5.1 MB | Large + moderate density |

### Format Specification (DIMACS CLIQUE)

```
c FILE:  C1000.9.clq
c SOURCE: Generated by Michael Trick using ggen
c DESCRIPTION: Random graph. Cx.y has x nodes and edge probability .y
c
c number of vertices : 1000
c number of edges     : 450079
c edge probability   : 0.900000
c
p edge 1000 450079
e 1 2
e 1 3
e 1 4
...
```

**Key Lines:**
- Lines starting with `c`: Comments
- Line starting with `p edge`: `p edge <num_vertices> <num_edges>`
- Lines starting with `e`: `e <vertex_u> <vertex_v>`

**Loader Status:** 🔄 Needs implementation

### Why These Are CRITICAL

**Unique Stress Tests:**
1. **Extreme Density**: p=0.9 means ~90% of possible edges exist!
2. **Algorithm Weaknesses**: Will expose performance issues on dense graphs
3. **Novel Contribution**: No existing edge cover studies test ultra-dense graphs
4. **Practical Relevance**: Real networks can be dense (social cliques, molecular graphs)

**Expected Algorithm Behavior:**

| Algorithm | C1000.9 (450k edges) | C2000.9 (1.8M edges) |
|-----------|---------------------|---------------------|
| **Exact** | May timeout (many edges) | Likely timeout |
| **Lazy Greedy** | Slow (priority queue overhead) | Very slow or timeout |
| **Nearest Neighbor** | Fast (linear scan) | Should complete |
| **Israeli-Itai** | May struggle (conflicts) | Likely poor quality |

**Research Value:**
- **C1000.9**: Comparable size to SW1000EWD but **53x more edges!**
- Shows how density affects algorithm performance independently of graph size
- Can prove: "Nearest Neighbor dominates on ultra-dense graphs"

### Computational Challenges

**C1000.9 (1,000 vertices, 450k edges):**
- Exact: O(n²√n) = O(31M) operations, but matching on dense graph is expensive
- Lazy Greedy: O(m log m) = O(8.5M) operations, but priority queue on 450k edges
- Estimated runtime: 10-60 seconds for approximations, 5-10 minutes for exact

**C2000.9 (2,000 vertices, 1.8M edges):**
- **WARNING**: May be too large for exact algorithm
- Approximations: 30-300 seconds estimated
- Exact: 10-30 minutes or timeout

**C4000.5 (4,000 vertices, ~4M edges):**
- **EXTREME STRESS TEST**
- Exact: Almost certainly timeout (>30 min)
- Approximations: 1-5 minutes if successful

### Recommendations

**Tiered Testing Approach:**

**Tier 1: C1000.9** (highest priority)
- Test all algorithms with extended timeouts
- Document performance degradation vs sparse 1k graphs
- Expected: Complete successfully

**Tier 2: C2000.9** (medium priority)
- Test approximations only (skip exact or use 30-min timeout)
- Compare to sparse 2k graphs (if we generate them)
- Expected: Some timeouts, but valuable data

**Tier 3: C4000.5** (stretch goal)
- Only if time permits
- Approximations only
- Expected: High failure rate, but impressive if successful

**Research Contribution:**
- First study to test edge cover algorithms on DIMACS dense benchmarks
- Clear demonstration of density's impact on algorithm performance
- Practical guidance: "Use Nearest Neighbor for dense graphs (p > 0.5)"

---

## 4. NetworkX Built-in Graphs

**Status:** 2 tested, more available
**Purpose:** Small validation graphs

| Graph | Vertices | Edges | Tested | Use Case |
|-------|----------|-------|--------|----------|
| **karate** | 34 | 78 | ✅ Yes | Validation baseline |
| **florentine** | 15 | 20 | ✅ Yes | Tiny validation |
| **davis** | 18 | 9 | 🔄 Ready | Tiny validation |
| **football** | 115 | 486 | ✅ Yes | Small benchmark |

**Loader Status:** ✅ Implemented

**Recommendation:** Include karate and florentine in all test suites for validation baseline.

---

## 5. Graph Selection Strategy for Experiments

### Categorization by Size

**Tiny (< 100 vertices):** Quick validation, baseline testing
- SWtinyG (13v) ✅
- ego-698 (61v)
- ego-3980 (52v)
- karate (34v) ✅
- florentine (15v)

**Small (100-500 vertices):** Algorithm comparison, quality testing
- ego-414 (150v)
- ego-686 (168v)
- ego-348 (224v)
- SWmediumG (250v) ✅
- ego-0 (333v)

**Medium (500-2,000 vertices):** Scalability testing
- ego-3437 (534v)
- ego-1684 (786v)
- ego-1912 (747v, but 60k edges!)
- C1000.9 (1,000v, 450k edges - DENSE!)
- SW1000EWD (1,000v) ✅
- ego-107 (1,034v)
- email-Eu-core (1,005v)

**Large (2,000-8,000 vertices):** Advanced scalability
- C2000.9 (2,000v, 1.8M edges - EXTREME!)
- C4000.5 (4,000v)
- facebook_combined (4,039v)
- CA-GrQc (5,242v)
- Wiki-Vote (7,115v)

**Very Large (> 8,000 vertices):** "Very Large Graph" proof
- **SW10000EWD** (10,000v) ⭐ PRIMARY TARGET
- **CA-HepPh** (12,008v) ⭐ BACKUP/ALTERNATIVE

### Categorization by Density

**Sparse (density < 0.01):**
- CA-GrQc, CA-HepPh, Wiki-Vote, SW10000EWD
- Characteristic: Real-world social/collaboration networks

**Moderate (0.01 ≤ density < 0.1):**
- SWmediumG, SW1000EWD, ego-0, ego-3437, ego-1684, ego-107
- Characteristic: Ego networks, medium social graphs

**Dense (0.1 ≤ density < 0.5):**
- ego-1912, facebook_combined, karate
- Characteristic: Tightly connected communities

**Ultra-Dense (density ≥ 0.5):**
- **C1000.9 (0.9), C2000.9 (0.9), C4000.5 (0.5)**
- **ego-414 (0.3), ego-348 (0.26), ego-698 (0.3)**
- Characteristic: Synthetic benchmarks, small ego networks

### Recommended Benchmark Suite (20-25 graphs)

**Tier 1: MUST TEST (15 graphs)**
1. SWtinyG (13v) - validation
2. karate (34v) - validation baseline
3. florentine (15v) - tiny validation
4. ego-698 (61v) - tiny ego
5. ego-414 (150v) - small dense
6. SWmediumG (250v) - medium baseline
7. ego-0 (333v) - medium ego
8. ego-3437 (534v) - medium ego
9. ego-1684 (786v) - medium-large
10. SW1000EWD (1,000v) - 1k baseline
11. **C1000.9 (1,000v, 450k edges)** - dense stress test ⭐
12. ego-107 (1,034v) - 1k+ ego
13. CA-GrQc (5,242v) - large sparse
14. **SW10000EWD (10,000v)** - very large proof ⭐
15. **CA-HepPh (12,008v)** - very large alternative ⭐

**Tier 2: RECOMMENDED (5-7 graphs)**
16. ego-3980 (52v) - additional tiny
17. ego-686 (168v) - additional small
18. email-Eu-core (1,005v) - 1k email network
19. facebook_combined (4,039v) - 4k social
20. Wiki-Vote (7,115v) - 7k voting network
21. SWmediumEWD (250v) - weighted variant
22. ego-1912 (747v, 60k edges) - dense stress

**Tier 3: STRETCH (2-4 graphs)**
23. **C2000.9 (2,000v, 1.8M edges)** - extreme density
24. C4000.5 (4,000v) - large + moderate density
25. SWlargeG (~100kv) - extreme scale (high risk)

**Total: 20-25 graphs** spanning:
- **Vertices**: 13 to 12,008
- **Edges**: 13 to 1,800,000+
- **Density**: 0.001 to 0.9
- **Domains**: Social, collaboration, ego, random

---

## 6. Loader Implementation Checklist

### Status Overview

| Format | Status | Priority | Implementation Needed |
|--------|--------|----------|----------------------|
| SW Format | ✅ Done | - | None |
| NetworkX Built-in | ✅ Done | - | None |
| SNAP Edge List | 🔄 Needed | HIGH | Skip # comments, space/tab separated |
| Facebook Ego | 🔄 Needed | HIGH | Simple edge list |
| DIMACS CLIQUE | 🔄 Needed | HIGH | Parse 'p edge' and 'e' lines |

### Implementation Tasks

**1. SNAP Edge List Loader** (`load_snap_graph()`)
```python
def load_snap_graph(filename: str, data_dir: str = 'data/SNAP') -> nx.Graph:
    # Skip lines starting with #
    # Parse space or tab separated edges
    # Convert to undirected
    # Remove self-loops and isolated vertices
```

**2. Facebook Ego Network Loader** (`load_facebook_ego()`)
```python
def load_facebook_ego(ego_id: str, data_dir: str = 'data/SNAP/facebook/facebook') -> nx.Graph:
    # Load {ego_id}.edges file
    # Simple space-separated edge list
    # Add ego node connected to all nodes in file
```

**3. DIMACS CLIQUE Loader** (`load_dimacs_graph()`)
```python
def load_dimacs_graph(filename: str, data_dir: str = 'data/DIMACS') -> nx.Graph:
    # Parse p edge line for node count
    # Parse e lines for edges
    # Build undirected graph
```

**4. Universal Graph Catalog** (`load_from_catalog()`)
```python
# Create data/graph_catalog.json with metadata for all graphs
# Single function to load any graph by name
def load_from_catalog(graph_name: str) -> Tuple[nx.Graph, Dict]:
    # Returns (graph, metadata)
```

---

## 7. Testing Recommendations

### Phase 1: Quick Validation (30 minutes)
Test 5-8 small graphs to verify all loaders work:
- SWtinyEWD, SWtinyDG (SW loader verification)
- ego-698, ego-414 (Facebook loader verification)
- email-Eu-core (SNAP loader verification)
- Run all algorithms, ensure valid covers

### Phase 2: Comprehensive Testing (2-3 hours)
Test all Tier 1 graphs (15 graphs):
- Document results in `implementation_3.md`
- Special focus on SW10000EWD and C1000.9
- Identify any algorithm failures or timeouts

### Phase 3: Dense Graph Study (1-2 hours)
Dedicated testing of DIMACS graphs:
- C1000.9: All algorithms, extended timeouts
- C2000.9: Approximations only
- Document density impact on performance

### Phase 4: Overnight Benchmark Suite (8-12 hours)
Run 20-25 graphs × 3-4 algorithms × 40 repetitions:
- Estimated 2,400-3,200 trials
- Checkpointing every 50 trials
- Full statistical analysis ready for Day 2

---

## 8. Risk Assessment

### High-Risk Graphs (may timeout or fail)

| Graph | Risk | Mitigation |
|-------|------|------------|
| SW10000EWD | Exact may timeout | Use 10-min timeout, skip if necessary |
| CA-HepPh (12k) | Exact will timeout | Approximations only |
| C2000.9 (1.8M edges) | All may be slow | Extended timeouts, approximations only |
| C4000.5 | Exact will fail | Approximations only, stretch goal |
| SWlargeG (100MB) | May not load | Optional only, expect failures |

### Conservative Approach

**Safe Benchmark Suite (No Risk):**
- Use only graphs with < 5,000 vertices and < 100k edges
- Guaranteed to complete: 15-18 graphs
- Sufficient for A+ if larger graphs fail

**Aggressive Approach (Maximum Impact):**
- Include all Tier 1 + Tier 2 (20-22 graphs)
- Attempt SW10000EWD, CA-HepPh, C1000.9, C2000.9
- Some timeouts expected, but impressive scope

**Recommended:** Hybrid approach
- Test all Tier 1 manually first
- If successful, include in overnight run
- If timeouts, document and use conservative suite

---

## 9. File Organization

```
data/
├── SW_ALGUNS_GRAFOS/          # 11 SW graphs (3 tested)
├── SNAP/
│   ├── ca-grqc/               # CA-GrQc.txt (5,242v)
│   ├── ca-hepph/              # CA-HepPh.txt (12,008v) ⭐
│   ├── email_eu_core/         # email-Eu-core.txt (1,005v)
│   ├── facebook/
│   │   ├── facebook_combined.txt (4,039v)
│   │   └── facebook/*.edges   # 10 ego networks (52-1,034v)
│   ├── wiki_vote/             # Wiki-Vote.txt (7,115v)
│   ├── friendster/            # ⚠️ 31GB - DO NOT USE
│   ├── youtube/               # ⚠️ Large - DO NOT USE
│   ├── live_journal/          # ⚠️ Large - DO NOT USE
│   └── orkut/                 # ⚠️ Large - DO NOT USE
├── DIMACS/
│   ├── C1000.9/c1000.txt      # 1,000v, 450k edges (p=0.9) ⭐
│   ├── C2000.9/c2000.txt      # 2,000v, 1.8M edges (p=0.9) ⭐
│   └── C4000.5/c4000.txt      # 4,000v, ~4M edges (p=0.5)
└── graph_catalog.json         # 🔄 To be created
```

---

## 10. Summary & Next Steps

### What We Have
- **32 usable graphs** spanning 13v to 12,008v
- **Excellent diversity**: sparse to ultra-dense (0.001 to 0.9)
- **Multiple domains**: social, collaboration, ego, random
- **Unique assets**: DIMACS dense benchmarks (novel contribution!)

### What We Need
1. **Implement 3 loaders**: SNAP, Facebook ego, DIMACS (2-3 hours)
2. **Create graph catalog**: JSON metadata file (30 min)
3. **Test all Tier 1 graphs**: 15 graphs comprehensive testing (2-3 hours)
4. **Configure overnight suite**: 20-25 graphs, 40 reps (1 hour)

### Success Criteria
- ✅ Load and test all 32 usable graphs
- ✅ Prove scalability to 10k-12k vertices
- ✅ Demonstrate algorithm performance on ultra-dense graphs (DIMACS)
- ✅ Statistical rigor: 2,400+ trials across diverse graphs
- ✅ Novel contribution: First edge cover study with dense benchmark analysis

### Critical Warnings
- **DO NOT** attempt Friendster (31GB file)
- **DO NOT** attempt YouTube/LiveJournal/Orkut (multi-GB compressed)
- **BE CAREFUL** with SWlargeG (100MB, may fail)
- **EXPECT TIMEOUTS** on CA-HepPh exact, C2000.9, C4000.5 exact

---

**Document Version:** 1.0
**Last Updated:** November 30, 2025
**Next Review:** After Phase 1 loader implementation
