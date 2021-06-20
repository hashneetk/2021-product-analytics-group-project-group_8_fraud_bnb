import folium
import matplotlib as mpl
import matplotlib.pyplot as plt
from sqlalchemy.orm import load_only

from app import classes

def map_html(max_listing):
    map = folium.Map(
        [34.052235, -118.243683], zoom_start=11,
    )

    color_map = plt.get_cmap('RdYlGn')
    query_res = classes.Listings.query \
        .filter(classes.Listings.listing_reliability.isnot(None)) \
        .filter(classes.Listings.latitude.isnot(None)) \
        .options(
            load_only(
                classes.Listings.listing_id,
                classes.Listings.listing_reliability,
                classes.Listings.latitude,
                classes.Listings.longtitude,
            )
        ) \
        .distinct(classes.Listings.listing_id).limit(max_listing)

    for res in query_res:
        score = round(res.listing_reliability, 2)
        color_hex = mpl.colors.rgb2hex(color_map(score/100))

        folium.CircleMarker(
            location=[res.latitude, res.longtitude],
            popup=f'ID: {res.listing_id}\nScore : {score}',
            radius=8,
            color=color_hex,
            fill_color=color_hex,
            fill_opacity=1,
            tooltip = "Click for more"
        ).add_to(map)

    return map._repr_html_()