"""hdd-internals — HDD reveals a platter + head arm; NVMe flashes 'no moving parts'."""
from manim import (
    DOWN, LEFT, RIGHT, UP, Create, FadeIn, FadeOut, Rotate, Scene, Text, PI,
)

from anyone_can_code_assets import HDD, NVMe


class HddInternals(Scene):
    def construct(self):
        hdd = HDD().shift(LEFT * 3.0)
        nvme = NVMe().shift(RIGHT * 3.5 + DOWN * 0.3)

        self.play(Create(hdd), Create(nvme), run_time=1.2)
        self.wait(0.3)

        # HDD timings appear
        seek_label = Text("seek: 9 ms", font_size=22).next_to(hdd, UP, buff=0.5)
        self.play(FadeIn(seek_label), run_time=0.3)

        # Animate the head arm swinging
        original_arm = hdd.get_head_arm().copy()
        self.play(
            Rotate(hdd.get_head_arm(), PI / 4, about_point=hdd.get_enclosure().get_right() + LEFT * 0.3 + UP * 0.6),
            run_time=1.2,
        )
        self.wait(0.3)

        rotate_label = Text("rotate: 4 ms", font_size=22).next_to(hdd, UP, buff=0.5)
        self.play(FadeOut(seek_label), FadeIn(rotate_label), run_time=0.3)
        self.play(Rotate(hdd.get_platter(), PI, about_point=hdd.get_spindle().get_center()), run_time=1.0)

        total_label = Text("~13 ms", font_size=26, color="#FFCC33").next_to(hdd, DOWN, buff=0.3)
        self.play(FadeOut(rotate_label), FadeIn(total_label), run_time=0.3)

        # NVMe side: flashes 'no moving parts' and '~100 μs'
        nomov = Text("no moving parts", font_size=20).next_to(nvme, UP, buff=0.5)
        time_label = Text("~100 μs", font_size=26, color="#66FF99").next_to(nvme, DOWN, buff=0.3)
        self.play(FadeIn(nomov), FadeIn(time_label), run_time=0.6)

        # Summary
        summary = Text("130× faster", font_size=28, color="#66FF99").shift(DOWN * 2.5)
        self.play(FadeIn(summary), run_time=0.6)
        self.wait(1.5)
