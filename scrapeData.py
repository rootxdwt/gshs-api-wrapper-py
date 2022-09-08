import gshs
import asyncio

f = open("sessionKey.txt", "r")
token = f.read()

wrapper = gshs.Wrapper(token)

obj={}

async def getAllAuthors():
    itmList = await wrapper.getMissingItemList()
    grdlst = [0]*3
    classlst=[0]*8
    for item in itmList:
        monthYear = item.date.split(".")[0]+"-"+item.date.split(".")[1]
        obj[monthYear] = 1 if monthYear not in obj else obj[monthYear]+1
        if item.type=="lost":
            try:
                if item.author.type=="student":
                    studentData = await wrapper.searchFromStudent(item.author.name, searchby="name")
                    grade = studentData[0].year
                    grdlst[int(grade)-1]+=1
                    if int(grade)==1:
                        _class = studentData[0]._class
                        classlst[int(_class) - 1]+=1
                    await asyncio.sleep(0.2)
            except:
                    pass
    print(grdlst, classlst)
    print(obj)

asyncio.run(getAllAuthors())