import sys
from pathlib import Path
from apply_solutions import update_year_solutions

SOLUTIONS_2015 = {}

# -----------------------------------------------------------------------------
# toc-2015-q6a (8 marks)
# Define instantaneous description of a Turing Machine (TM). What is the role
# of checking off symbols in TM?
# -----------------------------------------------------------------------------
SOLUTIONS_2015["toc-2015-q6a"] = r"""### 1. Instantaneous Description (ID) of a Turing Machine

#### Definition:
An **Instantaneous Description (ID)** is a formal representation of the complete configuration of a Turing Machine at any single step in its computation.

It is written as:
$$\alpha_1 q \alpha_2$$
where:
- $q \in Q$ is the **current state** of the machine.
- $\alpha_1 \alpha_2 \in \Gamma^*$ represents the **contents of the tape** from the leftmost non-blank to the rightmost non-blank symbol.
- The head is currently positioned over the **first symbol of $\alpha_2$** (or over a blank symbol $B$ if $\alpha_2 = \epsilon$).

#### Move Relation ($\vdash$):
- **Right move:** If $\delta(q, X) = (p, Y, R)$, then $\alpha_1 q X \beta \vdash \alpha_1 Y p \beta$.
- **Left move:** If $\delta(q, X) = (p, Y, L)$, then $(\alpha_1 Z) q X \beta \vdash \alpha_1 p Z Y \beta$.

---

### 2. The Role of Checking Off Symbols in a Turing Machine

#### Why is Checking Off Needed?
Because a Turing Machine only has a sequential linear tape and no random-access memory, matching elements between different sections of the tape (e.g., verifying equal counts in $0^n 1^n$) requires repeated passes. "Checking off" is the practice of replacing an unprocessed input symbol with a marker symbol (e.g., $0 \to X, 1 \to Y$).

#### Roles & Advantages:
1. **Accurate Tracking (Accounting):** Guarantees each symbol is processed exactly once, preventing double-counting or skipping symbols during head sweeps.
2. **Boundary Signaling:** The marker symbols serve as physical endpoints during sweeps, telling the head where to stop and reverse direction.
3. **Guarantees Termination:** Since at least one symbol is checked off per cycle, the machine is guaranteed to terminate on finite inputs.
4. **Clean Restoration:** After the comparison completes, markers can be easily erased or restored to original values."""

# -----------------------------------------------------------------------------
# toc-2015-q6b (14 marks)
# Design a Turing Machine (TM) M to implement the function "Subtraction".
# Simulate the action for the input 00000100.
# -----------------------------------------------------------------------------
SOLUTIONS_2015["toc-2015-q6b"] = r"""### 1. Problem Formulation
Design a Turing Machine $M$ to compute **Proper Subtraction (Monus)**:
$$f(m, n) = m \dot{-} n = \begin{cases} m - n & \text{if } m \ge n \\ 0 & \text{if } m < n \end{cases}$$
- **Unary Input Format:** $0^m 1 0^n$
- **Test Input String:** `00000100` ($m = 5, n = 2$).
- **Expected Output:** $0^{5 - 2} = 0^3$ (`000`).

---

### 2. High-Level Algorithm
1. **Find and cross off the first zero of $m$:**
   - Replace the leftmost `0` with a blank symbol $B$.
2. **Travel right past the separator `1` into $n$:**
   - Find the first unmarked `0` of $n$ and cross it off (replace with a marker $X$, or blank $B$).
3. **Return to the left:**
   - Move left past the separator `1` back to the next unprocessed zero of $m$.
4. **Repeat:** Repeat steps 1–3 until all $n$ zeros have been matched and crossed off.
5. **Termination:**
   - When all $n$ zeros have been matched (head reaches the end of $n$ with no more zeros), the number of remaining $0$'s from $m$ is exactly $m - n$.
   - If $m < n$, all zeros of $m$ are erased, leaving 0 (or blank tape).

---

### 3. Transition Function Table ($\delta$)

| State | Symbol `0` | Symbol `1` | Marker `X` | Blank `B` |
| :---: | :---: | :---: | :---: | :---: |
| **$q_0$ (Pick 0 of $m$)** | $(q_1, B, R)$ | $(q_5, B, R)$ | — | — |
| **$q_1$ (Scan to $n$)** | $(q_1, 0, R)$ | $(q_2, 1, R)$ | — | — |
| **$q_2$ (Pick 0 of $n$)** | $(q_3, X, L)$ | $(q_{clean}, 1, L)$ | $(q_2, X, R)$ | $(q_4, B, L)$ |
| **$q_3$ (Return left to $m$)** | $(q_3, 0, L)$ | $(q_3, 1, L)$ | $(q_3, X, L)$ | $(q_0, B, R)$ |
| **$q_4$ (Clean up & halt)** | $(q_4, 0, L)$ | $(q_f, B, L)$ | $(q_4, B, L)$ | $(q_4, B, L)$ |

---

### 4. Step-by-Step Simulation on "00000100" ($5 \dot{-} 2$)
Initial tape: `00000100`

- **Round 1 (Match 1st zero):**
  1. $q_0 00000100 \vdash B q_1 0000100 \vdash \dots \vdash B00001 q_2 00$
  2. First zero of $n$ marked as $X$: tape becomes $B00001X0$
  3. Head returns left to first blank: enters $q_0$ scanning the second zero of $m$.

- **Round 2 (Match 2nd zero):**
  1. Head erases second zero: tape becomes $BB0001X0$
  2. Scans right past `1` and $X$, finds second zero of $n$ and marks it $X$:
     - Tape becomes $BB0001XX$
  3. Head returns left to blank, enters $q_0$ scanning the third zero of $m$.

- **Round 3 (Attempt Match 3):**
  1. Head erases third zero: tape becomes $BBB001XX$.
  2. Scans right past `1` and $XX$, reaches blank $B$!  
     All zeros of $n$ have already been matched!
  3. Machine realizes $n$ is completely exhausted, restores the third erased zero (or adjusts $B \to 0$), and erases $1XX$:
     - Tape becomes:
       $$\mathbf{000} \quad (\text{exactly } 3 \text{ zeros})$$

**Final Result:** `000` (representing $5 - 2 = 3$)."""

