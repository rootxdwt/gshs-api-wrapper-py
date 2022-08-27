import gshs
import asyncio

wrapper = gshs.wrapper('5CACFDEA8E6954CE6251539DC49A915F')


async def getAllAuthors():
    itmList = await wrapper.searchFromPhone("01035979395")
    print(itmList)

asyncio.run(getAllAuthors())