# {py:mod}`fastlife.testing.testclient`

```{py:module} fastlife.testing.testclient
```

```{autodoc2-docstring} fastlife.testing.testclient
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`Element <fastlife.testing.testclient.Element>`
  - ```{autodoc2-docstring} fastlife.testing.testclient.Element
    :summary:
    ```
* - {py:obj}`WebForm <fastlife.testing.testclient.WebForm>`
  - ```{autodoc2-docstring} fastlife.testing.testclient.WebForm
    :summary:
    ```
* - {py:obj}`WebResponse <fastlife.testing.testclient.WebResponse>`
  - ```{autodoc2-docstring} fastlife.testing.testclient.WebResponse
    :summary:
    ```
* - {py:obj}`Session <fastlife.testing.testclient.Session>`
  - ```{autodoc2-docstring} fastlife.testing.testclient.Session
    :summary:
    ```
* - {py:obj}`WebTestClient <fastlife.testing.testclient.WebTestClient>`
  - ```{autodoc2-docstring} fastlife.testing.testclient.WebTestClient
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`CookieTypes <fastlife.testing.testclient.CookieTypes>`
  - ```{autodoc2-docstring} fastlife.testing.testclient.CookieTypes
    :summary:
    ```
* - {py:obj}`Cookies <fastlife.testing.testclient.Cookies>`
  - ```{autodoc2-docstring} fastlife.testing.testclient.Cookies
    :summary:
    ```
````

### API

````{py:data} CookieTypes
:canonical: fastlife.testing.testclient.CookieTypes
:value: >
   None

```{autodoc2-docstring} fastlife.testing.testclient.CookieTypes
```

````

````{py:data} Cookies
:canonical: fastlife.testing.testclient.Cookies
:value: >
   None

```{autodoc2-docstring} fastlife.testing.testclient.Cookies
```

````

`````{py:class} Element(client: fastlife.testing.testclient.WebTestClient, tag: bs4.Tag)
:canonical: fastlife.testing.testclient.Element

```{autodoc2-docstring} fastlife.testing.testclient.Element
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.testing.testclient.Element.__init__
```

````{py:method} click() -> fastlife.testing.testclient.WebResponse
:canonical: fastlife.testing.testclient.Element.click

```{autodoc2-docstring} fastlife.testing.testclient.Element.click
```

````

````{py:property} node_name
:canonical: fastlife.testing.testclient.Element.node_name
:type: str

```{autodoc2-docstring} fastlife.testing.testclient.Element.node_name
```

````

````{py:property} attrs
:canonical: fastlife.testing.testclient.Element.attrs
:type: dict[str, str]

```{autodoc2-docstring} fastlife.testing.testclient.Element.attrs
```

````

````{py:property} text
:canonical: fastlife.testing.testclient.Element.text
:type: str

```{autodoc2-docstring} fastlife.testing.testclient.Element.text
```

````

````{py:property} h1
:canonical: fastlife.testing.testclient.Element.h1
:type: fastlife.testing.testclient.Element

```{autodoc2-docstring} fastlife.testing.testclient.Element.h1
```

````

````{py:property} h2
:canonical: fastlife.testing.testclient.Element.h2
:type: typing.Sequence[fastlife.testing.testclient.Element]

```{autodoc2-docstring} fastlife.testing.testclient.Element.h2
```

````

````{py:property} form
:canonical: fastlife.testing.testclient.Element.form
:type: Element | None

```{autodoc2-docstring} fastlife.testing.testclient.Element.form
```

````

````{py:property} hx_target
:canonical: fastlife.testing.testclient.Element.hx_target
:type: typing.Optional[str]

```{autodoc2-docstring} fastlife.testing.testclient.Element.hx_target
```

````

````{py:method} by_text(text: str, *, node_name: str | None = None) -> Element | None
:canonical: fastlife.testing.testclient.Element.by_text

```{autodoc2-docstring} fastlife.testing.testclient.Element.by_text
```

````

````{py:method} iter_all_by_text(text: str, *, node_name: str | None = None) -> Iterator[Element]
:canonical: fastlife.testing.testclient.Element.iter_all_by_text

```{autodoc2-docstring} fastlife.testing.testclient.Element.iter_all_by_text
```

````

````{py:method} get_all_by_text(text: str, *, node_name: str | None = None) -> Sequence[Element]
:canonical: fastlife.testing.testclient.Element.get_all_by_text

```{autodoc2-docstring} fastlife.testing.testclient.Element.get_all_by_text
```

````

````{py:method} by_label_text(text: str) -> Element | None
:canonical: fastlife.testing.testclient.Element.by_label_text

```{autodoc2-docstring} fastlife.testing.testclient.Element.by_label_text
```

````

````{py:method} by_node_name(node_name: str, *, attrs: dict[str, str] | None = None) -> list[fastlife.testing.testclient.Element]
:canonical: fastlife.testing.testclient.Element.by_node_name

```{autodoc2-docstring} fastlife.testing.testclient.Element.by_node_name
```

````

````{py:method} __repr__() -> str
:canonical: fastlife.testing.testclient.Element.__repr__

````

````{py:method} __str__() -> str
:canonical: fastlife.testing.testclient.Element.__str__

````

`````

