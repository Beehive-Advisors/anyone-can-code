"""hierarchy-pyramid — build the five-tier memory hierarchy pyramid."""
from manim import FadeIn, Scene

from anyone_can_code_assets import HierarchyPyramid


class HierarchyPyramidScene(Scene):
    def construct(self):
        pyramid = HierarchyPyramid(height=5.0, width=6.5)
        # Tiers fade in one by one, top to bottom
        for i in range(pyramid.tier_count()):
            self.play(
                FadeIn(pyramid.get_tier(i)),
                FadeIn(pyramid.get_tier_label(i)),
                run_time=0.5,
            )
        # Then the axis annotations
        self.play(
            FadeIn(pyramid._axis_fast),
            FadeIn(pyramid._axis_slow),
            FadeIn(pyramid._axis_small),
            FadeIn(pyramid._axis_big),
            run_time=0.8,
        )
        self.wait(2.0)
