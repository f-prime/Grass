import sys
import re

__version__ = "0.1.0"

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
            data = self.unnest(self.simplify(file.readlines()))
        self.parse(data) #Takes the ouput of of simplify() and uses it as an argument for parse() file.readlines() returns a string while still keeping the \n

        self.write() #Write the output after everything is done
    
    def unnest(self, data):
        for num, x in enumerate(data):
            if x == "":
                data[num] = " "
        nest = 0
        code = {}
        output = []
        for x in data:
            if "{" in x:
                nest += 1
            
            if nest not in code:
                code[nest] = x+"\n"
            else:
                code[nest] += x+"\n"
        
            if "}" in x:
                nest -= 1
        for x in code:
            out = code[x]
            if x > 1:
                length = x
                while True:
                    get_pre = code[length].replace(" ", '').split("{")[0]
                    if get_pre in out:
                        pass
                    else:
                        out = get_pre +" "+ out
                    if length == 1:
                        break
                    length -= 1
            for x in out.split("\n"):
                output.append(x)
        return output
    
    def parse(self, data):
        """

            There are two types of tokens that the parser looks for, inline tokens and regular tokens. Inline tokens are tokens such as $ and // that are not normally in CSS and aren't their own lines.

            Regular tokens are commands such as var and import that have their own line.


        """



        for line in data:
            check = line.split()
            if not check:
                continue

            if check[0] in self.tokens:
                self.tokens[check[0]](line)
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
        self.variables[line[0]] = line[1]

    def import_(self, line):
        line = line.split()
        with open(line[1], 'r') as file:
            self.parse(self.unnest(self.simplify(file.readlines())))
    
    def write(self):
        name = self.name.split(".")[0]
        name += ".css"
        with open(name, 'w') as file:
            file.write(self.out)

if __name__ == "__main__":
    Grass = Grass()
    if len(sys.argv) != 2:
        print "Usage: {0} <file.gss>"

    else:
        Grass.run()
