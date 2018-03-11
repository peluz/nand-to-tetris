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
    def __init__(self, tokenizer, symbolTable, vmWriter):
        self.tokenizer = tokenizer
        self.symbolTable = symbolTable
        self.writer = vmWriter
        self.currentToken = ""
        self.currentTokenType = ""
        self.stoppers = [']', ')', ';']
        self.ops = {'+': 'add', '-': 'sub', '*': 'multiply', '/': 'divide',
                    '&': 'and', '|': 'or', '<': 'lt', '>': 'gt', '=': 'eq'}
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
        self.currentClass = None
        self.nArgs = 0
        self.expression = []
        
    def updateToken(self):
        self.currentToken = self.tokenizer.advance()
        self.currentTokenType = self.tokenizer.tokenType(self.currentToken)
    
    def compileJack(self):
        self.updateToken()
        assert self.currentToken == 'class'
        self.compileClass()
        self.writer.close()
        
    def compileClass(self):
        self.updateToken()
        self.currentClass = self.currentToken
        self.updateToken()
        assert self.currentToken == '{'
        self.updateToken()
        while self.currentToken in ['static', 'field', 'constructor', 'function', 'method']:
            self.tokenToFunction[self.currentToken]()
        assert self.currentToken == '}'
    
    def compileClassVarDec(self):
        assert self.currentToken in ['static', 'field']
        kind = self.currentToken
        self.updateToken()
        symbolType = self.currentToken
        self.updateToken()
        self.symbolTable.define(self.currentToken, symbolType, kind)
        self.updateToken()
        while self.currentToken == ',':
            self.updateToken()
            self.symbolTable.define(self.currentToken, symbolType, kind)
            self.updateToken()
        assert self.currentToken == ';'
        self.updateToken()
    
    def compileSubRoutine(self):
        self.symbolTable.startSubroutine()
        assert self.currentToken in ['constructor', 'method', 'function']
        if self.currentToken == 'method':
            self.symbolTable.define("this", self.currentClass, "argument")
        self.updateToken()
        self.updateToken()
        name = self.currentToken
        self.updateToken()
        assert self.currentToken == '('
        self.updateToken()
        self.compileParameterList()
        assert self.currentToken == ')'
        self.updateToken()
        assert self.currentToken == '{'
        self.updateToken()
        while self.currentToken == 'var':
            self.compileVarDec()
        nLocals = self.symbolTable.varCount('var')
        self.writer.writeFunction(".".join([self.currentClass, name]), nLocals)
        while self.currentToken != '}':            
            self.compileStatements()
        assert self.currentToken == '}'
        self.updateToken()
    
    def compileParameterList(self):
        while self.currentToken != ')':
            if self.currentToken != ',':
                symbolType = self.currentToken
                self.updateToken()
                self.symbolTable.define(self.currentToken, symbolType, 'argument')
                self.updateToken()
            else:
                self.updateToken()
    
    def compileVarDec(self):
        assert self.currentToken == 'var'
        self.updateToken()
        symbolType = self.currentToken
        self.updateToken()
        while self.currentToken != ';':
            if self.currentToken != ',':
                self.symbolTable.define(self.currentToken, symbolType, 'var')
            self.updateToken()
        assert self.currentToken == ';'
        self.updateToken()
    
    def compileStatements(self):
        while self.currentToken in self.statements:
            self.tokenToFunction[self.currentToken]()
    
    def compileDo(self):
        assert self.currentToken == 'do'
        self.updateToken()
        identifier1 = self.currentToken
        self.updateToken()
        if self.currentToken == '.':
            self.updateToken()
            function = ".".join([identifier1, self.currentToken])
            self.updateToken()
        assert self.currentToken == '('
        self.updateToken()
        self.compileExpressionList()
        assert self.currentToken == ')'
        self.updateToken()
        assert self.currentToken == ';'
        self.updateToken()
        self.writer.writeCall(function, self.nArgs)
        self.writer.writePop('temp', 0)
        self.nArgs = 0
        
    
    def compileLet(self):
        assert self.currentToken == 'let'
        self.updateToken()
        self.updateToken()
        if self.currentToken == '[':
            self.updateToken()
            self.compileExpression()
            assert self.currentToken == ']'
            self.updateToken()
        assert self.currentToken == '='
        self.updateToken()
        self.compileExpression()
        assert self.currentToken == ';'
        self.updateToken()
        
    
    def compileWhile(self):
        assert self.currentToken == 'while'
        self.updateToken()
        assert self.currentToken == '('
        self.updateToken()
        self.compileExpression()
        assert self.currentToken == ')'
        self.updateToken()
        assert self.currentToken == '{'
        self.updateToken()
        self.compileStatements()
        assert self.currentToken == '}'
        self.updateToken()
    
    def compileIf(self):
        assert self.currentToken == 'if'
        self.updateToken()
        assert self.currentToken == '('
        self.updateToken()
        self.compileExpression()
        assert self.currentToken == ')'
        self.updateToken()
        assert self.currentToken == '{'
        self.updateToken()
        self.compileStatements()
        assert self.currentToken == '}'
        self.updateToken()
        if self.currentToken == 'else':
            self.updateToken()
            assert self.currentToken == '{'
            self.updateToken()
            self.compileStatements()
            assert self.currentToken == '}'
            self.updateToken()
            
    
    def compileReturn(self):
        assert self.currentToken == 'return'
        self.updateToken()
        if self.currentToken != ';':
            self.compileExpression()
        else:
            self.writer.writePush('constant', 0)
        assert self.currentToken == ';'
        self.writer.writeReturn()
        self.updateToken()
    
    def compileExpression(self):
        self.compileTerm()
        while self.currentToken in self.ops.keys():
            self.expression.append(self.currentToken)
            self.updateToken()
            self.compileTerm()
        print(self.expression)
        self.expressionWrite(self.expression)
        self.expression = []
        
    def expressionWrite(self, expressions):
        print(expressions)
        if len(expressions) == 1:
            if expressions[0].isdigit():
                self.writer.writePush('constant', expressions[0])
            else:
                self.writer.writePush(self.symbolTable.kindOf(expressions[0]),
                                      self.symbolTable.indexOf(expressions[0]))
        elif len(self.expression) == 2:
            op = expressions.pop(0)
            self.expressionWrite(expressions[0])
            self.writer.writeArithmetic(self.ops[op])
        elif len(self.expression) > 2:
            split = 0
            for exp in expressions:
                if exp in self.ops.keys():
                    op = exp
                    break;      
                split += 1
            self.expressionWrite(expressions[:split])
            self.expressionWrite(expressions[split + 1:])
            self.writer.writeArithmetic(self.ops[op])
    
    def compileTerm(self):
        if self.currentToken == '(':
            self.updateToken()
            self.compileExpression()
            assert self.currentToken == ')'
            self.updateToken()
        elif self.currentToken in self.unaryOps:
            self.expression.append(self.currentToken)
            self.updateToken()
            self.compileTerm()
        else:
            self.expression.append(self.currentToken)
            self.updateToken()
            if self.currentToken == '[':
                self.updateToken()
                self.compileExpression()
                assert self.currentToken == ']'
                self.updateToken()
            elif self.currentToken in ['.', '(']:
                if self.currentToken == '.':
                    self.updateToken()
                    self.updateToken()
                assert self.currentToken == '('
                self.updateToken()
                self.compileExpressionList()
                assert self.currentToken == ')'
                self.updateToken()
    
    def compileExpressionList(self):
        if self.currentToken not in self.stoppers:
            self.compileExpression()
            self.nArgs += 1
            while self.currentToken == ',':
                self.updateToken()
                self.compileExpression()
                self.nArgs += 1
        
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
            symbolTable = SymbolTable()
            outputFile = f.rstrip('.jack') + '.vm'
            vmWriter = VMWriter(outputFile)
            engine = CompilationEngine(tokenizer, symbolTable, vmWriter)
            engine.compileJack()
            print(engine.symbolTable.classTable)
            inputFile.close()


class VMWriter(object):
    def __init__(self, outputFileName):
        self.output = open(outputFileName, 'w')
        
    def writePush(self,segment, index):
        self.output.write("push {} {}\n".format(segment, index))
        
    def writePop(self, segment, index):
        self.output.write("pop {} {}\n".format(segment, index))
    
    def writeArithmetic(self, command):
        if command in ['multiply', 'divide']:
            self.writeCall(".".join(["Math", command]), 2)
        else:
            self.output.write("{}\n".format(command))
    
    def writeLabel(self, label):
        self.output.write("label {}\n".format(label))
        
    def writeGoto(self, label):
        self.output.write("goto {}\n".format(label))
        
    def writeIf(self, label):
        self.output.write("if-goto {}\n".format(label))
        
    def writeCall(self, name, nArgs):
        self.output.write("call {} {}\n".format(name, nArgs))
        
    def writeFunction(self, name, nLocals):
        self.output.write("function {} {}\n".format(name, nLocals))
        
    def writeReturn(self):
        self.output.write("return\n")
        
    def close(self):
        self.output.close()

sourcePath = sys.argv[1]
jack = JackAnalyzer(sourcePath)
jack.translate()        