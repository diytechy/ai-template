"""TC-305: lane separation in freshly emitted dashboard SVG, not router inputs."""

from html.parser import HTMLParser
from itertools import combinations
import re

import pytest

from conftest import ROOT, load_script
from test_traj_render import _svg_subtrees


class _Tags(HTMLParser):
    def __init__(self, markup):
        super().__init__()
        self.tags = []
        self.groups = []
        self.feed(markup)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in {"g", "a"}:
            self.groups.append(attrs)
        if tag == "path" and self.groups:
            parent = self.groups[-1]
            if "ctxrel" in parent.get("class", "").split():
                attrs["class"] = "ctxrel"
            if "data-edge" in parent:
                attrs["data-edge"] = parent["data-edge"]
        self.tags.append((tag, attrs))

    def handle_endtag(self, tag):
        if tag in {"g", "a"}:
            self.groups.pop()


def _points(d):
    # Read the emitted vocabulary, including the Process station's quadratic bows.
    tokens = re.findall(r"[A-Za-z]|-?\d+(?:\.\d+)?", d)
    points, vertices, i = [], set(), 0
    while i < len(tokens):
        cmd = tokens[i]
        i += 1
        count = {"M": 2, "L": 2, "C": 6, "Q": 4}[cmd]
        nums = list(map(float, tokens[i : i + count]))
        i += count
        controls = list(zip(nums[::2], nums[1::2]))
        vertices.add(controls[-1])
        if cmd in {"M", "L"}:
            points.append(controls[0])
        else:
            start = points[-1]
            for k in range(1, 49):
                level = [start, *controls]
                t = k / 48
                while len(level) > 1:
                    level = [
                        ((1 - t) * a[0] + t * b[0], (1 - t) * a[1] + t * b[1])
                        for a, b in zip(level, level[1:])
                    ]
                points.append(level[0])
    return points, vertices


def _shared_run(a, b, c, d, shared=()):
    # Collinear intervals: positive overlap OR an end-to-end join. Perpendicular
    # crossings remain the critique's job. Degenerate segments carry no stroke.
    dx, dy = b[0] - a[0], b[1] - a[1]
    if a == b or c == d:
        return False
    if abs(dx * (d[1] - c[1]) - dy * (d[0] - c[0])) > 1e-7:
        return False
    if abs(dx * (c[1] - a[1]) - dy * (c[0] - a[0])) > 1e-7:
        return False
    axis = 0 if abs(dx) >= abs(dy) else 1
    lo = max(min(a[axis], b[axis]), min(c[axis], d[axis]))
    hi = min(max(a[axis], b[axis]), max(c[axis], d[axis]))
    if abs(hi - lo) < 1e-8 and any(
        abs(p[axis] - lo) < 1e-8 and abs(dx * (p[1] - a[1]) - dy * (p[0] - a[0])) < 1e-7
        for p in shared
    ):
        return False  # only a point that is both wires' actual terminal
    return lo <= hi + 1e-8


def _violations(body):
    tags = _Tags(re.sub(r"<defs>.*?</defs>", "", body, flags=re.S)).tags
    rects = [
        tuple(float(attrs[k]) for k in ("x", "y", "width", "height"))
        for tag, attrs in tags
        if tag == "rect" and "x" in attrs and float(attrs.get("width", 0)) > 20
    ]

    def endpoint(point):
        x, y = point
        for index, (rx, ry, rw, rh) in enumerate(rects):
            if rx - 10 <= x <= rx + rw + 10 and ry - 10 <= y <= ry + rh + 10:
                return index
        return point

    wires = []
    for tag, attrs in tags:
        if tag != "path" or not set(attrs.get("class", "").split()) & {
            "wire",
            "edge",
            "swedge",
            "kedge",
            "ctxwire",
            "ctxrel",
            "stedge",
        }:
            continue
        points, vertices = _points(attrs["d"])
        ends = (
            {attrs["data-from"], attrs["data-to"]}
            if "data-from" in attrs
            else {endpoint(points[0]), endpoint(points[-1])}
        )
        name = attrs.get("data-edge", tuple(sorted(map(str, ends))))
        wires.append((name, points, vertices))
    bad = []
    for (name, points, vertices), (other, other_points, other_vertices) in combinations(
        wires, 2
    ):
        shared = set((points[0], points[-1])) & set((other_points[0], other_points[-1]))
        # Only authored command ends can form an end-to-end join. Sampling a
        # curve must not turn a perpendicular interior crossing into such a join.
        if (vertices & other_vertices) - shared or any(
            _shared_run(a, b, c, d, shared)
            for a, b in zip(points, points[1:])
            for c, d in zip(other_points, other_points[1:])
        ):
            bad.append((name, other))
    return len(wires), bad


@pytest.fixture(scope="module")
def emitted():
    gt = load_script("gen_trajectory")
    ct = load_script("check_trajectory")
    wis, errors = ct.load_wis(ct.read_registry_rows(ROOT / ct.WI_CSV))
    assert not errors
    return gt.build_html(ROOT, wis)


@pytest.mark.parametrize("view", ["dag", "sw", "context", "process"])
def test_unrelated_emitted_edges_have_separate_lanes(emitted, view):
    panel_id = "sw" if view == "context" else view
    panel = emitted.split('id="' + panel_id + '"', 1)[1].split("</section>", 1)[0]
    swept, bad = 0, []
    for index, (_tag, body) in enumerate(_svg_subtrees(panel)):
        context = 'class="ctxent"' in body
        if view in {"sw", "context"} and context != (view == "context"):
            continue
        count, collisions = _violations(body)
        swept += count
        bad.extend((index, pair) for pair in collisions)
    assert swept, view
    assert not bad, (view, bad)


def test_lane_oracle_detects_short_overlaps_and_end_to_end_joins():
    assert _shared_run((452, 49), (452, 71), (452, 60), (452, 82))
    assert _shared_run((220, 49), (220, 71), (220, 71), (220, 93))
    assert not _shared_run((0, 0), (10, 0), (5, -5), (5, 5))
    assert not _shared_run((0, 0), (10, 0), (10.1, 0), (20, 0))
    assert not _shared_run((0, 0), (10, 0), (10, 0), (20, 0), {(10, 0)})
    assert _shared_run((0, 0), (10, 0), (0, 0), (5, 0), {(0, 0)})


def test_emitted_join_oracle_includes_perpendicular_corners():
    markup = (
        '<path class="wire" data-from="A" data-to="B" d="M0,0 L10,0 L10,10"/>'
        '<path class="wire" data-from="C" data-to="D" d="M5,-5 L10,0 L20,0"/>'
    )
    assert _violations(markup)[1] == [(("A", "B"), ("C", "D"))]
    assert _shared_run((0, 0), (10, 0), (10, 0), (20, 0), {(10, 5)})
