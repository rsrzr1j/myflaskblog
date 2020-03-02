#创建数据库模型后就编写生成虚拟数据的函数，便于编写前后台程序

#生成虚拟管理员信息
from bluelog.models import Admin
from bulelog.extensions import db

def fake_admin():
	admin=Admin(
		username='admin',blog_title='Bluelog',
		blog_sub_title="No,I'm the real thing.",
		name='Mima Kirigoe',
		about='Um,l,Mima kirigoe,had a fun time as a member of CHAM...'
	)
	admin.set_password('helloflask')
	db.session.add(admin)
	db.session.commit()

#生成虚拟分类信息
from faker import Faker 
from bluelog.models import Category

fake=Faker()

def fake_categories(count=10):
	category=Category(name='Default')
	#先创建一个默认分类，用于创建文章时默认的分类
	db.session.add(category)
	#生成包含随机名称的虚拟分类
	for i in range(count):#默认从0开始
		category=Category(name=fake.word())
		db.session.add(category)
		try:
			db.session.commit()
		except IntegrityError:#当分类重复时会出错，抛出
		#sqlalchemy.exc.IntegrityError,此时需要进行回滚操作
			db.session.rollback()


#生成虚拟文章数据
from bluelog.models import Post
def fake_posts(count=50):#默认生成50篇文章
	for i in range(count):
		post=Post(
			title=fake.sentence(),
			body=fake.text(2000),
			#每一篇文章随机分类，使用get查询，主键值使用1-分类数量的随机值
			category=Category.query.get(random.randint(1,Category.query.count())),
			timestamp=fake.date_time_this_year()
		)
		db.session.add(post)
	db.session.commit()

#生成虚拟评论

from bluelog.models import Comment

def fake_comments(count=500):#默认生成500条评论
	for i in range(count):
		comment=Comment(
			author=fake.name(),
			email=fake.email(),
			site=fake.url(),
			body=fake.sentence(),
			timestamp=fake.date_time_this_year(),
			reviewed=True,
			post=Post.query.get(random.randint(1,Post.query.count()))
		)
		db.session.add(comment)
	salt=int(count*0.1)#另外再添加50条未审核评论、50条管理员评论、50条回复
	for i in range(salt):
		#未审核评论
		comment=Comment(
			author=fake.name(),
			email=fake.email(),
			site=fake.url(),
			body=fake.sentence(),
			timestamp=fake.date_time_this_year(),
			reviewed=False,
			post=Post.query.get(random.randint(1,Post.query.count()))
		)
		db.session.add(comment)
		#管理员发表的评论
		comment=Comment(
			author='Mima Kirigoe',
			email='mima@example.com',
			site='example.com',
			body=fake.sentence(),
			timestamp=fake.date_time_this_year(),
			from_admin=True,
			post=Post.query.get(random.randint(1,Post.query.count()))
		)
		db.session.add(comment)
	db.session.commit()
	#回复
	for i in range(salt):
		comment=Comment(
			author=fake.name(),
			email=fake.email(),
			site=fake.url(),
			body=fake.sentence(),
			timestamp=fake.date_time_this_year(),
			reviewed=True,
			#回复就从评论内挑就行
			replied=Comment.query.get(random.randint(1,Commen.query.count())),
			post=Post.query.get(random.randint(1,Post.query.count()))
		)
		db.session.add(comment)
	db.session.commit()


#创建生成虚拟数据的命令
#使用一个commands.py里的forge函数来整合
