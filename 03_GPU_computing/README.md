# GPU VS. CPU COMPUTING

Normalized Difference Vegetation Index" (NDVI)
Calculated using Spectral Bands 4 (Red) and 5 (Near Infrared – NIR) - scale from 0 to 1
Urban areas: 0, rural areas: 1

## Question 1
- I replicated the original serial NDVI computation in this file: [q1_serial.py](https://github.com/magabrielaa/large-scale-computing/blob/main/03_GPU_computing/q1/serial/q1_serial.py). The corresponding sbatch file is [q1_serial.sbatch](https://github.com/magabrielaa/large-scale-computing/blob/main/03_GPU_computing/q1/serial/q1_serial.sbatch), which runs the code on one CPU core using the broadwl partition.

    - The serial version of NDVI runs in **0.114404 seconds**, which is contained in [q1_serial.out](https://github.com/magabrielaa/large-scale-computing/blob/main/03_GPU_computing/q1/serial/q1_serial.out)

- For the parallelizable version of NDVI, I wrapped the NDVI calculation with numba, using the vectorize decorator in a file called [q1_parallel.py](https://github.com/magabrielaa/large-scale-computing/blob/main/03_GPU_computing/q1/parallel/q1_parallel.py) as follows:

    ```python
    @vectorize(['f8(f8, f8)'], target='cuda')
    def parallel_ndvi(red, nir):
        ndvi = (nir - red) / (nir + red) # NDVI calculation
        return ndvi
    ```
    - The corresponding sbatch file is [q1_parallel.sbatch](https://github.com/magabrielaa/large-scale-computing/blob/main/03_GPU_computing/q1/parallel/q1_parallel.sbatch), in which I request one GPU node and one CPU host to drive the GPU.

    - The parallel version with Numba on a GPU runs in **0.256568 seconds**, which is logged in [q1_parallel.out](https://github.com/magabrielaa/large-scale-computing/blob/main/03_GPU_computing/q1/parallel/q1_parallel.out)


## Question 2
In comparison, the parallelized GPU implementation runs **slower** than the CPU serial implementation. For a given application to run faster on a GPU vs. a CPU, it has to be either computationally intensive or massively parallel. The dataset we are working with is _small_, with an np.shape of (1338, 2107). At this size, we don't yet see the speedup benefits of running the NDVI calculation in a GPU.

In GPU programming there are two bottlenecks that represent an overhead: transferring inputs from the HOST CPU to the DEVICE GPU and transferring the results back from the DEVICE GPU to the HOST CPU. If the database is small, this overhead outweights the benefits of parallelism and the CPU can perform computations more efficiently. Also, CPU's perform better with serial code than do GPU's. In this application, there is still a considerable proportion of the total code that is serial, hence why it is faster on a CPU.

CPU's have bigger (and fewer) cores, so they run eally fast. In contrast, GPU's have a lot more cores but run much slower. The benefit of GPU's comes at massively parallel applications, because the parallelizable code can be run in a lot more cores _simulatenously_, which is not possible with CPU's. As a reference, the Floating Point Operation Per Second (FLOPs) run in the Giga Hz in CPU's compared to Mega Hz in GPU's. For these reasons, when the database is _small_, the CPU implementation performs better in terms of speed than the GPU implementation.


## Question 3
For this question, I created two sets of files both for the serial and parallel versions:

- The **serial** code is contained in [q3_serial.py](https://github.com/magabrielaa/large-scale-computing/blob/main/03_GPU_computing/q3/serial/q3_serial.py) and through [q3_serial.sbatch](https://github.com/magabrielaa/large-scale-computing/blob/main/03_GPU_computing/q3/serial/q3_serial.sbatch) I had to request 25G for the code to run. The `.py` file times three runs for 50x, 100x, and 150x Landsat scenes. The results are in [q3_serial.out](https://github.com/magabrielaa/large-scale-computing/blob/main/03_GPU_computing/q3/serial/q3_serial.out)

- Likewise, the **parallel** code is in [q3_parallel.py](https://github.com/magabrielaa/large-scale-computing/blob/main/03_GPU_computing/q3/parallel/q3_parallel.py). In this case, I had to allocate 10G of memory in [q3_parallel.sbatch](https://github.com/magabrielaa/large-scale-computing/blob/main/03_GPU_computing/q3/parallel/q3_parallel.sbatch) for the code to run. The output is in [q3_parallel.out](https://github.com/magabrielaa/large-scale-computing/blob/main/03_GPU_computing/q3/parallel/q3_parallel.out)

For comparison purposes, I generated the following plot to capture the computation times for serial and parallel at 1x, 50x, 100x, and 150x database magnitude:

![Plot](https://github.com/magabrielaa/large-scale-computing/blob/main/03_GPU_computing/plot.png)

As can be seen from the graph and the output files, as the size of the database increases, the benefits of parallelism become more significant and apparent. At the original database size, the CPU serial code is faster than the GPU parallel code. However, at 50x the size of the original database, the GPU outperforms the CPU. As the order of magnitude of the database increases, the difference in speedup between the serial and parallel versions grows larger. This result is expected, for the reasons outlined in **Question 2** above.

Another reason why parallel code on a GPU performs better is due to **memory bandwidth**. Compared to CPU's, GPU's have a much higher memory bandwidth. This means that GPU's can process large amounts of data, which comes in handy when dealing with large databases in which the amount of data being processed can exceed memory on a CPU. An evidence of this is that my `q3_parallel.sbatch` runs with **10G** whereas my `q3_serial.sbatch` requires **25G** of RAM.

Moreover, in my code I avoid storing intermediate results on the GPU. This is because, even though storing on the GPU can sometimes result in more speedup, there is a limit to the GPU's memory bandwidth. If there is an excessive transfer of data between the CPU and the GPU, like there would likely be in this exercise due to the large size of the database, then the GPU can become idle while it waits for the data to be transferred. Therefore, in this case it is more efficient to store intermediate results on the CPU (ie. the fixed serial parameters) and transfer them to the GPU only when necessary (ie. when calling the parallelized numba function)