#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <sys/time.h>

/*
 * Function received from the
 * time.c file from INF-1101
 */
unsigned long long gettime(void)
{
    struct timeval tp;
    unsigned long long ctime;

    gettimeofday(&tp, NULL);
    ctime = tp.tv_sec;
    ctime *= 1000000;
    ctime += tp.tv_usec;

    return ctime;
}


// Declaring that assembly function is provided elsewhere
extern void asm_function(int *array, int left, int right, int mid, int *L, int *R, int a1, int a2);

// This should be the C equivalent to the assembly implementation
void sort(int *array, int left, int right, int mid, int *L, int *R, int a1, int a2) {
	int i, j;

	// Putte begge for-loopene inn i mergesort istedet for å redusere arbeid? HUSK Å TA NY PROFILING
  // Copy the data into the temp arrays
  for(i = 0; i < a1; i++){
    L[i] = array[left + i];
  }
	// Copy the data into temp arrays
  for(j = 0; j < a2; j++){
    R[j] = array[mid + j + 1];
  }

  int m = 0;
  int n = 0;
  int p = left;

  // Compare elements from both arrays,
  // and add the smallest one into the main array
  while(m < a1 && n < a2){
    if(L[m] <= R[n]){
      array[p] = L[m];
      m++;

    } else {
      array[p] = R[n];
      n++;
    }
    p++;
  }

  // Check for remainding elements
  // in the first subarray, and adding
  // into the main array if
  while(m < a1){
    array[p] = L[m];
    m++;
    p++;
  }

  // Check for remainding elements
  // in the second subarray, and adding
  // into the main array if
  while(n < a2){
    array[p] = R[n];
    n++;
    p++;
  }
}

static void mergesort(int array[], int left, int right)
{
  if (left < right) {
    int mid = (left + right) / 2;

    // Sort first and second halves
    mergesort(array, left, mid);
    mergesort(array, mid + 1, right);

		// The amount of elements in the subarrays
		int a1 = mid - left + 1;
		int a2 = right - mid;

		// Temp arrays
		int L[a1];
		int R[a2];

		// Sort and put all the elements into a single array
		 asm_function(array, left, right, mid, L, R, a1, a2);
		// sort(array, left, right, mid, L, R, a1, a2);
  }
}

int main(int argc, char **argv) {

	if(argc != 2){
		printf("Usage: <number of elements>\n");
		return 1;
	}

	// Number of elements to sort
	int numitems = atoi(argv[1]);

	int i, number;
	int array[numitems];

	// Adding numbers in to the array
	for(i = 0; i < numitems; i++){
	  number = rand();
	  array[i] = number;
	}

	// Finding the size of the array
	int size = sizeof(array) / sizeof(array[0]);

	unsigned long long t1, t2;
	t1 = gettime();
	//Sorting the array in C
	mergesort(array, 0, size - 1);
	t2 = gettime();
	printf("Time used: %lluμs\n", t2-t1);

	  return 0;
}
