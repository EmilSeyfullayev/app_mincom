import pandas as pd
import numpy as np
import streamlit as st


@st.cache()
def read_ceki_data():
    df = pd.read_excel('TİR-lar.xlsx')
    df.drop('Unnamed: 0', axis=1, inplace=True)
    df['len'] = df['FromTo'].apply(lambda x: len(x.split('-')))
    df['From'] = df['FromTo'].apply(lambda x: x.split('-')[0])
    df['To'] = df['FromTo'].apply(lambda x: x.split('-')[1])
    df['To'] = df['To'].replace("Lanka", "Şri-Lanka")
    df['Ay_sirasi'] = df['Month'].replace({"Yanvar": 1, 'Fevral': 2, "Mart": 3,
                                           "Aprel": 4, "May": 5, "İyun": 6,
                                           "İyul": 7, "Avqust": 8, "Sentyabr": 9,
                                           "Oktyabr": 10, "Noyabr": 11, "Dekabr": 12})
    df['Sum'] = df[['Mazımçay', 'Qırmızı körpü',
                    'Samur', 'Biləsuvar', 'Eyvazlı', 'Astara', 'Culfa', 'Sədərək',
                    'Şahtaxtı', 'Şirvanlı', 'Xanoba']].sum(axis=1) / 1000
    return df


@st.cache()
def read_say_data():
    df = pd.read_excel('TİR-lar.xlsx', sheet_name='Say')
    df.drop('Unnamed: 0', axis=1, inplace=True)
    df['len'] = df['FromTo'].apply(lambda x: len(x.split('-')))
    df['From'] = df['FromTo'].apply(lambda x: x.split('-')[0])
    df['To'] = df['FromTo'].apply(lambda x: x.split('-')[1])
    df['To'] = df['To'].replace("Lanka", "Şri-Lanka")
    df['Ay_sirasi'] = df['Month'].replace({"Yanvar": 1, 'Fevral': 2, "Mart": 3,
                                           "Aprel": 4, "May": 5, "İyun": 6,
                                           "İyul": 7, "Avqust": 8, "Sentyabr": 9,
                                           "Oktyabr": 10, "Noyabr": 11, "Dekabr": 12})
    df['Sum'] = df[['Mazımçay', 'Qırmızı körpü',
                    'Samur', 'Biləsuvar', 'Eyvazlı', 'Astara', 'Culfa', 'Sədərək',
                    'Şahtaxtı', 'Şirvanlı', 'Xanoba']].sum(axis=1)
    return df


@st.cache()
def unique_countries_list():
    # df = read_ceki_data()
    # unique_countries = sorted(list(set(np.append(df['From'].unique(), df['To'].unique()))))
    # unique_countries = np.delete(unique_countries, np.where(unique_countries == "Azərbaycan"), axis=0)
    return ['Türkiyə', "Gürcüstan", "İran", "Rusiya",
            "Qazaxıstan", "Türkmənistan", "Qırğızıstan", "Çin", ]


