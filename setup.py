from setuptools import setup, find_packages

setup(
    name='bloomfilter',
    version = '0.0.1',
    description='low level functional bloomfilter',
    url='https://github.com/tommyvn/bloomfilter',
    author='Tom van Neerijnen',
    author_email='tom@tomvn.com',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=[],
    keywords='bloomfilter',
    license='Apache',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
    ],
)