# -----------------------------------------------------------------------------
# toc-2015-q7a (10 marks)
# Define Chomsky Normal Form (CNF). Find a grammar in CNF equivalent to
# S -> aAbB
# A -> aA / a
# B -> bB / b
# -----------------------------------------------------------------------------
SOLUTIONS_2015["toc-2015-q7a"] = r"""### 1. Definition of Chomsky Normal Form (CNF)
A Context-Free Grammar $G = (V, T, P, S)$ is in **Chomsky Normal Form (CNF)** if every production rule is in one of the following two forms:
1. $A \to BC$ where $A, B, C \in V$ (a variable derives exactly two variables)
2. $A \to a$ where $A \in V$ and $a \in T$ (a variable derives exactly one terminal)

*(If $\epsilon \in L(G)$, the rule $S \to \epsilon$ is permitted, provided $S$ does not appear on the right-hand side of any production).*

---

### 2. Converting the Given Grammar to CNF

Given Grammar:
$$\begin{aligned}
S &\to aAbB \\
A &\to aA \mid a \\
B &\to bB \mid b
\end{aligned}$$

#### Step 1: Check for $\epsilon$, Unit, and Useless Productions
- **$\epsilon$-productions:** None.
- **Unit productions:** None.
- **Useless symbols:** All variables $\{S, A, B\}$ are generating and reachable.

#### Step 2: Introduce Variables for Terminals
Replace each terminal in composite production rules with a dedicated variable:
- Let $X_a \to a$
- Let $X_b \to b$

Substitute $X_a$ and $X_b$ into the grammar:
- $S \to aAbB \implies S \to X_a A X_b B$
- $A \to aA \implies A \to X_a A$
- $A \to a$ (already in valid CNF!)
- $B \to bB \implies B \to X_b B$
- $B \to b$ (already in valid CNF!)

#### Step 3: Break Bodies of Length $\ge 3$ into Pairs
The rule $S \to X_a A X_b B$ has a body of length 4. We break it down using new intermediate variables:
1. $S \to X_a C_1$
2. $C_1 \to A C_2$
3. $C_2 \to X_b B$

Now, all rules have bodies of length 2 (two variables) or length 1 (a single terminal).

---

### 3. Final Equivalent Grammar in CNF
$$\begin{aligned}
S &\to X_a C_1 \\
C_1 &\to A C_2 \\
C_2 &\to X_b B \\
A &\to X_a A \mid a \\
B &\to X_b B \mid b \\
X_a &\to a \\
X_b &\to b
\end{aligned}$$"""

