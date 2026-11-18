import sys
from pathlib import Path
from apply_solutions import update_year_solutions

SOLUTIONS_2022 = {}

# -----------------------------------------------------------------------------
# toc-2022-q5a (20 marks)
# Consider the grammar:
# S -> AaA | CA | BaB
# A -> aaBa | CDA | aa | DC
# C -> Ca | bC | D
# D -> bD | eps
# - i) Eliminate eps-productions,
# - ii) Eliminate unit productions from the resulting grammar from (i),
# - iii) Eliminate useless productions from the resulting grammar from (ii),
# - iv) Convert the grammar from (iii) into Chomsky Normal Form.
# -----------------------------------------------------------------------------
SOLUTIONS_2022["toc-2022-q5a"] = r"""### Problem Overview
We are given the context-free grammar:
$$\begin{aligned}
S &\to AaA \mid CA \mid BaB \\
A &\to aaBa \mid CDA \mid aa \mid DC \\
C &\to Ca \mid bC \mid D \\
D &\to bD \mid \epsilon
\end{aligned}$$
*(Variables: $S, A, B, C, D$; Terminals: $a, b$. Note that variable $B$ has no production rules).*

We will transform this grammar step by step following the standard CFG simplification and CNF conversion procedure.

---

### Step (i): Eliminate $\epsilon$-Productions

1. **Find all nullable variables (variables deriving $\epsilon$):**
   - Directly nullable: $D \to \epsilon \implies D$ is nullable.
   - Since $D$ is nullable and $C \to D \implies C$ is nullable.
   - Since both $C$ and $D$ are nullable, in $A \to DC$: both symbols are nullable, so $A \Rightarrow^* \epsilon \implies A$ is nullable.
   - Since $A$ is nullable, in $S \to CA$: both $C$ and $A$ are nullable, so $S \Rightarrow^* \epsilon \implies S$ is nullable.
   - Variable $B$ is not nullable (it has no productions).
   - **Set of nullable variables:** $\{S, A, C, D\}$.

2. **Form new productions without $\epsilon$:**
   Replace productions containing nullable variables with all non-empty combinations of their presence/absence:
   - **For $D \to bD$:**
     - Keeping or dropping $D$: $D \to bD \mid b$. (Drop $D \to \epsilon$).
   - **For $C \to Ca \mid bC \mid D$:**
     - From $Ca$: $Ca \mid a$
     - From $bC$: $bC \mid b$
     - From $D$: $D$
     - Thus: $C \to Ca \mid a \mid bC \mid b \mid D$
   - **For $A \to aaBa \mid CDA \mid aa \mid DC$:**
     - From $aaBa$: $B$ is not nullable, so $aaBa$ remains $aaBa$.
     - From $CDA$: $C$ and $A$ and $D$ are nullable:
       Combinations: $CDA \mid CD \mid CA \mid DA \mid C \mid D \mid A$ (dropping all 3 would be $\epsilon$, which is omitted).
     - From $aa$: $aa$
     - From $DC$: $DC \mid D \mid C$
     - Combining all unique alternatives for $A$:
       $$A \to aaBa \mid CDA \mid CD \mid CA \mid DA \mid C \mid D \mid A \mid DC \mid aa$$
   - **For $S \to AaA \mid CA \mid BaB$:**
     - From $AaA$: both $A$'s nullable: $AaA \mid aA \mid Aa \mid a$
     - From $CA$: both nullable: $CA \mid C \mid A$
     - From $BaB$: $B$ is not nullable, so $BaB$ remains $BaB$.
     - Combining all unique alternatives for $S$:
       $$S \to AaA \mid aA \mid Aa \mid a \mid CA \mid C \mid A \mid BaB$$

---

### Step (ii): Eliminate Unit Productions
We eliminate productions of the form $X \to Y$ (where $X, Y \in V$).
Note: Remove self-loops like $A \to A$.

1. **Find all unit pairs $(X, Y)$ where $X \Rightarrow^* Y$:**
   - From $D$: only $(D, D)$.
   - From $C \to D$: unit pairs are $(C, C)$ and $(C, D)$.
   - From $A \to C$ and $A \to D$: unit pairs are $(A, A), (A, C), (A, D)$.
   - From $S \to C$ and $S \to A$: unit pairs are $(S, S), (S, C), (S, A)$, and through $C$ or $A \to D$, $(S, D)$.

2. **Replace each unit production $X \to Y$ with all non-unit productions of $Y$:**
   - **For $D$:** Non-unit productions:
     $$D \to bD \mid b$$
   - **For $C$:** Inherits from $(C, C)$ and $(C, D)$:
     $$C \to Ca \mid a \mid bC \mid b \mid bD$$
   - **For $A$:** Inherits from $(A, A), (A, C), (A, D)$:
     $$A \to aaBa \mid CDA \mid CD \mid CA \mid DA \mid DC \mid aa \mid Ca \mid a \mid bC \mid b \mid bD$$
   - **For $S$:** Inherits from $(S, S), (S, A), (S, C), (S, D)$:
     $$S \to AaA \mid aA \mid Aa \mid BaB \mid aaBa \mid CDA \mid CD \mid CA \mid DA \mid DC \mid aa \mid Ca \mid a \mid bC \mid b \mid bD$$

---

### Step (iii): Eliminate Useless Productions
A symbol is useful if and only if it is both **generating** (can derive a terminal string) and **reachable** (can be reached from start symbol $S$).

1. **Phase 1: Identify Generating Symbols:**
   - Variable $B$ has NO production rules in the grammar. Thus, **$B$ cannot generate any terminal string!**
   - Any production containing $B$ is non-generating and must be eliminated:
     - Discard $BaB$ from $S$.
     - Discard $aaBa$ from $A$ and from $S$.
   - Check remaining variables:
     - $D \to b \implies D$ is generating.
     - $C \to a \implies C$ is generating.
     - $A \to a \implies A$ is generating.
     - $S \to a \implies S$ is generating.
   - All remaining variables $\{S, A, C, D\}$ are generating!
   - Result after removing non-generating rules:
     $$\begin{aligned}
     S &\to AaA \mid aA \mid Aa \mid a \mid CDA \mid CD \mid CA \mid DA \mid DC \mid aa \mid Ca \mid bC \mid b \mid bD \\
     A &\to CDA \mid CD \mid CA \mid DA \mid DC \mid aa \mid Ca \mid a \mid bC \mid b \mid bD \\
     C &\to Ca \mid a \mid bC \mid b \mid bD \\
     D &\to bD \mid b
     \end{aligned}$$

2. **Phase 2: Identify Reachable Symbols:**
   - Start with $S$: $\text{Reachable} = \{S\}$.
   - $S$ productions contain variables $A, C, D$.
   - Thus, $\text{Reachable} = \{S, A, C, D\}$. All variables are reachable.
   - No unreachable symbols exist.

---

### Step (iv): Convert into Chomsky Normal Form (CNF)
In CNF, every production must be of the form $X \to YZ$ or $X \to x$.

1. **Introduce variables for terminals:**
   - Let $X_a \to a$
   - Let $X_b \to b$

2. **Replace terminals in mixed bodies of length $\ge 2$:**
   - $aA \implies X_a A$
   - $Aa \implies A X_a$
   - $aa \implies X_a X_a$
   - $Ca \implies C X_a$
   - $bC \implies X_b C$
   - $bD \implies X_b D$

3. **Break long bodies (length 3) into pairs of variables:**
   - $AaA \implies A X_a A \implies A Y_1$ where $Y_1 \to X_a A$
   - $CDA \implies C Y_2$ where $Y_2 \to D A$

4. **Final CNF Grammar:**
   $$\begin{aligned}
   S &\to A Y_1 \mid X_a A \mid A X_a \mid a \mid C Y_2 \mid CD \mid CA \mid DA \mid DC \mid X_a X_a \mid C X_a \mid X_b C \mid b \mid X_b D \\
   A &\to C Y_2 \mid CD \mid CA \mid DA \mid DC \mid X_a X_a \mid C X_a \mid a \mid X_b C \mid b \mid X_b D \\
   C &\to C X_a \mid a \mid X_b C \mid b \mid X_b D \\
   D &\to X_b D \mid b \\
   Y_1 &\to X_a A \\
   Y_2 &\to D A \\
   X_a &\to a \\
   X_b &\to b
   \end{aligned}$$"""

