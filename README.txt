根目录
config.yaml && index.wsgi && index.wsgic 为SAE服务器配置文件；
manage.py 为django配置文件；

static 静态文件
admin文件夹中为django自带的管理员页面的相关文件；
ranking文件夹中排行榜页面的相关文件；

wechat 项目
setting.py 为项目配置文件，其中包括数据库设置、管理员页面开启设置等；
urls.py 中指定了url和view间的对应关系；

weixininterface 应用
creatmenu.py 文件用来设置公众号菜单；
game_handler.py 文件处理猜数字和点歌台部分的逻辑；
question_handler.py 文件处理答题逻辑；
views.py 文件进行微信消息的分发和回复，以及排行榜页面的后端逻辑；
models.py 文件进行数据库设置；