from django.core.management.base import BaseCommand
from products.models import ProductCategory

CATEGORIES = [
    ("Di động", "01010000", "https://stg-images.samsung.com/is/image/samsung/assets/vn/2501/pcd/smartphones/Visual_LNB_All-Smartphones__144x144.png?$ORIGIN_PNG$"),
    ("Máy tính bảng", "01020000", "https://images.samsung.com/is/image/samsung/p6pim/vn/epp/vn-eppcms-co04image-543870611?$100_100_IMG$"),
    ("Thiết bị đeo", "01030000", "https://images.samsung.com/is/image/samsung/p6pim/vn/epp/vn-eppcms-co04image-542624677?$100_100_IMG$"),
    ("TV & AV", "04010000", "https://images.samsung.com/is/image/samsung/p6pim/vn/epp/vn-eppcms-co04image-542106139?$100_100_IMG$"),
    ("Tủ lạnh", "08030000", "https://images.samsung.com/is/image/samsung/p6pim/vn/epp/vn-eppcms-co04image-545500021?$100_100_IMG$"),
    ("Máy giặt sấy", "08010000", "https://images.samsung.com/is/image/samsung/p6pim/vn/epp/vn-eppcms-co04image-545500023?$100_100_IMG$"),
    ("Màn hình", "07010000", "https://images.samsung.com/is/image/samsung/p6pim/vn/epp/vn-eppcms-co04image-536891303?$100_100_IMG$"),
    ("Điều hòa", "08050000", "https://images.samsung.com/is/image/samsung/p6pim/vn/epp/vn-eppcms-co04image-538342531?$100_100_IMG$"),
    ("Bộ nhớ", "09010000", "https://images.samsung.com/is/image/samsung/p6pim/vn/epp/vn-eppcms-co04image-540753566?$100_100_IMG$"),
    ("Thiết bị nhà bếp", "08080000", "https://images.samsung.com/is/image/samsung/p6pim/vn/epp/vn-eppcms-co04image-540753568?$100_100_IMG$")
]

class Command(BaseCommand):
    help = "Thêm danh mục mặc định nếu chưa có"

    def handle(self, *args, **kwargs):
        count = 0
        for name, type_code, thumb_url in CATEGORIES:
            if not ProductCategory.objects.filter(type_code=type_code).exists():
                ProductCategory.objects.create(name=name, type_code=type_code, thumb_url=thumb_url)
                count += 1
                self.stdout.write(self.style.SUCCESS(f'✔ Đã thêm: {name}'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠ Đã tồn tại: {name}'))

        if count == 0:
            self.stdout.write(self.style.SUCCESS("✅ Không có danh mục mới cần thêm."))
        else:
            self.stdout.write(self.style.SUCCESS(f"🎉 Đã thêm {count} danh mục mới."))

