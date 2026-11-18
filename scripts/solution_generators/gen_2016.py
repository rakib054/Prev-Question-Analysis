import sys
from pathlib import Path
from apply_solutions import update_year_solutions

SOLUTIONS_2016 = {}

# -----------------------------------------------------------------------------
# toc-2016-q6a (25 marks)
# Consider the following grammar:
# S -> AACD
# A -> aAb | eps
# C -> aC | a
# D -> aDa | bDb | eps
# - (i) Eliminate eps-production.
# - (ii) Eliminate unit production.
# - (iii) Eliminate Useless symbols
# - (iv) Put the grammar in CNF
# -----------------------------------------------------------------------------
SOLUTIONS_2016["toc-2016-q6a"] = r"""### Problem Overview
We are given the context-free grammar:
$$\begin{aligned}
S &\to AACD \\
A &\to aAb \mid \varepsilon \\
C &\to aC \mid a \\
D &\to aDa \mid bDb \mid \varepsilon
\end{aligned}$$
*(Variables: $S, A, C, D$; Terminals: $a, b$)*

We simplify and convert this grammar to Chomsky Normal Form (CNF) in the safe, canonical order.

---

### Step (i): Eliminate $\varepsilon$-Productions

1. **Find all nullable variables:**
   - $A \to \varepsilon \implies A$ is nullable.
   - $D \to \varepsilon \implies D$ is nullable.
   - $C$ produces $aC \mid a$, containing terminal $a$, so $C$ is not nullable.
   - $S \to AACD$. Even when $A$ and $D$ are dropped, $C$ remains, so $S$ is not nullable.
   - **Nullable variables:** $\{A, D\}$.

2. **Form new productions without $\varepsilon$:**
   - **For $A \to aAb \mid \varepsilon$:**
     Drop $\varepsilon \implies A \to aAb \mid ab$.
   - **For $C \to aC \mid a$:**
     Remains $C \to aC \mid a$.
   - **For $D \to aDa \mid bDb \mid \varepsilon$:**
     Drop $\varepsilon \implies D \to aDa \mid aa \mid bDb \mid bb$.
   - **For $S \to AACD$:**
     Both $A$'s and $D$ are nullable. We take all combinations of keeping/dropping them (leaving $C$ always present):
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
Identify all unit productions $X \to Y$ ($X, Y \in V$):
- Unit pair: $(S, C)$ from $S \to C$.
- Replace $S \to C$ with non-unit productions of $C$ ($aC \mid a$):
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
1. **Generating Symbols:**
   - $C \to a \implies C$ is generating.
   - $A \to ab \implies A$ is generating.
   - $D \to aa \implies D$ is generating.
   - $S \to a \implies S$ is generating.
   - All symbols $\{S, A, C, D\}$ are generating.
2. **Reachable Symbols:**
   - $S$ reaches $A, C, D$ through $AACD$.
   - All symbols are reachable.
   - No useless symbols exist in this grammar.

---

### Step (iv): Put the Grammar in Chomsky Normal Form (CNF)
In CNF, rules must be $X \to YZ$ or $X \to x$.

1. **Variables for terminals:**
   - $X_a \to a$
   - $X_b \to b$

2. **Replace terminals in composite bodies:**
   - $S \to a \implies$ valid CNF.
   - $S \to AC \mid CD \implies$ valid CNF.
   - $S \to aC \implies S \to X_a C$
   - $C \to a \implies$ valid CNF.
   - $C \to aC \implies C \to X_a C$
   - $A \to ab \implies A \to X_a X_b$
   - $D \to aa \implies D \to X_a X_a$
   - $D \to bb \implies D \to X_b X_b$

3. **Break long bodies (length $\ge 3$) into pairs:**
   - $S \to AAC \implies S \to A Y_1$ where $Y_1 \to AC$
   - $S \to ACD \implies S \to A Y_2$ where $Y_2 \to CD$
   - $S \to AACD \implies S \to A Y_3$ where $Y_3 \to A Y_2$
   - $A \to aAb \implies A \to X_a Y_4$ where $Y_4 \to A X_b$
   - $D \to aDa \implies D \to X_a Y_5$ where $Y_5 \to D X_a$
   - $D \to bDb \implies D \to X_b Y_6$ where $Y_6 \to D X_b$

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
# toc-2016-q7a (6 marks)
# State pumping lemma for CFL's and its advantages
# -----------------------------------------------------------------------------
SOLUTIONS_2016["toc-2016-q7a"] = r"""### 1. Statement of the Pumping Lemma for CFLs
If $L$ is a Context-Free Language, then there exists a constant $p \ge 1$ (called the **pumping length**) such that any string $s \in L$ with length $|s| \ge p$ can be written as:
$$s = uvwxy$$
satisfying the following three conditions:
1. **Length condition:** $|vwx| \le p$
2. **Non-empty pump condition:** $|vx| \ge 1$ (at least one of $v$ or $x$ is non-empty)
3. **Pumping property:** For all integers $k \ge 0$:
   $$u v^k w x^k y \in L$$

