# -*- coding: utf-8 -*-
import os
import glob
import sys


class JackTokenizer(object):
    def __init__(self, inputFile):
        self.input = inputFile
        self.tokens = []
        self.symbols = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+',
                         '-', '*', '/', '&', '|', '<', '>', '=', '~', '"']
        self.keywords = ['class', 'constructor', 'function', 'method',
                         'field', 'static', 'var', 'int', 'char', 'boolean',
                         'void', 'true', 'false', 'null', 'this', 'let', 'do',
                         'if', 'else', 'while', 'return']
        self.tokenize()
        
    def tokenize(self):
        current_line = self.input.readline()
        comment= False
        while current_line != '':
            tokens = current_line.strip('\r\t\n').split('//', 1)[0].rstrip(
                    ' ').split(' ')
            for token in tokens:
                if token == '':
                    continue
                if token == '/**' or token == '/*':
                    comment = True
                if token == '*/':
                    comment = False
                    continue
                if not comment:
                    self.tokens.append(token)
            current_line = self.input.readline()
            
    def hasMoreTokens(self):
        return self.tokens
    
    def advance(self):
        if self.hasMoreTokens():
            word = self.tokens.pop(0)
            token = ''
            flag = False
            if word in self.symbols:
                if word == '"':
                    token += '"'
                    while '"' not in self.tokens[0]:
                        token += self.tokens.pop(0) + " "
                    word = self.tokens.pop(0)
                    token += word.split('"')[0] + '"'
                    self.tokens.insert(0, word.split('"')[1])
                    return token
                else:
                    return word
            split = []
            for c in word:
                if c in self.symbols:                    
                    if len(token) > 0:
                        split.append(token)
                    split.append(c)
                    token = ""
                    flag = True
                    continue
                token += c
            if flag:
                if len(token) > 0:
                    split.append(token)
                for index, word in enumerate(split):
                    self.tokens.insert(index, word)
                return self.advance()
                
            else:
                return token
            
    def tokenType(self, string):
        if string in self.keywords:
            return 'keyword'
        elif string in self.symbols:
            return 'symbol'
        elif string[0] == '"':
            return 'stringConstant'
        elif string.isdigit():
            return 'integerConstant'
        else:
            return 'identifier'
        
    def printTokens(self):
        out = open("output.xml", "w")
        out.write("<tokens>\n")
        while self.hasMoreTokens():
            token = self.advance()
            tokenType = self.tokenType(token)
            if token in ['<', '>', '&']:
                if token == '<':
                    token = '&lt;'
                elif token == '>':
                    token = '&gt;'
                elif token == '&':
                    token = '&amp;'                        
            out.write("<{}> {} </{}>\n".format(tokenType, token.strip('"'), tokenType))
        out.write("</tokens>")
        out.close()
     
        
class CompilationEngine(object):
    def __init__(self, tokenizer, outputFile):
        self.tokenizer = tokenizer
        self.output = outputFile
        self.currentToken = ""
        self.currentTokenType = ""
        self.tokenToFunction = {'class': self.compileClass,
                               'static': self.compileClassVarDec,
                               'field': self.compileClassVarDec,
                               'constructor': self.compileSubRoutine,
                               'function': self.compileSubRoutine,
                               'method': self.compileSubRoutine,
                               'var': self.compileVarDec,
                               'let': self.compileLet,
                               'if': self.compileIf,
                               'while': self.compileWhile,
                               'do': self.compileDo,
                               'return': self.compileReturn
                               }
        
    def updateToken(self):
        self.currentToken = self.tokenizer.advance()
        self.currentTokenType = self.tokenizer.tokenType(self.currentToken)
    
    def printLine(self):
        self.output.write("<{}> {} </{}>\n".format(self.currentTokenType,
                          self.currentToken, self.currentTokenType))
    
    def compileJack(self):
        self.updateToken()
        assert self.currentToken == 'class'
        self.compileClass()
        
    def compileClass(self):
        self.output.write("<class>\n<keyword> class </keyword>\n")
        self.updateToken()
        self.printLine()
        self.updateToken()
        assert self.currentToken == '{'
        self.printLine()
        self.currentToken = 'static'
        while self.currentToken in ['static', 'field', 'constructor', 'function', 'method']:
            self.updateToken()
            self.tokenToFunction[self.currentToken]()
            self.updateToken()
        assert self.currentToken == '}'
        self.printLine()
        self.output.write("</class>\n")
    
    def compileClassVarDec(self):
        assert self.currentToken in ['static', 'field']
        self.output.write("<classVarDec>\n")
        self.printLine()
        self.updateToken()
        self.printLine() 
        self.updateToken()
        self.printLine()
        self.updateToken()
        while self.currentToken == ',':
            self.printLine()
            self.updateToken()
            self.printLine()
            self.updateToken()
        assert self.currentToken == ';'
        self.printLine()
        self.output.write("</classVarDec>\n")
    
    def compileSubRoutine(self):
        assert self.currentToken in ['constructor', 'method', 'function']
        self.output.write("<subroutineDec>\n")
        self.printLine()
        self.updateToken()
        self.printLine()
        self.updateToken()
        self.printLine()
        self.updateToken()
        assert self.currentToken == '('
        self.printLine()
        self.updateToken()
        self.compileParameterList()
        self.updateToken()
        assert self.currentToken == ')'
        self.printLine()
        self.output.write("<subroutineBody>\n")
        self.updateToken()
        assert self.currentToken == '{'
        self.printLine()
        self.updateToken()
        while self.currentToken != '}':
            if self.currentToken == 'var':
                self.compileVarDec()
            else:
                self.compileStatements()
            self.updateToken()
        assert self.currentToken == '}'
        self.printLine()
        self.output.write("</subroutineBody>\n")
        self.output.write("</subroutineDec>\n")
    
    def compileParameterList(self):
        pass
    
    def compileVarDec(self):
        pass
    
    def compileStatements(self):
        pass
    
    def compileDo(self):
        pass
    
    def compileLet(self):
        pass
    
    def compileWhile(self):
        pass
    
    def compileIf(self):
        pass
    
    def compileReturn(self):
        pass
    
    def compileExpression(self):
        pass
    
    def compileTerm(self):
        pass
    
    def compileExpressionList(self):
        pass
        
class JackAnalyzer(object):
    def __init__(self, sourcePath):
        self.files = []
        if os.path.isdir(sourcePath):
            os.chdir(sourcePath)
            for f in glob.glob('./*.jack'):
                self.files.append(f)
        else:
            self.files.append(sourcePath) 

    def translate(self):
        '''
        Translate from Jack code  to xml
        '''
        for f in self.files:
            inputFile = open(f, 'r')
            tokenizer = JackTokenizer(inputFile)
            outputFile = f.rstrip('.jack') + '.xml'
            output = open(outputFile, 'w')
            engine = CompilationEngine(tokenizer, output)
            engine.compileJack()
            inputFile.close()
            output.close()


sourcePath = sys.argv[1]
jack = JackAnalyzer(sourcePath)
jack.translate()        