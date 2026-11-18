import sys
from pathlib import Path
from apply_solutions import update_year_solutions

SOLUTIONS_2020 = {}

# -----------------------------------------------------------------------------
# toc-2020-q4c (4 marks)
# Define NP Hard and NP Complete problems.
# -----------------------------------------------------------------------------
SOLUTIONS_2020["toc-2020-q4c"] = r"""### 1. NP-Hard Problems
A decision problem $H$ is **NP-Hard** if every problem $L$ in the complexity class $NP$ can be reduced to $H$ in polynomial time:
$$\forall L \in NP, \quad L \le_p H$$

#### Key Characteristics:
- An NP-hard problem is **at least as hard as the hardest problems in NP**.
- **Does NOT need to be in NP:** An NP-hard problem does not necessarily have a polynomial-time verifiable certificate, and it does not even need to be decidable (for example, the Halting Problem is NP-hard!).
- If any NP-hard problem could be solved in polynomial time ($P$), then $P = NP$.

---

### 2. NP-Complete Problems
A decision problem $C$ is **NP-Complete** if it satisfies BOTH of the following conditions:
1. **$C \in NP$:** A candidate solution (certificate) can be verified deterministically in **polynomial time** $O(n^k)$.
2. **$C$ is NP-Hard:** Every problem in $NP$ can be reduced to $C$ in polynomial time ($L \le_p C$ for all $L \in NP$).

#### Key Characteristics:
- NP-complete problems are the **hardest problems inside NP**.
- If any NP-complete problem has a polynomial-time algorithm ($C \in P$), then **every problem in NP is in P** ($P = NP$).
- Examples: 3-SAT, Clique, Vertex Cover, Traveling Salesperson (decision version), Hamiltonian Cycle.

---

### 3. Summary Relationship

```
+-------------------------------------------------+
|                    NP-Hard                      |
|  (Includes undecidable problems like Halting)  |
|         +-----------------------------+         |
|         |         NP-Complete         |         |
|         |      (Both in NP & NP-hard) |         |
|         |  +-----------------------+  |         |
|         +--|         NP            |--+         |
|            |    +-------------+    |            |
|            |    |      P      |    |            |
|            |    +-------------+    |            |
|            +-----------------------+            |
+-------------------------------------------------+
```
*(Assuming $P \ne NP$)*"""

