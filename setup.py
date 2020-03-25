import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

dependencies = ['aiofiles', 'aiosqlite']
test_deps = ['pytest']

setuptools.setup(
    name="nanodelta",
    version="0.0.9",
    author="Berry Langerak",
    author_email="berry.langerak@gmail.com",
    description="Nanodelta is a simple package to run deltas on an SQLite database asynchronously. It depends on aiosqlite.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/berry-langerak/nanodelta",
    packages=['nanodelta'],
    install_requires=dependencies,
    tests_require=test_deps,
    extras_require={
        'test': test_deps
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
    ],
    python_requires='>=3.6',
)