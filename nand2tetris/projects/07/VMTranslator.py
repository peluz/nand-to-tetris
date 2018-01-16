#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 11:21:08 2018

@author: pedro
"""
import sys


class Parser(object):
    def __init__(self, filePath):
        self.f = open(filePath, 'r')
        self.currentLine = None
        self.command = None

    def hasMoreCommands(self):
        self.currentLine = self.f.readline()
        return self.currentLine != ''

    def advance(self):
        if self.hasMoreCommands():
            self.command = self.currentLine.strip(
                ' \r\t\n').split('//', 1)[0].split(' ')
            if self.command[0] == '':
                self.advance()
            return True
        else:
            return False

    def commandType(self):
        if len(self.command) == 1:
            return 'ARITHMETIC'
        else:
            return self.command[0].upper()

    def arg1(self):
        '''
        Returns the first argument of the current command. If ARITHMETIC, the
        command itself is returned. Should not be called if current command is
        RETURN
        '''
        assert self.commandType() != 'RETURN'
        
        if self.commandType() == 'ARITHMETIC':
            return self.command[0].upper()
        else:
            return self.command[1].upper()
    
    def arg2(self):
        '''
        Returns the second argument of the current command. Should only be
        called if command is of type PUSH, POP, FUNCTION or CALL
        '''
        validCommands = ['PUSH', 'POP', 'FUNCTION', 'CALL']
        assert self.commandType() in validCommands
        return self.command[2]
        

    def close(self):
        self.f.close()


class CodeWriter(object):
    def __init__(self, filePath):
        self.f = open(filePath, 'w')
        self.arithmeticCommand

    def writeArithmetic(self, command):
        '''
        Writes to output file assembly code that implements given arithmetic
        command
        '''
        self.f.write('//' + command)
    
    def writePushPop(self, command, segment, index):
        '''
        Writes to output file assembly code that implements given push or pop
        command
        '''
        
    def close(self):
        self.f.close()

class VMTranslator(object):
    def __init__(self, VMFilePath):
        self.parser = Parser(VMFilePath)
        self.assemblyFilePath = VMFilePath.rstrip('vm') + 'asm'
        self.codeWriter = CodeWriter(self.assemblyFilePath)

    def translate(self):
        '''
        Translate from VM code to assembly code
        '''
        while self.parser.advance():
            if self.parser.commandType() == 'ARITHMETIC':
                self.codeWriter.writeArithmetic(self.parser.arg1())
            elif self.parser.commandType() == 'PUSH' or 'POP':
                self.codeWriter.writePushPop(self.parser.command[0],
                                             self.parser.arg1(),
                                             self.parser.arg2())
        self.parser.close()
        self.codeWriter.close()


#
#VMFilePath = sys.argv[1]
#vm = VMTranslator(VMFilePath)
#vm.translate()
