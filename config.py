import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN', '7772858381:AAH2HVRp6b6udR4xzBjg33_VorLhqpqDMxs')
BOT_USERNAME = os.getenv('BOT_USERNAME', 'ProjectsDetailsBot')
BOT_NAME = os.getenv('BOT_NAME', 'مشاريع الشركة')

# Database Configuration
DATABASE_FILE = os.getenv('DATABASE_FILE', 'projects_new.json')

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Bot Settings
TRIGGER_WORDS = ['ديموز', 'demos', 'مشاريع', 'projects']
MAX_PROJECTS_PER_MESSAGE = 3
MESSAGE_DELAY = 0.5  # seconds between messages

# Group Protection Settings
GROUP_MESSAGE_TIMEOUT = 600  # 10 minutes
PROCESSING_TIMEOUT = 2  # 2 seconds 