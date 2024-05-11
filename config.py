import os

class Config:
    DEBUG = False
    DEVELOPMENT = False
    NEO_URI = os.environ.get('NeoURI_Remote', '')
    NEO_PWD = os.environ.get('NeoPwd_Remote', '')
    IMAGE_DIR = 'static/images/'
    GENERAL_IMAGES_DIR = IMAGE_DIR + 'general/'
    FRANCHISE_IMAGE_DIR = IMAGE_DIR + 'franchise_logos/'
    TEAM_IMAGE_DIR = IMAGE_DIR + 'team_logos/'
    PLAYER_IMAGE_DIR = IMAGE_DIR + 'player_images/'
    BBALL_REFERENCE_URL = 'https://www.baseball-reference.com/players/@@alpha@@/@@playerID@@.shtml'

class ProductionConfig(Config):
    pass

class StagingConfig(Config):
    DEBUG = True

class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True