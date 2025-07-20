import yaml
import requests
import os
from pathlib import Path
import fire

class Cli:

  def make_path(self, c, s):
      # Sanitize category and subcategory name to make them viable folder names
      return (c+ "_" +s).lower() \
              .replace(" & ", "_") \
              .replace(" ", "_") \
              .replace("_-","") \
              .replace(",","") \
              .replace("/", "_")

  def get_only_letter(self, x: str, landscape: list):
      # Give us the letter we want, not best performance but does the job
      return { self.make_path(c['name'], sub['name']): [item
              for item in sub['items'] if item['name'].startswith(x)]
          for c in landscape for sub in c['subcategories']}

  def run(self):
    landscape_raw = requests.get("https://raw.githubusercontent.com/cncf/landscape/master/landscape.yml")
    landscape = yaml.safe_load(landscape_raw.content)['landscape']
    
    categories = { c['name']: {sub['name']: self.make_path(c['name'], sub['name'])
        for sub in c ['subcategories']} 
    for c in landscape }

    with open("data/category_index.yaml", 'w+') as file:
        documents = yaml.dump(categories, file)

    items = { c['name']: {sub['name']: [item['name']
            for item in sub['items']]\
        for sub in c['subcategories']} 
    for c in landscape }

    with open("data/category_item_index.yaml", 'w+') as file:
        documents = yaml.dump(items, file)

    with open("data/categories.yaml", 'w+') as file:
        categories = [{
            'category': c['name'],
            'subcategories': [{
                'subcategory': sub['name'],
                'path': self.make_path(c['name'], sub['name']),
                'items': [item['name'] for item in sub['items']]
            } for sub in c['subcategories']]
        } for c in landscape]
        yaml.dump(categories, file)

    for letter in range(ord('A'), ord('Z')+1):
        index = letter - ord('A')
        partial = self.get_only_letter(chr(letter), landscape)

        for key in partial:
            
            path = Path(f'data/week_{str(index).zfill(2)}_{chr(letter)}')
            path.mkdir(parents=True, exist_ok=True)
            path = path.joinpath(f"{key}.yaml")

            with open(path, 'w+') as file:
                documents = yaml.dump(partial[key], file)

    stats_per_category = {c['name']: len(c['subcategories']) for c in landscape}
    with open("data/stats_per_category.yaml", 'w+') as file:
        yaml.dump(stats_per_category, file)

    stats_per_category_per_week = {
        f"week_{str(index).zfill(2)}_{chr(letter)}": {
            c['name']: len(c['subcategories']) for c in landscape
        }
        for index, letter in enumerate(range(ord('A'), ord('Z') + 1))
    }
    with open("data/stats_per_category_per_week.yaml", 'w+') as file:
        yaml.dump(stats_per_category_per_week, file)


if __name__ == '__main__':
  fire.Fire(Cli)
