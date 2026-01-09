"""HTML Form elements."""

from collections.abc import Mapping
from datetime import date
from typing import Literal

from xcomponent import XNode

from fastlife.adapters.xcomponent.registry import BUILTINS_CATALOG_NS, x_component


@x_component(namespace=BUILTINS_CATALOG_NS)
def Form(
    children: XNode,
    globals: Mapping[str, str],
    id: str | None = None,
    class_: str | None = None,
    method: Literal["get", "post"] | None = None,
    action: str | None = None,
    hx_target: str | None = None,
    hx_select: str | None = None,
    hx_swap: str | None = None,
    hx_post: str | Literal[True] | None = None,
    hx_disable: Literal[True] | None = None,
) -> str:
    """
    Generate the html `<form>` element.

    :param children: Child elements to be included within the form
    :param globals: Global template variables including default CSS classes
    :param id: Unique identifier for the form element
    :param class_: CSS class for the form element
    :param method: HTTP method for form submission (get or post)
    :param action: URL where the form data will be submitted
    :param hx_target: HTMX target element selector
    :param hx_select: HTMX element selector for content swapping
    :param hx_swap: HTMX swap strategy
    :param hx_post: HTMX POST request URL or True to submit to current URL
    :param hx_disable: HTMX attribute to disable HTMX processing
    """
    return """
        <form
            id={id}
            class={class_ or globals.FORM_CLASS}
            hx-disable={hx_disable}
            hx-post={hx_post}
            hx-select={hx_select}
            hx-swap={hx_swap}
            hx-target={hx_target}
            action={action}
            method={method}
            >
            <CsrfToken />
            { children }
        </form>
    """


@x_component(namespace=BUILTINS_CATALOG_NS)
def CsrfToken(globals: dict[str, str]) -> str:
    """Generate the html hidden field for CSRF validation."""
    return """
        <Hidden
            name={globals.request.csrf_token.name}
            value={globals.request.csrf_token.value}
            />
    """


@x_component(namespace=BUILTINS_CATALOG_NS)
def Input(
    name: str,
    value: str = "",
    type: Literal[
        "button",
        "checkbox",
        "color",
        "date",
        "datetime-local",
        "email",
        "file",
        "hidden",
        "image",
        "month",
        "number",
        "password",
        "radio",
        "range",
        "reset",
        "search",
        "submit",
        "tel",
        "text",
        "time",
        "url",
        "week",
    ] = "text",
    id: str | None = None,
    class_: str | None = None,
    aria_label: str | None = None,
    placeholder: str | None = None,
    pattern: str | None = None,
    inputmode: Literal[
        "none", "text", "decimal", "numeric", "tel", "search", "email", "url"
    ]
    | None = None,
    autocomplete: Literal[
        "on",
        "off",
        "name",
        "username",
        "current-password",
        "new-password",
        "one-time-code",
        "email",
        "tel",
        "organization",
        "street-address",
        "address-line1",
        "address-line2",
        "address-line3",
        "postal-code",
        "country",
        "country-name",
        "cc-name",
        "cc-number",
        "cc-exp",
        "cc-csc",
        "tel-country-code",
        "tel-national",
        "tel-area-code",
        "tel-local",
        "tel-extension",
        "bday",
        "bday-day",
        "bday-month",
        "bday-year",
        "transaction-amount",
        "transaction-currency",
    ]
    | None = None,
    autofocus: bool = False,
) -> str:
    """
    Generate an HTML `<input>` element.

    Note that all types, inputmode, autocomplete mode are declared,
    but specific input element should be used for password, checkbox,
    radio button, date, datetimes.

    :param name: Name attribute for the input element
    :param value: Initial value of the input element
    :param type: Type of input element (e.g., text, password, email)
    :param id: Unique identifier for the input element
    :param class_: CSS class for the input element
    :param aria_label: Accessible label for the input element
    :param placeholder: Hint text displayed in the input field
    :param pattern: Regular expression pattern for input validation
    :param inputmode: Hint for virtual keyboard configuration
    :param autocomplete: Browser autocomplete behavior for the input
    :param autofocus: Whether the input should automatically receive focus
    """
    return """
    <input
        type={type}
        name={name}
        value={value}
        id={id}
        aria-label={aria_label}
        placeholder={placeholder}
        pattern={pattern}
        inputmode={inputmode}
        autocomplete={autocomplete}
        class={class_ or globals.INPUT_CLASS}
        autofocus={autofocus}
    />
    """


