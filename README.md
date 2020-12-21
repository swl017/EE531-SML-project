# Project Repo for EE531 Statistical Machine Learning

Code implementation of 
[**Group Fairness for the Allocation of Indivisible Goods**, Conitzer, AAAI 2019](https://users.cs.duke.edu/~conitzer/group-fairness-full.pdf)

The code reaches group fair results only by evaluating pair of individuals' local Nash optimality.
The number of players `n` and items `m` can be adjusted in `code/run_allocation.py`

## Sample Output
```python
player 0's preference: [ 259.   71.   22.   75.   73.]
player 1's preference: [ 491.    7.    0.    1.    1.]
player 2's preference: [ 127.   36.   54.    1.  282.]
player 3's preference: [ 496.    2.    0.    0.    2.]
player 4's preference: [ 275.    1.  173.   47.    4.]
A_all:[[ 3.  3.  3.  3.  3.]
 [ 0.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.]]
===========
Number of players: 5
Number of goods  : 15
Initial allocation: 
[[ 3.  3.  3.  3.  3.]
 [ 0.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.]]
Resulting allocation: 
[[ 0.  3.  0.  3.  0.]
 [ 2.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  3.]
 [ 1.  0.  0.  0.  0.]
 [ 0.  0.  3.  0.  0.]]
Values: 
v_0(A) = 438.0
v_1(A) = 982.0
v_2(A) = 846.0
v_3(A) = 496.0
v_4(A) = 519.0
Num of itereations = 400
Max valuation v(M) = 1500.0
```