# -----------------------------------------------------------------------------
# toc-2015-q7b (25 marks)
# Consider the following grammar
# S -> a | aA | B | C
# A -> aB | eps
# B -> Aa
# C -> cCD
# D -> ddd
# and simply safe order
# - (i) Eliminate eps-production.
# - (ii) Eliminate Unit Productions.
# - (iii) Eliminate Useless Symbols.
# - (iv) Put the grammar into CNF.
# -----------------------------------------------------------------------------
SOLUTIONS_2015["toc-2015-q7b"] = r"""### Problem Overview
We are given the context-free grammar:
$$\begin{aligned}
S &\to a \mid aA \mid B \mid C \\
A &\to aB \mid \epsilon \\
B &\to Aa \\
C &\to cCD \\
D &\to ddd
\end{aligned}$$
*(Variables: $S, A, B, C, D$; Terminals: $a, c, d$)*

We simplify and convert the grammar into Chomsky Normal Form (CNF) following the required safe order.

---

### Step (i): Eliminate $\epsilon$-Productions

1. **Find all nullable variables:**
   - Directly nullable: $A \to \epsilon \implies A$ is nullable.
   - For $B \to Aa$: contains terminal $a$, so $B$ is not nullable.
   - For $S$: $S \to a \mid aA \mid B \mid C$. Since $aA$ contains terminal $a$, $S$ cannot derive $\epsilon$.
   - **Only nullable variable:** $\{A\}$.

2. **Form new productions without $\epsilon$:**
   - **For $A \to aB \mid \epsilon$:**
     Drop $\epsilon \implies A \to aB$.
   - **For $B \to Aa$:**
     Keep or drop $A \implies B \to Aa \mid a$.
   - **For $S \to a \mid aA \mid B \mid C$:**
     From $aA$: $aA \mid a$.
     Thus: $S \to a \mid aA \mid B \mid C$.
   - **For $C$ and $D$:** Unchanged: $C \to cCD$, $D \to ddd$.

**Grammar after Step (i):**
$$\begin{aligned}
S &\to a \mid aA \mid B \mid C \\
A &\to aB \\
B &\to Aa \mid a \\
C &\to cCD \\
D &\to ddd
\end{aligned}$$

---

### Step (ii): Eliminate Unit Productions
Identify all unit productions $X \to Y$ ($X, Y \in V$):
- Unit pairs: $(S, B)$ and $(S, C)$.

Replace unit productions with non-unit productions:
- **For $B$:** Non-unit productions: $Aa \mid a$.
- **For $C$:** Non-unit production: $cCD$.
- **For $S$:**
  Replace $S \to B$ with $Aa \mid a$.
  Replace $S \to C$ with $cCD$.
  $$S \to a \mid aA \mid Aa \mid cCD$$

**Grammar after Step (ii):**
$$\begin{aligned}
S &\to a \mid aA \mid Aa \mid cCD \\
A &\to aB \\
B &\to Aa \mid a \\
C &\to cCD \\
D &\to ddd
\end{aligned}$$

---

### Step (iii): Eliminate Useless Symbols

1. **Phase 1: Identify Generating Symbols:**
   - Terminals: $\{a, c, d\}$.
   - $D \to ddd \implies D$ is generating.
   - $B \to a \implies B$ is generating.
   - $A \to aB \implies A$ is generating.
   - $S \to a \implies S$ is generating.
   - Look at $C$: the only production is $C \to cCD$. To generate a terminal string, $C$ requires $C$ to already derive terminals (no non-recursive base rule exists).  
     Therefore, **$C$ is non-generating!**
   - Discarding non-generating variable $C$ removes $C \to cCD$ and $S \to cCD$:
     $$\begin{aligned}
     S &\to a \mid aA \mid Aa \\
     A &\to aB \\
     B &\to Aa \mid a \\
     D &\to ddd
     \end{aligned}$$

2. **Phase 2: Identify Reachable Symbols (from $S$):**
   - Start with $S$: Reachable $= \{S\}$.
   - $S$ reaches $A$ (via $aA$ and $Aa$).
   - $A$ reaches $B$ (via $aB$).
   - Reachable variables: $\{S, A, B\}$.
   - Variable **$D$ is never reached from $S$!**
   - Discarding unreachable variable $D$ leaves:
     $$\begin{aligned}
     S &\to a \mid aA \mid Aa \\
     A &\to aB \\
     B &\to Aa \mid a
     \end{aligned}$$

---

### Step (iv): Put the Grammar into Chomsky Normal Form (CNF)

1. **Introduce variable for terminal $a$:**
   - Let $X_a \to a$

2. **Convert all productions to binary variables or single terminals:**
   - $S \to a$ (already in CNF!)
   - $S \to aA \implies S \to X_a A$
   - $S \to Aa \implies S \to A X_a$
   - $A \to aB \implies A \to X_a B$
   - $B \to Aa \implies B \to A X_a$
   - $B \to a$ (already in CNF!)

---

### Final CNF Grammar
$$\begin{aligned}
S &\to X_a A \mid A X_a \mid a \\
A &\to X_a B \\
B &\to A X_a \mid a \\
X_a &\to a
\end{aligned}$$"""

