import os
from app.app import create_app

# config_name = os.getenv('APP_SETTING')
app = create_app('development')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)