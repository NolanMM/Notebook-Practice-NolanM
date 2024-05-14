#include <iostream>
#include <cstdlib>
#include <cmath>
#include <ctime>
#include <mpi.h>

void discretize(float* data, int n) {
    for (int i = 0; i < n; i++)
        data[i] = (pow(sin(data[i]), cos(data[i])) +
            pow(cos(data[i]), sin(data[i]))) / 2.0f;
}

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);  // Initialize MPI
    int world_size, world_rank;

    MPI_Comm_size(MPI_COMM_WORLD, &world_size);  // Get the total number of processes
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);  // Get the rank of the current process

    if (argc != 2) {
        if (world_rank == 0) {
            std::cout << argv[0] << " : invalid number of arguments\n"
                << "Usage: " << argv[0] << " no_of_elements\n";
        }
        MPI_Finalize();
        return 1;
    }

    int n = atoi(argv[1]);
    int elements_per_process = n / world_size;

    // Allocate memory for the entire data array on the root process
    float* data = nullptr;
    if (world_rank == 0) {
        data = new float[n];
        for (int i = 0; i < n; i++)
            data[i] = static_cast<float>(rand()) / RAND_MAX;
    }

    // Allocate memory for the local data on each process
    float* local_data = new float[elements_per_process];

    // Scatter the data to all processes
    MPI_Scatter(data, elements_per_process, MPI_FLOAT, local_data, elements_per_process, MPI_FLOAT, 0, MPI_COMM_WORLD);

    // Discretize local data
    discretize(local_data, elements_per_process);

    // Count zeros in local data
    int local_zeros = 0;
    for (int i = 0; i < elements_per_process; i++)
        if (local_data[i] < 0.707f)
            local_zeros++;

    // Gather results from all processes
    int* all_zeros = new int[world_size];
    MPI_Gather(&local_zeros, 1, MPI_INT, all_zeros, 1, MPI_INT, 0, MPI_COMM_WORLD);

    // Sum up the total zeros on the root process
    int total_zeros = 0;
    if (world_rank == 0) {
        for (int i = 0; i < world_size; i++)
            total_zeros += all_zeros[i];
    }

    // Print results on the root process
    if (world_rank == 0) {
        std::cout << n << " = " << total_zeros << " 0s + " << n - total_zeros << " 1s\n";
        delete[] data;
    }

    // Clean up
    delete[] local_data;
    delete[] all_zeros;

    MPI_Finalize();  // Finalize MPI

    return 0;
}