# -----------------------------------------------------------------------------
# toc-2022-q6a (15 marks)
# Consider the problem of checking a string whether belong to the language
# L = {0^n 1^{2n} | n >= 0} using Turing machine. State if the problem is decidable.
# -----------------------------------------------------------------------------
SOLUTIONS_2022["toc-2022-q6a"] = r"""### 1. Is the Problem Decidable?
**YES, the problem is DECIDABLE.**  
A language is decidable (or recursive) if there exists a Turing Machine that **halts on all inputs**—accepting strings that belong to the language and rejecting strings that do not.  
We can design a deterministic Turing Machine $M$ that decides $L = \{0^n 1^{2n} \mid n \ge 0\}$ in $O(|w|^2)$ time without ever looping infinitely.

---

### 2. High-Level Strategy & Intuition
For every single `0` read on the left:
1. Cross it off (mark it as `X`).
2. Move all the way right to find and cross off **two** corresponding `1`s (mark them as `Y`).
3. Move back left to the next unmarked `0` and repeat.
4. When all `0`s have been processed, verify that **no extra unmarked `1`s** remain on the tape.
5. If at any point the counts do not match or symbols are out of order, halt and REJECT.
6. If the input is empty ($n=0$), accept immediately.

---

### 3. Formal Definition of the Turing Machine
Define the decider TM $M = (Q, \Sigma, \Gamma, \delta, q_0, B, F)$ where:
- **States:** $Q = \{q_0, q_1, q_2, q_3, q_{check}, q_{accept}, q_{reject}\}$
- **Input Alphabet:** $\Sigma = \{0, 1\}$
- **Tape Alphabet:** $\Gamma = \{0, 1, X, Y, B\}$
- **Start State:** $q_0$
- **Blank Symbol:** $B$
- **Accept State:** $F = \{q_{accept}\}$

#### Roles of States:
- **$q_0$ (Start / Find 0):** Scans the first unmarked `0`. Replaces it with `X`, transitions to $q_1$. If it reads `Y`, transitions to $q_{check}$ to verify all symbols are exhausted. If it reads $B$, accepts ($\epsilon \in L$).
- **$q_1$ (Scan to first 1):** Moves right over `0`s and `Y`s to find the first unmarked `1`. Replaces it with `Y`, transitions to $q_2$.
- **$q_2$ (Find second 1):** Scans right over `Y`s to find the second unmarked `1`. Replaces it with `Y`, transitions to $q_3$ (return state).
- **$q_3$ (Return Left):** Moves left past `Y`s and `0`s until the marker `X` is reached. Moves one cell right and returns to $q_0$.
- **$q_{check}$ (Verification):** Checks that only `Y`s exist up to blank $B$. If so, enters $q_{accept}$.

---

### 4. Transition Function Table ($\delta$)

| State | Input `0` | Input `1` | Marker `X` | Marker `Y` | Blank `B` |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **$q_0$** | $(q_1, X, R)$ | Reject | — | $(q_{check}, Y, R)$ | $(q_{accept}, B, S)$ |
| **$q_1$** | $(q_1, 0, R)$ | $(q_2, Y, R)$ | — | $(q_1, Y, R)$ | Reject |
| **$q_2$** | Reject | $(q_3, Y, L)$ | — | $(q_2, Y, R)$ | Reject |
| **$q_3$** | $(q_3, 0, L)$ | — | $(q_0, X, R)$ | $(q_3, Y, L)$ | — |
| **$q_{check}$** | Reject | Reject | — | $(q_{check}, Y, R)$ | $(q_{accept}, B, S)$ |

*(Any unspecified transition leads directly to $q_{reject}$ and halts).*

---

### 5. Execution Example: Trace for $w = 011$ ($n=1$)
- $q_0 0 1 1 B \vdash X q_1 1 1 B$  *(marks 0 as X, enters $q_1$)*
- $X q_1 1 1 B \vdash X Y q_2 1 B$  *(marks first 1 as Y, enters $q_2$)*
- $X Y q_2 1 B \vdash X q_3 Y Y B$  *(marks second 1 as Y, enters $q_3$)*
- $X q_3 Y Y B \vdash q_3 X Y Y B \vdash X q_0 Y Y B$  *(moves left to X, returns to $q_0$)*
- $X q_0 Y Y B \vdash X Y q_{check} Y B$  *(reads Y, enters verification)*
- $X Y q_{check} Y B \vdash X Y Y q_{check} B$  *(reads Y, moves R)*
- $X Y Y q_{check} B \vdash X Y Y q_{accept} B$  *(reaches B, **ACCEPTS!**)*

### 6. Conclusion
Because $M$ halts on all strings $w \in \{0, 1\}^*$ in finite time without looping, the language $L = \{0^n 1^{2n} \mid n \ge 0\}$ is **decidable**."""

