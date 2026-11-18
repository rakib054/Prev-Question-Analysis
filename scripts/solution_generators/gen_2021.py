import sys
from pathlib import Path
from apply_solutions import update_year_solutions

SOLUTIONS_2021 = {}

# -----------------------------------------------------------------------------
# toc-2021-q5a (25 marks)
# Consider the grammar:
# S -> ASA | aB
# A -> B | S
# B -> b | eps
# - i) Eliminate eps productions.
# - ii) Eliminate unit productions in the resulting grammar from (i).
# - iii) Eliminate useless productions in the resulting grammar from (ii).
# - iv) Put the grammar from (iii) in Chomsky Normal Form (CNF).
# -----------------------------------------------------------------------------
SOLUTIONS_2021["toc-2021-q5a"] = r"""### Problem Overview
We are given the context-free grammar:
$$\begin{aligned}
S &\to ASA \mid aB \\
A &\to B \mid S \\
B &\to b \mid \epsilon
\end{aligned}$$
*(Variables: $S, A, B$; Terminals: $a, b$)*

We simplify and convert this grammar to Chomsky Normal Form step-by-step.

---

### Step (i): Eliminate $\epsilon$-Productions

1. **Find all nullable variables:**
   - $B \to \epsilon \implies B$ is nullable.
   - Since $B$ is nullable and $A \to B \implies A$ is nullable.
   - For $S$: $S \to ASA$ (if both $A$'s are dropped, we get $S \to S$, not $\epsilon$) and $S \to aB$ (if $B$ is dropped, we get $S \to a$, not $\epsilon$).  
     Thus, $S$ cannot derive $\epsilon$.
   - **Nullable variables:** $\{A, B\}$.

2. **Form new productions without $\epsilon$:**
   For each production, consider all combinations of presence/absence of nullable variables (omitting any rule that produces $\epsilon$):
   - **For $B \to b \mid \epsilon$:**
     Drop $\epsilon \implies B \to b$
   - **For $A \to B \mid S$:**
     $A \to B \mid S$
   - **For $S \to ASA \mid aB$:**
     - From $ASA$ ($A$ is nullable at positions 1 and 3):
       - Keep both: $ASA$
       - Drop first $A$: $SA$
       - Drop second $A$: $AS$
       - Drop both: $S$ (unit production $S \to S$ will be handled)
     - From $aB$ ($B$ is nullable):
       - Keep $B$: $aB$
       - Drop $B$: $a$
     - Combining:
       $$S \to ASA \mid AS \mid SA \mid S \mid aB \mid a$$
       *(Note: The trivial self-loop $S \to S$ can be omitted).*

**Grammar after Step (i):**
$$\begin{aligned}
S &\to ASA \mid AS \mid SA \mid aB \mid a \\
A &\to B \mid S \\
B &\to b
\end{aligned}$$

---

### Step (ii): Eliminate Unit Productions
Identify all unit pairs $(X, Y)$ where $X \Rightarrow^* Y$:
- Base unit pairs: $(S, S), (A, A), (B, B)$
- From $A \to B$: unit pair $(A, B)$
- From $A \to S$: unit pair $(A, S)$
- Variable $S$ has no unit productions to other variables.
- Variable $B$ has no unit productions.

Replace each unit production $X \to Y$ with the non-unit productions of $Y$:
- **For $B$:**
  $$B \to b$$
- **For $S$:**
  $$S \to ASA \mid AS \mid SA \mid aB \mid a$$
- **For $A$:**
  Inherits non-unit productions from $(A, A)$, $(A, B)$, and $(A, S)$:
  $$A \to b \mid ASA \mid AS \mid SA \mid aB \mid a$$

**Grammar after Step (ii):**
$$\begin{aligned}
S &\to ASA \mid AS \mid SA \mid aB \mid a \\
A &\to ASA \mid AS \mid SA \mid aB \mid a \mid b \\
B &\to b
\end{aligned}$$

---

### Step (iii): Eliminate Useless Productions
A symbol must be both generating and reachable.

1. **Check Generating Symbols:**
   - Terminals: $\{a, b\}$.
   - $B \to b \implies B$ is generating.
   - $S \to a \implies S$ is generating.
   - $A \to a \mid b \implies A$ is generating.
   - All variables $\{S, A, B\}$ are generating. No non-generating symbols exist.

2. **Check Reachable Symbols (from $S$):**
   - Start with $S$: Reachable $= \{S\}$.
   - $S \to ASA \mid aB$ references variables $A$ and $B$.
   - Thus, Reachable $= \{S, A, B\}$.
   - All symbols are reachable. No unreachable symbols exist.

**Grammar after Step (iii):** (Identical to Step (ii))

---

### Step (iv): Put into Chomsky Normal Form (CNF)
In CNF, every production must be of the form $X \to YZ$ or $X \to x$.

1. **Introduce variables for terminals:**
   - Let $X_a \to a$
   - Let $X_b \to b$ (or simply use existing $B \to b$)

2. **Replace terminals in composite bodies:**
   - $aB \implies X_a B$
   - $a$ is already a single terminal ($S \to a, A \to a$).
   - $b$ is already a single terminal ($A \to b, B \to b$).
   - $AS$ and $SA$ are already pairs of two variables (valid CNF!).

3. **Break long bodies (length 3) into pairs:**
   - $ASA \implies A Y_1$ where $Y_1 \to SA$

4. **Final CNF Grammar:**
   $$\begin{aligned}
   S &\to A Y_1 \mid AS \mid SA \mid X_a B \mid a \\
   A &\to A Y_1 \mid AS \mid SA \mid X_a B \mid a \mid b \\
   B &\to b \\
   Y_1 &\to SA \\
   X_a &\to a
   \end{aligned}$$"""

