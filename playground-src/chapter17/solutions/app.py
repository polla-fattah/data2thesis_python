import os
from shiny import App, render, ui, reactive
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data_dir = ".." if os.path.exists("../students.csv") else "."
students = pd.read_csv(os.path.join(data_dir, "students.csv"))
semesters = pd.read_csv(os.path.join(data_dir, "semesters.csv"))

# Semester records with each student's faculty and study mode
wellbeing_data = semesters.merge(
    students[["student_id", "faculty", "study_mode"]], 
    on="student_id"
)

measures = {
    "wellbeing": "Wellbeing (0-100)",
    "sleep_hours": "Sleep (hours a night)",
    "study_hours": "Study (hours a week)"
}

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_select(
            "faculty", "Faculty", 
            choices=sorted(wellbeing_data["faculty"].unique().tolist())
        ),
        ui.input_radio_buttons(
            "measure", "Measure", 
            choices=measures
        ),
        ui.input_slider(
            "semesters", "Semesters", 
            min=1, max=4, value=(1, 4), step=1
        )
    ),
    ui.card(ui.output_plot("trend")),
    ui.card(ui.output_table("summary")),
    title="Graduate student wellbeing"
)

def server(input, output, session):
    @reactive.calc
    def selected():
        s_range = input.semesters()
        df = wellbeing_data[wellbeing_data["faculty"] == input.faculty()]
        return df[(df["semester"] >= s_range[0]) & (df["semester"] <= s_range[1])]

    @render.plot
    def trend():
        df = selected()
        meas = input.measure()
        summary = (
            df.groupby(["semester", "study_mode"])[meas]
            .mean()
            .reset_index()
        )
        fig, ax = plt.subplots(figsize=(6.5, 3.8))
        sns.lineplot(
            data=summary, x="semester", y=meas, hue="study_mode", 
            marker="o", linewidth=2.5, markersize=8, ax=ax
        )
        ax.set_xlabel("Semester")
        ax.set_ylabel(measures[meas])
        s_range = input.semesters()
        ax.set_xticks(list(range(s_range[0], s_range[1] + 1)))
        ax.grid(True, linestyle="--", alpha=0.5)
        plt.tight_layout()
        return fig

    @render.table
    def summary():
        df = selected()
        meas = input.measure()
        tbl = (
            df.groupby("semester")
            .agg(
                students=("student_id", "nunique"),
                mean=(meas, "mean")
            )
            .reset_index()
            .round(2)
        )
        tbl.columns = ["Semester", "Students", "Mean"]
        return tbl

app = App(app_ui, server)
