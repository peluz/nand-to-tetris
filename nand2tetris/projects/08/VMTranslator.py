#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 11:21:08 2018

@author: pedro
"""
import sys
import os
import glob


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
            if self.command == 'RETURN':
                return self.command
            else:
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
    def __init__(self, filePath, isdir):
        self.f = open(filePath, 'w')
        self.labelNum = 0
        self.staticName = filePath.rstrip('.asm').split('/')[-1]
        self.isdir = isdir
        if self.isdir:
            self.writeBootstrap()

    def writeArithmetic(self, command):
        '''
        Writes to output file assembly code that implements given arithmetic
        command
        '''
        self.f.write("// {}\n".format(command))
        
        if command == 'ADD':
            self.f.write("@SP\nM=M-1\nA=M\nD=M\n@SP\nA=M-1\nM=D+M\n")
        elif command == 'SUB':
            self.f.write("@SP\nM=M-1\nA=M\nD=M\n@SP\nA=M-1\nM=M-D\n")
        elif command == 'NEG':
            self.f.write("@SP\nA=M-1\nM=-M\n")
        elif command == 'EQ':
            self.f.write("@SP\nM=M-1\nA=M\nD=M\n@SP\nA=M-1\nD=M-D\n@TRUE{}\nD;JEQ\n".format(self.labelNum) +
                         "@SP\nA=M-1\nM=0\n@END{}\n0;JMP\n(TRUE{})\n@SP\nA=M-1\nM=-1\n(END{})\n".format(self.labelNum, self.labelNum, self.labelNum))
            self.labelNum += 1
        elif command  == 'GT':
            self.f.write("@SP\nM=M-1\nA=M\nD=M\n@SP\nA=M-1\nD=M-D\n@TRUE{}\nD;JGT\n".format(self.labelNum) +
                         "@SP\nA=M-1\nM=0\n@END{}\n0;JMP\n(TRUE{})\n@SP\nA=M-1\nM=-1\n(END{})\n".format(self.labelNum, self.labelNum, self.labelNum))
            self.labelNum += 1
        elif command == 'LT':
            self.f.write("@SP\nM=M-1\nA=M\nD=M\n@SP\nA=M-1\nD=M-D\n@TRUE{}\nD;JLT\n".format(self.labelNum) +
                         "@SP\nA=M-1\nM=0\n@END{}\n0;JMP\n(TRUE{})\n@SP\nA=M-1\nM=-1\n(END{})\n".format(self.labelNum, self.labelNum, self.labelNum))
            self.labelNum += 1
        elif command == 'AND':
            self.f.write("@SP\nM=M-1\nA=M\nD=M\n@SP\nA=M-1\nM=D&M\n")
        elif command == 'OR':
            self.f.write("@SP\nM=M-1\nA=M\nD=M\n@SP\nA=M-1\nM=D|M\n")
        elif command == 'NOT':
            self.f.write("@SP\nA=M-1\nM=!M\n")
            
    
    def writePushPop(self, command, segment, index):
        '''
        Writes to output file assembly code that implements given push or pop
        command
        '''
        self.f.write("// {}\n".format((' ').join([command, segment, index])))
        
        if segment == 'CONSTANT':
            self.f.write("@{}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
                         .format(index))
            return
        
        if command == 'PUSH':
            if segment in ['LOCAL', 'ARGUMENT', 'THIS', 'THAT']:
                if segment == 'LOCAL':
                    segment = 'LCL'
                elif segment == 'ARGUMENT':
                    segment = 'ARG'
                self.f.write("@{}\nD=A\n@{}\nD=D+M\nA=D\nD=M\n".format(index, segment) +
                             "@SP\nA=M\nM=D\n@SP\nM=M+1\n")
            elif segment == 'STATIC':
                self.f.write('@{}.{}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'.format(self.staticName, index))
            elif segment == 'TEMP':
                self.f.write("@{}\nD=A\n@5\nD=D+A\nA=D\nD=M\n".format(index) +
                             "@SP\nA=M\nM=D\n@SP\nM=M+1\n")
            elif segment == 'POINTER':
                assert index in ['0', '1']
                if index == '0':
                    index = 'THIS'
                else:
                    index = 'THAT'
                self.f.write("@{}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n".format(index))
                
        if command == 'POP':
            if segment in ['LOCAL', 'ARGUMENT', 'THIS', 'THAT']:
                if segment == 'LOCAL':
                    segment = 'LCL'
                elif segment == 'ARGUMENT':
                    segment = 'ARG'
                self.f.write("@{}\nD=A\n@{}\nD=D+M\n@R13\nM=D\n@SP\nM=M-1\n".format(index, segment) +
                             "A=M\nD=M\n@R13\nA=M\nM=D\n")
            elif segment == 'STATIC':
                self.f.write("@SP\nM=M-1\nA=M\nD=M\n@{}.{}\nM=D\n".format(self.staticName, index))
            elif segment == 'TEMP':
                self.f.write("@{}\nD=A\n@5\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\n".format(index) +
                             "A=M\nD=M\n@R13\nA=M\nM=D\n")
            elif segment == 'POINTER':
                assert index in ['0', '1']
                if index == '0':
                    index = 'THIS'
                else:
                    index = 'THAT'
                self.f.write("@SP\nM=M-1\nA=M\nD=M\n@{}\nM=D\n".format(index))
    
    def writeCall(self, functionName, numArgs):
        '''
        Write Assembly code that effects the call command
        '''
        self.f.write("// {}\n".format((' ').join(['CALL',
                     functionName, numArgs])))
    
    def writeBootstrap(self):
        self.f.write('@256\nD=A\n@SP\nM=D\n')
        self.writeCall('Sys.init', '0')
                
    def close(self):
        self.f.close()

class VMTranslator(object):
    def __init__(self, VMFilePath):
        self.parsers = []
        self.isdir = False
        if os.path.isdir(VMFilePath):
            self.isdir = True
            os.chdir(VMFilePath)
            for f in glob.glob('./*.vm'):
                self.parsers.append(Parser(f))
            pwd = os.getcwd()
            self.assemblyFilePath = os.path.basename(pwd) + '.asm'
        else:
            self.parsers.append(Parser(VMFilePath)) 
            self.assemblyFilePath = VMFilePath.rstrip('vm') + 'asm'
        self.codeWriter = CodeWriter(self.assemblyFilePath, self.isdir)

    def translate(self):
        '''
        Translate from VM code to assembly code
        '''
        for parser in self.parsers:
            while parser.advance():
                if parser.commandType() == 'ARITHMETIC':
                    self.codeWriter.writeArithmetic(parser.arg1())
                elif parser.commandType() in ['PUSH', 'POP']:
                    self.codeWriter.writePushPop(parser.command[0].upper(),
                                                 parser.arg1(),
                                                 parser.arg2())
            parser.close()
        self.codeWriter.close()



#VMFilePath = sys.argv[1]
#vm = VMTranslator(VMFilePath)
#vm.translate()
