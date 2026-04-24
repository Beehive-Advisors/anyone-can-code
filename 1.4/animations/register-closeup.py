"""register-closeup — ALU in the center with register neighbors, values flowing in and out."""
from manim import (
    DOWN, LEFT, RIGHT, UP, Arrow, Create, FadeIn, FadeOut, Scene, VGroup, Write,
)

from anyone_can_code_assets import ALU, Register


class RegisterCloseup(Scene):
    def construct(self):
        alu = ALU()
        r0 = Register(name="R0", value="—", width=1.0).next_to(alu, UP, buff=1.3).shift(LEFT * 2.0)
        r1 = Register(name="R1", value="—", width=1.0).next_to(alu, UP, buff=1.3).shift(LEFT * 0.6)
        r2 = Register(name="R2", value="—", width=1.0).next_to(alu, UP, buff=1.3).shift(RIGHT * 0.8)
        r3 = Register(name="R3", value="—", width=1.0).next_to(alu, UP, buff=1.3).shift(RIGHT * 2.2)

        regs = VGroup(r0, r1, r2, r3)

        self.play(Create(alu), run_time=0.8)
        self.play(Create(regs), run_time=1.2)
        self.wait(0.3)

        # First cycle: R1=5, R2=7, result -> R0=12
        new_r1 = Register(name="R1", value="5", width=1.0).move_to(r1.get_center())
        new_r2 = Register(name="R2", value="7", width=1.0).move_to(r2.get_center())
        self.play(FadeOut(r1), FadeOut(r2), run_time=0.2)
        self.play(FadeIn(new_r1), FadeIn(new_r2), run_time=0.4)

        arrow1 = Arrow(new_r1.get_bottom(), alu.get_top() + LEFT * 0.3, buff=0.05, stroke_width=3)
        arrow2 = Arrow(new_r2.get_bottom(), alu.get_top() + RIGHT * 0.3, buff=0.05, stroke_width=3)
        self.play(Create(arrow1), Create(arrow2), run_time=0.8)
        self.wait(0.3)

        arrow_out = Arrow(alu.get_bottom(), alu.get_bottom() + DOWN * 0.6, buff=0.05, stroke_width=3)
        self.play(Create(arrow_out), run_time=0.5)

        new_r0 = Register(name="R0", value="12", width=1.0).move_to(r0.get_center())
        self.play(FadeOut(r0), FadeIn(new_r0), run_time=0.4)
        self.wait(0.8)

        # Hold final frame
        self.wait(1.5)
