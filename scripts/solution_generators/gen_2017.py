import sys
from pathlib import Path
from apply_solutions import update_year_solutions

SOLUTIONS_2017 = {}

# -----------------------------------------------------------------------------
# toc-2017-q5d (9 marks)
# Use the Context Free Language (CFL) pumping lemma to show each of these
# languages not to be context free:
# - (i) {0^i 1^j | j = i^2},
# - (ii) {a^n b^n c^n | n >= 1}.
# -----------------------------------------------------------------------------
SOLUTIONS_2017["toc-2017-q5d"] = r"""### Statement of the Pumping Lemma for CFLs
If $L$ is a CFL, there exists a constant $p \ge 1$ such that any string $s \in L$ with $|s| \ge p$ can be written as $s = uvwxy$ with:
1. $|vwx| \le p$
2. $|vx| \ge 1$
3. $u v^k w x^k y \in L$ for all $k \ge 0$.

---

### Part (i): Prove $L_1 = \{0^i 1^j \mid j = i^2\}$ is NOT Context-Free

1. **Assume $L_1$ is a CFL.** Let $p$ be its pumping length.
2. **Choose string $s \in L_1$:**
   $$s = 0^p 1^{p^2}$$
   Here $i = p, j = p^2 = i^2$. Length $|s| = p + p^2 \ge p$.
3. **Decomposition $s = uvwxy$:**
   Since $|vwx| \le p$, $vwx$ can span a window of at most $p$ characters.
4. **Cases for $vwx$:**
   - **Case A ($vwx$ contains only `0`s):**
     $vx = 0^m$ with $1 \le m \le p$. Pump $k = 2$: the string has $p + m$ zeros and $p^2$ ones. But $(p+m)^2 = p^2 + 2pm + m^2 > p^2$, so $s' \notin L_1$.
   - **Case B ($vwx$ contains only `1`s):**
     $vx = 1^m$ with $1 \le m \le p$. Pump $k = 2$: string has $p$ zeros and $p^2 + m$ ones. But $p^2 \ne p^2 + m$, so $s' \notin L_1$.
   - **Case C ($vwx$ spans the boundary of `0`s and `1`s):**
     Let $v = 0^a$ and $x = 1^b$ ($a + b \ge 1, a+b \le p$).
     Pump $k = 2$: new zeros $= p + a$, new ones $= p^2 + b$.
     For $s' \in L_1$:
     $$(p + a)^2 = p^2 + 2pa + a^2 = p^2 + b \implies 2pa + a^2 = b$$
     If $a \ge 1$, then $b = 2pa + a^2 \ge 2p + 1$. But $|vwx| \le p \implies b \le p$.  
     Then $2p + 1 \le b \le p \implies 2p + 1 \le p$, which is impossible!
     If $a = 0$, then $b = 0$, but $a + b \ge 1$, impossible!
5. **Conclusion:** In all cases, $s' \notin L_1$. Hence, $L_1 = \{0^i 1^j \mid j = i^2\}$ is **not context-free**.

---

### Part (ii): Prove $L_2 = \{a^n b^n c^n \mid n \ge 1\}$ is NOT Context-Free

1. **Assume $L_2$ is a CFL.** Let $p$ be its pumping length.
2. **Choose string $s \in L_2$:**
   $$s = a^p b^p c^p$$
   Clearly $s \in L_2$ and $|s| = 3p \ge p$.
3. **Decomposition $s = uvwxy$:**
   By the lemma, $|vwx| \le p$.  
   Because $|vwx| \le p$, the substring $vwx$ cannot contain both $a$'s and $c$'s simultaneously (they are separated by $b^p$ of length $p$).  
   Thus, $vx$ can contain symbols from at most **two** of the three types $\{a, b, c\}$.
4. **Pumping with $k = 2$:**
   - If $vx$ contains only $a$'s (or only $b$'s, or only $c$'s):
     Pumping $k=2$ increases the count of that single symbol, while the other two symbol counts remain $p$. Thus the counts are not all equal $\implies s' \notin L_2$.
   - If $vx$ contains $a$'s and $b$'s (no $c$'s):
     Pumping $k=2$ increases the number of $a$'s and/or $b$'s. But the number of $c$'s remains strictly $p$. The counts cannot all be equal $\implies s' \notin L_2$.
   - If $vx$ contains $b$'s and $c$'s (no $a$'s):
     Pumping $k=2$ increases the number of $b$'s and/or $c$'s, while $a$'s remain $p \implies s' \notin L_2$.
5. **Conclusion:** In all cases, $u v^2 w x^2 y \notin L_2$.  
   Contradiction! Hence, $L_2 = \{a^n b^n c^n \mid n \ge 1\}$ is **not context-free**."""

