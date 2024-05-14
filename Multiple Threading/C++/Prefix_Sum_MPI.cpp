/*

// Student Name: Minh Nguyen
// Lab 5 Prefix sum by MPI

*/


#include <iostream>
#include <vector>
#include <mpi.h>

const int MASTER = 0;
const int FROM_MASTER = 1;
const int FROM_WORKER = 2;

int main(int argc, char* argv[]) {
    MPI_Init(&argc, &argv);

    int numtasks, taskid;

    MPI_Comm_size(MPI_COMM_WORLD, &numtasks);
    MPI_Comm_rank(MPI_COMM_WORLD, &taskid);

    if (numtasks < 2) {
        std::cerr << "This program requires at least 2 processes." << std::endl;
        MPI_Abort(MPI_COMM_WORLD, 1);
    }

    const int num_elements = 10;
    std::vector<int> Original_Array(num_elements);
    std::vector<int> Prefix_Array(num_elements);
    int sum = 0;

    if (taskid == MASTER) {
        std::cout << "MPI Master starting to work" << std::endl;
        std::cout << "Number of workers = " << numtasks - 1 << std::endl;

        // Initialize the original array
        for (int i = 0; i < num_elements; i++) {
            Original_Array[i] = i;
        }

        // Broadcast the original array to all processes
        MPI_Bcast(&Original_Array[0], num_elements, MPI_INT, MASTER, MPI_COMM_WORLD);
    }

    int numworkers = numtasks - 1;
    int elements_per_worker = num_elements / numworkers;
    int start = 0, end = 0;

    if (taskid > MASTER) {
        // Worker task
        start = (taskid - 1) * elements_per_worker;
        end = (taskid == numworkers) ? num_elements : start + elements_per_worker;

        // Each worker calculates its partial sum
        for (int i = start; i < end; i++) {
            sum += Original_Array[i];
        }

        // Send the partial sum back to the master
        MPI_Send(&sum, 1, MPI_INT, MASTER, FROM_WORKER, MPI_COMM_WORLD);
    }

    if (taskid == MASTER) {
        // Master collects partial sums from workers and computes the prefix sum
        for (int i = 1; i <= numworkers; i++) {
            MPI_Recv(&sum, 1, MPI_INT, i, FROM_WORKER, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            Prefix_Array[i * elements_per_worker] = sum;
        }

        // Calculate the prefix sum using the master process
        Prefix_Array[0] = Original_Array[0];
        for (int i = 1; i < num_elements; i++) {
            Prefix_Array[i] = Prefix_Array[i - 1] + Original_Array[i];
        }

        std::cout << "\nPrefix Sum Array\n";
        for (int count = 0; count < num_elements; count++)
            std::cout << Prefix_Array[count] << " ";
        std::cout << std::endl;
    }

    MPI_Finalize();
    return 0;
}
