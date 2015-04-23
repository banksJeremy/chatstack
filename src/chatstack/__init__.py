import asyncio
import collections
import collections.abc

import aiohttp
import typing


class Client(collections.abc.Hashable):
    def __init__(self, email, password):
        self._hosts_by_hostname = {} # type: typing.Dict[str, Host]

    def host(self, hostname):
        if hostname not in self._hosts_by_hostname:
            self._hosts_by_hostname[hostname] = Host(self, hostname)
        return self._hosts_by_hostname[hostname]

    def __hash__(self):
        return id(self)



class Host(collections.abc.Hashable):
    def __init__(self, client:Client, hostname:str):
        self.client = client
        self.hostname = hostname

        self._rooms_by_id = {} # type: typing.Dict[str, Room]
        self._users_by_id = {} # type: typing.Dict[str, User]

    @asyncio.coroutine
    def request(self, path):
        return aiohttp.request(
            'GET', 'http://%s/%s' % (self.hostname, path))


    def room(self, id):
        if id not in self._rooms_by_id:
            self._rooms_by_id[id] = Room(self, id)
        return self._rooms_by_id[id]

    def user(self, id):
        if id not in self._users_by_id:
            self._users_by_id[id] = User(self, id)
        return self._users_by_id[id]

    def __hash__(self):
        return hash((self.client, self.hostname))

    def __eq__(self, other:'Host'):
        return (
            isinstance(other, Host) and
            self.client == other.client and
            self.hostname == other.hostname)


class Room(collections.abc.Hashable):
    def __init__(self, host:Host, id:int):
        self.host = host
        self.id = id

    def __hash__(self):
        return hash((self.host, self.id))

    def __eq__(self, other:'Room'):
        return (
            isinstance(other, Room) and
            self.host == other.host and
            self.id == other.id)


class User(collections.abc.Hashable):
    def __init__(self, host:Host, id:int):
        self.host = host
        self.id = id

    def __hash__(self):
        return hash((self.host, self.id))

    def __eq__(self, other:'User'):
        return (
            isinstance(other, User) and
            self.host == other.host and
            self.id == other.id)

