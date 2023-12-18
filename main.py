import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import pydeck as pdk
import seaborn as sns
import numpy as np

# reading the csv file
df = pd.read_csv('Cannabis_Registry.csv')
print(df)

st.set_page_config(page_title="Cannabis Registry", page_icon="🍃")

# Title for the Webpage
st.markdown("<h1 style='text-align: center;color: #3C873A; font-family: Georgia;'> The Cannabis Registry</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;color: #3C873A; font-family: Georgia;'> A One Stop-Shop for all your Cannabis Needs </h4>", unsafe_allow_html=True)

# Slider to check age of customer
age = st.slider("Select your age", 0, 100, 21)
if age < 21:
    st.error("Illegal to be here!")
else:
    st.success("Welcome!")

# Video
st.divider()
st.markdown("<h4 style='text-align: center;color: #3C873A; font-family: Georgia;'> Video on Safer Use of Cannabis </h4>", unsafe_allow_html=True)
video_file = open('cannabisvideo.mp4', 'rb')
video_bytes = video_file.read()

st.video(video_bytes)

# Map1
st.divider()
st.markdown("<h4 style='text-align: center;color: #3C873A; font-family: Georgia;'> Cannabis Dispensaries in Boston </h4>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center;color: #FFFFFF; font-family: Georgia;'> This is a Gridlayer map, which shows the dispensary's around Boston and its locations, with frequency of dispensaries in a similar location.</h6>", unsafe_allow_html=True)

df['COORDINATES'] = df[['longitude', 'latitude']].values.tolist()

layer = pdk.Layer(
    "GridLayer",
    df,
    pickable=True,
    extruded=True,
    cell_size=200,
    elevation_scale=4,
    get_position="COORDINATES",
)

view_state = pdk.ViewState(
    latitude=df['latitude'].mean(),
    longitude=df['longitude'].mean(),
    zoom=11,
    bearing=0,
    pitch=45
)

r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "{position}\nCount: {count}"},
)

st.pydeck_chart(r)

# Donut Chart
st.divider()
st.markdown("<h4 style='text-align: center;color: #3C873A; font-family: Georgia;'> Donut Chart for Equity Programs </h4>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center;color: #FFFFFF; font-family: Georgia;'> This is a Donut Chart which shows the percentage of Cannabis Dispensaries providing an Equity Program, an Equity Program is designed to support equal opportunity in the cannabis industry by making legal cannabis business ownership and employment opportunities more accessible to low-income individuals and communities most impacted by the criminalization of cannabis.</h6>", unsafe_allow_html=True)

equity_program_counts = df['equity_program_designation'].value_counts()
fige, ax = plt.subplots()

ax.pie(equity_program_counts, labels=['{:.1f}%'.format(p) for p in equity_program_counts / equity_program_counts.sum() * 100],
       startangle=90, wedgeprops=dict(width=0.3))

ax.legend(equity_program_counts.index, title="Equity Program Designation", loc="center left", bbox_to_anchor=(1, 0.5))
ax.axis('equal')

st.pyplot(fige)

# Pi Chart
st.divider()
st.markdown("<h4 style='text-align: center;color: #3C873A; font-family: Georgia;'> Pi Chart for Count of App License Status </h4>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center;color: #FFFFFF; font-family: Georgia;'> This is a Pi Chart wchich shows the percentages of the of the App License Status, with a legend, whcih describes each color and its elements </h6>", unsafe_allow_html=True)

status_counts = df['app_license_status'].value_counts()
percentages = 100 * status_counts / status_counts.sum()
figr, ax = plt.subplots()

ax.pie(status_counts, startangle=90)
legend_labels = ['{0} - {1:.1f}%'.format(i, j) for i, j in zip(status_counts.index, percentages)]
ax.legend(legend_labels, title="App License Status", loc="center left", bbox_to_anchor=(1, 0.5))
ax.set_title("App License Status Distribution", pad=20)

st.pyplot(figr)

# Pivot Table
st.divider()
st.markdown("<h4 style='text-align: left;color: #3C873A; font-family: Georgia;'> Pivot table - License Category Vs License Status </h4>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center;color: #FFFFFF; font-family: Georgia;'> This is a Pivot table which shows us the comparision between the app license status and app license categories, with aggregates.</h6>", unsafe_allow_html=True)

pivot_table = df.pivot_table(index='app_license_category', columns='app_license_status',
                             aggfunc='size', fill_value=0)

# Add row totals
pivot_table['Total'] = pivot_table.sum(axis=1)

# Add column totals
pivot_table.loc['Total'] = pivot_table.sum()

# Display the pivot table with aggregates in Streamlit
st.dataframe(pivot_table)

#pivot_table = df.pivot_table(index='app_license_category', columns='app_license_status', aggfunc='size', fill_value=0)
#st.dataframe(pivot_table)

# Map 2 with Filter
st.divider()
st.markdown("<h4 style='text-align: center;color: #3C873A; font-family: Georgia;'> Select an App License Category </h4>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center;color: #FFFFFF; font-family: Georgia;'> This is a Scatter Plot Map which uses Pydeck to display the map, we have a filter which allows us to select a App License Category, and diplays the filtered results on the Map, we are able to hover over it to see the name of the store.</h6>", unsafe_allow_html=True)