# -----------------------------------------------------------------------------
# toc-2017-q6a (8 marks)
# Explain how a Turing Machine can be regarded as a computing device to
# compute integer functions.
# -----------------------------------------------------------------------------
SOLUTIONS_2017["toc-2017-q6a"] = r"""### 1. Concept: Turing Machines as Computers of Functions
While a Turing Machine is often introduced as a language recognizer (accepting or rejecting strings), it is fundamentally a **general-purpose computer**.  
By viewing the tape contents at the end of execution as the **output**, a Turing Machine computes a mathematical function:
$$f: \mathbb{N}^k \to \mathbb{N}$$

---

### 2. Input and Output Representation (Unary Encoding)
Because a Turing Machine operates on discrete symbols, non-negative integers are traditionally represented using **unary notation**:
- An integer $n \ge 0$ is represented as a block of $n$ identical symbols, typically $0^n$ (or $0^{n+1}$ to distinguish zero from the empty tape):
  $$0 \mapsto \epsilon \quad (\text{or } 0), \quad 1 \mapsto 0, \quad 2 \mapsto 00, \quad 3 \mapsto 000, \dots$$
- For a multi-argument function $f(n_1, n_2, \dots, n_k)$, arguments are written consecutively separated by a delimiter symbol (usually `1`):
  $$\text{Initial Tape Configuration:} \quad 0^{n_1} 1 0^{n_2} 1 \dots 1 0^{n_k}$$

---

### 3. Computation Process
1. **Initial Instantaneous Description:**
   The machine begins in start state $q_0$ with its head on the leftmost symbol of the input:
   $$\text{ID}_{initial} = q_0 0^{n_1} 1 0^{n_2}$$
2. **Execution:**
   The machine reads, modifies tape cells, and shifts head positions according to its transition function $\delta$.
3. **Halting & Output:**
   If the function $f(n_1, n_2)$ is defined for $(n_1, n_2)$, the machine reaches a halting state $q_f$ with the result written on the tape:
   $$q_0 0^{n_1} 1 0^{n_2} \vdash^* q_f 0^{f(n_1, n_2)}$$
   The output is defined as the number of zeros remaining on the tape upon halting.

If $f$ is a partial function and undefined for an input, the machine may loop forever or halt in an error/rejection state.

---

### 4. Canonical Examples of Integer Functions Computed by TMs
1. **Successor Function ($f(n) = n + 1$):**
   Scans to the end of $0^n$ and appends one more `0`.
2. **Addition ($f(m, n) = m + n$):**
   Input: $0^m 1 0^n$. The TM replaces the separator `1` with `0` and erases one trailing `0` (or one leading `0`), leaving $0^{m+n}$.
3. **Proper Subtraction / Monus ($f(m, n) = m \dot{-} n = \max(0, m - n)$):**
   Matches and crosses off each zero of $n$ with one zero of $m$.
4. **Multiplication ($f(m, n) = m \times n$):**
   Uses repeated addition via copying.

---

### 5. Church-Turing Thesis Connection
The **Church-Turing Thesis** states that any function on the integers that can be calculated by an effective algorithm can be computed by a Turing Machine (such functions are called **Turing-computable** or **partial recursive functions**)."""

