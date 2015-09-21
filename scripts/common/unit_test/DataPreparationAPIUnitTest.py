#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of asrt.

# asrt is free software: you can redistribute it and/or modify
# it under the terms of the BSD 3-Clause License as published by
# the Open Source Initiative.

# asrt is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# BSD 3-Clause License for more details.

# You should have received a copy of the BSD 3-Clause License
# along with asrt. If not, see <http://opensource.org/licenses/>.

__author__ = "Alexandre Nanchen"
__version__ = "Revision: 1.0 "
__date__ = "Date: 2015/08"
__copyright__ = "Copyright (c) 2015 Idiap Research Institute"
__license__ = "BSD 3-Clause"

import os
scriptsDir = os.path.abspath(os.path.dirname(__file__))

import unittest, logging

from ioread import Ioread
from DataPreparationAPI import DataPreparationAPI
from config import TEMPDIRUNITTEST

class TestDataPreparationAPI(unittest.TestCase):
    logger  = logging.getLogger("Asrt.TestDataPreparationAPI")

    workingDirectory    = TEMPDIRUNITTEST 
    targetDir           = scriptsDir + "/resources"
    targetFolder1       = targetDir + "/target-folder-2"
    regexFile           = targetDir + "/regexpattern.csv"

    testFileList = [(1, scriptsDir + "/resources/test-strings-datapreparationapi-french.csv"),
                    (2, scriptsDir + "/resources/test-strings-datapreparationapi-german.csv")]

    def setUp(self):
        print ""

    def getTestList(self, strFileName):
        """Get CSV content of 'strFileName'.
        """
        io = Ioread()
        return io.readCSV(strFileName, delim='\t')

    ############
    #Tests
    #
    def testLoadRegexes(self):
        api = DataPreparationAPI(None,None)
        api.setRegexFile(self.regexFile)

        api._getRegexes()

        self.assertTrue(api.substitutionRegexFormula.hasPatterns())
        self.assertTrue(len(api.validationPatternList) > 0)
        self.assertTrue(len(api.substitutionRegexFormula.substitutionPatternList[0]) > 1)
    
    def testPrepareDocument(self):
        api = DataPreparationAPI(None, None)
        api.setLMModeling(True)
        for languageId, strFileName in self.testFileList:
            self.logger.info("Testing %s" % strFileName)
            testList = self.getTestList(strFileName)
            for test, gt, bDiscard in testList:
                if int(bDiscard): 
                    continue
                #Main call
                api.setFormattedText(test)
                api.prepareDocument(languageId)
                formattedText = api.getCleanedText()
                self.assertEquals(formattedText.encode('utf-8'), gt.encode('utf-8'),
                    "'%s' is not '%s':%s" % (formattedText.encode('utf-8'), 
                                    gt.encode('utf-8'), strFileName))