# -----------------------------------------------------------------------------
# toc-2015-q8a (6 marks)
# State Pumping lemma and its advantages?
# -----------------------------------------------------------------------------
SOLUTIONS_2015["toc-2015-q8a"] = r"""### 1. Statement of the Pumping Lemma for Context-Free Languages
If $L$ is a Context-Free Language, there exists a constant $p \ge 1$ (the pumping length) such that every string $s \in L$ with $|s| \ge p$ can be written as:
$$s = uvwxy$$
satisfying three properties:
1. $|vwx| \le p$
2. $|vx| \ge 1$ (at least one of $v$ or $x$ is non-empty)
3. For every integer $k \ge 0$, the pumped string:
   $$u v^k w x^k y \in L$$

---

### 2. Advantages of the Pumping Lemma
1. **Definitive Tool for Proving Non-Context-Freeness:**
   Provides an airtight, formal proof-by-contradiction framework to prove that a language cannot be generated by any context-free grammar.
2. **Defines Expressive Power of Pushdown Automata:**
   Reveals the core structural limitation of a single stack: a PDA cannot maintain more than two dependent counters simultaneously.
3. **Formal Verification in Language Hierarchy:**
   Serves as a fundamental milestone in classifying languages within the Chomsky Hierarchy (distinguishing CFLs from Context-Sensitive and Turing-Recognizable languages)."""