# -----------------------------------------------------------------------------
# toc-2021-q5b (10 marks)
# Is Context-free language (CFL) closed under Union and Intersection? Verify your answer.
# -----------------------------------------------------------------------------
SOLUTIONS_2021["toc-2021-q5b"] = r"""### 1. Overview of the Answer
- **Is CFL closed under Union?** **YES.**
- **Is CFL closed under Intersection?** **NO.**

---

### 2. Verification for UNION (CFL is Closed under Union)

#### Formal Statement:
If $L_1$ and $L_2$ are context-free languages, then $L_1 \cup L_2$ is also a context-free language.

#### Proof by Grammar Construction:
Let $G_1 = (V_1, T_1, P_1, S_1)$ generate $L_1$ and $G_2 = (V_2, T_2, P_2, S_2)$ generate $L_2$.
1. Rename variables if necessary so that $V_1 \cap V_2 = \emptyset$.
2. Create a new start symbol $S \notin V_1 \cup V_2$.
3. Construct the combined grammar $G = (V, T, P, S)$ where:
   - $V = V_1 \cup V_2 \cup \{S\}$
   - $T = T_1 \cup T_2$
   - $P = P_1 \cup P_2 \cup \{S \to S_1 \mid S_2\}$
4. **Correctness:**
   - If $w \in L_1$, then $S \Rightarrow S_1 \Rightarrow^* w$.
   - If $w \in L_2$, then $S \Rightarrow S_2 \Rightarrow^* w$.
   - Any derivation from $S$ must choose either $S_1$ or $S_2$, producing a string in $L_1$ or $L_2$.
   - Hence, $L(G) = L_1 \cup L_2$.
Since $G$ is a valid CFG, **CFLs are closed under union**.

---

### 3. Verification for INTERSECTION (CFL is NOT Closed under Intersection)

#### Formal Statement:
There exist context-free languages $L_1$ and $L_2$ such that $L_1 \cap L_2$ is NOT context-free.

#### Counterexample Proof:
Consider the two languages over $\Sigma = \{a, b, c\}$:
$$L_1 = \{a^n b^n c^m \mid n \ge 0, m \ge 0\}$$
$$L_2 = \{a^m b^n c^n \mid m \ge 0, n \ge 0\}$$

1. **$L_1$ is a CFL:**
   Can be generated by the CFG:
   $$S \to AB, \quad A \to aAb \mid \epsilon, \quad B \to cB \mid \epsilon$$
2. **$L_2$ is a CFL:**
   Can be generated by the CFG:
   $$S \to CD, \quad C \to aC \mid \epsilon, \quad D \to bDc \mid \epsilon$$
3. **Now compute their intersection:**
   $$L = L_1 \cap L_2 = \{a^n b^n c^n \mid n \ge 0\}$$
   A string in $L_1 \cap L_2$ must satisfy both:
   - Equal number of $a$'s and $b$'s (from $L_1$).
   - Equal number of $b$'s and $c$'s (from $L_2$).
   - Therefore, the number of $a$'s, $b$'s, and $c$'s must all be identical.
4. **Is $L_1 \cap L_2$ Context-Free?**
   **NO.** The language $\{a^n b^n c^n \mid n \ge 0\}$ is a well-known non-context-free language (proven via the Pumping Lemma for CFLs). A pushdown automaton has only one stack and can compare at most two counts (e.g. $a$ with $b$), but cannot verify that a third count ($c$) also matches.

---

### 4. Summary
- **Union:** **CLOSED** (verified by the construction $S \to S_1 \mid S_2$).
- **Intersection:** **NOT CLOSED** (verified by the counterexample $L_1 \cap L_2 = \{a^n b^n c^n\}$)."""

