import sys
from pathlib import Path
from apply_solutions import update_year_solutions

SOLUTIONS_2019 = {}

# -----------------------------------------------------------------------------
# toc-2019-q7a (25 marks)
# Consider the following grammar:
# S -> aAa | bBb | eps
# A -> C | a
# B -> C | b
# C -> CDE | eps
# D -> A | B | ab
# - i) Are there any useless symbols? Eliminate them if so.
# - ii) Eliminate eps-productions.
# - iii) Eliminate unit productions.
# - iv) Put the grammar into CNF.
# -----------------------------------------------------------------------------
SOLUTIONS_2019["toc-2019-q7a"] = r"""### Problem Overview
We are given the context-free grammar:
$$\begin{aligned}
S &\to aAa \mid bBb \mid \epsilon \\
A &\to C \mid a \\
B &\to C \mid b \\
C &\to CDE \mid \epsilon \\
D &\to A \mid B \mid ab
\end{aligned}$$
*(Variables: $S, A, B, C, D, E$; Terminals: $a, b$. Note that variable $E$ has no production rules).*

---

### Step (i): Are There Any Useless Symbols? Eliminate Them If So.
A symbol is useful if it is both **generating** (can derive a string of terminals) and **reachable** (can be reached from $S$).

1. **Check Generating Symbols in the initial grammar:**
   - Terminals: $\{a, b\}$.
   - $E$ has NO production rules at all! Thus, $E$ can never derive any terminal string. **$E$ is non-generating.**
   - Since $E$ is non-generating, any production containing $E$ cannot derive a terminal string. Thus, rule $C \to CDE$ cannot generate terminals.
   - However, $C \to \epsilon$ is a terminal derivation (since $\epsilon$ is a string of terminals of length 0). So in the initial grammar, $C \Rightarrow \epsilon$ is generating.
   - $A \to a \implies A$ is generating.
   - $B \to b \implies B$ is generating.
   - $D \to ab \implies D$ is generating.
   - $S \to \epsilon \implies S$ is generating.
   - Therefore, the only non-generating symbol in the initial grammar is **$E$**.
   - Eliminating $E$ removes the rule $C \to CDE$.

2. **Check Reachability:**
   - All symbols $\{S, A, B, C, D\}$ can be reached from $S$ via $S \to aAa$ and $A \to C$, etc.
   - Result after removing non-generating symbol $E$:
     $$\begin{aligned}
     S &\to aAa \mid bBb \mid \epsilon \\
     A &\to C \mid a \\
     B &\to C \mid b \\
     C &\to \epsilon \\
     D &\to A \mid B \mid ab
     \end{aligned}$$

---

### Step (ii): Eliminate $\epsilon$-Productions

1. **Identify all nullable variables:**
   - Directly nullable: $S \to \epsilon$, $C \to \epsilon \implies \{S, C\}$
   - Since $C$ is nullable and $A \to C, B \to C \implies \{S, C, A, B\}$
   - Since $A$ and $B$ are nullable and $D \to A \mid B \implies \{S, C, A, B, D\}$
   - All variables $\{S, A, B, C, D\}$ are nullable.

2. **Form new productions without $\epsilon$:**
   - **For $C \to \epsilon$:** Dropping $\epsilon$ leaves $C$ with no productions!
   - **For $A \to C \mid a$:** $A \to C \mid a$
   - **For $B \to C \mid b$:** $B \to C \mid b$
   - **For $D \to A \mid B \mid ab$:** $D \to A \mid B \mid ab$
   - **For $S \to aAa \mid bBb$:**
     - From $aAa$: $aAa \mid aa$
     - From $bBb$: $bBb \mid bb$
     - Thus: $S \to aAa \mid aa \mid bBb \mid bb$

**Grammar after Step (ii):**
$$\begin{aligned}
S &\to aAa \mid aa \mid bBb \mid bb \\
A &\to C \mid a \\
B &\to C \mid b \\
D &\to A \mid B \mid ab
\end{aligned}$$
*(Notice that variable $C$ now has NO productions, making it non-generating. When removing $C$, unit rules $A \to C$ and $B \to C$ vanish).*

---

### Step (iii): Eliminate Unit Productions
Identify all unit pairs $(X, Y)$ where $X \Rightarrow^* Y$:
- $(S, S), (A, A), (B, B), (D, D)$
- From $D \to A, D \to B$: pairs $(D, A)$ and $(D, B)$
- $S, A, B$ have no unit productions to other active variables.

Replace unit productions with non-unit productions:
- **For $A$:** $A \to a$
- **For $B$:** $B \to b$
- **For $D$:** Inherits from $D \to A$ (giving $a$) and $D \to B$ (giving $b$):
  $$D \to a \mid b \mid ab$$
- **For $S$:**
  $$S \to aAa \mid aa \mid bBb \mid bb$$

*(Useless symbol cleanup: Variable $D$ is now completely unreachable from $S$, so $D$ is safely eliminated).*

**Grammar after Step (iii):**
$$\begin{aligned}
S &\to aAa \mid aa \mid bBb \mid bb \\
A &\to a \\
B &\to b
\end{aligned}$$

---

### Step (iv): Put the Grammar into Chomsky Normal Form (CNF)

1. **Introduce variables for terminals:**
   - Let $X_a \to a$
   - Let $X_b \to b$
   *(Note that existing variables $A \to a$ and $B \to b$ already serve as variables for $a$ and $b$!).*

2. **Convert rules of $S$:**
   - $S \to aa \implies S \to X_a X_a$ (or $A A$)
   - $S \to bb \implies S \to X_b X_b$ (or $B B$)
   - $S \to aAa \implies S \to X_a Y_1$ where $Y_1 \to A X_a$
   - $S \to bBb \implies S \to X_b Y_2$ where $Y_2 \to B X_b$

---

### Final CNF Grammar
$$\begin{aligned}
S &\to X_a Y_1 \mid X_a X_a \mid X_b Y_2 \mid X_b X_b \\
Y_1 &\to A X_a \\
Y_2 &\to B X_b \\
A &\to a \\
B &\to b \\
X_a &\to a \\
X_b &\to b
\end{aligned}$$
*(If including $\epsilon \in L(G)$, add $S_0 \to S \mid \epsilon$)*."""

