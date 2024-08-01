#include "asmdef.h"

DECLARE_GLOBAL(asm_test)


################################################################################
# name:          asm_test
# action:        
# in:             
#
# out:
# modifies:
# notes:
################################################################################
FUNC(asm_test):

	# Setting up registers to start doing some assembly awesomeness
	pushl %ebp			# Preserving old stackframe
	movl %esp, %ebp		# Create a new stackframe
	pushl %ebx
	pushl %esi			# Preserve called saved register so...
	pushl %edi			# We can use them

	# Moving all arguments into registers and stack
	movl 8(%ebp), %ebx	# %ebx = first argument
	movl 12(%ebp), %ecx	# %ecx = second argument

	jmp swap
	
	# movl $33, (%ebx)	# Modifying ebx pointer
	# movl (%ebx), %eax	# %eax = value in a (&a)
		
	# jmp end				# Jumping to end-function

swap:
	# %edx = tmp
	movl %ebx, %edx		# tmp/%edx = a	
	movl %ecx, %ebx		# %ecx = *b
	movl %edx, %ecx		# %edi = tmp

	movl %ebx, %eax

	jmp end
end:
	# Restoring registers to previous state
	popl %edi
	popl %esi
	popl %ebx
	popl %ebp
	
	
	
	ret		# returning whatever exists in %eax register