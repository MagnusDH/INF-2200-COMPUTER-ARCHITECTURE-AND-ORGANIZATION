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
		
	# jmp end				# Jumping to end-function

swap:
	movl (%ebx), %edi	# Moving adress in ebx to edi
	movl (%ecx), %esi	# Moving adress in ecx to esi
	
	movl %edi, (%ecx)	# Moving value in edi to adress in ecx
	movl %esi, (%ebx)	# Moving value in esi to adress in ebx

	jmp end
end:
	# Restoring registers to previous state
	popl %edi
	popl %esi
	popl %ebx
	popl %ebp
	
	ret		# returning whatever exists in %eax register