import pandas as pd
import streamlit as st


@st.cache()
def read_ady_data():
    df = pd.read_excel("ady_tranzit_2017-2022_9_ay.xlsx")
    df['Ay_sirasi'] = df['Tarix Hierarchy - Ay'].replace({"Yanvar": 1, 'Fevral': 2, "Mart": 3,
                                                          "Aprel": 4, "May": 5, "İyun": 6,
                                                          "İyul": 7, "Avqust": 8, "Sentyabr": 9,
                                                          "Oktyabr": 10, "Noyabr": 11, "Dekabr": 12})
    df['Ceki_min_ton'] = df['Həcm'] / 1000
    df = df[[
        'Tarix Hierarchy - İl', 'Yük qrupu (ADY)',
        'Göndərən (az)', 'Alan (az)', 'Koridor tranzit',
        'Ay_sirasi', 'Ceki_min_ton'
    ]]
    return df


def final_table(selected_country):
    df = read_ady_data()
    max_year = df['Tarix Hierarchy - İl'].max()
    before_max_year = max_year-1
    max_year_asterisk = f'{max_year}*'
    before_max_year_asterisk = f'{before_max_year}*'
    max_month = df[df['Tarix Hierarchy - İl'] == max_year]['Ay_sirasi'].max()

    pivot = pd.pivot_table(
        df[
            ((df['Göndərən (az)'] == selected_country) |
             (df['Alan (az)'] == selected_country))
            ],
        index='Koridor tranzit',
        columns='Tarix Hierarchy - İl',
        values='Ceki_min_ton',
        aggfunc='sum'
    )

    pivot_monthly = pd.pivot_table(
        df[
            ((df['Göndərən (az)'] == selected_country) |
             (df['Alan (az)'] == selected_country)) &
            (df['Ay_sirasi'] <= max_month)
            ],
        index='Koridor tranzit',
        columns='Tarix Hierarchy - İl',
        values='Ceki_min_ton',
        aggfunc='sum'
    )
    pivot = pivot.rename({max_year: max_year_asterisk}, axis=1)
    pivot_monthly.columns = [f'{i}*' for i in pivot_monthly.columns]
    final_pivot = pd.concat([pivot, pivot_monthly[before_max_year_asterisk]], axis=1)
    final_pivot = final_pivot[[*final_pivot.columns[:-2], final_pivot.columns[-1], final_pivot.columns[-2]]]

    final_pivot = final_pivot.sort_values(max_year_asterisk, ascending=False)
    final_pivot.loc['Cəmi:'] = final_pivot.sum(axis=0)

    final_pivot['Artım'] = (final_pivot[max_year_asterisk]/final_pivot[before_max_year_asterisk]-1)*100
    final_pivot['Artım'] = final_pivot['Artım'].apply(lambda x: f'{round(x, 0)}%')
    final_pivot = final_pivot.fillna(0)
    final_pivot['Artım'] = final_pivot['Artım'].replace('nan%', "-")

# # mehsul olkeden full years
    mehsul_pivot_olkeden = pd.pivot_table(
        df[df['Göndərən (az)'] == selected_country],
        index='Yük qrupu (ADY)',
        columns='Tarix Hierarchy - İl',
        values='Ceki_min_ton',
        aggfunc='sum'
    ).iloc[:, -2:]
# # mehsul olkeden monthly
    mehsul_pivot_olkeden_monthly = pd.pivot_table(
        df[
            (df['Göndərən (az)'] == selected_country) &
            (df['Ay_sirasi'] <= max_month)
            ],
        index='Yük qrupu (ADY)',
        columns='Tarix Hierarchy - İl',
        values='Ceki_min_ton',
        aggfunc='sum'
    ).iloc[:, -2:]
