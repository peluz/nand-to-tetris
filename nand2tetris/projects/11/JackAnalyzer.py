# -*- coding: utf-8 -*-
import os
import glob
import sys


class SymbolTable(object):
    def __init__(self):
        self.classTable = {}
        self.subRoutineTable = {}
        self.index = {'static': 0, 'field': 0, 'argument':0, 'var': 0}
        
    def startSubroutine(self):
        '''
        Start a new subroutine scope
        '''
        self.index['argument'] = 0
        self.index['var'] = 0
        self.subRoutineTable = {}
        
    def define(self, name, symbolType, kind):
        '''
        defines new identifier and assignt to it
        a index
        '''
        if kind in ['static', 'field']:
            self.classTable[name] = [symbolType, kind, self.index[kind]]
            self.index[kind] += 1
        else:
            self.subRoutineTable[name] = [symbolType, kind, self.index[kind]]
            self.index[kind] += 1
            
    def varCount(self, kind):
        '''
        returns number of variables of given kind
        already defined in current scope
        '''
        return self.index[kind]
    
    def kindOf(self, name):
        '''
        return kind of named identifier in
        current scope
        '''
        if name in self.subRoutineTable:
            return self.subRoutineTable[name][1]
        elif name in self.classTable:
            return self.classTable[name][1]
        else:
            return None
        
    def typeOf(self, name):
        '''
        return type of named identifier in
        current scope
        '''
        if name in self.subRoutineTable:
            return self.subRoutineTable[name][0]
        elif name in self.classTable:
            return self.classTable[name][0]
        else:
            return None
        
    def indexOf(self, name):
        '''
        return index assigned to identifier in
        current scope
        '''
        if name in self.subRoutineTable:
            return self.subRoutineTable[name][2]
        elif name in self.classTable:
            return self.classTable[name][2]
        else:
            return None
        


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
            if tokenType == 'stringConstant':
                token = token.strip('"')                       
            out.write("<{}> {} </{}>\n".format(tokenType, token.strip('"'), tokenType))
        out.write("</tokens>")
        out.close()
     
        