# -----------------------------------------------------------------------------
# toc-2022-q6b (10 marks)
# State Boolean satisfiability problem is NP complete problem.
# -----------------------------------------------------------------------------
SOLUTIONS_2022["toc-2022-q6b"] = r"""### 1. The Statement (Cook-Levin Theorem)
The **Cook-Levin Theorem** (Stephen Cook 1971, Leonid Levin 1973) states:
> **"The Boolean Satisfiability Problem (SAT) is NP-Complete."**

This is the landmark foundational theorem of computational complexity theory. It established the very first NP-complete problem, providing the anchor from which all other NP-completeness proofs (such as 3-SAT, Clique, Vertex Cover, Hamiltonian Path) are derived via polynomial-time reductions.

---

### 2. Definition of Boolean Satisfiability (SAT)
- **Input:** A Boolean formula $\phi$ consisting of $n$ Boolean variables $x_1, x_2, \dots, x_n$, logical operators ($\wedge$ AND, $\vee$ OR, $\neg$ NOT), and parentheses. Typically written in Conjunctive Normal Form (CNF):
  $$\phi = C_1 \wedge C_2 \wedge \dots \wedge C_m$$
- **Question:** Does there exist a truth assignment $\tau: \{x_1, \dots, x_n\} \to \{\text{TRUE}, \text{FALSE}\}$ such that $\phi$ evaluates to **TRUE**?
- If such an assignment exists, $\phi$ is **satisfiable**; otherwise, it is **unsatisfiable**.

---

### 3. Proof Structure: Why SAT is NP-Complete
To prove that SAT is NP-complete, two requirements must be satisfied:
1. **$\text{SAT} \in NP$** (Verification in polynomial time)
2. **$\text{SAT is NP-Hard}$** (Every problem in NP can be reduced to SAT in polynomial time)

#### Part 1: Proving $\text{SAT} \in NP$
- **Certificate:** A candidate truth assignment $\tau = (v_1, v_2, \dots, v_n)$ assigning 0 or 1 to each variable $x_i$.
- **Verification Algorithm:**
  1. Substitute the boolean values of $\tau$ into the formula $\phi$.
  2. Evaluate the truth value of each clause $C_j$.
  3. Check if all clauses evaluate to TRUE.
- **Time Complexity:** The evaluation takes $O(|\phi|)$ linear time, which is polynomial in the input length.
- Therefore, **$\text{SAT} \in NP$**.

#### Part 2: Proving SAT is NP-Hard (The Cook-Levin Proof Idea)
We must show that **for EVERY language $A \in NP$, $A \le_p \text{SAT}$**.

1. Since $A \in NP$, there exists a Non-deterministic Turing Machine (NTM) $M$ that decides $A$ in polynomial time $p(n)$ on any input $w$ of length $n$.
2. The entire computation of $M$ on $w$ can be represented as an $p(n) \times p(n)$ grid (called a **computation tableau**):
   - Row $t$ represents the configuration (tape contents, head position, state) of $M$ at time step $t$.
3. Cook and Levin constructed a Boolean formula $\phi_{M, w}$ that simulates this computation using propositional variables:
   $$\phi_{M, w} = \phi_{cell} \wedge \phi_{start} \wedge \phi_{move} \wedge \phi_{accept}$$
   - **$\phi_{cell}$:** Asserts that each cell in the tableau contains exactly one tape symbol.
   - **$\phi_{start}$:** Asserts that the first row matches the initial configuration of $M$ on input $w$.
   - **$\phi_{move}$:** Asserts that each row follows validly from the previous row according to the transition function $\delta$ of $M$ (using local $2 \times 3$ windows).
   - **$\phi_{accept}$:** Asserts that an accepting state appears somewhere in the tableau.
4. **Equivalence & Complexity:**
   - $M$ accepts $w \iff \phi_{M, w}$ is satisfiable.
   - The size of $\phi_{M, w}$ is $O(p(n)^2)$, which can be constructed deterministically in **polynomial time**.

---

### 4. Conclusion
Because $\text{SAT} \in NP$ and every language in NP can be reduced to SAT in polynomial time ($A \le_p \text{SAT}$), **SAT is NP-Complete**."""