@x_component(namespace=BUILTINS_CATALOG_NS)
def Date(
    name: str,
    value: str = "",
    type: Literal["date"] = "date",
    id: str | None = None,
    class_: str | None = None,
    aria_label: str | None = None,
    min: date | None = None,
    max: date | None = None,
) -> str:
    """
    Generate an HTML `<input>` element for date.

    :param name: Name attribute for the date input element
    :param value: Initial value of the date input element in ISO format (YYYY-MM-DD)
    :param type: Type of input element (always "date" for this component)
    :param id: Unique identifier for the date input element
    :param class_: CSS class for the date input element
    :param aria_label: Accessible label for the date input element
    :param min: Minimum allowed date (as date object)
    :param max: Maximum allowed date (as date object)
    """

    return """
    <input
        type={type}
        name={name}
        value={value}
        min={isoformat(min)}
        max={isoformat(max)}
        id={id}
        aria-label={aria_label}
        class={class_ or globals.INPUT_CLASS}
    />
    """


@x_component(namespace=BUILTINS_CATALOG_NS)
def DateTime(
    name: str,
    value: str = "",
    type: Literal["datetime-local"] = "datetime-local",
    id: str | None = None,
    class_: str | None = None,
    aria_label: str | None = None,
    min: date | None = None,
    max: date | None = None,
) -> str:
    """
    Generate an HTML `<input>` element for datetime-local.

    :param name: Name attribute for the datetime input element
    :param value: Initial value of the datetime input element in ISO format (YYYY-MM-DDTHH:MM)
    :param type: Type of input element (always "datetime-local" for this component)
    :param id: Unique identifier for the datetime input element
    :param class_: CSS class for the datetime input element
    :param aria_label: Accessible label for the datetime input element
    :param min: Minimum allowed datetime (as date object)
    :param max: Maximum allowed datetime (as date object)
    """
    return """
    <input
        type={type}
        name={name}
        value={value}
        min={isoformat(min)}
        max={isoformat(max)}
        id={id}
        aria-label={aria_label}
        class={class_ or globals.INPUT_CLASS}
    />
    """


@x_component(namespace=BUILTINS_CATALOG_NS)
def Hidden(
    name: str,
    value: str,
    id: str | None = None,
) -> str:
    """
    Generate an HTML hidden input element.

    Hidden inputs are used to include data in a form that should not be visible
    or editable by the user, but needs to be submitted with the form.

    :param name: Name attribute for the hidden input element
    :param value: Value of the hidden input element
    :param id: Unique identifier for the hidden input element
    """
    return """
        <input name={name} value={value} type="hidden" id={id} />
    """