# -----------------------------------------------------------------------------
# toc-2017-q6b (14 marks)
# Design a Turing Machine to implement "multiplication". Simulate the action
# for 001000.
# -----------------------------------------------------------------------------
SOLUTIONS_2017["toc-2017-q6b"] = r"""### 1. Problem Formulation
Design a Turing Machine $M$ to compute unary integer multiplication:
$$f(m, n) = m \times n$$
- **Unary Encoding:** Integer $k$ is represented as $0^k$.
- **Input on Tape:** $0^m 1 0^n 1$ (or $0^m 1 0^n B$).
- **Test Input:** `001000` ($m = 2, n = 3$).
- **Expected Output:** $0^{2 \times 3} = 0^6$ (`000000`).

---

### 2. High-Level Algorithm
Multiplication is repeated addition. We copy the $n$ zeros to the result area $m$ times:
1. Scan the first operand: replace one `0` with marker $X$.
2. Travel to the second operand: for each `0`, mark it as $Y$, travel to the end of the tape, and write a `0`.
3. Restore all $Y$'s back to `0`.
4. Return to the first operand and repeat for the next `0`.
5. When all $m$ zeros have been marked $X$, erase the inputs and leave only the $m \times n$ product zeros.

---

### 3. Step-by-Step Simulation on "001000" ($2 \times 3$)
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
# toc-2017-q6c (7 marks)
# What are the differences between single-tape and multi-tape Turing Machine?
# -----------------------------------------------------------------------------
SOLUTIONS_2017["toc-2017-q6c"] = r"""### 1. Differences Between Single-Tape and Multi-Tape Turing Machines

| Comparison Parameter | Single-Tape Turing Machine | Multi-Tape Turing Machine ($k \ge 2$) |
| :--- | :--- | :--- |
| **Tape Architecture** | Exactly **1 infinite tape** holding input, workspace, and output. | **$k$ distinct infinite tapes** (Tape 1 holds input; Tapes $2 \dots k$ are scratch tapes). |
| **Head Architecture** | Exactly **1 read/write head**. | **$k$ independent read/write heads**, one for each tape. |
| **Head Movement** | Head moves Left ($L$) or Right ($R$). | Each of the $k$ heads can move **independently** ($L, R, \text{or } S$ - Stay). |
| **Transition Function** | $\delta: Q \times \Gamma \to Q \times \Gamma \times \{L, R\}$ | $\delta: Q \times \Gamma^k \to Q \times \Gamma^k \times \{L, R, S\}^k$ |
| **Algorithmic Efficiency** | Palindrome checking $\{ww^R\}$ requires $\Omega(n^2)$ time. | Palindrome checking $\{ww^R\}$ takes $O(n)$ **linear time**. |
| **Simulation Theorem** | Baseline model. | Any $k$-tape TM running in time $T(n)$ can be simulated by a 1-tape TM in $O(T(n)^2)$ time. |
| **Computational Power** | Recognizes **Recursively Enumerable (RE)** languages. | Recognizes **Recursively Enumerable (RE)** languages (**strictly identical power**). |"""

# -----------------------------------------------------------------------------
# toc-2017-q6d (6 marks)
# Explain the multi tape Turing Machine mode. Is it more powerful that the
# basic Turing Machine? Justify your answer.
# -----------------------------------------------------------------------------
SOLUTIONS_2017["toc-2017-q6d"] = r"""### 1. Explanation of the Multi-Tape Turing Machine Model
A **Multi-Tape Turing Machine** consists of:
- A finite control unit with state set $Q$.
- $k$ physical tapes ($k \ge 1$), each infinite in one (or two) directions, divided into cells.
- $k$ independent read/write heads, where head $i$ scans tape $i$.
- **Initialization:** Tape 1 contains the input string $w_1 w_2 \dots w_n$, with its head at the leftmost symbol. Tapes $2, 3, \dots, k$ are completely blank.
- **Operation:** In each step, the machine reads the $k$-tuple of symbols scanned by the heads, changes state, writes new symbols on each tape, and moves each head independently ($L, R, \text{or } S$):
  $$\delta: Q \times \Gamma^k \to Q \times \Gamma^k \times \{L, R, S\}^k$$

---

### 2. Is it More Powerful than the Basic Turing Machine?
**Direct Answer:** **NO, it is NOT more powerful in terms of computational capability.**  
Both models accept the **exact same class of languages** (the Recursively Enumerable languages).

