'''
Implements CPU element for Data Memory in MEM stage.

Code written for inf-2200, University of Tromso
'''

import unittest
from cpuElement import CPUElement
from testElement import TestElement
from memory import Memory
import random

class DataMemory(Memory):
    def __init__(self, filename):
        Memory.__init__(self, filename)

    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        '''
        Connect datamemory to input sources and controller
        '''
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        # Check if the amount of input and output are correct
        assert(len(inputSources) == 2), 'Datamemory should only have two inputs'
        assert(len(outputValueNames) == 1), 'Datamemory should only have one output'
        assert(len(control) == 2), 'Datamemory should only have two control signals'
        assert(len(outputSignalNames) == 0), 'Datamemory should not output control signals'

        # Store the keys for the input- and output values
        self.inputA = inputSources[0][1]
        self.inputB = inputSources[1][1]
        self.outputName = outputValueNames[0]
        self.controlRead = control[0][1]
        self.controlWrite = control[1][1]

    def writeOutput(self):
        # Store the keys for the control signals
        memRead = self.controlSignals[self.controlRead]
        memWrite = self.controlSignals[self.controlWrite]

        # Check if control signals are correct
        assert(isinstance(memRead, int)), 'MemRead signal is not an int'
        assert(isinstance(memWrite, int)), 'MemWrite signal is not an int'
        assert(memRead == 0 or memRead == 1), 'MemRead signal is not 0 or 1'
        assert(memWrite == 0 or memWrite == 1), 'MemWrite signal is not 0 or 1'

        # Store memory address to read from and/or write to
        reg = self.inputValues[self.inputA]

        # Read from memory if
        # read signal is 1
        if memRead == 1:
            # Check if key is in memory
            if reg in self.memory:
                # Look up data from given address, and give as output
                regOut = self.memory[reg]
                self.outputValues[self.outputName] = regOut
            # If key is not in memory
            # output 0
            else:
                regOut = 0
                self.outputValues[self.outputName] = regOut

        # If write signal is 1,
        # write data to the given address
        if memWrite == 1:
            # Store the data given as second input
            data = self.inputValues[self.inputB]
            # Write data to memory
            self.memory[reg] = data

# Class for testing the datamemory
class Test_dataMemory(unittest.TestCase):
    def setUp(self):
        self.dataMemory = DataMemory('add.mem')
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
        [],
        ['inputA', 'inputB'],
        [],
        ['controlA, controlB']
        )

        self.dataMemory.connect(
        [(self.testInput, 'inputA'), (self.testInput, 'inputB')],
        ['memData'],
        [(self.testInput, 'controlA'), (self.testInput, 'controlB')],
        []
        )

        self.testOutput.connect(
        [(self.dataMemory, 'memData')],
        [],
        [],
        []
        )

    # Testing the behavior of the datamemory
    def test_correct_behavior(self):
        for i in range(100):
            j = random.randint(0, 100)
            # Give input values to the data memory
            self.testInput.setOutputValue('inputA', i)
            self.testInput.setOutputValue('inputB', j)

            # Set memory-read singal to low,
            # and memory-write signal to high
            self.testInput.setOutputControl('controlA', 0)
            self.testInput.setOutputControl('controlB', 1)

            # Read input and perform operations
            self.dataMemory.readInput()
            self.dataMemory.readControlSignals()
            self.dataMemory.writeOutput()
            self.testOutput.readInput()

            # Set memory-read signal to high,
            # and memory-write signal to low
            self.testInput.setOutputControl('controlA', 1)
            self.testInput.setOutputControl('controlB', 0)

            # Read input and perform operations
            self.dataMemory.readInput()
            self.dataMemory.readControlSignals()
            self.dataMemory.writeOutput()
            self.testOutput.readInput()

            # Check if output is as expected
            output = self.testOutput.inputValues['memData']
            self.assertEqual(output, j)


if __name__ == '__main__':
    unittest.main()
