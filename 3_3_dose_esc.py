from manim import *

class ThreePlusThree(Scene):
    def construct(self):
# Create axes
        axes = Axes(
            x_range=[0, 7, 1],
            y_range=[0, 5, 1],
            axis_config={"color": WHITE},
            x_axis_config={
                "numbers_to_include": [1, 2, 3, 4, 5],  # Only show ticks for x values from 1 to 5
            }
        )
        labels = axes.get_axis_labels(
            Tex("Time").scale(0.9), Text("Dose").scale(0.8)
        )
        self.play(Create(axes), Write(labels),run_time=1.5)
        self.wait(1)
# Define the function to add a blue arrow between cohorts
        def add_cohort_arrow(cohort_dots, y=0.2, color=BLUE, run_time=0.5):
            first_dot = cohort_dots[0]
            last_dot = cohort_dots[-1]
            start_point = first_dot.get_x()
            end_point = last_dot.get_x()
            arrow = Arrow(
                start=axes.c2p(start_point, y),
                end=axes.c2p(end_point, y),
                buff=0,
                stroke_width=6,
                tip_length=0.15,
                color=color
            )
            self.play(GrowArrow(arrow), run_time=run_time)
            self.wait(0.5)
# Draw legend
        # Green Dot
        non_dlt_dot = Dot(color=GREEN, radius=0.15)
        non_dlt_label = Text("Non-DLT").scale(0.6).next_to(non_dlt_dot, RIGHT, buff=0.1)
        # Red dot
        red_dot = Dot(color=RED, radius=0.15)
        dlt_label = Text("DLT").scale(0.6).next_to(red_dot, RIGHT, buff=0.1)
        # Dose escalation arrow
        up_arrow =  Arrow(
            start=ORIGIN,
            end=UP * 0.4,
            buff=0,
            stroke_width=5,     
            tip_length=0.15         
        )   
        esc_label = Text("Dose escalation").scale(0.6).next_to(up_arrow, RIGHT, buff=0.1)
        # Patient cohort
        cohort_square = Square(
            side_length=0.3,
            stroke_color=RED,
            stroke_width=4,
            fill_opacity=0
        )
        cohort_label = Text("Patient cohort").scale(0.6).next_to(cohort_square, RIGHT, buff=0.1)
        # Stack them vertically
        legend = VGroup(
            VGroup(non_dlt_dot, non_dlt_label),
            VGroup(red_dot, dlt_label),
            VGroup(up_arrow, esc_label),
            VGroup(cohort_square, cohort_label),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        legend.to_corner(UR, buff=0.5)
        for item in legend:
            self.play(FadeIn(item), run_time=0.5)
            self.wait(0.3)
        self.wait(3)

# Draw first dose
        positions = [0.25, 0.5, 0.75]
        dots = VGroup()
        for x in positions:
            # c2p(x, y) converts (x,y) in data coords → scene coords
            dot = Dot(
                point=axes.c2p(x, 0.5),
                radius=0.20, 
                color=GREEN)
            self.play(FadeIn(dot), run_time=0.5)
            self.wait(0.5)
            dots.add(dot)
        box = SurroundingRectangle(
            dots,
            color=RED,
            stroke_width=4,
            buff=0.15  # space between dots and rectangle edge
        )
        self.play(Create(box), run_time=1)
        self.wait(2)
        # --- Up arrow above the third dot ---
        third_dot = dots[2]
        arrow = Arrow(
            start=third_dot.get_top() + UP * 0.05,
            end=third_dot.get_top() + UP * 1,
            buff=0,
            stroke_width=4,
            tip_length=0.15,
            color=YELLOW
        )
        self.play(GrowArrow(arrow), run_time=0.7)
        self.wait(0.5)

# Second cohort
        new_positions = [1.25, 1.5, 1.75]
        second_dots = VGroup()
        for x in new_positions:
            dot = Dot(point=axes.c2p(x, 1.5), radius=0.20, color=GREEN)
            self.play(FadeIn(dot), run_time=0.5)
            self.wait(0.2)
            second_dots.add(dot)
        second_box = SurroundingRectangle(second_dots, color=RED, stroke_width=4, buff=0.15)
        self.play(Create(second_box), run_time=1)
        # --- Up arrow above the third dot ---
        third_dot = second_dots[2]
        arrow = Arrow(
            start=third_dot.get_top() + UP * 0.05,
            end=third_dot.get_top() + UP * 1,
            buff=0,
            stroke_width=4,
            tip_length=0.15,
            color=YELLOW
        )
        self.play(GrowArrow(arrow), run_time=0.7)
        self.wait(0.5)
# Third cohort at y=2.5 between x=2 and x=3
        third_positions = [2.25, 2.5, 2.75]
        third_dots = VGroup()
        colors = [GREEN, GREEN, RED]  # Third dot is red

        for x, color in zip(third_positions, colors):
            dot = Dot(point=axes.c2p(x, 2.5), radius=0.20, color=color)
            self.play(FadeIn(dot), run_time=0.5)
            self.wait(0.2)
            third_dots.add(dot)
        third_box = SurroundingRectangle(third_dots, color=RED, stroke_width=4, buff=0.15)
        self.play(Create(third_box), run_time=1)
        self.wait(1.5)
        plus = Text("+").scale(1.2)
        plus.next_to(third_dots[-1], RIGHT, buff=0.3)
        self.play(Write(plus), run_time=0.5)
        self.wait(0.5)

# Fourth cohort at y=3.5 between x=3 and x=4
        fourth_positions = [3.55, 3.80, 4.05]
        fourth_dots = VGroup()
        colors = [GREEN, RED, RED]  # Two reds
        for x, color in zip(fourth_positions, colors):
            dot = Dot(point=axes.c2p(x, 2.5), radius=0.20, color=color)
            self.play(FadeIn(dot), run_time=0.5)
            self.wait(0.2)
            fourth_dots.add(dot)
        fourth_box = SurroundingRectangle(fourth_dots, color=RED, stroke_width=4, buff=0.15)
        dashed_box = DashedVMobject(fourth_box, num_dashes=20)
        self.play(Create(dashed_box), run_time=1)
        self.wait(0.5)
        # --- Up arrow above the third dot ---
        fourth_dot = fourth_dots[2]
        arrow = Arrow(
            start=fourth_dot.get_top() + UP * 0.05,
            end=fourth_dot.get_top() + UP * 1,
            buff=0,
            stroke_width=4,
            tip_length=0.15,
            color=YELLOW
        )
        self.play(GrowArrow(arrow), run_time=0.7)
# Fifth Cohort
        fifth_positions = [4.35, 4.6, 4.85]
        fifth_dots = VGroup()
        for x in fifth_positions:
            dot = Dot(point=axes.c2p(x, 3.5), radius=0.20, color=GREEN)
            self.play(FadeIn(dot), run_time=0.5)
            self.wait(0.2)
            fifth_dots.add(dot)
        fifth_box = SurroundingRectangle(fifth_dots, color=RED, stroke_width=4, buff=0.15)
        self.play(Create(fifth_box), run_time=1)
        self.wait(0.5)
# End
        self.wait(1.5)