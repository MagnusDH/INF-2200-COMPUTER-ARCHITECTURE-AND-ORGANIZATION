import unittest
from cpuElement import  CPUElement
from testElement import TestElement

class Concatenator(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        '''
        Connect concatenator to input sources
        '''

        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        # Check if amount of input and output are correct
        assert(len(inputSources) == 2), 'Concatenator should only have one input'
        assert(len(outputValueNames) == 1), 'Concatenator should only have one output'
        assert(len(control) == 0), 'Concatenator has no control signal'
        assert(len(outputSignalNames) == 0), 'Concatenator has no control signal output'

        # Store the keys for the input and output values
        self.inputA = inputSources[0][1]
        self.inputB = inputSources[1][1]
        self.outputName = outputValueNames[0]

    def writeOutput(self):
        # Only want the 4 significant bits
        shiftR = self.inputValues[self.inputB] >> 28
        # Get number back to 32 bits, with 4 possible significant bits
        shiftL = shiftR << 28
        # Add the two addresses together
        result = self.inputValues[self.inputA] + shiftL
        self.outputValues[self.outputName] = result

# Test class for the concatenator
class TestConcatenator(unittest.TestCase):
    def setUp(self):
        self.shift = Concatenator()
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
            [],
            ['inputA', 'inputB'],
            [],
            []
        )

        self.shift.connect(
            [(self.testInput, 'inputA'), (self.testInput, 'inputB')],
            ['shiftData'],
            [],
            []
        )

        self.testOutput.connect(
            [(self.shift, 'shiftData')],
            [],
            [],
            []
        )

    # Testing the concatenator
    def test_correct_behavior(self):
        self.testInput.setOutputValue('inputA', 134217729)
        self.testInput.setOutputValue('inputB', 4026531840)
        self.shift.readInput()
        self.shift.writeOutput()
        self.testOutput.readInput()
        output = self.testOutput.inputValues['shiftData']

        # Check if output is as expected
        self.assertEqual(output, 4160749569)
        

if __name__ == '__main__':
    unittest.main()
