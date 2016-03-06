import setuptools


setuptools.setup(
    version="0.0.1",
    license='mit',
    name="agr",
    author='nathan todd-stone',
    author_email='me@nathants.com',
    url='http://github.com/nathants/agr',
    packages=['agr'],
    install_requires=['argh',
                      'pager'],
    entry_points={'console_scripts': ['agr = agr:main']},
    description='agr',
)
