# -*- coding: utf-8 -*-

class JackTokenizer(object):
    def __init__(self, inputFile):
        self.input = inputFile
        self.tokens = []
        self.keywords = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+',
                         '-', '*', '/', '&', '|', '<', '>', '=', '~', '"']
        self.tokenize()
        
    def tokenize(self):
        current_line = self.input.readline()
        while current_line != '':
            tokens = current_line.strip('\r\t\n').split('//', 1)[0].rstrip(
                    ' ').split(' ')
            comment= False
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
            if word in self.keywords:
                if word == '"':
                    while '"' not in self.tokens[0]:
                        token += self.tokens.pop(0) + " "
                    word = self.tokens.pop(0)
                    token += word.split('"')[0]
                    self.tokens.insert(0, word.split('"')[1])
                    return token
                else:
                    return word
            split = []
            for c in word:
                if c in self.keywords:                    
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

                
    
        