# A1

All the code and analysis can be found in the Jupyter Notebook [here](https://github.com/macs30113-s23/a1-magabrielaa/blob/main/assignment_1.ipynb) but it is also repeated below in this self-contained README.md

## Question 1
### Part (a)
For part (a), I captured the nested loop of the original code in a function called `loop`  and created a new function called `loop_jit` that contains the
same nested for loop but with the `@jit` decorator.

```python
# Original version
def loop (S,T,z_0,eps_mat,rho,mu,z_mat):
    for s_ind in range(S):
        z_tm1 = z_0
        for t_ind in range(T):
            e_t = eps_mat[t_ind, s_ind]
            z_t = rho * z_tm1 + (1 - rho) * mu + e_t
            z_mat[t_ind, s_ind] = z_t
            z_tm1 = z_t
    return z_mat

# Jit-accelerated version
@jit(nopython=True)
def loop_jit (S,T, z_0,eps_mat, rho, mu, z_mat):
    for s_ind in range(S):
        z_tm1 = z_0
        for t_ind in range(T):
            e_t = eps_mat[t_ind, s_ind]
            z_t = rho * z_tm1 + (1 - rho) * mu + e_t
            z_mat[t_ind, s_ind] = z_t
            z_tm1 = z_t
    return z_mat
```
Then, I timed both functions in two rounds. First, I used `%time` to measure the time to run each function in one iteration:

```python
# Original version time
%time loop(S,T,z_0,eps_mat,rho,mu, z_mat)

CPU times: user 3.21 s, sys: 3.85 ms, total: 3.21 s
Wall time: 3.4 s
```

```python
# Jit version FIRST time will include compilation time
%time loop_jit(S,T,z_0,eps_mat,rho,mu, z_mat)

CPU times: user 222 ms, sys: 1.89 ms, total: 224 ms
Wall time: 225 ms
```

```python
# Jit version after initial compilation
%time loop_jit(S,T,z_0,eps_mat,rho,mu, z_mat)

CPU times: user 51.8 ms, sys: 0 ns, total: 51.8 ms
Wall time: 53 ms
```
#### Results in one iteration:
When using `%time`, I get that the original version runs in **3.21 s**. In comparison, the jit-version takes **224 ms** the first time, which is already considerably faster than the original version.However, it should be noted that this first timing includes the compilation time. When I run the jit-version a second time, as expected, it is runs much faster, now in **51.8 ms** because it is already pre-compiled.


Next, I compare both version by using `%timeit`, which times how long it takes to run each function across multiple iterations and therefore provides a more reliable time count. This is the code I used and accompanying output:

```python
# Now, run the original version and time it in several iterations
%timeit loop(S,T,z_0,eps_mat,rho,mu, z_mat)

3.71 s ± 638 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
```

```python
# Likewise, time jit-accelerated version with several iterations
%timeit loop_jit(S,T,z_0,eps_mat,rho,mu, z_mat)

83.4 ms ± 3.89 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
```

### Results in multiple iterations:

When timed in multiple runs, the original version runs in **3.71 s** vs. **83.4 ms** with the jit-accelerated version. This is a **significant speed-up** and shows that when we use NumPy arrays and for loops, Numba performs best as a compiler and results in efficiency gains. Even though on average, `%timeit` gives a run time of 83.4 ms for the jit-version compared to the 51.8 ms I got with `%time` in the second run, it is still below the 224 ms time from the first run, which included the compilation time.

### Part (b)
Here, I created a pre-compiled module with the following code:

```python
from numba.pycc import CC

# name of compiled module to create:
cc = CC('compiled_aot')

# name of function in module, with explicit data types required
@cc.export('loop_aot', 'f8[:, :](i4, i4, f4, f8[:, :], f4, f4, f8[:, :])')
def loop_aot(S, T, z_0, eps_mat, rho, mu, z_mat):
  for s_ind in range(S):
    z_tm1 = z_0
    for t_ind in range(T):
        e_t = eps_mat[t_ind, s_ind]
        z_t = rho * z_tm1 + (1 - rho) * mu + e_t
        z_mat[t_ind, s_ind] = z_t
        z_tm1 = z_t
  return z_mat

cc.compile()
```

Then, I import the generated pre-compiled module and use `%timeit` to measure how long it takes to run.

```python
import compiled_aot

# Time compiled version with several iterations
%timeit compiled_aot.loop_aot(S, T, z_0, eps_mat, rho, mu, z_mat)

31.3 ms ± 477 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
```
# Results from pre-compiled code:

Using %timeit, I get that the pre-compiled version runs in **31.3 ms**, compared to **3.71 s** (ie. 3710 ms) with the original version. The pre-compiled version is therefore 3678.7 ms faster than the original version, a considerable speedup.


### Part (c)
Given that the original version, as measured with %timeit, runs in 3.71 s (ie. **3710 ms**):
<br>
<br> **Speedup difference between original and @jit version**
<br> = 83.4 ms - 3710 ms = **-3626.6 ms**
<br>
<br> **Speedup difference between original and pre-compiled AOT version**
<br> = 31.3 ms - 3710 ms = **-3678.7 ms**

<br>
The pre-compiled version is faster than the @jit version by **52.1 ms** (ie. 31.3 ms - 83.4 ms). If we calculate the percentage difference, this is equivalent to 83.9%, that is to say, the pre-compiled AOT version is 90.85% faster than the @jit version. One of the reasons that ahead-of-time compilation is faster than just-in-time is because the data types are explicitly specified before the compiling takes place. In AOT, the signature needs to specify the data types, which allows the compiler to create machine code that is optimized for the specific data types that will be processed **ahead of time**. In contrast, @jit infers the data types at runtime, which is relatively slower (compared to AOT),but gives more flexibility for cases where the data types might change through the execution of the code.
<br>
<br>
It makes sense to use @jit when we are in a production mode that is subject to constant changes/adjustments in the code. In the AOT case, we have to pre-compile a new module each time we make a change in the compilation code, which takes additional time. Once the code is set, using the AOT is beneficial because it is faster and it needs to be pre-compiled only once.
<br>
<br>
If the data types change during the execution, then it is preferrable to use @jit because it infers the type dynamically, whereas with AOT, the types are fixed ahead of the compilation and cannot be changed during the execution.
<br>
<br>
The AOT compilation module that is generated is specific to a particular architecture and OS so the module cannot simply be shared between architectures as it will not work. If there is a need to share code, then using @jit would be better.
<br>
<br>
If the size of the problem is very large, with a big number of simulations, then the AOT compiler is a better choice as it has more speedup than @jit.


## Question 2

*  The model parameters are fixed values, so they **cannot be parallelized**.

  * rho = 0.5
  * mu = 3.0
  * sigma = 1.0
  * z_0 = mu

* In the simulation parameters: S, T, the random seed, and the initial z_mat (which is a zero matrix) are all fixed/given at the beginning of the model and therefore **cannot be parallelized** as they happen in one single moment.

  * S = 1000
  * T = 4160 
  * np.random.seed(25)
  * z_mat = np.zeros((T, S))

* We are assuming that the generation of eps_mat **cannot be parallelized** and must occurr in a single process.
  * eps_mat = sts.norm.rvs(loc=0, scale=sigma, size=(T, S))

* The nested for loop can be **parallelized** because each iteration in the loop is independent from one another and there are no dependencies between runs. This is an example of a Monte Carlo simulation, which is parallelizable.

### EXPECTATION

I expect the theoretical speedup to be dictated by Amdalh's law rather than Gustafson's because Amdalh assumes the size of the problem is fixed.
<br>
<br>
In our Monte Carlo simulation, we have a **fixed problem size** because we are running a set/fixed number of 1000 lifetimes of health shocks, with each lifetime equivalent to 4160 weeks. Therefore, the theoretical speedup for this application, as it is currently defined, will not be linear. Below I calculate the theoretical speedups using both laws.

### THEORETICAL SPEED UP CALCULATIONS
Since only the nested for loop can be parallelized, to calculate the theoretical speed-ups, I need to know the approximate percentage of the time that is run by the serial vs. potentially parallelizable code.

```python
# (1) Create function that contains the serial portion of the code

def serial_parameters():
  # Set model parameters
  rho = 0.5
  mu = 3.0
  sigma = 1.0
  z_0 = mu

  # Set simulation parameters, draw all idiosyncratic random shocks,
  # and create empty containers
  S = 1000  # Set the number of lives to simulate
  T = 4160  # Set the number of periods for each simulation
  np.random.seed(25)
  eps_mat = sts.norm.rvs(loc=0, scale=sigma, size=(T, S))
  z_mat = np.zeros((T, S))

# (2) Create function that contains the potentially-parallelizable portion
# of the code
def parallel_loop (S,T,z_0,eps_mat,rho,mu,z_mat):
  for s_ind in range(S):
      z_tm1 = z_0
      for t_ind in range(T):
          e_t = eps_mat[t_ind, s_ind]
          z_t = rho * z_tm1 + (1 - rho) * mu + e_t
          z_mat[t_ind, s_ind] = z_t
          z_tm1 = z_t
  return z_mat
```
Then, I time how long it takes to run each portion of the code.

```python
# Time serial portion of the code
%timeit serial_parameters()

176 ms ± 22.3 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
```

```python
# Time potentially parallelizable portion of the code
%timeit parallel_loop (S,T,z_0,eps_mat,rho,mu,z_mat)

3.56 s ± 517 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
```

The total run-time for the simulation is given by:

<br> S + P = 1 = 100%
<br> 176 ms + 3560 ms = 3736 ms
<br>

<br> Then, the serial and parallelizable percentages are:

<br> **Serial %**= 176 ms / 3736 ms = 0.050 = 5%
<br> **Parallel %** = 3560 ms / 3736 ms = 0.95 = 95%

### AMDALH'S LAW

Calculates the potential speedup based on the amount of the code that is parallel. It estimates the theoretical speedup of a fixed-sized problem as the number of processors increase. 

Formula: Speedup(N) = 1 / (S + P/N)

I wrote the following code to get the theoretical speedup with Amdalh's Law:

```python
s = 0.05
p = 0.95
# Calculate Amdalh's speed up with 1 processor
print("1 processor Amdalh speed up", 1 / ((s) + (p/1)))

# Calculate Amdalh's speed up with 10 processors
print("10 processor Amdalh speed up", 1 / ((s) + (p/10)))

# Calculate Amdalh's speed up with 100 processors
print("100 processor Amdalh speed up", 1 / ((s) + (p/100)))
```

Results:

```python
1 processor Amdalh speed up 1.0
10 processor Amdalh speed up 6.896551724137931
100 processor Amdalh speed up 16.806722689075627
```

### GUSTAFSON'S LAW

Calculates the potential speedup if the size of the problem grows proportionally to the number of processors. It states that parallel code runs should increase the size of the problem as more processors are added.

**Formula:** Speedup(N) = N - S * (N - 1)

```python
s = 0.05
p = 0.95

# Calculate Gustafson's speed up with 1 processor
print("1 processor Gustafson speed up", 1 - s * (1 - 1))

# Calculate Gustafson's speed up with 10 processors
print("10 processor Gustafson speed up", 10 - s * (10 - 1))

# Calculate Gustafson's speed up with 10 processors
print("100 processor Gustafson speed up", 100 - s * (100 - 1))
```

Results:

```python
1 processor Gustafson speed up 1.0
10 processor Gustafson speed up 9.55
100 processor Gustafson speed up 95.05
```

### CONCLUSION

With Amdalh's Law, as expected, there is no linear speedup because 5% of the code is serial. This means that there is some speedup as we increase the number of of processors, but the speed performance gains we get in return are **not linear** as we increase the number of processors. That is, the speed up goes from 1 to 6.9 to 16.8 as we increase from 1 to 10 to 100 processors. No matter how fast the parallel portion of the code is, we are limited by the serial portion so there is a cap in the speedup we can gain. 

This is likely to be the theoretical speedup for this particular application, because the **size of the problem is fixed**: 1000 lifetimes of health shocks, each lifetime equivalent to 4160 weeks.

In contrast, with Gustafson's Law, the theoretical speedup is linear as we increase the number of processors. The potential speedup increases from 1 to 9.6 to 95.1 as we increase from 1 to 10 to 100 processors. This tells us that a larger problem can be solved in the same amount of time if we have more processors. Here, the speedup is entirely dependent on the number of processors N. If we were to increase the number of simulations in our application, then the theoretical speedup would be dictated by Gustafson's Law.