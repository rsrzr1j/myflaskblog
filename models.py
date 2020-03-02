

#创建管理员模型，存储管理员设置相关的信息
from bluelog.extensions iport db
class Admin(db.Model):
	id=db.Column(db.Integer,primary_key=True)#主键
	username=db.Column(db.String(20))
	password_hash=db.Column(db.String(128))#密码hash
	blog_title=db.Column(db.String(60))
	bolog_sub_title=db.Column(db.String(100))
	name=db.Column(db.String(30))#用户姓名
	about=db.Column(db.Text)


#创建存储文章分类的数据库模型
class Category(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(30),unique=True)#分类的名称不允许重复
	posts=db.relationship('Post',back_populates='category')#创建集合关系属性


#创建存文章的Post模型
from datetime import datetime

class Post(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	title=db.Column(db.String(60))#文章标题
	body=db.Column(db.Text)#内容
	timestamp=db.Column(db.DateTime,default=datetime.utcnow)#时间戳
	category_id=db.Column(db.Integer,db.ForeignKey('category.id')) #此id是外键，
	#作为执行分类模型的外键，存储分类记录的主键值，因为分类与文章存在一对多的关系
	category=db.relationship('Category',back_populates='posts')
	#创建文章-分类关系标量的属性
	comments=db.relationship('Comment',backref='post',cascade='all')
	#文章和评论也是一对多的关系，并创建了级联删除，删除文章也将对应的评论全部删除

#创建评论模型
#用于存储评论，文章和评论也是一对多的关系
class Comment(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	author=db.Column(db.String(30))
	email=db.Column(db.String(254))
	site=db.Column(db.String(255))
	body=db.Column(db.Text)
	from_admin=db.Column(db.Boolean,default=False)#判断是否是管理员的评论
	reviewd=db.Column(db.Boolean,default=False)#判断是否通过审核，防止垃圾评论和不当评论
	timestamp=db.Column(db.DateTime,default=datetime.utcnow,index=True)
	post_id=db.Column(db.Integer,db.ForeignKey('post.id'))
	#创建外键，存储Post记录的主键
	post=db.relationship('Post',back_populates='comments')
	#创建评论-文章关系标量的属性
	
	#下面将创建邻接表关系（在sqlalchemy中这样称呼）实现父评论-子评论的一对多关系
	replied_id=db.Column(db.Integer,db.ForeignKey('comment.id'))
	#在评论内设置一个外键指向自身的id,本地侧，多这一侧需要设置外键
	replied=db.relationship('Comment',back_populates='replies',remote_side=[id])
	#远程侧，通过remote_side将id字段定义为这个关系的远程侧
	replies=db.relationship('Comment',back_populates='replied',cascade='all')
	#评论的级联关系，在少这一侧设置级联关系可达到删除一个父评论子评论也一并删除的效果