---

### 2. Advantages & Uses of the Pumping Lemma
1. **Primary Tool for Disproving Context-Freeness:**
   It is the standard, definitive mathematical tool used to **prove that a given language is NOT context-free** (by contradiction).
2. **Establishing Theoretical Boundaries of Computation:**
   It demonstrates the inherent physical limitations of a Pushdown Automaton (PDA). Because a PDA has only one stack, it can only compare or count two independent blocks of symbols simultaneously; it cannot recognize languages requiring three or more correlated counts (such as $\{a^n b^n c^n\}$) or non-nested string duplications (such as $\{ww\}$).
3. **Simplifies Language Classification:**
   Provides an algorithmic template (proof by contradiction) to classify languages rigorously within the Chomsky Hierarchy.
4. **Helps in Compiler Design:**
   Shows language designers which programming language syntax constructs can be parsed by context-free parsers (LR/LL parsers) and which semantic checks (such as type-checking and variable declaration before use, which resemble $\{ww\}$) must be deferred to the semantic analysis phase."""

# -----------------------------------------------------------------------------
# toc-2016-q7b (12 marks)
# Use pumping lemma to show the following:
# (i) a^n b^m c^p is context free for n >= 0, m >= 0 and p = n.
# (ii) a^n b^m c^p is not context free for n >= 0, m = 2n and p = m + n.
# -----------------------------------------------------------------------------
SOLUTIONS_2016["toc-2016-q7b"] = r"""### Part (i): Analysis of $L_1 = \{a^n b^m c^p \mid n \ge 0, m \ge 0, p = n\}$

#### Note on Proof Technique:
The Pumping Lemma is a property that all context-free languages possess; therefore, it is used to prove a language is **NOT** context-free.  
To prove that $L_1 = \{a^n b^m c^n \mid n \ge 0, m \ge 0\}$ **IS context-free**, we construct an explicit **Context-Free Grammar (CFG)**:
$$\begin{aligned}
S &\to aSc \mid B \\
B &\to bB \mid \epsilon
\end{aligned}$$
- $S \Rightarrow^n a^n S c^n \Rightarrow a^n B c^n \Rightarrow^m a^n b^m c^n$.
- Because an unambiguous CFG exists for $L_1$, **$L_1$ is a Context-Free Language**.