# -----------------------------------------------------------------------------
# toc-2022-q7b (8 marks)
# Compare how recursive and recursively enumerable language acts differently
# on Turing machine.
# -----------------------------------------------------------------------------
SOLUTIONS_2022["toc-2022-q7b"] = r"""### 1. Fundamental Distinction: Halting vs. Looping
The key difference between **Recursive Languages** and **Recursively Enumerable (RE) Languages** lies in how their recognizing Turing Machines behave when given a string that **does NOT belong to the language**:

```
Input string w
      |
      v
+-------------+
| Turing Mach |
+-------------+
   /       \
  /         \
w in L     w NOT in L
  |             |
Halt &     +----------------------------------------+
Accept     | Recursive: ALWAYS Halts & Rejects      |
           | RE:        May Halt & Reject OR LOOP!  |
           +----------------------------------------+
```

---

### 2. Detailed Side-by-Side Comparison

| Feature | Recursive Language (Decidable) | Recursively Enumerable Language (Turing-Recognizable) |
| :--- | :--- | :--- |
| **Definition** | A language $L$ for which there exists a TM that **always halts** on every input $w \in \Sigma^*$. | A language $L$ for which there exists a TM that halts and accepts if $w \in L$. |
| **Behavior on $w \in L$** | Halts and **ACCEPTS**. | Halts and **ACCEPTS**. |
| **Behavior on $w \notin L$** | **Always halts** and **REJECTS**. | May **REJECT** (by halting) or **LOOP FOREVER**. |
| **Machine Name** | Recognized by a **Decider** (or Total Turing Machine). | Recognized by a standard **Recognizer** (Semi-decider). |
| **Decision Problem** | The membership problem ($w \in L$) is **Decidable**. | The membership problem is **Undecidable** (Semi-decidable). |
| **Closure under Complement** | **Closed under complementation:** If $L$ is recursive, $\overline{L}$ is also recursive. | **NOT closed under complementation:** If $L$ is RE, $\overline{L}$ is not necessarily RE (e.g., $A_{TM}$ is RE, but $\overline{A_{TM}}$ is not). |
| **Classic Example** | $L = \{0^n 1^n \mid n \ge 0\}$, any context-free or regular language. | $A_{TM} = \{\langle M, w \rangle \mid M \text{ accepts } w\}$, $HALT_{TM}$. |

---

### 3. Key Theorem Connecting the Two
> **Theorem:** A language $L$ is **Recursive** if and only if both $L$ and its complement $\overline{L}$ are **Recursively Enumerable**.

**Proof Intuition:**
- If both $L$ and $\overline{L}$ are RE, we have two TMs: $M_1$ recognizing $L$ and $M_2$ recognizing $\overline{L}$.
- To decide whether $w \in L$, run $M_1$ and $M_2$ **in parallel (interleaved)** on $w$.
- Since $w$ must belong to either $L$ or $\overline{L}$, exactly one of the two machines is guaranteed to halt and accept in finite time!
- If $M_1$ halts $\implies$ Accept. If $M_2$ halts $\implies$ Reject. Thus, we have built a decider that always halts."""

