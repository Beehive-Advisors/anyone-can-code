"""sram-vs-dram-cell — SRAM stable, DRAM capacitor leaks and refreshes."""
from manim import (
    DOWN, LEFT, RIGHT, UP, Arrow, Create, FadeIn, FadeOut, Scene, Text, VGroup,
)

from anyone_can_code_assets import MemoryCell


class SramVsDramCell(Scene):
    def construct(self):
        sram = MemoryCell(kind="sram").shift(LEFT * 3.0)
        dram = MemoryCell(kind="dram").shift(RIGHT * 3.0)

        self.play(Create(sram), Create(dram), run_time=1.0)
        self.wait(0.5)

        # DRAM cycle 1: leak
        for _ in range(2):
            # Leak from full to half over 1.5 s
            cap = dram.get_capacitor()
            self.play(
                cap.animate.set_fill(opacity=0.2),
                run_time=1.2,
            )
            # Refresh arrow appears and bumps it back up
            arrow = Arrow(
                dram.get_right() + RIGHT * 0.4 + UP * 0.5,
                dram.get_right() + RIGHT * 0.05 + UP * 0.2,
                buff=0.0,
                stroke_width=4,
            )
            refresh_label = Text("refresh", font_size=18).next_to(arrow, UP, buff=0.05)
            self.play(Create(arrow), FadeIn(refresh_label), run_time=0.3)
            self.play(cap.animate.set_fill(opacity=0.85), run_time=0.4)
            self.play(FadeOut(arrow), FadeOut(refresh_label), run_time=0.3)

        self.wait(1.5)