# -----------------------------------------------------------------------------
# toc-2020-q5b (15 marks)
# Design a Turing Machine to implement "multiplication." Simulate the action for 001000.
# -----------------------------------------------------------------------------
SOLUTIONS_2020["toc-2020-q5b"] = r"""### 1. Representation & Objective
We design a standard single-tape Turing Machine $M$ to compute unary integer multiplication:
$$f(m, n) = m \times n$$
- **Unary Input Format:** $0^m 1 0^n 1$ (or $0^m 1 0^n B$).
- **Test Input String:** `001000` (representing $m = 2$ and $n = 3$).
- **Target Output:** $0^{2 \times 3} = 0^6$ (`000000`).

---

### 2. Algorithmic Strategy (Repeated Addition)
Multiplication $m \times n$ is computed by copying the $n$ zeros to the result area $m$ times:
1. Scan the first operand ($0^m$):
   - Replace the first unmarked `0` with marker $X$.
2. Travel to the second operand ($0^n$):
   - For each of the $n$ zeros, mark it temporarily as $Y$, move right to the output area, and append a `0`.
   - Restore all $Y$'s back to `0`.
3. Move back left to the next unmarked `0` of the first operand and repeat.
4. When all $m$ zeros have been marked as $X$ (the head encounters `1`), the multiplication is complete.
5. Erase the inputs ($X$'s, $1$'s, and $0^n$), leaving only the output zeros on the tape.

---

### 3. State Breakdown & Transitions
- **$q_0$ (Main Loop):**
  - $\delta(q_0, 0) = (q_1, X, R)$: Mark one zero of $m$, move towards $n$.
  - $\delta(q_0, 1) = (q_{clean}, B, R)$: All $m$ zeros processed, begin cleanup.
- **$q_1$ (Traverse to second operand):**
  - $\delta(q_1, 0) = (q_1, 0, R)$: Skip remaining zeros of $m$.
  - $\delta(q_1, 1) = (q_2, 1, R)$: Pass separator `1`, enter copy loop.
- **$q_2$ (Copy subroutine - find next zero of $n$):**
  - $\delta(q_2, 0) = (q_3, Y, R)$: Mark one zero of $n$ as $Y$, travel right to write a product zero.
  - $\delta(q_2, 1) = (q_5, 1, L)$: End of $n$ reached, start restoring $Y \to 0$.
  - $\delta(q_2, B) = (q_5, B, L)$: (If blank terminates $n$).
- **$q_3$ (Travel Right to Output Area):**
  - $\delta(q_3, 0) = (q_3, 0, R)$
  - $\delta(q_3, 1) = (q_3, 1, R)$
  - $\delta(q_3, B) = (q_4, 0, L)$: Append new product zero, move left.
- **$q_4$ (Return Left to next zero of $n$):**
  - Skip left over $0$'s and $1$'s until reaching marker $Y$: $\delta(q_4, Y) = (q_2, Y, R)$.
- **$q_5$ (Restore $Y \to 0$ and return to $m$):**
  - $\delta(q_5, Y) = (q_5, 0, L)$: Restore each $Y$ back to $0$.
  - $\delta(q_5, 1) = (q_6, 1, L)$: Crossed separator `1`, now moving back through $m$.
- **$q_6$ (Move left to marker $X$):**
  - $\delta(q_6, 0) = (q_6, 0, L)$
  - $\delta(q_6, X) = (q_0, X, R)$: Back at processed zero, step right to start next cycle.
- **$q_{clean}$ (Tape Cleanup):**
  - Erases remaining $0$'s and $1$'s up to the output block, halts in $q_f$.

---

### 4. Step-by-Step Simulation on "001000" ($2 \times 3$)
Initial tape: `0010001` (with blank $B$ after).

- **Cycle 1 (First zero of $m=2$):**
  1. $q_0 0010001 \vdash X q_1 010001 \vdash X0 q_1 10001 \vdash X01 q_2 0001$
  2. First zero of $n$ copied: $X01 Y0010$
  3. Second zero of $n$ copied: $X01 YY0100$
  4. Third zero of $n$ copied: $X01 YYY1000$
  5. Restore $Y \to 0$: tape becomes $X010001000$
  6. Return to $q_0$: head scans second zero of $m$. Output so far: $0^3$.

- **Cycle 2 (Second zero of $m=2$):**
  1. Head marks second zero: tape becomes $XX10001000$
  2. Subroutine copies the 3 zeros of $n$ again to the end:
     - Tape becomes $XX1 YYY1000000$
  3. Restore $Y \to 0$: tape becomes $XX10001000000$
  4. Return to $q_0$: head is at cell 3 scanning `1`.

- **Cycle 3 (Termination & Cleanup):**
  1. In state $q_0$, head reads `1` $\implies$ all zeros of $m$ have been processed!
  2. Enters $q_{clean}$: erases $XX10001$, leaving only the product zeros:
     $$\mathbf{000000} \quad (\text{exactly } 6 \text{ zeros})$$

**Result:** The TM halts with $6$ zeros, correctly computing $2 \times 3 = 6$."""

