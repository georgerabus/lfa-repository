import random
from collections import defaultdict, deque

class Grammar:
    def __init__(self):
        self.VN = {'S', 'A', 'B', 'C'}
        self.VT = {'a', 'b', 'c'}
        self.P = {
            'S': ["aA", "bB"],
            'A': ["bS", "cA", "aB"],
            'B': ["aB", "b"],
        }
        self.S = 'S'
    
    def classify_grammar(self):
        # Check if the grammar is right-linear (A → aB or A → a)
        for non_terminal, productions in self.P.items():
            for production in productions:
                if len(production) > 2:  # More than one non-terminal
                    return "Context Free Grammar (Type-2)"
                if len(production) == 2 and not production[0].islower():  # First character should be terminal
                    return "Context Free Grammar (Type-2)"

        return "Regular Grammar (Type-3)"

    
    def generate_string(self):
        result = "S"
        while any(c in self.VN for c in result):
            for non_terminal in self.VN:
                if non_terminal in result:
                    replacement = random.choice(self.P[non_terminal])
                    result = result.replace(non_terminal, replacement, 1)
        return result

class FiniteAutomaton:
    def __init__(self):
        self.States = {"q0", "q1", "q2", "q3"}
        self.Alphabet = {'a', 'b'}
        self.StartState = "q0"
        self.FinalStates = {"q3"}
        self.Transitions = {
            ("q0", 'a'): ["q1"],
            ("q1", 'b'): ["q2"],
            ("q1", 'a'): ["q3", "q1"],
            ("q0", 'b'): ["q2"],
            ("q2", 'b'): ["q3"],
        }


    def is_deterministic(self):
        return all(len(states) == 1 for states in self.Transitions.values())
    
    def convert_to_regular_grammar(self):
        grammar = defaultdict(list)
        for (from_state, symbol), to_states in self.Transitions.items():
            for to_state in to_states:
                grammar[from_state].append(f"{symbol}{to_state}")
        return dict(grammar)
    
    def convert_ndfa_to_dfa(self):
        dfa_transitions = {}
        new_states = deque()
        processed_states = set()
        initial_state = frozenset([self.StartState])
        new_states.append(initial_state)
        
        while new_states:
            current_set = new_states.popleft()
            state_name = "".join(sorted(current_set))
            if state_name in processed_states:
                continue
            processed_states.add(state_name)
            
            for symbol in self.Alphabet:
                new_state_set = set()
                for state in current_set:
                    if (state, symbol) in self.Transitions: 
                        new_state_set.update(self.Transitions[(state, symbol)]) #adds all reachable NDFA states
                
                if new_state_set:
                    new_state_name = "".join(sorted(new_state_set)) # convert it into a DFA state
                    dfa_transitions[(state_name, symbol)] = new_state_name # store the transition 
                    if new_state_name not in processed_states:
                        new_states.append(frozenset(new_state_set))
        
        return dfa_transitions

if __name__ == "__main__":
    grammar = Grammar()
    print("Grammar Classification: ", grammar.classify_grammar())
    
    print("Generated strings:")
    for _ in range(5):
        print(grammar.generate_string())
    
    fa = FiniteAutomaton()
    print("The FA is", "Deterministic" if fa.is_deterministic() else "Non-Deterministic")
    
    print("Regular Grammar Representation:")
    regular_grammar = fa.convert_to_regular_grammar()
    for key, value in regular_grammar.items():
        print(f"{key} -> {' | '.join(value)}")
    
    print("DFA Representation (Converted from NDFA):")
    dfa = fa.convert_ndfa_to_dfa()
    for (state, symbol), new_state in dfa.items():
        print(f"({state}, {symbol}) -> {new_state}")