selected_category = st.selectbox("", df['app_license_category'].unique())
def make_map(data, filter):
    data = data[data['app_license_category'] == filter]
    print(data)
    layer = pdk.Layer(
        "ScatterplotLayer",
        data,
        get_position=['longitude', 'latitude'],
        get_color=[255, 0, 0, 200],
        get_radius=100,
        tooltip={"text": "{app_business_name}"}
    )

    view_state = pdk.ViewState(latitude=data['latitude'].mean(), longitude=data['longitude'].mean(), zoom=10)

    st.pydeck_chart(
        pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=view_state,
            layers=[layer],
            tooltip={"text": "{app_business_name}"}
        )
    )


make_map(df, selected_category)

# Bar Graph 1
st.divider()
st.markdown("<h4 style='text-align: center;color: #3C873A; font-family: Georgia;'> Bar Chart for Count of App License Category </h4>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center;color: #FFFFFF; font-family: Georgia;'> This is a Bar Chart which shows the Distribution of the App License Category, it counts the frequency for each category. It uses the colors which are associated with Cannabis.</h6>", unsafe_allow_html=True)

sns.set_theme(style="white", context="talk")
category_counts = df['app_license_category'].value_counts()
green_palette = sns.light_palette("green", len(category_counts), reverse=True)

fig, ax = plt.subplots(figsize=(10, 8))
sns.barplot(x=category_counts.index, y=category_counts.values, palette=green_palette, ax=ax)

ax.set_xlabel('App License Categories')
ax.set_ylabel('Count')
ax.set_title('Count of App License Categories')
ax.set_xticklabels(category_counts.index, rotation=45, ha='right')
sns.despine()

st.pyplot(fig)

#Bar Graph 2
st.divider()
st.markdown("<h4 style='text-align: center;color: #3C873A; font-family: Georgia;'> Bar Chart for Count of App License Category with License Status </h4>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center;color: #FFFFFF; font-family: Georgia;'> This is a combination of a Bar Chart and the line graph. It is an addition of the graph above. It shows us a breakdown of each category with regards to it's license status.</h6>", unsafe_allow_html=True)

sns.set_theme(style="darkgrid")
long_form_df = df.groupby(['app_license_category', 'app_license_status']).size().reset_index(name='count')
sns.lineplot(x="app_license_category", y="count",
             hue="app_license_status", style="app_license_status",
             data=long_form_df, linewidth=2.5)

plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(plt.gcf())

# Datasheet
st.divider()
st.markdown("<h4 style='text-align: center;color: #3C873A; font-family: Georgia;'> Cannabis Registry Datasheet </h4>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center;color: #FFFFFF; font-family: Georgia;'> This is the complete cannabis registry datasheet.</h6>", unsafe_allow_html=True)

st.write(df.head(195))

# Filter - Zipcode and License Ststaus
st.divider()
st.markdown("<h4 style='text-align: center;color: #3C873A; font-family: Georgia;'> Filter by Zipcode and License Status </h4>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center;color: #FFFFFF; font-family: Georgia;'> This is a filter which allows you to look for Store Names, and their adressses, using the zipcode and license status. The results are sorted alphabetically according to the name of the store.</h6>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: left;color: #3C873A; font-family: Georgia;'> Select Facility Zip Codes </h6>", unsafe_allow_html=True)

selected_zip_codes = st.multiselect(
    "",
    df['facility_zip_code'].unique()
)

st.divider()
st.markdown("<h6 style='text-align: left;color: #3C873A; font-family: Georgia;'> Select App License Status </h6>", unsafe_allow_html=True)
selected_license_status = st.radio(
    "",
    df['app_license_status'].unique()
)

filtered_df = df[df['facility_zip_code'].isin(selected_zip_codes) & (df['app_license_status'] == selected_license_status)]
sorted_filtered_df = filtered_df.sort_values(by='app_business_name')

if not sorted_filtered_df.empty:
    for _, row in sorted_filtered_df.iterrows():
        st.write(f"**Business Name:** {row['app_business_name'] or 'N/A'}")
        st.write(f"**Address:** {row['facility_address'] or 'N/A'}")
        st.write("---")
else:
    st.write("No entries found for the selected conditions.")

# sidebar Image
st.sidebar.image('Weed-Background-Pictures.jpg')

# Filter 2 (sidebar) - Business Name and Address
selected_business_name = st.sidebar.selectbox("Select Business Name:", df['app_business_name'].dropna().unique())

selected_rows = df[df['app_business_name'] == selected_business_name]

facility_addresses = selected_rows['facility_address']
facility_zip_codes = selected_rows['facility_zip_code']

for address, zip_code in zip(facility_addresses, facility_zip_codes):
    st.sidebar.success(f"Facility Address: {address}-{zip_code}")

# Filter 3 (sidebar) - Owner Name and Business Nmae + License No.
st.sidebar.divider()

selected_name = st.sidebar.selectbox("Select Owner's Name:", df['id_full_name'].unique())
selected_row = df[df['id_full_name'] == selected_name]

business_name = selected_row['app_business_name'].iloc[0]
license_no = selected_row['app_license_no'].iloc[0]

st.sidebar.success(f"Business Name: {business_name}\n - {license_no}")
