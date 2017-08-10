import setuptools

setuptools.setup(
    name='Pynome',
    author='Tyler Biggs',
    author_email='biggstd@gmail.com',
    version='0.1.0',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'pynome = pynome.__main__:main'
        ]
    },
)