# -----------------------------------------------------------------------------
# toc-2021-q6c (8 marks)
# Write short notes on:
# - i) Post's Correspondence Problem
# - ii) Circuit Satisfiability Problem
# -----------------------------------------------------------------------------
SOLUTIONS_2021["toc-2021-q6c"] = r"""### (i) Post's Correspondence Problem (PCP)

#### 1. What is PCP?
Introduced by Emil Post in 1946, **Post's Correspondence Problem (PCP)** is a famous decision problem about string matching:
- **Input:** Two lists of $k$ strings over an alphabet $\Sigma$:
  - List $A = (u_1, u_2, \dots, u_k)$
  - List $B = (v_1, v_2, \dots, v_k)$
- **Question:** Does there exist a sequence of indices $i_1, i_2, \dots, i_m$ ($m \ge 1$, where indices can repeat) such that:
  $$u_{i_1} u_{i_2} \dots u_{i_m} = v_{i_1} v_{i_2} \dots v_{i_m}$$
  If such a sequence exists, it is called a **match** (or correspondence).

#### 2. Illustrative Example:
Let List $A = (b, bab^3, a)$ and List $B = (b^3, ba, a)$.
- Pairs: $(u_1, v_1) = (b, b^3)$, $(u_2, v_2) = (bab^3, ba)$, $(u_3, v_3) = (a, a)$.
- Choose index sequence: $(2, 1, 1, 3)$:
  - From $A$: $u_2 u_1 u_1 u_3 = (bab^3)(b)(b)(a) = bab^5 a$
  - From $B$: $v_2 v_1 v_1 v_3 = (ba)(b^3)(b^3)(a) = bab^7 a$ (Mismatch).
- Finding a match requires exact equality of concatenated strings.

#### 3. Significance & Decidability:
- **PCP is UNDECIDABLE.** There is no general algorithm that can determine whether an arbitrary PCP instance has a match.
- Proven undecidable via reduction from the Turing Machine Acceptance Problem ($A_{TM}$) through a variant called **Modified PCP (MPCP)**.
- PCP is widely used as a stepping stone to prove that many problems in formal grammars (e.g., ambiguity of CFGs, equivalence of CFGs) are undecidable.

---

### (ii) Circuit Satisfiability Problem (Circuit-SAT)

#### 1. What is Circuit-SAT?
**Circuit Satisfiability (Circuit-SAT)** is a central decision problem in computational complexity:
- **Input:** A Boolean combinational circuit consisting of:
  - Input gates (variables $x_1, x_2, \dots, x_n$).
  - Logic gates (AND, OR, NOT).
  - A single output wire.
  - No feedback loops (a Directed Acyclic Graph).
- **Question:** Does there exist an assignment of truth values ($\{0, 1\}$) to the input wires that causes the output wire to evaluate to **1 (TRUE)**?

#### 2. Significance in Complexity Theory:
- **Circuit-SAT is NP-Complete.**
- Historically, the **Cook-Levin Theorem** proved Circuit-SAT to be NP-complete directly by simulating the polynomial-time computation of a Non-deterministic Turing Machine using logic gates:
  - Each tape cell, state transition, and head position at each clock cycle is modeled by simple logic gates.
  - The circuit outputs 1 if and only if the NTM reaches an accepting state.
- **Verification in NP:** Given a candidate binary input string (certificate), evaluating the circuit gate by gate in topological order takes linear time $O(\text{size of circuit})$. Thus, $\text{Circuit-SAT} \in NP$.
- Circuit-SAT serves as the base problem used to reduce to formula SAT, which in turn reduces to 3-SAT."""

