#  Intro to formal languages. Regular grammars. Finite Automata.

### Course: Formal Languages & Finite Automata
### Author: George Răbuș

----

## Theory
Finite automata are abstract machines used to recognize patterns in input sequences, forming the basis for understanding regular languages in computer science. They consist of states, transitions, and input symbols, processing each symbol step-by-step. If the machine ends in an accepting state after processing the input, it is accepted; otherwise, it is rejected. Finite automata come in deterministic (DFA) and non-deterministic (NFA), both of which can recognize the same set of regular languages. They are widely used in text processing, compilers, and network protocols.


## Objectives:

1. Discover what a language is and what it needs to have in order to be considered a formal one;

2. Provide the initial setup for the evolving project that you will work on during this semester. You can deal with each laboratory work as a separate task or project to demonstrate your understanding of the given themes, but you also can deal with labs as stages of making your own big solution, your own project. Do the following:

a. Create GitHub repository to deal with storing and updating your project;

b. Choose a programming language. Pick one that will be easiest for dealing with your tasks, you need to learn how to solve the problem itself, not everything around the problem (like setting up the project, launching it correctly and etc.);

c. Store reports separately in a way to make verification of your work simpler (duh)

3. According to your variant number, get the grammar definition and do the following:

a. Implement a type/class for your grammar;

b. Add one function that would generate 5 valid strings from the language expressed by your given grammar;

c. Implement some functionality that would convert and object of type Grammar to one of type Finite Automaton;

d. For the Finite Automaton, please add a method that checks if an input string can be obtained via the state transition from it;


## Implementation description

* About 2-3 sentences to explain each piece of the implementation.


* Code snippets from your files.

I utilized a recursive backtracking approach. Because my grammar has only one valid string. My method can generate all of the strings until n recursions, or until the stack of the computer manages.
Also because of its nature it works with any grammar.
Here is the main method:

```py
    def getStrings(self):
        result_strs = set()
        size = 5
        def iter(grammar_str, result_str, visited, NT):
            if len(result_strs) == size:
                return
            
            for chars in grammar_str:
                for char in chars:
                    if self.parsed_grammar.get(char):
                        visited.setdefault(char, 0)
                        visited[char] += 1
                        if visited[char] < 3: 
                            iter(self.parsed_grammar[char], result_str.copy(), visited.copy(), char)
                        result_str.pop()
                    else:
                        result_str.append(char)
            if len(result_strs) == size:
                return
            if NT in self.end_symbols:
                result_strs.add("".join(result_str))
                
        iter(self.parsed_grammar[self.start_symbol], [], {}, self.start_symbol)
        return result_strs
```


Here, I used a recursive backtracking approach again. We check every single choice we have from the first one. If none of them are equal to the current index of the word we need to create, that means the word cannot be created with this grammar. However, if one of them is equal to the value at the current index of the needed string, we check that path. We increase the index of the string, then check if any of the next possibilities have the current index value of the needed string, and so on. It checks all possibilities, and if none are found, it's returned as False. If at least one is True, we return True.

```py
    def checkStr(self, check_str):        
        def iter(grammar_str, i, path_str, NT):
            if i > len(check_str) - 1:
                return path_str == check_str
            
            for chars in grammar_str:
                if len(chars) == 1:
                    if chars == check_str[i]:
                        return iter(self.parsed_grammar[NT], i + 1, path_str + chars, NT)
                else:
                    if chars[0] == check_str[i]:
                        if iter(self.parsed_grammar[chars[1]], i + 1, path_str + chars[0], chars[1]):
                            return True
            return False
        
        return iter(self.parsed_grammar[self.start_symbol], 0, "", self.start_symbol)
```

* If needed, screenshots.


## Conclusions / Screenshots / Results

In conclusion, the laboratory work was pretty challenging, I had to research different methods to parse grammar and chose interative backtracking, which is a really great fondation for a more complex grammar.

* checking string: `acabba`

```
S: ['aA', 'bB']
A: ['bS', 'cA', 'aB']
B: ['aB', 'b']
{'abaaab', 'ababbab', 'abaab', 'ababbb', 'abbab'}
True
```

## References

https://www.geeksforgeeks.org
https://stackoverflow.com/
