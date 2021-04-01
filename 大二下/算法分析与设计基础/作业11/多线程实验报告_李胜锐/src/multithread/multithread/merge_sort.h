#pragma once

#include<iostream>
#include"omp.h"

int binary_search(int x, int* T, int p, int r)
{
	int low = p;
	int high = p > (r + 1) ? p : (r + 1);
	while (low < high)
	{
		int mid = (low + high) / 2;
		if (x <= T[mid])
		{
			high = mid;
		}
		else
		{
			low = mid + 1;
		}
	}
	return high;
}

void p_merge(int* T, int p1, int r1, int p2, int r2, int* A, int p3)
{
	int n1 = r1 - p1 + 1;
	int n2 = r2 - p2 + 1;
	if (n1 < n2)
	{
		int tmp = 0;
		tmp = p1; p1 = p2; p2 = tmp;
		tmp = r1; r1 = r2; r2 = tmp;
		tmp = n1; n1 = n2; n2 = tmp;
	}
	if (n1 == 0)
		return;
	else
	{
		int q1 = (p1 + r1) / 2;
		int q2 = binary_search(T[q1], T, p2, r2);
		int q3 = p3 + (q1 - p1) + (q2 - p2);
		A[q3] = T[q1];

#pragma omp parallel for
		for (int thread = 0; thread < 2; thread++)
		{
			if (thread == 0)
				p_merge(T, p1, q1 - 1, p2, q2 - 1, A, p3);
			else
				p_merge(T, q1 + 1, r1, q2, r2, A, q3 + 1);
		}
	}


}

void p_merge_sort(int* A, int p, int r, int* B, int s)
{
	int n = r - p + 1;
	if (n == 1)
	{
		B[s] = A[p];
	}
	else
	{
		int* T = new int[n + 1];
		int q = (p + r) / 2;
		int q_prime = q - p + 1;
#pragma omp parallel for
		for (int thread = 0; thread < 2; thread++)
		{
			if (thread == 0)
				p_merge_sort(A, p, q, T, 1);
			else
				p_merge_sort(A, q + 1, r, T, q_prime + 1);
		}
		p_merge(T, 1, q_prime, q_prime + 1, n, B, s);

		delete[] T;
	}
}
