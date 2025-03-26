import geopandas as gpd
import folium
import unicodedata

# 🔤 Türkçe karakter temizleyici
def temizle(metin):
    if not isinstance(metin, str): return ""
    return unicodedata.normalize('NFKD', metin).encode('ascii', 'ignore').decode('utf-8').lower()

# 📁 Dosya yolları
il_geojson_path = "./data/tr.json"
ilce_shapefile_path = "./data/İl_İlçe_Sınır_ve_Yerleşim_Verisi/Yerlesim_Noktas.shp"

# ✅ Kayyum listeleri
kayyum_iller = [
    "Batman",
    "Hakkari",
    "Mardin Büyükşehir",
    "Siirt",
    "Tunceli",
    "Van Büyükşehir"
]
kayyum_ilçeler = [
  "Akdeniz",
  "Bahçesaray",
  "Esenyurt",
  "Halfeti",
  "Kağızman",
  "Şişli"
]

kayyum_iller_temiz = [temizle(x) for x in kayyum_iller]
kayyum_ilceler_temiz = [temizle(x) for x in kayyum_ilçeler]

# 📍 1. İllerin GeoJSON'unu oku
iller_gdf = gpd.read_file(il_geojson_path)
iller_gdf['il_temiz'] = iller_gdf['name'].apply(temizle)
iller_gdf['renk'] = iller_gdf['il_temiz'].apply(lambda x: 'black' if x in kayyum_iller_temiz else 'red')
iller_gdf = iller_gdf.to_crs(epsg=4326)

# 📍 2. İlçelerin shapefile’ını oku
ilceler_gdf = gpd.read_file(ilce_shapefile_path)
ilceler_gdf['kategori_temiz'] = ilceler_gdf['KATEGORI'].apply(temizle)
ilceler_gdf['adi_temiz'] = ilceler_gdf['Adı'].apply(temizle)

# 🔍 Sadece kayyum ilçelerini filtrele
kayyum_ilceler_gdf = ilceler_gdf[
    (ilceler_gdf['kategori_temiz'] == 'ilce') &
    (ilceler_gdf['adi_temiz'].isin(kayyum_ilceler_temiz))
].copy()
kayyum_ilceler_gdf = kayyum_ilceler_gdf.to_crs(epsg=4326)

# 🌍 Folium haritası oluştur
m = folium.Map(location=[39, 35], zoom_start=6, tiles="cartodbpositron")

# 🟫 İllerin sınırlarını çiz
for _, row in iller_gdf.iterrows():
    folium.GeoJson(
        row['geometry'],
        style_function=lambda feature, renk=row['renk']: {
            'fillColor': renk,
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.7,
        },
        tooltip=folium.Tooltip(f"{row['name']} Belediyesi")
    ).add_to(m)

# 📍 Kayyum ilçeleri POINT olarak göster
for _, row in kayyum_ilceler_gdf.iterrows():
    coords = [row.geometry.y, row.geometry.x]  # (lat, lon)
    folium.CircleMarker(
        location=coords,
        radius=7,
        color='black',
        fill=True,
        fill_color='black',
        fill_opacity=0.9,
        tooltip=folium.Tooltip(f"{row['Adı']} Belediyesi")  # ilçe adı
    ).add_to(m)

# 💾 HTML olarak kaydet
m.save("interaktif_kayyum_il_ilce_harita.html")
print("✅ interaktif_kayyum_il_ilce_harita.html oluşturuldu!")
