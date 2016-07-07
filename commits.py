# Open the file
changes_file = 'changes_python.txt'

# For each line convert to lower case, strip whitespace and add to list data
data = [line.lower().strip() for line in open(changes_file)]

#number of lines in the file
print len(data)

# Separator between commits is a line of hyphens
sep = '------------------------------------------------------------------------'


#Initialise index and count to zero
index, count = 0, 0
commits = {}

while True:
    try:
        details = data[index+1].split('|')
        revision = details[0].strip('r').strip()
        author = details[1].strip()
        date_time = details[2].strip().split(' ')
        date = date_time[0]
        time = date_time[1]
        day = date_time[3].strip('(,')
        lines = int(details[3].strip()[0])
        commit = data[index+3: data.index(sep, index + 1)]
        adds = len(filter(lambda x: x.startswith('a /'), commit))
        mods = len(filter(lambda x: x.startswith('m /'), commit))
        dels = len(filter(lambda x: x.startswith('d /'), commit))
        # Change index to be next occurrence of sep
        index = data.index(sep, index + 1)
        # Comment is the last 'lines' number of lines before index
        comment = data[index - lines: index]
        count += 1
        # test print statements    
        print revision
        print author   
        print date
        print time
        print day
        print lines 
        print adds, mods, dels 
        print comment
    except IndexError:
        break

# test print statements        
print revision
print author  
print date_time      
print date
print time
print day
print lines 
print commit 
print adds, mods, dels 
print comment
print 'no of commits', count