#
#     # mehsul olkeden artimla
#
    mehsul_pivot_olkeden = mehsul_pivot_olkeden.rename({max_year: max_year_asterisk}, axis=1)
    mehsul_pivot_olkeden_monthly.columns = [f'{i}*' for i in mehsul_pivot_olkeden_monthly.columns]
    mehsul_olkeden_final = pd.concat([mehsul_pivot_olkeden, mehsul_pivot_olkeden_monthly[before_max_year_asterisk]],
                                     axis=1)
    mehsul_olkeden_final = mehsul_olkeden_final[[*mehsul_olkeden_final.columns[:-2],
                                                 mehsul_olkeden_final.columns[-1],
                                                 mehsul_olkeden_final.columns[-2]]]

    mehsul_olkeden_final = mehsul_olkeden_final.sort_values(max_year_asterisk, ascending=False)
    mehsul_olkeden_final.loc['Cəmi:'] = mehsul_olkeden_final.sum(axis=0)
    mehsul_olkeden_final['Artım'] = (mehsul_olkeden_final[max_year_asterisk]/mehsul_olkeden_final
                                            [before_max_year_asterisk]-1)*100
    mehsul_olkeden_final['Artım'] = mehsul_olkeden_final['Artım'].apply(lambda x: f'{round(x, 0)}%')
    mehsul_olkeden_final = mehsul_olkeden_final.fillna(0)
    mehsul_olkeden_final['Artım'] = mehsul_olkeden_final['Artım'].replace('nan%', "-")

    # # mehsul olkeden full years
    mehsul_pivot_olkeye = pd.pivot_table(
        df[df['Alan (az)'] == selected_country],
        index='Yük qrupu (ADY)',
        columns='Tarix Hierarchy - İl',
        values='Ceki_min_ton',
        aggfunc='sum'
    ).iloc[:, -2:]
    # # mehsul olkeden monthly
    mehsul_pivot_olkeye_monthly = pd.pivot_table(
        df[
            (df['Alan (az)'] == selected_country) &
            (df['Ay_sirasi'] <= max_month)
            ],
        index='Yük qrupu (ADY)',
        columns='Tarix Hierarchy - İl',
        values='Ceki_min_ton',
        aggfunc='sum'
    ).iloc[:, -2:]
    #
    #     # mehsul olkeden artimla
    #
    mehsul_pivot_olkeye = mehsul_pivot_olkeye.rename({max_year: max_year_asterisk}, axis=1)
    mehsul_pivot_olkeye_monthly.columns = [f'{i}*' for i in mehsul_pivot_olkeye_monthly.columns]
    mehsul_olkeye_final = pd.concat([mehsul_pivot_olkeye, mehsul_pivot_olkeye_monthly[before_max_year_asterisk]],
                                     axis=1)
    mehsul_olkeye_final = mehsul_olkeye_final[[*mehsul_olkeye_final.columns[:-2],
                                                 mehsul_olkeye_final.columns[-1],
                                                 mehsul_olkeye_final.columns[-2]]]

    mehsul_olkeye_final = mehsul_olkeye_final.sort_values(max_year_asterisk, ascending=False)
    mehsul_olkeye_final.loc['Cəmi:'] = mehsul_olkeye_final.sum(axis=0)
    mehsul_olkeye_final['Artım'] = (mehsul_olkeye_final[max_year_asterisk] / mehsul_olkeye_final
    [before_max_year_asterisk] - 1) * 100
    mehsul_olkeye_final['Artım'] = mehsul_olkeye_final['Artım'].apply(lambda x: f'{round(x, 0)}%')
    mehsul_olkeye_final = mehsul_olkeye_final.fillna(0)
    mehsul_olkeye_final['Artım'] = mehsul_olkeye_final['Artım'].replace('nan%', "-")

    ###############################################################################################
    # # mehsul olkeden full years
    mehsul_dovriyye = pd.pivot_table(
        df[(df['Alan (az)'] == selected_country) |
           (df['Göndərən (az)'] == selected_country)
        ],
        index='Yük qrupu (ADY)',
        columns='Tarix Hierarchy - İl',
        values='Ceki_min_ton',
        aggfunc='sum'
    ).iloc[:, -2:]

    mehsul_dovriyye_monthly = pd.pivot_table(
        df[
            ((df['Alan (az)'] == selected_country) |
            (df['Göndərən (az)'] == selected_country)) &
            (df['Ay_sirasi'] <= max_month)
            ],
        index='Yük qrupu (ADY)',
        columns='Tarix Hierarchy - İl',
        values='Ceki_min_ton',
        aggfunc='sum'
    ).iloc[:, -2:]
    #
    #     # mehsul olkeden artimla
    #
    mehsul_dovriyye = mehsul_dovriyye.rename({max_year: max_year_asterisk}, axis=1)
    mehsul_dovriyye_monthly.columns = [f'{i}*' for i in mehsul_dovriyye_monthly.columns]
    mehsul_dovriyye_final = pd.concat([mehsul_dovriyye, mehsul_dovriyye_monthly[before_max_year_asterisk]],
                                     axis=1)
    mehsul_dovriyye_final = mehsul_dovriyye_final[[*mehsul_dovriyye_final.columns[:-2],
                                                 mehsul_dovriyye_final.columns[-1],
                                                 mehsul_dovriyye_final.columns[-2]]]

    mehsul_dovriyye_final = mehsul_dovriyye_final.sort_values(max_year_asterisk, ascending=False)
    mehsul_dovriyye_final.loc['Cəmi:'] = mehsul_dovriyye_final.sum(axis=0)
    mehsul_dovriyye_final['Artım'] = (mehsul_dovriyye_final[max_year_asterisk] / mehsul_dovriyye_final
    [before_max_year_asterisk] - 1) * 100
    mehsul_dovriyye_final['Artım'] = mehsul_dovriyye_final['Artım'].apply(lambda x: f'{round(x, 0)}%')
    mehsul_dovriyye_final = mehsul_dovriyye_final.fillna(0)
    mehsul_dovriyye_final['Artım'] = mehsul_dovriyye_final['Artım'].replace('nan%', "-")

    return final_pivot, max_month, mehsul_olkeden_final, mehsul_olkeye_final, mehsul_dovriyye_final


@st.cache()
def return_list_of_countries():
    return sorted(['Rusiya Federasiyası', 'Gürcüstan', 'Gürcüstan (tranzit)', 'Özbəkistan',
            'Türkmənistan', 'Türkiyə', "İran", "Qırğızıstan", "Çin"])

