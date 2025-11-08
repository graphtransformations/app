from core.parser import parse
from core.ast import postfix, postfixToAST

class FunctionEntry:
    def __init__(self, user_input: str):
        self.user_input = user_input
        self.tokens = []
        self.variable = ""
        self.ast = None

    def parseFunction(self):
        """
        Tokenise the user input string
        """
        self.tokens, self.variable = parse(self.user_input)
        if not self.tokens:
            return False  
        return True
    
    def functionAST(self):
        """
        Convert tokens to postfix then build the AST
        """
        if not self.tokens:
            print ("ValueError: Token list is empty")

        else:
            self.tokens = postfix(self.tokens)
            self.ast = postfixToAST(self.tokens)
    
    def outputFunction(self):
        """
        Return the AST
        """
        if not self.ast:
            print ("ValueError: No AST found") 
        else:
            print (f"Function Variable: {self.variable}")
            return self.ast, self.variable
            