@x_component(namespace=BUILTINS_CATALOG_NS)
def Button(
    children: XNode,
    globals: Mapping[str, str],
    type: Literal["submit", "button", "reset"] = "submit",
    id: str | None = None,
    class_: str | None = None,
    name: str = "action",
    value: str = "submit",
    hidden: bool = False,
    aria_label: str | None = None,
    onclick: str | None = None,
    hx_target: str | None = None,
    hx_swap: str | None = None,
    hx_select: str | None = None,
    hx_on_after_request: str | None = None,
    hx_vals: str | None = None,
    hx_confirm: str | None = None,
    hx_get: str | None = None,
    hx_post: str | None = None,
    hx_put: str | None = None,
    hx_patch: str | None = None,
    hx_delete: str | None = None,
    hx_params: str | None = None,
    hx_push_url: bool = False,
    full_width: bool = False,
) -> str:
    """
    Generate an HTML `<button>` element with HTMX support.

    This component creates a button element that can be used in forms or as standalone
    interactive elements. It supports various button types, HTMX attributes for dynamic
    behavior, and styling options.

    :param children: Child elements to be included within the button
    :param globals: Global template variables including default CSS classes
    :param type: Button type (submit, button, or reset)
    :param id: Unique identifier for the button element
    :param class_: CSS class for the button element
    :param name: Name attribute for the button (used in form submission)
    :param value: Value associated with the button (used in form submission)
    :param hidden: Whether the button should be hidden
    :param aria_label: Accessible label for the button
    :param onclick: JavaScript to execute when the button is clicked
    :param hx_target: HTMX target element selector
    :param hx_swap: HTMX swap strategy
    :param hx_select: HTMX element selector for content swapping
    :param hx_on_after_request: HTMX event handler for after request completion
    :param hx_vals: HTMX values to include in the request
    :param hx_confirm: HTMX confirmation message before request
    :param hx_get: HTMX GET request URL
    :param hx_post: HTMX POST request URL
    :param hx_put: HTMX PUT request URL
    :param hx_patch: HTMX PATCH request URL
    :param hx_delete: HTMX DELETE request URL
    :param hx_params: HTMX parameters to include in the request
    :param hx_push_url: Whether to push the URL to the browser's history
    :param full_width: Whether the button should span the full width of its container
    """
    return """
    <button
        type={type}
        name={name}
        value={value}
        id={id}
        hx-target={hx_target}
        hx-swap={hx_swap}
        hx-select={hx_select}
        onclick={onclick}
        hx-on::after-request={hx_on_after_request}
        hx-vals={hx_vals}
        hx-confirm={hx_confirm}
        hx-get={hx_get}
        hx-post={hx_post}
        hx-put={hx_put}
        hx-patch={hx_patch}
        hx-delete={hx_delete}
        hx-push-url={
            if is_bool(hx_push_url) {
                if hx_push_url { "true" } else { false }
            }
            else { hx_push_url }
        }
        hx-params={hx_params}
        aria-label={aria_label}
        class={
            if full_width {
                "w-full " + (class_ or globals.BUTTON_CLASS)
            }
            else {
                class_ or globals.BUTTON_CLASS
            }
        }
        hidden={hidden}
        >
        {children}
    </button>
    """


@x_component(namespace=BUILTINS_CATALOG_NS)
def Checkbox(
    name: str,
    globals: Mapping[str, str],
    id: str | None = None,
    class_: str | None = None,
    value: str | None = None,
    checked: bool = False,
) -> str:
    """
    Generate an HTML `<input type="checkbox">` element.

    This component creates a checkbox input element that can be used in forms.
    Checkboxes allow users to select one or more options from a set.

    :param name: Name attribute for the checkbox element (used in form submission)
    :param globals: Global template variables including default CSS classes
    :param id: Unique identifier for the checkbox element
    :param class_: CSS class for the checkbox element, defaults to
                  :attr:`fastlife.template_globals.Globals.CHECKBOX_CLASS`
    :param value: Value that will be submitted if the checkbox is checked
    :param checked: Whether the checkbox should be initially checked
    """
    return """
        <input
            name={name}
            type="checkbox"
            id={id}
            value={value}
            class={class_ or globals.CHECKBOX_CLASS }
            checked={checked}
            />
    """


