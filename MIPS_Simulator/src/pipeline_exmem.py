import unittest
from cpuElement import CPUElement
from testElement import TestElement


class Pipeline_ExMem(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        '''
        Connect pipeline to input sources and controller
        '''
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        # Check if amount of input and output are correct
        assert(len(inputSources) == 6), 'ExMem-pipeline should only have six inputs'
        assert(len(outputValueNames) == 6), 'ExMem-pipeline should only have six outputs'
        assert(len(control) == 9), 'ExMem-pipeline should only have nine control signals'
        assert(len(outputSignalNames) == 9), 'ExMem-pipeline should only have nine output-control signals'

        # Store the keys for the input values
        self.newAddress = inputSources[0][1]
        self.jumpAddress = inputSources[1][1]
        self.aluOut = inputSources[2][1]
        self.readData2 = inputSources[3][1]
        self.lui = inputSources[4][1]
        self.mux = inputSources[5][1]

        # Store the keys for the output values
        self.out1 = outputValueNames[0]
        self.out2 = outputValueNames[1]
        self.out3 = outputValueNames[2]
        self.out4 = outputValueNames[3]
        self.out5 = outputValueNames[4]
        self.out6 = outputValueNames[5]

        # Store the keys for the control signals
        self.memtoReg = control[0][1]
        self.regWrite = control[1][1]
        self.memRead = control[2][1]
        self.memWrite = control[3][1]
        self.branch = control[4][1]
        self.jump = control[5][1]
        self.lui = control[6][1]
        self.bne = control[7][1]
        self.zero = control[8][1]


        # Store the keys for the output signals
        self.sig1 = outputSignalNames[0]
        self.sig2 = outputSignalNames[1]
        self.sig3 = outputSignalNames[2]
        self.sig4 = outputSignalNames[3]
        self.sig5 = outputSignalNames[4]
        self.sig6 = outputSignalNames[5]
        self.sig7 = outputSignalNames[6]
        self.sig8 = outputSignalNames[7]
        self.sig9 = outputSignalNames[8]



    # Send output
    def writeOutput(self):
        self.outputValues[self.out1] = self.inputValues[self.newAddress]
        self.outputValues[self.out2] = self.inputValues[self.jumpAddress]
        self.outputValues[self.out3] = self.inputValues[self.aluOut]
        self.outputValues[self.out4] = self.inputValues[self.readData2]
        self.outputValues[self.out5] = self.inputValues[self.lui]
        self.outputValues[self.out6] = self.inputValues[self.mux]

    # Send out control signals
    def setControlSignals(self):
        self.outputControlSignals[self.sig1] = self.controlSignals[self.memtoReg]
        self.outputControlSignals[self.sig2] = self.controlSignals[self.regWrite]
        self.outputControlSignals[self.sig3] = self.controlSignals[self.memRead]
        self.outputControlSignals[self.sig4] = self.controlSignals[self.memWrite]
        self.outputControlSignals[self.sig5] = self.controlSignals[self.branch]
        self.outputControlSignals[self.sig6] = self.controlSignals[self.jump]
        self.outputControlSignals[self.sig7] = self.controlSignals[self.lui]
        self.outputControlSignals[self.sig8] = self.controlSignals[self.bne]
        self.outputControlSignals[self.sig9] = self.controlSignals[self.zero]



# Test class for pipeline
class TestPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = Pipeline_ExMem()
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
        [],
        ['newaddress', 'jumpaddress', 'aluout', 'readdata2', 'lui', 'mux'],
        [],
        ['memtoreg', 'regwrite', 'memread', 'memwrite', 'branch', 'jump', 'lui', 'bne', 'zero']
        )

        self.pipeline.connect(
        [(self.testInput, 'newaddress'), (self.testInput, 'jumpaddress'), (self.testInput, 'aluout'),
         (self.testInput, 'readdata2'), (self.testInput, 'lui'), (self.testInput, 'mux')],
        ['out1', 'out2', 'out3', 'out4', 'out5', 'out6'],
        [(self.testInput, 'memtoreg'), (self.testInput, 'regwrite'), (self.testInput, 'memread'),
         (self.testInput, 'memwrite'), (self.testInput, 'branch'), (self.testInput, 'jump'),
         (self.testInput, 'lui'), (self.testInput, 'bne'), (self.testInput, 'zero')],
        ['sig1', 'sig2', 'sig3', 'sig4', 'sig5', 'sig6', 'sig7', 'sig8', 'sig9']
        )

        self.testOutput.connect(
        [(self.pipeline, 'out1'), (self.pipeline, 'out2'), (self.pipeline, 'out3'), (self.pipeline, 'out4'),
         (self.pipeline, 'out5'), (self.pipeline, 'out6')],
        [],
        [(self.pipeline, 'sig1'), (self.pipeline, 'sig2'), (self.pipeline, 'sig3'), (self.pipeline, 'sig4'),
         (self.pipeline, 'sig5'), (self.pipeline, 'sig6'), (self.pipeline, 'sig7'), (self.pipeline, 'sig8'),
         (self.pipeline, 'sig9')],
        []
        )

    def test_correct_behavior(self):
        # Set input values
        self.testInput.setOutputValue('newaddress', 0)
        self.testInput.setOutputValue('jumpaddress', 1)
        self.testInput.setOutputValue('aluout', 2)
        self.testInput.setOutputValue('readdata2', 3)
        self.testInput.setOutputValue('lui', 4)
        self.testInput.setOutputValue('mux', 5)

        # Set control signals
        self.testInput.setOutputControl('memtoreg', 0)
        self.testInput.setOutputControl('regwrite', 1)
        self.testInput.setOutputControl('memread', 2)
        self.testInput.setOutputControl('memwrite', 3)
        self.testInput.setOutputControl('branch', 4)
        self.testInput.setOutputControl('jump', 5)
        self.testInput.setOutputControl('lui', 6)
        self.testInput.setOutputControl('bne', 7)
        self.testInput.setOutputControl('zero', 8)

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
        sig4 = self.testOutput.controlSignals['sig4']
        sig5 = self.testOutput.controlSignals['sig5']
        sig6 = self.testOutput.controlSignals['sig6']
        sig7 = self.testOutput.controlSignals['sig7']
        sig8 = self.testOutput.controlSignals['sig8']
        sig9 = self.testOutput.controlSignals['sig9']


        # Check if output is as expected
        self.assertEqual(out1, 0)
        self.assertEqual(out2, 1)
        self.assertEqual(out3, 2)
        self.assertEqual(out4, 3)
        self.assertEqual(out5, 4)
        self.assertEqual(out6, 5)

        # Check if control signals are as expected
        self.assertEqual(sig1, 0)
        self.assertEqual(sig2, 1)
        self.assertEqual(sig3, 2)
        self.assertEqual(sig4, 3)
        self.assertEqual(sig5, 4)
        self.assertEqual(sig6, 5)
        self.assertEqual(sig7, 6)
        self.assertEqual(sig8, 7)
        self.assertEqual(sig9, 8)



if __name__ == '__main__':
    unittest.main()
