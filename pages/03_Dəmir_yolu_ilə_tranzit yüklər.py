from ADY_functions import *

return_list_of_countries = return_list_of_countries()

selected_country = st.sidebar.selectbox("Seçilmiş ölkə",
                                        options=return_list_of_countries)

dataframe, max_month, artimla1, artimla2, artimla3 = final_table(selected_country)

st.title(f'{selected_country}, *ilk {max_month} ay')
st.subheader('Yüklərin dəhlizlər üzrə bölgüsü, ümumi dövryyə, min ton')
st.dataframe(dataframe, use_container_width=True)

st.subheader("Seçilmiş ÖLKƏDƏN daşınan məhsullar, min ton")
st.dataframe(artimla1, use_container_width=True)

st.subheader("Seçilmiş ÖLKƏYƏ daşınan məhsullar, min ton")
st.dataframe(artimla2, use_container_width=True)

st.subheader("Daşınan məhsulların dövriyyəsi, min ton")
st.dataframe(artimla3, use_container_width=True)
