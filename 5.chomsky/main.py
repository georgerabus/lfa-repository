from collections import defaultdict

class Grammar:
    def __init__(self, grammar):
        self.productions = self.getProductions(grammar)
        self.start_symbol = "Add a start symbol"
        self.end_symbols = []
    
    def getProductions(self, grammar):
        productions = defaultdict(list)
        for line in grammar.split('\n'):
            if line.strip():
                non_terminal, production = line.split('→')
                productions[non_terminal.strip()].append(production.strip())

        return productions
    
    def printProductions(self):
        print()
        for non_terminal, productions in self.productions.items():
            print(f"{non_terminal}: {productions}")
        print()

    def addFirstState(self):
        self.productions["S0"] = ["S", "ɛ"]
                
    def removeEmptyStates(self):
        def getAllEpsilonNonTerminals():
            epsilonNonTerminals = set()
            def dfs(bad_value="ɛ"):
                for non_terminal in self.productions.keys():
                    if non_terminal not in epsilonNonTerminals:
                        for productions in self.productions[non_terminal]:
                            if bad_value in list(productions):
                                epsilonNonTerminals.add(non_terminal)
                                dfs(non_terminal)
            dfs()
            return epsilonNonTerminals
    
        def getEpsilonEmptyProduction(productions):
            res = set()
            def dfs(ignore=set()):
                if len(productions) == 1:
                    return
                
                curr = ""
                for part_id in range(len(productions)):
                    str_part_id = str(part_id)
                    if str_part_id not in ignore:
                        part = productions[part_id]
                        curr += part
                        if part.isalpha() and part == part.upper():
                            dfs(ignore | {str_part_id})

                if curr not in ["", productions]: 
                    res.add(curr)

            dfs()
            return res
        
        epsilonNonTerminals = getAllEpsilonNonTerminals()
        for non_terminal in epsilonNonTerminals:
            for production_id in range(len(self.productions[non_terminal])):
                production = self.productions[non_terminal][production_id]

                if len(production) > 1 and production != production.lower():
                    self.productions[non_terminal].extend(list(getEpsilonEmptyProduction(production)))

        for non_terminal in epsilonNonTerminals:
            productions_copy = self.productions[non_terminal][:]
            for production_id in range(len(productions_copy)):
                if productions_copy[production_id] == "ɛ":
                    self.productions[non_terminal].remove("ɛ")
                    break
                    
    def moveNonTerminals(self):
        changed = True
        while changed:
            changed = False
            for non_terminal, productions in self.productions.items():
                # Work with a copy to avoid modification during iteration
                productions_copy = productions[:]
                new_productions = []
                
                for production in productions_copy:
                    if len(production) == 1 and production != production.lower():
                        # This is a unit production (A → B where B is non-terminal)
                        # Replace it with all productions of B
                        if production in self.productions:
                            new_productions.extend(self.productions[production])
                            changed = True
                    else:
                        # Keep the original production
                        new_productions.append(production)
                
                # Update productions for this non-terminal
                self.productions[non_terminal] = new_productions
            
    class Iterator():
        def __init__(self, data, iterr=0):
            self.data = data
            self.iter = iterr
        
        def __iter__(self):
            return self
        
        def __next__(self):
            if self.iter < len(self.data):
                result = self.data[self.iter]
                self.iter += 1
                return result
            else: 
                raise StopIteration("Iterator exhausted")
        
        def reset(self):
            self.iter = 0

    def replaceTerminals(self):
        data = ['Б', 'Г', 'Д', 'Є', 'Ж', 'Ꙃ', 'Ꙁ', 'И', 'Л', 'П', 'Ꙋ', 'Ф', 'Ѡ', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'ЪІ']
        iterator = self.Iterator(data)
        new_non_terminals = {}

        for non_terminal, productions in self.productions.items():
            for production_id in range(len(productions)):
                production = list(productions[production_id])
                if len(production) > 1:
                    for item_id in range(len(production)):
                        item = production[item_id]
                        if item == item.lower():
                            if new_non_terminals.get(item) == None:
                                new_non_terminal = next(iterator)
                                new_non_terminals[item] = new_non_terminal
                            production[item_id] = new_non_terminals[item]
                    productions[production_id] = "".join(production)

        for productions, non_terminal in new_non_terminals.items():
            self.productions[non_terminal] = [productions]

    def groupSelfLiterals(self):
        data = ['Ѣ', 'Ҍ', 'Ꙗ', 'Ѥ', 'Ю', 'Ѫ', 'Ѭ', 'Ѧ', 'Ѩ', 'Ѯ', 'Ѱ', 'Ѳ', 'Ҁ']
        iterator = self.Iterator(data)
        new_non_terminals = {}
        
        def group():
            for non_terminal, productions in self.productions.items():
                for production_id in range(len(productions)):
                    production = list(productions[production_id])
                    if len(production) > 2:
                        new_production = []
                        i = 0
                        while i < len(production):
                            if i + 1 < len(production):
                                item = production[i] + production[i+1]
                                if new_non_terminals.get(item) == None:
                                    new_non_terminal = next(iterator)
                                    new_non_terminals[item] = new_non_terminal
                                new_production.append(new_non_terminals[item])
                                i += 2
                            else:
                                new_production.append(production[i])
                                i += 1
                        productions[production_id] = "".join(new_production)

            for productions, non_terminal in new_non_terminals.items():
                self.productions[non_terminal] = [productions]

        while True:
            temp = self.productions.copy()
            group()
            if temp == self.productions:
                break

    def printConvertWithoutCyrillic(self):
        character_value_dict1 = {'Ѣ': 'N1', 'Ҍ': 'N2', 'Ꙗ': 'N3', 'Ѥ': 'N4', 'Ю': 'N5', 'Ѫ': 'N6', 'Ѭ': 'N7', 'Ѧ': 'N8', 'Ѩ': 'N9', 'Ѯ': 'N10', 'Ѱ': 'N11', 'Ѳ': 'N12', 'Ҁ': 'N13'}
        character_value_dict2 = {'Б': 'M1', 'Г': 'M2', 'Д': 'M3', 'Є': 'M4', 'Ж': 'M5', 'Ꙃ': 'M6', 'Ꙁ': 'M7', 'И': 'M8', 'Л': 'M9', 'П': 'M10', 'Ꙋ': 'M11', 'Ф': 'M12', 'Ѡ': 'M13', 'Ц': 'M14', 'Ч': 'M15', 'Ш': 'M16', 'Щ': 'M17', 'Ъ': 'M18', 'ЪІ': 'M19'}

        def convert_symbol(symbol):
            return character_value_dict1.get(symbol, character_value_dict2.get(symbol, symbol))

        def convert_production(production):
            return ''.join([convert_symbol(symbol) for symbol in production])

        def print_productions(productions):
            print()
            for non_terminal, prod_list in productions.items():
                converted_productions = [convert_production(prod) for prod in prod_list]
                print(f"{convert_symbol(non_terminal)}: {converted_productions}")
            print()

        print_productions(self.productions)

    def transformToCNF(self):
        self.removeEmptyStates()
        self.printProductions()
        self.moveNonTerminals()
        self.printProductions()
        self.replaceTerminals()
        self.printProductions()
        self.groupSelfLiterals()
        self.printProductions()
        self.addFirstState()
        self.printProductions()

def main():
    grammar = """
    S → dB
    S → A
    A → d
    A → dS
    A → aAdAB
    B → aC
    B → aS
    B → AC
    C → ɛ
    E → AS
    """

    grammar = Grammar(grammar)
    grammar.printProductions()
    grammar.transformToCNF()
    grammar.printConvertWithoutCyrillic()

if __name__ == "__main__":
    main()