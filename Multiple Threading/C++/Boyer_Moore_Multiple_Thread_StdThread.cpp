/*

// Design Sprint  - Parallel Class
// Name Student: Minh Nguyen
// Student ID: 8723388

// Submit (MIMD) Version
*/

// Include Libraries
#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <thread>
#include <vector>

// Test Input Files
const std::string inputfile = "Hamlet.txt";

// Define the variables input to test for each design performances
std::vector<std::string> patterns = { "Horatio", "and", "Hamlet", "God" };
const int numThreads = 4;

// Function to stream large file using type BufIt defined type alias as a char type to iterator over all character in ifstream in and using rdbuf() function to read the alias type
std::string Reading_Files(std::string const& filename) {
    using BufIt = std::istreambuf_iterator<char>;
    std::ifstream in(filename);
    return std::string(BufIt(in.rdbuf()), BufIt());
}

void countWordsInSegment_MIMD(const std::string& text, const std::vector<std::string>& patterns,
    int& result_count_all_words_in_segment, int*& result_count_for_each_pattern, int patternSize) {

    std::istringstream iss(text);
    std::string word;
    int localCount = 0;

    // using iss >> word to fast loop through all words
    while (iss >> word) {
        ++localCount;
    }

    // Store the number of total words inside this specific chunk text
    result_count_all_words_in_segment = localCount;

    // Allocate memory for the list to store all the results is the count of times a specific word in specific patterns list occurred inside the text
    result_count_for_each_pattern = new int[patternSize + 1];

    for (size_t i = 0; i < patterns.size(); i++) {
        int count = 0;
        int length_pattern = patterns[i].size();
        int length_text_input = text.size();

        std::vector<int> bad_char(256, -1);

        for (int j = 0; j < length_pattern; j++) {
            bad_char[static_cast<int>(patterns[i][j])] = j;
        }

        int shift_value = 0;
        while (shift_value <= length_text_input - length_pattern) {
            int j = length_pattern - 1;
            while (j >= 0 && patterns[i][j] == text[shift_value + j])
                --j;

            if (j < 0) {
                ++count;
                shift_value += (shift_value + length_pattern < length_text_input) ? length_pattern - bad_char[text[shift_value + length_pattern]] : 1;
            }
            else {
                shift_value += std::max(1, j - bad_char[text[shift_value + j]]);
            }
        }
        result_count_for_each_pattern[i] = count;
    }
}

int main()
{
    auto startTime = std::chrono::high_resolution_clock::now();
    std::cout << "Start Process MIMD Design ..." << std::endl;
    std::string text = Reading_Files(inputfile);
    // Defined the list of threads and the results
    std::vector<std::thread> threads(numThreads);
    std::vector<std::string> chunk_char_each_threads(numThreads);
    std::vector<int> results_count_all_words_in_segment(numThreads);
    std::vector<int*> results_count_for_each_pattern(numThreads);
    int totalCount = 0;
    int sizepatterns = patterns.size();

    // Loop through all the threads to split the original text into chunks corresponding to the number of threads
    for (int i = 0; i < numThreads; i++) {
        int start = i * (text.size() / numThreads);
        int end = (i == numThreads - 1) ? text.size() : (start + (text.size() / numThreads));
        chunk_char_each_threads[i] = text.substr(start, end - start);
    }

    // Loop through all the threads to assign the task with their specific input - results location to write/read
    for (int i = 0; i < numThreads; i++) {
        threads[i] = std::thread([&, i]() {
            results_count_for_each_pattern[i] = new int[sizepatterns];
            countWordsInSegment_MIMD(chunk_char_each_threads[i], patterns,
                results_count_all_words_in_segment[i],
                results_count_for_each_pattern[i], sizepatterns);
            });
    }

    // Loop through all the threads to call join method to make the main thread wait for all threads to finish their works
    for (auto& thread : threads) {
        thread.join();
    }

    // Loop through all the results to sum up for total words counted inside each thread in results_count_all_words_in_segment int*
    for (int i = 0; i < numThreads; i++) {
        totalCount += results_count_all_words_in_segment[i];
    }

    // Loop through all the results corresponding to the pattern to sum up for total times that words are occurred are counted inside each thread in results_count_for_each_pattern int**
    for (size_t i = 0; i < patterns.size(); i++) {
        int patternTotalCount = 0;
        for (int j = 0; j < numThreads; j++) {
            patternTotalCount += results_count_for_each_pattern[j][i];
        }
        std::cout << patternTotalCount << ": " << patterns[i] << std::endl;
    }
    std::cout << "Total word count: " << totalCount << " words" << std::endl;

    // Delete allocated memory
    for (int i = 0; i < numThreads; i++) {
        delete[] results_count_for_each_pattern[i];
    }

    std::cout << "End Process MIMD Design" << std::endl;
    auto endTime = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> totalTime = endTime - startTime;
    std::cout << "Total time: " << totalTime.count() << " seconds" << std::endl;

    return 0;
}