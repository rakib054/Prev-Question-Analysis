import sys
from pathlib import Path
from apply_solutions import update_year_solutions

SOLUTIONS_2018 = {}

# -----------------------------------------------------------------------------
# toc-2018-q6a (26 marks)
# Consider the following grammar:
# S -> AACD
# A -> aAb | eps
# C -> aC | a
# D -> aDa | bDb | eps
# and simply safe order
# - (i) Eliminate eps-production.
# - (ii) Eliminate Unit production.
# - (iii) Eliminate useless symbols.
# - (iv) Put the grammar in CNF.
# -----------------------------------------------------------------------------
SOLUTIONS_2018["toc-2018-q6a"] = r"""### Problem Overview
We are given the context-free grammar:
$$\begin{aligned}
S &\to AACD \\
A &\to aAb \mid \varepsilon \\
C &\to aC \mid a \\
D &\to aDa \mid bDb \mid \varepsilon
\end{aligned}$$
*(Variables: $S, A, C, D$; Terminals: $a, b$)*

We simplify and convert the grammar into Chomsky Normal Form (CNF) following the standard, safe order.

---

### Step (i): Eliminate $\varepsilon$-Productions

1. **Find all nullable variables:**
   - Directly nullable: $A \to \varepsilon \implies A$ is nullable.
   - Directly nullable: $D \to \varepsilon \implies D$ is nullable.
   - For $C$: productions are $C \to aC \mid a$, containing terminal $a$, so $C$ is not nullable.
   - For $S$: $S \to AACD$. Even if $A$ and $D$ are dropped, $C$ remains, so $S$ is not nullable.
   - **Nullable variables:** $\{A, D\}$.

2. **Form new productions without $\varepsilon$:**
   - **For $A \to aAb \mid \varepsilon$:**
     - Keeping or dropping $A$: $A \to aAb \mid ab$. (Drop $A \to \varepsilon$).
   - **For $C \to aC \mid a$:**
     - $C$ contains no nullable variables: $C \to aC \mid a$.
   - **For $D \to aDa \mid bDb \mid \varepsilon$:**
     - From $aDa$: $aDa \mid aa$
     - From $bDb$: $bDb \mid bb$
     - Drop $D \to \varepsilon$.
     - Thus: $D \to aDa \mid aa \mid bDb \mid bb$.
   - **For $S \to AACD$:**
     - Here, the first $A$, the second $A$, and $D$ are nullable ($C$ is not nullable).
     - Possible non-empty combinations of keeping/dropping nullable variables:
       - Keep all: $AACD$
       - Drop $D$: $AAC$
       - Drop one $A$: $ACD$
       - Drop both $A$'s: $CD$
       - Drop one $A$ and $D$: $AC$
       - Drop both $A$'s and $D$: $C$
     - Thus:
       $$S \to AACD \mid AAC \mid ACD \mid AC \mid CD \mid C$$

**Grammar after Step (i):**
$$\begin{aligned}
S &\to AACD \mid AAC \mid ACD \mid AC \mid CD \mid C \\
A &\to aAb \mid ab \\
C &\to aC \mid a \\
D &\to aDa \mid aa \mid bDb \mid bb
\end{aligned}$$

---

### Step (ii): Eliminate Unit Productions
We identify and eliminate all productions of the form $X \to Y$ ($X, Y \in V$).

1. **Find unit pairs $(X, Y)$ where $X \Rightarrow^* Y$:**
   - Trivial pairs: $(S, S), (A, A), (C, C), (D, D)$
   - From $S \to C$: unit pair $(S, C)$
   - Variables $A, C, D$ have no unit productions to other variables.

2. **Replace unit production $S \to C$ with all non-unit productions of $C$:**
   - Non-unit productions of $C$ are: $aC \mid a$.
   - Add these to $S$ and remove $S \to C$:
     $$S \to AACD \mid AAC \mid ACD \mid AC \mid CD \mid aC \mid a$$

**Grammar after Step (ii):**
$$\begin{aligned}
S &\to AACD \mid AAC \mid ACD \mid AC \mid CD \mid aC \mid a \\
A &\to aAb \mid ab \\
C &\to aC \mid a \\
D &\to aDa \mid aa \mid bDb \mid bb
\end{aligned}$$

---

### Step (iii): Eliminate Useless Symbols

1. **Check Generating Symbols:**
   - Terminals: $\{a, b\}$.
   - $C \to a \implies C$ is generating.
   - $A \to ab \implies A$ is generating.
   - $D \to aa \mid bb \implies D$ is generating.
   - $S \to a \implies S$ is generating.
   - All variables $\{S, A, C, D\}$ are generating! No non-generating symbols exist.

2. **Check Reachable Symbols (from $S$):**
   - $S$ directly reaches $A, C, D$ through $AACD$.
   - All symbols are reachable!
   - No useless symbols exist in this grammar.

---

### Step (iv): Put the Grammar in Chomsky Normal Form (CNF)
In CNF, every production must have the form $X \to YZ$ or $X \to x$.

1. **Introduce variables for terminals:**
   - Let $X_a \to a$
   - Let $X_b \to b$

2. **Replace terminals in composite rules:**
   - $S \to a$ (already in CNF!)
   - $S \to AC$ and $S \to CD$ (already in CNF!)
   - $S \to aC \implies S \to X_a C$
   - $C \to a$ (already in CNF!)
   - $C \to aC \implies C \to X_a C$
   - $A \to ab \implies A \to X_a X_b$
   - $D \to aa \implies D \to X_a X_a$
   - $D \to bb \implies D \to X_b X_b$

3. **Break long bodies (length $\ge 3$) into pairs of variables:**
   - **For $S \to AAC$:** $S \to A Y_1$ where $Y_1 \to AC$
   - **For $S \to ACD$:** $S \to A Y_2$ where $Y_2 \to CD$
   - **For $S \to AACD$:** $S \to A Y_3$ where $Y_3 \to A Y_2$ (reusing $Y_2 \to CD$)
   - **For $A \to aAb$:** $A \to X_a Y_4$ where $Y_4 \to A X_b$
   - **For $D \to aDa$:** $D \to X_a Y_5$ where $Y_5 \to D X_a$
   - **For $D \to bDb$:** $D \to X_b Y_6$ where $Y_6 \to D X_b$

---

### Final CNF Grammar
$$\begin{aligned}
S &\to A Y_3 \mid A Y_1 \mid A Y_2 \mid AC \mid CD \mid X_a C \mid a \\
Y_3 &\to A Y_2 \\
Y_1 &\to AC \\
Y_2 &\to CD \\
A &\to X_a Y_4 \mid X_a X_b \\
Y_4 &\to A X_b \\
C &\to X_a C \mid a \\
D &\to X_a Y_5 \mid X_a X_a \mid X_b Y_6 \mid X_b X_b \\
Y_5 &\to D X_a \\
Y_6 &\to D X_b \\
X_a &\to a \\
X_b &\to b
\end{aligned}$$"""

