# -*- coding: utf-8 -*-

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
        