# -----------------------------------------------------------------------------
# toc-2020-q5c (4 marks)
# What do you mean by Recursive Languages and Recursively Enumerable Languages?
# -----------------------------------------------------------------------------
SOLUTIONS_2020["toc-2020-q5c"] = r"""### 1. Recursive Languages (Decidable Languages)
A language $L$ is **Recursive** (or Turing-Decidable) if there exists a Turing Machine $M$ that **halts on every input string**:
- If $w \in L$, $M$ halts and **accepts**.
- If $w \notin L$, $M$ halts and **rejects**.

Such a Turing Machine is called a **Decider**. It never enters an infinite loop.  
**Properties:** Recursive languages are closed under complement, union, intersection, and concatenation.  
**Example:** $L = \{a^n b^n c^n \mid n \ge 0\}$, any context-free or regular language.

---

### 2. Recursively Enumerable (RE) Languages (Turing-Recognizable)
A language $L$ is **Recursively Enumerable (RE)** (or Turing-Recognizable) if there exists a Turing Machine $M$ that accepts every string belonging to $L$:
- If $w \in L$, $M$ eventually halts and **accepts**.
- If $w \notin L$, $M$ may either halt and **reject**, or **loop forever**.

Such a Turing Machine is called a **Recognizer** (or semi-decider).  
**Properties:** RE languages are closed under union and intersection, but **NOT closed under complementation**.  
**Example:** The Turing Machine Acceptance Problem $A_{TM} = \{\langle M, w \rangle \mid M \text{ accepts } w\}$, and the Halting Problem $HALT_{TM}$.

---

### 3. Key Relationship
$$\text{Regular} \subset \text{Context-Free} \subset \text{Recursive (Decidable)} \subset \text{Recursively Enumerable (RE)}$$
A language $L$ is recursive if and only if both $L$ and its complement $\overline{L}$ are recursively enumerable."""