`````{py:class} WebForm(client: fastlife.testing.testclient.WebTestClient, origin: str, form: fastlife.testing.testclient.Element)
:canonical: fastlife.testing.testclient.WebForm

```{autodoc2-docstring} fastlife.testing.testclient.WebForm
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.testing.testclient.WebForm.__init__
```

````{py:method} set(fieldname: str, value: str) -> typing.Any
:canonical: fastlife.testing.testclient.WebForm.set

```{autodoc2-docstring} fastlife.testing.testclient.WebForm.set
```

````

````{py:method} unset(fieldname: str, value: str) -> typing.Any
:canonical: fastlife.testing.testclient.WebForm.unset

```{autodoc2-docstring} fastlife.testing.testclient.WebForm.unset
```

````

````{py:method} select(fieldname: str, value: str) -> typing.Any
:canonical: fastlife.testing.testclient.WebForm.select

```{autodoc2-docstring} fastlife.testing.testclient.WebForm.select
```

````

````{py:method} unselect(fieldname: str, value: str) -> typing.Any
:canonical: fastlife.testing.testclient.WebForm.unselect

```{autodoc2-docstring} fastlife.testing.testclient.WebForm.unselect
```

````

````{py:method} button(text: str, position: int = 0) -> fastlife.testing.testclient.WebForm
:canonical: fastlife.testing.testclient.WebForm.button

```{autodoc2-docstring} fastlife.testing.testclient.WebForm.button
```

````

````{py:method} submit(follow_redirects: bool = True) -> fastlife.testing.testclient.WebResponse
:canonical: fastlife.testing.testclient.WebForm.submit

```{autodoc2-docstring} fastlife.testing.testclient.WebForm.submit
```

````

````{py:method} __contains__(key: str) -> bool
:canonical: fastlife.testing.testclient.WebForm.__contains__

```{autodoc2-docstring} fastlife.testing.testclient.WebForm.__contains__
```

````

````{py:method} __repr__() -> str
:canonical: fastlife.testing.testclient.WebForm.__repr__

````

`````

`````{py:class} WebResponse(client: fastlife.testing.testclient.WebTestClient, origin: str, response: httpx.Response)
:canonical: fastlife.testing.testclient.WebResponse

```{autodoc2-docstring} fastlife.testing.testclient.WebResponse
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.testing.testclient.WebResponse.__init__
```

````{py:property} status_code
:canonical: fastlife.testing.testclient.WebResponse.status_code
:type: int

```{autodoc2-docstring} fastlife.testing.testclient.WebResponse.status_code
```

````

````{py:property} is_redirect
:canonical: fastlife.testing.testclient.WebResponse.is_redirect
:type: bool

```{autodoc2-docstring} fastlife.testing.testclient.WebResponse.is_redirect
```

````

````{py:property} content_type
:canonical: fastlife.testing.testclient.WebResponse.content_type
:type: str

```{autodoc2-docstring} fastlife.testing.testclient.WebResponse.content_type
```

````

````{py:property} headers
:canonical: fastlife.testing.testclient.WebResponse.headers
:type: httpx.Headers

```{autodoc2-docstring} fastlife.testing.testclient.WebResponse.headers
```

````

````{py:property} text
:canonical: fastlife.testing.testclient.WebResponse.text
:type: str

```{autodoc2-docstring} fastlife.testing.testclient.WebResponse.text
```

````

````{py:property} html
:canonical: fastlife.testing.testclient.WebResponse.html
:type: fastlife.testing.testclient.Element

```{autodoc2-docstring} fastlife.testing.testclient.WebResponse.html
```

````

````{py:property} html_body
:canonical: fastlife.testing.testclient.WebResponse.html_body
:type: fastlife.testing.testclient.Element

```{autodoc2-docstring} fastlife.testing.testclient.WebResponse.html_body
```

````

````{py:property} form
:canonical: fastlife.testing.testclient.WebResponse.form
:type: fastlife.testing.testclient.WebForm

```{autodoc2-docstring} fastlife.testing.testclient.WebResponse.form
```

````

````{py:method} by_text(text: str, *, node_name: str | None = None) -> fastlife.testing.testclient.Element | None
:canonical: fastlife.testing.testclient.WebResponse.by_text

```{autodoc2-docstring} fastlife.testing.testclient.WebResponse.by_text
```

````

````{py:method} by_label_text(text: str) -> fastlife.testing.testclient.Element | None
:canonical: fastlife.testing.testclient.WebResponse.by_label_text

```{autodoc2-docstring} fastlife.testing.testclient.WebResponse.by_label_text
```

````

````{py:method} by_node_name(node_name: str, *, attrs: dict[str, str] | None = None) -> list[fastlife.testing.testclient.Element]
:canonical: fastlife.testing.testclient.WebResponse.by_node_name

```{autodoc2-docstring} fastlife.testing.testclient.WebResponse.by_node_name
```

````

`````

