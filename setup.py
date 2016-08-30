try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from distutils.errors import DistutilsSetupError

DESCRIPTION = 'ome_seadragon_cache: A cache mechanism for tiles and thumbnails that can be used with both' \
              ' ome_seadragon and ome_seadragon_gateway'

AUTHOR_INFO = [
    ('Luca Lianas', 'luca.lianas@crs4.it')
]
MAINTAINER_INFO = AUTHOR_INFO
AUTHOR = '', ''.join(t[0] for t in AUTHOR_INFO)
AUTHOR_EMAIL = '', ''.join('<%s>' % t[1] for t in AUTHOR_INFO)
MAINTAINER = ", ".join(t[0] for t in MAINTAINER_INFO)
MAINTAINER_EMAIL = ", ".join("<%s>" % t[1] for t in MAINTAINER_INFO)
URL = 'https://github.com/lucalianas/pyBaseX'
DOWNLOAD_URL = 'https://github.com/lucalianas/pyBaseX/releases'

try:
    with open("NAME") as f:
        NAME = f.read().strip()
    with open("VERSION") as f:
        VERSION = f.read().strip()
except IOError:
    raise DistutilsSetupError("failed to read name/version info")

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    download_url=DOWNLOAD_URL,
    license='MIT License',
    platforms=['any'],
    keywords=['ome_seadraon', 'Redis', 'cache', 'python'],
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
    ],
    packages=[
        'ome_seadragon_cache'
    ],
    requires=[
        'setuptools',
        'redis',
        'Pillow',
    ],
    install_requires=[
        'setuptools',
        'redis',
        'Pillow',
    ]
)
