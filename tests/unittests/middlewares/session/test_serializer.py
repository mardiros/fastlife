from base64 import b64decode, b64encode

from fastlife.middlewares.session.serializer import SignedSessionSerializer


def test_serializer():
    srlz = SignedSessionSerializer("secret", 10)
    s = srlz.serialize({"foo": "bar"})
    assert b"." in s
    payload = s.split(b".")[0]
    assert b64decode(payload) == b'{"foo": "bar"}'
    assert srlz.deserialize(s) == ({"foo": "bar"}, False)


def test_serializer_signature_failed():
    srlz = SignedSessionSerializer("secret", 10)
    data = srlz.serialize({"foo": "bar"})
    payload, bsignature = data.split(b".", maxsplit=1)
    assert b"." in data
    payload = b64encode(b'{"foo": "baz"}').decode("utf-8")
    signature = bsignature.decode("utf-8")
    assert srlz.deserialize(f"{payload}.{signature}".encode()) == ({}, True)
