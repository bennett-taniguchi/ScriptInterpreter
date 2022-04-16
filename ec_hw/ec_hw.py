""" 
    Bennett Taniguchi
    Extra Credit Assignment : Language Interpreter
    * This module interprets a given csv file, pipes file, and
    chosen pipeline command inside said pipes file to perform
    operations and store said results in a variable cols.
    Throws Exceptions upon an improperly formatted file, 
    column non existant in csv file, or improper usage of
    syntax in a pipes file. Ignores additional pipelines in
    file beyond requested pipeline to be interpreted.
"""


''' Global Variable Representing Final Table Results
    Format will be in format as follows:
    {'Column1': [val1,val2,...], 'Column2': [val1,val2,...],...}
    Where each entry inside the dictionary is correspondent to a
    key value pair representing the head of a column in the csv
    file and the following entries in said column. Values representing
    column data can be variable length dependent on csv file format.
'''
cols = {} 


def createCols(name):
    """
        Parameters:
            name : CSV File to be processed           
        Assumptions:
            Input file exists
        Throws: 
            Throws exception upon encountering non-head values that aren't 
            float values.
        Assumes:
            Assumes CSV file isn't empty.
        Behavior:  
            Otherwise modifies global cols variable to contain a representation of 
            values in csv file. Data stored in cols variable as outlined in 
            cols docstring.
    """
    f = open(name,"r") 
    colNames = (f.readline().strip().split(','))
    for names in colNames: cols[names] = []
    for x in f:
        count = 0 
        for y in x.strip().split(','):
            if(y.count('.') != 1 or not(y.replace('.','')).isnumeric()): 
                raise Exception("Incorrectly Formatted File")
            if(count == len(colNames)): 
                count = 0
            key = colNames[count]
            cols[key].append(y)
            count += 1


def arithmetic(op, A, B, new): 
    """
        Parameters:
            op : Type of operation to perform
            A : First Column used as argument in column expression
            B : Second Column used as argument in column expression 
            new : Name of new Column as result of column expression         
        Returns:
            New Column of which is the results of a column operation
            performed A operation B where same value row pairs in A,B
            engage in the operation and the resultant value is stored
            in the same value row in new.
        Throws:
            Throws Exception upon encountering value of A or B or both where
            the value doesn't exist as a head in csv file. Throws Exception 
            upon encountering an op that isn't one of as follows: * - + / %
    """
    if(A not in cols or B not in cols): raise Exception("Invalid Column(s)")
    deepNew = []
    if(op in '*-+/%'):
        for x in range(len(cols[A])):
            deepNew.append(eval(str(cols[A][x]) + op + str(cols[B][x])))  
    else: raise Exception("Invalid Operation")
    return {**cols, **{new:deepNew}}
    
def project(*args):   
    """
        Parameters:
            *args : Variable amount of arguments to process where each
                    value is a column to be represented in cols variable.        
        Returns:
            Returns a cols object as outlined in the cols docstring, where
            values passed as arguments for project are maintained and 
            excess values in cols not specified in project are pruned.
        Assumptions:
            Assumes cols is populated with values.
        Throws: 
            Throws Exception upon encountering args value which doesn't
            exist in cols variable as a head value.

    """
    for items in args:
        for item in items:
            
            if(item not in cols): raise Exception("Invalid Column(s)")
    newCopy = {}
    for x in args[0]:
        if(cols[x]):
            newCopy[x] = cols[x]
    return newCopy


def validName(name):
    """
        Helper Function:
            Parameters:
                name : Column name to be checked      
            Returns:
                True if name is only comprised of alphabnumeric characters
                with or without a '_' . Otherwise returns False        
    """
    result = ''.join(i for i in name if not i.isdigit())
    if(result.isalpha()): return True
    elif((result.replace('_','').isalpha())): return True
    else: return False

def interpret(rules,data,call):
    """
        Parameters:
            rules : pipes file to be processed  
            data  : CSV file to be processed
            call  : Pipeline to be interpreted   
        Assumptions:
            Input file exists and is properly formatted for 
            pipes file and csv file.
        Behavior: interpret reads through the pipes file and performs
        outlined operations specified upon column values in csv file.
        Intepret will only perform operations specified to the pipeline
        variable named in call and will ignore any other pipelines not
        specified.   
    """
    global cols
    p = open(rules,'r')
    createCols(data)
    pipes = (p.read().strip().split())
    tokenTotal = (len(pipes))
    isProject = False
    projections = []
    matchedCall = False
    for ins in range(tokenTotal):
        if(call == pipes[ins]): matchedCall = True
        if(not matchedCall): continue
        elif(matchedCall and pipes[ins] == ';'): matchedCall = False
        if(isProject):
            if(pipes[ins] not in ['arithmetic','project','|',';']): 
                if(not validName(pipes[ins]) and pipes[ins] != ';'): 
                    raise Exception("Syntax Error in Input Script") 
                projections.append(pipes[ins])
            elif(pipes[ins] == ';'): 
                if(pipes[ins] in ['arithmetic','project']): 
                    raise Exception("Syntax Error in Input Script") 
                isProject = False
                cols = project(projections)
                projections = []
        if(pipes[ins] == 'arithmetic'): 
            op = pipes[ins+1]
            a = pipes[ins+2]
            b = pipes[ins+3]
            c = pipes[ins+4]                       
            if(op not in '*-+/%'): raise Exception("Syntax Error in Input Script")
            elif ( (a or b or c) in  ['arithmetic','project'] or not validName(a) 
                                          or not validName(b) or not validName(c)): 
                raise Exception("Syntax Error in Input Script") 
            cols = arithmetic(op,a,b,c)
        elif(pipes[ins] == 'project'): 
            isProject = True
            projections = []
 

'''TOP LEVEL FUNCTIONALITY'''
# Call to interpret here
interpret('testCurry.pipes','testCurry.csv','testCurry')
# Displays results in cols to calls to interpret
print(cols)