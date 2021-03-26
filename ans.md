```
Entry

Block A (4)
(1) 	param p
(2) 	param q
(3) 	param r
(4) 	q0 <-- #0

Block B (1)
(5) 	L1: ifTrue q0 >= p goto L2

Block C (14)
(6) 	q0 <-- +, q0,  r
(7) 	q1 <-- +, p,   q
(8) 	r  <-- *, r,  #2
(9) 	q2 <-- +, p,   q
(10)	q0 <-- +, p,  #1
(11)	q2 <-- +, q0,  r
(12)	s  <-- +, q2,  q
(13)	s  <-- +,  s,  q
(14)	q2 <-- +, p,   q
(15)	q3 <-- -, q2, q1
(16)	q3 <-- -, q2, q3
(17)	q3 <-- +,  p,  q
(18)	q1 <-- -, q3,  s
(19)	ifTrue q < #256 goto L1

Block D (5)
(20)	q3 <-- +, q0, q1
(21)	s  <-- +, q2, q3
(22)	p  <-- -, s,  p
(23)	r  <-- -, r,  #256
(24)	goto L1

Block E (2)
(25)	L2: q <-- *, p,   q
(26)	return q

Exit
```

Control Flow Graph

![CFG](cfg/1.png)

Dominator Tree

![DT](dt/1.png)

| node=      | A    | B       | C       | D          | E       |
|:-----------|:-----|:--------|:--------|:-----------|:--------|
| Pred(node) | None | A, C, D | B       | C          | B       |
| Dom(node)  | A    | A, B    | A, B, C | A, B, C, D | A, B, E |
| Idom(node) | None | A       | B       | C          | B       |
| DF(node)   | None | B       | B       | B          | None    |
