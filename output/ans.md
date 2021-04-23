```
Entry

Block A [4]
(1) 	k <-- n
(2) 	b <-- #1
(3) 	c <-- a
(4) 	ifTrue k = #0 goto L4

Block B [2]
(5) 	L1: t1 <-- %mod, k, #2
(6) 	ifFalse t1 = #0 goto L2

Block C [3]
(7) 	k <-- %div, k, #2
(8) 	c <-- *, c, c
(9) 	goto L3

Block D [2]
(10)	b <-- *, b, c
(11)	c <-- *, b, c

Block E [4]
(12)	L2: k <-- -, k, #1
(13)	k <-- %div, k, #2
(14)	c <-- *, c, c
(15)	b <-- *, b, c

Block F [1]
(16)	L3: goto L1

Block G [2]
(17)	c <-- *, c, c
(18)	k <-- %div, k, #4

Block H [1]
(19)	L4: return c

Exit
```

Detached blocks : ```{D, G}```

### Control Flow Graph

![CFG_plt](cfg/draw_planar.png)

### Dominator Tree

![DT_plt](dt/draw_planar.png)

| node =     | Entry   | A        | B           | C              | E              | F              | H           | Exit              |
|:-----------|:--------|:---------|:------------|:---------------|:---------------|:---------------|:------------|:------------------|
| Pred(node) | None    | Entry    | A, F        | B              | B              | C, E           | A           | H                 |
| Dom(node)  | Entry   | Entry, A | Entry, A, B | Entry, A, B, C | Entry, A, B, E | Entry, A, B, F | Entry, A, H | Entry, A, H, Exit |
| Idom(node) | None    | Entry    | A           | B              | B              | B              | A           | H                 |
| DF(node)   | None    | None     | B           | F              | F              | B              | None        | None              |

```
Entry-block:
	def_Entry : {}
A-block:
	def_A : {}
	k <-- n
		Globals : {n}
		def_A : {k}
		Blocks(k) : {A}
	b <-- #1
		def_A : {b, k}
		Blocks(b) : {A}
	c <-- a
		Globals : {a, n}
		def_A : {b, c, k}
		Blocks(c) : {A}
	ifTrue k = #0 goto L4
B-block:
	def_B : {}
	L1: t1 <-- %mod, k, #2
		Globals : {a, k, n}
		def_B : {t1}
		Blocks(t1) : {B}
	ifFalse t1 = #0 goto L2
C-block:
	def_C : {}
	k <-- %div, k, #2
		Globals : {a, k, n}
		def_C : {k}
		Blocks(k) : {A, C}
	c <-- *, c, c
		Globals : {a, c, k, n}
		def_C : {c, k}
		Blocks(c) : {A, C}
	goto L3
E-block:
	def_E : {}
	L2: k <-- -, k, #1
		Globals : {a, c, k, n}
		def_E : {k}
		Blocks(k) : {A, C, E}
	k <-- %div, k, #2
		def_E : {k}
		Blocks(k) : {A, C, E}
	c <-- *, c, c
		Globals : {a, c, k, n}
		def_E : {c, k}
		Blocks(c) : {A, C, E}
	b <-- *, b, c
		Globals : {a, b, c, k, n}
		def_E : {b, c, k}
		Blocks(b) : {A, E}
F-block:
	def_F : {}
	L3: goto L1
H-block:
	def_H : {}
	L4: return c
		Globals : {a, b, c, k, n}
Exit-block:
	def_Exit : {}
```

| var =       | a    | b    | c       | k       | n    | t1    |
|:------------|:-----|:-----|:--------|:--------|:-----|:------|
| Blocks(var) | None | A, E | A, C, E | A, C, E | None | B     |
| is Global   | True | True | True    | True    | True | False |

```
variable n:
	WorkList : {}
variable b:
	WorkList : {A, E}
	insert φ(*b) in F-block
	WorkList : {A, E, F}
	insert φ(*b) in B-block
	WorkList : {A, B, E, F}
variable k:
	WorkList : {A, C, E}
	insert φ(*k) in F-block
	WorkList : {A, C, E, F}
	insert φ(*k) in B-block
	WorkList : {A, B, C, E, F}
variable c:
	WorkList : {A, C, E}
	insert φ(*c) in F-block
	WorkList : {A, C, E, F}
	insert φ(*c) in B-block
	WorkList : {A, B, C, E, F}
variable a:
	WorkList : {}
```

