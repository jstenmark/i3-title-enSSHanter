from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='i3-title-enSSHanter',
    version='1.0.0',
    description='Automatically update the i3wm window title when establishing an SSH connection through a shell.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='JStenmark',
    author_email='johannes@stenmark.in',
    url='https://github.com/jstenmark/i3-title-ensshanter',
    packages=['i3_ssh_title_updater'],
    license='MIT',
    install_requires=[
        'i3ipc==2.2.1',
        'python-xlib==0.33',
        'six==1.16.0',
        'webcolors==1.13',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
    ],
)
