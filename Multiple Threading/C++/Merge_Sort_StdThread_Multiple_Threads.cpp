/*
    Student name: Minh Nguyen
    Student ID: 8723388
    Lab 3: Parallel Computing
    Date: 01/10/2023
*/

#include <iostream>
#include <thread>
#include <vector>
#include <algorithm>
#include <chrono>
#include <iomanip>
using namespace std;

// Change the number of threads, number of times run, and size of array here
unsigned int NUMBER_PAIRS_OF_THREADS = 1; // 2 * NUMBER_PAIRS_OF_THREADS threads will be created
unsigned int NUMBER_TIMES_RUN = 1;
unsigned int SIZE_OF_ARRAY = 1000000;
vector<std::thread::id> list_thread_working;

void Sequential_Merge_Sort(int* array, unsigned int left, unsigned int right);
void Parallel_Merge_Sort(int* array, unsigned int left, unsigned int right, int number_of_pair_thread);
void Merge(int* array, unsigned int left, unsigned int mid, unsigned int right);
void Check_merged(int* array, int size, bool* is_sorted);
bool Compare(int* array1, int* array2, int size);

void Sequential_Merge_Sort(int* array, unsigned int left, unsigned int right) {
    if (left < right) {
        unsigned int mid = (left + right) / 2;
        Sequential_Merge_Sort(array, left, mid);
        Sequential_Merge_Sort(array, mid + 1, right);
        Merge(array, left, mid, right);
    }
}

void Merge(int* array, unsigned int left, unsigned int mid, unsigned int right) {
    unsigned int num_left = mid - left + 1; // number of elements in left subarray
    unsigned int num_right = right - mid; // number of elements in right subarray

    // copy data into temporary left and right subarrays to be merged
    int* array_left = new int[num_left];
    int* array_right = new int[num_right];
    copy(&array[left], &array[mid + 1], array_left);
    copy(&array[mid + 1], &array[right + 1], array_right);

    // initialize indices for array_left, array_right, and input subarrays
    unsigned int index_left = 0;    // index to get elements from array_left
    unsigned int index_right = 0;    // index to get elements from array_right
    unsigned int index_insert = left; // index to insert elements into input array

    // merge temporary subarrays into original input array
    while ((index_left < num_left) || (index_right < num_right)) {
        if ((index_left < num_left) && (index_right < num_right)) {
            if (array_left[index_left] <= array_right[index_right]) {
                array[index_insert] = array_left[index_left];
                index_left++;
            }
            else {
                array[index_insert] = array_right[index_right];
                index_right++;
            }
        }
        // copy any remain elements of array_left into array
        else if (index_left < num_left) {
            array[index_insert] = array_left[index_left];
            index_left += 1;
        }
        // copy any remain elements of array_right into array
        else if (index_right < num_right) {
            array[index_insert] = array_right[index_right];
            index_right += 1;
        }
        index_insert++;
    }
}

void Parallel_Merge_Sort(int* array, unsigned int left, unsigned int right, int number_of_pair_thread) {
    if (left < right) {
        // Check if the number of pair thread is greater than 0
        if (number_of_pair_thread > 0) {
            unsigned int mid = (left + right) / 2;

            // Create 2 threads to sort the left and right subarrays
            thread t1(Parallel_Merge_Sort, array, left, mid, number_of_pair_thread - 1);
            thread t2(Parallel_Merge_Sort, array, mid + 1, right, number_of_pair_thread - 1);

            // store the thread id to the vector space
            list_thread_working.push_back(t1.get_id());
            list_thread_working.push_back(t2.get_id());

            // Wait for both threads to complete
            t1.join();
            t2.join();
        }
        // If the number of pair thread is 0, use sequential_merge_sort() function to sort the array for each thread process
        else {
            Sequential_Merge_Sort(array, left, right);
        }
        // After all thread be done, re merged all threads result
        Merge(array, left, (left + right) / 2, right);
    }
}

void Check_merged(int* array, int size, bool* is_sorted) {
    for (int i = 0; i < size - 1; i++) {
        if (array[i] > array[i + 1]) {
            *is_sorted = false;
            break;
        }
    }
}

bool Compare(int* array1, int* array2, int size) {
    bool is_same = true;
    for (int i = 0; i < size - 1; i++) {
        if (array1[i] != array2[i]) {
            is_same = false;
            break;
        }
    }
    return is_same;
}

