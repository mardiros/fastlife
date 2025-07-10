import pytest
from bs4 import PageElement

table_css = "table-auto w-full text-left border-collapse"
th_css = "px-4 py-2 font-medium border-b dark:border-neutral-500"
td_css = "px-4 py-2 font-normal border-b dark:border-neutral-500"


@pytest.mark.parametrize(
    "template_string,expected_string",
    [
        pytest.param(
            """
            <Table>
                <Thead>
                    <Tr><Th>A</Th><Th>B</Th></Tr>
                </Thead>
                <Tbody>
                    <Tr><Td>1</Td><Td>2</Td></Tr>
                    <Tr><Td>3</Td><Td>4</Td></Tr>
                </Tbody>
                <Tfoot>
                    <Tr><Td>Y</Td><Td>Z</Td></Tr>
                </Tfoot>
            </Table>
            """,
            f"""
            <table class="{table_css}">
                <thead>
                    <tr><th class="{th_css}">A</th><th class="{th_css}">B</th></tr>
                </thead>
                <tbody>
                    <tr><td class="{td_css}">1</td><td class="{td_css}">2</td></tr>
                    <tr><td class="{td_css}">3</td><td class="{td_css}">4</td></tr>
                </tbody>
                <tfoot>
                    <tr><td class="{td_css}">Y</td><td class="{td_css}">Z</td></tr>
                </tfoot>
            </table>
            """,
            id="default",
        ),
        pytest.param(
            """
            <Table class="t">
                <Thead class="thead">
                    <Tr><Th class="th">A</Th><Th>B</Th></Tr>
                </Thead>
                <Tbody class="tbody">
                    <Tr><Td class="td">1</Td><Td>2</Td></Tr>
                    <Tr><Td>3</Td><Td>4</Td></Tr>
                </Tbody>
                <Tfoot class="tfoot">
                    <Tr><Td>Y</Td><Td>Z</Td></Tr>
                </Tfoot>
            </Table>
            """,
            f"""
            <table class="t">
                <thead class="thead">
                    <tr><th class="th">A</th><th class="{th_css}">B</th></tr>
                </thead>
                <tbody class="tbody">
                    <tr><td class="td">1</td><td class="{td_css}">2</td></tr>
                    <tr><td class="{td_css}">3</td><td class="{td_css}">4</td></tr>
                </tbody>
                <tfoot class="tfoot">
                    <tr><td class="{td_css}">Y</td><td class="{td_css}">Z</td></tr>
                </tfoot>
            </table>
            """,
            id="overide css",
        ),
        pytest.param(
            """
            <Table id="t1" class="t">
                <Thead id="thead">
                    <Tr><Th id="th1">A</Th></Tr>
                </Thead>
                <Tbody id="tbody">
                    <Tr><Td id="td1">A</Td></Tr>
                </Tbody>
                <Tfoot id="tfoot">
                </Tfoot>
            </Table>
            """,
            f"""
            <table id="t1" class="t">
                <thead id="thead">
                    <tr><th id="th1" class="{th_css}">A</th></tr>
                </thead>
                <tbody id="tbody">
                    <tr><td id="td1" class="{td_css}">A</td></tr>
                </tbody>
                <tfoot id="tfoot">
                </tfoot>
            </table>
            """,
            id="ids",
        ),
    ],
)
def test_table(soup_rendered: PageElement, soup_expected: PageElement):
    assert soup_rendered == soup_expected