# -----------------------------------------------------------------------------
# toc-2021-q7a (6 marks)
# Write the differences between Multi-track and multitape Turing Machines.
# -----------------------------------------------------------------------------
SOLUTIONS_2021["toc-2021-q7a"] = r"""### 1. Overview
Both **Multi-Track** and **Multi-Tape** Turing Machines are variations of the standard Turing Machine designed to represent and process multiple data streams. However, their physical organization and head mechanics differ significantly.

---

### 2. Comparison Table

| Comparison Criteria | Multi-Track Turing Machine | Multi-Tape Turing Machine |
| :--- | :--- | :--- |
| **Number of Tapes** | Exactly **1 physical tape**, divided into $k$ parallel tracks. | **$k$ physically separate tapes** ($k \ge 1$). |
| **Number of Heads** | Exactly **1 read/write head** that scans across all $k$ tracks at the same position. | **$k$ independent read/write heads**, one for each tape. |
| **Head Movement** | All tracks move together: the single head moves Left or Right as one unit. | Each head moves **independently** (Left, Right, or Stay) on its respective tape. |
| **Tape Alphabet** | Cartesian product $\Gamma = \Gamma_1 \times \Gamma_2 \times \dots \times \Gamma_k$. Each tape cell holds a tuple of $k$ symbols. | Each tape has its own tape alphabet $\Gamma$. |
| **Transition Function** | $\delta: Q \times \Gamma^k \to Q \times \Gamma^k \times \{L, R\}$ | $\delta: Q \times \Gamma^k \to Q \times \Gamma^k \times \{L, R, S\}^k$ |
| **Time Complexity** | Runs in essentially the **same time** as a standard single-tape TM (no asymptotic speedup). | Can achieve **quadratic speedup** (e.g., palindrome recognition in $O(n)$ time vs $O(n^2)$). |
| **Computational Power** | Exactly identical (recognizes Recursively Enumerable languages). | Exactly identical (recognizes Recursively Enumerable languages). |

---

### 3. Key Takeaway
- A **multi-track TM** is simply a single-tape TM with a richer tape alphabet (tuples of symbols). It is used for bookkeeping (such as marking checked-off symbols on track 2 without altering original inputs on track 1).
- A **multi-tape TM** has true independent read/write heads moving in different directions at different speeds, offering significant practical algorithmic flexibility."""

