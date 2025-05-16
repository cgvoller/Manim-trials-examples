from manim import *
import numpy as np


class ShadedBoundaryAnimation(Scene):
    def construct(self):
        # Define k values and boundaries (boundaries start at k=1)
        k_values = np.array([0, 1, 2, 3, 4, 5])
        a_crit = np.array([-1.61511306, -0.07126633, 0.81610852, 1.46393433, 1.986610])  # No k=0 boundary
        b_crit = np.array([4.442196, 3.141107, 2.564703, 2.221098, 1.986610])  # No k=0 boundary
        a_crit_ext = np.insert(a_crit, 0, a_crit[0])
        b_crit_ext = np.insert(b_crit, 0, b_crit[0])
        # Observed paths (starting from k=0, y=0)
        observed_red_cross = np.array([0, 1.5, 2.3, 2.7, 4.5])  # Crosses upper boundary
        observed_green_cross = np.array([0, -1.2, -1.8, -2.2, -2.5])  # Crosses lower boundary
        observed_no_cross = np.array([0,1.8, 1, 1.5, 1.8, 2.1])  # Stays within bounds

        # Create axes
        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[-3, 5, 1],
            axis_config={"color": WHITE},
            x_axis_config={
                "numbers_to_include": [1, 2, 3, 4, 5],  # Only show ticks for x values from 1 to 5
            }
        )
        x_label = Tex("Analysis (k)").next_to(axes.x_axis, DOWN, buff=0.5)
        y_label = MathTex("Z_k").next_to(axes.y_axis, LEFT, buff=0.1)
        
        self.play(Create(axes), Write(x_label), Write(y_label))

        # Plot boundaries (starting at k=1)
        a_crit_line = axes.plot_line_graph(
            x_values=k_values[1:], y_values=a_crit, add_vertex_dots=False, line_color=GREEN, stroke_width=4
        )
        b_crit_line = axes.plot_line_graph(
            x_values=k_values[1:], y_values=b_crit, add_vertex_dots=False, line_color=RED, stroke_width=4
        )
        self.play(Create(a_crit_line), Create(b_crit_line))
        # Labels on graph
        reject_text = MathTex(r"\text{Reject } H_0", font_size=24)
        reject_text.move_to(axes.c2p(3, b_crit[2]) + UP * 0.5)
        self.play(Write(reject_text))

        accept_text = MathTex(r"\text{Accept } H_0", font_size=24)
        accept_text.move_to(axes.c2p(3, a_crit[2]) + DOWN * 0.4)
        self.play(Write(accept_text))


        
        upper_curve = axes.plot_line_graph(
            x_values=k_values[1:], y_values=b_crit,
            add_vertex_dots=False, line_color=RED, stroke_width=0  # Invisible curve
        )

        lower_curve = axes.plot_line_graph(
            x_values=k_values[1:], y_values=a_crit,
            add_vertex_dots=False, line_color=GREEN, stroke_width=0  # Invisible curve
        )
        fill_tracker = ValueTracker(0.0)

        def get_blue_region():
            lower_points = [axes.c2p(x, a) for x, a in zip(k_values[1:], a_crit)]
            upper_points = [axes.c2p(x, a + (b - a) * fill_tracker.get_value())
                    for x, a, b in zip(k_values[1:], a_crit, b_crit)]
            return Polygon(*lower_points, *reversed(upper_points),
                   color=BLUE, fill_opacity=0.1, stroke_opacity=0)

        blue_region = always_redraw(get_blue_region)
        self.add(blue_region)

        def get_left_blue_strip():
            top_y = axes.y_range[1]
            bottom_y = axes.y_range[0]
            k0 = 0
            k1 = 1
            return Polygon(
                axes.c2p(k0, bottom_y),
                axes.c2p(k1, bottom_y),
                axes.c2p(k1, bottom_y + (top_y - bottom_y) * fill_tracker.get_value()),
                axes.c2p(k0, bottom_y + (top_y - bottom_y) * fill_tracker.get_value()),
                color=BLUE, fill_opacity=0.1, stroke_opacity=0
            )

        left_blue_strip = always_redraw(get_left_blue_strip)
        self.add(left_blue_strip)

        def get_red_region():
            top_y = axes.y_range[1]
            upper_points = [axes.c2p(x, b) for x, b in zip(k_values[1:], b_crit)]
            top_points = [axes.c2p(x, b + (top_y - b) * fill_tracker.get_value())
                  for x, b in zip(k_values[1:], b_crit)]
            return Polygon(*upper_points, *reversed(top_points),
                   color=RED, fill_opacity=0.2, stroke_opacity=0)

        red_region = always_redraw(get_red_region)
        self.add(red_region)

        def get_green_region():
            bottom_y = axes.y_range[0]
            lower_points = [axes.c2p(x, a) for x, a in zip(k_values[1:], a_crit)]
            bottom_points = [axes.c2p(x, a + (bottom_y - a) * fill_tracker.get_value())
                     for x, a in zip(k_values[1:], a_crit)]
            return Polygon(*lower_points, *reversed(bottom_points),
                   color=GREEN, fill_opacity=0.2, stroke_opacity=0)

        green_region = always_redraw(get_green_region)
        self.add(green_region)
        # Add shaded regions in the correct back-to-front order
        #self.add(red_region, green_region, blue_region)
        self.play(fill_tracker.animate.set_value(1.0), run_time=2)


        # Function to animate each scenario
        def animate_path(observed_values):
            observed_dot = Dot(axes.c2p(k_values[0], observed_values[0]), color=BLUE)
            self.add(observed_dot)

            prev_point = axes.c2p(k_values[0], observed_values[0])
            line_segments = []
            for i in range(1, len(k_values)):
                target_point = axes.c2p(k_values[i], observed_values[i])
                new_line = Line(prev_point, target_point, color=BLUE)
                line_segments.append(new_line)

                self.play(observed_dot.animate.move_to(target_point), Create(new_line), run_time=1)

                # Check only for k >= 1 (boundaries start at k=1)
                if i >= 1:
                    print(f"k = {k_values[i]}, observed = {observed_values[i]}, a_crit = {a_crit[i-1]}, b_crit = {b_crit[i-1]}")

                    if observed_values[i] > b_crit[i-1]:  # Crossed upper boundary
                        new_line.set_color(RED)
                        self.play(observed_dot.animate.set_color(RED), new_line.animate.set_color(RED), run_time=0.5)
                        break
                    elif observed_values[i] < a_crit[i-1]:  # Crossed lower boundary
                        new_line.set_color(GREEN)
                        self.play(observed_dot.animate.set_color(GREEN), new_line.animate.set_color(GREEN), run_time=0.5)
                        break

                prev_point = target_point

            self.wait(1)
            self.play(*[FadeOut(obj) for obj in line_segments], FadeOut(observed_dot))

        # Run all three scenarios separately
        animate_path(observed_red_cross)  # Scenario 1: Turns red
        animate_path(observed_green_cross)  # Scenario 2: Turns green
        animate_path(observed_no_cross)  # Scenario 3: Stays blue

        self.wait(2)