# -----------------------------------------------------------------------------
# toc-2022-q7c (15 marks)
# Suppose, you and your friend are playing a game where there are 'k' spots.
# Each spot has balls of same color. Each of you simultaneously picks a
# (single) ball from each spot and approach forward. You start from first spot
# and your friend from last spot to first spot. Determine using Turing machine
# with storage if both of you have chosen balls of same color in same sequence
# when you meet at the middle spot.
# -----------------------------------------------------------------------------
SOLUTIONS_2022["toc-2022-q7c"] = r"""### 1. Problem Modeling
- We have $k$ spots arranged linearly from $1$ to $k$.
- Each spot contains a ball of a specific color from a finite set of colors $\Sigma = \{c_1, c_2, \dots, c_m\}$ (e.g., $\{R, G, B\}$).
- **Your movement:** Starts from spot $1$ moving forward: picks balls in sequence $b_1, b_2, \dots$.
- **Friend's movement:** Starts from spot $k$ moving backward: picks balls in sequence $b_k, b_{k-1}, \dots$.
- **Winning Condition:** When meeting at the middle spot ($\lfloor k/2 \rfloor$), the sequence of colors picked by you must match the sequence picked by your friend:
  $$b_1 = b_k, \quad b_2 = b_{k-1}, \quad \dots, \quad b_i = b_{k-i+1}$$
- This is mathematically equivalent to verifying whether the tape input string $w = b_1 b_2 \dots b_k$ is a **PALINDROME** ($w = w^R$)!

---

### 2. Concept of a Turing Machine with Storage
In a **Turing Machine with Storage in its Finite Control**:
- The state is not just a simple label $q$, but a **tuple**:
  $$[q, s]$$
  where:
  - $q \in Q$ is the primary control state (e.g., `scan_right`, `scan_left`, `check`).
  - $s \in \Sigma \cup \{B\}$ is a **memory register** that stores a symbol (the color of the ball currently being compared).
- This allows the TM head to read a ball color from one end, remember it in its internal register, travel to the opposite end, and verify if the corresponding ball matches the stored color.

---

### 3. Step-by-Step Machine Operation
Let marked/picked spots be replaced with a blank symbol $B$ (or marker $X$):

1. **Step 1 (Read and store leftmost ball):**
   - Head is at the leftmost unprocessed spot.
   - Read color $c \in \Sigma$.
   - Erase/mark the spot (write $B$).
   - Transition to state $[q_{right}, c]$, storing the color $c$ in the finite control register.
2. **Step 2 (Traverse to the right end):**
   - In state $[q_{right}, c]$, move right across remaining balls without altering them until the blank $B$ marking the right boundary is encountered.
3. **Step 3 (Compare with rightmost ball):**
   - Step one cell left to the rightmost unprocessed ball.
   - Read its color $c'$.
   - **Check match:**
     - If $c' == c$ (same color!): overwrite with $B$ (spot processed), and transition to state $q_{left}$.
     - If $c' \ne c$ (colors do not match): transition immediately to $q_{reject}$ (the sequences differ).
4. **Step 4 (Return to left end):**
   - In state $q_{left}$, move left across the tape until the left boundary $B$ is reached.
   - Step one cell right.
5. **Step 5 (Meeting condition / Termination):**
   - If the head finds no more balls (only $B$), or only one middle ball remains (when $k$ is odd), both players have successfully met at the middle with all pairs matched!
   - Transition to $q_{accept}$.

---

### 4. Formal Transition Definition
Let state set be $Q' = \{[q_{start}, -], [q_{right}, c], [q_{left}, -], q_{accept}, q_{reject}\}$ where $c \in \Sigma$:
- **Store & Move Right:**
  $$\delta([q_{start}, -], c) = ([q_{right}, c], B, R)$$
- **Travel Right:**
  $$\delta([q_{right}, c], x) = ([q_{right}, c], x, R) \quad \text{for any ball color } x \in \Sigma$$
- **At Right Boundary, Step to Last Ball:**
  $$\delta([q_{right}, c], B) = ([q_{check}, c], B, L)$$
- **Compare:**
  $$\delta([q_{check}, c], c) = ([q_{left}, -], B, L) \quad (\text{Match!})$$
  $$\delta([q_{check}, c], x) = (q_{reject}, x, S) \quad \text{for } x \ne c \quad (\text{Mismatch!})$$
- **Return Left:**
  $$\delta([q_{left}, -], x) = ([q_{left}, -], x, L)$$
  $$\delta([q_{left}, -], B) = ([q_{start}, -], B, R)$$
- **Acceptance:**
  $$\delta([q_{start}, -], B) = (q_{accept}, B, S)$$

---

### 5. Conclusion
By utilizing a **Turing Machine with storage in its finite control**, the machine stores each picked ball color in its state register, compares the symmetric positions from both ends, and decides in $O(k^2)$ steps whether both players selected the identical color sequence."""

