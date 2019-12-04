import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


cwd = os.path.abspath(os.path.dirname(__file__))
os.chdir(cwd)

version_contents = {}
with open(os.path.join(cwd, 'rocketreach', 'version.py')) as f:
    exec(f.read(), version_contents)


with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='rocketreach',
    version=version_contents['VERSION'],
    packages=['rocketreach', ],
    url='https://rocketreach.co',
    author='RocketReach',
    author_email='engineering@rocketreach.co',
    description='Python bindings for RocketReach API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.4, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    install_requires=['requests>=2.2', ],
    project_urls={
        'Documentation': 'https://rocketreach.co/api',
        'Source Code': 'https://github.com/rocketreach/rocketreach_python',
    },
)