# -----------------------------------------------------------------------------
# toc-2018-q7a (5 marks)
# What is meant by a Turing Machine (TM) with two way infinite tape?
# Give example(s).
# -----------------------------------------------------------------------------
SOLUTIONS_2018["toc-2018-q7a"] = r"""### 1. Definition of Two-Way Infinite Tape TM
In a **standard Turing Machine**, the tape is semi-infinite: it has a leftmost cell (index 0) and extends infinitely only to the right ($0, 1, 2, \dots$). Attempting to move left from cell 0 keeps the head on cell 0.

In a **Two-Way Infinite Tape Turing Machine**:
- The tape extends **infinitely in BOTH directions**:
  $$\dots, -3, -2, -1, 0, 1, 2, 3, \dots$$
- There is no left boundary or end-of-tape barrier.
- Initially, the input string $w = w_1 w_2 \dots w_n$ is placed on cells $0$ through $n-1$, and all other cells (both to the left of 0 and to the right of $n-1$) hold the blank symbol $B$.
- The read/write head begins on cell 0.

---

### 2. Computational Equivalence
> **Theorem:** A Turing Machine with a two-way infinite tape is **computationally equivalent** to a standard single-tape (one-way infinite) Turing Machine.

#### Simulation Idea:
A standard one-way infinite tape can simulate a two-way infinite tape using **two tracks**:
- **Track 1:** Holds the non-negative tape cells ($0, 1, 2, 3, \dots$).
- **Track 2:** Holds the negative tape cells ($-1, -2, -3, \dots$).
- When the two-way head moves right, the simulator moves right along Track 1. When the two-way head moves into negative indices, the simulator switches to Track 2 and moves right.

---

### 3. Example Use Cases
1. **Integer Arithmetic with Negative Numbers:**
   Computing integer operations where intermediate values or indices can be negative without needing to shift the entire tape content rightward.
2. **Centered Palindrome Checking:**
   A two-way tape allows placing an input in the center and expanding outwards symmetrically in both positive and negative directions without hitting an artificial left wall."""