class CompilationEngine(object):
    def __init__(self, tokenizer, outputFile):
        self.tokenizer = tokenizer
        self.output = outputFile
        self.currentToken = ""
        self.currentTokenType = ""
        self.stoppers = [']', ')', ';']
        self.ops = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
        self.statements = ['let', 'while', 'do', 'return', 'if']
        self.unaryOps = ['-', '~']
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
        if self.currentTokenType == 'stringConstant':
            self.currentToken = self.currentToken.strip('"')
        elif self.currentToken in ['<', '>', '&']:
            if self.currentToken == '<':
                self.currentToken = '&lt;'
            elif self.currentToken == '>':
                self.currentToken = '&gt;'
            elif self.currentToken == '&':
                self.currentToken = '&amp;'
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
        self.updateToken()
        while self.currentToken in ['static', 'field', 'constructor', 'function', 'method']:
            self.tokenToFunction[self.currentToken]()
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
        self.updateToken()
    
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
        assert self.currentToken == '}'
        self.printLine()
        self.output.write("</subroutineBody>\n")
        self.output.write("</subroutineDec>\n")
        self.updateToken()
    
    def compileParameterList(self):
        self.output.write("<parameterList>\n")
        while self.currentToken != ')':
            self.printLine()
            self.updateToken()
        self.output.write("</parameterList>\n")
    
    def compileVarDec(self):
        assert self.currentToken == 'var'
        self.output.write("<varDec>\n")
        while self.currentToken != ';':
            self.printLine()
            self.updateToken()
        assert self.currentToken == ';'
        self.printLine()
        self.output.write("</varDec>\n")
        self.updateToken()
    
    def compileStatements(self):
        self.output.write("<statements>\n")
        while self.currentToken in self.statements:
            self.tokenToFunction[self.currentToken]()
        self.output.write("</statements>\n")
    
    def compileDo(self):
        assert self.currentToken == 'do'
        self.output.write("<doStatement>\n")
        self.printLine()
        self.updateToken()
        self.printLine()
        self.updateToken()
        if self.currentToken == '.':
            self.printLine()
            self.updateToken()
            self.printLine()
            self.updateToken()
        assert self.currentToken == '('
        self.printLine()
        self.updateToken()
        self.compileExpressionList()
        assert self.currentToken == ')'
        self.printLine()
        self.updateToken()
        assert self.currentToken == ';'
        self.printLine()
        self.output.write("</doStatement>\n")
        self.updateToken()
        
    
    def compileLet(self):
        assert self.currentToken == 'let'
        self.output.write("<letStatement>\n")
        self.printLine()
        self.updateToken()
        self.printLine()
        self.updateToken()
        if self.currentToken == '[':
            self.printLine()
            self.updateToken()
            self.compileExpression()
            assert self.currentToken == ']'
            self.printLine()
            self.updateToken()
        assert self.currentToken == '='
        self.printLine()
        self.updateToken()
        self.compileExpression()
        assert self.currentToken == ';'
        self.printLine()
        self.output.write("</letStatement>\n")
        self.updateToken()
        
    
    def compileWhile(self):
        assert self.currentToken == 'while'
        self.output.write("<whileStatement>\n")
        self.printLine()
        self.updateToken()
        assert self.currentToken == '('
        self.printLine()
        self.updateToken()
        self.compileExpression()
        assert self.currentToken == ')'
        self.printLine()
        self.updateToken()
        assert self.currentToken == '{'
        self.printLine()
        self.updateToken()
        self.compileStatements()
        assert self.currentToken == '}'
        self.printLine()
        self.output.write("</whileStatement>\n")
        self.updateToken()
    
    def compileIf(self):
        assert self.currentToken == 'if'
        self.output.write("<ifStatement>\n")
        self.printLine()
        self.updateToken()
        assert self.currentToken == '('
        self.printLine()
        self.updateToken()
        self.compileExpression()
        assert self.currentToken == ')'
        self.printLine()
        self.updateToken()
        assert self.currentToken == '{'
        self.printLine()
        self.updateToken()
        self.compileStatements()
        assert self.currentToken == '}'
        self.printLine()
        self.updateToken()
        if self.currentToken == 'else':
            self.printLine()
            self.updateToken()
            assert self.currentToken == '{'
            self.printLine()
            self.updateToken()
            self.compileStatements()
            assert self.currentToken == '}'
            self.printLine()
            self.updateToken()
        self.output.write("</ifStatement>\n")
            
    
    def compileReturn(self):
        assert self.currentToken == 'return'
        self.output.write("<returnStatement>\n")
        self.printLine()
        self.updateToken()
        if self.currentToken != ';':
            self.compileExpression()
        assert self.currentToken == ';'
        self.printLine()
        self.updateToken()
        self.output.write("</returnStatement>\n")
    
    def compileExpression(self):
        self.output.write("<expression>\n")
        self.compileTerm()
        while self.currentToken in self.ops:
            self.printLine()
            self.updateToken()
            self.compileTerm()
        self.output.write("</expression>\n")
    
    def compileTerm(self):
        self.output.write("<term>\n")
        if self.currentToken == '(':
            self.printLine()
            self.updateToken()
            self.compileExpression()
            assert self.currentToken == ')'
            self.printLine()
            self.updateToken()
        elif self.currentToken in self.unaryOps:
            self.printLine()
            self.updateToken()
            self.compileTerm()
        else:
            self.printLine()
            self.updateToken()
            if self.currentToken == '[':
                self.printLine()
                self.updateToken()
                self.compileExpression()
                assert self.currentToken == ']'
                self.printLine()
                self.updateToken()
            elif self.currentToken in ['.', '(']:
                if self.currentToken == '.':
                    self.printLine()
                    self.updateToken()
                    self.printLine()
                    self.updateToken()
                assert self.currentToken == '('
                self.printLine()
                self.updateToken()
                self.compileExpressionList()
                assert self.currentToken == ')'
                self.printLine()
                self.updateToken()
        self.output.write("</term>\n")
    
    def compileExpressionList(self):
        self.output.write("<expressionList>\n")
        if self.currentToken not in self.stoppers:
            self.compileExpression()
            while self.currentToken == ',':
                self.printLine()
                self.updateToken()
                self.compileExpression()
        self.output.write("</expressionList>\n")
        
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