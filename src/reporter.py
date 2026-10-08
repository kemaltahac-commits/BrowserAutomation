from pathlib import Path

import pandas as pd

# Proje kökünü dosya konumundan bul, çalıştırma dizininden bağımsız olsun
OUTPUT_FILE = Path(__file__).resolve().parent.parent / "output" / "all_books.xlsx"


class ReportGenerator:

    def create_report(self, products):
        print("Report oluşturuluyor...")
        print(f"Toplam ürün: {len(products)}")

        df = pd.DataFrame(products)

        print(f"Ortalama fiyat: {df['price'].mean():.2f}")
        print(f"En yüksek fiyat: {df['price'].max():.2f}")
        print(f"En düşük fiyat: {df['price'].min():.2f}")

        # output/ yoksa oluştur (FileNotFoundError'ı önler)
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

        df.to_excel(OUTPUT_FILE, index=False)

        print(f"Excel oluşturuldu: {OUTPUT_FILE}")

        return df