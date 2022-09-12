import datetime
from index import datetimeToIndex, dayToIndexRatio, startIndex, indexToDatetime

def correct_datetime(datetime):
    date, time = datetime.split(" ")
    try:
        hour, minute, second = time.split(":")
    except:
        hour, minute = time.split(":")
        second = "00"
    month, day, year = date.split("-")

    if int(month) > 12:
        # probably year, month, day
        year1 = month
        month1 = day
        day1 = year

        year = year1
        month = month1
        day = day1

    if len(year) == 4:
        year = year[-2:]

    return year, month, day, hour, minute, second

def getIndexList():
    # go from the start date to now
    # gets today's datetime
    now = str(datetime.datetime.now())
    date, time = now.split(" ")
    year, month, day = date.split("-")
    year = year[2:]
    hour, minute, second = time.split(":")
    second = second[:2]

    # gives todays date a value, or endIndex number
    endIndex = datetimeToIndex(year, month, day, hour, minute, second)
    endIndex = round(endIndex / dayToIndexRatio) * dayToIndexRatio

    # calculates the number of entries (numIndices) since the project start date
    diff = endIndex - startIndex
    numIndices = diff / dayToIndexRatio

    # creates the indexList by multiplying the ith entry by the dayToIndexRatio one by one and making the list.
    indexList = []
    for i in range(0, int(numIndices)):
        newVal = startIndex + (i * dayToIndexRatio)
        indexList.append(newVal)

    return indexList

def getDateList(indexList):
    startYear = 18
    dateList = []
    # Takes indexList and applies a datetime to each of the index values, starts at 10/1/18(m:d:y) and adds on 15min intervals
    for index in indexList:
        year, month, day, hour, minute, second = indexToDatetime(index, startYear)
        datetime = str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + str(minute) + ":" + str(
            second)
        dateList.append(datetime)
    return dateList

def joinDict(dict1, dischargeDfDict):
    indexToDayRatio = 4 * 24
    # Joins all of the cursor data to the ongoing dataframe sent in with it.
    dataNames = dict1.keys()
    for name in dataNames:
        if name == "index" or name == "datetime":
            pass

        elif name == "batch_id" and "batch_id" in dischargeDfDict.keys() and len(dischargeDfDict["batch_id"]) == len(
                dischargeDfDict["index"]):
            pass

        else:
            dataList = dict1[name]
            indices = dict1["index"]
            dtime = dict1["datetime"]
            newData = [None] * len(dischargeDfDict["index"])
            # print(fullDict["datetime"][-5:])
            for i in range(len(indices)):
                index = indices[i]
                listIndex = round(index * indexToDayRatio)

                data = dataList[i]
                dt = dtime[i]
                newData[listIndex] = data

            dischargeDfDict[name] = newData
    return dischargeDfDict