# -----------------------------------------------------------------------------
# toc-2018-q7b (9 marks)
# Show that context free languages are closed under union operation but not
# under intersection.
# -----------------------------------------------------------------------------
SOLUTIONS_2018["toc-2018-q7b"] = r"""### 1. Part 1: CFLs are Closed under Union

#### Claim:
If $L_1$ and $L_2$ are context-free languages, then $L_1 \cup L_2$ is context-free.

#### Proof by Grammar Construction:
Let $G_1 = (V_1, T_1, P_1, S_1)$ generate $L_1$, and $G_2 = (V_2, T_2, P_2, S_2)$ generate $L_2$.
1. Rename variables so that $V_1 \cap V_2 = \emptyset$.
2. Create a new start symbol $S \notin V_1 \cup V_2$.
3. Define the combined grammar $G = (V, T, P, S)$ where:
   - $V = V_1 \cup V_2 \cup \{S\}$
   - $T = T_1 \cup T_2$
   - $P = P_1 \cup P_2 \cup \{S \to S_1 \mid S_2\}$
4. **Correctness:**
   - Any derivation begins with either $S \Rightarrow S_1$ (which derives all strings in $L_1$) or $S \Rightarrow S_2$ (which derives all strings in $L_2$).
   - Therefore, $L(G) = L_1 \cup L_2$.
Since $G$ is a valid CFG, **CFLs are closed under union**.

---

### 2. Part 2: CFLs are NOT Closed under Intersection

#### Claim:
There exist context-free languages $L_1$ and $L_2$ whose intersection $L_1 \cap L_2$ is NOT context-free.

#### Counterexample Proof:
Consider the two languages over $\Sigma = \{a, b, c\}$:
$$L_1 = \{a^n b^n c^m \mid n \ge 0, m \ge 0\}$$
$$L_2 = \{a^m b^n c^n \mid m \ge 0, n \ge 0\}$$

1. **Both $L_1$ and $L_2$ are CFLs:**
   - CFG for $L_1$: $S_1 \to AB, \; A \to aAb \mid \epsilon, \; B \to cB \mid \epsilon$
   - CFG for $L_2$: $S_2 \to CD, \; C \to aC \mid \epsilon, \; D \to bDc \mid \epsilon$
2. **Their Intersection:**
   $$L_1 \cap L_2 = \{a^n b^n c^n \mid n \ge 0\}$$
   A string in $L_1 \cap L_2$ must have $\#_a = \#_b$ (from $L_1$) AND $\#_b = \#_c$ (from $L_2$), requiring all three counts to be equal: $n = m$.
3. **Is $L_1 \cap L_2$ Context-Free?**
   **NO.** The language $\{a^n b^n c^n \mid n \ge 0\}$ is proven to be non-context-free via the Pumping Lemma for CFLs (a pushdown stack can compare two blocks of symbols, but cannot hold a third simultaneous count).

---

### 3. Conclusion
- **Union:** **CLOSED** (by construction $S \to S_1 \mid S_2$).
- **Intersection:** **NOT CLOSED** (by counterexample $L_1 \cap L_2 = \{a^n b^n c^n\}$)."""

