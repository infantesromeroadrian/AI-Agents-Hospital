from setuptools import setup, find_packages

setup(
    name="hospital_system",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'groq',
        'python-dotenv',
    ]
) 