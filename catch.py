# -*- coding:utf8 -*-

import hashlib
import http.cookiejar
import re
import urllib
from datetime import datetime

from mysite import app

# Configurations
BASE_URL = 'http://www.qiushibaike.com/text/'
HEAD = {
    "Accept": "text/html,application/xhtml+xml,application" +
              "/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64)" +
                  "AppleWebKit/537.36 (KHTML, like Gecko)" +
                  "Chrome/50.0.2661.102 Safari/537.36"
}
from mysite import Entries

def urlOpener(head=HEAD):
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.
                                         HTTPCookieProcessor(cj))
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    return opener


def md5(string):
    md5 = hashlib.md5(string.encode(encoding='utf8', errors='igonre'))
    return md5.hexdigest()


def stamp():
    return datetime.now()


from database.config import db_session


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


def save_data(list_obj):
    # with app.app_context():
    md5_generator = Entries.query.values(Entries.md5)
    md5_values = [row[0] for row in md5_generator]
    for e in list_obj:
        if e['md5'] in md5_values:
            continue
        entries = Entries()
        entries.title, entries.text, entries.md5, entries.stamp = e['title'], e['text'], e['md5'], e['stamp']
        db_session.add(entries)
        app.logger.info('Found data:\n%s\n%s' % (e['title'], e['text']))
    db_session.commit()

def main():
    import time
    while True:
        try:
            with app.app_context():
                app.logger.info('Five seconds after the starting fetch data from internet ...')
                time.sleep(5)
                content_pattern = re.compile('<h2>(.*?)</h2>.*?<div class="content">(.*?)</div>', re.S)
                opener = urlOpener()
                web = opener.open(BASE_URL, timeout=30)
                html = web.read().decode(encoding='utf8', errors='ignore')
                stories = []
                for e in content_pattern.finditer(html):
                    story = e.groups()
                    stories.append({'title': story[0],
                                    'text': story[1],
                                    'md5': md5(story[1]),
                                    'stamp': stamp()})
                save_data(stories)
                app.logger.info('After data has been saved, 600 seconds to fetch again.')
                time.sleep(600)
        except KeyboardInterrupt:
            opt = input('Are you sure terminate [Y/n]: ')
            if opt is '' or opt.startswith('y') or opt.startswith('Y'):
                app.logger.exception('*** Terminated by user. ***')
                exit(0)
            else:
                pass
        except:
            app.logger.exception('*** Here is a except handle ***')
            pass


if __name__ == '__main__':
    main()
