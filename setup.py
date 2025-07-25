import setuptools


setuptools.setup(
    version="0.0.1",
    license='mit',
    name="agr",
    author='nathan todd-stone',
    author_email='me@nathants.com',
    url='http://github.com/nathants/agr',
    install_requires=['argh'],
    packages=['agr'],
    entry_points={
        'console_scripts': [
            'agr=agr.main:main',
        ],
    },
    description='agr',
)
