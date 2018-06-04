from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('scraper.py', base=base, targetName = 'meme-scraper')
]

setup(name='meme-scraper',
      version = '0.1',
      description = 'Scrape memes from 4chan.',
      options = dict(build_exe = buildOptions),
      executables = executables)
