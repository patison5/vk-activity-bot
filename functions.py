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
    votes         = len(data['votes'])

    for key in data['comments']:
        for i in range(data['comments'][key]):
            commentsScore += pow(0.5, i+1)

    total = likesScore + repostsScore + commentsScore + votes + data['adminDecision']

    return total


def updateCurrentMember(id, data, sign = 1):
    fileData = []

    if checkEmptyFile():
        fileData = readFromFile()

    # checking if file contains object, that's id == id
    flag = True if len([el for el in fileData if el['id'] == id]) > 0 else False

    if not flag:
        fileData.append({
            'id': id,
            'score': 0,
            'likes': [],
            'comments': [],
            'reposts': [],
            'votes': [],
            'adminDecision': 0,
        })

    for oldItem in fileData:
        if id == oldItem['id']:
            if (data['key'] == 'likes') or (data['key'] == 'reposts') or (data['key'] == 'votes'):

                if not data['value'] in oldItem[data['key']]:
                    if sign == 1:
                        oldItem[data['key']].append(data['value'])
                    else:
                        print("trying to delete unexisting value")
                else:
                    if not sign == 1:
                        oldItem[data['key']].remove(data['value'])

            if data['key'] == 'comments':
                if str(data['value']) in oldItem[data['key']]:
                    if oldItem[data['key']][str(data['value'])] > 0:
                        oldItem[data['key']][str(data['value'])] += 1 * sign
                    elif sign == 1 and oldItem[data['key']][str(data['value'])] == 0:
                        oldItem[data['key']][str(data['value'])] += 1
                    else:
                        print("trying to delete unexisting value")

                else:
                    if len(oldItem[data['key']]) == 0:
                        oldItem[data['key']] = {str(data['value']): 1}
                    else:
                        oldItem[data['key']][str(data['value'])] = 1

            if data['key'] == 'adminDecision':
                print(oldItem[data['key']])
                oldItem[data['key']] += data['value'] * sign
                print(oldItem[data['key']])

            oldItem['score'] = calculateScore(oldItem)
            break

    with open('data.json', 'w') as outfile:
        json.dump(fileData, outfile)



# updateCurrentMember(170877706, {'key': 'comments', 'value': 25}, 1) #id, key of action, value to setup, sign(optional) to decrease value