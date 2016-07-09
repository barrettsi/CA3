# Open the file
changes_file = 'changes_python.txt'

# For each line convert to lower case, strip white space and add to list, data
data = [line.lower().strip() for line in open(changes_file)]

# Separator between commits is a line of hyphens
sep = '------------------------------------------------------------------------'

class Commit(object):
    
    def __init__(self):
        self.revision = 0
        self.author = ''
        self.date = ''
        self.time = ''
        self.day = ''
        self.lines = 0
        self.adds = 0
        self.mods = 0
        self.dels = 0
        self.comment = ''     
     
     
#Initialise index to zero
index = 0
# Create empty list to hold commit objects
commits = list()

while True:
    try:
        current_commit = Commit()
        details = data[index+1].split('|')
        current_commit.revision = details[0].strip('r').strip()
        current_commit.author = details[1].strip()
        date_time = details[2].strip().split(' ')
        current_commit.date = date_time[0]
        current_commit.time = date_time[1]
        current_commit.day = date_time[3].strip('(,')
        current_commit.lines = int(details[3].strip()[0])
        #Commit info consists of all lines from index +3 to next sep index - length of comment
        commit_info = data[index+3: data.index(sep, index + 1)-current_commit.lines]
        current_commit.adds = len(filter(lambda x: x.startswith('a /'), commit_info))
        current_commit.mods = len(filter(lambda x: x.startswith('m /'), commit_info))
        current_commit.dels = len(filter(lambda x: x.startswith('d /'), commit_info))
        # Change index to be next occurrence of sep
        index = data.index(sep, index + 1)
        # Comment is the last 'lines' number of lines before index
        current_commit.comment = data[index - current_commit.lines: index]
        commits.append(current_commit)
        # test print statements 
    except IndexError:
        break

print 'No of lines in original file:', len(data)        
print 'No of commits:', len(commits)   
print commits[420].adds,commits[420].mods, commits[420].dels