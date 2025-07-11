from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="YtubeData",
    version="1.0.0",
    author="Sayers Linux",
    author_email="sayerlinux@gmail.com",
    description="أداة قوية لاستخراج البيانات الوصفية من يوتيوب",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/YtubeData",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "ytubedata=YtubeData:main",
        ],
    },
)