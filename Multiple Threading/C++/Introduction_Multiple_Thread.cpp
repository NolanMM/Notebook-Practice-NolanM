/*
//	Code by Minh Nguyen
//	Student ID: 8723388
//	Lab 1 - Parallel Class
//	Date: 11/09/2023
*/

#include <thread>
#include <iostream>
#include <chrono>

// Function prototype
void instruction();
void instruction_thread_2();
void instruction_thread_3(const char* name);
void instruction_thread_4(const char* name);

void instruction() {
	std::cout << "Thread 1 is running" << std::endl;
	while(true){
		std::cout << "Thread Id " << std::this_thread::get_id() << ": Cleanup Complete" << std::endl;
		std::this_thread::sleep_for(std::chrono::seconds(1));
	}
}

void instruction_thread_2() {
	std::cout << "Thread 2 instruction_2 is running" << std::endl;
	// Create thread 3 and 4 and wait for them to complete
	std::thread T3(instruction_thread_3, "<Name Thread 3>");
	T3.join();
	std::thread T4(instruction_thread_4, "<Name Thread 4>");
	T4.join();
	std::cout << "Thread 2 has completed because thread 3 and thread 4 have completed" << std::endl;
}

void instruction_thread_3(const char* name) {
	std::cout << name << " is running" << std::endl;
	std::this_thread::sleep_for(std::chrono::seconds(5));
	std::cout << "Thread 3: " << name << " complete" << std::endl;
}

void instruction_thread_4(const char* name) {
	std::cout << name << " is running" << std::endl;
	std::this_thread::sleep_for(std::chrono::seconds(2));
	std::cout << "Thread 4: " << name <<  " complete" << std::endl;
}

int main() {
	// Create thread 1 and turn to deamon thread
	std::thread T1(instruction);
	T1.detach();
	std::this_thread::sleep_for(std::chrono::seconds(1));
	std::thread T2(instruction_thread_2);
	//T2.join();
	// Check if thread 2 is joinable
	if (T2.joinable()) { T2.join(); }
	else { std::cout << "Thread 2 is not joinable" << std::endl; }
	std::cout << "Main thread is now terminating" << std::endl;
}