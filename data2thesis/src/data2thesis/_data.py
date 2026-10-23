"""Core dataset loading utilities and metadata for the data2thesis package.

Provides direct access to the Graduate Wellbeing Study datasets used in
'FROM DATA TO THESIS: Using Python for Non-Technical'.
"""

from __future__ import annotations

import importlib.resources
from pathlib import Path
from typing import Any, Dict, List, Optional
import pandas as pd

DATASET_NAMES = [
    "students",
    "questionnaire",
    "semesters",
    "supervisors",
    "open_responses",
    "open_responses_coded",
    "counselling_visits",
    "toothgrowth",
    "faithful",
    "sleep",
    "trees",
    "ucbadmissions",
    "usarrests",
    "sleepstudy",
    "chickweight",
    "credit_data",
    "titanic",
    "penguins",
    "concrete",
    "quakes",
]

EXAMPLE_FILES = [
    "students.csv",
    "questionnaire.csv",
    "semesters.csv",
    "supervisors.csv",
    "open_responses.csv",
    "open_responses_coded.csv",
    "counselling_visits.csv",
    "toothgrowth.csv",
    "faithful.csv",
    "sleep.csv",
    "trees.csv",
    "ucbadmissions.csv",
    "usarrests.csv",
    "sleepstudy.csv",
    "chickweight.csv",
    "credit_data.csv",
    "titanic.csv",
    "penguins.csv",
    "concrete.csv",
    "quakes.csv",
    "wellbeing_raw.xlsx",
    "wellbeing.sav",
]

_DATA_CACHE: Dict[str, pd.DataFrame] = {}


def get_data_dir() -> Path:
    """Return the absolute Path to the packaged datasets directory."""
    local_dir = Path(__file__).resolve().parent / "datasets"
    if local_dir.is_dir():
        return local_dir
    ref = importlib.resources.files("data2thesis") / "datasets"
    return Path(str(ref))


def example_file(name: Optional[str] = None) -> Path | List[str]:
    """Get the file path to a raw example dataset, or list available example files.

    Used especially in chapters on importing and cleaning raw data (e.g. Excel
    and SPSS files).

    Parameters
    ----------
    name : str, optional
        Name of the file (e.g. 'wellbeing_raw.xlsx', 'wellbeing.sav', 'students.csv').
        If None, returns a list of all available example file names.

    Returns
    -------
    Path or list of str
        The Path to the example file if name is provided, or list of file names if None.

    Raises
    ------
    FileNotFoundError
        If the specified file is not found in the example datasets.

    Examples
    --------
    >>> import data2thesis as dt
    >>> dt.example_file()
    ['counselling_visits.csv', ...]
    >>> path = dt.example_file('wellbeing_raw.xlsx')
    >>> import pandas as pd
    >>> df = pd.read_excel(path)
    """
    data_dir = get_data_dir()
    if name is None:
        files = [p.name for p in data_dir.iterdir() if p.is_file() and not p.name.startswith(".")]
        return sorted(files)

    target = data_dir / name
    if not target.exists():
        available = [p.name for p in data_dir.iterdir() if p.is_file() and not p.name.startswith(".")]
        raise FileNotFoundError(
            f"'{name}' is not one of the example files in data2thesis. "
            f"Available files: {sorted(available)}"
        )
    return target


# Alias matching R package function name for ease of transition
data2thesis_example = example_file


def list_example_files() -> List[str]:
    """Return a list of all available example files in the package."""
    result = example_file(None)
    assert isinstance(result, list)
    return result


def _load_csv(filename: str, parse_dates: Optional[List[str]] = None) -> pd.DataFrame:
    filepath = get_data_dir() / filename
    if not filepath.exists():
        raise FileNotFoundError(f"Dataset file '{filename}' not found in package data.")
    return pd.read_csv(filepath, parse_dates=parse_dates, keep_default_na=True)


