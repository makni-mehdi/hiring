# Algorithm Description
The implemented algorithm is a greedy algorithm which goes through each row in the first dataset A, finds the rows in dataset B -in constant time- whose company name shares at least one word with the company name of that row from dataset A and runs a scoring function which takes into account all the attributes but the address on the selected rows. Finally, it finds the maximum score, compares it to a certain threshold and decides whether it is a match or not. Each company in dataset A is matched to the most likely comopany in dataset B.

# Implementation Details

### Graph of Possibilities
Before running the algorithm, we go through the data points in dataset B and look at the set of words in each company name. We create a dictionary which maps words to companies whose name contain that word. We then filter some if we attain a certain threshold depending on the size of input. This eliminates redundant words like 'la' ,'et', 'du'...

### Phone Suffix
Select the last 8 digits of the phone number after processing to avoid any confusion between countries fast and presence/absence of 0 in French phone numbers.

### Website Suffix
Eliminates the initial "www." or "https://" or ""http://"... which sometimes prevents from matching two companies who in reality share the same website.

# Complexity
The algorithm runs in O(n^2).  
However since we filter our search and all words have key values with length at most n/200, we get a much faster algorithm than naive all-couples-comparison and since we rely on data processing and scoring functions, we get a much more effective than comparing single attributes.  
Please allow for around 15s depending on computational power for the given datasets (8000+) x (8000+). 