from setuptools import setup, find_packages

REQUIREMENTS = [
    'setuptools',
    'pyserial',
    'progressbar2',
]


setup(
    name='py_ASA_loader',
    version='0.1.0',
    description = 'The program to load binary into ASA series board.',
    long_description='',
    author = 'mickey9910326',
    author_email = 'mickey9910326@gmail.com',
    url='https://pypi.org/py_ASA_loader',
    license = 'MIT',
    packages=find_packages(),
    zip_safe=False,
    entry_points = {
        'console_scripts': [
            'asaloader = py_asa_loader.__main__:run',
        ],
    },
    install_requires=REQUIREMENTS
)
