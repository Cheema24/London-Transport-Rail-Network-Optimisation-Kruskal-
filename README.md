# London Underground System Algorithms (COMP1828)

## Overview

This project, developed as part of a **COMP1828 group coursework** at the University of Greenwich, focuses on designing, implementing, and analysing algorithmic solutions for the London Underground network.

The system models real-world transport data and applies multiple core computer science algorithms to solve problems such as:

* Station status tracking
* Journey planning (time & stops)
* Network optimisation

**Uzbek Imtiaz Cheema** contributed to key parts of the implementation, including completing missing subtasks, algorithm implementation, and system validation.

---

## Key Features

### 1. Operational Station Status System

* Implemented using a **Direct Address Hash Table (DAHT)**
* Supports:

  * O(1) lookup
  * O(1) insertion
* Efficiently tracks whether stations are operational

Empirical testing showed constant-time performance even with large datasets (up to 50,000 stations). 

---

### 2. Journey Planner (Shortest Time)

* Modelled as a **weighted graph (adjacency list)**
* Implemented **Dijkstra’s Algorithm**
* Computes shortest travel time between stations

Example result:

* Shortest path: **A → C → E = 10 minutes** 

Real-world testing:

* Covent Garden → Leicester Square = **1 minute**
* Wimbledon → Stratford ≈ **50 minutes** 

---

### 3. Journey Planner (Fewest Stops)

* Implemented using **Breadth-First Search (BFS)**
* Guarantees shortest path in terms of number of stops
* Time complexity: **O(V + E)**

Example:

* Path: **A → C → E (2 stops)** 

Performance testing confirmed near-linear growth across increasing network sizes.

---

### 4. Network Backbone Optimisation

* Implemented **Kruskal’s Algorithm**
* Computes a **Minimum Spanning Tree (MST)**
* Identifies essential connections in the network

Key finding:

* Removing redundant edges keeps the network connected but increases journey time
* Example: route increased from **11 min → 18 min** when restricted to backbone 

---

## Key Learnings

* Different problems require **different data structures and algorithms** (hash tables, graphs, MSTs)
* Real-world networks are best modelled using **graph-based approaches**
* Algorithm complexity (O(1), O(V log V), O(V+E)) directly impacts scalability
* Empirical testing is essential to validate theoretical complexity
* Trade-offs exist between **efficiency and practicality** (e.g. removing edges vs journey time)
* BFS and Dijkstra solve similar problems but optimise for different metrics (stops vs time)
* Handling real-world data requires preprocessing, cleaning, and mapping

---

## Tech Stack

* Python
* Pandas
* Matplotlib
* CLRS Python Library

---

## Author Contribution

**Uzbek Imtiaz Cheema**

* Completed missing subtasks (including Task 4 components)
* Implemented and validated algorithmic solutions
* Contributed to testing and performance evaluation

---

## Group Members

* Uzbek Imtiaz Cheema
* Missaoui Mohamed Ilias
* Mihir Patel
* Sharea Ibrahim
* Abdullah Saliùe
* Hammad Yacub

---

## Context

University of Greenwich – Computer Science
COMP1828 Coursework

---

## References

* Cormen et al. (2009). *Introduction to Algorithms*
* Additional sources included in full report
