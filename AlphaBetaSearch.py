'''
Miguel Zavala
4/13/20
CISC481-Intro To AI
Dr.Rahmat
Homework 2: Alpha-Beta Search
'''

def getUserInputNumbers(n:int=12)->[int]:
    listOfNumbers = []
    i=1
    while i<=n:
        print(str(i)+")Enter number:")
        curr_input = input()
        if(curr_input.isdigit()==False):
            i=i-1
            print('This is not a valid number, retry')
            continue
        else:
            listOfNumbers.append(int(curr_input))

        i+=1

    #print("These are your input values:"+str(listOfNumbers))
    return listOfNumbers






#terminalstates = getUserInputNumbers(12)
terminalstates = [4, 5435, 6, 4, 2, 5, 6, 6, 6, 4, 3, 5]
print("Terminal states:"+str(terminalstates))