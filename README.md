Python Toolkit for EOSIO

<h3>
  <a
    target="_blank"
    href="https://mybinder.org/v2/gh/uuosio/UUOSKit/master?filepath=notebooks%2Fhelloworld.ipynb"
  >
    Quick Start
    <img alt="Binder" valign="bottom" height="25px"
    src="https://mybinder.org/badge_logo.svg"
    />
  </a>
</h3>

# Latest Release

[uuoskit v0.8.3](https://github.com/uuosio/uuoskit/releases)

# [Docs](https://uuosio.github.io/UUOSKit)

# Building from Source Code

### Installing Prerequirements(macOS X and linux)

```
python3 -m pip install scikit-build
python3 -m pip install cython==0.28.5
```

### Downloading Source Code

```
git clone https://www.github.com/uuosio/uuoskit
cd uuoskit
git submodule update --init --recursive
```

### Building on macOS
```
./build-mac.sh
```

### Building on Ubuntu
```
./build-linux.sh
```

### Building on Centos
```
CC=gcc CXX=g++ python3 setup.py sdist bdist_wheel  -- -DCMAKE_TOOLCHAIN_FILE=$(pwd)/cmake/polly/gcc-pic.cmake -- -j7
```

### Installation

```
ls dist
python3 -m pip install dist/uuoskit-[SUFFIX].whl
```

### Example1
```python
import os
from uuoskit import uuosapi, wallet

if os.path.exists('mywallet.wallet'):
    os.remove('mywallet.wallet')
psw = wallet.create('mywallet')
#import your account private key here
wallet.import_key('mywallet', '5K463ynhZoCDDa4RDcr63cUwWLTnKqmdcoTKTHBjqoKfv4u5V7p')

uuosapi.set_node('https://eos.greymass.com')
info = uuosapi.get_info()
print(info)
args = {
    'from': 'test1',
    'to': 'test2',
    'quantity': '1.0000 EOS',
    'memo': 'hello,world'
}
uuosapi.push_action('eosio.token', 'transfer', args, {'test1':'active'})
```

### Async Example
```python
import os
import asyncio
from uuoskit import wallet
from uuoskit.chainapi import ChainApiAsync

if os.path.exists('mywallet.wallet'):
    os.remove('mywallet.wallet')
psw = wallet.create('mywallet')
#import your account private key here
wallet.import_key('mywallet', '5K463ynhZoCDDa4RDcr63cUwWLTnKqmdcoTKTHBjqoKfv4u5V7p')

async def test():
    uuosapi = ChainApiAsync('https://eos.greymass.com')
    info = await uuosapi.get_info()
    print(info)
    args = {
        'from': 'test1',
        'to': 'test2',
        'quantity': '1.0000 EOS',
        'memo': 'hello,world'
    }
    r = await uuosapi.push_action('eosio.token', 'transfer', args, {'test1':'active'})
    print(r)

asyncio.run(test())
```

### License
[MIT](./LICENSE)
