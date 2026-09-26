import pandas as pd


class ReportGenerator:

    def create_report(self, products):
        print("Report oluşturuluyor...")
        print(f"Toplam ürün: {len(products)}")

        df = pd.DataFrame(products)

        print(f"Ortalama fiyat: {df['price'].mean():.2f}")
        print(f"En yüksek fiyat: {df['price'].max():.2f}")
        print(f"En düşük fiyat: {df['price'].min():.2f}")

        output_file = "output/all_books.xlsx"

        df.to_excel(output_file, index=False)

        print(f"Excel oluşturuldu: {output_file}")

        return df