# -----------------------------------------------------------------------------
# toc-2015-q8b (10 marks)
# Show that the following languages are not context-free:
# - (i) L = {w \in {a,b,c}* : w has equal numbers of a's and b's and c's}
# - (ii) L = {a^n b^m a^n : n >= m}
# -----------------------------------------------------------------------------
SOLUTIONS_2015["toc-2015-q8b"] = r"""### Part (i): Prove $L_1 = \{w \in \{a,b,c\}^* \mid \#_a(w) = \#_b(w) = \#_c(w)\}$ is NOT Context-Free

#### Method 1: Closure Under Intersection with Regular Languages (Quickest & Most Elegant)
1. Recall the closure theorem: *The intersection of a Context-Free Language and a Regular Language is always Context-Free.*
2. Assume, for contradiction, that $L_1$ is context-free.
3. The language $R = a^* b^* c^*$ is a regular language.
4. Intersect $L_1$ with $R$:
   $$L_1 \cap R = \{a^n b^n c^n \mid n \ge 0\}$$
5. But $\{a^n b^n c^n \mid n \ge 0\}$ is famously NOT context-free!
6. This contradicts the closure property. Therefore, $L_1$ cannot be context-free.

#### Method 2: Direct Pumping Lemma Proof
- Select $s = a^p b^p c^p \in L_1$.
- Any decomposition $s = uvwxy$ with $|vwx| \le p$ means $vwx$ can contain at most two of the three symbols $\{a, b, c\}$.
- Pumping $k=2$ increases the count of at most two symbols while leaving the third unchanged, breaking the equality $\#_a = \#_b = \#_c$. Hence $s' \notin L_1$.

---

### Part (ii): Prove $L_2 = \{a^n b^m a^n \mid n \ge m\}$ is NOT Context-Free

#### 1. Assume $L_2$ is a CFL
Assume, for contradiction, that $L_2$ is a CFL with pumping length $p \ge 1$.

#### 2. Choose test string $s \in L_2$
Choose:
$$s = a^p b^p a^p$$
- Here the prefix has $p$ $a$'s, middle has $p$ $b$'s, suffix has $p$ $a$'s.
- Since $n = p$ and $m = p$, $n \ge m$ holds, so $s \in L_2$.
- Length: $|s| = 3p \ge p$.

#### 3. Properties of decomposition $s = uvwxy$
By the Pumping Lemma:
- $|vwx| \le p$
- $|vx| \ge 1$
- $u v^k w x^k y \in L_2$ for all $k \ge 0$.

Because $|vwx| \le p$, the substring $vwx$ **cannot contain $a$'s from both the first block of $a$'s and the second block of $a$'s**, because they are separated by $b^p$ of length $p$.

#### 4. Case Analysis on $vwx$:
- **Case 1: $vwx$ lies completely in the first half ($a^p b^p$):**
  - Pump DOWN with $k = 0$ ($s' = uwy$).
  - At least one symbol from the first $a^p$ or $b^p$ is deleted.
  - If any $a$ from the first block is deleted, the prefix number of $a$'s becomes $n' < p$. But the suffix number of $a$'s is still $p$.  
    Then prefix and suffix counts are unequal ($n' \ne p$), so $s'$ is no longer of the form $a^n b^m a^n$! Thus $s' \notin L_2$.
- **Case 2: $vwx$ lies completely in the second half ($b^p a^p$):**
  - Symmetric to Case 1: pumping $k=0$ deletes some $a$'s from the suffix, making suffix $a$'s fewer than prefix $a$'s. Thus $s' \notin L_2$.
- **Case 3: $vwx$ lies entirely within the middle block $b^p$:**
  - Then $vx$ consists exclusively of $b$'s ($|vx| = d \ge 1$).
  - Pump UP with $k = 2$: the number of $b$'s becomes $m' = p + d > p$.
  - But the prefix and suffix number of $a$'s remain $n = p$.
  - Now check condition $n \ge m'$:
    $$p \ge p + d$$
    Since $d \ge 1$, $p \ge p + 1$, which is impossible! Thus $s' \notin L_2$.

#### Conclusion:
In all cases, a contradiction is reached. Therefore, $L_2 = \{a^n b^m a^n \mid n \ge m\}$ is **NOT context-free**."""

# -----------------------------------------------------------------------------
# toc-2015-q8c (9 marks)
# Prove that context free languages are closed under (i) Homomorphism (ii) Reversal
# -----------------------------------------------------------------------------
SOLUTIONS_2015["toc-2015-q8c"] = r"""### Part (i): Prove CFLs are Closed under Homomorphism

#### Definition:
Let $\Sigma$ and $\Gamma$ be alphabets. A homomorphism $h: \Sigma \to \Gamma^*$ is a mapping from each symbol of $\Sigma$ to a string over $\Gamma$.  
For any string $w = a_1 a_2 \dots a_k$, $h(w) = h(a_1) h(a_2) \dots h(a_k)$.  
For a language $L$, $h(L) = \{h(w) \mid w \in L\}$.

#### Proof:
Let $L$ be a context-free language generated by grammar $G = (V, \Sigma, P, S)$.  
Construct a new grammar $G' = (V, \Gamma, P', S)$ where:
- The variables $V$ and start symbol $S$ remain identical.
- For each production rule $A \to \alpha \in P$, define a corresponding rule in $P'$:
  $$A \to h(\alpha)$$
  where each terminal $a \in \Sigma$ in $\alpha$ is replaced with the string $h(a)$, and all variables in $\alpha$ are left unchanged.

**Correctness:**
- Every derivation $S \Rightarrow^* w$ in $G$ corresponds directly to a derivation $S \Rightarrow^* h(w)$ in $G'$.
- Since every rule in $P'$ still has a single variable on the left-hand side ($A \in V$), $G'$ is a valid Context-Free Grammar.
- Therefore, $L(G') = h(L)$, proving **CFLs are closed under homomorphism**.

---

### Part (ii): Prove CFLs are Closed under Reversal

#### Definition:
For any string $w = a_1 a_2 \dots a_k$, its reversal is $w^R = a_k a_{k-1} \dots a_1$.  
The reversed language is $L^R = \{w^R \mid w \in L\}$.

#### Proof:
Let $L$ be generated by CFG $G = (V, T, P, S)$.  
Construct a reversed grammar $G^R = (V, T, P^R, S)$ where:
- The variables $V$, terminals $T$, and start symbol $S$ remain unchanged.
- For each production $A \to \alpha \in P$, add the reversed production to $P^R$:
  $$A \to \alpha^R$$
  *(For example, if $A \to a B C$, then $P^R$ has $A \to C B a$).*

**Correctness:**
- By induction on parse tree derivations:
  $$A \Rightarrow^* w \text{ in } G \iff A \Rightarrow^* w^R \text{ in } G^R$$
- Each production in $P^R$ has a single variable on the left, so $G^R$ is a valid CFG.
- Hence, $L(G^R) = L^R$, proving **CFLs are closed under reversal**."""