@x_component(namespace=BUILTINS_CATALOG_NS)
def Password(
    name: str,
    globals: Mapping[str, str],
    id: str | None = None,
    class_: str | None = None,
    aria_label: str | None = None,
    placeholder: str | None = None,
    autocomplete: Literal[
        "on",
        "off",
        "current-password",
        "new-password",
    ]
    | None = None,
    inputmode: Literal[
        "none",
        "text",
        "numeric",
    ]
    | None = None,
    minlength: int | None = None,
    maxlength: int | None = None,
    pattern: str | None = None,
    autofocus: bool = False,
    required: bool = False,
    readonly: bool = False,
) -> str:
    """
    Generate an HTML password input element.

    This component creates a secure password input field that masks user input.
    It's commonly used in login forms, registration forms, and any other context
    where sensitive information needs to be collected.

    :param name: Name attribute for the password input element (used in form submission)
    :param globals: Global template variables including default CSS classes
    :param id: Unique identifier for the password input element
    :param class_: CSS class for the password input element, defaults to
                  :attr:`fastlife.template_globals.Globals.INPUT_CLASS`
    :param aria_label: Accessible label for the password input element
    :param placeholder: Hint text displayed in the password field
    :param autocomplete: Browser autocomplete behavior for the password field
                         (on, off, current-password, new-password)
    :param inputmode: Hint for virtual keyboard configuration (none, text, numeric)
    :param minlength: Minimum number of characters required
    :param maxlength: Maximum number of characters allowed
    :param pattern: Regular expression pattern for password validation
    :param autofocus: Whether the password field should automatically receive focus
    :param required: Whether the password field is mandatory
    :param readonly: Whether the password field is read-only
    """
    return """
    <input
        name={name}
        type="password"
        id={id}
        aria-label={aria_label}
        placeholder={placeholder}
        autocomplete={autocomplete}
        inputmode={inputmode}
        minlength={minlength}
        maxlength={maxlength}
        pattern={pattern}
        class={class_ or globals.INPUT_CLASS}
        autofocus={autofocus}
        required={required}
        readonly={readonly}
    />
    """


@x_component(namespace=BUILTINS_CATALOG_NS)
def Label(
    children: XNode,
    globals: Mapping[str, str],
    for_: str | None = None,
    id: str | None = None,
    class_: str | None = None,
) -> str:
    """
    Generate an HTML `<label>` element.

    Labels provide accessible descriptions for form elements, improving usability
    and screen reader compatibility. The label can be associated with an input
    element using the `for_` attribute.

    :param children: Content to be displayed within the label element
    :param globals: Global template variables including default CSS classes
    :param for_: ID of the form element this label is associated with
    :param id: Unique identifier for the label element
    :param class_: CSS class for the label element, defaults to
                  :attr:`fastlife.template_globals.Globals.LABEL_CLASS`
    """
    return """
    <label for={for_} class={class_ or globals.LABEL_CLASS} id={id}>
        {children}
    </label>
    """


@x_component(namespace=BUILTINS_CATALOG_NS)
def Option(
    children: XNode,
    value: str,
    id: str | None = None,
    selected: bool = False,
) -> str:
    """
    Generate an HTML `<option>` element for use in select dropdowns.

    This component creates an option element that can be used within a select element
    to provide choices for user selection in forms.

    :param children: Content to be displayed as the option label
    :param value: Value that will be submitted when this option is selected
    :param id: Unique identifier for the option element
    :param selected: Whether this option should be pre-selected when the form renders
    """
    return """
    <option value={value} id={id} selected={selected}>
        {children}
    </option>
    """


@x_component(namespace=BUILTINS_CATALOG_NS)
def Select(
    children: XNode,
    name: str,
    id: str | None = None,
    class_: str | None = None,
    multiple: bool = False,
    hx_get: str | None = None,
    hx_trigger: str | None = None,
    hx_target: str | None = None,
    hx_include: str | None = None,
    hx_swap: str | None = None,
) -> str:
    """
    Generate an HTML `<select>` dropdown element with HTMX support.

    This component creates a select dropdown that allows users to choose from a list of options.
    It supports both single and multiple selection modes and includes HTMX attributes for
    dynamic behavior.

    :param children: Child elements (typically Option components) to populate the dropdown
    :param name: Name attribute for the select element (used in form submission)
    :param id: Unique identifier for the select element
    :param class_: CSS class for the select element, defaults to
                  :attr:`fastlife.template_globals.Globals.SELECT_CLASS`
    :param multiple: Whether to allow multiple selections
    :param hx_get: HTMX attribute to specify a GET request URL for dynamic content loading
    :param hx_trigger: HTMX attribute to specify when the request should be triggered
    :param hx_target: HTMX attribute to specify the target element for the response
    :param hx_include: HTMX attribute to specify which elements to include in the request
    :param hx_swap: HTMX attribute to specify how the response content should be swapped
    """
    return """
    <select name={name} id={id} class={class_ or globals.SELECT_CLASS}
            multiple={multiple}
            hx-get={hx_get}
            hx-trigger={hx_trigger}
            hx-target={hx_target}
            hx-include={hx_include}
            hx-swap={hx_swap}
            >
        {children}
    </select>
    """


