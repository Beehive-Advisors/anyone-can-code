"""latency-log-ladder — log-scale bars with human-scale analogies (1s to 4 months).

lib-free: this is a one-off log-scale chart with custom human-scale analogy labels.
No reusable asset in anyone_can_code_assets fits, and the research phase
intentionally kept it inline rather than adding a narrow-purpose LogLatencyChart
class to the library (see 1.4/proposed_new_assets.md audit trail in commit history).
"""
from manim import (
    DOWN, LEFT, RIGHT, UP, Create, FadeIn, Rectangle, Scene, Text, VGroup,
)


class LatencyLogLadder(Scene):
    def construct(self):
        # Data: name, nanoseconds, raw label, human analogy
        rows = [
            ("L1 Cache", 1, "1 ns", "1 second"),
            ("RAM", 100, "100 ns", "100 seconds"),
            ("SSD", 100_000, "100 µs", "28 hours"),
            ("HDD", 10_000_000, "10 ms", "4 months"),
        ]

        # Log scale normalization
        import math
        max_log = math.log10(rows[-1][1])
        max_bar_width = 9.0

        title = Text("Memory latency on a human scale", font_size=28).to_edge(UP)
        self.play(FadeIn(title), run_time=0.5)

        y_offset = 1.7
        bars = VGroup()
        for i, (name, ns, raw, human) in enumerate(rows):
            log_val = math.log10(ns)
            width = max(0.4, (log_val / max_log) * max_bar_width) if ns > 1 else 0.4

            name_label = Text(name, font_size=22).move_to([-6.0, y_offset, 0])
            bar = Rectangle(
                width=width,
                height=0.5,
                fill_color="#4A90E2",
                fill_opacity=0.7,
                stroke_color="#FFFFFF",
                stroke_width=2,
            )
            bar.move_to([-3.5 + width / 2, y_offset, 0])

            raw_label = Text(raw, font_size=18, color="#CCCCCC").next_to(bar, RIGHT, buff=0.15)
            if_scaled = Text(f"if this were {human}", font_size=16, color="#99FF99").next_to(raw_label, RIGHT, buff=0.2)

            self.play(
                FadeIn(name_label), Create(bar), FadeIn(raw_label), FadeIn(if_scaled),
                run_time=0.6,
            )
            bars.add(name_label, bar, raw_label, if_scaled)
            y_offset -= 1.0

        self.wait(2.5)
