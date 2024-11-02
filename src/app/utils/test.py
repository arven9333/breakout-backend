s = [{
    "map_id": 52,
    "name": "Тест",
    "status": "wait",
    "layers": [
      {
        "map_layer_id": 132,
        "height": 7680,
        "width": 7680,
        "leaflet_path": "images/maps/52/132/tiles",
        "levels": {
          "easy": {
            "map_level_id": 349,
            "icons": [
              {
                "icon_level_id": 378,
                "coord_x": -88.23942724915767,
                "coord_y": -52.898619078566306,
                "radius": 18,
                "radius_color": "#F43636",
                "icon_id": 44,
                "image": "images/icons/6/48ef10c1a95a489f8b7b726b3708e705.svg"
              }
            ],
            "figures": [
              {
                "icon_metric_figure_id": 1,
                "coord_x": 1.23,
                "coord_y": 1.23,
                "color": "any_color",
                "content": "any_content",
                "type": "circle",
                "bold": 0,
              }
            ]
          },
          "hard": {
            "map_level_id": 351,
            "icons": []
          },
          "medium": {
            "map_level_id": 350,
            "icons": []
          }
        }
      }
    ]
  }
]
d = [
  {
    "action": "create",
    "type": "icon_metric_figure",
    "data": {
      "map_level_id": 1,
      "coord_x": 1.23,
      "coord_y": 1.23,
      "color": "any_color",
      "content": "any_content",
      "type": "circle", #береться из types
      "bold": 0, #не обязательное
    }
  },
  {
    "action": "update",
    "type": "icon_metric_figure",
    "data": {
      "map_level_id": 1,
      "icon_metric_figure_id": 1,
      "coord_x": 1.23,
      "coord_y": 1.23,
      "color": "any_color",
      "content": "any_content",
      "type": "circle",  # береться из types
      "bold": 0,  # не обязательное
    }
  },
  {
    "action": "delete",
    "type": "icon_metric_figure",
    "data": {
      "icon_metric_figure_id": 1
    }
  }
]


d = """
- координаты как сейчас 
- цвет 
- контент 
- элемент класс (значения: круг, квадрат, произвольная фигура, карандаш, маркер, надпись) 
- жирность(не обязательный параметр)
- мапЛвлАйди
"""