# -----------------------------------------------------------------------------
# toc-2019-q7b (10 marks)
# Show that the language L = {a^n b^j c^k | k = jn} on \Sigma = {a, b, c}
# is not context-free.
# -----------------------------------------------------------------------------
SOLUTIONS_2019["toc-2019-q7b"] = r"""### 1. Understanding the Language
Given:
$$L = \{a^n b^j c^k \mid k = j \cdot n, \text{ with } n, j, k \ge 0\}$$
In this language, the number of $c$'s must equal the **product** of the number of $a$'s and the number of $b$'s:
$$\#_c = \#_a \times \#_b$$
Because a pushdown automaton's single stack cannot perform multiplication between two arbitrary counts, we intuitively expect $L$ to be non-context-free. We prove this rigorously using the Pumping Lemma for CFLs.

---

### 2. Step-by-Step Proof Using Pumping Lemma

#### Step 1: Assume $L$ is context-free
Assume, for contradiction, that $L$ is a CFL.  
Let $p \ge 1$ be the pumping length guaranteed by the Pumping Lemma.

#### Step 2: Choose a test string $s \in L$
Select:
$$s = a^p b^p c^{p^2}$$
- Number of $a$'s: $n = p$
- Number of $b$'s: $j = p$
- Number of $c$'s: $k = p \cdot p = p^2$
- Since $k = j \cdot n$, $s \in L$.
- Length: $|s| = 2p + p^2 \ge p$.

#### Step 3: Properties of decomposition $s = uvwxy$
By the Pumping Lemma:
1. $|vwx| \le p$
2. $|vx| \ge 1$
3. $u v^i w x^i y \in L$ for all $i \ge 0$.

Because $|vwx| \le p$, the substring $vwx$ can span a window of at most $p$ consecutive symbols.  
Since the block of $b$'s has length $p$, **$vwx$ cannot contain both $a$'s and $c$'s simultaneously**!

#### Step 4: Case Analysis on $vwx$

- **Case 1: $vwx$ contains no $c$'s (it lies entirely within $a^p b^p$):**
  - Then $vx$ consists of some $a$'s and/or $b$'s ($|vx| \ge 1$).
  - Pump UP with $i = 2$: the new string $s' = uv^2wx^2y$ has $n' \ge p$ and $j' \ge p$, with at least one strictly greater ($n' > p$ or $j' > p$).
  - The required number of $c$'s for $s'$ to belong to $L$ is $n' \cdot j' > p \cdot p = p^2$.
  - But the number of $c$'s in $s'$ is **unchanged** (still $p^2$).
  - Therefore, $\#_c(s') = p^2 < n' \cdot j'$, so $s' \notin L$.

- **Case 2: $vwx$ contains only $c$'s:**
  - Then $vx = c^m$ where $1 \le m \le p$.
  - Pump UP with $i = 2$: the string $s'$ has $p$ $a$'s, $p$ $b$'s, and $p^2 + m$ $c$'s.
  - For $s' \in L$, we must have $\#_c(s') = p \times p = p^2$.  
    However, $p^2 + m \ne p^2$ because $m \ge 1$.
  - Hence, $s' \notin L$.

- **Case 3: $vwx$ spans the boundary between $b^p$ and $c^{p^2}$:**
  - Then $vx$ contains some $b$'s (say $m_b \ge 0$) and some $c$'s (say $m_c \ge 0$), with $m_b + m_c \ge 1$ and $m_b + m_c \le p$.  
    Crucially, it contains **no $a$'s**, so the count of $a$'s remains strictly $n = p$.
  - Pump UP with $i = 2$:
    - The new number of $b$'s is $j' = p + m_b$.
    - The new number of $c$'s is $k' = p^2 + m_c$.
  - For $s' \in L$, the relationship $k' = n \cdot j'$ must hold:
    $$p^2 + m_c = p(p + m_b) = p^2 + p \cdot m_b \implies m_c = p \cdot m_b$$
  - If $m_b = 0$, then $m_c = 0$, but $|vx| = m_b + m_c \ge 1$, which is impossible.
  - If $m_b \ge 1$, then $m_c = p \cdot m_b \ge p$.
  - But from $|vwx| \le p$, we know $m_b + m_c \le p$. If $m_b \ge 1$ and $m_c \ge p$, then $m_b + m_c \ge 1 + p > p$, a direct contradiction!
  - Therefore, $m_c \ne p \cdot m_b$, so $s' \notin L$.

---

### 3. Conclusion
In every possible case, the pumped string $s' \notin L$.  
By contradiction, the language $L = \{a^n b^j c^k \mid k = jn\}$ is **NOT context-free**."""

