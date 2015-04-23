#!/usr/bin/env python3
import asyncio
import logging
import sys

import chatstack


@asyncio.coroutine
def main():
    logging.basicConfig()

    import credentials
    chat_client = chatstack.Client(credentials.email, credentials.password)

    response = yield from chat_client.host('stackoverflow.com').request('')

    body = yield from response.read()

    print(body)

    return asyncio.Future()


if __name__ == '__main__':
    sys.exit(asyncio.get_event_loop().run_until_complete(main(*sys.argv[1:])))
