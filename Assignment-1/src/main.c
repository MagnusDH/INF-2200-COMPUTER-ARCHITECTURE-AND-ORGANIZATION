#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>

// Declaring that assembly function is provided elsewhere
// extern void asm_function();
extern int asm_function();
extern int asm_test();

// This should be the C equivalent to the assembly implementation
void c_function() {
	
}

/*Prints a given array*/
void print_array(int array[], int size)
{
	printf("Array[");

	for(int i=0; i<size; i++){
		printf("%d, ", array[i]);
	}

	printf("]\n");
}

/*Second part of "merge" function which is implemented in assembly*/
void second_part_of_merge(int part1, int part2, int left_array[], int right_array[], int array[], int start)
{
	int i = 0;
	int j = 0;
	int k = start;

	while(i < part1 && j < part2){
		if(left_array[i] <= right_array[j]){
			array[k] = left_array[i];
			i++;
		}
		else{
			array[k] = right_array[j];
			j++;
		}

		k++;
	}

	while(i < part1){
		array[k] = left_array[i];
		i++;
		k++;
	}

	while(j < part2){
		array[k] = right_array[j];
		j++;
		k++;
	}
}

/*Sorts and merges arrays*/
void merge(int array[], int start, int mid, int end)
{
	int i, j, k;

	/*Defining size of the arrays two halves*/
	int part1 = mid - start +1;
	int part2 = end - mid;

	/*Creating arrays for the two halves*/
	int left_array[part1];
	int right_array[part2];

	/*Filling the two halves with elements from original array*/
	for(i=0; i<part1; i++){
		left_array[i] = array[start+i];
	}

	for(j=0; j<part2; j++){
		right_array[j] = array[mid+1+j];
	} 

	second_part_of_merge(part1, part2, left_array, right_array, array, start);
	// asm_function(part1, part2, left_array, right_array, array, start);
}

/*Recursivly dividing and sorting given array*/ 
void mergesort(int array[], int start, int end)
{
	if(start < end){
		//Finding middle of array
		int middle = start+(end-start)/2;

		//recursivly sorting both the halves
		mergesort(array, start, middle);
		mergesort(array, middle+1, end);

		//Merge the two half arrays
		merge(array, start, middle, end);
	}
}




/*Swaps the position of two elements*/
void swap(int *a, int *b)
{
	int temp = *a;
	*a = *b;
	*b = temp;
}

/*Creates a MAX-heap of a given array*/
//i = number of non-leaf-nodes in a tree
void heapify(int array[], int array_size, int i)
{
	//Find largest node among root node, left child and right child
	int largest = i;
	int left = 2*i+1;	//Left node of root node
	int right = 2*i+2;	//Right node of root node

	//Checking if left child node is smaller than its parent node
	//Swaps the nodes if child node is greater than parent node 
	if(left < array_size && array[left] > array[largest]){
		largest = left;
	}

	//Checking if right child node is smaller than its parent node
	//Swaps the nodes if child node is greater than parent node 
	if(right < array_size && array[right] > array[largest]){
		largest = right;
	}

	//Swap and continue heapifying if the root is not the largest
	if(largest != i){
		swap(&array[i], &array[largest]);
		heapify(array, array_size, largest);
	}
}

void heapsort(int array[], int array_size)
{
	//Creating a max-heap of the array
	int n = array_size/2 - 1;	//Number of non-leaf-nodes in the tree
	int result;
	int result2;

	for(int i = n; i >= 0; i--){
		//heapify(array, array_size, i);
		result = asm_function(array, array_size, i);
		// printf("Result = %d\n", result);
	}

	//Heap sort
	for(int i = array_size-1; i >= 0; i--){
		swap(&array[0], &array[i]);
		
		//Heapify root element to get the highest element at root again
		int k = 0;
		//heapify(array, i, 0);
		result2 = asm_function(array, i, 0);
		//printf("Result2 = %d\n", result2);
	}
}


int main(int argc, char **argv) {
	

	int array_size = 4;
	int random_number = 10;
				
	int array[4] = {9, 2, 6, 3};

	// /*preparing random numbers*/
	// srand((unsigned)time(NULL));

	// for(int i=0; i<array_size; i++){
	// 	array[i] = rand() % random_number;
	// }
	print_array(array, array_size);
	heapsort(array, 4);
	print_array(array, array_size);
}