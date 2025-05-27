from Tokenizer import *

class Parser: # 
    def parse(self, string):
        self._string = string
        self._tokenizer = Tokenizer(string)

        self._lookahead = self._tokenizer.getNextToken()

        return self.Program()
    
    def Program(self): #
        return {
            "type": "Program",
            "body": self.StatementList()
        }
    

    def StatementList(self): #
        statementList = []
        
        while self._lookahead != None:
            if self._lookahead["type"] == "}":
                break
            statementList.append(self.Statement())
        
        return statementList

    # Statement : ExpressionStatement ;
    def Statement(self):
        match self._lookahead["type"]:
            case "DECLARATOR": return self.VariableDeclaration()
            case "IF": return self.IfStatement()
            case "PRINT": return self.PrintStatement()
            case _: return self.ExpressionStatement()

    def IfStatement(self):
        self._eat("IF")
        binary_expression = self.ParanthesizedExpression()
        block_statement = self.BlockStatement()
        alternative_if = self.AlternateIf()
        return {
            "type": "IfStatement",
            "BooleanStatement": binary_expression,
            "IfBlock": block_statement,
            "AlternativeIf": alternative_if
        }

    def BlockStatement(self):
        self._eat("{")
        statement_list = self.StatementList()
        self._eat("}")
        return {
            "type": "BlockStatement",
            "body": statement_list
        }
    
    def AlternateIf(self):
        if not self._lookahead:
            return 
        
        if self._lookahead["type"] == "ELSE":
            self._eat("ELSE")
            if self._lookahead["type"] == "IF":
                return self.IfStatement()

            return {
                "IfBlock": self.BlockStatement()
            }
    
    # PrintStatement : PRINT '(' Expression ')' ';' ;
    def PrintStatement(self):
        self._eat("PRINT")
        self._eat("(")
        expression = self.Expression()
        self._eat(")")
        self._eat(";")
        return {
            "type": "PrintStatement",
            "expression": expression
        }
    
    # ExpressionStatement : Expression ';' ;
    def ExpressionStatement(self):
        expression = self.Expression()
        self._eat(";")
        return {
            "type": "ExpressionStatement",
            "expression": expression
        }
    
    # VariableDeclaration : VariableDeclarator ';' ;
    def VariableDeclaration(self):
        declaration = self.VariableDeclarator()
        self._eat(";")
        return {
            "type": "VariableDeclaration",
            "declarations": declaration
        }
    
    # VariableDeclarator : DECLARATOR Indentifier DECLARATOR_OPERATOR
    def VariableDeclarator(self):
        self._eat("DECLARATOR")
        variable = self.Variable()
        self._eat("DECLARATOR_OPERATOR")
        literal = self.Expression()
        return {
            "type": "VariableDeclarator",
            "id": variable,
            "init": literal
        }
    
    # Expression : Literal ;
    def Expression(self): # 
        return self.BinaryExpression()
    
    # Variable : VARIABLE ;
    def Variable(self):
        token = self._eat("VARIABLE")
        return {
            "type": "Variable",
            "value": token["value"]
        }
    
    def BinaryExpression(self):
        left = self.MultiplicativeExpression()

        while self._lookahead["type"] == "ADDITIVE_OPERATOR":
            operator = self._eat("ADDITIVE_OPERATOR")

            right = self.MultiplicativeExpression()

            left = {
                "type": "BinaryExpression",
                "left": left,
                "operator": operator,
                "right": right
            }

        while self._lookahead["type"] == "EQUAL_OPERATOR":
            operator = self._eat("EQUAL_OPERATOR")

            right = self.BinaryExpression()

            left = {
                "type": "BinaryExpression",
                "left": left,
                "operator": operator,
                "right": right
            }

        return left
    
    def MultiplicativeExpression(self):
        left = self.PrimaryExpression()

        while self._lookahead["type"] == "MULTIPLICATIVE_OPERATOR":
            operator = self._eat("MULTIPLICATIVE_OPERATOR")

            right = self.PrimaryExpression()

            left = {
                "type": "BinaryExpression",
                "left": left,
                "operator": operator,
                "right": right
            }
        return left
    
    def PrimaryExpression(self):
        match self._lookahead["type"]:
            case "VARIABLE": return self.Variable()
            case "(": return self.ParanthesizedExpression()
            case _: return self.Literal()

    def ParanthesizedExpression(self):
        self._eat("(")
        expression = self.Expression()
        self._eat(")")
        return expression

    # Literal : NumericLiteral | StringLiteral ;
    def Literal(self):
        match self._lookahead["type"]:
            case "STRING": return self.StringLiteral()
            case "NUMBER": return self.NumericLiteral()

    # NumericLiteral : NUMBER ;
    def NumericLiteral(self):
        token = self._eat("NUMBER")
        return {
            "type": "NumericLiteral",
            "value": int(token["value"])
        }
    
    # StringLiteral : STRING ;
    def StringLiteral(self):
        token = self._eat("STRING")
        return {
            "type": "StringLiteral",
            "value": token["value"]
        }
    
    def _eat(self, tokenType): #
        token = self._lookahead

        if token == None:
            raise SyntaxError(f"Unexpected end of input, expected {tokenType}.") 
    
        if token["type"] != tokenType:
            print(self._string[self._tokenizer._coursor], self._tokenizer._coursor, self._lookahead)
            val = token["value"]
            raise SyntaxError(f"Unexpected token {val}, expected {tokenType}.")
        
        self._lookahead = self._tokenizer.getNextToken()

        return token