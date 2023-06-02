import pandas as pd


def usa_covid_cases():
    """
    Get daily covid cases for covid beta section
    """
    output_df = pd.DataFrame()
    covid_df = pd.read_csv(r'https://covid.ourworldindata.org/data/owid-covid-data.csv')
    usa_df = covid_df[covid_df["iso_code"] == "USA"]
    output_df["Date"] = usa_df["date"]
    output_df["New Cases"] = usa_df["new_cases"]
    output_df["Fully Vaccinated / 100"] = usa_df["people_fully_vaccinated_per_hundred"]
    print(output_df)
    output_df.to_csv("database/usa_covid.csv", index=False)


if __name__ == '__main__':
    usa_covid_cases()
