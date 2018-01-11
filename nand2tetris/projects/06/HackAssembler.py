#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 11:21:08 2018

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
            self.command = self.currentLine.strip(' \r\t\n').replace(' ','').split('//', 1)[0]
            if self.command == '':
                self.advance()
            return True
        else:
            return False
                        
    def commandType(self):
        if self.command[0] == '@':
            return 'A_COMMAND'
        elif self.command[0] == '(':
            return 'L_COMMAND'
        else:
            return 'C_COMMAND'
        
    def symbol(self):
        return self.command.strip('@()')
    
    def dest(self):
        if '=' in self.command:
            return self.command.split('=', 1)[0]
        else:
            return None
    
    def comp(self):
        if '=' in self.command:
            return self.command.split('=', 1)[1].split(';', 1)[0]
        else:
            return self.command.split(';', 1)[0]
    
    def jump(self):
        if ';' in self.command:
            return self.command.split(';', 1)[1]
        else:
            return None
        
    def restart(self):
        self.f.seek(0)
    
    def close(self):
        self.f.close()
        

class Coder(object):
    def __init__(self):
        self.destCodes = {
            None: '000',
            'M': '001',
            'D': '010',
            'MD': '011',
            'A': '100',
            'AM': '101',
            'AD': '110',
            'AMD': '111'
        }
        self.jumpCodes = {
            None: '000',
            'JGT': '001',
            'JEQ': '010',
            'JGE': '011',
            'JLT': '100',
            'JNE': '101',
            'JLE': '110',
            'JMP': '111'
        }
        self.compCodes = {
            '0':  '0101010',
            '1':  '0111111',
            '-1': '0111010',
            'D':  '0001100',
            'A':  '0110000',
            '!D': '0001101',
            '!A': '0110001',
            '-D': '0001111',
            '-A': '0110011',
            'D+1':'0011111',
            'A+1':'0110111',
            'D-1':'0001110',
            'A-1':'0110010',
            'D+A':'0000010',
            'D-A':'0010011',
            'A-D':'0000111',
            'D&A':'0000000',
            'D|A':'0010101',
            'M':  '1110000',
            '!M': '1110001',
            '-M': '1110011',
            'M+1':'1110111',
            'M-1':'1110010',
            'D+M':'1000010',
            'D-M':'1010011',
            'M-D':'1000111',
            'D&M':'1000000',
            'D|M':'1010101'
        }
        
    def dest(self, mnemonic):
        return self.destCodes[mnemonic]
    
    def comp(self, mnemonic):
        return self.compCodes[mnemonic]
    
    def jump(self, mnemonic):
        return self.jumpCodes[mnemonic]


class SymbolTable(object):
    def __init__(self):
        self.symbolTable = {
            'SP': 0,
            'LCL': 1,
            'ARG': 2,
            'THIS': 3,
            'THAT': 4,
            'R0' : 0,
            'R1' : 1,
            'R2' : 2,
            'R3' : 3,
            'R4' : 4,
            'R5' : 5,
            'R6' : 6,
            'R7' : 7,
            'R8' : 8,
            'R9' : 9,
            'R10' : 10,
            'R11' : 11,
            'R12' : 12,
            'R13' : 13,
            'R14' : 14,
            'R15' : 15,
            'SCREEN': 16384,
            'KBD': 24576
        }
        
    def addEntry(self, symbol, address):
        self.symbolTable[symbol] = address
        
    def contains(self, symbol):
        return symbol in self.symbolTable
    
    def getAddress(self, symbol):
        return self.symbolTable[symbol]


class HackAssembler(object):
    def __init__(self, assembleFilePath):
        self.parser = Parser(assembleFilePath)
        self.coder = Coder()
        self.symbolTable = SymbolTable()
        self.hackFilePath = assembleFilePath.rstrip('asm') + 'hack'
        self.f = open(self.hackFilePath, 'w')
        self.symbolAddress = 16
        self.pseudoCommandAddress = 0
        
    def buildPseudoCommandTable(self):
        while self.parser.advance():
            if self.parser.commandType() != 'L_COMMAND':
                self.pseudoCommandAddress += 1
            else:
                symbol = self.parser.symbol()
                self.symbolTable.addEntry(symbol, self.pseudoCommandAddress)                
        self.parser.restart()
    
    def translate(self):
        while self.parser.advance():
            if self.parser.commandType() == 'A_COMMAND':
                self.printACommand()
            elif self.parser.commandType() == 'C_COMMAND':
                self.printCCommand()
        self.close()
    
    def printACommand(self):
        symbol = self.parser.symbol()
        if symbol[0].isdigit():
            code = symbol
        elif self.symbolTable.contains(symbol):
            code = self.symbolTable.getAddress(symbol)
        else:
            self.symbolTable.addEntry(symbol, self.symbolAddress)
            code = self.symbolAddress
            self.symbolAddress += 1
        code = "{0:b}".format(int(code)).zfill(16)
        self.f.write(str(code) + '\n')
        
    def printCCommand(self):
        code = '111'
        code += self.coder.comp(self.parser.comp())
        code += self.coder.dest(self.parser.dest())
        code += self.coder.jump(self.parser.jump())
        self.f.write(code + '\n')
        
    def assemble(self):
        self.buildPseudoCommandTable()
        self.translate()
    
    def close(self):
        self.f.close()
        
#assembleFilePath = sys.argv[1]
#hack = HackAssembler(assembleFilePath)
#hack.assemble()