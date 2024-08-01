import unittest
from cpuElement import CPUElement
from testElement import TestElement


class SignExtend(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        '''
        Connect sign-extend to input source
        '''
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        # Check if amount of input and output is correct
        assert(len(inputSources) == 1), 'SignExtend should only have one input'
        assert(len(outputValueNames) == 1), 'SignExtend should only have one ouput'
        assert(len(control) == 0), 'SignExtend should not recieve control signals'
        assert(len(outputSignalNames) == 0), 'SignExtend should not output control signals'

        # Store the keys for the input and output values
        self.inputA = inputSources[0][1]
        self.outputName = outputValueNames[0]

    def writeOutput(self):
        # Extend the input by 16 bits
        result = self.inputValues[self.inputA]
        tmp = result >> 15
        # Check the most significant bit
        if tmp == 0:
            result = result | 0x00000000
        else:
            result = result | 0xffff0000

        self.outputValues[self.outputName] = result

# Class for testing the behavior of the
# sign extend component
class TestSE(unittest.TestCase):
    def setUp(self):
        self.se = SignExtend()
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
            [],
            ['inputA'],
            [],
            []
        )

        self.se.connect(
            [(self.testInput, 'inputA')],
            ['seData'],
            [],
            []
        )

        self.testOutput.connect(
            [(self.se, 'seData')],
            [],
            [],
            []
        )

    # Test if sign-extend component is
    # working as intended
    def test_correct_behavior(self):
        self.testInput.setOutputValue('inputA', 14)
        self.se.readInput()
        self.se.writeOutput()
        self.testOutput.readInput()

        # Check if output is as expected
        output = self.testOutput.inputValues['seData']
        self.assertEqual(output, 14)

        self.testInput.setOutputValue('inputA', -8)
        self.se.readInput()
        self.se.writeOutput()
        self.testOutput.readInput()

        # Check if output is as expected
        output = self.testOutput.inputValues['seData']
        self.assertEqual(output, -8)


if __name__ == '__main__':
    unittest.main()
