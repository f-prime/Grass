import sys
import re

__version__ = "0.1.2"

class Grass:

    def __init__(self):
        self.tokens = {"var":self.var, "import":self.import_}
        self.inline_tokens = {"$":self.variable, "//":self.comment}
        self.variables = {}
        self.out = ""

    def simplify(self, data):
        """

            This function removes all preceding spaces so that splitting up of the lines becomes easier during parsing. 

        """
        
        for num, x in enumerate(data):
            if x == "":
                continue
            x = filter(None, x.split()) 
            x = ' '.join(x)
            data[num] = x
        if not data[0]:
            data.pop(0)
        return data
    
        
    def run(self, file_=None):

        if file_:
            grass = file_ #Only if we call it from another program
        else:
            grass = sys.argv[1]
        self.name = grass
        with open(grass, 'rb') as file:
            data = self.simplify(file.readlines())
        
        data = self.preparse(data)
        self.parse(self.unnest(data)) #Takes the ouput of of simplify() and uses it as an argument for parse() file.readlines() returns a string while still keeping the \n

        self.write() #Write the output after everything is done
    
    def unnest(self, data):
        for num, x in enumerate(data):
            if x == "":
                data[num] = " "
        nest = 0
        code = {}
        output = []
        prev = []
        for x in data:
            if "{" in x:
                prev_ = re.findall("([-!$%^&*()_+|~=`{}\[\]:\";'<>?,.\/a-zA-Z0-9_]*){", x.replace(" ",''))[0]
                x = x.replace(prev_, '') 
                if nest != len(prev):
                    prev.append(prev_)
                elif nest > len(prev) and len(prev) != 0:
                    prev.pop(nest-1)
                    prev.append(prev_)
                else:
                    prev.append(prev_)
                nest += 1
            
            if nest not in code:
                if "{" not in x:
                    code[nest] = x+"\n"
                else:
                    code[nest] = " ".join(prev) + " "+x+"\n"
            else:
                if "{" not in x:
                    code[nest] += x+"\n"
                else:
                    code[nest] += " ".join(prev) + " "+x+"\n"
            if "}" in x:
                nest -= 1
                if len(prev) > nest:
                    prev.pop(nest) 
        for x in code:
            output.append(code[x].replace("\n",''))
        output.append("}") 
        return output
    
    def preparse(self, data):
        out = []
        for line in data:
            check = line.split()
            if not check:
                continue
            if check[0] in self.tokens:
                self.tokens[check[0]](line)
                continue
            out.append(line)
        return out

    def parse(self, data):
        """

            There are two types of tokens that the parser looks for, inline tokens and regular tokens. Inline tokens are tokens such as $ and // that are not normally in CSS and aren't their own lines.

            Regular tokens are commands such as var and import that have their own line.


        """



        for line in data:
            check = line.split()
            if not check:
                continue

            for token in self.inline_tokens:
                if token in line:
                    line = self.inline_tokens[token](line)        
            
            self.out += line #Now we append it to the global output 
    
    def variable(self, line):
    
        find_all = re.findall("(\$[a-zA-Z0-9_]*)", line)
        for x in find_all:
            var = x.replace("$", '')
            
            if var in self.variables:
                line = line.replace(x, self.variables[var])
            
            else:
                print "Variable Error: {0} has not been declared".format(x)
                sys.exit()
        return line

    def comment(self, line):
        line = line.split("//")[0]
        return line

    def var(self, line):
        line = line.replace("var", '').replace(" ", '')
        line = line.split("=")
        self.variables[line[0]] = self.variable(line[1])

    def import_(self, line):
        line = line.split()
        with open(line[1], 'r') as file:
            data = self.simplify(file.readlines())
            data = self.preparse(data)
            self.parse(self.unnest(data))
    def write(self):
        name = self.name.split(".")[0]
        name += ".css"
        with open(name, 'w') as file:
            file.write(self.out.replace("}}", '}')) #Just incase there is a double up of curly braces

if __name__ == "__main__":
    Grass = Grass()
    if len(sys.argv) != 2:
        print "Usage: {0} <file.gss>"

    else:
        Grass.run()
