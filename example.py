"""
example.py
~~~~~~~~~~

This file contains an example script using the library. It creates a single ipset
with no elements.

It exists as a manual verification step while this library is under development.
"""
from ipset.lib import ffi, C

def main():
    C.ipset_load_types()

    session = C.ipset_session_init(C.printf)
    C.ipset_envopt_parse(session, C.IPSET_ENV_EXIST, ffi.NULL)

    rc = C.ipset_data_set(C.ipset_session_data(session), C.IPSET_SETNAME, "test")
    assert rc == 0

    C.ipset_data_set(C.ipset_session_data(session), C.IPSET_OPT_TYPENAME, "hash:net")

    t = C.ipset_type_get(session, C.IPSET_CMD_CREATE)

    C.ipset_data_set(C.ipset_session_data(session), C.IPSET_OPT_TYPE, t)
    family = ffi.new("int *", C.NFPROTO_IPV4)

    C.ipset_data_set(C.ipset_session_data(session), C.IPSET_OPT_FAMILY, family)

    rc = C.ipset_cmd(session, C.IPSET_CMD_CREATE, 0)
    assert rc == 0

    C.ipset_session_fini(session)

main()
