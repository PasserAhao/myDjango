from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "this is a test demo"

    def add_arguments(self, parser):
        parser.add_argument('args', nargs='*', type=str, help='Multiple arguments')

    def handle(self, *args, **options):
        print(args)
        print(options)
        # 重置所有文本样式
        reset = "\033[0m"

        # 不同颜色的 ANSI 转义码
        red = "\033[31m"
        arg1 = f"{red}红色文本{reset}"
        self.stdout.write(f'Argument 1: {arg1}')
