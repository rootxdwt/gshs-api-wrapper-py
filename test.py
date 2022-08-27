import gshs
import asyncio

wrapper = gshs.Wrapper()


async def getAllAuthors():
    itmList = await wrapper.searchFromStudent("김", searchby="name")
    print(itmList)

asyncio.run(getAllAuthors())