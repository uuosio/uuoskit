import json
import json as json_
import httpx

from . import _uuosapi
from . import wasmcompiler
from .exceptions import ChainException

def raise_last_error():
    raise ChainException(_uuosapi.get_last_error())

def check_result(r, json=False):
    if not r:
        raise ChainException(_uuosapi.get_last_error())
    if json:
        return json_.loads(r)
    return r

class ChainNative(object):

    def get_abi_sync(self, account):
        args = {
            'account_name': account
        }
        r = httpx.post(f'{self.node_url}/v1/chain/get_abi', json=args)
        r = r.json()
        abi = r['abi']
        return json.dumps(abi)

    @staticmethod
    def n2s(n):
        '''convert integer to name string
        Example:
        ```python
            from uuoskit import uuosapi
            s = uuosapi.n2s(10927537166380695552)
            print(s)
        ```
        ```
            'myname'
        ```
        '''
        return _uuosapi.n2s(n)

    @staticmethod
    def s2n(s):
        return _uuosapi.s2n(s)

    @staticmethod
    def s2b(s):
        n = _uuosapi.s2n(s)
        return int.to_bytes(n, 8, 'little')

    @staticmethod
    def b2s(b):
        n = int.from_bytes(b, 'little')
        return _uuosapi.n2s(n)

    @staticmethod
    def string_to_symbol(precision, str_symbol):
        return _uuosapi.string_to_symbol(precision, str_symbol)

    def check_abi(self, account):
        if not _uuosapi.is_abi_cached(account):
            abi = self.get_abi_sync(account)
            _uuosapi.set_abi(account, abi)

    def pack_args(self, account, action, args):
        if isinstance(args, dict):
            args = json.dumps(args)
        else:
            assert isinstance(args, (str, bytes))

        self.check_abi(account)

        success, binargs = _uuosapi.pack_args(account, action, args)
        if not success:
            raise_last_error()
        return binargs

    def unpack_args(self, account, action, binargs, json=False):
        if isinstance(binargs, str):
            binargs = bytes.fromhex(binargs)
        else:
            assert isinstance(binargs, bytes)

        self.check_abi(account)

        success, args = _uuosapi.unpack_args(account, action, binargs)
        if not success:
            raise_last_error()
        return check_result(args, json)

    def pack_abi_type(self, account, struct_name, args):
        if isinstance(args, dict):
            args = json.dumps(args)

        self.check_abi(account)

        return _uuosapi.pack_abi_type(account, struct_name, args)

    def unpack_abi_type(self, account, struct_name, binargs):
        self.check_abi(account)
        return _uuosapi.unpack_abi_type(account, struct_name, binargs)

    @staticmethod
    def clear_abi_cache(account):
        return _uuosapi.clear_abi_cache(account)

    @staticmethod
    def set_abi(account, abi):
        ret = _uuosapi.set_abi(account, abi)
        return check_result(ret)

    @staticmethod
    def pack_abi(abi):
        if isinstance(abi, dict):
            abi = json.dumps(abi)
        return _uuosapi.pack_abi(abi)

    @staticmethod
    def unpack_abi(packed_abi):
        return _uuosapi.unpack_abi(packed_abi)

    def gen_transaction(self, actions, expiration, reference_block_id, json=False):
        for a in actions:
            args = a[2]
            if isinstance(args, dict):
                a[2] = self.pack_args(a[0], a[1], args)
        r = _uuosapi.gen_transaction(actions, expiration, reference_block_id)
        return check_result(r, json)

    def generate_transaction(self, actions, expiration, reference_block_id, json=False):
        return self.gen_transaction(actions, expiration, reference_block_id, json)

    @staticmethod
    def sign_transaction(trx, private_key, chain_id, json=False):
        if isinstance(trx, dict):
            trx = json_.dumps(trx)
        ret = _uuosapi.sign_transaction(trx, private_key, chain_id)
        return check_result(ret, json)

    @staticmethod
    def pack_transaction(trx, compress=0, json=False):
        if isinstance(trx, dict):
            trx = json_.dumps(trx)
        assert isinstance(trx, (dict, str, bytes))
        ret = _uuosapi.pack_transaction(trx, compress)
        return check_result(ret, json)

    @staticmethod
    def unpack_transaction(trx, json=False):
        if isinstance(trx, str):
            trx = bytes.fromhex(trx)
        assert isinstance(trx, bytes)
        ret = _uuosapi.unpack_transaction(trx)
        return check_result(ret)

    @staticmethod
    def create_key():
        return _uuosapi.create_key()

    @staticmethod
    def get_public_key(priv):
        return _uuosapi.get_public_key(priv)

    @staticmethod
    def from_base58(pub_key):
        return _uuosapi.from_base58(pub_key)

    @staticmethod
    def to_base58(raw_pub_key):
        return _uuosapi.to_base58(raw_pub_key)

    @staticmethod
    def recover_key(digest, sign):
        ret = _uuosapi.recover_key(digest, sign)
        return check_result(ret)

    @staticmethod
    def pack_cpp_object(obj_type, json_str):
        return _uuosapi.pack_cpp_object(obj_type, json_str)

    @staticmethod
    def unpack_cpp_object(obj_type, raw_data):
        return _uuosapi.unpack_cpp_object(obj_type, raw_data)

    @staticmethod
    def sign_digest(priv_key, digest):
        if isinstance(digest, str):
            if not len(digest) == 64:
                raise Exception('digest should be a hex str with 64 charactors or a bytes with a size of 32 long')
            digest = bytes.fromhex(digest)
        elif isinstance(digest, bytes):
            if not len(digest) == 32:
                raise Exception('digest should be a hex str with 64 charactors or a bytes with a size of 32 long')
        else:
            raise TypeError('digest should be a hex str with 64 charactors or a bytes with a size of 32 long')
        return _uuosapi.sign_digest(priv_key, digest)

    @staticmethod
    def set_public_key_prefix(prefix):
        _uuosapi.set_public_key_prefix(prefix)

    @staticmethod
    def get_public_key_prefix():
        return _uuosapi.get_public_key_prefix()

    @staticmethod
    def mp_compile(contract, src):
        return _uuosapi.compile_py(contract, src)

    def mp_make_frozen(self, code):
        mpy_code = ((code, len(code)),)

        code_region = b''
        code_size_region = b''
        for code, size in mpy_code:
            code_region += code
            code_size_region += int.to_bytes(size, 4, 'little')

        name_region = b'main.mpy\x00'

        region_sizes = b''
        region_sizes += int.to_bytes(len(name_region), 4, 'little')
        region_sizes += int.to_bytes(len(code_size_region), 4, 'little')
        region_sizes += int.to_bytes(len(code_region), 4, 'little')

        header = int.to_bytes(5, 4, 'little')
        header += bytearray(60)
        frozen_code = header + region_sizes + name_region + code_size_region + code_region
        return frozen_code

    def compile(self, contract_name, code, vm_type):
        if vm_type == 0:
            return wasmcompiler.compile_cpp_src(contract_name, code)
        elif vm_type == 1:
            code = self.mp_compile(contract_name, code)
            assert code
            return self.mp_make_frozen(code)
        else:
            assert 0, f'unsupported vm type: {vm_type}'

    @staticmethod
    def get_last_error():
        return _uuosapi.get_last_error()
