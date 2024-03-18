from django.core.management.base import BaseCommand, CommandError
from models_portal.models import Post, Category


class Command(BaseCommand):
    help = 'Данная команда удаляет посты выбранной категории'

    def handle(self, *args, **options):

        category = Category.objects.all()

        for n in range(len(category)):
            self.stdout.write(self.style.SUCCESS(f'{n} - {category[n]}'))

        answer = int(input('Выберите номер нужной категории для удаления постов: '))
        self.stdout.write(self.style.SUCCESS(category[answer]))

        control_answer = input('Вы действительно хотите удалить новости выбранной категории(yes/no)? ')

        if control_answer.lower() == 'yes':
            try:
                Post.objects.filter(post_category_category=category[answer]).delete()
                self.stdout.write(self.style.SUCCESS('Посты успешно были удалены !!!'))
            except Post.DoesNotExist:
                self.stdout.write(self.style.ERROR('Посты не найдены в данной категории!!!'))
        else:
            self.stdout.write(self.style.ERROR('Ваше действие отменено'))
