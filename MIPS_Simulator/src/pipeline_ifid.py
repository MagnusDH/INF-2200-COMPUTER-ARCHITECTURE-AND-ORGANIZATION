import unittest
from cpuElement import CPUElement
from testElement import TestElement


class Pipeline_IfId(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        '''
        Connect pipeline to input sources
        '''
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        # Check if amount of input/output are correct
        assert(len(inputSources) == 9), 'Ifid-pipeline should only have nine inputs'
        assert(len(outputValueNames) == 9), 'Ifid-pipeline should only have nine outputs'
        assert(len(control) == 0), 'Ifid-pipeline should not have control signals'
        assert(len(outputSignalNames) == 0), 'Ifid-pipeline should not have output-control signals'

        # Store the keys for the input values
        self.newAddress = inputSources[0][1]
        self.opcode = inputSources[1][1]
        self.rs = inputSources[2][1]
        self.rt = inputSources[3][1]
        self.rt2 = inputSources[4][1]
        self.rd = inputSources[5][1]
        self.immediate = inputSources[6][1]
        self.funct = inputSources[7][1]
        self.address = inputSources[8][1]

        # Store the keys for the output values
        self.out1 = outputValueNames[0]
        self.out2 = outputValueNames[1]
        self.out3 = outputValueNames[2]
        self.out4 = outputValueNames[3]
        self.out5 = outputValueNames[4]
        self.out6 = outputValueNames[5]
        self.out7 = outputValueNames[6]
        self.out8 = outputValueNames[7]
        self.out9 = outputValueNames[8]

    # Send output
    def writeOutput(self):
        self.outputValues[self.out1] = self.inputValues[self.newAddress]
        self.outputValues[self.out2] = self.inputValues[self.opcode]
        self.outputValues[self.out3] = self.inputValues[self.rs]
        self.outputValues[self.out4] = self.inputValues[self.rt]
        self.outputValues[self.out5] = self.inputValues[self.rt2]
        self.outputValues[self.out6] = self.inputValues[self.rd]
        self.outputValues[self.out7] = self.inputValues[self.immediate]
        self.outputValues[self.out8] = self.inputValues[self.funct]
        self.outputValues[self.out9] = self.inputValues[self.address]

    # Testclass for pipeline
class TestPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = Pipeline_IfId()
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
        [],
        ['inputA', 'inputB', 'inputC', 'inputD', 'inputE', 'inputF', 'inputG', 'inputH', 'inputI'],
        [],
        []
        )

        self.pipeline.connect(
        [(self.testInput, 'inputA'), (self.testInput, 'inputB'), (self.testInput, 'inputC'), (self.testInput, 'inputD'), (self.testInput, 'inputE'),
         (self.testInput, 'inputF'), (self.testInput, 'inputG'), (self.testInput, 'inputH'), (self.testInput, 'inputI')],
        ['out1', 'out2', 'out3', 'out4', 'out5', 'out6', 'out7', 'out8', 'out9'],
        [],
        []
        )

        self.testOutput.connect(
        [(self.pipeline, 'out1'), (self.pipeline, 'out2'), (self.pipeline, 'out3'), (self.pipeline, 'out4'), (self.pipeline, 'out5'),
         (self.pipeline, 'out6'), (self.pipeline, 'out7'), (self.pipeline, 'out8'), (self.pipeline, 'out9'), ],
        [],
        [],
        []
        )

    def test_correct_behavior(self):
        # Set input values
        self.testInput.setOutputValue('inputA', 0)
        self.testInput.setOutputValue('inputB', 1)
        self.testInput.setOutputValue('inputC', 2)
        self.testInput.setOutputValue('inputD', 3)
        self.testInput.setOutputValue('inputE', 4)
        self.testInput.setOutputValue('inputF', 5)
        self.testInput.setOutputValue('inputG', 6)
        self.testInput.setOutputValue('inputH', 7)
        self.testInput.setOutputValue('inputI', 8)

        self.pipeline.readInput()
        self.pipeline.writeOutput()
        self.testOutput.readInput()

        # Store the output values
        out1 = self.testOutput.inputValues['out1']
        out2 = self.testOutput.inputValues['out2']
        out3 = self.testOutput.inputValues['out3']
        out4 = self.testOutput.inputValues['out4']
        out5 = self.testOutput.inputValues['out5']
        out6 = self.testOutput.inputValues['out6']
        out7 = self.testOutput.inputValues['out7']
        out8 = self.testOutput.inputValues['out8']
        out9 = self.testOutput.inputValues['out9']

        # Check if output is as expected
        self.assertEqual(out1, 0)
        self.assertEqual(out2, 1)
        self.assertEqual(out3, 2)
        self.assertEqual(out4, 3)
        self.assertEqual(out5, 4)
        self.assertEqual(out6, 5)
        self.assertEqual(out7, 6)
        self.assertEqual(out8, 7)
        self.assertEqual(out9, 8)

if __name__ == '__main__':
    unittest.main()