#### Justification (Simulation Proof):
Every multi-tape TM $M$ can be simulated by an equivalent single-tape TM $S$:
1. **Multi-Track Encoding:**
   The single tape of $S$ is divided into $2k$ tracks:
   - Tracks $1, 3, 5, \dots, 2k-1$ store the contents of tapes $1, 2, \dots, k$.
   - Tracks $2, 4, 6, \dots, 2k$ store marker symbols (e.g., $\hat{X}$) showing the current head position of each tape.
2. **Simulation of One Multi-Tape Step:**
   To simulate a single transition of $M$, machine $S$:
   - Sweeps from the leftmost head marker to the rightmost head marker to read the $k$ symbols scanned by the virtual heads.
   - Updates its internal state according to $M$'s transition function $\delta$.
   - Sweeps back, updates the symbols on the content tracks, and shifts the marker symbols left or right.
3. If $M$ accepts/rejects, $S$ accepts/rejects.
4. Hence, $L(M) = L(S)$.

---

### 3. Efficiency Note
While they have identical computational power, a multi-tape TM can be **quadratically faster**:
$$\text{Time on 1-tape TM} = O((\text{Time on } k\text{-tape TM})^2)$$"""

# -----------------------------------------------------------------------------
# toc-2017-q7a (25 marks)
# Consider the following grammar
# S -> aAa | bBb | eps
# A -> C | a
# B -> C | b
# C -> CDE | eps
# D -> A | B | ab
# - (i) Are there any useless symbols? Eliminate them if so.
# - (ii) Eliminate eps-productions.
# - (iii) Eliminate unit productions.
# - (iv) Put the grammar into Chomosky Normal Form (CNF).
# -----------------------------------------------------------------------------
SOLUTIONS_2017["toc-2017-q7a"] = r"""### Problem Overview
We are given the context-free grammar:
$$\begin{aligned}
S &\to aAa \mid bBb \mid \varepsilon \\
A &\to C \mid a \\
B &\to C \mid b \\
C &\to CDE \mid \varepsilon \\
D &\to A \mid B \mid ab
\end{aligned}$$
*(Variables: $S, A, B, C, D, E$; Terminals: $a, b$. Note that variable $E$ has no production rules).*

---

### Step (i): Identify & Eliminate Useless Symbols
1. **Generating Symbols in original grammar:**
   - $E$ has NO productions $\implies E$ cannot generate any terminal string.
   - Any rule containing $E$ cannot generate terminals ($C \to CDE$ is non-generating).
   - $C \to \varepsilon$ generates a string of length 0 (generating).
   - $A \to a$, $B \to b$, $D \to ab$, $S \to \varepsilon$ are generating.
   - Discarding non-generating symbol $E$ removes rule $C \to CDE$.
2. **Reachability:** All remaining symbols $\{S, A, B, C, D\}$ are reachable from $S$.
3. **Grammar after Step (i):**
   $$\begin{aligned}
   S &\to aAa \mid bBb \mid \varepsilon \\
   A &\to C \mid a \\
   B &\to C \mid b \\
   C &\to \varepsilon \\
   D &\to A \mid B \mid ab
   \end{aligned}$$

---

### Step (ii): Eliminate $\varepsilon$-Productions
1. **Nullable variables:**
   - $S \to \varepsilon, C \to \varepsilon \implies \{S, C\}$.
   - $A \to C, B \to C \implies \{S, C, A, B\}$.
   - $D \to A \mid B \implies \{S, C, A, B, D\}$.
   - All variables $\{S, A, B, C, D\}$ are nullable.
2. **Form productions without $\varepsilon$:**
   - $C \to \varepsilon$ is dropped, leaving $C$ with no productions (making $C$ non-generating).
   - $A \to a$
   - $B \to b$
   - $D \to A \mid B \mid ab$
   - $S \to aAa \mid aa \mid bBb \mid bb$

---

### Step (iii): Eliminate Unit Productions
1. **Unit pairs:**
   - $(D, A)$ and $(D, B)$
2. **Replace unit productions:**
   - $D \to a \mid b \mid ab$
   - $A \to a$
   - $B \to b$
   - $S \to aAa \mid aa \mid bBb \mid bb$
3. **Useless symbol cleanup:** Variable $D$ is now completely unreachable from $S$, so $D$ is eliminated.

