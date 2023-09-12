import pandas as pd
import io
from pandas.api.types import CategoricalDtype


def free_time_calc(csv_string):
    df = pd.read_csv(io.StringIO(csv_string))

    free_time_df = df[df["Text"].str.startswith("Free")].reset_index(drop=True)

    free_time_df["Start"] = pd.to_datetime(free_time_df["Start"], format="%H:%M")
    free_time_df["End"] = pd.to_datetime(free_time_df["End"], format="%H:%M")

    free_time_df["Duration"] = (free_time_df["End"] - free_time_df["Start"]).dt.total_seconds() / 60

    result_df = free_time_df.groupby(["Day", "Text"])["Duration"].sum().reset_index()
    result_df = result_df.pivot(index="Day", columns="Text", values="Duration").reset_index().fillna(0)

    ordered_days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    cat_type = CategoricalDtype(categories=ordered_days_of_week, ordered=True)
    result_df["Day"] = result_df["Day"].astype(cat_type)
    result_df = result_df.sort_values(by="Day")

    result_df["Total"] = result_df.iloc[:, 1:].sum(axis=1)

    return result_df
