import requests
import folium
import logging
import branca
from datetime import datetime

class CongestionMap:
    def __init__(self, api_url, output_file,map):
        self.api_url = api_url
        self.output_file = output_file
        self.map = map

    @staticmethod
    def get_color(congestion):
        congestion_normalized = min(congestion / 40, 1)
        if congestion_normalized <= 0.5:
            red = int(255 * (congestion_normalized * 2))
            green = 255
            blue = 0
        else:
            red = 255
            green = int(255 * (2 * (1 - congestion_normalized)))
            blue = 0
        return f'#{red:02x}{green:02x}{blue:02x}'

    def fetch_data(self):
        response = requests.get(self.api_url)
        response.raise_for_status()
        return response.json()

    def add_routes_to_map(self, data):
        for item in data:
            origin = [item['origin_location']['Latitude'], item['origin_location']['Longitude']]
            destination = [item['destination_location']['Latitude'], item['destination_location']['Longitude']]
            congestion = item.get('congestion', 0)
            id = item.get('id', 0)
            name = item.get('name')
            color = self.get_color(congestion)

            line = folium.PolyLine(
                locations=[origin, destination],
                color=color,
                weight=5,
                opacity=0.7
            )

            popup_content = f"origin_location: {origin}<br>destination_location: {destination}<br>congestion: {congestion}<br>id: {id}<br>name: {name}"
            popup = folium.Popup(popup_content, max_width=300)
            tooltip = folium.Tooltip(popup_content)

            line.add_child(popup)
            line.add_child(tooltip)
            self.map.add_child(line)

    def add_legend(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        legend_html = f'''
         <div style="
         position: fixed; 
         bottom: 50px; left: 50px; width: 150px; height: 220px; 
         border:2px solid grey; z-index:9999; font-size:14px;
         background-color:white;
         padding: 10px;
         ">
         <b>Congestion Legend</b><br>
         <i style="background: #ff0000; width: 20px; height: 10px; display: inline-block;"></i> 20-40 <br>
         <i style="background: #ffff00; width: 20px; height: 10px; display: inline-block;"></i> 10-20 <br>
         <i style="background: #00ff00; width: 20px; height: 10px; display: inline-block;"></i> 0-10 <br>
         <br>
         <b>Current Time:</b><br>
         {current_time}
         </div>
         '''
        self.map.get_root().html.add_child(folium.Element(legend_html))

    def save_map(self):
        self.map.save(self.output_file)
        logger.info("Map created successfully")

    def generate_map(self):
        try:
            data = self.fetch_data()
            self.add_routes_to_map(data)
            self.add_legend()
            folium.LayerControl().add_to(self.map)
            #self.save_map()
        except Exception as e:
            logger.error(f"Failed to fetch data from the API: {e}")

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建 CongestionMap 实例并生成地图
api_url = "http://127.0.0.1:9090/realtimecongestion"
output_file = "path_map_white_background2.html"
congestion_map = CongestionMap(api_url, output_file,map)
##调用：
congestion_map.generate_map()