# -----------------------------------------------------------------------------
# toc-2020-q6a (20 marks)
# Consider the following grammar:
# S -> ABCd
# A -> BC
# B -> bB | eps
# C -> cC | eps
# - i) Eliminate eps-productions.
# - ii) Eliminate unit productions.
# - iii) Put the grammar into Chomsky Normal Form (CNF).
# -----------------------------------------------------------------------------
SOLUTIONS_2020["toc-2020-q6a"] = r"""### Problem Overview
We are given the context-free grammar:
$$\begin{aligned}
S &\to ABCd \\
A &\to BC \\
B &\to bB \mid \epsilon \\
C &\to cC \mid \epsilon
\end{aligned}$$
*(Variables: $S, A, B, C$; Terminals: $b, c, d$)*

---

### Step (i): Eliminate $\epsilon$-Productions

1. **Find all nullable variables:**
   - Directly nullable: $B \to \epsilon \implies B$ is nullable.
   - Directly nullable: $C \to \epsilon \implies C$ is nullable.
   - For $A$: $A \to BC$. Since both $B$ and $C$ are nullable, $A \Rightarrow^* \epsilon \implies A$ is nullable.
   - For $S$: $S \to ABCd$. Because of the trailing terminal $d$, $S$ cannot derive $\epsilon$.
   - **Nullable variables:** $\{A, B, C\}$.

2. **Form new productions without $\epsilon$:**
   Consider all combinations of presence and absence of nullable variables:
   - **For $B \to bB \mid \epsilon$:**
     - Keeping or dropping $B$: $B \to bB \mid b$. (Drop $B \to \epsilon$).
   - **For $C \to cC \mid \epsilon$:**
     - Keeping or dropping $C$: $C \to cC \mid c$. (Drop $C \to \epsilon$).
   - **For $A \to BC$:**
     - Combinations for $B$ and $C$: $BC, B, C$. (Dropping both would yield $\epsilon$, which is omitted).
     - Thus: $A \to BC \mid B \mid C$.
   - **For $S \to ABCd$:**
     - In $ABCd$, the variables $A, B, C$ are all nullable.
     - 3 variables $\implies 2^3 = 8$ combinations:
       - Keep all: $ABCd$
       - Drop one: $BCd, ACd, ABd$
       - Drop two: $Cd, Bd, Ad$
       - Drop all three: $d$
     - Thus:
       $$S \to ABCd \mid ABd \mid ACd \mid BCd \mid Ad \mid Bd \mid Cd \mid d$$

**Grammar after Step (i):**
$$\begin{aligned}
S &\to ABCd \mid ABd \mid ACd \mid BCd \mid Ad \mid Bd \mid Cd \mid d \\
A &\to BC \mid B \mid C \\
B &\to bB \mid b \\
C &\to cC \mid c
\end{aligned}$$

---

### Step (ii): Eliminate Unit Productions
We identify and eliminate all unit productions $X \to Y$ ($X, Y \in V$).

1. **Find unit pairs $(X, Y)$ where $X \Rightarrow^* Y$:**
   - Base: $(S, S), (A, A), (B, B), (C, C)$
   - From $A \to B$ and $A \to C$: unit pairs $(A, B)$ and $(A, C)$.
   - $S, B, C$ have no unit productions to other variables.

2. **Replace unit productions with non-unit productions:**
   - **For $B$:** Non-unit productions:
     $$B \to bB \mid b$$
   - **For $C$:** Non-unit productions:
     $$C \to cC \mid c$$
   - **For $A$:** Non-unit productions from $(A, A), (A, B), (A, C)$:
     $$A \to BC \mid bB \mid b \mid cC \mid c$$
   - **For $S$:**
     $$S \to ABCd \mid ABd \mid ACd \mid BCd \mid Ad \mid Bd \mid Cd \mid d$$

*(Note: Check useless symbols: All variables are generating and reachable from $S$. No useless symbols exist).*

---

### Step (iii): Put the Grammar into Chomsky Normal Form (CNF)
In CNF, rules must be $X \to YZ$ or $X \to x$.

1. **Introduce variables for terminals:**
   - $X_b \to b$ (or note $B \to b$)
   - $X_c \to c$ (or note $C \to c$)
   - $X_d \to d$

2. **Rewrite productions using variable substitutions:**
   - **For $B$:**
     - $B \to bB \implies B \to X_b B$
     - $B \to b$ (already in CNF!)
   - **For $C$:**
     - $C \to cC \implies C \to X_c C$
     - $C \to c$ (already in CNF!)
   - **For $A$:**
     - $A \to BC$ (already in CNF!)
     - $A \to X_b B \mid b \mid X_c C \mid c$
   - **For $S$:**
     - $S \to d$ (already in CNF!)
     - $S \to Ad \implies S \to A X_d$
     - $S \to Bd \implies S \to B X_d$
     - $S \to Cd \implies S \to C X_d$

3. **Break bodies of length $\ge 3$ into binary pairs:**
   - **$S \to BCd$:** $S \to B Y_1$ where $Y_1 \to C X_d$
   - **$S \to ABd$:** $S \to A Y_2$ where $Y_2 \to B X_d$
   - **$S \to ACd$:** $S \to A Y_3$ where $Y_3 \to C X_d$ (note $Y_3 = Y_1$)
   - **$S \to ABCd$:** $S \to A Y_4$ where $Y_4 \to B Y_1$

---

### Final CNF Grammar
$$\begin{aligned}
S &\to A Y_4 \mid A Y_2 \mid A Y_1 \mid B Y_1 \mid A X_d \mid B X_d \mid C X_d \mid d \\
Y_4 &\to B Y_1 \\
Y_2 &\to B X_d \\
Y_1 &\to C X_d \\
A &\to BC \mid X_b B \mid b \mid X_c C \mid c \\
B &\to X_b B \mid b \\
C &\to X_c C \mid c \\
X_b &\to b \\
X_c &\to c \\
X_d &\to d
\end{aligned}$$"""

