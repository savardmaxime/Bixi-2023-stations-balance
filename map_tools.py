
import branca.colormap as cm
import folium

# function prepare map and add markers
def make_map(map_gdf, feature):
    linear = cm.linear.RdBu_10.scale(-50, 50)

    tooltip_html = """
    <table>
    <tr><td><strong style="margin-right:15px;">{0}</strong></td><td>{1}</td></tr>
    <tr><td><strong>{2}</strong></td><td>{3}</td></tr>
    </table>
    """

    center = map_gdf['geometry'].y.mean(), map_gdf['geometry'].x.mean()
    f = folium.Figure(width=800, height=600)
    m = folium.Map(location=center,
                zoom_start=12,
                tiles='CartoDB Positron',
                control_scale = True
                ).add_to(f)


    def add_markers(row):
        loc = (float(row['geometry'].y), float(row['geometry'].x))
        html = row[[feature,'name','arrondissement']].to_frame().to_html(classes="table table-striped table-hover table-condensed table-responsive")
        popup = folium.Popup(html, max_width=1500)
        folium.CircleMarker(loc,
                            radius=3,
                            column=feature,
                            color='gray',
                            weight=1,
                            fill=True,
                            fill_color=linear(row[feature]),
                            opacity=0.8,
                            fill_opacity=1,
                            popup=popup,
                            tooltip = tooltip_html.format('Station name', row['name'], feature, round(row[feature],2)),
                            ).add_to(m)
    


    map_gdf.apply(add_markers,axis=1)
    _ = linear.add_to(m)
    return m