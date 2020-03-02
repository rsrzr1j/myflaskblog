
#创建生成虚拟数据的命令
#使用一个commands.py里的forge函数来整合

import click

def register_commands(app):

	@app.cli.command()
	#通过click添加option装饰器，方便自定义数据
	@click.option('--category',default=10,help='Quantity of categories,default is 10.')

	@click.option('--post',default=50,help='Quantity of posts,defaultis 50.')
	@click.option('--comment',default=500,help='Quantity of comments,default is 500')
	def forge(category,post,comment):
		'''Generates the fake categories ,posts,and comments.'''
		form buleblog.fakes imort fake_admin,fake_categories,fake_posts,fake_comments
		db.drop_all()
		db.create_all()
		#注意虚拟数据生成的顺序，管理员-分类-文章-评论
		click.echo('Generating the administrator...')
		fake_admin()
		click.echo('Generating %d categories...'% category)
		fake_categories(category)
		click.echo('Generating %d posts...' % post)
		fake_posts(post)
		click.echo('Generating %d comments...'% comment)
		fake_comments(comment)
		click.echo('Done.')
	#之后在终端使用flask forge就能生成数据