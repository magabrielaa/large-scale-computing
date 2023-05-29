from mpi4py import MPI
import time
from numba.pycc import CC
import numpy as np
import scipy.stats as sts
import compiled_aot # Import pre-compiled module

def parallel_simulation(n_runs):
    # Get rank of process and overall size of communicator:
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Start time:
    t0 = time.time()

    # Set model parameters
    rho = 0.5
    mu = 3.0
    sigma = 1.0
    z_0 = mu

    # Set simulation parameters, draw all idiosyncratic random shocks,
    # and create empty containers
    S = int(n_runs/size) # Evenly distribute number of simulation runs across processes
    T = 4160  # Set the number of periods for each simulation
    np.random.seed(rank) # Set rank as random seed
    eps_mat = sts.norm.rvs(loc=0, scale=sigma, size=(T, S))
    z_mat = np.zeros((T, S))

    # Run simulation with pre-compiled AOT module
    z_mat_aot = compiled_aot.loop_aot(S, T, z_0, eps_mat, rho, mu, z_mat)

    # Gather all simulation z_mat arrays to buffer of expected size/dtype on rank 0
    z_mat_all = None
    if rank == 0:
        z_mat_all = np.empty([S * size, T], dtype='float')
    comm.Gather(sendbuf=z_mat_aot, recvbuf=z_mat_all, root=0)

    # Print time elapsed
    if rank == 0:
        time_elapsed = time.time() - t0
        
        print("Simulated %d Parallelized Simulations in: %f seconds on %d MPI processes"
            % (n_runs, time_elapsed, size))
    
    return

def main():
    parallel_simulation(n_runs=1000)

if __name__ == '__main__':
    main() 