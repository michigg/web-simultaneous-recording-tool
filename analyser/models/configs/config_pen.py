class ConfigPen:
    def __init__(self, pen_id, pen_brand, pen_brands):
        self.pen_id = pen_id
        self.pen_brand = pen_brand
        self.pen_brands = pen_brands

    @classmethod
    def from_json(cls, json_data):
        if not json_data:
            return None
        return cls(
            json_data["penId"],
            json_data["penBrand"],
            json_data["penBrands"]
        )

    def __str__(self):
        return f'Brand: {self.pen_brand}; ID: {self.pen_id}'