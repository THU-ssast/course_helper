#include<iostream>
#include<stdlib.h>
#include <chrono>   
#include <random>

#include"omp.h"
#include"merge_sort.h"
#include"quick_sort.h"

using namespace std;
using namespace chrono;


int main()
{
	for (int n = 1000; n <= 1000000; n *= 10)
	{
		// initialization
		//int n = NUM_SIZE;
		int* A = new int[n + 1];
		int* B = new int[n + 1]{ 0 };

		// generate random array
		std::random_device rd;
		std::uniform_int_distribution<int> dist(0, 10 * n);
		for (int i = 0; i < n; i++)
		{
			A[i] = dist(rd);
		}

		// sort

		auto start = system_clock::now();
		p_merge_sort(A, 1, n, B, 1);
		auto end = system_clock::now();
		auto duration = duration_cast<microseconds>(end - start);
		cout << double(duration.count()) * microseconds::period::num / microseconds::period::den << endl;

		start = system_clock::now();
		quick_sort(A, 1, n);
		end = system_clock::now();
		duration = duration_cast<microseconds>(end - start);
		cout << double(duration.count()) * microseconds::period::num / microseconds::period::den << endl;
	}


	return 0;
}