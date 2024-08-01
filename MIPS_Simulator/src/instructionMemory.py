'''Implemented by Magnus Dahl-Hansen'''

# The instruction memory's task is to read an adress value given by the ProgramCounter which is taken from memory.
# The value is to be read and converted into an instruction for further operations
# OperationCodes for MIPS: http://alumni.cs.ucr.edu/~vladimir/cs161/mips.html

import unittest
from testElement import TestElement
from cpuElement import CPUElement
from memory import Memory


class InstructionMemory(Memory):
    def __init__(self, filename):
        Memory.__init__(self, filename)

    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        # Checking if length of inputs and outputs are correct
        assert(len(inputSources) == 1), 'InstructionMemory should have one input'
        assert(len(outputValueNames) == 8), 'InstructionMemory has 8 outputs'
        assert(len(control) == 0), 'InstructionMemory has no control signal'
        assert(len(outputSignalNames) == 0), 'InstructionMemory does not have any control output'


        #Storing keys for the input and output values
        self.input = inputSources[0][1]
        self.opcode = outputValueNames[0]
        self.rs = outputValueNames[1]
        self.rt = outputValueNames[2]
        self.rt2 = outputValueNames[3]
        self.rd = outputValueNames[4]
        self.immediate = outputValueNames[5]
        self.funct = outputValueNames[6]
        self.address = outputValueNames[7]

    def writeOutput(self):
        hex1 = self.inputValues[self.input]
        bin1 = self.memory[hex1]

        # Set all bits outside the
        # output-field to 0
        opcode = (bin1 & 4227858432)>>26
        rs = (bin1 & 65011712)>>21
        rt = (bin1 & 2031616)>>16
        rd = (bin1 & 63488)>>11
        shamt = (bin1 & 1984)>>6
        funct = (bin1 & 63)>>0
        immediate = (bin1 & 65535)>>0
        address = (bin1 & 67108863)>>0

        self.outputValues[self.opcode] = opcode
        self.outputValues[self.rs] = rs
        self.outputValues[self.rt] = rt
        self.outputValues[self.rt2] = rt
        self.outputValues[self.rd] = rd
        self.outputValues[self.immediate] = immediate
        self.outputValues[self.funct] = funct
        self.outputValues[self.address] = address

class TestInstructionMemory(unittest.TestCase):
    def setUp(self):
        self.instructionmemory = InstructionMemory("add.mem")
        self.testInput = TestElement()
        self.testOutput = TestElement()


        self.testInput.connect(
            [],
            ['dataA'],
            [],
            []
        )

        self.instructionmemory.connect(
            [(self.testInput, 'dataA')],
            ['0', '1', '2', '3', '4', '5', '6', '7'],
            [],
            []
        )

        self.testOutput.connect(
            [(self.instructionmemory, '0'), (self.instructionmemory, '1'), (self.instructionmemory, '2'),
            (self.instructionmemory, '3'), (self.instructionmemory, '4'), (self.instructionmemory, '5'),
            (self.instructionmemory, '6'), (self.instructionmemory, '7')],        
            [],
            [],
            []
        )

    def test_correct_behavior(self):
        # Set input value
        self.testInput.setOutputValue('dataA', 0xbfc00000)

        self.instructionmemory.readInput()
        self.instructionmemory.writeOutput()
        self.testOutput.readInput()

        output0 = self.testOutput.inputValues['0']
        output1 = self.testOutput.inputValues['1']
        output2 = self.testOutput.inputValues['2']
        output3 = self.testOutput.inputValues['2']
        output4 = self.testOutput.inputValues['4']
        output5 = self.testOutput.inputValues['5']
        output6 = self.testOutput.inputValues['6']
        output7 = self.testOutput.inputValues['7']

        # Check if output is as expected
        self.assertEqual(output0, 2) # 000010 = 2
        self.assertEqual(output1, 31)
        self.assertEqual(output2, 16)
        self.assertEqual(output3, 16)
        self.assertEqual(output4, 0)
        self.assertEqual(output5, 128)
        self.assertEqual(output6, 0)
        self.assertEqual(output7, 66060416)


if __name__ == '__main__':
    unittest.main()
