import unittest
from cpuElement import CPUElement
from testElement import TestElement


class Pipeline_MemWb(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        '''
        Connect pipeline to input sources and controller
        '''
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        # Check if amount of input and output are correct
        assert(len(inputSources) == 6), 'MemWb-pipeline should only have six inputs'
        assert(len(outputValueNames) == 6), 'MemWb-pipeline should only have six outputs'
        assert(len(control) == 3), 'MemWb-pipeline should only have three control signals'
        assert(len(outputSignalNames) == 3), 'MemWb-pipeline should only have three output-control signals'

        # Store the keys for the input values
        self.jumpAddress = inputSources[0][1]
        self.mux1 = inputSources[1][1]
        self.readData = inputSources[2][1]
        self.aluRes = inputSources[3][1]
        self.lui = inputSources[4][1]
        self.mux2 = inputSources[5][1]

        # Store the keys for the output values
        self.out1 = outputValueNames[0]
        self.out2 = outputValueNames[1]
        self.out3 = outputValueNames[2]
        self.out4 = outputValueNames[3]
        self.out5 = outputValueNames[4]
        self.out6 = outputValueNames[5]

        # Store the keys for the control signals
        self.memtoReg = control[0][1]
        self.luisig = control[1][1]
        self.jump = control[2][1]

        # Store the keys for the output signals
        self.sig1 = outputSignalNames[0]
        self.sig2 = outputSignalNames[1]
        self.sig3 = outputSignalNames[2]

    # Send output
    def writeOutput(self):
        self.outputValues[self.out1] = self.inputValues[self.jumpAddress]
        self.outputValues[self.out2] = self.inputValues[self.mux1]
        self.outputValues[self.out3] = self.inputValues[self.readData]
        self.outputValues[self.out4] = self.inputValues[self.aluRes]
        self.outputValues[self.out5] = self.inputValues[self.lui]
        self.outputValues[self.out6] = self.inputValues[self.mux2]

    # Send out control signals
    def setControlSignals(self):
        self.outputControlSignals[self.sig1] = self.controlSignals[self.memtoReg]
        self.outputControlSignals[self.sig2] = self.controlSignals[self.luisig]
        self.outputControlSignals[self.sig3] = self.controlSignals[self.jump]


# Test class for pipeline
class TestPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = Pipeline_MemWb()
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
        [],
        ['in1', 'in2', 'in3', 'in4', 'in5', 'in6'],
        [],
        ['memtoreg', 'lui', 'jump']
        )

        self.pipeline.connect(
        [(self.testInput, 'in1'), (self.testInput, 'in2'), (self.testInput, 'in3'),
         (self.testInput, 'in4'), (self.testInput, 'in5'), (self.testInput, 'in6'), ],
        ['out1', 'out2', 'out3', 'out4', 'out5', 'out6'],
        [(self.testInput, 'memtoreg'), (self.testInput, 'lui'), (self.testInput, 'jump')],
        ['sig1', 'sig2', 'sig3']
        )

        self.testOutput.connect(
        [(self.pipeline, 'out1'), (self.pipeline, 'out2'), (self.pipeline, 'out3'), (self.pipeline, 'out4'),
         (self.pipeline, 'out5'), (self.pipeline, 'out6')],
        [],
        [(self.pipeline, 'sig1'), (self.pipeline, 'sig2'), (self.pipeline, 'sig3')],
        []
        )

    def test_correct_behavior(self):
        # Set input values
        self.testInput.setOutputValue('in1', 0)
        self.testInput.setOutputValue('in2', 1)
        self.testInput.setOutputValue('in3', 2)
        self.testInput.setOutputValue('in4', 3)
        self.testInput.setOutputValue('in5', 4)
        self.testInput.setOutputValue('in6', 5)

        # Set control signals
        self.testInput.setOutputControl('memtoreg', 1)
        self.testInput.setOutputControl('lui', 2)
        self.testInput.setOutputControl('jump', 3)

        self.pipeline.readInput()
        self.pipeline.readControlSignals()
        self.pipeline.writeOutput()
        self.pipeline.setControlSignals()
        self.testOutput.readInput()
        self.testOutput.readControlSignals()

        # Store output and output control signals in variables
        out1 = self.testOutput.inputValues['out1']
        out2 = self.testOutput.inputValues['out2']
        out3 = self.testOutput.inputValues['out3']
        out4 = self.testOutput.inputValues['out4']
        out5 = self.testOutput.inputValues['out5']
        out6 = self.testOutput.inputValues['out6']
        sig1 = self.testOutput.controlSignals['sig1']
        sig2 = self.testOutput.controlSignals['sig2']
        sig3 = self.testOutput.controlSignals['sig3']

        # Check if output is as expected
        self.assertEqual(out1, 0)
        self.assertEqual(out2, 1)
        self.assertEqual(out3, 2)
        self.assertEqual(out4, 3)
        self.assertEqual(out5, 4)
        self.assertEqual(out6, 5)

        # Check if control signals are as expected
        self.assertEqual(sig1, 1)
        self.assertEqual(sig2, 2)
        self.assertEqual(sig3, 3)


if __name__ == '__main__':
    unittest.main()