def load_students(copy: bool = True) -> pd.DataFrame:
    """Load the students dataset (Graduate Wellbeing Study baseline).

    Contains baseline demographics, academic programme, randomly assigned
    workshop group, and year-1 dropout consideration for 600 graduate students.

    Parameters
    ----------
    copy : bool, default True
        If True, returns a fresh copy of the DataFrame so modifications
        do not affect cached data.

    Returns
    -------
    pd.DataFrame
        600 rows, 14 columns:
        - student_id: Identifier (S0001 to S0600)
        - supervisor_id: Supervisor identifier (SUP001 to SUP120)
        - age: Age in years at start of study
        - gender: 'Female' or 'Male'
        - faculty: Student's faculty
        - programme: 'Master\\'s' or 'PhD'
        - study_mode: 'Full-time' or 'Part-time'
        - employment: 'None', 'Part-time job', or 'Full-time job'
        - has_children: 'Yes' or 'No'
        - lives_away: 'Yes' or 'No' (moved away from family)
        - financial_worry: Likert rating 1 (not at all) to 5 (extremely)
        - workshop: 'Invited' or 'Not invited'
        - workshop_sessions: Number of 6 sessions attended (0 if not invited)
        - considering_dropout: 'Yes' or 'No' at end of year 1
    """
    if "students" not in _DATA_CACHE:
        df = _load_csv("students.csv")
        # In students.csv, 'None' represents the employment category (no job).
        # Pandas read_csv parses 'None' as NaN by default, so restore 'None'.
        df["employment"] = df["employment"].fillna("None")
        _DATA_CACHE["students"] = df
    return _DATA_CACHE["students"].copy() if copy else _DATA_CACHE["students"]


def load_questionnaire(copy: bool = True) -> pd.DataFrame:
    """Load the 22-item baseline questionnaire dataset.

    Answers to the 22-item wellbeing survey given at the start of the study,
    measuring Stress (items 1-6), Burnout (items 1-6), Supervisor Support
    (items 1-6), and Academic Satisfaction (items 1-4).

    Parameters
    ----------
    copy : bool, default True
        If True, returns a fresh copy of the DataFrame.

    Returns
    -------
    pd.DataFrame
        600 rows, 23 columns:
        - student_id: Links to students
        - stress_1 to stress_6: Stress items (stress_4 is reverse-worded)
        - burnout_1 to burnout_6: Burnout items
        - support_1 to support_6: Supervisor support items
        - satisfaction_1 to satisfaction_4: Satisfaction items
    """
    if "questionnaire" not in _DATA_CACHE:
        _DATA_CACHE["questionnaire"] = _load_csv("questionnaire.csv")
    return _DATA_CACHE["questionnaire"].copy() if copy else _DATA_CACHE["questionnaire"]


def load_semesters(copy: bool = True) -> pd.DataFrame:
    """Load longitudinal semester records (long format over 4 semesters).

    One row per student per semester, tracking GPA, sleep, study habits,
    caffeine intake, supervisor meetings, and overall wellbeing index.

    Parameters
    ----------
    copy : bool, default True
        If True, returns a fresh copy of the DataFrame.

    Returns
    -------
    pd.DataFrame
        2,326 rows, 9 columns:
        - student_id: Links to students
        - semester: Semester number (1 to 4)
        - gpa: Semester GPA (0.0 to 4.0 scale)
        - sleep_hours: Average hours of sleep per night
        - study_hours: Hours of study per week
        - exercise_days: Days per week with at least 30 min exercise
        - caffeine_mg: Daily caffeine intake in milligrams
        - supervisor_meetings: Number of meetings during semester
        - wellbeing: Wellbeing index from 0 to 100 (higher is better)
    """
    if "semesters" not in _DATA_CACHE:
        _DATA_CACHE["semesters"] = _load_csv("semesters.csv")
    return _DATA_CACHE["semesters"].copy() if copy else _DATA_CACHE["semesters"]


def load_supervisors(copy: bool = True) -> pd.DataFrame:
    """Load the supervisors dataset.

    Information on the 120 academic supervisors, used to demonstrate
    multilevel / mixed-effects modeling.

    Parameters
    ----------
    copy : bool, default True
        If True, returns a fresh copy of the DataFrame.

    Returns
    -------
    pd.DataFrame
        120 rows, 4 columns:
        - supervisor_id: Supervisor identifier (SUP001 to SUP120)
        - faculty: Supervisor's academic faculty
        - rank: 'Lecturer', 'Assistant Professor', or 'Professor'
        - n_students: Number of students supervised in the study
    """
    if "supervisors" not in _DATA_CACHE:
        _DATA_CACHE["supervisors"] = _load_csv("supervisors.csv")
    return _DATA_CACHE["supervisors"].copy() if copy else _DATA_CACHE["supervisors"]


def load_open_responses(copy: bool = True) -> pd.DataFrame:
    """Load open-ended qualitative survey answers.

    Answers to the final survey question:
    "What has been your biggest challenge during your studies?"

    Parameters
    ----------
    copy : bool, default True
        If True, returns a fresh copy of the DataFrame.

    Returns
    -------
    pd.DataFrame
        535 rows, 2 columns:
        - student_id: Links to students
        - biggest_challenge: The student's free-text response
    """
    if "open_responses" not in _DATA_CACHE:
        _DATA_CACHE["open_responses"] = _load_csv("open_responses.csv")
    return _DATA_CACHE["open_responses"].copy() if copy else _DATA_CACHE["open_responses"]


