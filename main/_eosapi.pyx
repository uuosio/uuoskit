# cython: c_string_type=str, c_string_encoding=ascii

from cython.operator cimport dereference as deref, preincrement as inc
from libcpp.string cimport string
from libcpp.vector cimport vector
from libcpp.map cimport map
from libcpp cimport bool

import json

cdef extern from * :
    ctypedef long long int64_t
    ctypedef unsigned long long uint64_t

cdef extern from "eosapi.hpp":
    void pack_args_(string& rawabi, uint64_t action, string& _args, string& binargs)
    void unpack_args_(string& rawabi, uint64_t action, string& binargs, string& _args)
    uint64_t s2n_(string& s);
    void n2s_(uint64_t n, string& s);

    void memcpy(char* dst, char* src, size_t len)

    cdef cppclass permission_level:
        permission_level()
        uint64_t    actor
        uint64_t permission

    cdef cppclass action:
        action()
        uint64_t                    account
        uint64_t                    name
        vector[permission_level]    authorization
        vector[char]                data

    object gen_transaction_(vector[action]& v, int expiration, string& reference_block_id);

account_abi = {}

def N(string& s):
    return s2n_(s)

def s2n(string& s):
    return s2n_(s)

def n2s(uint64_t n):
    cdef string s
    n2s_(n, s)
    return s

def set_abi(account, abi):
    account_abi[account] = abi

def pack_args(string& rawabi, action, _args):
    cdef string binargs
    cdef string args
    args = json.dumps(_args)
    pack_args_(rawabi, N(action), args, binargs)
    return <bytes>binargs

def unpack_args(string& rawabi, action, string& binargs):
    cdef string _args
    unpack_args_(rawabi, N(action), binargs, _args)
    return json.loads(_args)

def gen_transaction(actions, int expiration, string& reference_block_id):
    cdef vector[action] v
    cdef action act
    cdef permission_level per
    cdef vector[permission_level] pers

    v = vector[action]()
    for a in actions:
        act = action()
        account = a[0]
        action_name = a[1]
        act.account = s2n(account)
        act.name = s2n(action_name)
        pers = vector[permission_level]()
        for auth in a[3]:
            per = permission_level()
            per.actor = s2n(auth)
            per.permission = s2n(a[3][auth])
            pers.push_back(per)
        act.authorization = pers
        act.data.resize(0)
        act.data.resize(len(a[2]))
        if isinstance(a[2], dict):
            if not account in account_abi:
                raise Exception('no abi specified!')
            abi = account_abi[account]
            pack_args(abi, action_name, a[2])
        else:
            memcpy(act.data.data(), a[2], len(a[2]))
        v.push_back(act)

    return gen_transaction_(v, expiration, reference_block_id)
