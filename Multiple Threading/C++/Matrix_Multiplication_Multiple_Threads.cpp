#include <iostream>
#include <cmath>
#include <chrono>
#include <list>
#include <thread>
#include <vector>
#include <mutex>
using namespace std;

const unsigned int NUM_ROWS_A = 1000;
const unsigned int NUM_COLS_A = 1000;
const unsigned int NUM_ROWS_B = NUM_COLS_A;
const unsigned int NUM_COLS_B = 1000;
const unsigned int NUM_THREADS = 4;

void InitArray(int**& Matrix, unsigned int Rows, unsigned int Cols) {
    Matrix = new int* [Rows];
    if (Matrix == NULL) {
        exit(2);
    }
    for (unsigned int i = 0; i < Rows; i++) {
        Matrix[i] = new int[Cols];
        if (Matrix[i] == NULL) {
            exit(2);
        }
        for (unsigned int j = 0; j < Cols; j++) {
            Matrix[i][j] = rand() % 100 + 1;
        }
    }
}

void DisplayArray(int**& Matrix, unsigned int Rows, unsigned int Cols) {
    for (unsigned int i = 0; i < Rows; i++) {
        for (unsigned int j = 0; j < Cols; j++) {
            cout << " [" << Matrix[i][j] << "] ";
        }
        cout << endl;
    }
}

//Sequential Matrix Multiplication
void sequential_matrix_multiply(int**& Matrix_A, unsigned int num_rows_a, unsigned int num_cols_a,
    int**& Matrix_B, unsigned int num_rows_b, unsigned int num_cols_b,
    int**& Result) {
    for (unsigned int i = 0; i < num_rows_a; i++) {
        for (unsigned int j = 0; j < num_cols_b; j++) {
            Result[i][j] = 0;
            for (unsigned int k = 0; k < num_cols_a; k++) {
                Result[i][j] += Matrix_A[i][k] * Matrix_B[k][j];
            }
        }
    }
}

void parallel_helper(int**& Matrix_A,
    int**& Matrix_B, int**& Result, int start_row, int end_row, int row_per_thread) {
    for (int i = 0; i < row_per_thread; i++) { // i range 0 - > 250
        for (unsigned int j = 0; j < 1000; j++) { // J range 0 -> 1000
            Result[i][j] = 0;
            for (unsigned int k = 0; k < 1000; k++) { // K range 0 -> 1000
                Result[i][j] += Matrix_A[i][k] * Matrix_B[k][j];
            }
        }
    }
}