#### Pumping Lemma Verification:
For any string $s = a^n b^m c^n$ with length $\ge p$:
- If $m \ge 1$: choose $v = \epsilon, w = b, x = b$ (pump the $b$'s without changing $n$).
- If $m = 0$: choose $v = a, w = \epsilon, x = c$ (pump $a$ and $c$ synchronously).  
In both cases, $u v^k w x^k y \in L_1$ for all $k \ge 0$, showing the lemma holds.

---

### Part (ii): Prove $L_2 = \{a^n b^m c^p \mid n \ge 0, m = 2n, p = m + n\}$ is NOT Context-Free

#### 1. Language Formulation:
Substitute $m = 2n$ and $p = 2n + n = 3n$:
$$L_2 = \{a^n b^{2n} c^{3n} \mid n \ge 0\}$$

#### 2. Proof by Contradiction Using Pumping Lemma:
1. Assume $L_2$ is a CFL. Let $p$ be its pumping length.
2. Select string $s = a^p b^{2p} c^{3p} \in L_2$. Length $|s| = 6p \ge p$.
3. Any decomposition $s = uvwxy$ satisfies:
   - $|vwx| \le p$
   - $|vx| \ge 1$
   - $u v^k w x^k y \in L_2$ for all $k \ge 0$.
4. **Position of $vwx$:**
   Since $|vwx| \le p$, and the middle block $b^{2p}$ has length $2p > p$, the substring $vwx$ **cannot contain both $a$'s and $c$'s**.
   Therefore, $vx$ can contain symbols from at most two of the three sets $\{a, b, c\}$.
5. **Pumping with $k = 2$:**
   - If $vx$ contains only $a$'s and/or $b$'s: The count of $c$'s remains strictly $3p$. If $a$'s increase to $n' > p$, then $c$'s should be $3n' > 3p$, but the string only has $3p$ $c$'s. Thus $s' \notin L_2$.
   - If $vx$ contains only $b$'s and/or $c$'s: The count of $a$'s remains strictly $p$. But $|vx| \ge 1$ means $b$'s or $c$'s increased, breaking the ratio $2p : 3p$. Thus $s' \notin L_2$.
   - In all cases, $s' = uv^2wx^2y \notin L_2$.

#### Conclusion:
By contradiction, $L_2 = \{a^n b^{2n} c^{3n} \mid n \ge 0\}$ is **NOT context-free**."""

# -----------------------------------------------------------------------------
# toc-2016-q7d (7 marks)
# Explain the halting problem of Turing Machine (TM).
# -----------------------------------------------------------------------------
SOLUTIONS_2016["toc-2016-q7d"] = r"""### 1. The Halting Problem Explained
The **Halting Problem** is a foundational decision problem in computer science:
> *"Given an arbitrary Turing Machine $M$ and an arbitrary input string $w$, can a computer program determine whether $M$ will eventually halt on $w$, or loop forever?"*

Formally:
$$HALT_{TM} = \{ \langle M, w \rangle \mid M \text{ is a TM that halts on input } w \}$$

**Verdict:** The Halting Problem is **UNDECIDABLE** (proven by Alan Turing in 1936).

---

### 2. Proof of Undecidability (Proof by Contradiction)
1. **Assume a decider $H$ exists:**
   $$H(\langle M, w \rangle) = \begin{cases} \text{Accept} & \text{if } M \text{ halts on } w \\ \text{Reject} & \text{if } M \text{ loops on } w \end{cases}$$
2. **Construct an inverting machine $D$:**
   Given input $\langle M \rangle$:
   - Run $H$ on $\langle M, \langle M \rangle \rangle$.
   - If $H$ outputs **Accept**, $D$ enters an **infinite loop**.
   - If $H$ outputs **Reject**, $D$ **halts and accepts**.
3. **Run $D$ on its own description $\langle D \rangle$:**
   - If $D$ halts on $\langle D \rangle \implies D$ loops forever on $\langle D \rangle$.
   - If $D$ loops on $\langle D \rangle \implies D$ halts on $\langle D \rangle$.
4. This yields the logical impossibility:
   $$\text{"}D \text{ halts on } \langle D \rangle \iff D \text{ does not halt on } \langle D \rangle\text{"}$$

**Conclusion:** Our initial assumption is false. Decider $H$ cannot exist, and the Halting Problem is **undecidable**."""

# -----------------------------------------------------------------------------
# toc-2016-q8a (5 marks)
# What is meant by a Turing Machine (TM) with two way infinite tape?
# Give example(s).
# -----------------------------------------------------------------------------
SOLUTIONS_2016["toc-2016-q8a"] = r"""### 1. Definition of Two-Way Infinite Tape TM
A standard Turing Machine has a **one-way infinite tape** (cells indexed $0, 1, 2, \dots$ extending infinitely to the right).

In a **Two-Way Infinite Tape Turing Machine**:
- The tape extends **infinitely in BOTH directions**:
  $$\dots, -3, -2, -1, 0, 1, 2, 3, \dots$$
- There is no leftmost cell and no left-end barrier. The head can move left indefinitely without stopping.
- The input string $w = w_1 \dots w_n$ is initially placed in cells $0$ to $n-1$. All cells to the left and right are blank ($B$).

---

### 2. Equivalence to Standard TM
A two-way infinite tape TM has the **exact same computational power** as a standard one-way infinite tape TM:
- A standard one-way tape can simulate a two-way tape using **two tracks**:
  - Track 1 represents non-negative cells $0, 1, 2, \dots$
  - Track 2 represents negative cells $-1, -2, -3, \dots$
- Any language recognized by a two-way infinite TM is Recursively Enumerable.

---

### 3. Examples
- **Bilateral integer operations:** Adding or subtracting values that cross zero into negative ranges.
- **Symmetric scanning:** Inspecting palindromes from the center outwards into positive and negative directions."""

# -----------------------------------------------------------------------------
# toc-2016-q8b (14 marks)
# Design a Turing Machine (TM) to implement the function "multiplication"
# using the subroutine copy. Simulate the action for the input 001000.
# -----------------------------------------------------------------------------
SOLUTIONS_2016["toc-2016-q8b"] = r"""### 1. Problem Formulation
Design a Turing Machine $M$ to compute unary integer multiplication:
$$f(m, n) = m \times n$$
- **Input Format:** $0^m 1 0^n 1$ (or $0^m 1 0^n B$).
- **Test Input:** `001000` ($m = 2, n = 3$).
- **Target Output:** $0^{2 \times 3} = 0^6$ (`000000`).

---

### 2. High-Level Algorithm
1. Mark the first unmarked `0` of $m$ with an $X$.
2. Call subroutine `copy`: for each zero of $n$, temporarily mark it as $Y$ and append a `0` to the result area at the right end of the tape.
3. Restore all $Y$'s back to `0`.
4. Return left to the first operand and repeat for the next zero of $m$.
5. When all $m$ zeros are marked $X$, erase the inputs, leaving only the product zeros.

---

### 3. Step-by-Step Simulation on "001000" ($2 \times 3$)
Initial tape: `0010001`

- **Iteration 1 (1st zero of $m=2$):**
  1. $q_0$ marks first zero as $X$: tape becomes $X010001$.
  2. Subroutine `copy` copies the 3 zeros of $n=3$ to the end:
     - Tape becomes $X01YYY1000$
  3. Restores $YYY \to 000$: tape becomes $X010001000$.
  4. Returns left to $q_0$. Current product: $0^3$.

- **Iteration 2 (2nd zero of $m=2$):**
  1. $q_0$ marks second zero as $X$: tape becomes $XX10001000$.
  2. Subroutine `copy` copies the 3 zeros of $n$ again to the end:
     - Tape becomes $XX1YYY1000000$
  3. Restores $YYY \to 000$: tape becomes $XX10001000000$.
  4. Returns left to $q_0$, positioning head at the separator `1`. Current product: $0^6$.

- **Cleanup:**
  1. Reading `1` in state $q_0$ signals completion.
  2. Erases input block $XX10001$, leaving only:
     $$\mathbf{000000} \quad (\text{exactly } 6 \text{ zeros})$$

**Final Output:** `000000` (representing $2 \times 3 = 6$)."""

# -----------------------------------------------------------------------------
# toc-2016-q8d (6 marks)
# Write the differences between single and multi-tape TM.
# -----------------------------------------------------------------------------
SOLUTIONS_2016["toc-2016-q8d"] = r"""### 1. Differences Between Single and Multi-Tape TM

| Feature | Single-Tape TM | Multi-Tape TM ($k \ge 2$) |
| :--- | :--- | :--- |
| **Number of Tapes** | Exactly 1 tape used for input, output, and scratch work. | $k$ distinct physical tapes (Tape 1 is input; others are scratch tapes). |
| **Heads** | Exactly 1 read/write head. | $k$ distinct read/write heads (one per tape). |
| **Head Movement** | Head moves Left or Right. | Each head moves **independently** ($L, R, \text{or } S$ - Stay). |
| **Transition Function** | $\delta: Q \times \Gamma \to Q \times \Gamma \times \{L, R\}$ | $\delta: Q \times \Gamma^k \to Q \times \Gamma^k \times \{L, R, S\}^k$ |
| **Time Complexity** | Palindrome check $\{ww^R\}$ takes $\Omega(n^2)$ time. | Palindrome check $\{ww^R\}$ takes $O(n)$ **linear time**. |
| **Computational Power** | Recognizes **Recursively Enumerable** languages. | Recognizes **Recursively Enumerable** languages (strictly equivalent power). |"""

if __name__ == "__main__":
    update_year_solutions(2016, SOLUTIONS_2016)
