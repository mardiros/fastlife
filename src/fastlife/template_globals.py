"""
Template Constants injects as global variables in templates.

Constants are configurable using the setting :attrs:`jinjax_global_catalog_class`,
in order to customize templates.

Those constants are heavy used to inject CSS classes in primary html element
that are bound to Jinja component.

"""

from pydantic import BaseModel


def space_join(*segments: str) -> str:
    return " ".join(segments)


class Globals(BaseModel):
    """Templates constants."""

    A_CLASS: str = space_join(
        "text-primary-600",
        "hover:text-primary-500",
        "hover:underline",
        "dark:text-primary-300",
        "dark:hover:text-primary-400",
    )
    """Default css class for {jinjax:component}`A`."""

    BUTTON_CLASS: str = space_join(
        "bg-primary-600",
        "px-5",
        "py-2.5",
        "font-semibold",
        "rounded-lg",
        "text-center",
        "text-sm",
        "text-white",
        "hover:bg-primary-700",
        "hover:bg-primary-200",
        "focus:outline-hidden",
        "focus:ring-4",
        "focus:ring-primary-300",
        "dark:bg-primary-600",
        "dark:focus:ring-primary-800",
        "dark:hover:bg-primary-700",
    )
    """Default css class for {jinjax:component}`Button`."""

    DETAILS_CLASS: str = "border border-neutral-100 p-4 rounded-m"
    """Default css class for {jinjax:component}`Details`."""

    SECONDARY_BUTTON_CLASS: str = space_join(
        "bg-neutral-300",
        "px-5",
        "py-2.5",
        "rounded-lg",
        "font-semibold",
        "text-center",
        "text-neutral-900",
        "text-sm",
        "focus:outline-hidden",
        "focus:ring-4",
        "focus:ring-primary-300",
        "hover:bg-neutral-200",
        "dark:bg-neutral-400",
        "dark:focus:ring-neutral-100",
        "dark:hover:bg-neutral-300",
    )
    """
    css class for {jinjax:component}`Button`.

    usage:

    ```html
    <Button :class="SECONDARY_BUTTON_CLASS">secondary</Button>
    ```
    """

    ICON_BUTTON_CLASS: str = space_join(
        "bg-white",
        "p-1",
        "rounded-xs",
        "text-primary-600",
        "border",
        "border-primary-600",
        "hover:bg-primary-200",
        "focus:outline-hidden",
        "focus:ring-4",
        "focus:ring-primary-500",
        "dark:bg-primary-900",
        "dark:text-neutral-300",
        "dark:hover:bg-primary-800",
        "dark:focus:ring-primary-500",
        "dark:hover:text-primary-300",
    )
    """
    css class for {jinjax:component}`Button`.

    usage:

    ```html
    <Button :class="ICON_BUTTON_CLASS">
      <icons.PencilSquare class="w-6 h-6" title="Copy" />
    </Button>

    ```
    """

    CHECKBOX_CLASS: str = space_join(
        "bg-neutral-100",
        "border-neutral-300",
        "h-4",
        "rounded-sm",
        "text-primary-600",
        "w-4",
        "dark:bg-neutral-700",
        "dark:border-neutral-600",
        "dark:focus:ring-primary-600",
        "dark:ring-offset-neutral-800",
        "focus:ring-2",
        "focus:ring-primary-500",
    )
    """Default css class for {jinjax:component}`Checkbox`."""

    FORM_CLASS: str = "space-y-4 md:space-y-6"
    """Default css class for {jinjax:component}`Form`."""

    H1_CLASS: str = space_join(
        "block",
        "font-bold",
        "font-sans",
        "leading-tight",
        "pb-4",
        "text-5xl",
        "text-neutral-900",
        "tracking-tight",
        "dark:text-white",
        "md:text-4xl",
    )
    """Default css class for {jinjax:component}`H1`."""

    H2_CLASS: str = space_join(
        "block",
        "font-bold",
        "font-sans",
        "leading-tight",
        "pb-4",
        "text-4xl",
        "text-neutral-900",
        "tracking-tight",
        "dark:text-white",
        "md:text-4xl",
    )
    """Default css class for {jinjax:component}`H2`."""

    H3_CLASS: str = space_join(
        "block",
        "font-bold",
        "font-sans",
        "leading-tight",
        "pb-4",
        "text-3xl",
        "text-neutral-900",
        "tracking-tight",
        "dark:text-white",
        "md:text-3xl",
    )
    """Default css class for {jinjax:component}`H3`."""

    H3_SUMMARY_CLASS: str = space_join(
        "block",
        "font-bold",
        "font-sans",
        "leading-tight",
        "text-3xl",
        "text-neutral-900",
        "tracking-tight",
        "dark:text-white",
        "md:text-3xl",
    )
    """
    Default css class for {jinjax:component}`H3` inside {jinjax:component}`Summary`.
    """

    H4_CLASS: str = space_join(
        "block",
        "font-bold",
        "font-sans",
        "leading-tight",
        "pb-4",
        "text-2xl",
        "text-neutral-900",
        "tracking-tight",
        "dark:text-white",
        "md:text-2xl",
    )
    """Default css class for {jinjax:component}`H4`."""

    H5_CLASS: str = space_join(
        "block",
        "font-bold",
        "font-sans",
        "leading-tight",
        "pb-4",
        "text-xl",
        "text-neutral-900",
        "tracking-tight",
        "dark:text-white",
        "md:text-xl",
    )
    """Default css class for {jinjax:component}`H5`."""

    H6_CLASS: str = space_join(
        "block",
        "font-bold",
        "font-sans",
        "leading-tight",
        "pb-4",
        "text-l",
        "text-neutral-900",
        "tracking-tight",
        "dark:text-white",
        "md:text-l",
    )
    """Default css class for {jinjax:component}`H6`."""

    INPUT_CLASS: str = space_join(
        "bg-neutral-50",
        "block",
        "border",
        "border-neutral-300",
        "p-2.5",
        "rounded-lg",
        "text-base",
        "text-neutral-900",
        "w-full",
        "dark:bg-neutral-700",
        "dark:border-neutral-600",
        "dark:focus:border-primary-500",
        "dark:focus:ring-primary-500",
        "dark:placeholder-neutral-400",
        "dark:text-white",
        "focus:border-primary-500",
        "focus:ring-primary-500",
    )
    """Default css class for {jinjax:component}`Input`."""

    LABEL_CLASS: str = space_join(
        "block",
        "font-bold",
        "mb-2",
        "text-base",
        "text-neutral-900",
        "dark:text-white",
    )
    """Default css class for {jinjax:component}`Label`."""

    P_CLASS: str = space_join(
        "text-base",
        "text-neutral-900",
        "dark:text-white",
    )
    """Default css class for {jinjax:component}`P`."""

    RADIO_DIV_CLASS: str = "flex items-center mb-4"
    """Default css class for {jinjax:component}`Radio` `<div>` container."""

    RADIO_INPUT_CLASS: str = space_join(
        "bg-neutral-100",
        "border-neutral-300",
        "w-4",
        "h-4",
        "text-primary-600",
        "focus:ring-2",
        "focus:ring-primary-500",
        "dark:bg-neutral-700",
        "dark:border-neutral-600",
        "dark:focus:ring-primary-600",
        "dark:ring-offset-neutral-800",
    )
    """
    Default css class for {jinjax:component}`Radio` `<input type="radio">`.
    """

    RADIO_LABEL_CLASS: str = (
        "ms-2 text-sm font-medium text-neutral-900 dark:text-neutral-300"
    )
    """
    Default css class for {jinjax:component}`Radio` `<label>` element.
    """

    SELECT_CLASS: str = space_join(
        "bg-neutral-50",
        "block",
        "border",
        "border-neutral-300",
        "p-2.5",
        "rounded-lg",
        "text-base",
        "text-neutral-900",
        "w-full",
        "focus:border-primary-500",
        "focus:ring-primary-500",
        "dark:bg-neutral-700",
        "dark:border-neutral-600",
        "dark:focus:border-primary-500",
        "dark:focus:ring-primary-500",
        "dark:placeholder-neutral-400",
        "dark:text-white",
    )
    """Default css class for {jinjax:component}`Select`."""

    SUMMARY_CLASS: str = "flex items-center items-center font-medium cursor-pointer"
    """Default css class for {jinjax:component}`Summary`."""

    TABLE_CLASS: str = "table-auto w-full text-left border-collapse"
    """Default css class for {jinjax:component}`Table`."""

    TD_CLASS: str = "px-4 py-2 font-normal border-b dark:border-neutral-500"
    """Default css class for {jinjax:component}`Td`."""

    TH_CLASS: str = "px-4 py-2 font-medium border-b dark:border-neutral-500"
    """Default css class for {jinjax:component}`Th`."""

    ERROR_CLASS: str = "mt-2 text-sm text-danger-500 dark:text-danger-400"
    """Default css class for {jinjax:component}`pydantic_form.Error`."""

    FATAL_ERROR_CLASS: str = (
        "flex items-center bg-red-50 border border-red-400 text-red-700"
    )
    """Default css class for {jinjax:component}`pydantic_form.FatalError`."""

    FATAL_ERROR_ICON_CLASS: str = "m-3 w-16 h-16 fill-orange-500"
    """Default css class for {jinjax:component}`pydantic_form.FatalError` icon."""

    FATAL_ERROR_TEXT_CLASS: str = "sm:inline text-xl"
    """Default css class for {jinjax:component}`pydantic_form.FatalError` text."""
