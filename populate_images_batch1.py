"""
Populate image_url for products with official manufacturer product images
(sourced from each product's official page meta og:image / hero image).
First batch of the image-sourcing effort -- none of the 244 products had
an image_url populated before this. Images are hotlinked directly to the
manufacturer's own official CDN, matching the existing frontend rendering
pattern (<img src="{image_url}">) with graceful fallback to an icon if a
link ever breaks.

Run once: python3 populate_images_batch1.py
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

IMAGES = {
    26: "https://pim-media.roche.com/Images/Product_INS_7235_im_en.jpg?scl=1",  # Roche cobas 6800
    115: "https://www.mindray.com/content/dam/xpace/en/products-solutions/products/laboratory-diagnostics/hematology/medium-test-volume/bc-6800-plus/glp5-s1-kv.jpg",  # Mindray BC-6800Plus
    23: "https://www.stago-us.com/sites/stago_us/files/inline-images/Star%20Max-v3_1.png",  # Diagnostica Stago STA R Max
    150: "https://www.cepheid.com/content/dam/www-cepheid-com/images/pep/cards/cep-genexpert-4-module-system.jpeg",  # Cepheid GeneXpert
}

def main():
    conn = sqlite3.connect(DB_PATH)
    updated = 0
    for pid, url in IMAGES.items():
        row = conn.execute("SELECT id, product_name, image_url FROM products WHERE id = ?", (pid,)).fetchone()
        if not row:
            print(f"SKIP (not found): id={pid}")
            continue
        if row[2]:
            print(f"SKIP (already has image_url): id={pid} ({row[1]})")
            continue
        conn.execute("UPDATE products SET image_url = ? WHERE id = ?", (url, pid))
        print(f"UPDATED: id={pid} ({row[1]}) -> {url}")
        updated += 1
    conn.commit()
    conn.close()
    print(f"\nDone. Updated: {updated}")

if __name__ == "__main__":
    main()
