# ponder

```
C:\Users\Stefan>py ponder.py "p^q>r|q"
p q r  p^q>r|q
0 0 0  1
0 0 1  1
0 1 0  1
0 1 1  1
1 0 0  0
1 0 1  1
1 1 0  1
1 1 1  1
```

```
C:\Users\Stefan>py ponder.py "!p%T^q"
p T q  !p%T^q
0 1 0  1
0 1 1  0
0 1 0  1
0 1 1  0
1 1 0  0
1 1 1  1
1 1 0  0
1 1 1  1
```

```
C:\Users\Stefan>py ponder.py "(p|q>r)^s>p&s"
p q r s  (p|q>r)^s>p&s
0 0 0 0  0
0 0 0 1  1
0 0 1 0  0
0 0 1 1  1
0 1 0 0  1
0 1 0 1  0
0 1 1 0  0
0 1 1 1  1
1 0 0 0  1
1 0 0 1  1
1 0 1 0  0
1 0 1 1  1
1 1 0 0  1
1 1 0 1  1
1 1 1 0  0
1 1 1 1  1
```
