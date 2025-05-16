from manim import *

class MAMS(Scene):
    def construct(self):
    # Draw axes
        x_max = 10
        y_max = 10
        axes = Axes(
            x_range=[0, x_max, 1],
            y_range=[0, y_max, 1],
            axis_config={"color": WHITE},
            x_axis_config={"include_ticks": False},
            y_axis_config={"include_ticks": False},
            tips=False
        )
        label = Text("Begin Phase II", font_size=24)
        y_axis_end = axes.c2p(0, axes.y_range[1])
        label.next_to(y_axis_end, UP, buff=0.2)

        self.play(Create(axes), Write(label), run_time=1.5)
        self.wait(1)

        # Example vertical lines and labels for context (optional)
        for frac, text in [(1/3, "Interim analysis I"), (2/3, "Interim analysis II")]:
            v_line = DashedLine(
                start=axes.c2p(x_max*frac, 0),
                end=axes.c2p(x_max*frac, axes.y_range[1]),
                color=RED
            )
            v_label = Text(text, font_size=24)
            v_label.next_to(axes.c2p(x_max*frac, axes.y_range[1]), UP, buff=0.2)
            self.play(Create(v_line), Write(v_label))

        y_base = 0.5
        line_height = 1.5
        start_x = 0

        end_text = Text("End Phase II/\nBegin Phase III", font_size=20)
        end_text.move_to(axes.c2p(x_max,axes.y_range[1]))
        end_text.shift(UP * 0.5)  # small vertical buffer to place above the lines
        self.play(Write(end_text))

        lines_info = [
            ("Control", 1, 1),
            ("Novel Regimen 4", 2/3, 2),
            ("Novel Regimen 3", 1, 3),
            ("Novel Regimen 2", 1/3, 4),
            ("Novel Regimen 1", 1/3, 5),
        ]
        # Define 
        arrow_color = [GREEN, RED, YELLOW, ORANGE, PURPLE]
        self.add(axes)
         # Find the longest distance
        max_frac = max(frac for _, frac, _ in lines_info)
        longest_distance = x_max * max_frac
        constant_speed = 1  # units per second
        total_duration = longest_distance / constant_speed  # duration based on longest line
        dots = []
        anims = []
        durations = []
        trackers = []
        for label_text, frac, idx in lines_info:
            color = arrow_color[idx % len(arrow_color)]
            y = y_base + line_height * idx
            y_coord = axes.c2p(0, y)[1]  # fixed y-coord in scene space
            target_x = x_max * frac
            start = axes.c2p(start_x, y)
            end = axes.c2p(target_x, y)
            duration = target_x / constant_speed
            durations.append(duration)
            tracker = ValueTracker(start_x)
            trackers.append(tracker)
            # Use always_redraw to create an arrow that updates with the tracker
            arrow = always_redraw(
                lambda st=tracker, y=y,color=color,frac=frac: Arrow(
                    start=axes.c2p(start_x,y),
                    end=axes.c2p(st.get_value(), y),
                    buff=0,
                    stroke_width=4,
                    tip_shape=ArrowSquareTip,
                    tip_length=0.1, 
                    color=color
                )
            )
            
            label = Text(label_text, font_size=20)
            label.next_to(start, UP+RIGHT*2, buff=0.1)

            self.add(arrow, label)

        max_duration = max(durations)
        # Animate all trackers manually in parallel
        def make_updater(tracker, target, duration):
            def updater(mob, alpha):
                t = alpha * max_duration
                if t <= duration:
                    value = start_x + (target - start_x) * (t / duration)
                    tracker.set_value(value)
            return updater

        anims = [
            UpdateFromAlphaFunc(tracker, make_updater(tracker, x_max * frac, dur))
            for tracker, (label, frac, idx), dur in zip(trackers, lines_info, durations)
        ]

        self.play(*anims, run_time=max_duration, rate_func=linear)
        self.wait(2)
 