int parallel_matrix_multiply(int**& Matrix_A, unsigned int num_rows_a, unsigned int num_cols_a,
    int**& Matrix_B, unsigned int num_rows_b, unsigned int num_cols_b,
    int**& Results) {
    unsigned int time = 0;

    // Check number of thread available in the hardwares
    int number_threads_available = thread::hardware_concurrency();
    int num_threads = std::min(number_threads_available != 0 ? number_threads_available : 4, int(NUM_THREADS));
    int rows_per_thread = 0; // First declare for the rows_per_thread to calculate the number of blocks

    // Check if the number of block is even or odd to not miss any row
    if (NUM_ROWS_A % num_threads == 0) {
        rows_per_thread = 1000 / num_threads;
    }
    else {
        rows_per_thread = 1000 / num_threads + 1;
    }

    vector<thread> threads(num_threads);

    int** chunks_A[NUM_THREADS];
    int** chunks_B[NUM_THREADS];
    int** chunks_Result[NUM_THREADS];

    int start_row[NUM_THREADS];
    int end_row[NUM_THREADS];

    // Loop through the number of the blocks
    for (int i = 0; i < num_threads; i++) {
        // set the start and end of the block
        start_row[i] = i * rows_per_thread;
        end_row[i] = start_row[i] + rows_per_thread;

        // Initialize the chunks
        chunks_A[i] = nullptr;
        chunks_B[i] = nullptr;
        chunks_Result[i] = nullptr;
        InitArray(chunks_A[i], rows_per_thread, NUM_COLS_A);
        InitArray(chunks_B[i], NUM_COLS_B, NUM_COLS_B);
        InitArray(chunks_Result[i], rows_per_thread, NUM_COLS_A);

        // Copy the data from the original matrix to the chunks
        for (int j = start_row[i]; j < end_row[i]; j++) {
            for (int k = 0; k < NUM_COLS_A; k++) {
                chunks_A[i][j - start_row[i]][k] = Matrix_A[j][k];
            }
        }
        // Copy the data from the original matrix to the chunks B
        for (int j = 0; j < NUM_ROWS_B; j++) {
            for (int k = 0; k < NUM_COLS_B; k++) {
                chunks_B[i][j][k] = Matrix_B[j][k];
            }
        }
    }

    chrono::duration<double> Seq_Time(0);
    auto startTime = chrono::high_resolution_clock::now();

    threads[0] = thread(parallel_helper, ref(chunks_A[0]),ref(chunks_B[0]), ref(chunks_Result[0]), start_row[0], end_row[0], rows_per_thread);
    threads[1] = thread(parallel_helper, ref(chunks_A[1]), ref(chunks_B[1]), ref(chunks_Result[1]), start_row[1], end_row[1], rows_per_thread);
    threads[2] = thread(parallel_helper, ref(chunks_A[2]), ref(chunks_B[2]), ref(chunks_Result[2]), start_row[2], end_row[2], rows_per_thread);
    threads[3] = thread(parallel_helper, ref(chunks_A[3]), ref(chunks_B[3]), ref(chunks_Result[3]), start_row[3], end_row[3], rows_per_thread);

    threads[0].join();
    threads[1].join();
    threads[2].join();
    threads[3].join();

    Seq_Time = chrono::high_resolution_clock::now() - startTime;
    time = Seq_Time.count() * 1000;

    int** Result = nullptr;
    Result = new int* [NUM_ROWS_A];
    for (unsigned int i = 0; i < NUM_ROWS_A; i++) {
        Result[i] = new int[NUM_COLS_B];
    }

    // Combine chunks result to the final result
    for (int i = 0; i < num_threads; i++) {
        for (int j = start_row[i]; j < end_row[i]; j++) {
            for (int k = 0; k < NUM_COLS_B; k++) {
                Result[j][k] = chunks_Result[i][j - start_row[i]][k];
			}
		}
	}
    //DisplayArray(Result, NUM_ROWS_A, NUM_COLS_B);
    return time;
}


int main()
{
    int** MatrixA = nullptr;
    int** MatrixB = nullptr;
    int** Result = nullptr;

    //Allocate data for the resulting arrays
    Result = new int* [NUM_ROWS_A];
    for (unsigned int i = 0; i < NUM_ROWS_A; i++) {
        Result[i] = new int[NUM_COLS_B];
    }

    InitArray(MatrixA, NUM_ROWS_A, NUM_COLS_A);
    InitArray(MatrixB, NUM_ROWS_B, NUM_COLS_B);

    cout << "Evaluating Sequential Task" << endl;
    chrono::duration<double> Seq_Time(0);
    auto startTime = chrono::high_resolution_clock::now();
    sequential_matrix_multiply(MatrixA, NUM_ROWS_A, NUM_COLS_A,
        MatrixB, NUM_ROWS_B, NUM_COLS_B,
        Result);
    Seq_Time = chrono::high_resolution_clock::now() - startTime;

    //DisplayArray(MatrixA, NUM_ROWS_A, NUM_COLS_A);
    //cout << endl << endl;
    //DisplayArray(MatrixB, NUM_ROWS_B, NUM_COLS_B);
    //cout << endl << endl;
    //DisplayArray(Result, NUM_ROWS_A, NUM_COLS_B);

    cout << "Evaluating Parallel Task" << endl;
    chrono::duration<double> Seq_Time_Par(0);
    auto startTime_Par = chrono::high_resolution_clock::now();
    int Calculation_process_time = parallel_matrix_multiply(MatrixA, NUM_ROWS_A, NUM_COLS_A,
        MatrixB, NUM_ROWS_B, NUM_COLS_B,
        Result);
    Seq_Time_Par = chrono::high_resolution_clock::now() - startTime_Par;

    cout << "FINAL RESULTS" << endl;
    cout << "=============" << endl;
    cout << "Sequential Processing took: " << Seq_Time.count() * 1000 << endl;
    cout << "Parallel Processing took: " << Seq_Time_Par.count() * 1000 << endl;
    cout << "Parallel Calculation Processing took: " << Calculation_process_time << endl;
    cout << "=============" << endl;

    return 1;
}