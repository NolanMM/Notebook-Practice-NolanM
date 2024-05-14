/*
    Student name: Minh Nguyen
    Student ID: 8723388
    Lab 4: Prefix Sum Parallel Computing
    Date: 08/10/2023
*/

//  Overview Function

/*

Try: 
    Parallel run on 500,000,000 with 50 threads = 0.40 seconds
    ==> Thoughput ratio: 0.434032 (Throughput Sequential / Throughput Parallel)
    ==> Latency ratio: 2.30398 (Latency Sequential / Latency Parallel)
    ==> Speedup: 2.30398 (Sequential Time / Parallel Time)
    ==> Efficiency: 4.60796 % (Speedup / Number of Threads)

Functions:
    - Sequential_Prefix_Sum: Calculate the Prefix Sum in traditional way
    - Parallel_Prefix_Sum: Calculate the Prefix Sum using OMP library
    - Evaluate_Performance: Evaluate Performance between Sequetial Prefix Sum process and Parallel Prefix Sum process with throughput, latency, Speed
    - Check_Array_Results: Check the result Array return by Parallel process
    - Print_Results : Print out table if needed

Explain for the Parallel Process

1. Create array to store the sum of each chunk (sum_each_chunks_list pointer)

2. Start the parallel process with number of threads input by calling the pragma omp parallel

3. Retrieve the thread number, number of threads and the size of each chunk

4. Use omp single to just allow 1 thread to intialize memory allocation in the heap for sum_each_chunks_list to avoid deadlock 

5. Intialize the sum_each_chunks_list in the heap by dynamic memory allocation corresponding to the number of threads input and 
   store the total (sum) of all elements inside that list to avoid stack overflow
   (Because the schedule(static) nowait will separate equal number of elements among the threads and execute independently to calculate the
    sum of all elements inside that list)
    For example:

        Input List [0,3,5,1,3,5,3,4,5,6] size = 10 and numthread = 2 

        => Each threads will contains 5 elements input to calculate the sum of all elements inside the list independently. 
                The first sum_each_chunks_list[0] = 0 to add up later to avoid the difference measured value
        Then => 

        {
            sum_each_chunks_list[0] (value int inside pointer) = 0
            sum_each_chunks_list[1] List Elements Input = [0,3,5,1,3] (value int inside pointer) = 0 + 3 + 5 + 1 + 3 = 12
            sum_each_chunks_list[2] List Elements Input = [5,3,4,5,6] (value int inside pointer) = 5 + 3 + 4 + 5 + 6 = 23

            And sum = 0. 2 Threads run independently

                -> For Thread 0: Input List [0,3,5,1,3]
                    i = 0 , Prefix_Array[0] = sum + Input List[0] = 0 + 0 = 0, re value sum = 0 , store sum to sum_each_chunks_list[1] = 0 and continue next iterator
                    i = 1 , Prefix_Array[1] = sum + Input List[1] = 0 + 3 = 3, re value sum = 3 , store sum to sum_each_chunks_list[1] = 3 and continue next iterator
                    i = 2 , Prefix_Array[2] = sum + Input List[2] = 3 + 5 = 8, re value sum = 8 , store sum to sum_each_chunks_list[1] = 8 and continue next iterator
                    i = 3 , Prefix_Array[3] = sum + Input List[3] = 8 + 1 = 9, re value sum = 9 , store sum to sum_each_chunks_list[1] = 9 and continue next iterator
                    i = 4 , Prefix_Array[4] = sum + Input List[4] = 9 + 3 = 12, re value sum = 12 , store sum to sum_each_chunks_list[1] = 12 
                    
                    Ouput List 1 = Prefix_Array[:4] = [0, 3, 8, 9, 12]
                                    sum_each_chunks_list[1] = 12 

                    and break with barrier to wait other threads done then continue to calculate the offset internal because the nowait declare above

                -> For Thread 1: Input List [5,3,4,5,6]
                    i = 0 , Prefix_Array[5] = sum + Input List[5] = 0 + 5 = 5, re value sum = 5 , store sum to sum_each_chunks_list[2] = 5 and continue next iterator
                    i = 1 , Prefix_Array[6] = sum + Input List[6] = 5 + 3 = 8, re value sum = 8 , store sum to sum_each_chunks_list[2] = 8 and continue next iterator
                    i = 2 , Prefix_Array[7] = sum + Input List[7] = 8 + 4 = 12, re value sum = 12 , store sum to sum_each_chunks_list[2] = 12 and continue next iterator
                    i = 3 , Prefix_Array[8] = sum + Input List[8] = 12 + 5 = 17, re value sum = 17 , store sum to sum_each_chunks_list[2] = 17 and continue next iterator
                    i = 4 , Prefix_Array[9] = sum + Input List[9] = 17 + 6 = 23, re value sum = 23 , store sum to sum_each_chunks_list[2] = 23 
                    
                    Ouput List 2 = Prefix_Array[5:9] = [5, 8, 12, 17, 23]
                                    sum_each_chunks_list[2] = 23

                    and break with barrier to wait other threads done then continue to calculate the offset internal because the nowait declare above
        }

        - We have the prefix_array right now but it just inside each chunk and we have stored the total value of all elements inside each chunk into
          the sum_each_chunks_list pointer array in heap to set to the offset later
        - So we need to re calculate the Prefix_Array[ 5 : 9 ] again with the offset value = sum_each_chunks_list[1] by looping through all the element
          inside sum_each_chunks_list corresponding to the threadID assigned before
        - Then we re-caculate all the element inside the Original input list with the offset

            First For loop to calculate the offset with for loop range ithread + 1 so we can loop through all the number of elements 
            inside the sum_each_chunks_list corresponding to the thread number and always avoid to forget to loop through any elements or the counter exceed the
            number of chunks = the number of thread + 1
        
        **********

        - Note: the index of sum_each_chunks_list element will always be 1 index smaller because we want to re calculate the Prefix[range] inside that chunk with
          the sum in the previous chunk only -> that also why we need the barrier to make sure that all the calculation for the value of the sum of each chunk finished
          before calculate the offset
        
        **********
        {
            And define offset = 0.  2 Threads run independently

                ->> Continue run Independently Thread 0: Input sum_each_chunks_list[i] = Input sum_each_chunks_list[0] = 0
                    i = 0 < threadid + 1 = 1 because there is always 1 thread working(main thread id 0) , offset = offset + sum_each_chunks_list[0] = 0 + 0 = 0, 
                            store the offset = 0 and continue to re-caculate the Prefix_Array[:4] again with offset

                        Input List = Ouput List 1 = Prefix_Array[:4] = [0, 3, 8, 9, 12] and offset = 0
                            i = 0 , re-store the Prefix_Array[0] = offset + Input List[0] = 0 + 0 = 0, and continue next iterator
                            i = 1 , re-store the Prefix_Array[1] = offset + Input List[1] = 0 + 3 = 3, and continue next iterator
                            i = 2 , re-store the Prefix_Array[2] = offset + Input List[2] = 0 + 8 = 8, and continue next iterator
                            i = 3 , re-store the Prefix_Array[3] = offset + Input List[3] = 0 + 9 = 9, and continue next iterator
                            i = 4 , re-store the Prefix_Array[4] = offset + Input List[4] = 0 + 12 = 12, and stop
                    
                    Ouput List 1 = Prefix_Array[:4] = [0, 3, 8, 9, 12] and free the sum_each_chunks_list[0]

                ->> Continue run Independently Thread 1: Input sum_each_chunks_list[i] = Input sum_each_chunks_list[1] = 12
                    i = 1 < threadid + 1 = 2 because there is always 1 thread working(main thread id 0) ,  offset = offset + sum_each_chunks_list[1] = 0 + 12 = 12 , 
                           store the offset = 12 and continue to re-caculate the Prefix_Array[5:9] again with offset

                        Input List = Ouput List 2 = Prefix_Array[5:9] = [5, 8, 12, 17, 23]
                            i = 5 , re-store the Prefix_Array[5] = offset + Input List[5] = 12 + 5 = 17, and continue next iterator
                            i = 6 , re-store the Prefix_Array[6] = offset + Input List[6] = 12 + 8 = 20, and continue next iterator
                            i = 7 , re-store the Prefix_Array[7] = offset + Input List[7] = 12 + 12 = 24, and continue next iterator
                            i = 8 , re-store the Prefix_Array[8] = offset + Input List[8] = 12 + 17 = 29, and continue next iterator
                            i = 9 , re-store the Prefix_Array[9] = offset + Input List[9] = 12 + 23 = 35, and stop
                    
                    Ouput List 2 = Prefix_Array[5:9] = [17, 20, 24, 29, 35] and free the sum_each_chunks_list[1]
        }

6. The Output Prefix_Array[0:9] final after the parallel process with

=====> Input List [0, 3, 5, 1, 3, 5, 3, 4, 5, 6] size = 10 numthread = 2

=====> Prefix_Array[0:9] = [0, 3, 8, 9, 12, 17, 20, 24, 29, 35]

*/

