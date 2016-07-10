import pandas as pd
import matplotlib.pyplot as plt
import unittest


# Find the number of adds, modifications or deletions in a commit
def get_num_changes(change_id, commit_info):
    return len(filter(lambda x: x.startswith(change_id), commit_info)) 

# Split the details list into revision number, author, a list of date/time info  and the number of comments lines  
def split_details(details_list):
    revision = details_list[0].strip('r').strip()
    author = details_list[1].strip()
    date_time = details_list[2].strip().split(' ') 
    comment_lines = int(details_list[3].strip()[0])
    return revision, author, date_time, comment_lines

# Extract date, hour and time from the date/time list extracted from the commit details
def get_date_time_info(datetime_list):
    date = datetime_list[0]
    month = int(datetime_list[0].split('-')[1])
    hour = int(datetime_list[1].split(':')[0])
    day = datetime_list[3].strip('(,').capitalize()
    return date, month, hour, day

    
if __name__ == '__main__':  
    
    # Open the file
    changes_file = 'changes_python.txt'

    # For each line convert to lower case, strip white space and add to list, data
    data = [line.lower().strip() for line in open(changes_file)]

    # Separator between commits is a line of hyphens
    sep = '------------------------------------------------------------------------'  
    
    # Initialise index to zero
    index = 0
    
    # Create dataframe to hold information from the files    
    df = pd.DataFrame()

    # Starting at index 0 go through the file taking the interesting pieces of information for each commit, 
    # adding it to dataframe df and then moving on to the next commit by finding the next separator    
    while True:
        try:
            details = data[index+1].split('|')
            #Use split_details function to extract the revision, author and a list of date/time information
            revision, author, date_time, comment_lines = split_details(details)
            #Use get_date_time_info to extract date, month, day and hour from list of date/time info
            date, month, hour, day = get_date_time_info(date_time)
            #Commit info consists of all lines from index+3 up to next sep index - no of comment lines
            commit_info = data[index+3: data.index(sep, index + 1)-comment_lines]
            #Get the number of each type of change - addition, modification and deletion
            adds = get_num_changes('a /', commit_info)
            mods = get_num_changes('m /', commit_info) 
            dels = get_num_changes('d /', commit_info) 
            #Get total number of changes
            total_changes = adds + mods + dels
            # Change index to be next occurrence of sep
            index = data.index(sep, index + 1)
            # Comment is the last 'lines' number of lines before index
            comment = data[index - comment_lines: index]
            # Append the information for this commit to the dataframe
            df = df.append({'Author': author, 'Revision': revision, 'Date': date, 'Month': month, 'Hour': hour, 'Day': day, 'Comment lines': comment_lines, 'No of Changes': total_changes, 'No of Adds': adds, 'No of Modifications': mods, 'No of Deletes': dels}, ignore_index=True)
        except IndexError:
            break

    print 'No of lines in original file:', len(data)        
    print 'No of commits:', len(df) 

    #Summary of Dataframe
    print df.info()

   
    # CHANGES PER COMMIT
    # Plot histogram showing the number of changes per commit
    df['No of Changes'].plot(kind='hist', figsize=(15,10),bins=100, xlim=(0,300))
    fig = plt.gcf()
    fig.savefig('changes-hist.png')
    plt.clf()

    # Show the average number of changes per commit and then the average per commit by author
    print 'Average number of changes per commit:', df['No of Changes'].mean()
    print 'Average number of changes per commit by author:'
    print df.groupby(['Author'])['No of Changes'].mean()
    

    # COMMITS BY TIME
    # Look at when do most/least commits take place where hour is the hour of the day in 24 hour clock
    df['Hour'].value_counts(sort = False).plot(kind='bar')
    fig = plt.gcf()
    fig.savefig('hours-bar.png')
    plt.clf()

    # Table of authors showing the times they have committed and their total number of changes for that time
    print 'Number of changes by Author by time:'
    print df.groupby(['Author','Hour'])['No of Changes'].sum() 

    # Commits by Day
    df['Day'].value_counts().plot(kind = 'bar')
    fig = plt.gcf()
    fig.savefig('day-bar.png')
    plt.clf()

    # Look at commits trend over time
    # First change data type of Date column to datetime64
    df['Date'] = df['Date'].astype('datetime64') 

    # Plot commits by date to see any trends
    df['Date'].value_counts().plot()
    fig = plt.gcf()
    fig.savefig('date-line.png')
    plt.clf()
    
    #Print the date with the highest number of commits using the idxmax function
    print 'Date with the highest number of commits:', df['Date'].value_counts().idxmax()
    
    # Plot a line chart showing the number of commits per month
    df['Month'].value_counts(sort = False).plot(kind = 'line', xlim=(6.8, 11.2), ylim=(0,120))
    fig = plt.gcf()
    fig.savefig('month-line.png')
    plt.clf()
    
    
    # COMMITS BY AUTHOR
    # Look at who has done the most and least commits 
    print 'Authors and the number of commits for each:'
    print df['Author'].value_counts()

    # Adjust the plot size so that the x labels are not cut off
    plt.gcf().subplots_adjust(bottom=0.30)
    
    # Create bar chart of number of commits by author
    df['Author'].value_counts().plot(kind='bar')
    fig = plt.gcf()
    fig.savefig('author-commits-bar.png')
    plt.clf()


    
    





