# -----------------------------------------------------------------------------
# toc-2018-q7c (14 marks)
# Design a TM M to implement the function "Multiplication" using the subroutine
# copy. Simulate the action for the input 001000.
# -----------------------------------------------------------------------------
SOLUTIONS_2018["toc-2018-q7c"] = r"""### 1. Problem Formulation
Design a Turing Machine $M$ to compute multiplication of two unary integers:
$$f(m, n) = m \times n$$
- **Unary Input on Tape:** $0^m 1 0^n 1$ (or $0^m 1 0^n B$).
- **Input String:** `001000` ($m = 2, n = 3$).
- **Expected Output:** $0^{2 \times 3} = 0^6$ (`000000`).

---

### 2. High-Level Algorithm Using Subroutine `copy`
Multiplication is repeated addition. We copy the $n$ zeros to the output area $m$ times:
1. **Outer Loop (controlled by $m$):**
   - Scan the first operand: replace the first unmarked `0` with $X$.
   - Call the **`copy` subroutine**.
2. **`copy` Subroutine (copies $n$ zeros):**
   - For each zero of the second operand $0^n$: mark it as $Y$, travel to the right end of the tape, append a `0`, and return.
   - Once all $n$ zeros are copied, restore all $Y$'s back to `0` so they are ready for the next iteration.
3. **Repeat:** Return to the first operand and process the next `0`.
4. **Cleanup:** When all $m$ zeros have been marked $X$ (reading `1`), erase the operands and markers, leaving only the $m \times n$ result zeros.

---

### 3. Step-by-Step Simulation on "001000" ($2 \times 3$)
Initial tape: `0010001`

- **Iteration 1 (Process 1st zero of $m=2$):**
  1. $q_0$ marks first zero as $X$: tape becomes $X010001$.
  2. Subroutine `copy` runs on the three zeros of $n=3$:
     - Marks 1st zero $Y$, writes `0` at end: $X01Y0010$
     - Marks 2nd zero $Y$, writes `0` at end: $X01YY0100$
     - Marks 3rd zero $Y$, writes `0` at end: $X01YYY1000$
  3. Restores $YYY \to 000$: tape becomes $X010001000$.
  4. Returns left to $q_0$. Current product: $0^3$.

- **Iteration 2 (Process 2nd zero of $m=2$):**
  1. $q_0$ marks second zero as $X$: tape becomes $XX10001000$.
  2. Subroutine `copy` copies the 3 zeros of $n$ again to the end:
     - Tape becomes $XX1YYY1000000$
  3. Restores $YYY \to 000$: tape becomes $XX10001000000$.
  4. Returns left to $q_0$, positioning head at the separator `1`. Current product: $0^6$.

- **Termination & Cleanup:**
  1. In $q_0$, the head reads `1`, indicating that all zeros of $m$ are exhausted.
  2. Erases the input block $XX10001$, leaving only:
     $$\mathbf{000000} \quad (\text{exactly } 6 \text{ zeros})$$

**Final Output:** `000000` (representing $2 \times 3 = 6$)."""

