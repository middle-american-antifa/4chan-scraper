from cx_Freeze import setup, Executable

import os

os.environ['TCL_LIBRARY'] = "C:\\Users\\chan\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\chan\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tk8.6"

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [], include_files = ['tcl86t.dll', 'tk86t.dll'])

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