# -----------------------------------------------------------------------------
# toc-2019-q8a (14 marks)
# Design a Turing Machine (TM) to implement the function "multiplication".
# Simulate the action for the input 001000.
# -----------------------------------------------------------------------------
SOLUTIONS_2019["toc-2019-q8a"] = r"""### 1. Problem Formulation
Design a Turing Machine to compute unary integer multiplication:
$$f(m, n) = m \times n$$
- **Unary Encoding:** Integer $k$ is represented as $0^k$.
- **Input on Tape:** $0^m 1 0^n 1$ (or $0^m 1 0^n B$).
- **Test Input String:** `001000` ($m = 2, n = 3$).
- **Expected Output:** $0^{2 \times 3} = 0^6$ (`000000`).

---

### 2. High-Level Algorithm
Multiplication is repeated addition. We add $n$ zeros to the result area $m$ times:
1. Scan the first operand: replace one `0` with marker $X$.
2. Travel to the second operand: for each `0`, mark it as $Y$, travel to the end of the tape, and write a `0`.
3. Restore all $Y$'s back to `0`.
4. Return to the first operand and repeat for the next `0`.
5. When all $m$ zeros have been marked $X$, erase the inputs and leave only the $m \times n$ product zeros.

---

### 3. Transition Function Table ($\delta$)

| State | Symbol `0` | Symbol `1` | Marker `X` | Marker `Y` | Blank `B` |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **$q_0$ (Pick 0 of $m$)** | $(q_1, X, R)$ | $(q_{clean}, B, R)$ | — | — | — |
| **$q_1$ (Seek operand $n$)** | $(q_1, 0, R)$ | $(q_2, 1, R)$ | — | — | — |
| **$q_2$ (Pick 0 of $n$)** | $(q_3, Y, R)$ | $(q_5, 1, L)$ | — | — | $(q_5, B, L)$ |
| **$q_3$ (Travel Right)** | $(q_3, 0, R)$ | $(q_3, 1, R)$ | — | — | $(q_4, 0, L)$ |
| **$q_4$ (Seek left to $Y$)** | $(q_4, 0, L)$ | $(q_4, 1, L)$ | — | $(q_2, Y, R)$ | — |
| **$q_5$ (Restore $Y \to 0$)** | — | $(q_6, 1, L)$ | — | $(q_5, 0, L)$ | — |
| **$q_6$ (Seek left to $X$)** | $(q_6, 0, L)$ | $(q_6, 1, L)$ | $(q_0, X, R)$ | — | — |
| **$q_{clean}$ (Erase input)** | $(q_{clean}, B, R)$ | $(q_{clean}, B, R)$ | $(q_{clean}, B, R)$ | — | $(q_f, B, S)$ |

---

### 4. Step-by-Step Simulation on "001000" ($2 \times 3$)
Initial tape: `0010001`

- **Iteration 1 (First zero of $m=2$):**
  1. $q_0 0010001 \vdash X q_1 010001 \vdash X0 q_1 10001 \vdash X01 q_2 0001$
  2. First zero of $n$ marked $Y \implies$ appends 0 at end: tape becomes $X01Y0010$
  3. Second zero of $n$ marked $Y \implies$ appends 0 at end: tape becomes $X01YY0100$
  4. Third zero of $n$ marked $Y \implies$ appends 0 at end: tape becomes $X01YYY1000$
  5. In $q_2$, reads `1` $\implies$ all 3 zeros of $n$ copied.
  6. $q_5$ restores $YYY \to 000$: tape becomes $X010001000$.
  7. $q_6$ moves left to $X$, steps right, enters $q_0$ at the second zero of $m$.

- **Iteration 2 (Second zero of $m=2$):**
  1. $X q_0 010001000 \vdash XX q_1 10001000 \vdash XX1 q_2 0001000$
  2. The 3 zeros of $n$ are copied one by one to the end:
     - Tape becomes $XX1YYY1000000$
  3. $q_5$ restores $YYY \to 000$: tape becomes $XX10001000000$.
  4. $q_6$ moves left to $XX$, steps right, enters $q_0$ scanning `1`.

- **Termination & Tape Cleanup:**
  1. In $q_0$, reading `1` signals that all $m$ zeros are processed.
  2. Enters $q_{clean}$: clears the prefix $XX10001$, leaving:
     $$\mathbf{000000} \quad (\text{exactly } 6 \text{ zeros})$$

**Output:** `000000` (representing $2 \times 3 = 6$)."""

