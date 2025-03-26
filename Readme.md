# 🗺️ Kayyum Harita Projesi

Bu web projesi, Türkiye'de kayyum atanan il ve ilçelerin görsel olarak harita üzerinde gösterilmesini amaçlar.  
Proje, statik HTML + CSS + JavaScript altyapısıyla hazırlanmıştır ve Python/Folium ile oluşturulan interaktif haritayı içerir.

---

## 🎯 Proje Amacı

Bu projede:

- Kayyum atanan iller ve ilçeler görselleştirilmiştir.
- Veriler, açık kaynak shapefile ve geojson dosyalarından alınmıştır.
- Harita, `folium` kütüphanesi kullanılarak oluşturulmuştur.
- Kullanıcı dostu ve mobil uyumlu bir arayüz hedeflenmiştir.

---

## 📁 Klasör Yapısı
```
harita-projesi/
│
├── data/                                   # Shapefile ve GeoJSON veri dosyaları
│   ├── Yerlesim_Noktas.shp
│   └── tr.json
│
├── images/                                 # Görseller (logo vb.)
│   └── kayyum_logo.png
│
├── index.html                              # Ana sayfa (harita içerir)
├── bilgi.html                              # Bilgi ve kaynak sayfası
├── style.css                               # Tüm sayfa stilleri
├── map_embedder.py                         # Haritayı HTML’e gömmek için script
├── index_template.html                     # index.html dönüşümü için template sayfa
├── interaktif_kayyum_harita.py             # Haritayı oluşturan ve işaretleyen script
├── interaktif_kayyum_il_ilce_harita.html   # Sadece haritayı gösteren sayfa
└── README.md                               # Bu dosya
```
---

## 🛠️ Kullanılan Teknolojiler

- HTML5, CSS3
- JavaScript (folium üzerinden Leaflet.js)
- Python 3 (folium, geopandas, beautifulsoup4)
- Leaflet + CDN kaynakları

---

## 🚀 Projeyi Çalıştırmak

1. Gerekli Python paketlerini yükle:

```bash
pip install folium geopandas beautifulsoup4
```

2. Haritayı oluşturmak için
```bash
python3 interaktif_kayyum_harita.py
```

3. index.html 'i oluşturmak için
```bash
python3 map_embedder.py
```

4. projeyi başlatmak için
```bash
python3 -m http.server
```

5. Tarayıcıda aç
http://localhost:8000/index.html
