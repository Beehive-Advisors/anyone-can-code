"""the-stall — CPU steadily ticks, one miss freezes it, 'you could have issued' counter climbs."""
from manim import (
    DOWN, LEFT, RIGHT, UP, Create, FadeIn, FadeOut, Rectangle, Scene, Text, VGroup,
    YELLOW,
)

from anyone_can_code_assets import CPU, Cache, RAM


class TheStall(Scene):
    def construct(self):
        cpu = CPU(cores=1).scale(0.7).shift(LEFT * 4.0)
        cache = Cache(level="L1", width=1.6).scale(0.7).next_to(cpu, RIGHT, buff=0.6)
        ram = RAM(chips=4).scale(0.6).shift(RIGHT * 4.5)

        self.play(Create(cpu), Create(cache), Create(ram), run_time=1.0)

        instr_label = Text("instructions issued:", font_size=22).to_edge(UP).shift(LEFT * 2)
        instr_val = Text("0", font_size=30, color="#66FF99").next_to(instr_label, RIGHT, buff=0.2)
        self.play(FadeIn(instr_label), FadeIn(instr_val), run_time=0.4)

        # Tick 4 instructions smoothly
        for n in range(1, 5):
            new_val = Text(str(n), font_size=30, color="#66FF99").move_to(instr_val.get_center())
            self.play(FadeOut(instr_val), FadeIn(new_val), run_time=0.25)
            instr_val = new_val

        # Cache miss fires
        miss_label = Text("CACHE MISS — wait for RAM", font_size=24, color=YELLOW).shift(DOWN * 2.8)
        self.play(FadeIn(miss_label), cache.get_box().animate.set_stroke(YELLOW, width=5), run_time=0.4)

        # Progress bar
        bar_bg = Rectangle(width=6, height=0.4, stroke_color="#CCCCCC", fill_opacity=0).shift(DOWN * 2.0)
        bar_fill = Rectangle(width=0.01, height=0.4, fill_color=YELLOW, fill_opacity=0.9, stroke_width=0)
        bar_fill.align_to(bar_bg, LEFT)
        bar_fill.shift(DOWN * 2.0)
        bar_label = Text("waiting for DRAM (~350 cycles)", font_size=18).next_to(bar_bg, UP, buff=0.15)
        self.play(Create(bar_bg), FadeIn(bar_label), run_time=0.3)

        missed_label = Text("instructions you could have issued:", font_size=18, color="#FF6666").shift(UP * 0.5 + LEFT * 1)
        missed_val = Text("0", font_size=24, color="#FF6666").next_to(missed_label, RIGHT, buff=0.2)
        self.play(FadeIn(missed_label), FadeIn(missed_val), run_time=0.3)

        # Crawl the progress bar while the missed counter climbs
        for fraction, count in [(0.2, 200), (0.5, 500), (0.8, 800), (1.0, 1050)]:
            new_fill = Rectangle(
                width=6 * fraction, height=0.4, fill_color=YELLOW, fill_opacity=0.9, stroke_width=0
            )
            new_fill.align_to(bar_bg, LEFT).shift(DOWN * 2.0)
            new_missed = Text(str(count), font_size=24, color="#FF6666").move_to(missed_val.get_center())
            self.play(
                bar_fill.animate.stretch_to_fit_width(6 * fraction).align_to(bar_bg, LEFT),
                FadeOut(missed_val), FadeIn(new_missed),
                run_time=0.7,
            )
            missed_val = new_missed

        takeaway = Text("1 miss = ~1000 instructions of lost work", font_size=24, color="#FFCC33").to_edge(DOWN)
        self.play(FadeIn(takeaway), run_time=0.6)
        self.wait(2.0)
