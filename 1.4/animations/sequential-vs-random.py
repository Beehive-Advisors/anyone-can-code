"""sequential-vs-random — two identical array walks, one in order, one random, 10x time gap."""
import random

from manim import (
    DOWN, GREEN, LEFT, RIGHT, UP, Circle, Create, FadeIn, FadeOut, Scene, Text,
    VGroup, YELLOW,
)

from anyone_can_code_assets import ArrayStrip


class SequentialVsRandom(Scene):
    def construct(self):
        random.seed(42)

        left_label = Text("sequential", font_size=22).shift(UP * 2.8 + LEFT * 3.5)
        right_label = Text("random", font_size=22).shift(UP * 2.8 + RIGHT * 3.5)

        left_arr = ArrayStrip(length=10, show_indices=True).scale(0.75).shift(LEFT * 3.5 + UP * 1.5)
        right_arr = ArrayStrip(length=10, show_indices=True).scale(0.75).shift(RIGHT * 3.5 + UP * 1.5)

        left_cursor = Circle(radius=0.12, color=YELLOW, fill_opacity=0.8).move_to(
            left_arr.get_cell(0).get_center() + DOWN * 0.7
        )
        right_cursor = Circle(radius=0.12, color=YELLOW, fill_opacity=0.8).move_to(
            right_arr.get_cell(0).get_center() + DOWN * 0.7
        )

        hits_label_l = Text("hits: 0", font_size=18, color=GREEN).shift(LEFT * 3.5 + DOWN * 0.5)
        misses_label_r = Text("misses: 0", font_size=18, color=YELLOW).shift(RIGHT * 3.5 + DOWN * 0.5)

        timer_l = Text("0 cyc", font_size=20).shift(LEFT * 3.5 + DOWN * 1.3)
        timer_r = Text("0 cyc", font_size=20).shift(RIGHT * 3.5 + DOWN * 1.3)

        self.play(
            Create(left_arr), Create(right_arr),
            FadeIn(left_label), FadeIn(right_label),
            FadeIn(left_cursor), FadeIn(right_cursor),
            FadeIn(hits_label_l), FadeIn(misses_label_r),
            FadeIn(timer_l), FadeIn(timer_r),
            run_time=1.2,
        )

        left_order = list(range(10))
        right_order = [7, 2, 9, 4, 0, 6, 1, 8, 3, 5]

        hits = 0
        misses = 0
        cycles_l = 0
        cycles_r = 0

        for step in range(10):
            # Advance left cursor: sequential access, mostly hits
            left_i = left_order[step]
            is_hit = (step % 4) != 0  # 3 out of 4 are hits (spatial locality)
            new_left_cursor = Circle(radius=0.12, color=YELLOW, fill_opacity=0.8).move_to(
                left_arr.get_cell(left_i).get_center() + DOWN * 0.7
            )
            left_arr.get_cell(left_i).set_fill(GREEN if is_hit else YELLOW, opacity=0.5)
            if is_hit:
                hits += 1
                cycles_l += 4
            else:
                cycles_l += 40  # L2 miss

            # Advance right cursor: random access, mostly misses
            right_i = right_order[step]
            new_right_cursor = Circle(radius=0.12, color=YELLOW, fill_opacity=0.8).move_to(
                right_arr.get_cell(right_i).get_center() + DOWN * 0.7
            )
            right_arr.get_cell(right_i).set_fill(YELLOW, opacity=0.5)
            misses += 1
            cycles_r += 100  # RAM miss

            new_hits = Text(f"hits: {hits}", font_size=18, color=GREEN).move_to(hits_label_l.get_center())
            new_misses = Text(f"misses: {misses}", font_size=18, color=YELLOW).move_to(misses_label_r.get_center())
            new_timer_l = Text(f"{cycles_l} cyc", font_size=20).move_to(timer_l.get_center())
            new_timer_r = Text(f"{cycles_r} cyc", font_size=20).move_to(timer_r.get_center())

            self.play(
                left_cursor.animate.move_to(new_left_cursor.get_center()),
                right_cursor.animate.move_to(new_right_cursor.get_center()),
                FadeOut(hits_label_l), FadeIn(new_hits),
                FadeOut(misses_label_r), FadeIn(new_misses),
                FadeOut(timer_l), FadeIn(new_timer_l),
                FadeOut(timer_r), FadeIn(new_timer_r),
                run_time=0.25,
            )
            hits_label_l, misses_label_r = new_hits, new_misses
            timer_l, timer_r = new_timer_l, new_timer_r

        summary = Text(f"{cycles_r // cycles_l}× slower", font_size=28, color=YELLOW).shift(DOWN * 2.5)
        self.play(FadeIn(summary), run_time=0.6)
        self.wait(1.5)
