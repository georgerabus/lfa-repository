import random
import re

def generate_regex_strings(regex_pattern, num_strings=5):
    """Generate valid strings matching the given regex pattern"""
    
    # Parse the regex pattern into a set of rules
    rules = parse_regex(regex_pattern)
    
    # Generate the specified number of strings
    results = set()
    for _ in range(num_strings * 3):  # Try more times to get unique results
        if len(results) >= num_strings:
            break
        results.add(generate_string_from_rules(rules))
    
    return list(results)[:num_strings]

def parse_regex(pattern):
    """Parse a regex pattern into a list of rules"""
    rules = []
    i = 0
    
    while i < len(pattern):
        # Handle character classes (P|Q|R)
        if pattern[i] == '(':
            end_paren = pattern.find(')', i)
            if end_paren == -1:
                raise ValueError("Unmatched parenthesis")
            
            options = pattern[i+1:end_paren].split('|')
            
            # Check for quantifiers after the parenthesis
            next_pos = end_paren + 1
            quantifier = None
            exact_count = None
            
            if next_pos < len(pattern):
                if pattern[next_pos] == '+':
                    quantifier = '+'
                    next_pos += 1
                elif pattern[next_pos] == '*':
                    quantifier = '*'
                    next_pos += 1
                elif pattern[next_pos] == '?':
                    quantifier = '?'
                    next_pos += 1
                elif pattern[next_pos] == '^':
                    quantifier = '^'
                    next_pos += 1
                    # Check for a number after ^
                    num_start = next_pos
                    while next_pos < len(pattern) and pattern[next_pos].isdigit():
                        next_pos += 1
                    if next_pos > num_start:
                        exact_count = int(pattern[num_start:next_pos])
            
            rules.append({
                'type': 'choice',
                'options': options,
                'quantifier': quantifier,
                'exact_count': exact_count
            })
            
            i = next_pos
        
        # Handle single characters with possible quantifiers
        else:
            char = pattern[i]
            i += 1
            
            # Check for quantifiers
            quantifier = None
            exact_count = None
            
            if i < len(pattern):
                if pattern[i] == '+':
                    quantifier = '+'
                    i += 1
                elif pattern[i] == '*':
                    quantifier = '*'
                    i += 1
                elif pattern[i] == '?':
                    quantifier = '?'
                    i += 1
                elif pattern[i] == '^':
                    quantifier = '^'
                    i += 1
                    # Check for a number after ^
                    num_start = i
                    while i < len(pattern) and pattern[i].isdigit():
                        i += 1
                    if i > num_start:
                        exact_count = int(pattern[num_start:i])
            
            rules.append({
                'type': 'char',
                'char': char,
                'quantifier': quantifier,
                'exact_count': exact_count
            })
    
    return rules

def generate_string_from_rules(rules):
    """Generate a string that follows the given regex rules"""
    result = ""
    
    for rule in rules:
        if rule['type'] == 'char':
            char = rule['char']
            count = determine_count(rule['quantifier'], rule['exact_count'])
            result += char * count
        
        elif rule['type'] == 'choice':
            count = determine_count(rule['quantifier'], rule['exact_count'])
            for _ in range(count):
                result += random.choice(rule['options'])
    
    return result

def determine_count(quantifier, exact_count):
    """Determine how many times to repeat based on the quantifier"""
    if exact_count is not None:
        return exact_count
    
    if quantifier is None:
        return 1
    elif quantifier == '+':
        return random.randint(1, 5)  # 1 or more, limited to 5
    elif quantifier == '*':
        return random.randint(0, 5)  # 0 or more, limited to 5
    elif quantifier == '?':
        return random.randint(0, 1)  # 0 or 1
    else:
        return 1  # Default

def explain_regex_processing(regex_pattern):
    """Explain how the regex pattern is processed step by step"""
    rules = parse_regex(regex_pattern)
    explanations = []
    
    for i, rule in enumerate(rules):
        step_num = i + 1
        
        if rule['type'] == 'char':
            char = rule['char']
            quantifier = rule['quantifier']
            exact_count = rule['exact_count']
            
            if quantifier is None:
                explanations.append(f"Step {step_num}: Match exactly one '{char}'")
            elif quantifier == '+':
                explanations.append(f"Step {step_num}: Match one to five '{char}' characters (1 or more, limited to 5)")
            elif quantifier == '*':
                explanations.append(f"Step {step_num}: Match zero to five '{char}' characters (0 or more, limited to 5)")
            elif quantifier == '?':
                explanations.append(f"Step {step_num}: Match zero or one '{char}' character")
            elif quantifier == '^' and exact_count is not None:
                explanations.append(f"Step {step_num}: Match exactly {exact_count} '{char}' characters")
        
        elif rule['type'] == 'choice':
            options = '|'.join(rule['options'])
            quantifier = rule['quantifier']
            exact_count = rule['exact_count']
            
            if quantifier is None:
                explanations.append(f"Step {step_num}: Match one of ({options})")
            elif quantifier == '+':
                explanations.append(f"Step {step_num}: Match one to five of ({options}) (1 or more, limited to 5)")
            elif quantifier == '*':
                explanations.append(f"Step {step_num}: Match zero to five of ({options}) (0 or more, limited to 5)")
            elif quantifier == '?':
                explanations.append(f"Step {step_num}: Match zero or one of ({options})")
            elif quantifier == '^' and exact_count is not None:
                explanations.append(f"Step {step_num}: Match exactly {exact_count} of ({options})")
    
    return explanations


if __name__ == "__main__":
    patterns = [
        "O(P|Q|R)+2(3|4)",
        "A*B(C|D|E)F(G|H|i)^2",
        "J+K(L|u|N)*O?(P|Q)^3"
    ]
    
    for i, pattern in enumerate(patterns):
        print(f"\nPattern {i+1}: {pattern}")
        print("\nProcessing steps:")
        steps = explain_regex_processing(pattern)
        for step in steps:
            print(step)
        
        print("\nGenerated strings:")
        strings = generate_regex_strings(pattern, 5)
        print(", ".join(strings))