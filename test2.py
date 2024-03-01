inputlist = input().split()
inputstr = inputlist[0]
k = int(inputlist[1])
outputstring = ""
for i in range(len(inputstr)):
    front = max(0,i - k)
    tempchar = inputstr[i]
    if (tempchar in inputstr[front:i]):
        tempchar = '-'
    outputstring += tempchar
print(outputstring)