import sys

def simplify(file_):
    with open(file_, "rb") as file:
        data = file.readlines()
        
    for num, x in enumerate(data):
        x = filter(None, x.split())
        x = ' '.join(x)
        data[num] = x
    
    parse(data)

def parse(data):
    variables = {}
    out = ""
    for x in data:
        if x.startswith("var"):
            x = x.replace("var", '').replace(" ", "")
            x = x.split("=")
            variables[x[0]] = x[1]
            continue

        elif "$" in x:
            var = x.split("$")[1]
            if var in variables:
                out_var = variables[var]
            if not x.endswith(";"):
                x = x.replace("$"+var, out_var+";")
            else:
                x = x.replace("$"+var, out_var)
                
        elif ":" in x and not x.endswith(";"):
            x = x.replace("\n", ";")
        
        out += x
    
    write(out)



def write(data):
    file_ = sys.argv[1]
    name = file_.split(".")
    with open(name+".css", 'wb') as file:
        data.write(file.read())

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: {0} <file.gss>"

    else:
        simplify(sys.argv[1])
