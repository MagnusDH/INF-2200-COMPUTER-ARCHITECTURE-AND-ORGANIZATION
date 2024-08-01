Stack:
high memory (0xffffff)
    
    []<-- EBP 
    [] 
    [] 
    []<-- ESP
    
low memory (0)

/*
ORIGINAL
%eax: int i (Largest)
%ebx: int left = 2*i+1
%ecx: int right = 2*i+2
%edx: int i
%esi: int array_size
%edi: int array[]



From last time trying to implement &array[i] and so on....
%eax: int i (Largest)
%ebx: array[i]
%ecx: array[largest]
%edx: int i
%esi: int array_size
%edi: int array[]
*/