#!/usr/bin/env python

import os
import json
try:
    import urllib.request
except:
    import urllib
    urllib.request = urllib

BASE_URL = 'https://a.4cdn.org/'
IMAGE_URL = 'https://i.4cdn.org/'

_THREAD_URL = None
_SAVE_DIR = './'


def get_image_urls_from_thread(thread_path):
    '''
    Args:
        thread_path: Part of a 4chan url containing the the board, thread,
            and thread_id as a string.
    Returns:
        A list of tuples of the form: (image_url, image_name)
    '''
    images = []
    partial_image_url = os.path.join(IMAGE_URL, thread_path.split('/')[0])
    partial_data_url = os.path.join(BASE_URL, thread_path.split('/')[0])
    thread_no = ''
    for char in thread_path.split('/')[-1]:
        if not char.isdigit():
            break
        thread_no += char
    data_url = os.path.join(partial_data_url, 'thread', thread_no + '.json')
    print('fetching ' + data_url)
    t = urllib.request.urlopen(data_url).read()
    print('fetched ' + data_url)
    t_data = json.loads(t)
    for p in t_data['posts']:
        if not p.get('tim') or not p.get('ext') or not p.get('filename'):
            continue
        i_url = os.path.join(partial_image_url, '{tim}{ext}'.format(**p))
        i_name = '{filename}{ext}'.format(**p).replace(' ', '_')
        images.append((i_url, i_name))
    return images


def fetch_and_store_images(images, save_dir):
    for image in images:
        i_url, i_name = image
        pathname = os.path.join(save_dir, i_name)
        if os.path.exists(pathname):
            yield pathname
        else:
            i_data = urllib.request.urlopen(i_url).read()
            with open(pathname, 'wb') as out:
                out.write(i_data)
            yield pathname


if __name__ == '__main__':
    import appJar
    import threading

    _STATUS = ''
    _PROGRESS = 0

    def run(thread_url, save_dir):
        global _STATUS
        global _PROGRESS

        _PROGRESS = 0
        _STATUS = ''

        if '://boards.4chan.org/' not in thread_url:
            _STATUS = '{} doesn\'t look like a valid url.'.format(thread_url)
            return

        thread_path = thread_url.split('/')[-3:]
        if len(thread_path) < 2:
            _STATUS = '"{}" doesn\'t look like a valid url.'.format(thread_url)
            return

        try:
            thread_path = '/'.join(thread_path)
            _STATUS = 'pulling thread data....'
            images = get_image_urls_from_thread(thread_path)
            image_count = len(images)

            _STATUS = '\nfound {} dank maymays'.format(image_count)
            _PROGRESS = 5

            fetcher = fetch_and_store_images(images, save_dir)
            count = 0
            for pathname in fetcher:
                count += 1
                _STATUS = '\nsaved {}/{} : {}'.format(count, image_count, pathname)
                _PROGRESS = 5 + (95 * count / image_count)
                print(_STATUS)

            _STATUS = 'completed thread: {}'.format(thread_url)
        except Exception as e:
            _STATUS = str(e)

    def update_status():
        app.clearMessage('status')
        app.setMessage('status', _STATUS)

    def update_progress():
        app.setMeter('progress', _PROGRESS)

    def scrape():
        thread_url = app.entry("thread url")
        save_dir = app.entry("save directory")
        t = threading.Thread(target=run, args=(thread_url, save_dir))
        t.start()

    app = appJar.gui('dank maymays', '800x600')
    app.setFont(18)
    app.addLabel('title', '4chan meme scraper')
    app.setLabelBg('title', 'green')
    app.addLabelEntry('thread url')
    app.addDirectoryEntry('save directory')
    app.buttons(["start scraping", "quit"], [scrape, app.stop])
    app.addEmptyMessage('status')
    app.setMessageWidth('status', 800)
    app.addMeter('progress')
    app.registerEvent(update_status)
    app.registerEvent(update_progress)
    app.go()