# -----------------------------------------------------------------------------
# toc-2018-q7d (7 marks)
# Write about halting problem of TM.
# -----------------------------------------------------------------------------
SOLUTIONS_2018["toc-2018-q7d"] = r"""### 1. What is the Halting Problem?
The **Halting Problem** is the problem of determining whether an arbitrary Turing Machine $M$, when run on an arbitrary input string $w$, will eventually **halt** (terminate), or continue running in an **infinite loop** forever.

Formally defined as:
$$HALT_{TM} = \{ \langle M, w \rangle \mid M \text{ is a TM that halts on input } w \}$$

---

### 2. Proof of Undecidability (Turing, 1936)

#### Step 1: Assume a decider $H$ exists
Suppose there exists a Turing Machine $H$ that decides $HALT_{TM}$:
$$H(\langle M, w \rangle) = \begin{cases} 
\text{Accept} & \text{if } M \text{ halts on } w \\
\text{Reject} & \text{if } M \text{ loops on } w 
\end{cases}$$

#### Step 2: Construct adversarial machine $D$
Using $H$ as a subroutine, construct machine $D$ that takes the encoding of any TM $\langle M \rangle$ as input:
- Run $H$ on $\langle M, \langle M \rangle \rangle$.
- If $H$ outputs **Accept** ($M$ halts on $\langle M \rangle$), $D$ enters an **infinite loop**.
- If $H$ outputs **Reject** ($M$ loops on $\langle M \rangle$), $D$ **halts**.

#### Step 3: Self-Reference Contradiction
Now evaluate $D$ on its own encoding $\langle D \rangle$:
$$D(\langle D \rangle) = \begin{cases} 
\text{loops forever} & \text{if } D \text{ halts on } \langle D \rangle \\
\text{halts} & \text{if } D \text{ loops on } \langle D \rangle 
\end{cases}$$

This asserts that $D$ halts on $\langle D \rangle$ if and only if $D$ does NOT halt on $\langle D \rangle$.  
This direct contradiction proves that **no such decider $H$ can exist**.

---

### 3. Key Takeaway
The Halting Problem is **undecidable**. It is the classic example showing that algorithmic decidability has strict mathematical boundaries."""

# -----------------------------------------------------------------------------
# toc-2018-q8a (6 marks)
# What do you mean by tractable and intractable problem? Give example(s).
# -----------------------------------------------------------------------------
SOLUTIONS_2018["toc-2018-q8a"] = r"""### 1. Tractable Problems

#### Definition:
A computational problem is called **tractable** (or efficiently solvable) if there exists an algorithm that solves it in **polynomial time**:
$$O(n^k) \quad \text{for some constant } k$$
where $n$ is the input size. These problems belong to the complexity class **$P$**.

#### Characteristics:
- Can be solved realistically on modern computers even for large inputs (e.g., $n = 10^5$).
- Polynomial-time algorithms scale gracefully as $n$ grows.

#### Examples:
1. **Shortest Path Problem:** Dijkstra's Algorithm ($O(V^2)$ or $O(E + V \log V)$).
2. **Sorting:** Merge Sort / Heap Sort ($O(n \log n)$).
3. **Minimum Spanning Tree:** Kruskal's or Prim's Algorithm ($O(E \log V)$).
4. **Greatest Common Divisor (GCD):** Euclidean Algorithm ($O(\log(\min(a, b)))$).

---

### 2. Intractable Problems

#### Definition:
A computational problem is called **intractable** if there is **no known polynomial-time algorithm** to solve it in the worst case. Solving it requires **super-polynomial or exponential time**:
$$O(2^n), \quad O(n!), \quad \text{or } O(n^n)$$
*(or the problem is undecidable).*

#### Characteristics:
- For even moderate input sizes (e.g., $n = 100$), an exponential-time algorithm would take longer than the age of the universe to terminate.
- In practice, we solve intractable problems using **approximation algorithms**, **heuristics**, or **parameterized algorithms**.

#### Examples:
1. **Traveling Salesperson Problem (TSP - optimization):** Finding the exact shortest tour visiting all $n$ cities takes $O(n!)$ or $O(n^2 2^n)$ time.
2. **Boolean Satisfiability (3-SAT):** Checking if a 3-CNF formula is satisfiable.
3. **Hamiltonian Cycle:** Determining whether a graph contains a cycle visiting each vertex exactly once.
4. **Vertex Cover / Clique Problem.**

---

### 3. Summary Comparison Table

| Feature | Tractable Problems | Intractable Problems |
| :--- | :--- | :--- |
| **Time Complexity** | Polynomial time $O(n^k)$ | Exponential time $O(2^n)$ or worse |
| **Complexity Class** | Class $P$ | NP-Complete, NP-Hard, EXPTIME |
| **Practical Feasibility**| Solvable efficiently for large $n$ | Infeasible for large $n$; requires approximations |
| **Typical Examples** | Sorting, Shortest Path, MST | TSP, 3-SAT, Clique, Hamiltonian Cycle |"""

