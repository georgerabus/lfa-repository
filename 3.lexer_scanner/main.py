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
]

class Tokenizer:
    def __init__(self, string):
        self._string = string
        self._cursor = 0
    
    def hasMoreTokens(self):
        return self._cursor < len(self._string)
    
    def getNextToken(self):
        if not self.hasMoreTokens():
            return None
        
        curr_string = self._string[self._cursor:]

        for regex, literal_type in Tokens:
            match = re.findall(regex, curr_string, flags=re.MULTILINE)
            
            if len(match) == 0:
                continue

            self._cursor += len(match[0])

            if literal_type in ["WHITESPACE", "BCOMMENT", "COMMENT"]:
                return self.getNextToken()
            
            return {
                "type": literal_type,
                "value": match[0]
            }
        
        return None  # No valid token found

    def tokenize(self):
        tokens = []
        while self.hasMoreTokens():
            token = self.getNextToken()
            if token:
                tokens.append(token)
        return tokens

# Example usage:
if __name__ == "__main__":
    code = """
    let x = 10;
    if x == 10 {
        # This is a comment
        print("Hello");
    }
    """
    tokenizer = Tokenizer(code)
    tokens = tokenizer.tokenize()
    for token in tokens:
        print(token)
