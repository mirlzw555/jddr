# -*- coding: utf8 -*-  
import asyncio
from pyppeteer import launch
from pyquery import PyQuery as pq


# ------------------------------------------------------------------------------------------
def count(n):
    while n > 0:
        print('before yield')
        yield n
        n -= 1
        print('after yield')

g = count(5)

print(g.send(None))
print(next(g))

#for i in g:
    #print(i)
# ------------------------------------------------------------------------------------------
#async def main():
    #br = await launch()
    #page = await br.newPage()
    #await page.goto('http://quotes.toscrape.com/js/')
    # #await page.goto('https://www.baidu.com/')
    #doc = pq(await page.content())
    #print('Quotes:', doc('.quote').length)
    #await br.close()
#asyncio.get_event_loop().run_until_complete(main())

# ------------------------------------------------------------------------------------------

