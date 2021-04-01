#pragma once

#include<iostream>
#include"omp.h"

void quick_sort(int s[], int l, int r)
{
	if (l < r)
	{
		int i = l, j = r, x = s[l];
		while (i < j)
		{
			while (i < j && s[j] >= x) // ���������ҵ�һ��С��x����
				j--;
			if (i < j)
				s[i++] = s[j];
			while (i < j && s[i] < x) // ���������ҵ�һ�����ڵ���x����
				i++;
			if (i < j)
				s[j--] = s[i];
		}
		s[i] = x;
		
#pragma omp parallel for
		for(int thread=0;thread<2;thread++)
		{
			if(thread==0)
				quick_sort(s, l, i - 1); // �ݹ����
			else
				quick_sort(s, i + 1, r);
		}
	}
}