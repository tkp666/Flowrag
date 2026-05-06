import asyncio
async def foo():
    print("foo body")
    return 123


async def main():
    x = foo()
    print("x = ", x)
    result = await x
    print("result = ", result)
    
asyncio.run(main())