```
Entry

Block A [6]
(1) 	param a
(2) 	param b
(3) 	j <-- +, #2, a
(4) 	c <-- -, #1, j
(5) 	j <-- -, #1, j
(6) 	ifTrue #flag goto L4

Block B [3]
(7) 	L1: a <-- +, 1, c
(8) 	b <-- +, 1, a
(9) 	ifTrue #flag goto L3

Block C [2]
(10)	L2: a <-- +, a, b
(11)	ifTrue #flag goto L2

Block D [3]
(12)	L3: a <-- +, a, b
(13)	b <-- -, 1, a
(14)	ifTrue #flag goto L1

Block E [2]
(15)	L4: a <-- +, a, c
(16)	b <-- +, a, b

Exit
```

[('Entry', 'A'), ('A', 'E'), ('A', 'B'), ('B', 'D'), ('B', 'C'), ('C', 'C'), ('C', 'D'), ('D', 'B'), ('D', 'E'), ('E', 'Exit')]
### Control Flow Graph

![CFG_plt](cfg/draw_planar.png)

[('Entry', 'A'), ('A', 'B'), ('A', 'E'), ('B', 'C'), ('B', 'D'), ('E', 'Exit')]
### Dominator Tree

![DT_plt](dt/draw_planar.png)

| node =     | Entry   | A        | B           | C              | D              | E           | Exit              |
|:-----------|:--------|:---------|:------------|:---------------|:---------------|:------------|:------------------|
| Pred(node) | None    | Entry    | A, D        | B, C           | B, C           | A, D        | E                 |
| Dom(node)  | Entry   | Entry, A | Entry, A, B | Entry, A, B, C | Entry, A, B, D | Entry, A, E | Entry, A, E, Exit |
| Idom(node) | None    | Entry    | A           | B              | B              | A           | E                 |
| DF(node)   | None    | None     | B, E        | C, D           | B, E           | None        | None              |

```
Entry-block:
	def_Entry : {}
A-block:
	def_A : {}
	param a
		Globals : {a}
	param b
		Globals : {a, b}
	j <-- +, #2, a
		Globals : {a, b}
		def_A : {j}
		Blocks(j) : {A}
	c <-- -, #1, j
		def_A : {c, j}
		Blocks(c) : {A}
	j <-- -, #1, j
		def_A : {c, j}
		Blocks(j) : {A}
	ifTrue #flag goto L4
B-block:
	def_B : {}
	L1: a <-- +, 1, c
		Globals : {a, b, c}
		def_B : {a}
		Blocks(a) : {B}
	b <-- +, 1, a
		def_B : {a, b}
		Blocks(b) : {B}
	ifTrue #flag goto L3
C-block:
	def_C : {}
	L2: a <-- +, a, b
		Globals : {a, b, c}
		Globals : {a, b, c}
		def_C : {a}
		Blocks(a) : {B, C}
	ifTrue #flag goto L2
D-block:
	def_D : {}
	L3: a <-- +, a, b
		Globals : {a, b, c}
		Globals : {a, b, c}
		def_D : {a}
		Blocks(a) : {B, C, D}
	b <-- -, 1, a
		def_D : {a, b}
		Blocks(b) : {B, D}
	ifTrue #flag goto L1
E-block:
	def_E : {}
	L4: a <-- +, a, c
		Globals : {a, b, c}
		Globals : {a, b, c}
		def_E : {a}
		Blocks(a) : {B, C, D, E}
	b <-- +, a, b
		Globals : {a, b, c}
		def_E : {a, b}
		Blocks(b) : {B, D, E}
Exit-block:
	def_Exit : {}
```

| var =       | a          | b       | c    | j     |
|:------------|:-----------|:--------|:-----|:------|
| Blocks(var) | B, C, D, E | B, D, E | A    | A     |
| is Global   | True       | True    | True | False |

