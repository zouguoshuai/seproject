type = "mysql+pymysql"
username = "root"
password = "zgs200301"
ipaddrsss = "localhost"
port = 3306
schema = "seproject"

SQLALCHEMY_DATABASE_URL = f"{type}://{username}:{password}@{ipaddrsss}:{port}/{schema}"

wxurl = "https://api.weixin.qq.com/sns/jscode2session"
wxappid = "wx9920876e73d730f6"
wxsecret = "a38821e8573155e56e61bc3da32a0e94"

# 在终端中通过uvicorn启动
# python -m uvicorn main:app --reload --host 192.168.231.150