import asyncio

from errors.db_errors import DidntFindOneError


def loop(func):
    def wrapper(*args, **kwargs):
        print('start')
        my_loop = asyncio.get_event_loop()
        my_loop.run_until_complete(func(*args, **kwargs))
        print('end')
    return wrapper


@loop
async def do_insert_one(collection, data):
    result = await collection.insert_one(data)
    print('result inserted %s' % repr(result.inserted_id))
    return 'result inserted %s' % repr(result.inserted_id)


@loop
async def do_find_one(collection, data):
    try:
        result = await collection.find_one(data)
    except DidntFindOneError:
        ex = DidntFindOneError(f'Не удалось найти элемент в базе {collection} - {data}')
        print(ex)
        result = None
    print('result founded %s' % result)
    return result


@loop
async def do_update_one(collection, data):
    result = await collection.update_one(data[0], data[1])
    print('result updated %s' % result)


@loop
async def do_update_many(collection, data):
    result = await collection.update_many(data[0], data[1])
    print('result updated many %s' % result)


@loop
async def do_delete_one(collection, data):
    result = await collection.delete_one(data)
    print('result deleted %s' % result)


@loop
async def do_delete_many(collection, data):
    result = await collection.delete_many(data)
    print('result deleted many %s' % result)
