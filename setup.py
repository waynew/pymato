try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from ast import literal_eval
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def opener(filename):
    with Path(__file__).parent.joinpath(filename).open() as f:
        yield f

with opener('README.rst') as f:
    readme = f.read()

with opener('pymato.py') as f:
    for line in f:
        if line.startswith('__version__'):
            version = literal_eval(line.partition('=')[2].strip())

setup(
    name='pymato',
    version=version,
    description='Simple command line pomodoro timer',
    long_description=readme,
    author='Wayne Werner',
    author_email='waynejwerner@gmail.com',
    license='MIT',
    url='https://github.com/waynew/pymato',
    keywords=[
        'console',
        'countdown',
        'stopwatch',
        'terminal',
        'timer',
        'pomodoro',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console :: Curses',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Utilities',
    ],
    install_requires=[
        'pytz',
        'tzlocal',
    ],
    py_modules=['pymato'],
    entry_points={
        'console_scripts': [
            'pymato=pymato:main',
        ],
    },
)
