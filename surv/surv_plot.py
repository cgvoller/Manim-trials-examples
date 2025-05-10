from manim import *
import pandas as pd

class SurvivalCurvePlot(Scene):
    def construct(self):
        # Load survival data
        df = pd.read_csv("survival_curve.csv")
        time_km = df["time"].values
        prob_km = df["survival_prob"].values

        # Create axes
        axes = Axes(
            x_range=[0, max(time_km) + 20, 50],
            y_range=[0, 1.1, 0.1],
            axis_config={"color": WHITE},
            x_axis_config={"numbers_to_include": [0, 100, 200, 300, 400]},
            y_axis_config={"numbers_to_include": [0, 0.5, 1.0]},
        ).add_coordinates()

        labels = axes.get_axis_labels(x_label="Time", y_label="Survival Probability")
        self.play(Create(axes), Write(labels), run_time=2)

        # Build step-wise lines
        curve_lines = VGroup()
        for i in range(len(time_km) - 1):
            # Horizontal segment
            x1, y1 = time_km[i], prob_km[i]
            x2 = time_km[i+1]
            p1 = axes.c2p(x1, y1)
            p2 = axes.c2p(x2, y1)
            horiz = Line(p1, p2, color=BLUE)
            curve_lines.add(horiz)

            # Vertical drop, unless last point
            y2 = prob_km[i+1]
            if y1 != y2:
                drop = Line(p2, axes.c2p(x2, y2), color=BLUE)
                curve_lines.add(drop)

        # Animate the curve
        self.play(LaggedStart(*[Create(seg) for seg in curve_lines], lag_ratio=0.1))
        self.wait()
