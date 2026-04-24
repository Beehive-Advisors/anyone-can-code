"""cache-levels-nested — CPU request walks L1 -> L2 -> L3 -> RAM, cycle counter climbs."""
from manim import (
    DOWN, LEFT, RED, RIGHT, UP, Arrow, Create, FadeIn, FadeOut, GREEN, Scene,
    Text, VGroup, Write,
)

from anyone_can_code_assets import CPU, Cache, RAM
from anyone_can_code_assets.hardware.bus import Bus


class CacheLevelsNested(Scene):
    def construct(self):
        cpu = CPU(cores=1).scale(0.7).shift(LEFT * 5.0)
        l1 = Cache(level="L1", width=1.4).scale(0.7).next_to(cpu, RIGHT, buff=0.5)
        l2 = Cache(level="L2", width=1.6).scale(0.7).next_to(l1, RIGHT, buff=0.5)
        l3 = Cache(level="L3", width=1.8).scale(0.7).next_to(l2, RIGHT, buff=0.5)
        ram = RAM(chips=6).scale(0.6).next_to(l3, RIGHT, buff=0.7)

        self.play(
            Create(cpu), Create(l1), Create(l2), Create(l3), Create(ram),
            run_time=1.4,
        )

        counter_label = Text("cycles:", font_size=24).to_edge(UP).shift(LEFT * 1)
        counter_val = Text("0", font_size=30, color=GREEN).next_to(counter_label, RIGHT, buff=0.2)
        self.play(FadeIn(counter_label), FadeIn(counter_val), run_time=0.4)

        # Miss in L1
        self.play(l1.get_box().animate.set_stroke(RED, width=4), run_time=0.4)
        new_counter = Text("4", font_size=30, color=GREEN).move_to(counter_val.get_center())
        self.play(FadeOut(counter_val), FadeIn(new_counter), run_time=0.2)
        counter_val = new_counter

        # Miss in L2
        self.play(l2.get_box().animate.set_stroke(RED, width=4), run_time=0.4)
        new_counter = Text("14", font_size=30, color=GREEN).move_to(counter_val.get_center())
        self.play(FadeOut(counter_val), FadeIn(new_counter), run_time=0.2)
        counter_val = new_counter

        # Miss in L3
        self.play(l3.get_box().animate.set_stroke(RED, width=4), run_time=0.4)
        new_counter = Text("45", font_size=30, color=GREEN).move_to(counter_val.get_center())
        self.play(FadeOut(counter_val), FadeIn(new_counter), run_time=0.2)
        counter_val = new_counter

        # Hit in RAM
        self.play(ram._pcb.animate.set_stroke(GREEN, width=4), run_time=0.4)
        new_counter = Text("~350", font_size=30, color=GREEN).move_to(counter_val.get_center())
        self.play(FadeOut(counter_val), FadeIn(new_counter), run_time=0.2)

        self.wait(2.0)