# -----------------------------------------------------------------------------
# toc-2015-q8d (10 marks)
# Define DPDA. Let \Sigma={0, 1}, consider the problem of testing whether a PDA
# accepts some string of the form { w \in 0^* 1^* }. Is this problem decidable?
# Prove your answer.
# -----------------------------------------------------------------------------
SOLUTIONS_2015["toc-2015-q8d"] = r"""### 1. Definition of a Deterministic Pushdown Automaton (DPDA)
A **Deterministic Pushdown Automaton (DPDA)** is a 7-tuple:
$$P = (Q, \Sigma, \Gamma, \delta, q_0, Z_0, F)$$
satisfying two strict determinism conditions for all states $q \in Q$, tape/input symbols $a \in \Sigma$, and stack symbols $X \in \Gamma$:
1. **Uniqueness:** $|\delta(q, a, X)| \le 1$ and $|\delta(q, \epsilon, X)| \le 1$  
   *(At most one transition is possible for any state, input symbol, and stack top).*
2. **No Conflict between $\epsilon$ and Input Moves:**  
   If $\delta(q, \epsilon, X) \ne \emptyset$, then $\delta(q, a, X) = \emptyset$ for all $a \in \Sigma$.  
   *(The machine cannot have a choice between making an $\epsilon$-transition and reading an input symbol).*

---

### 2. Is the Problem Decidable?
The question asks:  
> *"Given an arbitrary PDA $P$, does $P$ accept at least one string from $0^* 1^*$?"*  
In mathematical terms: Is $L(P) \cap 0^* 1^* \ne \emptyset$?

**Direct Answer:** **YES, this problem is DECIDABLE.**

---

### 3. Step-by-Step Proof of Decidability

#### Step 1: Characterize the Languages
- Let $L_1 = L(P)$ be the language accepted by the given PDA $P$. Since $P$ is a PDA, $L_1$ is a **Context-Free Language (CFL)**.
- Let $R = 0^* 1^*$. $R$ is a **Regular Language** (recognized by a simple 2-state DFA).

#### Step 2: Closure Property (CFL $\cap$ Regular is CFL)
A fundamental theorem of formal language theory states:
> *"The intersection of any Context-Free Language with a Regular Language is always a Context-Free Language."*

We can construct a product Pushdown Automaton $P'$ such that:
$$L(P') = L(P) \cap R = L(P) \cap 0^* 1^*$$
- **Construction Idea:** $P'$ runs the PDA $P$ and the DFA for $0^* 1^*$ in parallel.
  - The stack of $P'$ operates identically to the stack of $P$.
  - The finite control of $P'$ tracks pairs of states $[q_{pda}, q_{dfa}]$.
  - $P'$ accepts if and only if both the PDA and the DFA reach their respective accepting states.

#### Step 3: Emptiness Testing for CFLs
Now the problem reduces to:
$$\text{"Is } L(P') \ne \emptyset\text{?"}$$
- We can convert the PDA $P'$ into an equivalent Context-Free Grammar $G'$.
- Testing whether a CFG generates any strings (the **Emptiness Problem for CFGs**, $L(G') = \emptyset$) is **DECIDABLE**:
  - Run the algorithm to identify all **generating variables** of $G'$.
  - If the start symbol $S$ is generating, then $L(P') \ne \emptyset$ (meaning $P$ accepts at least one string in $0^* 1^*$).
  - If $S$ is not generating, then $L(P') = \emptyset$.

Since both the cross-product construction and the generating symbols algorithm terminate in finite time, the decision problem is **decidable**."""

if __name__ == "__main__":
    update_year_solutions(2015, SOLUTIONS_2015)
