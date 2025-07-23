from src.logger import get_logger

logger = get_logger(__name__)

def make_path(c: str, s: str) -> str:
    """
    This function sanitize a category and subcategory name to make it a viable folder name
    """
    return (c + "_" + s).lower() \
        .replace(" & ", "_") \
        .replace(" ", "_") \
        .replace("_-", "") \
        .replace(",", "") \
        .replace("/", "_")

class Transformer:
    def __init__(self, landscape_data):
        self.landscape_data = landscape_data
        self.categories = {}
        self.items = {}
        self.all_categories = []
        self.stats_per_category = {}
        self.stats_by_status = {}

    def transform(self):
        logger.info("Transforming landscape data...")
        for category in self.landscape_data:
            cat_name = category['name']
            self.stats_per_category[cat_name] = len(category['subcategories'])
            self.categories[cat_name] = {}
            self.items[cat_name] = {}

            subcategories_list = []
            for subcategory in category['subcategories']:
                sub_name = subcategory['name']
                path = make_path(cat_name, sub_name)
                self.categories[cat_name][sub_name] = path

                item_names = [item['name'] for item in subcategory['items'] if item.get('project') != 'archived']
                self.items[cat_name][sub_name] = item_names

                subcategories_list.append({
                    'subcategory': sub_name,
                    'path': path,
                    'items': item_names
                })

                for item in subcategory['items']:
                    status = item.get('project')
                    if status:
                        self.stats_by_status[status] = self.stats_by_status.get(status, 0) + 1

            self.all_categories.append({
                'category': cat_name,
                'subcategories': subcategories_list
            })

        logger.info("Finished transforming landscape data.")
        return {
            "categories": self.categories,
            "items": self.items,
            "all_categories": self.all_categories,
            "stats_per_category": self.stats_per_category,
            "stats_by_status": self.stats_by_status,
        }