`````{py:class} Session(client: fastlife.testing.testclient.WebTestClient)
:canonical: fastlife.testing.testclient.Session

Bases: {py:obj}`dict`\[{py:obj}`str`\, {py:obj}`typing.Any`\]

```{autodoc2-docstring} fastlife.testing.testclient.Session
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.testing.testclient.Session.__init__
```

````{py:method} __setitem__(__key: typing.Any, __value: typing.Any) -> None
:canonical: fastlife.testing.testclient.Session.__setitem__

```{autodoc2-docstring} fastlife.testing.testclient.Session.__setitem__
```

````

````{py:method} serialize() -> str
:canonical: fastlife.testing.testclient.Session.serialize

```{autodoc2-docstring} fastlife.testing.testclient.Session.serialize
```

````

`````

`````{py:class} WebTestClient(app: starlette.types.ASGIApp, *, settings: fastlife.config.settings.Settings | None = None, cookies: fastlife.testing.testclient.CookieTypes | None = None)
:canonical: fastlife.testing.testclient.WebTestClient

```{autodoc2-docstring} fastlife.testing.testclient.WebTestClient
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.testing.testclient.WebTestClient.__init__
```

````{py:property} cookies
:canonical: fastlife.testing.testclient.WebTestClient.cookies
:type: fastlife.testing.testclient.Cookies

```{autodoc2-docstring} fastlife.testing.testclient.WebTestClient.cookies
```

````

````{py:property} session
:canonical: fastlife.testing.testclient.WebTestClient.session
:type: collections.abc.MutableMapping[str, typing.Any]

```{autodoc2-docstring} fastlife.testing.testclient.WebTestClient.session
```

````

````{py:method} request(method: typing.Literal[GET, POST, DELETE], url: str, *, content: str | None = None, headers: typing.Mapping[str, str] | None = None, max_redirects: int = 0) -> fastlife.testing.testclient.WebResponse
:canonical: fastlife.testing.testclient.WebTestClient.request

```{autodoc2-docstring} fastlife.testing.testclient.WebTestClient.request
```

````

````{py:method} get(url: str, follow_redirects: bool = True) -> fastlife.testing.testclient.WebResponse
:canonical: fastlife.testing.testclient.WebTestClient.get

```{autodoc2-docstring} fastlife.testing.testclient.WebTestClient.get
```

````

````{py:method} delete(url: str, follow_redirects: bool = True) -> fastlife.testing.testclient.WebResponse
:canonical: fastlife.testing.testclient.WebTestClient.delete

```{autodoc2-docstring} fastlife.testing.testclient.WebTestClient.delete
```

````

````{py:method} post(url: str, data: multidict.MultiDict[str], *, headers: typing.Mapping[str, typing.Any] | None = None, follow_redirects: bool = True) -> fastlife.testing.testclient.WebResponse
:canonical: fastlife.testing.testclient.WebTestClient.post

```{autodoc2-docstring} fastlife.testing.testclient.WebTestClient.post
```

````

`````
