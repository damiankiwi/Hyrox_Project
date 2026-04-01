import pandas as pd
import matplotlib.pyplot as plt

#Wczytanie CSV
df = pd.read_csv("../data/RawData.csv")

#Zostawienie potrzebnych kolumn i filtr tylko open i pro
df = df[['gender', 'division', 'total_time']]
df = df[df['division'].isin(['open', 'pro'])]


#Konwersja total_time na sekundy
def time_to_seconds(t):
    h, m, s = t.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)


df['total_seconds'] = df['total_time'].apply(time_to_seconds)

#Obliczenie top 10% w każdej kategorii (gender + division)
df['top'] = df.groupby(['gender', 'division'])['total_seconds'] \
    .transform(lambda x: x <= x.quantile(0.1))

#Pivot średnich czasów Top vs Reszta
pivot = df.groupby(['gender', 'division', 'top'])['total_seconds'].mean().reset_index()

#Rysowanie wykresu z posortowaniem według średniego czasu Top
genders = df['gender'].unique()
plt.figure(figsize=(12, 6))

for i, gender in enumerate(genders, 1):
    plt.subplot(1, len(genders), i)
    gender_data = pivot[pivot['gender'] == gender]

    # sortujemy division wg średniego czasu Top
    top_data = gender_data[gender_data['top'] == True].sort_values('total_seconds')
    rest_data = gender_data[gender_data['top'] == False].set_index('division').loc[top_data['division']].reset_index()

    x = range(len(top_data))
    plt.bar([xi - 0.15 for xi in x], top_data['total_seconds'], width=0.3, label='Top 10%', color='green')
    plt.bar([xi + 0.15 for xi in x], rest_data['total_seconds'], width=0.3, label='Reszta', color='gray')

    plt.xticks(x, top_data['division'], rotation=45)
    plt.ylabel('Średni czas (sekundy)')
    plt.title(f'{gender.capitalize()} - Open & Pro (Top posortowane)')
    plt.legend()

plt.tight_layout()
plt.show()