from pydantic import BaseModel


def space_join(*segments: str) -> str:
    return " ".join(segments)


class Constants(BaseModel):
    A_CLASS: str = space_join(
        "text-primary-600",
        "hover:text-primary-500",
        "hover:underline",
        "dark:text-primary-300",
        "dark:hover:text-primary-400",
    )

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
        "focus:outline-none",
        "focus:ring-4",
        "focus:ring-primary-300",
        "dark:bg-primary-600",
        "dark:focus:ring-primary-800",
        "dark:hover:bg-primary-700",
    )

    DETAILS_CLASS: str = "border border-neutral-100 p-4 rounded-m"

    SECONDARY_BUTTON_CLASS: str = space_join(
        "bg-neutral-300",
        "px-5",
        "py-2.5",
        "rounded-lg",
        "font-semibold",
        "text-center",
        "text-neutral-900",
        "text-sm",
        "focus:outline-none",
        "focus:ring-4",
        "focus:ring-primary-300",
        "hover:bg-neutral-200",
        "dark:bg-neutral-400",
        "dark:focus:ring-neutral-100",
        "dark:hover:bg-neutral-300",
    )

    CHECKBOX_CLASS: str = space_join(
        "bg-neutral-100",
        "border-neutral-300",
        "h-4",
        "rounded",
        "text-primary-600",
        "w-4",
        "dark:bg-neutral-700",
        "dark:border-neutral-600",
        "dark:focus:ring-primary-600",
        "dark:ring-offset-neutral-800",
        "focus:ring-2",
        "focus:ring-primary-500",
    )
    FORM_CLASS: str = "space-y-4 md:space-y-6"
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
    LABEL_CLASS: str = space_join(
        "block",
        "font-bold",
        "mb-2",
        "text-base",
        "text-neutral-900",
        "dark:text-white",
    )
    P_CLASS: str = space_join(
        "text-base",
        "text-neutral-900",
        "dark:text-white",
    )
    RADIO_DIV_CLASS: str = "flex items-center mb-4"
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
    RADIO_LABEL_CLASS: str = (
        "ms-2 text-sm font-medium text-neutral-900 dark:text-neutral-300"
    )
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
    TABLE_CLASS: str = "table-auto w-full text-left border-colapse"
    TD_CLASS: str = "px-4 py-2 font-normal border-b dark:border-neutral-500"
    TH_CLASS: str = "px-4 py-2 font-medium border-b dark:border-neutral-500"
