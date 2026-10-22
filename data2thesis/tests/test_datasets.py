"""Tests for the data2thesis Python package."""

from pathlib import Path
import pandas as pd
import pytest

import data2thesis as dt


def test_package_metadata():
    assert dt.__version__ == "1.1.0"
    assert "Dr. Polla Fattah" in dt.__author__


def test_load_students():
    df = dt.load_students()
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (600, 14)
    expected_cols = [
        "student_id",
        "supervisor_id",
        "age",
        "gender",
        "faculty",
        "programme",
        "study_mode",
        "employment",
        "has_children",
        "lives_away",
        "financial_worry",
        "workshop",
        "workshop_sessions",
        "considering_dropout",
    ]
    assert list(df.columns) == expected_cols
    assert df["student_id"].nunique() == 600
    assert df["student_id"].iloc[0] == "S0001"
    assert set(df["gender"].dropna().unique()) == {"Female", "Male"}
    assert set(df["workshop"].dropna().unique()) == {"Invited", "Not invited"}


def test_load_questionnaire():
    df = dt.load_questionnaire()
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (600, 23)
    assert df["student_id"].iloc[0] == "S0001"
    assert "stress_1" in df.columns
    assert "burnout_1" in df.columns
    assert "support_1" in df.columns
    assert "satisfaction_1" in df.columns


def test_load_semesters():
    df = dt.load_semesters()
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2326, 9)
    assert set(df["semester"].unique()) == {1, 2, 3, 4}
    assert "gpa" in df.columns
    assert "wellbeing" in df.columns


def test_load_supervisors():
    df = dt.load_supervisors()
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (120, 4)
    assert df["supervisor_id"].nunique() == 120
    assert set(df["rank"].unique()) == {"Lecturer", "Assistant Professor", "Professor"}


def test_load_open_responses():
    df = dt.load_open_responses()
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (535, 2)
    assert list(df.columns) == ["student_id", "biggest_challenge"]


def test_load_open_responses_coded():
    df = dt.load_open_responses_coded()
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (200, 3)
    assert list(df.columns) == ["student_id", "biggest_challenge", "theme"]
    assert "theme" in df.columns


def test_load_counselling_visits():
    df = dt.load_counselling_visits(parse_dates=True)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (260, 2)
    assert list(df.columns) == ["week_start", "visits"]
    assert pd.api.types.is_datetime64_any_dtype(df["week_start"])

    # Raw string version
    df_raw = dt.load_counselling_visits(parse_dates=False)
    assert pd.api.types.is_object_dtype(df_raw["week_start"]) or pd.api.types.is_string_dtype(df_raw["week_start"])


def test_dynamic_attributes():
    # Test module-level __getattr__
    assert isinstance(dt.students, pd.DataFrame)
    assert dt.students.shape == (600, 14)
    assert isinstance(dt.semesters, pd.DataFrame)
    assert dt.semesters.shape == (2326, 9)
    assert isinstance(dt.supervisors, pd.DataFrame)

    with pytest.raises(AttributeError):
        _ = dt.non_existent_dataset


def test_generic_load():
    df = dt.load("students")
    assert df.shape == (600, 14)

    with pytest.raises(ValueError):
        dt.load("invalid_name")


def test_load_all():
    all_data = dt.load_all()
    assert len(all_data) == 7
    assert set(all_data.keys()) == set(dt.DATASET_NAMES)


def test_example_files():
    files = dt.list_example_files()
    assert isinstance(files, list)
    assert "wellbeing_raw.xlsx" in files
    assert "wellbeing.sav" in files
    assert "students.csv" in files

    path_xlsx = dt.example_file("wellbeing_raw.xlsx")
    assert isinstance(path_xlsx, Path)
    assert path_xlsx.exists()
    assert path_xlsx.suffix == ".xlsx"

    path_sav = dt.example_file("wellbeing.sav")
    assert isinstance(path_sav, Path)
    assert path_sav.exists()

    with pytest.raises(FileNotFoundError):
        dt.example_file("does_not_exist.xyz")


def test_r_alias_function():
    files = dt.data2thesis_example()
    assert "students.csv" in files
    path = dt.data2thesis_example("students.csv")
    assert Path(path).exists()
