//#include <iostream>
//#include <cmath>
//#include <omp.h>
//#include <chrono>
//#include <thread>
//using namespace std;
//
////Declare the global variables (Configuarable)
//const int Num_Elements = 6;
//const int Num_Threads = 2;
//
////Declare the functions
//void Sequential_Prefix_Sum(int Original_Array[], int Prefix_Array[], int Num_Elements);
//void Parallel_Prefix_Sum(int Original_Array[], int Prefix_Array[], int Num_Elements, int Num_Threads);
//void Evaluate_Performance(chrono::duration<double> parallel_time, chrono::duration<double> sequential_time);
//void Check_Array_Results(int Original_Array[], int Prefix_Array[], int Num_Elements);
//void Print_Results(int Original_Array[], int Parallel_Prefix_Array[], int Sequential_Prefix_Array[]);
//
//void Sequential_Prefix_Sum(int Original_Array[], int Prefix_Array[], int Num_Elements)
//{
//    int sum = 0;
//    int i = 0;
//
//    while (i < Num_Elements)
//    {
//        sum += Original_Array[i];
//        Prefix_Array[i] = sum;
//        Prefix_Array[i++];
//    }
//}
//
//void Parallel_Prefix_Sum(int Original_Array[], int Prefix_Array[], int Num_Elements, int Num_Threads) {
//    int* partial_sums = (int*)malloc(sizeof(int) * (Num_Elements + 1));
//    partial_sums[0] = 0;
//
//#pragma omp parallel num_threads(Num_Threads)
//    {
//        int ithread = omp_get_thread_num();
//        int nthreads = omp_get_num_threads();
//
//        int chunk_size = (Num_Elements + nthreads - 1) / nthreads;
//        int start = ithread * chunk_size;
//        int end = (ithread == (nthreads - 1)) ? Num_Elements : start + chunk_size;
//
//        int local_sum = 0;
//        for (int i = start; i < end; i++) {
//            local_sum += Original_Array[i];
//            Prefix_Array[i] = local_sum;
//        }
//
//        partial_sums[ithread + 1] = local_sum;
//
//#pragma omp barrier
//
//        int offset = 0;
//        for (int i = 0; i <= ithread; i++) {
//            offset += partial_sums[i];
//        }
//
//        for (int i = start; i < end; i++) {
//            Prefix_Array[i] += offset;
//        }
//    }
//
//    free(partial_sums);
//}
//
//void Evaluate_Performance(chrono::duration<double> parallel_time, chrono::duration<double> sequential_time) {
//    //Compare the throughtput between the sequential and parallel algorithms
//    double throughput_parallel = (double)Num_Elements / parallel_time.count();
//    double throughput_sequential = (double)Num_Elements / sequential_time.count();
//    double thoughput_ratio = throughput_parallel / throughput_sequential;
//    cout << endl << "__ Comparing the throughput between the sequential and parallel algorithms..." << endl;
//    cout << "Throughput of the sequential algorithm: " << throughput_sequential << " elements/second" << endl;
//    cout << "Throughput of the parallel algorithm: " << throughput_parallel << " elements/second" << endl;
//    cout << "Thoughput ratio: " << thoughput_ratio << endl;
//
//    //Compare the latency between the sequential and parallel algorithms
//    double latency_parallel = parallel_time.count() / Num_Elements;
//    double latency_sequential = sequential_time.count() / Num_Elements;
//    double latency_ratio = latency_parallel / latency_sequential;
//    cout << "\n__ Comparing the latency between the sequential and parallel algorithms..." << endl;
//    cout << "Latency of the sequential algorithm: " << latency_sequential << " seconds" << endl;
//    cout << "Latency of the parallel algorithm: " << latency_parallel << " seconds" << endl;
//    cout << "Latency ratio: " << latency_ratio << endl;
//
//    //Compare the speedup between the sequential and parallel algorithms
//    double speedup = sequential_time.count() / parallel_time.count();
//    cout << "\n__ Comparing the speedup between the sequential and parallel algorithms..." << endl;
//    cout << "Speedup: " << speedup << endl;
//
//    //Compare the efficiency between the sequential and parallel algorithms
//    double efficiency = speedup / Num_Threads;
//    cout << "\n__ Comparing the efficiency between the sequential and parallel algorithms..." << endl;
//    cout << "Efficiency: " << efficiency << endl;
//}
//
//void Check_Array_Results(int Original_Array[], int Prefix_Array[], int Num_Elements) {
//    int sum = 0;
//    for (int i = 0; i < Num_Elements; i++) {
//        sum += Original_Array[i];
//        if (sum != Prefix_Array[i]) {
//            cout << "Error: The prefix sum is not correct!" << endl;
//            break;
//        }
//    }
//    cout << endl << "The array result prefix sum is correct!" << endl;
//}
//
//void Print_Results(int Original_Array[], int Parallel_Prefix_Array[], int Sequential_Prefix_Array[])
//{
//    cout << endl << "Original Array: ";
//    //Auto initalize the original array with random numbers that in range 1 - 100 with the number of elements = Num_Elements
//    for (int i = 0; i < Num_Elements; i++) {
//        cout << Original_Array[i] << " ";
//    }
//    cout << endl;
//
//    //Print the results of the sequential algorithm
//    cout << "Parallel Prefix Sum: ";
//    for (int i = 0; i < Num_Elements; i++) {
//        printf("%d ", Parallel_Prefix_Array[i]);
//    }
//    printf("\n");
//
//    cout << "Sequential Prefix Sum: ";
//    for (int i = 0; i < Num_Elements; i++) {
//        printf("%d ", Sequential_Prefix_Array[i]);
//    }
//    printf("\n");
//}
//
//int main() {
//    //Initialize the variables by address to avoid stack overflow and store the values in the heap
//    int* Original_Array = new int[Num_Elements];
//    int* Parallel_Prefix_Array = new int[Num_Elements];
//    int* Sequential_Prefix_Array = new int[Num_Elements];
//
//    //Auto initalize the original array with random numbers that in range 1 - 100 with the number of elements = Num_Elements
//    for (int i = 0; i < Num_Elements; i++) {
//        Original_Array[i] = 1 + (rand() % 100);
//    }
//    cout << "__ Original Array Initialized" << endl;
//
//    //Sequential processing
//    cout << "\n__ Sequential processing..." << endl;
//    chrono::duration<double> sequential_time(0);
//    auto startTime = chrono::high_resolution_clock::now();
//    Sequential_Prefix_Sum(Original_Array, Sequential_Prefix_Array, Num_Elements);
//    sequential_time = chrono::high_resolution_clock::now() - startTime;
//    cout << "\n__ Sequential processing Done" << endl;
//
//    //Parallel processing
//    cout << "\n__ Parallel processing..." << endl;
//    chrono::duration<double> parallel_time(0);
//    startTime = chrono::high_resolution_clock::now();
//    Parallel_Prefix_Sum(Original_Array, Parallel_Prefix_Array, Num_Elements, Num_Threads);
//    parallel_time = chrono::high_resolution_clock::now() - startTime;
//    cout << "\n__ Parallel processing Done" << endl;
//
//    //Check the results of the parallel algorithm and evaluate the performance and print the results
//    thread T1(Check_Array_Results, Original_Array, Parallel_Prefix_Array, Num_Elements);
//    thread T2(Check_Array_Results, Original_Array, Sequential_Prefix_Array, Num_Elements);
//    T1.join();
//    T2.join();
//    thread T3(Evaluate_Performance, parallel_time, sequential_time);
//    T3.join();
//
//    Print_Results(Original_Array, Parallel_Prefix_Array, Sequential_Prefix_Array);
//    return 1;
//}