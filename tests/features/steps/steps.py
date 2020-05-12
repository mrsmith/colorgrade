import subprocess as sp
import re
from pprint import pformat, pprint

from colour import Color
from hamcrest import *


def check_output(command):
    try:
        return sp.check_output(command, shell=1, stderr=sp.PIPE).decode("utf-8")

    except sp.CalledProcessError as ex:
        stderr = ex.stderr.decode("utf-8").rstrip("\n")
        msg = f"command `{ex.cmd}` failed with rc: {ex.returncode}, stderr:\n{stderr}\n--"
        raise Exception(msg)


# '\x1b[38;2;0;255;0m1\x1b[39m'
def parse_colored_line(line):
    m = re.match("\x1b\\[38;2;([0-9]+);([0-9]+);([0-9]+)m(.*)\x1b\\[39m", line)
    rgb = [int(x) for x in m.groups()[0:3]]
    hex = "#%02x%02x%02x" % tuple(rgb)
    return Color(hex), m.group(4)


@when("I run `{command}`")
def step_impl(context, command):
    context.output = check_output(command)


@then("Output is colored as follows")
def step_impl(context):
    lines = context.output.rstrip("\n").split("\n")
    assert_that(lines, has_length(len(context.table.rows)))

    for line, expected in zip(lines, context.table):
        if expected["color"] == "<nocolor>":
            assert_that(line, equal_to(expected["line"]))

        else:
            color, text = parse_colored_line(line)

            assert_that(color, equal_to(Color(expected["color"])))
            assert_that(text, equal_to(expected["line"]))