# -----------------------------------------------------------------------------
# toc-2021-q7b (14 marks)
# What is NP-Complete problem? Prove that "Clique problem is NP-Complete problem".
# -----------------------------------------------------------------------------
SOLUTIONS_2021["toc-2021-q7b"] = r"""### 1. What is an NP-Complete Problem?
A decision problem $X$ is **NP-Complete** if it satisfies two conditions:
1. **$X \in NP$:** A candidate solution (certificate) can be verified deterministically in **polynomial time**.
2. **$X$ is NP-Hard:** Every problem $L \in NP$ can be reduced to $X$ in polynomial time ($L \le_p X$).

NP-complete problems represent the hardest problems in NP. If any single NP-complete problem can be solved in polynomial time, then $P = NP$.

---

### 2. Definition of the Clique Problem
- **Clique:** In an undirected graph $G = (V, E)$, a **clique** is a subset of vertices $V' \subseteq V$ such that every two distinct vertices in $V'$ are adjacent (connected by an edge in $E$).
- **The Decision Problem:** Given a graph $G = (V, E)$ and a positive integer $k$, does $G$ contain a clique of size at least $k$?
  $$\text{CLIQUE} = \{ \langle G, k \rangle \mid G \text{ is an undirected graph with a clique of size } \ge k \}$$

---

### 3. Proof that CLIQUE is NP-Complete

#### Step 1: Prove that $\text{CLIQUE} \in NP$
- **Certificate:** A subset of vertices $V' \subseteq V$.
- **Verification Algorithm:**
  1. Check if $|V'| \ge k$.
  2. For every pair of distinct vertices $u, v \in V'$, verify whether $\{u, v\} \in E$.
- **Time Complexity:** Checking all pairs takes $\binom{k}{2} = O(k^2) \le O(|V|^2)$ edge lookups, which runs in **polynomial time**.
- Therefore, $\text{CLIQUE} \in NP$.

#### Step 2: Prove that CLIQUE is NP-Hard
We reduce from the known NP-complete problem **3-SAT** to **CLIQUE** in polynomial time:
$$\text{3-SAT} \le_p \text{CLIQUE}$$

##### (a) The Reduction Construction
Let $\phi = C_1 \wedge C_2 \wedge \dots \wedge C_m$ be a 3-CNF Boolean formula with $m$ clauses, where each clause contains exactly 3 literals:
$$C_r = (l_{r1} \vee l_{r2} \vee l_{r3})$$

Construct an instance of CLIQUE $(G, k)$ as follows:
1. **Vertices $V$:** For each clause $C_r$ ($1 \le r \le m$), create 3 vertices corresponding to its 3 literals: $v_{r1}, v_{r2}, v_{r3}$.  
   Total number of vertices: $|V| = 3m$.
2. **Edges $E$:** Connect two distinct vertices $v_{ri}$ and $v_{sj}$ with an edge if and only if:
   - **Condition 1:** They belong to **different clauses** ($r \ne s$). (Never connect literals within the same clause).
   - **Condition 2:** The literals are **consistent** (they are NOT negations of each other, i.e., $l_{ri} \ne \neg l_{sj}$).
3. **Target size:** Set $k = m$ (the number of clauses).

##### (b) Polynomial Time
The graph $G$ has $3m$ vertices and at most $\binom{3m}{2} = O(m^2)$ edges. The construction takes $O(m^2)$ time, which is polynomial in the size of $\phi$.

##### (c) Correctness Proof ($\phi$ is satisfiable $\iff G$ has an $m$-clique)

- **Direction 1 ($\Rightarrow$): If $\phi$ is satisfiable, then $G$ has an $m$-clique.**
  - If $\phi$ is satisfiable, there is a truth assignment that makes at least one literal in each clause TRUE.
  - From each clause $C_r$, select one true literal $v_r$. This gives a set of $m$ vertices $V' = \{v_1, v_2, \dots, v_m\}$.
  - Any two selected vertices $v_r, v_s$ ($r \ne s$) are from different clauses and both evaluate to TRUE under the same assignment, so they cannot be contradictory ($l_r \ne \neg l_s$).
  - By construction, there is an edge between every pair of vertices in $V'$.
  - Thus, $V'$ forms a clique of size $m$.

- **Direction 2 ($\Leftarrow$): If $G$ has an $m$-clique, then $\phi$ is satisfiable.**
  - Let $V'$ be a clique of size $m$ in $G$.
  - Since vertices in the same clause have no edges between them, $V'$ must contain **exactly one vertex from each of the $m$ clauses**.
  - Since all vertices in $V'$ are connected by edges, no two vertices in $V'$ represent contradictory literals ($x$ and $\neg x$).
  - Assign TRUE to each literal corresponding to a vertex in $V'$. Any variable not in $V'$ can be assigned arbitrarily.
  - Since every clause contains at least one literal that is assigned TRUE, all $m$ clauses are satisfied.
  - Therefore, $\phi$ is satisfiable.

---

### 4. Conclusion
Because $\text{CLIQUE} \in NP$ and $\text{3-SAT} \le_p \text{CLIQUE}$, **the Clique problem is NP-Complete**."""

