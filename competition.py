from functions import readFromFile
from prettytable import PrettyTable

tableToShow = PrettyTable()

def getSum(list):
    sum = 0
    for item in list:
        sum += item['score']

    return sum

def getProcent(number):
    k = 2
    i = 0
    while True:
        if not (number[i] == '0' or number[i] == '.'):
            k -= 1

        if k == 0:
            break

        i += 1

    return str(int(float(number) * pow(10,i)) / pow(10,i)) + '%'

def getMembers():
    membersFromFile = readFromFile()
    members = []

    for member in membersFromFile:
        members.append({
            'id': member['id'],
            'score': member['score']
        })

    return members

def randomMember(data):
    membersProcents = []

    totalSum = getSum(data)

    for member in data:
        membersProcents.append({
            member['id'] : float(member['score'] / totalSum)
        })

    # print(data)
    # print(membersProcents)

    tableToShow.field_names = ['id', 'propability']
    for member in data:
        tableToShow.add_row([member['id'], getProcent(str(float(member['score'] / totalSum)))])

    print(tableToShow)

randomMember(getMembers())