@x_component(namespace=BUILTINS_CATALOG_NS)
def Radio(
    label: str,
    name: str,
    value: str,
    id: str | None = None,
    checked: bool = False,
    disabled: bool = False,
    onclick: str | None = None,
    div_class: str | None = None,
    class_: str | None = None,
    label_class: str | None = None,
) -> str:
    """
    Generate an HTML radio button input with its associated label wrapped in a div container.

    This component creates a radio button input element with a label, providing a complete
    radio button option that can be used in forms. The radio button and label are wrapped
    in a div container for better styling and layout control.

    :param label: Text to display as the label for the radio button
    :param name: Name attribute for the radio button (used in form submission)
    :param value: Value that will be submitted if this radio button is selected
    :param id: Unique identifier for the radio button element
    :param checked: Whether the radio button should be initially checked
    :param disabled: Whether the radio button should be disabled
    :param onclick: JavaScript code to execute when the radio button is clicked
    :param div_class: CSS class for the wrapping div element, defaults to
                     :attr:`fastlife.template_globals.Globals.RADIO_DIV_CLASS`
    :param class_: CSS class for the radio input element, defaults to
                   :attr:`fastlife.template_globals.Globals.RADIO_INPUT_CLASS`
    :param label_class: CSS class for the label element, defaults to
                        :attr:`fastlife.template_globals.Globals.RADIO_LABEL_CLASS`
    """

    return """
    <div class={div_class or globals.RADIO_DIV_CLASS}>
        <input type="radio" name={name} id={id} value={value}
            class={class_ or globals.RADIO_INPUT_CLASS}
            onclick={onclick}
            checked={checked}
            disabled={disabled} />
        <Label for={id} class={label_class or globals.RADIO_LABEL_CLASS}>
            {label}
        </Label>
    </div>
    """


@x_component(namespace=BUILTINS_CATALOG_NS)
@x_component(namespace=BUILTINS_CATALOG_NS)
def Textarea(
    children: XNode,
    globals: Mapping[str, str],
    name: str,
    id: str | None = None,
    class_: str | None = None,
    aria_label: str | None = None,
    placeholder: str | None = None,
    readonly: bool = False,
) -> str:
    """
    Generate an HTML `<textarea>` element.

    This component creates a multi-line text input field that allows users to enter longer
    text content. Textareas are commonly used in forms for collecting user feedback,
    descriptions, or any other multi-line text input.

    :param children: Initial content to be displayed within the textarea
    :param globals: Global template variables including default CSS classes
    :param name: Name attribute for the textarea element (used in form submission)
    :param id: Unique identifier for the textarea element
    :param class_: CSS class for the textarea element, defaults to
                  :attr:`fastlife.template_globals.Globals.INPUT_CLASS`
    :param aria_label: Accessible label for the textarea element
    :param placeholder: Hint text displayed in the textarea when empty
    :param readonly: Whether the textarea should be read-only
    """

    return """
    <textarea
        name={name}
        id={id}
        aria-label={aria_label}
        placeholder={placeholder}
        readonly={readonly}
        class={class_ or globals.INPUT_CLASS}>
        {children}
    </textarea>
    """
