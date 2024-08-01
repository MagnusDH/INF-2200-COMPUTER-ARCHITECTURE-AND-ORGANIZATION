import unittest
from cpuElement import CPUElement
from testElement import TestElement


class Pipeline_IdEx(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        '''
        Connect pipeline to input sources and controller
        '''
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        # Check if amount of input and output are correct
        assert(len(inputSources) == 7), 'Idex-pipeline should only have seven inputs'
        assert(len(outputValueNames) == 7), 'Idex-pipeline should only have seven outputs'
        assert(len(control) == 11), 'Idex-pipeline should only have eleven control signals'
        assert(len(outputSignalNames) == 11), 'Idex-pipeline should only have eleven output-control signals'

        # Store the keys for the input values
        self.newAddress = inputSources[0][1]
        self.jumpAddress = inputSources[1][1]
        self.readData1 = inputSources[2][1]
        self.readData2 = inputSources[3][1]
        self.signExtended = inputSources[4][1]
        self.aluControl = inputSources[5][1]
        self.lui = inputSources[6][1]

        # Store the keys for the output values
        self.out1 = outputValueNames[0]
        self.out2 = outputValueNames[1]
        self.out3 = outputValueNames[2]
        self.out4 = outputValueNames[3]
        self.out5 = outputValueNames[4]
        self.out6 = outputValueNames[5]
        self.out7 = outputValueNames[6]

        # Store the keys for the control signals
        self.regDst = control[0][1]
        self.aluSrc = control[1][1]
        self.memtoReg = control[2][1]
        self.regWrite = control[3][1]
        self.memRead = control[4][1]
        self.memWrite = control[5][1]
        self.branch = control[6][1]
        self.aluOp = control[7][1]
        self.jump = control[8][1]
        self.lui = control[9][1]
        self.bne = control[10][1]

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
        self.sig10 = outputSignalNames[9]
        self.sig11 = outputSignalNames[10]


    # Send output
    def writeOutput(self):
        self.outputValues[self.out1] = self.inputValues[self.newAddress]
        self.outputValues[self.out2] = self.inputValues[self.jumpAddress]
        self.outputValues[self.out3] = self.inputValues[self.readData1]
        self.outputValues[self.out4] = self.inputValues[self.readData2]
        self.outputValues[self.out5] = self.inputValues[self.signExtended]
        self.outputValues[self.out6] = self.inputValues[self.aluControl]
        self.outputValues[self.out7] = self.inputValues[self.lui]

    # Send out control signals
    def setControlSignals(self):
        self.outputControlSignals[self.sig1] = self.controlSignals[self.regDst]
        self.outputControlSignals[self.sig2] = self.controlSignals[self.aluSrc]
        self.outputControlSignals[self.sig3] = self.controlSignals[self.memtoReg]
        self.outputControlSignals[self.sig4] = self.controlSignals[self.regWrite]
        self.outputControlSignals[self.sig5] = self.controlSignals[self.memRead]
        self.outputControlSignals[self.sig6] = self.controlSignals[self.memWrite]
        self.outputControlSignals[self.sig7] = self.controlSignals[self.branch]
        self.outputControlSignals[self.sig8] = self.controlSignals[self.aluOp]
        self.outputControlSignals[self.sig9] = self.controlSignals[self.jump]
        self.outputControlSignals[self.sig10] = self.controlSignals[self.lui]
        self.outputControlSignals[self.sig11] = self.controlSignals[self.bne]


# Test class for pipeline
class TestPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = Pipeline_IdEx()
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
        [],
        ['newaddress', 'jumpaddress', 'readdata1', 'readdata2', 'extended', 'alucontrol', 'lui'],
        [],
        ['regdst', 'alusrc', 'memtoreg', 'regwrite', 'memread', 'memwrite', 'branch', 'aluop', 'jump', 'lui', 'bne']
        )

        self.pipeline.connect(
        [(self.testInput, 'newaddress'), (self.testInput, 'jumpaddress'), (self.testInput, 'readdata1'),
         (self.testInput, 'readdata2'), (self.testInput, 'extended'), (self.testInput, 'alucontrol'), (self.testInput, 'lui')],
        ['out1', 'out2', 'out3', 'out4', 'out5', 'out6', 'out7'],
        [(self.testInput, 'regdst'), (self.testInput, 'alusrc'), (self.testInput, 'memtoreg'), (self.testInput, 'regwrite'),
         (self.testInput, 'memread'), (self.testInput, 'memwrite'), (self.testInput, 'branch'),
         (self.testInput, 'aluop'), (self.testInput, 'jump'), (self.testInput, 'lui'), (self.testInput, 'bne')],
        ['sig1', 'sig2', 'sig3', 'sig4', 'sig5', 'sig6', 'sig7', 'sig8', 'sig9', 'sig10', 'sig11']
        )

        self.testOutput.connect(
        [(self.pipeline, 'out1'), (self.pipeline, 'out2'), (self.pipeline, 'out3'), (self.pipeline, 'out4'),
         (self.pipeline, 'out5'), (self.pipeline, 'out6'), (self.pipeline, 'out7')],
        [],
        [(self.pipeline, 'sig1'), (self.pipeline, 'sig2'), (self.pipeline, 'sig3'), (self.pipeline, 'sig4'),
         (self.pipeline, 'sig5'), (self.pipeline, 'sig6'), (self.pipeline, 'sig7'), (self.pipeline, 'sig8'),
         (self.pipeline, 'sig9'), (self.pipeline, 'sig10'), (self.pipeline, 'sig11')],
        []
        )

    def test_correct_behavior(self):
        # Set input values
        self.testInput.setOutputValue('newaddress', 0)
        self.testInput.setOutputValue('jumpaddress', 1)
        self.testInput.setOutputValue('readdata1', 2)
        self.testInput.setOutputValue('readdata2', 3)
        self.testInput.setOutputValue('extended', 4)
        self.testInput.setOutputValue('alucontrol', 5)
        self.testInput.setOutputValue('lui', 6)

        # Set control signals
        self.testInput.setOutputControl('regdst', 0)
        self.testInput.setOutputControl('alusrc', 1)
        self.testInput.setOutputControl('memtoreg', 2)
        self.testInput.setOutputControl('regwrite', 3)
        self.testInput.setOutputControl('memread', 4)
        self.testInput.setOutputControl('memwrite', 5)
        self.testInput.setOutputControl('branch', 6)
        self.testInput.setOutputControl('aluop', 7)
        self.testInput.setOutputControl('jump', 8)
        self.testInput.setOutputControl('lui', 9)
        self.testInput.setOutputControl('bne', 10)

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
        out7 = self.testOutput.inputValues['out7']

        sig1 = self.testOutput.controlSignals['sig1']
        sig2 = self.testOutput.controlSignals['sig2']
        sig3 = self.testOutput.controlSignals['sig3']
        sig4 = self.testOutput.controlSignals['sig4']
        sig5 = self.testOutput.controlSignals['sig5']
        sig6 = self.testOutput.controlSignals['sig6']
        sig7 = self.testOutput.controlSignals['sig7']
        sig8 = self.testOutput.controlSignals['sig8']
        sig9 = self.testOutput.controlSignals['sig9']
        sig10 = self.testOutput.controlSignals['sig10']
        sig11 = self.testOutput.controlSignals['sig11']

        # Check if output is as expected
        self.assertEqual(out1, 0)
        self.assertEqual(out2, 1)
        self.assertEqual(out3, 2)
        self.assertEqual(out4, 3)
        self.assertEqual(out5, 4)
        self.assertEqual(out6, 5)
        self.assertEqual(out7, 6)

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
        self.assertEqual(sig10, 9)
        self.assertEqual(sig11, 10)



if __name__ == '__main__':
    unittest.main()