**Grammar after Step (iii):**
$$\begin{aligned}
S &\to aAa \mid aa \mid bBb \mid bb \\
A &\to a \\
B &\to b
\end{aligned}$$

---

### Step (iv): Put into Chomsky Normal Form (CNF)
1. **Terminals:**
   - Let $X_a \to a$ and $X_b \to b$ (or reuse $A \to a, B \to b$).
2. **Binary form conversion:**
   - $S \to aa \implies S \to X_a X_a$
   - $S \to bb \implies S \to X_b X_b$
   - $S \to aAa \implies S \to X_a Y_1$ where $Y_1 \to A X_a$
   - $S \to bBb \implies S \to X_b Y_2$ where $Y_2 \to B X_b$

### Final CNF Grammar
$$\begin{aligned}
S &\to X_a Y_1 \mid X_a X_a \mid X_b Y_2 \mid X_b X_b \\
Y_1 &\to A X_a \\
Y_2 &\to B X_b \\
A &\to a \\
B &\to b \\
X_a &\to a \\
X_b &\to b
\end{aligned}$$"""

# -----------------------------------------------------------------------------
# toc-2017-q7b (10 marks)
# Show that "If a language L and its complement \overline{L} are both
# recursively enumerable, then both languages are recursive."
# -----------------------------------------------------------------------------
SOLUTIONS_2017["toc-2017-q7b"] = r"""### 1. Statement of the Theorem
> **Theorem:** A language $L$ is **Recursive (Decidable)** if and only if both $L$ and its complement $\overline{L}$ are **Recursively Enumerable (Turing-Recognizable)**.

We are asked to prove the forward direction:
$$\text{If } L \in \text{RE} \text{ and } \overline{L} \in \text{RE}, \text{ then } L \text{ and } \overline{L} \text{ are Recursive.}$$

---

### 2. High-Level Intuition
- Since $L$ is RE, there is a TM $M_1$ that accepts any $w \in L$ (but may loop forever if $w \notin L$).
- Since $\overline{L}$ is RE, there is a TM $M_2$ that accepts any $w \in \overline{L}$ (but may loop forever if $w \notin \overline{L}$).
- For ANY string $w \in \Sigma^*$, $w$ must belong to **either $L$ or $\overline{L}$**, but never both!
- If we run $M_1$ and $M_2$ **in parallel (interleaved step-by-step)** on input $w$, **one of them is guaranteed to halt and accept in finite time!**
- This allows us to construct a decider $M$ that always halts.

---

### 3. Step-by-Step Construction of Decider $M$

```
                  +--------------------------------+
                  | Input string w                 |
                  +--------------------------------+
                                 |
                  +--------------+---------------+
                  |                              |
                  v                              v
           +--------------+               +--------------+
           | Run M1 on w  |               | Run M2 on w  |
           +--------------+               +--------------+
                  |                              |
            If M1 halts                    If M2 halts
             and accepts                    and accepts
                  |                              |
                  v                              v
            HALT & ACCEPT                  HALT & REJECT
```

#### Algorithm for $M$ on input $w$:
1. On input string $w$:
2. Simulate $M_1$ and $M_2$ on input $w$ simultaneously (in parallel, alternating one step of $M_1$, then one step of $M_2$).
3. **If $M_1$ halts and accepts $w$:**
   - Machine $M$ halts and **ACCEPTS** $w$.
4. **If $M_2$ halts and accepts $w$:**
   - Machine $M$ halts and **REJECTS** $w$.

---

### 4. Proof of Correctness
- **Case 1: $w \in L$**
  Since $w \in L$, $M_1$ will halt and accept $w$ after some finite number of steps $k$. Since $M$ runs $M_1$, $M$ will halt and ACCEPT $w$ within $2k$ steps.
- **Case 2: $w \notin L$ (meaning $w \in \overline{L}$)**
  Since $w \in \overline{L}$, $M_2$ will halt and accept $w$ after some finite number of steps $m$. $M$ will halt and REJECT $w$ within $2m$ steps.

Because every string $w \in \Sigma^*$ falls into either Case 1 or Case 2, **machine $M$ always halts** on every input string.

---