# -----------------------------------------------------------------------------
# toc-2022-q8a (8 marks)
# Use the languages A = {a^m b^n c^n | m,n >= 0} and B = {a^n b^n c^m | m,n >= 0}
# to show whether Context-free language is closed under intersection and union.
# -----------------------------------------------------------------------------
SOLUTIONS_2022["toc-2022-q8a"] = r"""### 1. Preliminaries: Verifying $A$ and $B$ are Context-Free
Given the two languages:
$$A = \{a^m b^n c^n \mid m \ge 0, n \ge 0\}$$
$$B = \{a^n b^n c^m \mid m \ge 0, n \ge 0\}$$

Both $A$ and $B$ are Context-Free Languages (CFLs) because we can construct valid Context-Free Grammars for each:
- **CFG for $A$ ($G_A$):**
  $$\begin{aligned}
  S_A &\to M N \\
  M &\to aM \mid \epsilon \quad (\text{generates } a^m) \\
  N &\to bNc \mid \epsilon \quad (\text{generates } b^n c^n)
  \end{aligned}$$
- **CFG for $B$ ($G_B$):**
  $$\begin{aligned}
  S_B &\to P Q \\
  P &\to aPb \mid \epsilon \quad (\text{generates } a^n b^n) \\
  Q &\to cQ \mid \epsilon \quad (\text{generates } c^m)
  \end{aligned}$$

---

### 2. Part 1: Union of CFLs ($A \cup B$)
**Statement:** **Context-Free Languages ARE closed under Union.**

#### Proof using $A$ and $B$:
To form the union $A \cup B$, construct a new grammar $G_{union}$ with start symbol $S$:
$$S \to S_A \mid S_B$$
along with all productions of $G_A$ and $G_B$ (with disjoint variable names).
- Any derivation starting with $S \to S_A$ produces a string in $A$.
- Any derivation starting with $S \to S_B$ produces a string in $B$.
- Therefore, $L(G_{union}) = A \cup B$.

Since $G_{union}$ is a valid CFG, **$A \cup B$ is context-free**. CFLs are closed under union.

---

### 3. Part 2: Intersection of CFLs ($A \cap B$)
**Statement:** **Context-Free Languages are NOT closed under Intersection.**

#### Proof using $A$ and $B$:
Let us compute the intersection of $A$ and $B$:
- In language $A$, the number of $b$'s must equal the number of $c$'s ($n$), with any number of $a$'s ($m$).
- In language $B$, the number of $a$'s must equal the number of $b$'s ($n$), with any number of $c$'s ($m$).
- For a string to belong to BOTH $A$ and $B$:
  - The number of $a$'s must equal the number of $b$'s (from $B$).
  - The number of $b$'s must equal the number of $c$'s (from $A$).
  - Therefore, the number of $a$'s, $b$'s, and $c$'s must all be equal!

$$A \cap B = \{a^n b^n c^n \mid n \ge 0\}$$

#### Is $A \cap B$ context-free?
**NO.** The language $L_{3eq} = \{a^n b^n c^n \mid n \ge 0\}$ is the canonical non-context-free language (proven via the Pumping Lemma for CFLs, as a single pushdown stack cannot compare three independent counts simultaneously).

---

### 4. Conclusion
- Because $A$ and $B$ are both CFLs, and $A \cup B$ is generated by a CFG, **CFLs are closed under union**.
- Because $A$ and $B$ are both CFLs, but their intersection $A \cap B = \{a^n b^n c^n \mid n \ge 0\}$ is NOT a CFL, **CFLs are NOT closed under intersection**."""

