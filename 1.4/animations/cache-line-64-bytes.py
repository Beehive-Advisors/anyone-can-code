"""cache-line-64-bytes — fetching one byte actually fetches the whole 64-byte line."""
from manim import (
    DOWN, GREEN, LEFT, RIGHT, UP, Create, FadeIn, FadeOut, Scene, Text, VGroup,
    YELLOW,
)

from anyone_can_code_assets import CPU, Cache, CacheLine, RAM


class CacheLineSixtyFourBytes(Scene):
    def construct(self):
        cpu = CPU(cores=1).scale(0.6).shift(LEFT * 5.0)
        cache = Cache(level="L1", width=2.2).scale(0.7).next_to(cpu, RIGHT, buff=0.6)
        ram_box = RAM(chips=4).scale(0.6).shift(RIGHT * 4.5)

        # The cache line lives inside RAM initially
        line_in_ram = CacheLine(slots=8).scale(0.7).move_to(ram_box.get_center() + DOWN * 1.3)

        self.play(Create(cpu), Create(cache), Create(ram_box), Create(line_in_ram), run_time=1.2)

        # CPU requests byte index 3
        req_label = Text("request byte #3", font_size=20).to_edge(UP)
        self.play(FadeIn(req_label), run_time=0.4)
        # Highlight slot 3 in the RAM line
        self.play(line_in_ram.get_slot(3).animate.set_stroke(YELLOW, width=4), run_time=0.5)
        self.wait(0.3)

        # The whole line slides into the cache
        line_in_cache = CacheLine(slots=8).scale(0.7).move_to(cache.get_center() + DOWN * 0.1)
        line_in_cache.get_slot(3).set_stroke(YELLOW, width=4)
        self.play(
            FadeOut(line_in_ram),
            FadeIn(line_in_cache),
            run_time=1.0,
        )
        self.wait(0.5)

        # CPU requests byte index 4 — already there, zero cost
        req2 = Text("request byte #4 — already in cache", font_size=20, color=GREEN).to_edge(UP)
        self.play(FadeOut(req_label), FadeIn(req2), run_time=0.3)
        self.play(line_in_cache.get_slot(4).animate.set_stroke(GREEN, width=4), run_time=0.5)

        zero_cost = Text("0 cost", font_size=24, color=GREEN).next_to(line_in_cache, DOWN, buff=0.3)
        self.play(FadeIn(zero_cost), run_time=0.4)

        self.wait(2.0)