### 5. Conclusion
Since $M$ is a Turing Machine that always halts and correctly decides whether $w \in L$, the language $L$ is **Recursive (Decidable)**.  
Furthermore, because the complement of a recursive language is always recursive, $\overline{L}$ is also **Recursive**."""

# -----------------------------------------------------------------------------
# toc-2017-q8a (6 marks)
# Explain the halting problem of Turing Machine.
# -----------------------------------------------------------------------------
SOLUTIONS_2017["toc-2017-q8a"] = r"""### 1. What is the Halting Problem?
The **Halting Problem** asks:
> *"Does there exist an algorithm (Turing Machine) that can take the source code of any program (Turing Machine $M$) and an arbitrary input string $w$, and decide whether $M$ will halt on $w$, or run in an infinite loop?"*

Formally defined as:
$$HALT_{TM} = \{ \langle M, w \rangle \mid M \text{ is a TM that halts on input } w \}$$

---

### 2. Proof of Undecidability (Diagonalization Argument)
1. **Assume a decider $H$ exists:**
   $$H(\langle M, w \rangle) = \begin{cases} \text{Accept} & \text{if } M \text{ halts on } w \\ \text{Reject} & \text{if } M \text{ loops on } w \end{cases}$$
2. **Construct an inverting machine $D$:**
   Given input $\langle M \rangle$:
   - Run $H$ on $\langle M, \langle M \rangle \rangle$.
   - If $H$ says "Accept", $D$ enters an **infinite loop**.
   - If $H$ says "Reject", $D$ **halts**.
3. **Feed $D$ its own code $\langle D \rangle$:**
   - If $D$ halts on $\langle D \rangle \implies D$ loops forever.
   - If $D$ loops on $\langle D \rangle \implies D$ halts.
4. This logical impossibility ($P \iff \neg P$) proves that **no such decider $H$ can exist**.

**Conclusion:** The Halting Problem is **undecidable**."""

# -----------------------------------------------------------------------------
# toc-2017-q8b (10 marks)
# What is unrestricted grammar? Prove that CFLs are closed under (i) Homomorphism
# and (ii) Reversal.
# -----------------------------------------------------------------------------
SOLUTIONS_2017["toc-2017-q8b"] = r"""### 1. What is an Unrestricted Grammar?
An **Unrestricted Grammar** (also known as a **Type-0 Grammar** or Phase-Structure Grammar in the Chomsky Hierarchy) is the most general class of formal grammars:
- **Production Rule Format:**
  $$\alpha \to \beta$$
  where $\alpha \in (V \cup T)^+$ with at least one variable, and $\beta \in (V \cup T)^*$.
- **No Restrictions:** There are no length restrictions (unlike context-sensitive grammars where $|\alpha| \le |\beta|$), and the left-hand side can contain multiple symbols.
- **Computational Equivalence:** Unrestricted grammars generate exactly the **Recursively Enumerable (RE)** languages (equivalent in computing power to Turing Machines).

---

### 2. Prove CFLs are Closed under (i) Homomorphism

#### Definition:
A homomorphism $h: \Sigma \to \Gamma^*$ replaces each symbol $a \in \Sigma$ with a string $h(a) \in \Gamma^*$.  
For a language $L$, $h(L) = \{h(w) \mid w \in L\}$.

#### Proof:
Let $L$ be generated by CFG $G = (V, \Sigma, P, S)$.  
Construct a new grammar $G' = (V, \Gamma, P', S)$ where:
- The variables $V$ and start symbol $S$ remain unchanged.
- For each production rule $A \to \alpha \in P$:
  - Define a new rule $A \to \alpha'$ in $P'$, where $\alpha'$ is obtained by replacing each terminal symbol $a$ in $\alpha$ with the string $h(a)$, while leaving variables untouched.