# @st.cache()
# class Tables:
#     def __init__(self, selected_country):
#         self.df = read_ceki_data()
#         self.selected_country = selected_country
#
#     def return_final_table(self):
#         df = self.df
#         max_month = df[df['Year'] == max(df['Year'].unique())]['Ay_sirasi'].max()
#         max_year = df['Year'].max()
#         before_max_year = max_year - 1
#         max_year_with_asterix = "2022*"
#         before_max_year_with_asterix = "2021*"
#         countries_list = unique_countries_list()
#
#         from_ = pd.pivot_table(
#             df[df['From'] == self.selected_country],
#             columns='Year',
#             values='Sum',
#             aggfunc='sum'
#         ).rename(index={'Sum': 'Seçilmiş ölkədən'})
#
#         to_ = pd.pivot_table(
#             df[df['To'] == self.selected_country],
#             columns='Year',
#             values='Sum',
#             aggfunc='sum'
#         ).rename(index={'Sum': 'Seçilmiş ölkəyə'})
#
#         fromto = pd.concat([from_, to_], axis=0).rename({max_year: max_year_with_asterix},
#                                                         axis=1)
#
#         from_monthly = pd.pivot_table(
#             df[
#                 (df['From'] == self.selected_country) &
#                 (df['Ay_sirasi'] <= max_month)
#                 ],
#             columns='Year',
#             values='Sum',
#             aggfunc='sum'
#         ).rename(index={'Sum': 'Seçilmiş ölkədən'})
#
#         to_monthly = pd.pivot_table(
#             df[
#                 (df['To'] == self.selected_country) &
#                 (df['Ay_sirasi'] <= max_month)
#                 ],
#             columns='Year',
#             values='Sum',
#             aggfunc='sum'
#         ).rename(index={'Sum': 'Seçilmiş ölkəyə'})
#
#         fromto_monthly = pd.concat([from_monthly, to_monthly], axis=0).rename(
#             {before_max_year: before_max_year_with_asterix},
#             axis=1)
#
#         fromto.insert(len(fromto.columns) - 1,
#                       before_max_year_with_asterix,
#                       fromto_monthly[before_max_year_with_asterix])
#
#         fromto.loc['Avtomobil yolu ilə NV-lərin cəmi sayı:'] = fromto.sum()
#         fromto['Artım'] = (fromto[max_year_with_asterix] / fromto[before_max_year_with_asterix] - 1) * 100
#         fromto[before_max_year] = fromto[before_max_year].apply(lambda x: round(x, 2))
#         fromto[before_max_year_with_asterix] = fromto[before_max_year_with_asterix].apply(lambda x: round(x, 2))
#         fromto[max_year_with_asterix] = fromto[max_year_with_asterix].apply(lambda x: round(x, 2))
#
#         fromto['Artım'] = fromto['Artım'].apply(lambda x: round(x, 0))
#         fromto['Artım'] = fromto['Artım'].apply(lambda x: f'{x}%')
#         fromto = fromto[fromto.columns[2:]]
#
#         return fromto

@st.cache()
def return_final_table(selected_country, df):
    max_month = 10 # df[df['Year'] == max(df['Year'].unique())]['Ay_sirasi'].max()
    max_year = 2022#df['Year'].max()
    before_max_year = max_year - 1
    max_year_with_asterix = "2022*"
    before_max_year_with_asterix = "2021*"

    from_ = pd.pivot_table(
        df[df['From'] == selected_country],
        columns='Year',
        values='Sum',
        aggfunc='sum'
    ).rename(index={'Sum': 'Seçilmiş ölkədən'})

    to_ = pd.pivot_table(
        df[df['To'] == selected_country],
        columns='Year',
        values='Sum',
        aggfunc='sum'
    ).rename(index={'Sum': 'Seçilmiş ölkəyə'})

    fromto = pd.concat([from_, to_], axis=0).rename({max_year: max_year_with_asterix},
                                                    axis=1)

    from_monthly = pd.pivot_table(
        df[
            (df['From'] == selected_country) &
            (df['Ay_sirasi'] <= max_month)
            ],
        columns='Year',
        values='Sum',
        aggfunc='sum'
    ).rename(index={'Sum': 'Seçilmiş ölkədən'})

    to_monthly = pd.pivot_table(
        df[
            (df['To'] == selected_country) &
            (df['Ay_sirasi'] <= max_month)
            ],
        columns='Year',
        values='Sum',
        aggfunc='sum'
    ).rename(index={'Sum': 'Seçilmiş ölkəyə'})

    fromto_monthly = pd.concat([from_monthly, to_monthly], axis=0).rename(
        {before_max_year: before_max_year_with_asterix},
        axis=1)

    fromto.insert(len(fromto.columns) - 1,
                  before_max_year_with_asterix,
                  fromto_monthly[before_max_year_with_asterix])

    fromto.loc['Cəmi:'] = fromto.sum()
    fromto = fromto.fillna(0)
    fromto['Artım'] = (fromto[max_year_with_asterix] / fromto[before_max_year_with_asterix] - 1) * 100
    fromto[before_max_year] = fromto[before_max_year].apply(lambda x: round(x, 2))
    fromto[before_max_year_with_asterix] = fromto[before_max_year_with_asterix].apply(lambda x: round(x, 2))
    fromto[max_year_with_asterix] = fromto[max_year_with_asterix].apply(lambda x: round(x, 2))

    fromto['Artım'] = fromto['Artım'].apply(lambda x: round(x, 0))
    fromto['Artım'] = fromto['Artım'].apply(lambda x: f'{x}%')
    fromto['Artım'] = fromto['Artım'].replace("inf%", "-")
    # fromto = fromto.replace(0, '-')
    fromto = fromto[fromto.columns[2:]]

    def return_max_month():
        return max_month

    return fromto, return_max_month()
