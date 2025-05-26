s = "AXaD"
res = set()
productions = s
def backtrack(ignore=set()):
    if len(productions) == 1:
        return
    
    curr = ""
    for part_id in range(len(productions)):
        str_part_id = str(part_id)
        if str_part_id not in ignore:
            part = productions[part_id]
            curr += part
            if part.isalpha() and part == part.upper():
                backtrack(ignore | set(str_part_id))

    if curr not in ["", productions]: 
        res.add(curr)

backtrack()
print(res)
for i in res:
    print(i)