#include <iostream>
#include <cmath>
#include <omp.h>
#include <chrono>
using namespace std;

//Declare the global variables (Configuarable all values)
const int Num_Elements = 10;
const int Num_Threads = 2;

//Declare the functions
void Sequential_Prefix_Sum(int Original_Array[], int Prefix_Array[], int Num_Elements);
void Parallel_Prefix_Sum(int Original_Array[], int Prefix_Array[], int Num_Elements, int Num_Threads);
void Evaluate_Performance(chrono::duration<double> parallel_time, chrono::duration<double> sequential_time);
void Check_Array_Results(int Original_Array[], int Prefix_Array[], int Num_Elements);
void Print_Results(int Original_Array[], int Parallel_Prefix_Array[], int Sequential_Prefix_Array[]);

void Sequential_Prefix_Sum(int Original_Array[], int Prefix_Array[], int Num_Elements)
{
    int sum = 0;
    int i = 0;

    while (i < Num_Elements)
    {
        sum += Original_Array[i];
        Prefix_Array[i] = sum;
        Prefix_Array[i++];
    }
}

void Parallel_Prefix_Sum(int Original_Array[], int Prefix_Array[], int Num_Elements, int Num_Threads) {
    int* sum_each_chunks_list;
    int size = Num_Elements;
    // Start Parallel Processing
#pragma omp parallel num_threads(Num_Threads)
    {   
        int ithread = omp_get_thread_num();
        int num_threads = omp_get_num_threads();
    // Just main thread allocated the memory for sum_each_chunks_list array
#pragma omp single
        sum_each_chunks_list = (int*)malloc(sizeof(int) * (num_threads + 1));
        sum_each_chunks_list[0] = 0;

        int sum = 0;
#pragma omp for schedule(static) nowait
        for (int i = 0; i < size; i++) {
            sum += Original_Array[i];
            Prefix_Array[i] = sum; 
        }
        sum_each_chunks_list[ithread + 1] = sum;

    // Wait for all the threads to finish calculate the sum_each_chunks_list
#pragma omp barrier
        // Calculate the offset for each chunk
        int offset = 0;
        for (int i = 0; i < ithread + 1; i++) {
            offset += sum_each_chunks_list[i];
        }
#pragma omp for schedule(static)
        for (int i = 0; i < size; i++) {
            Prefix_Array[i] += offset;
        }
    }
    free(sum_each_chunks_list);
}

