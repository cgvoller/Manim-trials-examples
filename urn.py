from manim import *

class DrawUrn(Scene):
    def construct(self):
        def color_interpolate(start_color, end_color, alpha):
            start_rgb = color_to_rgb(start_color)
            end_rgb = color_to_rgb(end_color)
            interp_rgb = [(1 - alpha) * s + alpha * e for s, e in zip(start_rgb, end_rgb)]
            return rgb_to_color(interp_rgb)
        text = Text("Urn randomisation in clinical trials", font_size=32)
# Import urn svg
        urn = SVGMobject("urn.svg")
        urn.set_stroke(color="#3B2F2F", width=3)
        urn.set_fill(color="#C18F5A", opacity=1)
        urn.scale(2)
# Draw outline and fill
        text.next_to(urn, DOWN, buff=0.5)
        self.play(Write(text),run_time=2)
        self.play(DrawBorderThenFill(urn, run_time=4))
# Colour light and dark
        lighter_color = "#E6BE8A"  # Lighter color
        darker_color = "#3B2F2F"  # Darker color
        lighter_indices = [5,6,7,10]
        parts = [urn[i] for i in lighter_indices]
        anims = [
            UpdateFromAlphaFunc(part, lambda m, a: m.set_fill(color_interpolate("#C18F5A", lighter_color, a)))
            for part in parts
        ]
        dark_parts = [urn[i] for i in range(1, 5)]
        dark_anims = [
            UpdateFromAlphaFunc(part, lambda m, a: m.set_fill(color_interpolate("#C18F5A", darker_color, a)))
            for part in dark_parts
        ]
        self.play(*anims,*dark_anims, run_time=1)
        lid_parts = VGroup(urn[8], urn[10])
        rest_of_urn = VGroup(*[urn[i] for i in range(1, len(urn))])
        self.add(rest_of_urn, lid_parts)