# -----------------------------------------------------------------------------
# toc-2022-q8b (7 marks)
# Define Pumping lemma for CFG. Show L = {0^i 1^j | j = i^2} is not context-free
# grammar using Pumping lemma.
# -----------------------------------------------------------------------------
SOLUTIONS_2022["toc-2022-q8b"] = r"""### 1. Statement of the Pumping Lemma for CFLs
If $L$ is a Context-Free Language, then there exists a constant $p \ge 1$ (called the **pumping length**) such that any string $s \in L$ with length $|s| \ge p$ can be written as:
$$s = uvwxy$$
satisfying the following three mandatory conditions:
1. **Length condition:** $|vwx| \le p$
2. **Non-empty pump condition:** $|vx| \ge 1$ (at least one of $v$ or $x$ is non-empty)
3. **Pumping condition:** For all $k \ge 0$, the pumped string:
   $$u v^k w x^k y \in L$$

---

### 2. Proof that $L = \{0^i 1^j \mid j = i^2\}$ is Not Context-Free

#### Step 1: Assume $L$ is context-free
Assume, for contradiction, that $L$ is a CFL. Let $p$ be the pumping length given by the Pumping Lemma.

#### Step 2: Choose a string $s \in L$
Choose the test string:
$$s = 0^p 1^{p^2}$$
- Here $i = p$ and $j = p^2$, so $j = i^2$ is satisfied, and $s \in L$.
- The length is $|s| = p + p^2 \ge p$.

#### Step 3: Analyze the decomposition $s = uvwxy$
By Condition 1, $|vwx| \le p$. This means the substring $vwx$ has a maximum length of $p$.  
Now consider the possible positions of $vwx$ in $s = 0^p 1^{p^2}$:

- **Case 1: $vwx$ lies entirely within the `0`s ($vwx$ contains only `0`s):**
  - Then $v$ and $x$ consist entirely of `0`s ($|vx| = m \ge 1$ zeros, with no `1`s).
  - Pump with $k = 2$: the new string $s' = uv^2wx^2y$ has $p + m$ zeros, but the number of ones remains unchanged at $p^2$.
  - For $s' \in L$, we must have $(p + m)^2 = p^2$. But since $m \ge 1$, $(p + m)^2 = p^2 + 2pm + m^2 > p^2$.  
    Hence, $s' \notin L$.

- **Case 2: $vwx$ lies entirely within the `1`s ($vwx$ contains only `1`s):**
  - Then $v$ and $x$ consist entirely of `1`s ($|vx| = m \ge 1$ ones, with no `0`s).
  - Pump with $k = 2$: the number of zeros remains $p$, but the number of ones becomes $p^2 + m$.
  - For $s' \in L$, the number of ones must equal $p^2$. But $p^2 + m \neq p^2$ because $m \ge 1$.  
    Hence, $s' \notin L$.

- **Case 3: $vwx$ straddles the boundary between `0`s and `1`s:**
  - Since $|vwx| \le p$, $v$ can contain some `0`s and $x$ can contain some `1`s.
  - Let $v = 0^a$ and $x = 1^b$ where $a + b = |vx| \ge 1$ and $a + b \le p$.
  - Pump with $k = 2$:
    - The new number of zeros is $p + a$.
    - The new number of ones is $p^2 + b$.
  - For $s' \in L$, we must have:
    $$(p + a)^2 = p^2 + b \implies p^2 + 2pa + a^2 = p^2 + b \implies 2pa + a^2 = b$$
  - If $a = 0$, then $b \ge 1$, which gives $0 = b$ (impossible).
  - If $a \ge 1$, then $2pa + a^2 \ge 2p(1) + 1 = 2p + 1$.
  - But from $|vwx| \le p$, we know that $b \le p$.
  - This leads to:
    $$b = 2pa + a^2 \ge 2p + 1 > p \ge b$$
    A strict mathematical contradiction ($b > b$). Thus, $(p+a)^2 \neq p^2 + b$.  
    Hence, $s' \notin L$.

---

### 3. Conclusion
In every possible case, pumping $k=2$ produces a string $s' \notin L$, violating the Pumping Lemma.  
Therefore, our assumption is false, and $L = \{0^i 1^j \mid j = i^2\}$ is **NOT a context-free language**."""

if __name__ == "__main__":
    update_year_solutions(2022, SOLUTIONS_2022)
