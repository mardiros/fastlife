"""Serialize session."""
import abc
import json
from base64 import b64decode, b64encode
from typing import Any, Mapping, Tuple

import itsdangerous


class AbsractSessionSerializer(abc.ABC):
    """Session serializer base class"""

    @abc.abstractmethod
    def __init__(self, secret_key: str, max_age: int) -> None:
        ...

    @abc.abstractmethod
    def serialize(self, data: Mapping[str, Any]) -> bytes:
        """Serialize the session content to bytes in order to be saved."""
        ...

    @abc.abstractmethod
    def deserialize(self, data: bytes) -> Tuple[Mapping[str, Any], bool]:
        """Derialize the session raw bytes content and return it as a mapping."""
        ...


class SignedSessionSerializer(AbsractSessionSerializer):
    """
    The default fastlife session serializer.

    It's based on the itsdangerous package to sign the session with a secret key.

    :param secret_key: a secret used to sign the session payload.

    :param max_age: session lifetime in seconds.
    """

    def __init__(self, secret_key: str, max_age: int) -> None:
        self.signer = itsdangerous.TimestampSigner(secret_key)
        self.max_age = max_age

    def serialize(self, data: Mapping[str, Any]) -> bytes:
        """Serialize and sign the session."""
        dump = json.dumps(data).encode("utf-8")
        encoded = b64encode(dump)
        signed = self.signer.sign(encoded)
        return signed

    def deserialize(self, data: bytes) -> Tuple[Mapping[str, Any], bool]:
        """Deserialize the session.

        If the signature is incorect, the session restart from the begining.
        No exception raised.
        """
        try:
            data = self.signer.unsign(data, max_age=self.max_age)
            # We can't deserialize something wrong since the serialize
            # is signing the content.
            # If the signature key is compromise and we have invalid payload,
            # raising exceptions here is fine, it's dangerous afterall.
            session = json.loads(b64decode(data))
        except itsdangerous.BadSignature:
            return {}, True
        return session, False
