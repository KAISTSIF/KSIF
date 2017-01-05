from setuptools import setup

setup(
    name='KSIF',
    version='0.1.0.dev1',
    packages=['KSIF', 'KSIF.core'],
    url='',
    license='MIT',
    author='KSIF developers',
    author_email='rambor12@business.kaist.ac.kr',
    description='KSIF backtest library',
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
        'pyprind',
        'future',
        'cython',
        'tabulate',
        'sklearn',
        'scipy',
        'decorator'
    ],
    classifier=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers, Quants',
        'Topic :: Strategy Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.4',

    ]
)
