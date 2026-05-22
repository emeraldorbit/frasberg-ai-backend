from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='frasberg-ai-sdk',
    version='6.0.0',
    packages=find_packages(),
    install_requires=[
        'requests>=2.28.0',
    ],
    author='Frasberg Selassie (Mr. Clayton-M. Bernard-Ex.)',
    description='Python SDK for Frasberg AI',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/emeraldorbit/frasberg-ai',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 3.11',
    ],
)
