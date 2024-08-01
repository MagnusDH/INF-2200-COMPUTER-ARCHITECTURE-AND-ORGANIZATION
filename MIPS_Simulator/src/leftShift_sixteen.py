import unittest
from cpuElement import  CPUElement
from testElement import TestElement


class Shift_left_Sixteen(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        '''
        Connect the left-shift component to input source
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
        # Shift sixteen bits to the left
        result = self.inputValues[self.inputA] << 16
        self.outputValues[self.outputName] = result

# Test class for shift-left-by-16 class
class TestSE(unittest.TestCase):
    def setUp(self):
        self.sl = Shift_left_Sixteen()
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
        [],
        ['inputA'],
        [],
        []
        )

        self.sl.connect(
        [(self.testInput, 'inputA')],
        ['shifted'],
        [],
        []
        )

        self.testOutput.connect(
        [(self.sl, 'shifted')],
        [],
        [],
        []
        )

    # Test correct behavior
    def test_correct_behavior(self):
        # Set input value for shift-component
        self.testInput.setOutputValue('inputA', 1)

        self.sl.readInput()
        self.sl.writeOutput()
        self.testOutput.readInput()

        # Check if output is as expected
        output = self.testOutput.inputValues['shifted']
        self.assertEqual(output, 65536)


if __name__ == '__main__':
    unittest.main()
