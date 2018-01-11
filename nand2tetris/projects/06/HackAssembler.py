#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 11:21:08 2018

@author: pedro
"""

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
            'D':, '
            'A':,
            '!D':,
            '!A':,
            '-D':,
            '-A':,
            'D+1':,
            'A+1':,
            'D-1':,
            'A-1':,
            'D+A':,
            'D-A':,
            'A-D':,
            'D&A':,
            'D|A':,
            'M':,
            '!M':,
            '-M':,
            'M+1':,
            'M-1':,
            'D+M':,
            'D-M':.
            'M-D':,
            'D&M':,
            'D|M':
        }
    
    