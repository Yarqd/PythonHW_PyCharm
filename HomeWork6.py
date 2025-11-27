import csv
import json

PURCHASE_FILE = 'resources/purchase_log.txt'
VISIT_FILE = 'resources/visit_log__1_.csv'
FUNNEL_FILE = "resources/funnel.csv"

def load_purchases(path: str) -> dict:
    purchases = {}
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            data = json.loads(line)

            if data.get('user_id') == 'user_id':
                continue

            purchases[data['user_id']] = data['category']
    return purchases


def make_funnel(visit_path: str, purchase_path: str, funnel_path: str) -> None:
    purchases = load_purchases(purchase_path)

    with open(visit_path, encoding='utf-8') as fin, \
         open(funnel_path, 'w', encoding='utf-8', newline='') as fout:

        reader = csv.reader(fin)
        writer = csv.writer(fout)

        header = next(reader)
        header.append('category')
        writer.writerow(header)

        for row in reader:
            user_id = row[0]
            category = purchases.get(user_id)

            if category is None:
                continue

            writer.writerow(row + [category])


if __name__ == '__main__':
    make_funnel(VISIT_FILE, PURCHASE_FILE, FUNNEL_FILE)
    print('Готово, создан файл', FUNNEL_FILE)