# Move lid
# Move urn and scale
        new_text = Tex("Urn algorithm: ", font_size=32)
        ul = Underline(new_text)
        ul_text = VGroup(ul,new_text)
        ul_text.shift(UP*2 + RIGHT*2)
        self.play(urn.animate.scale(0.7).shift(LEFT * 4),
                  lid_parts.animate.scale(0.7).shift(UP * 1 + LEFT * 4).rotate(PI / 8),
                  Transform(text,ul_text),
                  run_time=2)
        self.wait(1)
        draw_text = "Draw a ball with replacement"
        # Define alpha + ball groups
        def make_alpha_ball(color):
            alpha = MathTex(r"\alpha")
            ball = Circle(radius=0.1, color=color, fill_opacity=1)
            ball.next_to(alpha, RIGHT, buff=0.2)
            return VGroup(alpha, ball), ball

        group_white, white_ball = make_alpha_ball(WHITE)
        group_red, red_ball = make_alpha_ball(RED)

        both_groups = VGroup(group_white, group_red).arrange(DOWN, aligned_edge=LEFT)
        both_groups.next_to(ul_text, DOWN, buff=1)

        self.play(Write(group_white[0]), GrowFromCenter(white_ball))
        self.wait(0.3)
        self.play(Write(group_red[0]), GrowFromCenter(red_ball))
        self.wait(0.5)

        # Move balls to starting point above scene
        white_anim = white_ball.copy()
        red_anim  = red_ball.copy()

        self.add(white_anim, red_anim )
        urn_front = urn[1]
        # Define final inside positions (center of urn)
        white_final = white_ball.copy().move_to(urn_front.get_center() + LEFT * 0.2 + DOWN * 1.2)
        red_final = red_ball.copy().move_to(urn_front.get_center() + RIGHT * 0.2 + DOWN * 1.5)
        white_final.set_z_index(-2)
        red_final.set_z_index(-2)
        white_final.set_opacity(1)
        red_final.set_opacity(1)

        # Create arcing paths
        white_path = CubicBezier(
            white_anim.get_center(),
            white_anim.get_center() + UP*2 + LEFT*1.3,
            urn_front.get_top() + UP + LEFT*0.8,
            urn_front.get_top() + DOWN * 1.5,
        )

        red_path = CubicBezier(
            red_anim.get_center(),
            red_anim.get_center() + UL * 2,
            urn_front.get_top() + UP + LEFT,
            urn_front.get_top() + DOWN * 1.5,
        )

        # Animate white ball
        self.play(MoveAlongPath(white_anim, white_path, run_time=1.8))
        self.play(white_anim.animate.scale(0.5), FadeOut(white_anim, shift=DOWN*0.2), FadeIn(white_final))
        self.wait(0.2)

        # Animate red ball
        self.play(MoveAlongPath(red_anim, red_path, run_time=1.8))
        self.play(red_anim.animate.scale(0.5), FadeOut(red_anim, shift=DOWN*0.2), FadeIn(red_final))
        self.wait(0.2)

        # Make urn transparent to reveal inside
        self.play(urn.animate.set_fill(opacity=0.3))
        # Add treatment labels
        label_white = Text("Treatment A", font_size=24).next_to(group_white, UP, buff=0.3)
        label_red = Text("Treatment B", font_size=24).next_to(group_red, UP, buff=0.3)

        # Group each alpha+ball with its label
        pair_white = VGroup(label_white, group_white)
        pair_red = VGroup(label_red, group_red)
        #side_side = VGroup(pair_white, pair_red)
       
        # Add to scene
        #self.play(side_side.animate.arrange(RIGHT, buff=1,center=True))

        # Animate down smoothly into position below ul_text
        self.play(
           pair_white.animate.move_to(ul_text.get_center() + DOWN*1.5 + LEFT * 1.5),
           pair_red.animate.move_to(ul_text.get_center() + DOWN*1.5 + RIGHT * 1.5),
            run_time=2,
            rate_func=smooth
        )
        #self.play(side_side.move_to(ul_text.get_center() + DOWN * 1.5))
        self.play(
            group_white.animate.move_to(pair_white[1].get_center()+LEFT*4),
            group_red.animate.move_to(pair_red[1].get_center()+LEFT*4),
            FadeOut(group_white[0]),
            FadeOut(group_red[0]),
            group_white[1].animate.move_to(pair_white[0].get_left()+LEFT*0.5),
            group_red[1].animate.move_to(pair_red[0].get_left()+LEFT*0.5),

          #  FadeIn(label_white, shift=UP * 0.3),
          #  FadeIn(label_red, shift=UP * 0.3),
            run_time=2,
            rate_func=smooth
        )
        self.wait(1)
        # Simulate drawing white ball
        start = white_final.get_center()
        control = start + UP * 2 + LEFT * 0.7
        end = pair_white.get_bottom() + DOWN * 0.5

# Quadratic Bezier ≈ Cubic Bezier with repeated control point
        arc_path = CubicBezier(start, control, control, end)
        # Copy the ball to animate (keep the original inside the urn)
        picked_ball = white_final.copy()
        picked_ball.set_z_index(5)
        self.add(picked_ball)

# Animate the ball moving along the arc
        self.play(MoveAlongPath(picked_ball, arc_path), run_time=2)

# Optionally, fade the picked ball into the final position (or keep it there)
        self.play(picked_ball.animate.move_to(end), run_time=0.3)
        def make_beta_ball(color):
            beta = MathTex(r"\beta")
            ball = Circle(radius=0.1, color=color, fill_opacity=1)
            ball.next_to(beta, RIGHT, buff=0.2)
            return VGroup(beta, ball)

        group_red2 = make_beta_ball(RED)
        group_red2.arrange(DOWN, aligned_edge=LEFT)
        group_red2.next_to(ul_text, DOWN*2, buff=1)

        self.play(Write(group_red2[0]), GrowFromCenter(group_red2[1]))
        self.wait(0.3)

# Path from current group position to urn
        start = group_red2.get_center()
        end = urn_front.get_center() + RIGHT * 0.1 + DOWN * 1.7

        red_path = CubicBezier(
            start,
            start + UL * 3,
            urn_front.get_top() + UP*1.1 + LEFT*1.1,
           end
        )

# Move the whole group
        self.play(MoveAlongPath(group_red2, red_path, run_time=1.8))
        self.wait(2)
        self.play(FadeOut(group_red2))
        self.play(urn.animate.set_fill(opacity=1))
        self.wait(2)