# -----------------------------------------------------------------------------
# toc-2018-q8c (11 marks)
# Use Pumping Lemma to show the followings:
# - (i) a^n b^m c^p is context free for n >= 0, m >= 0 and p = n.
# - (ii) a^n b^m c^p is not context free for n >= 0, m = 2n and p = m + n.
# -----------------------------------------------------------------------------
SOLUTIONS_2018["toc-2018-q8c"] = r"""### Part (i): Showing $L_1 = \{a^n b^m c^n \mid n \ge 0, m \ge 0\}$ is Context-Free

#### Important Theoretical Note:
The Pumping Lemma is a **necessary condition**, not a sufficient condition. Therefore, the Pumping Lemma is used strictly to prove a language is **NOT** context-free.  
To prove that a language **IS context-free**, we provide an explicit **Context-Free Grammar (CFG)** or a **Pushdown Automaton (PDA)**.

#### CFG Construction:
We can generate $L_1 = \{a^n b^m c^n \mid n \ge 0, m \ge 0\}$ using the grammar:
$$\begin{aligned}
S &\to aSc \mid B \\
B &\to bB \mid \epsilon
\end{aligned}$$
- Derivation of $a^n b^m c^n$:
  $$S \Rightarrow^n a^n S c^n \Rightarrow a^n B c^n \Rightarrow^m a^n b^m c^n$$
- Since an explicit CFG exists, **$L_1$ is guaranteed to be a Context-Free Language**.

#### Verification of Pumping Lemma Condition:
Any string $s = a^n b^m c^n$ with length $\ge p$ can be pumped:
- If $m \ge 1$, choose $v = \epsilon, w = b, x = b$ (pumping the $b$'s without changing $n$).
- If $m = 0$, choose $v = a, w = \epsilon, x = c$ (pumping $a$ and $c$ equally).  
In both cases, $u v^i w x^i y \in L_1$ for all $i \ge 0$.

---

### Part (ii): Prove $L_2 = \{a^n b^m c^p \mid n \ge 0, m = 2n, p = m + n\}$ is NOT Context-Free

#### 1. Simplify the Language
Substitute $m = 2n$ and $p = m + n = 2n + n = 3n$:
$$L_2 = \{a^n b^{2n} c^{3n} \mid n \ge 0\}$$
This requires a fixed ratio of $1 : 2 : 3$ between the counts of $a$'s, $b$'s, and $c$'s.

#### 2. Proof by Pumping Lemma for CFLs
1. **Assume $L_2$ is context-free.** Let $p \ge 1$ be its pumping length.
2. **Choose test string $s \in L_2$:**
   $$s = a^p b^{2p} c^{3p}$$
   Here $n = p$, so $|s| = 6p \ge p$.
3. **Decomposition $s = uvwxy$ satisfies:**
   - $|vwx| \le p$
   - $|vx| \ge 1$
   - $u v^i w x^i y \in L_2$ for all $i \ge 0$.
4. **Position of $vwx$:**
   Because $|vwx| \le p$, the substring $vwx$ can span a window of at most $p$ characters.  
   The block of $b$'s has length $2p > p$. Therefore, **$vwx$ can never contain both $a$'s and $c$'s simultaneously**.  
   Thus, $vx$ can contain symbols from at most **two** of the three groups $\{a, b, c\}$.
5. **Pumping with $i = 2$:**
   - If $vx$ contains only $a$'s and/or $b$'s:
     The number of $a$'s and/or $b$'s increases, but the number of $c$'s remains strictly $3p$.  
     If $a$'s increase, say to $n' > p$, then the required number of $c$'s is $3n' > 3p$, but the string still has only $3p$ copies of $c$. Thus $s' \notin L_2$.
   - If $vx$ contains only $b$'s and/or $c$'s:
     The count of $a$'s remains strictly $n = p$. For $s' \in L_2$, we must still have exactly $2p$ copies of $b$ and $3p$ copies of $c$. But since $|vx| \ge 1$, at least one of $b$ or $c$ increased in count. Thus $s' \notin L_2$.
   - In all cases, $u v^2 w x^2 y \notin L_2$.

#### Conclusion:
By contradiction, $L_2 = \{a^n b^{2n} c^{3n} \mid n \ge 0\}$ is **NOT context-free**."""

