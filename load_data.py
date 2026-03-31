import pandas as pd

# 1️⃣ Wczytanie CSV
df = pd.read_csv("data/RawData.csv")

# 2️⃣ Zostawienie tylko potrzebnych kolumn
df = df[['event_name','gender','nationality','age_group','division','total_time']]

# 3️⃣ Podgląd pierwszych 5 wierszy
print("Pierwsze 5 wierszy danych:")
print(df.head())

# 4️⃣ Konwersja total_time na sekundy
def time_to_seconds(t):
    h, m, s = t.split(':')
    return int(h)*3600 + int(m)*60 + int(s)

df['total_seconds'] = df['total_time'].apply(time_to_seconds)

# 5️⃣ Obliczenie top 10% w każdej kategorii (gender + division)
df['top'] = df.groupby(['gender','division'])['total_seconds'] \
               .transform(lambda x: x <= x.quantile(0.1))

# 6️⃣ Podgląd top vs reszta (pierwsze 10 wierszy)
print("\nTop zawodnicy (pierwsze 10 wierszy):")
print(df[df['top']].head(10))

print("\nReszta zawodników (pierwsze 10 wierszy):")
print(df[~df['top']].head(10))

#Liczba wszystkich zawodników i top 10%
print("\nLiczba wszystkich zawodników:", len(df))
print("Liczba zawodników w top 10%:", df['top'].sum())

#Pivot: średni czas top vs reszta w każdej kategorii
pivot = df.groupby(['gender','division','top'])['total_seconds'].mean().reset_index()

#Zamiana sekund na hh:mm:ss dla czytelności
def seconds_to_hms(s):
    h = s // 3600
    m = (s % 3600) // 60
    sec = s % 60
    return f"{int(h):02d}:{int(m):02d}:{int(sec):02d}"

pivot['avg_time_hms'] = pivot['total_seconds'].apply(seconds_to_hms)

#Wyświetlenie pivot
print("\nŚredni czas top vs reszta w każdej kategorii:")
print(pivot)

#Najszybszy i najwolniejszy zawodnik

#Najszybszy
fastest = df.loc[df['total_seconds'].idxmin()]

#Najwolniejszy
slowest = df.loc[df['total_seconds'].idxmax()]

print("\n🥇 Najszybszy zawodnik:")
print(fastest[['event_name','gender','division','total_time']])

print("\n🐢 Najwolniejszy zawodnik:")
print(slowest[['event_name','gender','division','total_time']])