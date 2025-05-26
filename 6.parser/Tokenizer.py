import re

Tokens = [
    [r"\A\s+", "WHITESPACE"],
    [r"\A;" , ";"],
    [r"\A[(]", "("],
    [r"\A[)]", ")"],
    [r"\A[{]", "{"],
    [r"\A[}]", "}"],
    [r'\A"""([\s\S]*?)"""', "BCOMMENT"],
    [r"\A\#.*$", "COMMENT"],
    [r"\A\bif\b", "IF"],
    # [r"\A\belif\b", "ELIF"],
    [r"\A\belse\b", "ELSE"],
    [r"\A\blet\b", "DECLARATOR"],
    [r"\A[^\s\W\d]+", "VARIABLE"],
    [r'\A=(?!=)', "DECLARATOR_OPERATOR"],
    [r'\A==(?!=)', "EQUAL_OPERATOR"],
    [r'\A[+\-]', "ADDITIVE_OPERATOR"],
    [r'\A[*\/]', "MULTIPLICATIVE_OPERATOR"],
    [r"\A\d+", "NUMBER"],
    [r'\A"[^"]*"', "STRING"],
    [r"\A'[^'']*'", "STRING"],
    # [r'^\"(?:[^"\\]|\\.)*"', "STRING"],
    # [r"^\'(?:[^'\\]|\\.)*'", "STRING"],
]

class Tokenizer:
    def __init__(self, string):
        self._string = string
        self._coursor = 0
    
    def hasMoreTokens(self):
        return self._coursor < len(self._string)
    
    def getNextToken(self):
        if not self.hasMoreTokens():
            return None
        
        curr_string = self._string[self._coursor:]

        for regex, literal_type in Tokens:
            match = re.findall(regex, curr_string, flags=re.MULTILINE)
            
            if len(match) == 0:
                continue

            self._coursor += len(match[0])

            if literal_type in ["WHITESPACE", "BCOMMENT","COMMENT", "NEWLINE"]:
                if literal_type == "BCOMMENT":
                    self._coursor += 6

                return self.getNextToken()
            
            return {
                "type": literal_type,
                "value": match[0]
            }