def load_open_responses_coded(copy: bool = True) -> pd.DataFrame:
    """Load manually coded open-ended responses subset (200 responses).

    Used for validating text classification and LLM coding benchmarks.

    Parameters
    ----------
    copy : bool, default True
        If True, returns a fresh copy of the DataFrame.

    Returns
    -------
    pd.DataFrame
        200 rows, 3 columns:
        - student_id: Links to students
        - biggest_challenge: Free-text response
        - theme: Assigned code ('Supervision', 'Workload', 'Finances',
                 'Family', 'Health', 'Isolation', or 'Other')
    """
    if "open_responses_coded" not in _DATA_CACHE:
        _DATA_CACHE["open_responses_coded"] = _load_csv("open_responses_coded.csv")
    return _DATA_CACHE["open_responses_coded"].copy() if copy else _DATA_CACHE["open_responses_coded"]


def load_counselling_visits(parse_dates: bool = True, copy: bool = True) -> pd.DataFrame:
    """Load weekly counselling service visit records.

    Weekly student visits to the university counselling service over five
    academic years (260 weeks), used for time series analysis and forecasting.

    Parameters
    ----------
    parse_dates : bool, default True
        If True, converts 'week_start' column to datetime64[ns].
    copy : bool, default True
        If True, returns a fresh copy of the DataFrame.

    Returns
    -------
    pd.DataFrame
        260 rows, 2 columns:
        - week_start: Monday of each week (datetime or ISO string)
        - visits: Number of student visits that week
    """
    cache_key = "counselling_visits_parsed" if parse_dates else "counselling_visits_raw"
    if cache_key not in _DATA_CACHE:
        dates = ["week_start"] if parse_dates else None
        _DATA_CACHE[cache_key] = _load_csv("counselling_visits.csv", parse_dates=dates)
    return _DATA_CACHE[cache_key].copy() if copy else _DATA_CACHE[cache_key]


def load_toothgrowth(copy: bool = True) -> pd.DataFrame:
    """Load the classic ToothGrowth dataset (Crampton, 1947)."""
    if "toothgrowth" not in _DATA_CACHE:
        _DATA_CACHE["toothgrowth"] = _load_csv("toothgrowth.csv")
    return _DATA_CACHE["toothgrowth"].copy() if copy else _DATA_CACHE["toothgrowth"]


def load_faithful(copy: bool = True) -> pd.DataFrame:
    """Load the classic Old Faithful geyser eruption dataset."""
    if "faithful" not in _DATA_CACHE:
        _DATA_CACHE["faithful"] = _load_csv("faithful.csv")
    return _DATA_CACHE["faithful"].copy() if copy else _DATA_CACHE["faithful"]


def load_sleep(copy: bool = True) -> pd.DataFrame:
    """Load Student's 1908 classic sleep dataset (Cushman and Peebles, 1904)."""
    if "sleep" not in _DATA_CACHE:
        _DATA_CACHE["sleep"] = _load_csv("sleep.csv")
    return _DATA_CACHE["sleep"].copy() if copy else _DATA_CACHE["sleep"]


def load_trees(copy: bool = True) -> pd.DataFrame:
    """Load the black cherry trees timber volume dataset."""
    if "trees" not in _DATA_CACHE:
        _DATA_CACHE["trees"] = _load_csv("trees.csv")
    return _DATA_CACHE["trees"].copy() if copy else _DATA_CACHE["trees"]


def load_ucbadmissions(copy: bool = True) -> pd.DataFrame:
    """Load the 1973 UC Berkeley graduate admissions aggregate dataset."""
    if "ucbadmissions" not in _DATA_CACHE:
        _DATA_CACHE["ucbadmissions"] = _load_csv("ucbadmissions.csv")
    return _DATA_CACHE["ucbadmissions"].copy() if copy else _DATA_CACHE["ucbadmissions"]


def load_usarrests(copy: bool = True) -> pd.DataFrame:
    """Load the 1973 US violent crime arrests per 100,000 residents dataset."""
    if "usarrests" not in _DATA_CACHE:
        _DATA_CACHE["usarrests"] = _load_csv("usarrests.csv")
    return _DATA_CACHE["usarrests"].copy() if copy else _DATA_CACHE["usarrests"]


