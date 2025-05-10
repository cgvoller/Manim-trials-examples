from manim import *
import random

class SimpleRandomisation(MovingCameraScene):
    def construct(self):
        def make_group_box(label_text, x_shift, color):
            label = Text(label_text, color=color).to_edge(UP).shift(RIGHT * x_shift)
            slots = VGroup()
            for i in range(N):
                row, col = divmod(i, cols)
                circle = Circle(radius=radius, color=WHITE).set_fill(GREY, opacity=0.2)
                circle.move_to([x_shift + col * 0.8 - 2, 2 - row * 0.8, 0])
                slots.add(circle)
            box = SurroundingRectangle(slots, buff=0.5)
            return label, slots, box

        N = 10
        cols = 5
        radius = 0.3

        # Treatment and Control Groups (First Box)
        treat_label, treat_slots, treat_box = make_group_box("Treatment", -3.5, RED)
        ctrl_label, ctrl_slots, ctrl_box = make_group_box("Control", 3.5, BLUE)

        group1 = VGroup(treat_label, ctrl_label, treat_slots, ctrl_slots, treat_box, ctrl_box)
        sample_text1 = Text(f"Sample size: {N}", font_size=30).next_to(group1, DOWN)
        self.add(group1, sample_text1)

        # Participants
        balls = VGroup()
        for i in range(N):
            ball = Circle(radius=radius,color=WHITE).set_fill(GREY).move_to([i * 0.6 - (N * 0.6) / 2, -3.5, 0])
            balls.add(ball)
        self.add(balls)

        # Randomisation
        treat_i = ctrl_i = 0
        for i in range(N):
            choice = random.choice(["treatment", "control"])
            ball = balls[i]
            if choice == "treatment":
                target = treat_slots[treat_i]
                color = RED
                treat_i += 1
            else:
                target = ctrl_slots[ctrl_i]
                color = BLUE
                ctrl_i += 1
            self.play(ball.animate.set_fill(color).move_to(target.get_center()), run_time=0.4)
            self.play(target.animate.set_fill(color, opacity=1), run_time=0.3)

        self.wait(0.5)

        # Camera pans out and moves to new box with n = 20
        group2_origin = DOWN * 15
        new_N = 20
        new_cols = 5
        new_radius = 0.3

        def make_secondary_box(label_text, x_shift, color):
            label = Text(label_text, color=color).move_to(group2_origin + UP * 2.2 + RIGHT * x_shift)
            slots = VGroup()
            for i in range(new_N):
                row, col = divmod(i, new_cols)
                circle = Circle(radius=new_radius, color=WHITE).set_fill(GREY, opacity=0.2)
                circle.move_to(group2_origin + [x_shift + col * 0.8 - 2, 1 - row * 0.8, 0])
                slots.add(circle)
            box = SurroundingRectangle(slots, buff=0.5)
            return label, slots, box

        new_treat_label, new_treat_slots, new_treat_box = make_secondary_box("Treatment", -3.5, RED)
        new_ctrl_label, new_ctrl_slots, new_ctrl_box = make_secondary_box("Control", 3.5, BLUE)
        group2 = VGroup(new_treat_label, new_ctrl_label, new_treat_slots, new_ctrl_slots, new_treat_box, new_ctrl_box)
        sample_text2 = Text(f"Sample size: {new_N}", font_size=30).next_to(group2, DOWN)

        # Camera zoom and pan
        self.add(group2, sample_text2)
        self.play(self.camera.frame.animate.move_to(group2_origin).scale(1.5), run_time=2)
       

        # Animate randomisation again
        balls2 = VGroup()
        for i in range(new_N):
            ball = Circle(radius=new_radius,color=WHITE).set_fill(GREY).move_to(group2_origin + [i * 0.6 - (new_N * 0.6) / 2, -3.5, 0])
            balls2.add(ball)
        self.add(balls2)

        treat_i = ctrl_i = 0
        for i in range(new_N):
            choice = random.choice(["treatment", "control"])
            ball = balls2[i]
            if choice == "treatment":
                target = new_treat_slots[treat_i]
                color = RED
                treat_i += 1
            else:
                target = new_ctrl_slots[ctrl_i]
                color = BLUE
                ctrl_i += 1
            self.play(ball.animate.set_fill(color).move_to(target.get_center()), run_time=0.4)
            self.play(target.animate.set_fill(color, opacity=1), run_time=0.3)

        self.wait()