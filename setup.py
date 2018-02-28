try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.rst') as f:
    readme = f.read()

setup(
    name='pymato',
    version='0.1.4',
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
