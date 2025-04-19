"""Class utilities to access to the DOM."""

import re
from collections.abc import Iterator, Sequence
from typing import TYPE_CHECKING, Literal, overload

import bs4

if TYPE_CHECKING:
    from .testclient import WebResponse, WebTestClient  # coverage: ignore


class Element:
    """Access to a dom element."""

    def __init__(self, client: "WebTestClient", tag: bs4.Tag):
        self._client = client
        self._tag = tag

    def click(self) -> "WebResponse":
        """Simulate a client to a a link. No javascript exectuted here."""
        return self._client.get(self._tag.attrs["href"])

    @property
    def node_name(self) -> str:
        """Get the node name of the dom element."""
        return self._tag.name

    @property
    def attrs(self) -> dict[str, str]:
        """Attributes of the element."""
        return self._tag.attrs

    @property
    def text(self) -> str:
        """
        Return the text of the element, with text of childs element.

        Note that the text is stripped for convenience but inner text may contains
        many spaces not manipulated here.
        """
        return self._tag.text.strip()

    @property
    def h1(self) -> "Element":
        """
        Return the h1 child element.

        Should be used on the html body element directly.
        """
        nodes = self.by_node_name("h1")
        assert len(nodes) == 1, f"Should have 1 <h1>, got {len(nodes)} in {self}"
        return nodes[0]

    @property
    def h2(self) -> Sequence["Element"]:
        """
        Return the h2 elements.
        """
        return self.by_node_name("h2")

    @property
    def form(self) -> "Element | None":
        """Get the form element of the web page."""
        return Element(self._client, self._tag.form) if self._tag.form else None

    @property
    def hx_target(self) -> str | None:
        """
        Return the hx-target of the element.

        It may be set on a parent. It also resolve special case "this" and return the id
        of the element.
        """
        el: bs4.Tag | None = self._tag
        while el:
            if "hx-target" in el.attrs:
                ret = el.attrs["hx-target"]
                if ret == "this":
                    ret = el.attrs["id"]
                return ret
            el = el.parent
        return None

    def by_text(
        self, text: str, *, node_name: str | None = None, position: int | None = None
    ) -> "Element | None":
        """Find the first element that match the text."""
        nodes = self.iter_all_by_text(text, node_name=node_name)
        ret = list(nodes)
        if not ret:
            return None
        if position is None:
            assert len(ret) == 1, f"Should have 1 element, got {len(ret)} in {self}"
        else:
            assert len(ret) > position, "Not enough element found"
        return ret[position or 0]

    def iter_all_by_text(
        self, text: str, *, node_name: str | None = None
    ) -> "Iterator[Element]":
        """Return an iterator of all elements that match the text."""
        nodes = self._tag.find_all(string=re.compile(rf"\s*{text}\s*"))
        for node in nodes:
            if isinstance(node, bs4.NavigableString):
                node = node.parent

            if node_name:
                while node is not None:
                    if node.name == node_name:
                        yield Element(self._client, node)
                    node = node.parent
            elif node:
                yield Element(self._client, node)
        return None

    def get_all_by_text(
        self, text: str, *, node_name: str | None = None
    ) -> "Sequence[Element]":
        """Return the list of all elements that match the text."""
        nodes = self.iter_all_by_text(text, node_name=node_name)
        return list(nodes)

    def by_label_text(self, text: str) -> "Element | None":
        """Return the element which is the target of the label having the given text."""
        label = self.by_text(text, node_name="label")
        assert label is not None
        assert label.attrs.get("for") is not None
        resp = self._tag.find(id=label.attrs["for"])
        assert not isinstance(resp, bs4.NavigableString)
        return Element(self._client, resp) if resp else None

    def by_id(self, id: str) -> "Element | None":
        """Find the element having the given id."""
        resp = self._tag.find_all(id=id)
        assert not isinstance(resp, bs4.NavigableString)
        if not resp:
            return None
        assert len(resp) == 1
        return Element(self._client, resp[0]) if resp else None

    @overload
    def by_node_name(
        self,
        node_name: str,
        *,
        attrs: dict[str, str] | None = None,
        multiple: Literal[False],
    ) -> "Element": ...

    @overload
    def by_node_name(
        self,
        node_name: str,
        *,
        attrs: dict[str, str] | None = None,
        multiple: Literal[True],
    ) -> "list[Element]": ...

    @overload
    def by_node_name(
        self,
        node_name: str,
        *,
        attrs: dict[str, str] | None = None,
    ) -> "list[Element]": ...

    def by_node_name(
        self,
        node_name: str,
        *,
        attrs: dict[str, str] | None = None,
        multiple: bool = True,
    ) -> "list[Element] | Element":
        """
        Return the list of elements with the given node_name.

        An optional set of attributes may given and must match if passed.
        """
        ret = [
            Element(self._client, e) for e in self._tag.find_all(node_name, attrs or {})
        ]
        if not multiple:
            assert len(ret) == 1
            return ret[0]
        return ret

    def __repr__(self) -> str:
        return f"<{self.node_name}>"

    def __str__(self) -> str:
        return str(self._tag)
