import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
                                        'mysql+pymysql://root:Heartattack1801!@localhost/nft_vc_platform')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