# -----------------------------------------------------------------------------
# toc-2021-q8a (15 marks)
# Design a Turing Machine to implement "Multiplication" operation using
# subroutine copy. Stimulate the action for 000100.
# -----------------------------------------------------------------------------
SOLUTIONS_2021["toc-2021-q8a"] = r"""### 1. Problem Understanding & Representation
We want to implement the multiplication function $f(m, n) = m \times n$ on a standard single-tape Turing Machine.
- **Unary Representation:** A non-negative integer $k$ is represented as a sequence of $k$ zeros ($0^k$).
- **Input on Tape:** $0^m 1 0^n 1$ (or $0^m 1 0^n B$).  
  For the given test string `000100`, $m = 3$ and $n = 2$.
- **Expected Output:** $0^{m \times n} = 0^{3 \times 2} = 0^6$ (`000000`).

---

### 2. Algorithm Using Subroutine `copy`

#### High-Level Idea:
Multiplication is repeated addition. We add $n$ zeros to our result $m$ times:
1. For each of the $m$ zeros of the first operand:
   - Mark one zero of $m$ with an $X$.
   - Call the **`copy` subroutine**: copy all $n$ zeros of the second operand to the output area at the right end of the tape.
2. Repeat until all $m$ zeros are marked as $X$.
3. Clean up the tape by erasing the markers and operands, leaving only the $m \times n$ zeros as the final output.

#### Subroutine `copy`:
- Scans the $n$ zeros of the second operand.
- For each `0`, marks it with a temporary symbol $Y$, travels right past the end of the tape, and appends a `0` to the result.
- Returns left and repeats until all $n$ zeros are marked $Y$.
- Restores all $Y$'s back to `0` so they can be copied again in the next iteration.

---

### 3. Step-by-Step State Design

- **State $q_0$ (Main Loop):**
  - Scans the first operand.
  - Replaces the first unmarked `0` with `X`, enters $q_1$ (moving toward the second operand).
  - If it reads `1` instead of `0`, all $m$ zeros have been processed $\implies$ enters cleanup state $q_{clean}$.
- **State $q_1$ (Move to second operand):**
  - Skips over remaining `0`s and the separator `1`, positions head at the start of the second operand, enters $q_2$ (subroutine `copy`).
- **Subroutine `copy` ($q_2, q_3, q_4, q_5$):**
  - **$q_2$:** Finds next unmarked `0` of the second operand. Replaces it with `Y`, enters $q_3$ to write a `0` at the end.
    - If it reads `1` (or blank), all $n$ zeros are copied $\implies$ enters $q_5$ to restore $Y \to 0$.
  - **$q_3$:** Travels right past all symbols to the end of the tape (blank $B$). Writes `0`, enters $q_4$ (return).
  - **$q_4$:** Travels left past all symbols until the marked $Y$ is found. Moves right to scan next zero in $q_2$.
  - **$q_5$ (Restore $Y$'s):** Moves left across the second operand, converting every $Y$ back to `0`. Once the middle `1` is crossed, moves left back to the first operand and returns to $q_0$.
- **Cleanup ($q_{clean}$):**
  - Erases all $X$'s and the separator `1`s and original operand, leaving only the newly written product zeros.

---

### 4. Simulation Trace for Input "000100" ($3 \times 2$)
Initial tape: `0001001` (with blank $B$ after).

1. **Iteration 1 (Process 1st zero of $m=3$):**
   - $q_0 000100 \vdash X q_1 00100 \vdash \dots \vdash X001 q_2 00$
   - Subroutine `copy` runs for each of the two `0`s of $n=2$:
     - Marks first `0` as $Y$, appends `0` at end: tape becomes $X001Y010$
     - Marks second `0` as $Y$, appends `0` at end: tape becomes $X001YY100$
   - Restores $Y \to 0$: tape becomes $X00100100$
   - Head returns to $q_0$: tape has 2 result zeros ($0^2$).
2. **Iteration 2 (Process 2nd zero of $m=3$):**
   - Head marks second `0`: tape becomes $XX0100100$.
   - Subroutine `copy` appends 2 more zeros at the end: tape becomes $XX010010000$.
   - Head returns to $q_0$: tape has 4 result zeros ($0^4$).
3. **Iteration 3 (Process 3rd zero of $m=3$):**
   - Head marks third `0`: tape becomes $XXX10010000$.
   - Subroutine `copy` appends 2 more zeros at the end: tape becomes $XXX1001000000$.
   - Head returns to $q_0$: tape has 6 result zeros ($0^6$).
4. **Completion & Cleanup:**
   - In state $q_0$, head reads `1` (all $m=3$ zeros are processed).
   - Machine erases $XXX1001$, leaving:
     $$\mathbf{000000} \quad (\text{exactly } 6 \text{ zeros})$$

**Final Output:** `000000` (representing $3 \times 2 = 6$)."""

