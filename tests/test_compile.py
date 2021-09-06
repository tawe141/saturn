import pytest
from saturn.compile import *
import os
import glob


def test_to_html():
    if os.path.isfile('site/home.html'):
        os.remove('site/home.html')
    convert_ipynb_to_html('notebooks/home.ipynb')
    assert os.path.isfile('site/home.html')


def test_compile_all():
    compile_notebooks(force=True)
    htmls = glob.glob('site/**/*.html', recursive=True)
    ipynbs = glob.glob('notebooks/**/*.ipynb', recursive=True)
    assert len(htmls) == len(ipynbs)
    assert os.path.isfile('ipynb_mtimes.json')