- Since each production in $P'$ still has a single variable on its left-hand side, $G'$ is a valid Context-Free Grammar.
- By induction on derivation length, $S \Rightarrow^* w$ in $G \iff S \Rightarrow^* h(w)$ in $G'$.
- Hence, $L(G') = h(L)$, proving **CFLs are closed under homomorphism**.

---

### 3. Prove CFLs are Closed under (ii) Reversal

#### Definition:
The reversal of a string $w = a_1 a_2 \dots a_k$ is $w^R = a_k \dots a_2 a_1$.  
The reversed language is $L^R = \{w^R \mid w \in L\}$.

#### Proof:
Let $L$ be generated by CFG $G = (V, T, P, S)$.  
Construct the reversed grammar $G^R = (V, T, P^R, S)$ where:
- For each production $A \to \alpha \in P$, add $A \to \alpha^R$ to $P^R$ (reversing the sequence of symbols on the right-hand side).
  - *Example:* If $A \to a B c$, then in $G^R$ we add $A \to c B a$.
- Since every rule in $P^R$ still has a single variable on the left, $G^R$ is a valid CFG.
- By induction on the derivation tree:
  $$A \Rightarrow^* w \text{ in } G \iff A \Rightarrow^* w^R \text{ in } G^R$$
- Therefore, $L(G^R) = L^R$, proving **CFLs are closed under reversal**."""

# -----------------------------------------------------------------------------
# toc-2017-q8c (11 marks)
# State the Pumping lemma for CFL's. Convert the following grammar to a PDA
# that accepts the same language by empty stack.
# S -> aAA
# A -> aS | bS | a
# -----------------------------------------------------------------------------
SOLUTIONS_2017["toc-2017-q8c"] = r"""### 1. Statement of the Pumping Lemma for CFLs
If $L$ is a Context-Free Language, there exists a pumping length $p \ge 1$ such that any string $s \in L$ with $|s| \ge p$ can be written as $s = uvwxy$ satisfying:
1. $|vwx| \le p$
2. $|vx| \ge 1$
3. $u v^i w x^i y \in L$ for all $i \ge 0$.

---

### 2. Conversion of CFG to PDA (Acceptance by Empty Stack)

#### Given Grammar:
$$\begin{aligned}
S &\to aAA \\
A &\to aS \mid bS \mid a
\end{aligned}$$
*(Variables: $V = \{S, A\}$; Terminals: $\Sigma = \{a, b\}$)*

#### Standard Construction Method:
We construct a Pushdown Automaton $P = (Q, \Sigma, \Gamma, \delta, q_0, Z_0, \emptyset)$ that simulates leftmost derivations:
- **State set:** $Q = \{q\}$ (a single state is sufficient).
- **Input alphabet:** $\Sigma = \{a, b\}$
- **Stack alphabet:** $\Gamma = V \cup \Sigma = \{S, A, a, b\}$
- **Start stack symbol:** $Z_0 = S$
- **Acceptance:** By empty stack ($N(P)$).

#### Transition Rules of the PDA:

1. **Variable expansion rules ($\epsilon$-transitions that replace top variable with RHS):**
   - For $S \to aAA$:
     $$\delta(q, \epsilon, S) = \{(q, aAA)\}$$
   - For $A \to aS \mid bS \mid a$:
     $$\delta(q, \epsilon, A) = \{(q, aS), (q, bS), (q, a)\}$$

2. **Terminal matching rules (match input symbol with top of stack and pop):**
   - For terminal $a$:
     $$\delta(q, a, a) = \{(q, \epsilon)\}$$
   - For terminal $b$:
     $$\delta(q, b, b) = \{(q, \epsilon)\}$$

---

### 3. Example Derivation and PDA Stack Trace
Consider deriving the shortest string $w = aaa$:
- **CFG derivation:** $S \Rightarrow aAA \Rightarrow aaA \Rightarrow aaa$
- **PDA Trace on input "aaa":**
  1. Initial ID: $(q, aaa, S)$
  2. Apply $\delta(q, \epsilon, S) = (q, aAA)$: ID becomes $(q, aaa, aAA)$
  3. Match $a$ with $\delta(q, a, a) = (q, \epsilon)$: ID becomes $(q, aa, AA)$
  4. Expand first $A$ using $A \to a$: ID becomes $(q, aa, aA)$
  5. Match $a$: ID becomes $(q, a, A)$
  6. Expand remaining $A$ using $A \to a$: ID becomes $(q, a, a)$
  7. Match final $a$: ID becomes $(q, \epsilon, \epsilon)$

The stack is now empty and all input has been consumed. The string is **accepted by empty stack**."""

if __name__ == "__main__":
    update_year_solutions(2017, SOLUTIONS_2017)