# -----------------------------------------------------------------------------
# toc-2021-q8b (12 marks)
# Use Pumping Lemma to show the following languages are not Context-free language:
# - i) L = {ww | w is in {0,1}*}
# - ii) L = {a^m b^m c^n | m <= n <= 2m}
# -----------------------------------------------------------------------------
SOLUTIONS_2021["toc-2021-q8b"] = r"""### Part (i): Prove $L = \{ww \mid w \in \{0, 1\}^*\}$ is NOT Context-Free

#### 1. Assume $L$ is context-free
Assume, for contradiction, that $L$ is a CFL. Let $p \ge 1$ be the pumping length given by the Pumping Lemma.

#### 2. Choose string $s \in L$
Choose the string:
$$s = 0^p 1^p 0^p 1^p$$
- Here $w = 0^p 1^p$, so $s = ww \in L$.
- The length is $|s| = 4p \ge p$.

#### 3. Analyze decomposition $s = uvwxy$
By the Pumping Lemma:
- $|vwx| \le p$
- $|vx| \ge 1$
- $u v^k w x^k y \in L$ for all $k \ge 0$.

Because $|vwx| \le p$, the substring $vwx$ can span a window of at most length $p$.  
In the string $s = \underbrace{0^p 1^p}_{\text{1st } w} \underbrace{0^p 1^p}_{\text{2nd } w}$, the two blocks of $0^p$ are separated by a block of $1^p$ of length $p$.  
Therefore, $vwx$ **cannot contain symbols from both the first $0^p$ and the second $0^p$** simultaneously!

#### 4. Case Analysis on $vwx$:
- **Case 1: $vwx$ falls entirely within the first half ($w_1 = 0^p 1^p$):**
  - Pumping $k = 2$ increases the length of the first half, but leaves the second half completely unchanged.
  - The new string $s' = uv^2wx^2y$ has length $> 4p$. If $s' = w'w'$, the midpoint shifts right, so the second half must now contain some symbols that originally belonged to the first half. The new halves cannot be identical ($w' \ne w'$). Thus $s' \notin L$.
- **Case 2: $vwx$ straddles the middle boundary (the first $1^p$ and second $0^p$):**
  - Then $vx$ contains only $1$'s from the first half and/or $0$'s from the second half.
  - Pump with $k = 0$ (pumping down): removing $vx$ reduces the number of $1$'s in the first half or reduces the number of $0$'s in the second half.
  - The first half now has fewer $1$'s than $0$'s, while the second half still has $p$ ones, making it impossible for the string to have the form $w'w'$. Thus $s' \notin L$.
- **Case 3: $vwx$ falls entirely within the second half ($w_2 = 0^p 1^p$):**
  - Symmetric to Case 1: pumping $k=2$ alters the second half while leaving the first half unchanged. Thus $s' \notin L$.

In all cases, a contradiction arises. Hence, $L = \{ww \mid w \in \{0, 1\}^*\}$ is **NOT a context-free language**.

---

### Part (ii): Prove $L = \{a^m b^m c^n \mid m \le n \le 2m\}$ is NOT Context-Free

#### 1. Assume $L$ is context-free
Assume, for contradiction, that $L$ is a CFL with pumping length $p$.

#### 2. Choose string $s \in L$
Choose:
$$s = a^p b^p c^{2p}$$
- Here $m = p$ and $n = 2p$.
- Since $m \le n \le 2m \implies p \le 2p \le 2p$ holds, $s \in L$.
- The length is $|s| = 4p \ge p$.

#### 3. Analyze decomposition $s = uvwxy$
By the lemma: $|vwx| \le p$ and $|vx| \ge 1$.  
Because $|vwx| \le p$, the substring $vwx$ cannot contain both $a$'s and $c$'s simultaneously (they are separated by $b^p$ of length $p$).

#### 4. Case Analysis on $vwx$:
- **Case 1: $vwx$ contains only $a$'s and/or $b$'s (no $c$'s):**
  - Pump DOWN with $k = 0$ ($s' = uwy$).
  - At least one $a$ or $b$ is removed from $vx$.
  - If unequal numbers of $a$'s and $b$'s are removed, the number of $a$'s no longer equals the number of $b$'s $\implies s' \notin L$.
  - If equal numbers of $a$'s and $b$'s are removed (say $d \ge 1$), the new count of $a$'s and $b$'s is $m' = p - d < p$.
  - The number of $c$'s remains $n = 2p$.
  - Now check the condition $n \le 2m'$:
    $$2p \le 2(p - d) = 2p - 2d$$
    Since $d \ge 1$, $2p \le 2p - 2$, which is mathematically impossible! Thus $s' \notin L$.
- **Case 2: $vwx$ contains only $c$'s:**
  - $vx$ contains $d \ge 1$ copies of $c$.
  - Pump UP with $k = 2$ ($s' = uv^2wx^2y$).
  - The number of $a$'s and $b$'s remains $m = p$.
  - The new number of $c$'s becomes $n' = 2p + d$.
  - Check the condition $n' \le 2m$:
    $$2p + d \le 2p$$
    Since $d \ge 1$, $2p + d > 2p$, violating $n \le 2m$! Thus $s' \notin L$.
- **Case 3: $vwx$ contains $b$'s and $c$'s (across the $b$-$c$ boundary):**
  - Then $vx$ contains $d_b$ copies of $b$ and $d_c$ copies of $c$ ($d_b + d_c \ge 1$, but contains no $a$'s).
  - The number of $a$'s remains strictly $p$.
  - If $d_b \ge 1$, pumping $k=2$ increases the number of $b$'s, so $\#_b(s') > p = \#_a(s')$, violating the requirement that the number of $a$'s equals the number of $b$'s! Thus $s' \notin L$.

In every case, we reach a contradiction. Therefore, $L = \{a^m b^m c^n \mid m \le n \le 2m\}$ is **NOT a context-free language**."""

