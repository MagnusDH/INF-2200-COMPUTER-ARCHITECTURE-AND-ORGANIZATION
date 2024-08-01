#include "asmdef.h"

DECLARE_GLOBAL(asm_function)


################################################################################
# name:          asm_function
# action:        
# in:            
#
# out:
# modifies:
# notes:
################################################################################
FUNC(asm_function):

	# Setting up registers to start doing some assembly awesomeness
	pushl %ebp			# Preserving old stackframe
	movl %esp, %ebp		# Create a new stackframe
	pushl %ebx
	pushl %esi			# Preserve called saved register so...
	pushl %edi			# We can use them


	# Moving all arguments into registers
	movl 8(%ebp), %edi	# edi = first argument(int array[])
	movl 12(%ebp), %esi # esi = second argument(int array_size)
	movl 16(%ebp), %edx	# edx = third argument(int i)

	# %eax = largest = i
	movl %edx, %eax	# Moving int i into %eax

	# %ebx = int left = 2*i+1;
	movl %edx, %ebx	# duplication "int i" into %ebx
	imul $2, %ebx	# %ebx = 2 * i
	addl $1, %ebx	# %ebx += 1
	
	
	# %ecx = int right = 2*i+2
	movl %edx, %ecx	# duplication "int i" into %ebx
	imul $2, %ecx	# %ecx = 2 * i
	addl $2, %ecx	# %ecx += 2

	jmp if1			# Jumping to first if-statement

# IF(left < array_size)
if1:
	cmpl %esi, %ebx	# Comparing ebx(left) with esi(array_size)
	jb if11			# jump to "if11" if left < array_size
	jmp if2			# if left is not less than array_size, jump to second if statement

# IF(array[left] > array[largest])
if11:
	pushl %ecx	# Pushing ecx to stack to make room for comparing function
	pushl %edx	# Pushing edx to stack to make room for comparing function

	movl (%edi, %ebx, 4), %ecx	# %ecx contains array[left] value
	movl (%edi, %eax, 4), %edx	# %edx contains array[largest] value
	
	cmpl %edx, %ecx				# Comparing ecx with edx
	ja if111					# Jump to if111 if ecx > edx
	
	# Restoring registers and stack back to normal if the "ja" jump did not execute
	# for code to run correct
	popl %edx					# Restoring int i back to edx
	popl %ecx					# Restoring int right back to ecx
	jmp if2						# if array[left] is not greater than array[largest], jump to second if-statement


# largest = left (line 126 in main.c)
if111:
	movl %ebx, %eax	# Largest(eax) = left(ebx)
	popl %edx		# Restoring int i back to edx
	popl %ecx		# Restoring int right back to ecx
	jmp if2			# Jumping to next if statement


# IF(right < array_size)
if2:
	cmpl %esi, %ecx	# Comparing ecx(right) with esi(array_size)
	jb if22			# jump to if22 if right < array_size
	jmp if3			# jump to if3 if right is not less than array_size

# IF(array[right] > array[largest])
if22:
	pushl %ebx		# Pushing ebx to stack to make room for comparing function
	pushl %edx		# Pushing edx to stack to make room for comparing function

	movl (%edi, %ecx, 4), %ebx	# %ebx contains array[right]
	movl (%edi, %eax, 4), %edx	# %edx contains array[largest]

	cmpl %edx, %ebx				# Comparing ebx with edx
	ja if222					# Jump to if222 if ebx > edx

	# Restoring registers and stack back to normal if the "ja" jump did not execute
	# for code to run correct
	popl %edx		# Restoring int i back to edx
	popl %ebx		# Restoring int left back to ebx
	jmp if3			# if array[right] is not greater than array[largest], jump to if3

# largest = right
if222:
	movl %ecx, %eax	# Largest(eax) = right(ecx)
	popl %edx		# Restoring int i back to edx
	popl %ebx 		# Restoring int left back to ebx

# IF(largest != i)
if3:
	cmpl %edx, %eax	# Comparing eax with edx
	jne if33		# jump to if33 if eax != edx
	jmp end			# if largest == i, jump to end

if33:
	movl (%edi, %edx, 4), %ebx	# %ebx = array[i]
	movl (%edi, %eax, 4), %ecx	# %ecx = array[largest]

	jmp swap


swap:
	# pushl %eax	# Pushing %eax to stack to make room for tmp register
	# Comment: ebx = array[i]
	# Comment: %ecx = array[largest]
	
	movl %ecx, (%edi, %edx, 4)		# Moving value in ecx to adress in array	
	movl %ebx, (%edi, %eax, 4)		# Moving value in ebx to adress in array

	# popl %eax			# Popping int largest back to its register
	pushl %eax			# Pushing int largest to stack for argument in heapify
	pushl %esi			# Pushing int array_size to stack for argument in heapify
	pushl %edi			# Pushing int array[] to stack for argument in heapify 
	
	call asm_function
	
# Cleaning up stack 
	popl %edi
	popl %esi
	popl %eax

	jmp end

end:
	# Restoring registers to previous state
	popl %edi
	popl %esi
	popl %ebx
	popl %ebp

	ret		# returning whatever exists in %eax register