void Evaluate_Performance(chrono::duration<double> parallel_time, chrono::duration<double> sequential_time) {
    // Print out the time of the parallel and sequential algorithms
    cout << "\n==> Comparing the time between the sequential and parallel algorithms..." << endl;
    cout << "__ Time of the sequential algorithm: " << sequential_time.count() << " seconds" << endl;
    cout << "__ Time of the parallel algorithm: " << parallel_time.count() << " seconds" << endl;

    //Compare the throughtput between the sequential and parallel algorithms
    double throughput_parallel = (double)Num_Elements / parallel_time.count();
    double throughput_sequential = (double)Num_Elements / sequential_time.count();
    cout << endl << "==> Comparing the throughput between the sequential and parallel algorithms..." << endl;
    cout << "__ Throughput of the sequential algorithm: " << throughput_sequential << " elements/second" << endl;
    cout << "__ Throughput of the parallel algorithm: " << throughput_parallel << " elements/second" << endl;
    cout << "==> Thoughput ratio: " << throughput_sequential / throughput_parallel << " (Throughput Sequential / Throughput Parallel)" << endl;

    //Compare the latency between the sequential and parallel algorithms
    double latency_parallel = parallel_time.count() / Num_Elements;
    double latency_sequential = sequential_time.count() / Num_Elements;
    cout << "\n==> Comparing the latency between the sequential and parallel algorithms..." << endl;
    cout << "__ Latency of the sequential algorithm: " << latency_sequential << " seconds" << endl;
    cout << "__ Latency of the parallel algorithm: " << latency_parallel << " seconds" << endl;
    cout << "==> Latency ratio: " << latency_sequential / latency_parallel << " (Latency Sequential / Latency Parallel)" << endl;

    //Compare the speedup between the sequential and parallel algorithms
    double speedup = sequential_time.count() / parallel_time.count();
    cout << "\n==> Comparing the speedup between the sequential and parallel algorithms..." << endl;
    cout << "==> Speedup: " << speedup << " (Sequential Time / Parallel Time)" << endl;

    // Calculate the efficiency from speedup
    double efficiency = speedup / Num_Threads;
    cout << "\n==> Comparing the efficiency between the sequential and parallel algorithms..." << endl;
    cout << "==> Efficiency: " << efficiency * 100 << " % (Speedup / Number of Threads)" << endl;
}

