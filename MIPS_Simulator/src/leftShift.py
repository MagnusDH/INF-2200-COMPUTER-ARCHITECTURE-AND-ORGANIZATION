import unittest
from cpuElement import  CPUElement
from testElement import TestElement

class Shift_left(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        '''
        Connect left-shift component to input source
        '''
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        # Check if amount of input and output is correct
        assert(len(inputSources) == 1), 'Left-shift should only have one input'
        assert(len(outputValueNames) == 1), 'Left-shift should only have one output'
        assert(len(control) == 0), 'Left-shift has no control signal'
        assert(len(outputSignalNames) == 0), 'Left-shift has no control signal output'

        # Store the keys for the input and output values
        self.inputA = inputSources[0][1]
        self.outputName = outputValueNames[0]

    def writeOutput(self):
        # Shift two bits to the left
        result = self.inputValues[self.inputA] << 2
        self.outputValues[self.outputName] = result


# Class for testing the left-shift component
class TestShift_left(unittest.TestCase):
    def setUp(self):
        self.shift = Shift_left()
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
            [],
            ['inputA'],
            [],
            []
        )

        self.shift.connect(
            [(self.testInput, 'inputA')],
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

    # Testing the left-shift component
    def test_correct_behavior(self):
        # Set input value for left-shift component
        self.testInput.setOutputValue('inputA', 1)

        self.shift.readInput()
        self.shift.writeOutput()
        self.testOutput.readInput()

        # Check if output is as expected
        output = self.testOutput.inputValues['shiftData']
        self.assertEqual(output, 4)

        # Set input value for left-shift component
        self.testInput.setOutputValue('inputA', 10)
        self.shift.readInput()
        self.shift.writeOutput()
        self.testOutput.readInput()

        # Checking if output is as expected
        output = self.testOutput.inputValues['shiftData']
        self.assertEqual(output, 40)


if __name__ == '__main__':
    unittest.main()
