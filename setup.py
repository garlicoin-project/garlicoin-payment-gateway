from setuptools import setup, find_packages

requires = [
    'pyramid',
    'waitress',
    'sqlalchemy',
    'psycopg2',
    'pyqrcode',
]

setup(
    name='grlc',
    version='0.0',
    description='Garlicoin Payment Gateway',
    author='Joe Carey',
    author_email='joecarey001@gmail.com',
    url='https://grlc.cash',
    packages=find_packages(),
    install_requires=requires,
    entry_points='[paste.app_factory]\nmain = grlc:main\n')