def load_sleepstudy(copy: bool = True) -> pd.DataFrame:
    """Load the Belenky et al. (2003) sleep deprivation reaction times dataset."""
    if "sleepstudy" not in _DATA_CACHE:
        _DATA_CACHE["sleepstudy"] = _load_csv("sleepstudy.csv")
    return _DATA_CACHE["sleepstudy"].copy() if copy else _DATA_CACHE["sleepstudy"]


def load_chickweight(copy: bool = True) -> pd.DataFrame:
    """Load the Crowder (1978) / Hand and Crowder (1996) chick growth trajectories dataset."""
    if "chickweight" not in _DATA_CACHE:
        _DATA_CACHE["chickweight"] = _load_csv("chickweight.csv")
    return _DATA_CACHE["chickweight"].copy() if copy else _DATA_CACHE["chickweight"]


def load_credit_data(copy: bool = True) -> pd.DataFrame:
    """Load the loan application credit risk dataset from modeldata."""
    if "credit_data" not in _DATA_CACHE:
        _DATA_CACHE["credit_data"] = _load_csv("credit_data.csv")
    return _DATA_CACHE["credit_data"].copy() if copy else _DATA_CACHE["credit_data"]


def load_titanic(copy: bool = True) -> pd.DataFrame:
    """Load the Titanic passenger survival dataset."""
    if "titanic" not in _DATA_CACHE:
        _DATA_CACHE["titanic"] = _load_csv("titanic.csv")
    return _DATA_CACHE["titanic"].copy() if copy else _DATA_CACHE["titanic"]


def load_penguins(copy: bool = True) -> pd.DataFrame:
    """Load the Palmer Penguins dataset (Gorman, Williams & Fraser, 2014)."""
    if "penguins" not in _DATA_CACHE:
        _DATA_CACHE["penguins"] = _load_csv("penguins.csv")
    return _DATA_CACHE["penguins"].copy() if copy else _DATA_CACHE["penguins"]


def load_concrete(copy: bool = True) -> pd.DataFrame:
    """Load the Yeh (1998) concrete compressive strength dataset."""
    if "concrete" not in _DATA_CACHE:
        _DATA_CACHE["concrete"] = _load_csv("concrete.csv")
    return _DATA_CACHE["concrete"].copy() if copy else _DATA_CACHE["concrete"]


def load_quakes(copy: bool = True) -> pd.DataFrame:
    """Load the locations of 1,000 earthquakes near Fiji since 1964."""
    if "quakes" not in _DATA_CACHE:
        _DATA_CACHE["quakes"] = _load_csv("quakes.csv")
    return _DATA_CACHE["quakes"].copy() if copy else _DATA_CACHE["quakes"]


def load(name: str, **kwargs: Any) -> pd.DataFrame:
    """Load a dataset by its string name.

    Parameters
    ----------
    name : str
        Name of dataset: 'students', 'questionnaire', 'semesters',
        'supervisors', 'open_responses', 'open_responses_coded',
        'counselling_visits', 'toothgrowth', 'faithful', 'sleep',
        'trees', 'ucbadmissions', 'usarrests', 'sleepstudy', 'chickweight',
        'credit_data', 'titanic', 'penguins', 'concrete', or 'quakes'.
    **kwargs : Any
        Passed to the underlying loader function.

    Returns
    -------
    pd.DataFrame
    """
    loaders = {
        "students": load_students,
        "questionnaire": load_questionnaire,
        "semesters": load_semesters,
        "supervisors": load_supervisors,
        "open_responses": load_open_responses,
        "open_responses_coded": load_open_responses_coded,
        "counselling_visits": load_counselling_visits,
        "toothgrowth": load_toothgrowth,
        "faithful": load_faithful,
        "sleep": load_sleep,
        "trees": load_trees,
        "ucbadmissions": load_ucbadmissions,
        "usarrests": load_usarrests,
        "sleepstudy": load_sleepstudy,
        "chickweight": load_chickweight,
        "credit_data": load_credit_data,
        "titanic": load_titanic,
        "penguins": load_penguins,
        "concrete": load_concrete,
        "quakes": load_quakes,
    }
    cleaned = name.strip().lower()
    if cleaned not in loaders:
        raise ValueError(
            f"Unknown dataset '{name}'. Available datasets: {list(loaders.keys())}"
        )
    return loaders[cleaned](**kwargs)


load_case_study = load


def load_all() -> Dict[str, pd.DataFrame]:
    """Load and return all 7 datasets in a dictionary."""
    return {name: load(name) for name in DATASET_NAMES}
