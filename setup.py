try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def trim_comment(line):
    i = line.find('#')
    if i >= 0:
        line = line[:i]
    return line.strip()

def load_reqs(filename):
    with open(filename) as info:
        return [trim_comment(line) for line in info if trim_comment(line)]


setup(
    name='celstash',
    version='0.1.0',
    description='log from celery to logstash and structured log',
    long_description=open('README.md').read(),
    author='CyberInt',
    author_email='tools@cyberint.com',
    license='MIT',
    url='https://github.com/CyberInt/celstash',
    py_modules=['celstash'],
    install_requires=load_reqs('requirements.txt'),
    tests_require=load_reqs('test-requirements.txt'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
