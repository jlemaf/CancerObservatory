import streamlit as st
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import altair as alt
import pydeck as pdk

st.set_page_config(
    page_title="Observatorio del Cáncer",
    page_icon="🧊",
    
    layout="wide",
    initial_sidebar_state="expanded",
)

#---------------------------------------------------------------------------------------
####SESSION STATE VARIABLES#####

# Hide elements

#hide hamburger button
if 'hamburger' not in st.session_state:
    st.session_state['hamburger'] = """
<style>
.e1fb0mya1.css-fblp2m.ex0cdmw0
{
    visibility:hidden;
}
"""

#hide footer
if 'footer' not in st.session_state:
    st.session_state['footer'] = """
<style>
.css-164nlkn.egzxvld1
{
    visibility:hidden;
}
"""

#hide line
if 'line' not in st.session_state:
    st.session_state['line'] = """
<style>
.css-1dp5vir.e8zbici1
{
    visibility:hidden;
}
"""

st.markdown(st.session_state.hamburger, unsafe_allow_html=True)
st.markdown(st.session_state.footer, unsafe_allow_html=True)
st.markdown(st.session_state.line, unsafe_allow_html=True)

#-----------------------------------------------------------------------------------

st.title('Observatorio del Cáncer')

def_16_22 = pd.read_csv('./data/defunciones_cancer_DEIS_2016_2022.csv', 
                       index_col=[0])
def_21_22 = pd.read_csv('./data/defunciones_cancer_DEIS_2021_2022.csv',
                       index_col=[0])

#with st.expander('Data'):
#    st.dataframe(def_16_22)
    #st.dataframe(def_21_22)


regions = alt.topo_feature("https://raw.githubusercontent.com/ProxyRobin/topojson/blob/main/minnesota state map.json", 'MIN_adm1')

map = alt.Chart(regions).mark_geoshape(
    stroke='white',
    strokeWidth=2
).encode(
    color=alt.value('#eee'),
)
st.altair_chart(map)#, use_container_width=False)



df = gpd.read_file('./shape/Chile_Simp_Comunas_data_sex_5.shp')


fig, ax = plt.subplots(1, 1, figsize=(15, 15))
ax.spines[['right', 'top','left','bottom']].set_visible(False)
ax.tick_params(left = False, right = False , labelleft = False , 
                labelbottom = False, bottom = False) 
df.plot('n_casos',ax=ax)
#st.pyplot(fig=fig)



st.set_option('deprecation.showPyplotGlobalUse', False)

data = gpd.read_file('./shape/Chile_Simp_Comunas_data_sex_5.shp')

point = alt.selection_single(on='mouseover', fields=['Comuna'], bind='legend')

chart=alt.Chart(data, #width=500, height=500
               ).mark_geoshape(
    ).encode(x='Long:Q',
             y='Lat:Q',
             #color=alt.condition(point, 'n_casos:Q', alt.value('lightgrey')),
             #tooltip=['Comuna','n_casos','Long']
            ).project('mercator')


st.altair_chart(chart)

df = alt.InlineData(values = data.to_json(), format = alt.DataFormat(property='features', type='json'))
df2 =pd.DataFrame(data.drop(columns='geometry'))
df2.rename(columns={'Long':'lon','Lat':'lat'},inplace=True)
gdf = gpd.GeoDataFrame(df2, geometry=gpd.points_from_xy(df2.lon, df2.lat))
gdf['wkt'] = gdf.geometry.to_wkt()
#gdf.drop('geometry',axis=1,inplace=True)
#st.write(gdf.head())
ax = data.plot(color='white', edgecolor='black')
gdf.plot(ax=ax, figsize=(20,20))
st.pyplot()

#df2['Lat'].rename('lat',inplace=True)
#df3 = df2[['lon','lat']].to_json()
df3 = data.to_json()
#with st.expander('BLBB'):
#    st.dataframe(df2)

#st.json(df3)

st.map(df2)
#st.graphviz_chart(df2)
st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=-33.45,
        longitude=-70.67,
        zoom=12,
        pitch=100,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=df3,
            get_position='[Long, Lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=200,
        ),
    ],
))

