from django.db import migrations

def transfer_images_to_cloudinary(apps, schema_editor):
    # Достаем модель Product из приложения catalog
    Product = apps.get_model('catalog', 'Product') 
    
    for product in Product.objects.all():
        # Если картинка привязана и путь локальный (не ссылка http)
        if product.image and not str(product.image).startswith('http'):
            try:
                name = product.image.name
                # Открываем локальный файл и пересохраняем через Cloudinary хранилище
                with product.image.open('rb') as f:
                    product.image.save(name, f, save=True)
                print(f"Успешно перенесено в Cloudinary: {product.name}")
            except Exception as e:
                print(f"Ошибка при переносе {product.name}: {e}")

class Migration(migrations.Migration):

    dependencies = [
        # Тут Django сам автоматически укажет предыдущую миграцию, не трогай её
    ]

    operations = [
        migrations.RunPython(transfer_images_to_cloudinary),
    ]