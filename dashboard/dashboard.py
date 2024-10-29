import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set up the page
st.title("Dashboard Bike Sharing Data Analysis")
st.write("By: Vivi Kurniawati")

# Dataset
df = pd.read_csv('dashboard/hour.csv')

# Data Wrangling
df['date'] = pd.to_datetime(df['dteday'])
df.rename(columns={
    'instant': 'record_index',
    'season': 'season',
    'yr': 'year',
    'mnth': 'month',
    'hr': 'hour',
    'holiday': 'is_holiday',
    'weekday': 'weekday',
    'workingday': 'is_workingday',
    'weathersit': 'weather_condition',
    'temp': 'temp_normalized',
    'atemp': 'atemp_normalized',
    'hum': 'humidity_normalized',
    'windspeed': 'windspeed_normalized',
    'casual': 'casual_count',
    'registered': 'registered_count',
    'cnt': 'total_count'
}, inplace=True)

# Sidebar Filters
st.sidebar.header("Filter Data")
year = st.sidebar.selectbox("Select Year", options=[2011, 2012], index=0)
season = st.sidebar.multiselect("Select Season", options=[1, 2, 3, 4], default=[1, 2, 3, 4])

filtered_df = df[(df['year'] == year - 2011) & (df['season'].isin(season))]

# Display Data
st.write("### Data Overview")
st.write(filtered_df.head())

# Exploratory Analysis

## Pertanyaan 1
st.write("### Pengaruh Cuaca terhadap Jumlah Penyewaan Sepeda")
weather_effect = filtered_df.groupby('weather_condition')['total_count'].mean()

fig, ax = plt.subplots()
sns.barplot(x=weather_effect.index, y=weather_effect.values, palette="Blues", ax=ax)
ax.set_title('Pengaruh Cuaca terhadap Jumlah Penyewaan')
ax.set_xlabel('Kondisi Cuaca')
ax.set_ylabel('Rata-rata Jumlah Penyewaan')
st.pyplot(fig)

## Pertanyaan 2
st.write("### Jumlah Penyewaan Berdasarkan Hari dalam Minggu")
rentals_by_weekday = filtered_df.groupby('weekday')['total_count'].sum().sort_values()

fig, ax = plt.subplots()
sns.barplot(x=rentals_by_weekday.index, y=rentals_by_weekday.values, palette="viridis", ax=ax)
ax.set_title('Jumlah Penyewaan Sepeda Berdasarkan Hari')
ax.set_xlabel('Hari dalam Minggu')
ax.set_ylabel('Total Penyewaan')
st.pyplot(fig)

## Pertanyaan 3
st.write("### Pola Penyewaan Musim Panas vs Musim Dingin")
summer_data = filtered_df[filtered_df['season'] == 2]
winter_data = filtered_df[filtered_df['season'] == 4]
summer_pattern = summer_data.groupby('hour')['total_count'].mean()
winter_pattern = winter_data.groupby('hour')['total_count'].mean()

fig, ax = plt.subplots()
ax.plot(summer_pattern, label='Musim Panas', color='orange', linestyle='-', linewidth=2)
ax.plot(winter_pattern, label='Musim Dingin', color='blue', linestyle='--', linewidth=2)
ax.set_title('Pola Penyewaan Sepeda pada Musim Panas vs Musim Dingin')
ax.set_xlabel('Jam')
ax.set_ylabel('Rata-rata Jumlah Penyewaan')
ax.legend()
st.pyplot(fig)

## Pertanyaan 4
st.write("### Tren Penyewaan Sepeda Selama Dua Tahun")
monthly_trend = filtered_df.groupby(['year', 'month'])['total_count'].mean().unstack()

fig, ax = plt.subplots()
monthly_trend.T.plot(kind='line', marker='o', ax=ax)
ax.set_title('Tren Penyewaan Sepeda Selama Dua Tahun')
ax.set_xlabel('Bulan')
ax.set_ylabel('Rata-rata Jumlah Penyewaan')
ax.legend(['2011', '2012'])
st.pyplot(fig)

# Conclusion
st.write("## Conclusion")
st.write("""
1. Cuaca: Penyewaan sepeda lebih tinggi saat cuaca cerah dan menurun saat cuaca buruk.
2. Hari Penyewaan: Penyewaan paling tinggi pada hari kerja, terutama pada hari Jumat.
3. Musim: Musim panas menunjukkan jumlah penyewaan lebih tinggi dan stabil sepanjang hari.
4. Tren Tahunan: Penyewaan meningkat dari 2011 ke 2012.
""")