# -----------------------------------------------------------------------------
# toc-2021-q8c (8 marks)
# Explain the halting problem of Turing Machine.
# -----------------------------------------------------------------------------
SOLUTIONS_2021["toc-2021-q8c"] = r"""### 1. What is the Halting Problem?
The **Halting Problem** is the problem of determining, given an arbitrary Turing Machine $M$ and an arbitrary input string $w$, whether $M$ will eventually **halt** on input $w$ (either accept or reject), or run forever in an **infinite loop**.

Formally represented as the decision language:
$$HALT_{TM} = \{ \langle M, w \rangle \mid M \text{ is a Turing Machine and } M \text{ halts on input } w \}$$

---

### 2. Why is the Halting Problem Significant?
- Proved by **Alan Turing in 1936**, the Halting Problem was the first problem mathematically proven to be **UNDECIDABLE**.
- It proves that there are well-defined algorithmic questions that **no computer program can ever solve**, regardless of memory or CPU power.

---

### 3. Step-by-Step Proof of Undecidability (Proof by Contradiction)

#### Step 1: Assume a decider exists
Assume that there exists a Turing Machine $H$ that decides the Halting Problem.  
Since $H$ is a decider, it always halts in finite time with an answer:
$$H(\langle M, w \rangle) = \begin{cases} 
\text{Accept} & \text{if } M \text{ halts on input } w \\
\text{Reject} & \text{if } M \text{ loops forever on input } w 
\end{cases}$$

#### Step 2: Construct the Inverting Machine $D$
Using $H$ as a subroutine, construct a new Turing Machine $D$ that takes the description of any Turing Machine $\langle M \rangle$ as input:
1. $D$ runs $H$ on the input $\langle M, \langle M \rangle \rangle$ (asking: *"Does $M$ halt on its own code?"*).
2. $D$ inverts the outcome of $H$:
   - If $H$ outputs **Accept** ($M$ halts on $\langle M \rangle$), then $D$ **enters an infinite loop**.
   - If $H$ outputs **Reject** ($M$ loops on $\langle M \rangle$), then $D$ **halts and accepts**.

#### Step 3: Self-Reference & Contradiction
Now feed machine $D$ its own description $\langle D \rangle$ as input:
$$D(\langle D \rangle) = \begin{cases} 
\text{loops forever} & \text{if } D \text{ halts on } \langle D \rangle \\
\text{halts} & \text{if } D \text{ loops on } \langle D \rangle 
\end{cases}$$

This gives an outright contradiction:
- $D$ halts on $\langle D \rangle \iff D$ loops forever on $\langle D \rangle$.

Because this is a logical impossibility ($P \iff \neg P$), the assumption that the decider $H$ exists must be false.

---

### 4. Conclusion
The Halting Problem is **undecidable**.  
*(Note: It is, however, **Recursively Enumerable (Turing-recognizable)**, because we can simulate $M$ on $w$; if $M$ halts, our simulator halts and accepts. But if $M$ loops, the simulator loops forever).*"""

if __name__ == "__main__":
    update_year_solutions(2021, SOLUTIONS_2021)