int main() {
    // Generate random array
    int* original_array = new int[SIZE_OF_ARRAY];
    int* result = new int[SIZE_OF_ARRAY + 1];
    int* result_par = new int[SIZE_OF_ARRAY + 1];

    for (int i = 0; i < SIZE_OF_ARRAY; i++) {
        original_array[i] = rand();
        //cout << "[" << original_array[i] << "] ";
    }
    cout << "\n-- Original array generated done" << endl;

    // Sequential processing
    cout << "\n-- Sequential processing..." << endl;
    chrono::duration<double> sequential_time(0);
    auto startTime = chrono::high_resolution_clock::now();
    for (int i = 0; i < NUMBER_TIMES_RUN; i++) {
        copy(&original_array[0], &original_array[SIZE_OF_ARRAY], result);
        Sequential_Merge_Sort(result, 0, SIZE_OF_ARRAY - 1);
    }
    sequential_time = chrono::high_resolution_clock::now() - startTime;
    cout << "\n-- Sequential processing Done" << endl;

    // Parallel processing
    cout << "\n-- Parallel processing..." << endl;
    chrono::duration<double> parallel_time(0);
    startTime = chrono::high_resolution_clock::now();
    for (int i = 0; i < NUMBER_TIMES_RUN; i++) {
        copy(&original_array[0], &original_array[SIZE_OF_ARRAY], result_par);
        Parallel_Merge_Sort(result_par, 0, SIZE_OF_ARRAY - 1, int(NUMBER_PAIRS_OF_THREADS));
    }
    parallel_time = chrono::high_resolution_clock::now() - startTime;
    cout << "\n-- Parallel processing Done" << endl;

    // Parallel check if the arrays be sorted correctly (Parallel and Sequential)
    delete[] original_array;
    bool* is_sorted = new bool(true);
    thread T1(Check_merged, result, SIZE_OF_ARRAY, is_sorted);

    bool* is_sorted_par = new bool(true);
    thread T2(Check_merged, result_par, SIZE_OF_ARRAY, is_sorted_par);

    T1.join();
    T2.join();

    cout << "\n-- Sequential sort: " << (*is_sorted ? "Pass, The array be sorted correctly" : "Fail. Something wrong happens") << endl;
    cout << "\n-- Parallel sort: " << (*is_sorted_par ? "Pass, The array be sorted correctly" : "Fail. Something wrong happens") << endl;

    // Wait for both threads to complete
    // Compare 2 arrays to check if they are the same
    bool is_same = Compare(result, result_par, SIZE_OF_ARRAY);
    cout << "\n-- Compare 2 arrays: " << (is_same ? "Results are the same" : "Results are NOT the same") << endl;
    delete[] result;
    delete[] result_par;

    // Display the time it took to run the sorting algorithm
    cout << setfill('=') << setw(39) << "" << endl;
    cout << "\t\tRESULTS" << endl << endl;
    cout << "-- Input: N = " << SIZE_OF_ARRAY << endl;
    cout << "-- Average time over " << NUMBER_TIMES_RUN << " runs: " << endl;
    cout << "-- Sequential merge sort: " << sequential_time.count() / NUMBER_TIMES_RUN << " s" << endl;
    cout << "-- Parallel merge sort: " << parallel_time.count() / NUMBER_TIMES_RUN << " s" << endl << endl;

    // Calculate the efficiency of the parallel processing 
    // by average time of sequential processing and parallel processing by TOTAL_TIME_PER_PROCESS/NUMBER_TIMES_RUN
    cout << setfill('=') << setw(39) << "" << endl;
    double ef = ((sequential_time.count() / NUMBER_TIMES_RUN) / (parallel_time.count() / NUMBER_TIMES_RUN)) / (NUMBER_PAIRS_OF_THREADS * 2);
    cout << "\n<---  EFFICENCY WHOLE PROCESS: " << ((sequential_time.count() / NUMBER_TIMES_RUN) / (parallel_time.count() / NUMBER_TIMES_RUN)) * 100 << "%" << "  --->" << endl << endl;
    cout << "<---  EFFICENCY EACH THREAD: " << ef * 100 << "%" << "  --->" << endl << endl;
    cout << "<*NOTE: Efficiency(%) = ((Sequential_Time / Parallel_Time) / Number of Threads) * 100" << endl;

    // Calculate the thread id use by the number of times parallel_merge_sort() function called by NUMBER_TIMES_RUN and the number of threads
    cout << "\nNumber of threads id working by configurations (In Theory): " << (NUMBER_PAIRS_OF_THREADS * 2) * NUMBER_TIMES_RUN << endl;
    cout << "\nNumber of threads id working be stored in the vector space (Actual counts): " << list_thread_working.size() << endl;

    // Print out the vector space for the thread list
    cout << "\nThread Id list: ";
    for (auto i = list_thread_working.cbegin(); i != list_thread_working.cend(); ++i)
        cout << *i << " " << ", ";
    cout << endl;

    return 1;
}

