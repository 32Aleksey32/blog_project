from setuptools import find_packages, setup


REQUIRES = [
    'pip==24.0',
    'Django==5.0.7',
    'psycopg2-binary==2.9.9',
    'djangorestframework==3.15.2',
]

setup(
    name='blog_project',
    packages=find_packages(),
    install_requires=REQUIRES
)
