from numba.pycc import CC
import numpy as np
import scipy.stats as sts
import timeit
import time

# name of compiled module to create:
cc = CC('compiled_aot')

# name of function in module, with explicit data types required
@cc.export('loop_aot', 'f8[:, :](i4, i4, f8, f8[:, :], f8, f8, f8[:, :])')
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

# Import pre-compiled module
import compiled_aot

# Start time:
t0 = time.time()

# Set model and simulation parameters
rho = 0.5
mu = 3.0
sigma = 1.0
z_0 = mu
S = 1000
T = 4160 
np.random.seed(25)
eps_mat = sts.norm.rvs(loc=0, scale=sigma, size=(T, S))
z_mat = np.zeros((T, S))

# Run compiled function
compiled_aot.loop_aot(S, T, z_0, eps_mat, rho, mu, z_mat)


# Print time elapsed
time_elapsed = time.time() - t0
print(f'AOT-compiled simulation in: {time_elapsed} seconds')