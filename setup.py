from setuptools import find_packages, setup


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="tello-sdk",
    packages=find_packages("tello_sdk"),
    version="2.4.1",
    license="MIT",
    description="Python SDK fro the Tello EDU and RMTT drones, with all commands and more.",
    author="ErnGusMik",
    author_email="ernests.mikuts@gmail.com",
    url="https://github.com/ErnGusMik/python-tello",
    download_url="https://github.com/ErnGusMik/python-tello/archive/refs/tags/v2.1.0-alpha.tar.gz",
    keywords=[
        "tello",
        "drone",
        "sdk",
        "python",
        "python3",
        "rmtt",
        "edu",
        "telloedu",
        "tello-rmtt",
        "tello-edu",
        "sdk",
    ],
    install_requires=["sentry-sdk"],
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
