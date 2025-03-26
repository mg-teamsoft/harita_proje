import folium

m = folium.Map(location=[39, 35], zoom_start=6)
m.save("test_map.html")
