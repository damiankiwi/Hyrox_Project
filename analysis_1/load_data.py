import pandas as pd
import os

#Ścieżka do pliku (działa niezależnie od miejsca uruchomienia)
base_dir = os.path.dirname(os.path.dirname(__file__))
file_path = os.path.join(base_dir, "data", "RawData.csv")

#Wczytanie CSV
df = pd.read_csv(file_path)

#Zostawienie tylko potrzebnych kolumn
df = df[['event_name', 'gender', 'nationality', 'age_group', 'division', 'total_time']]

#Podgląd danych
print("Pierwsze 5 wierszy danych:")
print(df.head())

#Konwersja czasu na sekundy (bezpieczna)
def time_to_seconds(t):
    try:
        h, m, s = t.split(':')
        return int(h) * 3600 + int(m) * 60 + int(s)
    except:
        return None

df['total_seconds'] = df['total_time'].apply(time_to_seconds)

# usunięcie błędnych rekordów (jeśli jakieś są)
df = df.dropna(subset=['total_seconds'])

#Top 10%
df['top'] = df.groupby(['gender', 'division'])['total_seconds'] \
              .transform(lambda x: x <= x.quantile(0.1))

#Podgląd danych
print("\nTop zawodnicy:")
print(df[df['top']].head(10))

print("\nReszta zawodników:")
print(df[~df['top']].head(10))

#Statystyki
print("\nLiczba wszystkich zawodników:", len(df))
print("Liczba zawodników w top 10%:", df['top'].sum())

#Pivot – średnie czasy
pivot = df.groupby(['gender', 'division', 'top'])['total_seconds'].mean().reset_index()

#Zamiana sekund na HH:MM:SS
def seconds_to_hms(s):
    h = int(s // 3600)
    m = int((s % 3600) // 60)
    sec = int(s % 60)
    return f"{h:02d}:{m:02d}:{sec:02d}"

pivot['avg_time_hms'] = pivot['total_seconds'].apply(seconds_to_hms)

print("\nŚredni czas top vs reszta:")
print(pivot)

#Najszybszy i najwolniejszy zawodnik
fastest = df.loc[df['total_seconds'].idxmin()]
slowest = df.loc[df['total_seconds'].idxmax()]

print("\nNajszybszy zawodnik:")
print(fastest[['event_name', 'gender', 'division', 'total_time']])

print("\nNajwolniejszy zawodnik:")
print(slowest[['event_name', 'gender', 'division', 'total_time']])