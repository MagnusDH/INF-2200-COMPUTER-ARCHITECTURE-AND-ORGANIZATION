'''
Implements base class for memory elements.

Note that since both DataMemory and InstructionMemory are subclasses of the Memory
class, they will read the same memory file containing both instructions and data
memory initially, but the two memory elements are treated separately, each with its
own, isolated copy of the data from the memory file.

Code written for inf-2200, University of Tromso
'''

from cpuElement import CPUElement
import common

class Memory(CPUElement):
    def __init__(self, filename):

        # Dictionary mapping memory addresses to data
        # Both key and value must be of type 'int'
        self.memory = {}

        self.initializeMemory(filename)

    def initializeMemory(self, filename):
        '''
        Helper function that reads initializes the data memory by reading input
        data from a file.
        '''
        # Open and read from mem-file
        file = open(filename, 'r')
        lines = file.readlines()
        file.close()
        mylist = []

        # GO through each line in mem-file
        for element in lines:
            # If line is a comment, or empty,
            # skip it
            if not element.startswith("#"):
                if not element.startswith("\n"):
                    # Only interested in the first
                    # 21 characters
                    element = element[0:21]
                    # Seperate lines into words
                    element = element.split()
                    # Split into words, and
                    # add the words into "mylist"
                    element[0] = int(element[0], 16)
                    element[1] = int(element[1], 16)
                    mylist.append(element)

        # Adding hex string to dict as key,
        # and binary string to dict as value
        for element in mylist:
            self.memory[element[0]] = element[1]


    def printAll(self):
        for key in sorted(self.memory.keys()):
            print("%s\t=> %s\t(%s)" % (hex(int(key)), common.fromUnsignedWordToSignedWord(self.memory[key]), hex(int(self.memory[key]))))