# -----------------------------------------------------------------------------
# toc-2019-q8b (7 marks)
# Explain the halting problem of TM.
# -----------------------------------------------------------------------------
SOLUTIONS_2019["toc-2019-q8b"] = r"""### 1. Statement of the Halting Problem
The **Halting Problem** is the classic question:
> *"Given an arbitrary Turing Machine $M$ and an input string $w$, can an algorithm decide whether $M$ will eventually stop running (halt) on $w$, or loop infinitely?"*

Formally defined as the decision language:
$$HALT_{TM} = \{ \langle M, w \rangle \mid M \text{ is a TM that halts on input } w \}$$

**Fundamental Result:** The Halting Problem is **UNDECIDABLE** (proven by Alan Turing in 1936).

---

### 2. Proof of Undecidability by Diagonalization

#### Step 1: Assume a decider exists
Assume there is a Turing Machine $H$ that decides $HALT_{TM}$:
$$H(\langle M, w \rangle) = \begin{cases} 
\text{Accept} & \text{if } M \text{ halts on input } w \\
\text{Reject} & \text{if } M \text{ loops forever on input } w 
\end{cases}$$
Because $H$ is a decider, $H$ itself **always halts**.

#### Step 2: Construct the adversarial machine $D$
Build a new Turing Machine $D$ that takes as input the code of any Turing Machine $\langle M \rangle$:
1. $D$ invokes $H$ with input $\langle M, \langle M \rangle \rangle$.
2. If $H$ says "Accept" ($M$ halts on $\langle M \rangle$), $D$ enters an **infinite loop**.
3. If $H$ says "Reject" ($M$ loops on $\langle M \rangle$), $D$ immediately **halts**.

#### Step 3: Run $D$ on its own description $\langle D \rangle$
What happens when we run $D$ on $\langle D \rangle$?
$$D(\langle D \rangle) = \begin{cases} 
\text{loops forever} & \text{if } D \text{ halts on } \langle D \rangle \\
\text{halts} & \text{if } D \text{ loops forever on } \langle D \rangle 
\end{cases}$$

This means:
$$\text{"}D \text{ halts on } \langle D \rangle \iff D \text{ loops forever on } \langle D \rangle\text{"}$$

This is a self-contradiction. Hence, no such decider $H$ can exist. The Halting Problem is **undecidable**."""

