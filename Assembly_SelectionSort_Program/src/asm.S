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
pushl %ebp 						# Preserving the old stack frame
movl %esp, %ebp 			# Creating a new stack frame
pushl %ebx 						# Pushing %ebx onto the stack
pushl %esi 						# Preserve caller saved registers so we can use them
pushl %edi 						# Preserve caller saved registers so we can use them

# Setting up registers before the loop
movl 24(%ebp), %eax 			# %eax = L[]
movl 8(%ebp), %ebx 				# %ebx = array[]
movl 32(%ebp), %ecx				# %ecx = a1
movl 12(%ebp), %edx				# %edx = left
movl $0, %edi             # %edi = i
addl %edi, %edx						# %edx = left + i

# Copy elements from array into tmp array
loop1:
	cmpl %ecx, %edi         		# comparing a1 with i
  jge end											# jump to end if: i >= a1
	pushl %ecx									# pushing a1 to the stack
	movl (%ebx, %edx, 4), %ecx  # %ecx = array[left + i]
	movl %ecx, (%eax, %edi, 4)	# L[i] = array[left + i]
	incl %edi										# i++
	incl %edx										# %edx++
	popl %ecx										# popping a1 back to ecx
	jmp loop1										# Jumping back to beginning of "loop1"

# Setting up registers before the loop
end:
													# %ebx = array[]
	movl 28(%ebp), %eax			# %eax = R[]
	movl $0, %edi						# %edi = j = 0
	movl 20(%ebp), %edx			# %edx = mid
	addl %edi, %edx					# %edx = mid + j
	incl %edx 							# %edx = mid + j + 1
	movl 36(%ebp), %ecx			# %ecx = a2

# Copy elements from array into tmp array
loop2:
	cmpl %ecx, %edi							# comparing a2 with j
	jge end2										# jump to end2 if j >= a2
	pushl %ecx									# pushing a2 to the stack
	movl (%ebx, %edx, 4), %ecx	# %ecx = array[mid+j+1]
	movl %ecx, (%eax, %edi, 4)	# R[j] = array[mid+j+1]
	incl %edi										# j++
	incl %edx										# %edx++
	popl %ecx										# %ecx = a2
	jmp loop2										# Jumping back to beginning of "loop2"

# Setting up variables into registers for the while loop
end2:
    											# %eax = R[]
													# %ebx = array[]
	movl 24(%ebp), %ecx			# %ecx = L[]
	movl 12(%ebp), %edx			# %edx = p = left
	pushl %edx							# push p on the stack
	movl 32(%ebp), %edx			# %edx = a1
	movl $0, %edi						# %edi = m
	movl $0, %esi						# %esi = n

# Check if m >= a1
first:
	cmpl %edx, %edi				# comparing a1 with m
	pushl %edx						# pushing a1 to stack
	jge endFirst					# jumping to endfirst if m >= a1
	jb second							# jumping to second if m < a1

# Check if n >= a2
second:
	movl 36(%ebp), %edx			# %edx = a2
	cmpl %edx, %esi					# comparing a2 with n
	pushl %edx							# pushing a2 to stack
	jge endSecond						# jumping to endSecond if n >= a2
	jb if										# jumpin to "if" if n < a2

# Comparing L[m] and R[n]
if:
	movl (%ecx, %edi, 4), %edx	# %edx = L[m]
	cmpl (%eax, %esi, 4), %edx	# comparing L[m] with R[n]
	pushl %esi									# pushing n to stack
	pushl %eax									# pushing R[] to stack
	movl 16(%esp), %eax					# %eax = p (from stack)
	jg else											# jump to "else" if R[n] > L[m]
	movl %edx, (%ebx, %eax, 4)	# array[p] = L[m]
	incl %edi										# m++
	incl %eax										# p++
	jmp resetif									# jumping to "resetif"

# If R[n] > L[m], add R[n]
# into array[p]
else:
	popl %edx										# popping R[] from stack into %edx
	pushl %edi									# pushing m to stack
	movl 4(%esp), %edi					# copying n from stack into %edi (second element)
	movl (%edx, %edi, 4), %esi	# %esi = R[n]
	movl %esi, (%ebx, %eax, 4)	# array[p] = R[n]
	incl %edi										# n++
	incl %eax										# p++
	jmp resetelse								# jumping to "resetelse"

	# Reset stack and registers to
	# be similar to when the loop started
	resetif:
	popl %edx										# edx = R[]
	popl %esi 									# esi = n
	popl %edx										# edx = a2, clearing the stack
	popl %edx										# edx = a1, clearing the stack
	popl %edx										# edx = p, clearing the stack
	pushl %eax     							# pushing updated p value on the stack
	movl 28(%ebp), %eax      		# eax = R[]
	movl 32(%ebp), %edx					# edx = a1
	jmp first										# jumping back to "first"

	# Reset stack and registers to
	# be similar to when the loop started
resetelse:
	movl %edi, %esi 			# esi = n
	popl %edi							# edi = m
	popl %edx							# edx = n, clearing the stack
	popl %edx							# edx = a2, clearing the stack
	popl %edx							# edx = a1, clearing the stack
	popl %edx							# edx = p, clearing the stack
	pushl %eax						# pushing updated p on the stack
	movl 32(%ebp), %edx   # edx = a1
	movl 28(%ebp), %eax   # eax = R[]
	jmp first							# jumping back to "first"

# If left tmp-array has reached the end
endFirst:
	popl %edx							# %edx = a1, clearing from stack
	popl %edx							# %edx = p
	movl 36(%ebp), %ecx		# %ecx = a2

# Add the remaining elements
# into the main array
loop3:
		cmpl %ecx, %esi 							# comparing n with a2
		jge finish										# jump to finish if n >= a2
		movl (%eax, %esi, 4), %edi 		# %edi = R[n]
		movl %edi, (%ebx, %edx, 4)		# array[p] = R[n]
		incl %esi 										# n++
		incl %edx											# p++
		jmp loop3											# jump back to "loop3"

# If right tmp-array has reached the end
endSecond:
	popl %edx							# edx = a2 (no need for this)
	popl %edx							# edx = a1
	popl %esi 						# esi = p

# Add the remaining elements
# into the main array
loop4:
	cmpl %edx, %edi          			# comparing m with a1
	jge finish										# jump to "finish" if m >= a1
	movl (%ecx, %edi, 4), %eax		# %eax = L[m]
	movl %eax, (%ebx, %esi, 4)		# array[p] = L[m]
	incl %edi 										# m++
	incl %esi                    	# p++
	jmp loop4											# jumping back to "loop4"

# Pop preserved caller values to
# their corresponding registers
finish:
	popl %edi
	popl %esi
	popl %ebx
	popl %ebp
	ret
