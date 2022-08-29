import gshs
import asyncio

wrapper = gshs.Wrapper("CEA0D4F7B3B57F6819D8D22045C15BFA")


async def getAllAuthors():
    itmList = await wrapper.searchFromTeacher("조")
    print(itmList)

asyncio.run(getAllAuthors())