# -----------------------------------------------------------------------------
# toc-2019-q8c (6 marks)
# Write the differences between single and multi-tape TM.
# -----------------------------------------------------------------------------
SOLUTIONS_2019["toc-2019-q8c"] = r"""### 1. Differences Between Single-Tape and Multi-Tape Turing Machines

| Feature | Single-Tape Turing Machine | Multi-Tape Turing Machine ($k \ge 2$) |
| :--- | :--- | :--- |
| **Number of Tapes** | Exactly **1 infinite tape** used for both input and scratch calculations. | **$k$ independent infinite tapes** (Tape 1 holds input; Tapes $2 \dots k$ are scratchpads). |
| **Read/Write Heads** | Exactly **1 head** scanning one tape cell. | **$k$ separate heads**, each scanning a cell on its own tape. |
| **Head Movement** | Head moves Left ($L$) or Right ($R$). | Each head moves **independently** ($L, R, \text{or } S$ - Stay). |
| **Transition Function** | $\delta: Q \times \Gamma \to Q \times \Gamma \times \{L, R\}$ | $\delta: Q \times \Gamma^k \to Q \times \Gamma^k \times \{L, R, S\}^k$ |
| **Time Complexity** | Recognizing palindromes takes $\Omega(n^2)$ quadratic time. | Recognizing palindromes takes $O(n)$ **linear time**. |
| **Simulation Cost** | Base model. | Can be simulated by a single-tape TM in $O(T(n)^2)$ time using $2k$ tracks. |
| **Computational Power** | Recognizes **Recursively Enumerable (RE)** languages. | Recognizes **Recursively Enumerable (RE)** languages (strictly equivalent power). |

---

### 2. Conclusion
While multi-tape Turing Machines offer superior convenience and can run up to quadratically faster, **they do not increase the set of solvable problems**. Any problem computable by a multi-tape TM is also computable by a single-tape TM."""

if __name__ == "__main__":
    update_year_solutions(2019, SOLUTIONS_2019)