# -----------------------------------------------------------------------------
# toc-2020-q6b (10 marks)
# Using pumping lemma, show that the following language is not context-free.
# L = {a^i b^j c^k | i < j < k}
# -----------------------------------------------------------------------------
SOLUTIONS_2020["toc-2020-q6b"] = r"""### 1. Statement of the Pumping Lemma for CFLs
If $L$ is context-free, there exists a pumping length $p \ge 1$ such that any string $s \in L$ with $|s| \ge p$ can be written as:
$$s = uvwxy$$
satisfying:
1. $|vwx| \le p$
2. $|vx| \ge 1$
3. $u v^m w x^m y \in L$ for all $m \ge 0$.

---

### 2. Step-by-Step Proof by Contradiction

#### Step 1: Assume $L$ is context-free
Assume, for contradiction, that $L = \{a^i b^j c^k \mid i < j < k\}$ is a CFL.  
Let $p$ be its pumping length.

#### Step 2: Select a test string $s \in L$
Choose the string:
$$s = a^p b^{p+1} c^{p+2}$$
- Number of $a$'s: $i = p$
- Number of $b$'s: $j = p + 1$
- Number of $c$'s: $k = p + 2$
- Since $p < p+1 < p+2$, the condition $i < j < k$ holds, so $s \in L$.
- Length: $|s| = 3p + 3 \ge p$.

#### Step 3: Analyze the decomposition $s = uvwxy$
By Condition 1, $|vwx| \le p$.  
This restriction means that $vwx$ can span a window of at most $p$ consecutive characters.  
Crucially, **$vwx$ cannot contain both $a$'s and $c$'s**, because the block of $b$'s separating them has length $p + 1 > p$.  
Thus, $vx$ can contain at most two different types of symbols (either only $a$'s, $a$'s and $b$'s, only $b$'s, $b$'s and $c$'s, or only $c$'s).

#### Step 4: Case Analysis

- **Case 1: $vx$ contains no $c$'s (it contains only $a$'s and/or $b$'s):**
  - If $vx$ has at least one $a$:
    Pump UP with $m = 2$: the number of $a$'s increases by at least 1. If we pump with $m = 3$ (or sufficiently large $m$), the number of $a$'s increases by at least 2, making $i' \ge p + 2$. But the number of $c$'s remains strictly $k = p + 2$.  
    Then $i' \ge k$, violating $i < k$!
  - If $vx$ has at least one $b$ and no $a$'s:
    Pump with $m = 2$: the number of $b$'s becomes $j' \ge (p + 1) + 1 = p + 2$. But $k = p + 2$.  
    Then $j' \ge k$, violating $j < k$!
  - In either scenario, the pumped string is NOT in $L$.

- **Case 2: $vx$ contains no $a$'s (it contains only $b$'s and/or $c$'s):**
  - Pump DOWN with $m = 0$ ($s' = uwy$):
  - At least one $b$ or $c$ is removed.
  - If $vx$ contains at least one $c$: the number of $c$'s decreases by at least 1, so $k' \le (p + 2) - 1 = p + 1$.  
    Meanwhile, the number of $b$'s is either $p + 1$ (if no $b$'s in $vx$) or fewer. If no $b$'s were removed, $j' = p + 1 \ge k'$, violating $j < k$!
  - If $vx$ contains at least one $b$: the number of $b$'s decreases, so $j' \le p$. But the number of $a$'s remains $i = p$.  
    Then $i \ge j'$, violating $i < j$!
  - Thus $s' \notin L$.

- **Case 3: $vx$ contains only $b$'s:**
  - Covered in Cases 1 and 2: pumping $m=2$ makes $j' \ge k$, and pumping $m=0$ makes $j' \le i$.

---

### 3. Conclusion
In every possible case, pumping either $m=0$ or $m=2$ produces a string $s' \notin L$.  
This contradicts the Pumping Lemma. Therefore, $L = \{a^i b^j c^k \mid i < j < k\}$ is **NOT a context-free language**."""

if __name__ == "__main__":
    update_year_solutions(2020, SOLUTIONS_2020)
