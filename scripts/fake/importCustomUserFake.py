import django
import os
import sys
from django.contrib.auth.hashers import make_password
import random

from faker import Faker
fake = Faker('ja-JP')
Faker.seed(0)

sys.path.append('/path/to/Djangi/project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.develop')

django.setup()
from accounts.models import CustomUser
"""
custome_user_obj = []
for _ in range(500):
	custome_user_obj.append(
		CustomUser(
			last_name=fake.last_name(),
			first_name=fake.first_name(),
			email=fake.user_name()+str(random.randint(10, 9999))+'@'+fake.domain_name(),
			password=make_password(fake.password(12)),
			company=fake.company(),
			occupation=fake.job(),
			username=fake.user_name()
	  )
	)
CustomUser.objects.bulk_create(custome_user_obj)
"""
dept=['企画部', '営業部', '物流部', '総務部', '経理部', '人事部', '技術部', '管理部', '法務部', '財務部', '情報システム部', 'マーケティング部', ]
post=['部長','課長','部長代理','課長代理','副部長','専任部長','次長','部長補佐','課長補佐','係長','参与','参事','主幹','主任','主査','ディレクター','マネージャー','チーフマネージャー','チーフディレクター',]

for _ in range(10000):
	CustomUser.objects.create(
		last_name=fake.last_name(),
		first_name=fake.first_name(),
		email=fake.user_name() + str(random.randint(10, 9999)) + '@' + fake.domain_name(),
		password=make_password(fake.password(12)),
		company=fake.company(),
		occupation=fake.job(),
		username=fake.user_name(),
		department=random.choice(dept),
		position=random.choice(post),
		mobile=random.randrange(10**10,10**11)
	)