```
variable a:
	WorkList : {B, C, D, E}
	insert phi(*a) in B-block
	insert phi(*a) in E-block
	insert phi(*a) in C-block
	insert phi(*a) in D-block
variable b:
	WorkList : {B, D, E}
	insert phi(*b) in B-block
	insert phi(*b) in E-block
variable c:
	WorkList : {A}
```

### Needs a phi-function:

| block =   | Entry   | A   | B   | C   | D   | E   | Exit   |
|:----------|:--------|:----|:----|:----|:----|:----|:-------|
| a         | -       | -   | +   | +   | +   | +   | -      |
| b         | -       | -   | +   | -   | -   | +   | -      |
| c         | -       | -   | -   | -   | -   | -   | -      |
| j         | -       | -   | -   | -   | -   | -   | -      |

```
Rename(Entry):
    no phi-functions
    no instructions
    fill(A):
        no phi-functions
    Rename(A):
        no phi-functions
        rename instructions:
            param a_0
            param b_0
            j <-- +, #2, a_0
            c_0 <-- -, #1, j
        fill(E):
            a_0 <-- phi(a_0)
            b_0 <-- phi(b_0)
        fill(B):
            a_0 <-- phi(a_0)
            b_0 <-- phi(b_0)
        Rename(B):
            rename phi-functions:
                a_1 <-- phi(a_0)
                b_1 <-- phi(b_0)
            rename instructions:
                L1: a_2 <-- +, 1, c_0
                b_2 <-- +, 1, a_2
            fill(D):
                a_0 <-- phi(a_2)
            fill(C):
                a_0 <-- phi(a_2)
            Rename(C):
                rename phi-functions:
                    a_3 <-- phi(a_2)
                rename instructions:
                    L2: a_4 <-- +, a_3, b_2
                fill(C):
                    a_3 <-- phi(a_2, a_4)
                fill(D):
                    a_0 <-- phi(a_2, a_4)
                clean();
                return to B;
            Rename(D):
                rename phi-functions:
                    a_5 <-- phi(a_2, a_4)
                rename instructions:
                    L3: a_6 <-- +, a_5, b_2
                    b_3 <-- -, 1, a_6
                fill(B):
                    a_1 <-- phi(a_0, a_6)
                    b_1 <-- phi(b_0, b_3)
                fill(E):
                    a_0 <-- phi(a_0, a_6)
                    b_0 <-- phi(b_0, b_3)
                clean();
                return to B;
            clean();
            return to A;
        Rename(E):
            rename phi-functions:
                a_7 <-- phi(a_0, a_6)
                b_4 <-- phi(b_0, b_3)
            rename instructions:
                L4: a_8 <-- +, a_7, c_0
                b_5 <-- +, a_8, b_4
            fill(Exit):
                no phi-functions
            Rename(Exit):
                no phi-functions
                no instructions
                clean();
                return to E;
            clean();
            return to A;
        clean();
        return to Entry;
    clean();
```

```
Entry

Block A [6]
(1) 	param a_0
(2) 	param b_0
(3) 	j <-- +, #2, a_0
(4) 	c_0 <-- -, #1, j
(5) 	j <-- -, #1, j
(6) 	ifTrue #flag goto L4

Block B [5]
(7) 	L1: a_1 <-- phi(a_0, a_6)
(8) 	b_1 <-- phi(b_0, b_3)
(9) 	a_2 <-- +, 1, c_0
(10)	b_2 <-- +, 1, a_2
(11)	ifTrue #flag goto L3

Block C [3]
(12)	L2: a_3 <-- phi(a_2, a_4)
(13)	a_4 <-- +, a_3, b_2
(14)	ifTrue #flag goto L2

Block D [4]
(15)	L3: a_5 <-- phi(a_2, a_4)
(16)	a_6 <-- +, a_5, b_2
(17)	b_3 <-- -, 1, a_6
(18)	ifTrue #flag goto L1

Block E [4]
(19)	L4: a_7 <-- phi(a_0, a_6)
(20)	b_4 <-- phi(b_0, b_3)
(21)	a_8 <-- +, a_7, c_0
(22)	b_5 <-- +, a_8, b_4

Exit
```

