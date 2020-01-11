from setuptools import find_packages, setup


VERSION = {}
with open("logexp/version.py", "r") as version_file:
    exec(version_file.read(), VERSION)

setup(
    name="logexp",
    version=VERSION["VERSION"],
    author="altescy",
    author_email="altescy@fastmail.com",
    description="simple experiment manager for machine learning.",
    keywords="machine learning experiment manager",
    url="https://github.com/altescy/logexp",
    license='MIT License',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            "logexp=logexp.cli:main"
        ]
    },
    tests_require=["pytest"],
    python_requires=">=3.7.3",
)
