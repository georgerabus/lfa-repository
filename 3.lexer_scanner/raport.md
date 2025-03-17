# Lexer & Scanner

## Course: Formal Languages & Finite Automata  
## Author: Chirtoaca Liviu  

## Theory  
Lexers, also called lexical analyzers, are important tools in computer science and compiler design. They help break down source code into small parts called tokens, which represent elements like keywords, variables, numbers, and symbols. These tokens are then used by parsers to understand the code’s structure.

A lexer works by reading the input code character by character and grouping them into tokens based on predefined rules. These rules are often defined using regular expressions or finite automata. One common method is using a deterministic finite automaton (DFA), which ensures fast and efficient tokenization by following a structured path through different states.

Lexers usually perform their tasks in stages. First, they remove unnecessary parts like spaces and comments. Then, they identify tokens and classify them. This step-by-step approach makes lexers more organized and easier to maintain.

Another important job of a lexer is handling errors. If it encounters an invalid character or an unknown sequence, it reports the issue to help programmers fix their code. Some lexers also try to recover from errors and continue processing instead of stopping completely.

Beyond compilers, lexers are used in many applications like syntax highlighters, code formatters, and text analyzers, making them useful tools for programming and text processing.
---

## Objectives  
- Understand what lexical analysis [1] is.
- Get familiar with the inner workings of a lexer/scanner/tokenizer.
- Implement a sample lexer and show how it works.

---

### Lexer

Before using a lexer, we have to define the tokens that the lexer uses. Here are the names of the
tokens and the delimiters which define these tokens. I chose a list of lists, where the delimiters are the regex
which follows the pattern of the token, and the names of those tokens

```
Tokens = [
[r"\A\s+", "WHITESPACE"],
[r"\A;" , ";"],
[r"\A[(]", "("],
[r"\A[)]", ")"],
[r"\A[{]", "{"],
[r"\A[}]", "}"],
[r'\A"""([\s\S]*?)"""', "BCOMMENT"],
[r"\A\#.*\$", "COMMENT"],
[r"\A\bif\b", "IF"],
[r"\A\belse\b", "ELSE"],
[r"\A\blet\b", "DECLARATOR"],
[r"\A[\^\s\W\d]+", "VARIABLE"],
[r'\A=(?!=)', "DECLARATOR_OPERATOR"],
[r'\A==(?!=)', "EQUAL_OPERATOR"],
[r'\A[+\-]', "ADDITIVE_OPERATOR"],
[r'\A[*\/]', "MULTIPLICATIVE_OPERATOR"],
[r"\A\d+", "NUMBER"],
[r'\A"[^"]*"', "STRING"],
[r"\A'[^'']*'", "STRING"],
]
```

Then, I initialize a class called Tokenizer (Lexer/Scanner), which initializes with 2 variables: the
string on which we will do tokenization and the cursor, which traverses the string so we don’t tokenize a
token that has already been met

```py
class Tokenizer:
    def __init__(self, string):
        self._string = string
        self._coursor = 0
```

Now, I can start with the actual tokenization. In order to do that, I have created a recursive method
which utilizes the cursor and regex to match all of the tokens inside the given string. The way I do this
is simple. I iterate through all of the tokens and see if the current string starts the same way as any of the
tokens do. If it does, but it is a whitespace or comment, then that token is skipped by advancing the cursor
and calling the method recursively again. Thus, as the cursor is shifted and that token is jumped over, we
can start to search for the next token. But only after we have checked if there can be a next token by using
the getNextToken method, which checks if the cursor did not exceed the length of the string. If yes, then
break out of the recursive loop.

```py
def hasMoreTokens(self):
    return self._coursor < len(self._string)
```

Then again, we can iterate through all of the tokens, and if the next token is found but it is not a
whitespace or comment, then the cursor is advanced, and the lexeme is returned in the form of a dictionary
made out of the type (name) of the lexeme (e.g., STRING, NUMBER) and its value (e.g., 1, ”Hello!”),
which is returned.

```py
def getNextToken(self):
    if not self.hasMoreTokens():
        return None
    curr_string = self._string[self._coursor:]
    for regex, literal_type in Tokens:
        match = re.findall(regex, curr_string, flags=re.MULTILINE)
        if len(match) == 0:
            continue
        self._coursor += len(match[0])
        if literal_type in ["WHITESPACE", "BCOMMENT","COMMENT"]:
            if literal_type == "BCOMMENT":
                self._coursor += 6
                return self.getNextToken()
            return {
                    "type": literal_type,
                    "value": match[0]
                    }
```

---
## Results
![Consola](/Images/lexer-code.png)
![Consola2](/Images/lexer.png)

# Conclusion

In this lab, I built a lexer to break a string into tokens based on predefined rules. The process involved defining token types, setting up a tokenizer class, and implementing the logic for scanning the input.

First, I created a list of token names paired with regular expressions to match them. Then, I set up a Tokenizer class, which stores the input string and tracks progress using a cursor.

The lexer scanned the string by checking each part against the token patterns. It skipped spaces and comments to focus only on meaningful tokens. When a match was found, the lexer recorded the token type and value, then moved the cursor forward.