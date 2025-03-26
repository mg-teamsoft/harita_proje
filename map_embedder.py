# import folium
from bs4 import BeautifulSoup
import os

# Haritayı üret
# m = folium.Map(location=[39, 35], zoom_start=6, tiles="cartodbpositron")

# Geçici harita HTML dosyasına kaydet
# temp_map_path = "interaktif_harita.html"
origin_map_path = "interaktif_kayyum_il_ilce_harita.html"

# m.save(temp_map_path)

# HTML içeriğini oku
with open(origin_map_path, encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# Harita div (id="map_xxx" olan div)
map_div = soup.find("div", id=lambda x: x and x.startswith("map_"))
map_div_html = str(map_div)

# JavaScript script tag'lerini sırayla al
script_tags = soup.find_all("script")
scripts_html = "\n".join([str(tag) for tag in script_tags])

# CSS + meta içeren HEAD kısmı
head_html = str(soup.find("head"))

# index_template.html şablonunu oku
with open("index_template.html", encoding="utf-8") as f:
    template_html = f.read()

# HARITA_BODY = map div + tüm script'ler
harita_body_html = map_div_html

# Şablondaki yerleri değiştir
final_html = template_html \
    .replace("{{ HARITA_HEAD }}", head_html) \
    .replace("{{ HARITA_BODY }}", harita_body_html) \
    .replace("{{ HARITA_SCRIPT }}", scripts_html)

# index.html olarak kaydet
with open("index.html", "w", encoding="utf-8") as f:
    f.write(final_html)

# Geçici dosyayı temizle
# os.remove(temp_map_path)

print("✅ Harita başarıyla index.html içine gömüldü!")
