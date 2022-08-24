from django.core.management.base import BaseCommand

from Common.Mongo import mycol

import random

from Sign.models import DayRecommends


class Command(BaseCommand):
    def handle(self, *args, **options):
        DayRecommends.objects.all().delete()
        citys = mycol.distinct("City")  # List
        categorys = ["밥집", "술집", "카페"]
        for city in citys:
            for category in categorys:
                mongodata = mycol.find({"City": city, "Category": category},
                                       {"_id": 1, "City": 1, "Category": 1, "Image": 1, "Name": 1, "Address": 1})
                random_datas = random.sample(list(mongodata), 5)

                for random_data in random_datas:
                    DayRecommends.objects.create(restaurant_id=random_data["_id"],
                                                 city=random_data["City"], category=random_data['Category'],
                                                 image=random_data["Image"], name=random_data["Name"],
                                                 address=random_data["Address"])