## Overview

Python port of Perl code from Perl Advent Calendar 2015 [Winter Platypus](http://perladvent.org/2015/2015-12-03.html) article.

## Requirements

On Fedora, requires the `python3-pyopengl` package.

On Ubuntu, requires the `python3-opengl` package.

## Troubleshooting

### "Attempt to retrieve context when no valid context" error

Setting this may work:

```shell
export PYOPENGL_PLATFORM=glx
```