void Check_Array_Results(int Original_Array[], int Prefix_Array[], int Num_Elements) {
    int sum = 0;
    for (int i = 0; i < Num_Elements; i++) {
        sum += Original_Array[i];
        if (sum != Prefix_Array[i]) {
            cout << "Error: The prefix sum is not correct!" << endl;
            break;
        }
    }
    cout << endl << "The array result prefix sum is correct!" << endl;
}

void Print_Results(int Original_Array[], int Parallel_Prefix_Array[], int Sequential_Prefix_Array[])
{
    cout << endl << "Original Array: ";
    for (int i = 0; i < Num_Elements; i++) {
        cout << Original_Array[i] << " ";
    }

    //Print the results of the Parallel algorithm
    cout << endl << "Parallel Prefix Sum: ";
    for (int i = 0; i < Num_Elements; i++) {
        cout << Parallel_Prefix_Array[i] << " ";
    }

    //Print the results of the Sequential algorithm
    cout << endl << "Sequential Prefix Sum: ";
    for (int i = 0; i < Num_Elements; i++) {
        cout << Sequential_Prefix_Array[i] << " ";
    } cout << endl;
}

int main() {
     // Use to test and expected output in theory [0, 3, 8, 9, 12, 17, 20, 24, 29, 35]
    int* Original_Array = new int[Num_Elements] {0, 3, 5, 1, 3, 5, 3, 4, 5, 6};
    //int* Original_Array = new int[Num_Elements];
    int* Parallel_Prefix_Array = new int[Num_Elements];
    int* Sequential_Prefix_Array = new int[Num_Elements];

    cout << endl << "==> The Prefix Sum Parallel Computing Program is Starting..." << endl;
    cout << endl << "__ Input: N = " << Num_Elements << endl;
    cout << endl << "__ Number of threads: " << Num_Threads << endl;

    //Auto initalize the original array with random numbers that in range 1 - 100 with the number of elements = Num_Elements
    //for (int i = 0; i < Num_Elements; i++) {
    //    Original_Array[i] = 1 + (rand() % 100);
    //}
    cout << endl << "==> Original Array Initialized" << endl;

    //Sequential processing
    cout << "\n==> Sequential processing..." << endl;
    chrono::duration<double> sequential_time(0);
    auto startTime = chrono::high_resolution_clock::now();
    Sequential_Prefix_Sum(Original_Array, Sequential_Prefix_Array, Num_Elements);
    sequential_time = chrono::high_resolution_clock::now() - startTime;
    cout << "\n==> Sequential processing Done" << endl;

    //Parallel processing
    cout << "\n==> Parallel processing..." << endl;
    chrono::duration<double> parallel_time(0);
    startTime = chrono::high_resolution_clock::now();
    Parallel_Prefix_Sum(Original_Array, Parallel_Prefix_Array, Num_Elements, Num_Threads);
    parallel_time = chrono::high_resolution_clock::now() - startTime;
    cout << "\n==> Parallel processing Done" << endl;

    //Check the results of the parallel algorithm and evaluate the performance and print the results
    Check_Array_Results(Original_Array, Parallel_Prefix_Array, Num_Elements);
    Check_Array_Results(Original_Array, Sequential_Prefix_Array, Num_Elements);
    Evaluate_Performance(parallel_time, sequential_time);
    //Check the results of the parallel algorithm and evaluate the performance and print the results
    //thread T1(Check_Array_Results,Original_Array, Parallel_Prefix_Array, Num_Elements);
    //thread T2(Check_Array_Results,Original_Array, Sequential_Prefix_Array, Num_Elements);
    //T1.join();
    //T2.join();
    //thread T3(Evaluate_Performance,parallel_time, sequential_time);
    //T3.join();

    // Print result if needed
    //Print_Results(Original_Array, Parallel_Prefix_Array, Sequential_Prefix_Array);
    cout << endl << "==> The Prefix Sum Parallel Computing Program Done..." << endl << "==> Exiting..." << endl;
    return 1;
}