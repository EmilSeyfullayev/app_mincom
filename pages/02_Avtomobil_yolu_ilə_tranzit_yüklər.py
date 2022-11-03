from TİR_functions import *

list_of_countries = unique_countries_list()
selected_country = st.sidebar.selectbox("Seçilmiş ölkə", list_of_countries,
                                        list_of_countries.index("Türkiyə"))

# tables = Tables(selected_country)
# dataframe = tables.return_final_table()
df_ceki = read_ceki_data()
df_say = read_say_data()
df_ceki_dataframe = return_final_table(selected_country, df_ceki)[0]
df_say_dataframe = return_final_table(selected_country, df_say)[0]
max_month = return_final_table(selected_country, df_ceki)[1]

st.title(f"{selected_country}, ilk {max_month} ay")
st.subheader("Yüklərin istiqamətlər üzrə həcmi, min ton")
st.dataframe(df_ceki_dataframe, use_container_width=True)

st.subheader("TIR-ların istiqamətlər üzrə sayı, ədəd")
st.dataframe(df_say_dataframe, use_container_width=True)
