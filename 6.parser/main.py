from Parser import *
import json

parser = Parser()
code = """
if (1){
 let a = 5*(3+2);
} else {
 let b = "3";
}
"""

result: dict = parser.parse(code)
print(json.dumps(result, indent=2))