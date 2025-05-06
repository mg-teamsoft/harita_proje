import geopandas as gpd
import folium
import json

# İl sınırlarını oku
gdf = gpd.read_file("./data/tr.json").to_crs(epsg=4326)

# İlçeleri oku
yerlesim_gdf = gpd.read_file("./data/İl_İlçe_Sınır_ve_Yerleşim_Verisi/Yerlesim_Noktas.shp").to_crs(epsg=4326)

# Kayyum listeleri
kayyum_iller = [
    "Batman",
    "Hakkari",
    "Mardin Büyükşehir",
    "Siirt",
    "Tunceli",
    "Van Büyükşehir"
]
kayyum_ilceler = [
  "Akdeniz",
  "Bahçesaray",
  "Esenyurt",
  "Halfeti",
  "Kağızman",
  "Şişli"
]
ilce_kayyumlu_iller = ["İstanbul Büyükşehir", "Kars", "Şanlıurfa Büyükşehir", "Mersin Büyükşehir"]

# Harita oluştur
m = folium.Map(location=[39, 35], zoom_start=6)

# Tüm iller darkgray olarak başlasın
def style_function(feature):
    return {
        'fillColor': 'darkgray',
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.7
    }

# GeoJson katmanı
geojson = folium.GeoJson(
    data=gdf,
    name='İller',
    style_function=style_function,
    tooltip=folium.GeoJsonTooltip(fields=["name"], aliases=[""])
).add_to(m)

toggle_js = f"""
<script>
window.addEventListener("load", function () {{
    alertify.set('notifier','position', 'buttom-right');
    alertify.set('notifier','delay', 3);

    const kayyumIller = {json.dumps(kayyum_iller)};
    const ilceKayyumluIller = {json.dumps(ilce_kayyumlu_iller)};

    function getNextColor(current, name) {{
        if (current === 'darkgray') {{
            return kayyumIller.includes(name) ? 'black' : 'red';
        }}
        return 'darkgray';
    }}

    function setColor(layer, color) {{
        layer.setStyle({{ fillColor: color }});
        layer.feature.properties._fillColor = color;
    }}

    function showKayyumMessage(il_adi) {{
        if (kayyumIller.includes(il_adi)) {{
            alertify.error(`${{il_adi}} : kayyum atanmış.`, 10);
        }} else if (ilceKayyumluIller.includes(il_adi)) {{
            alertify.warning(`${{il_adi}} : bazı ilçe belediyelerine kayyum atanmış.`, 6);
        }} else {{
            alertify.success(`${{il_adi}} : kayyum atanmamış.`);
        }}
    }}

    const geojson = {geojson.get_name()};
    geojson.eachLayer(function(layer) {{
        const name = layer.feature.properties.name;

        if (!layer.feature.properties._fillColor) {{
            layer.feature.properties._fillColor = 'darkgray';
        }}

        layer.on('click', function(e) {{
            const current = layer.feature.properties._fillColor;
            const next = getNextColor(current, name);
            setColor(layer, next);

            if (next !== 'darkgray') {{
                showKayyumMessage(name);
            }}
        }});
    }});
}});
</script>
"""

m.get_root().script.add_child(folium.Element(toggle_js))

# Kayyum ilçeleri filtrele
ilce_points = yerlesim_gdf[yerlesim_gdf["Adı"].isin(kayyum_ilceler)]

# Her ilçe için siyah nokta
for _, row in ilce_points.iterrows():
    coords = [row.geometry.y, row.geometry.x]
    folium.CircleMarker(
        location=coords,
        radius=6,
        color='darkgray',
        fill=True,
        fill_color='darkgray',
        fill_opacity=0.7,
        tooltip=f"{row['Adı']} Belediyesi"
    ).add_to(m)

m.save("interaktif_kayyum_oyun.html")
print("✅ interaktif_kayyum_oyun.html başarıyla oluşturuldu.")