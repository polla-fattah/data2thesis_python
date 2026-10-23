"""data2thesis: Companion datasets and tools for 'FROM DATA TO THESIS: Using Python for Non-Technical'.

By Dr. Polla Fattah.

Provides the Graduate Wellbeing Study case-study datasets used throughout
the book, plus example files for practising data import and cleaning.

Quickstart:
-----------
>>> import data2thesis as dt
>>> dt.students.head()
>>> dt.semesters.describe()

Explicit Loaders:
-----------------
>>> students = dt.load_students()
>>> questionnaire = dt.load_questionnaire()
>>> semesters = dt.load_semesters()
>>> supervisors = dt.load_supervisors()
>>> open_responses = dt.load_open_responses()
>>> open_responses_coded = dt.load_open_responses_coded()
>>> counselling_visits = dt.load_counselling_visits()

Raw Example Files (for Chapter 2 & 3 import/cleaning practice):
--------------------------------------------------------------
>>> dt.list_example_files()
>>> path = dt.example_file("wellbeing_raw.xlsx")
>>> import pandas as pd
>>> df = pd.read_excel(path)
"""

from __future__ import annotations

from typing import Any, List

from data2thesis._data import (
    DATASET_NAMES,
    EXAMPLE_FILES,
    data2thesis_example,
    example_file,
    get_data_dir,
    list_example_files,
    load,
    load_case_study,
    load_all,
    load_counselling_visits,
    load_open_responses,
    load_open_responses_coded,
    load_questionnaire,
    load_semesters,
    load_students,
    load_supervisors,
    load_toothgrowth,
    load_faithful,
    load_sleep,
    load_trees,
    load_ucbadmissions,
    load_usarrests,
    load_sleepstudy,
    load_chickweight,
    load_credit_data,
    load_titanic,
    load_penguins,
)

__version__ = "1.1.0"
__author__ = "Dr. Polla Fattah"

__all__ = [
    "__version__",
    "load_students",
    "load_questionnaire",
    "load_semesters",
    "load_supervisors",
    "load_open_responses",
    "load_open_responses_coded",
    "load_counselling_visits",
    "load_toothgrowth",
    "load_faithful",
    "load_sleep",
    "load_trees",
    "load_ucbadmissions",
    "load_usarrests",
    "load_sleepstudy",
    "load_chickweight",
    "load_credit_data",
    "load_titanic",
    "load_penguins",
    "load",
    "load_case_study",
    "load_all",
    "example_file",
    "list_example_files",
    "data2thesis_example",
    "get_data_dir",
    "DATASET_NAMES",
    "EXAMPLE_FILES",
    # Dynamic datasets available as attributes
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
]


def __getattr__(name: str) -> Any:
    """Dynamically load and return a dataset DataFrame when accessed as an attribute.

    Examples
    --------
    >>> import data2thesis as dt
    >>> dt.students.head()
    >>> from data2thesis import semesters
    >>> semesters.info()
    """
    if name in DATASET_NAMES:
        return load(name)
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


def __dir__() -> List[str]:
    """Include dynamic dataset names in autocomplete listings."""
    return sorted(list(globals().keys()) + DATASET_NAMES)