### Needs a φ-function:

| block =   | Entry   | A   | B   | C   | D   | E   | F   | G   | H   | Exit   |
|:----------|:--------|:----|:----|:----|:----|:----|:----|:----|:----|:-------|
| a         | -       | -   | -   | -   | -   | -   | -   | -   | -   | -      |
| b         | -       | -   | +   | -   | -   | -   | +   | -   | -   | -      |
| c         | -       | -   | +   | -   | -   | -   | +   | -   | -   | -      |
| k         | -       | -   | +   | -   | -   | -   | +   | -   | -   | -      |
| n         | -       | -   | -   | -   | -   | -   | -   | -   | -   | -      |
| t1        | -       | -   | -   | -   | -   | -   | -   | -   | -   | -      |

```
Rename(Entry):
    no φ-functions
    no instructions
    fill(A):
        no φ-functions
    Rename(A):
        no φ-functions
        rename instructions:
            k₀ <-- n₀
            b₀ <-- #1
            c₀ <-- a₀
            ifTrue k₀ = #0 goto L4
        fill(H):
            no φ-functions
        fill(B):
            b₀ <-- φ(b₀)
            c₀ <-- φ(c₀)
            k₀ <-- φ(k₀)
        Rename(H):
            no φ-functions
            rename instructions:
                L4: return c₀
            fill(Exit):
                no φ-functions
            Rename(Exit):
                no φ-functions
                no instructions
                clean();
                return to H;
            clean();
            return to A;
        Rename(B):
            rename φ-functions:
                b₁ <-- φ(b₀)
                c₁ <-- φ(c₀)
                k₁ <-- φ(k₀)
            rename instructions:
                L1: t1 <-- %mod, k₁, #2
            fill(E):
                no φ-functions
            fill(C):
                no φ-functions
            Rename(C):
                no φ-functions
                rename instructions:
                    k₂ <-- %div, k₁, #2
                    c₂ <-- *, c₁, c₁
                fill(F):
                    b₀ <-- φ(b₁)
                    c₀ <-- φ(c₂)
                    k₀ <-- φ(k₂)
                clean();
                return to B;
            Rename(E):
                no φ-functions
                rename instructions:
                    L2: k₃ <-- -, k₁, #1
                    k₄ <-- %div, k₃, #2
                    c₃ <-- *, c₁, c₁
                    b₂ <-- *, c₃, c₃
                fill(F):
                    b₀ <-- φ(b₁, b₂)
                    c₀ <-- φ(c₂, c₃)
                    k₀ <-- φ(k₂, k₄)
                clean();
                return to B;
            Rename(F):
                rename φ-functions:
                    b₃ <-- φ(b₁, b₂)
                    c₄ <-- φ(c₂, c₃)
                    k₅ <-- φ(k₂, k₄)
                no instructions
                fill(B):
                    b₁ <-- φ(b₀, b₃)
                    c₁ <-- φ(c₀, c₄)
                    k₁ <-- φ(k₀, k₅)
                clean();
                return to B;
            clean();
            return to A;
        clean();
        return to Entry;
    clean();
```

```
Entry

Block A [4]
(1) 	k₀ <-- n₀
(2) 	b₀ <-- #1
(3) 	c₀ <-- a₀
(4) 	ifTrue k₀ = #0 goto L4

Block B [5]
(5) 	L1: b₁ <-- φ(b₀, b₃)
(6) 	c₁ <-- φ(c₀, c₄)
(7) 	k₁ <-- φ(k₀, k₅)
(8) 	t1 <-- %mod, k₁, #2
(9) 	ifFalse t1 = #0 goto L2

Block C [3]
(10)	k₂ <-- %div, k₁, #2
(11)	c₂ <-- *, c₁, c₁
(12)	goto L3

Block D [1]
(13)	pass

Block E [4]
(14)	L2: k₃ <-- -, k₁, #1
(15)	k₄ <-- %div, k₃, #2
(16)	c₃ <-- *, c₁, c₁
(17)	b₂ <-- *, c₃, c₃

Block F [4]
(18)	L3: b₃ <-- φ(b₁, b₂)
(19)	c₄ <-- φ(c₂, c₃)
(20)	k₅ <-- φ(k₂, k₄)
(21)	goto L1

Block G [1]
(22)	pass

Block H [1]
(23)	L4: return c₀

Exit
```

