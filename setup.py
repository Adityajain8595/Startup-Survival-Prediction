from setuptools import setup, find_packages
from typing import List

def get_requirements()->List[str]:
    """
    This function returns a list of requirements for the package.
    It reads from a 'requirements.txt' file and returns the list of packages.
    """
    requirements_list = []
    try:
        with open('requirements.txt', 'r') as file:
            requirements = file.readlines()
            for req in requirements:
                req = req.strip()
                #ignore empty lines and -e
                if req and req != '-e .':
                    requirements_list.append(req)
    except FileNotFoundError:
        return "requirements file not found!"
    return requirements_list

setup(
    name="Startup Survival Prediction",
    version="0.0.1",
    author="Aditya Jain",
    author_email="meaditya1103@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)