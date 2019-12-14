import json

def checkEmptyFile():
    with open('data.json') as json_file:
        json_file.seek(0)
        if not json_file.read(1):
            return False
        else:
            return True

def writeOrUpdateFile(data):
    if not checkEmptyFile():
        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)
    else:
        oldData = readFromFile()
        print(oldData)
        print(data)

        for newItem in data:
            flag = False
            for oldItem in oldData:
                if newItem['id'] == oldItem['id']:
                    flag = True
                    break

            if flag:
                print(f"{newItem['id']} matched")
            else:
                print(f"{newItem['id']} didn't matched")

def readFromFile():
    with open('data.json') as json_file:
        if checkEmptyFile():
            data = json.load(json_file)
            return data



def getMemberFromFile(id):
    with open('data.json') as json_file:
        if checkEmptyFile():
            data = json.load(json_file)
            for member in data:
                if member['id'] == id:
                    return member
        return None




def calculateScore(data):
    commentsScore = 0
    likesScore    = len(data['likes'])
    repostsScore  = len(data['reposts']) * 2

    for key in data['comments']:
        for i in range(data['comments'][key]):
            commentsScore += pow(0.5, i+1)

    total = likesScore + repostsScore + commentsScore + data['adminDecision']

    return total


def updateCurrentMember(id, data):
    fileData = []

    if checkEmptyFile():
        fileData = readFromFile()

    flag = False
    for oldItem in fileData:
        if id == oldItem['id']:
            flag = True
            break

    if not flag:
        fileData.append({
            'id': id,
            'score': 0,
            'likes': [],
            'comments': [],
            'reposts': [],
            'adminDecision': 10,
        })

    for oldItem in fileData:
        if id == oldItem['id']:
            if data['key'] == 'likes' or data['key'] == 'reposts':
                if not data['value'] in oldItem[data['key']]:
                    oldItem[data['key']].append(data['value'])

            if data['key'] == 'comments':
                if str(data['value']) in oldItem[data['key']]:
                    oldItem[data['key']][str(data['value'])] += 1
                else:
                    if len(oldItem[data['key']]) == 0:
                        oldItem[data['key']] = {str(data['value']): 1}
                    else:
                        oldItem[data['key']][str(data['value'])] = 1

            if data['key'] == 'adminDecision':
                oldItem[data['key']] += data['value']

            oldItem['score'] = calculateScore(oldItem)
            break

    print(fileData)
    with open('data.json', 'w') as outfile:
        json.dump(fileData, outfile)



updateCurrentMember(170877706, {'key': 'likes', 'value': 122})

