import collections
import random

from django.test import TestCase
from faker import Faker

# Create your tests here.


def get_data():
    fake = Faker()
    return fake.name(locale='zh_CN')


if __name__ == '__main__':
    print(get_data())