# -----------------------------------------------------------------------------
# toc-2018-q8d (8 marks)
# Define instantaneous description of a TM. What is the role of checking off
# symbols in TM?
# -----------------------------------------------------------------------------
SOLUTIONS_2018["toc-2018-q8d"] = r"""### 1. Instantaneous Description (ID) of a Turing Machine

#### Definition:
An **Instantaneous Description (ID)** is a formal snapshot that captures the complete configuration of a Turing Machine at any single step of its computation.

An ID is written as:
$$\alpha_1 q \alpha_2$$
where:
- $q \in Q$ is the **current state** of the Turing Machine.
- $\alpha_1 \alpha_2 \in \Gamma^*$ represents the **current contents of the tape** from the leftmost non-blank symbol to the rightmost non-blank symbol.
- The read/write head is currently scanning the **first symbol of $\alpha_2$** (if $\alpha_2 = \epsilon$, the head scans a blank symbol $B$).

#### The Move Relation ($\vdash$):
If the machine transition is $\delta(q, X) = (p, Y, D)$:
- **Move Right ($D = R$):**
  $$\alpha_1 q X \beta \vdash \alpha_1 Y p \beta$$
- **Move Left ($D = L$):**
  $$(\alpha Z) q X \beta \vdash \alpha p Z Y \beta$$

---

### 2. The Role of Checking Off Symbols in a Turing Machine

#### Why is Checking Off Necessary?
Unlike modern computers with random-access memory (RAM), a Turing Machine possesses only a sequential tape. When comparing or matching groups of symbols (such as verifying $0^n 1^n$, or checking $w w$), it must travel back and forth across the tape repeatedly.

"Checking off" is the technique of replacing an unprocessed symbol with a marked symbol (e.g., $0 \to X$ and $1 \to Y$).

#### Key Roles & Purposes:
1. **Bookkeeping (Keeping Track of Processed Items):**
   Ensures each symbol is counted exactly once, preventing duplicate counting or omissions during back-and-forth head sweeps.
2. **Boundary Delimiters (Stop Signals):**
   When the head sweeps back left across the tape, the marked symbol $X$ serves as a boundary marker, signaling the machine exactly where the next unprocessed symbol begins.
3. **Loop Prevention:**
   Guarantees that the algorithm terminates: on each pass, at least one symbol is marked off, ensuring finite progress.
4. **Cleanup / Output Restoration:**
   Once all symbols have been successfully matched, the checked-off markers can either be restored to their original symbols or converted to blanks/output."""

if __name__ == "__main__":
    update_year_solutions(2018, SOLUTIONS_2018)
