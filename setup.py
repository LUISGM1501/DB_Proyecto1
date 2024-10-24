from setuptools import setup, find_packages

setup(
    name="redsocial",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask==2.2.3',
        'Werkzeug==2.2.3',
        'psycopg2-binary==2.9.5',
        'pymongo==4.3.3',
        'redis==4.5.1',
        'python-dotenv==1.0.0',
        'flask-jwt-extended==4.4.4',
        'pytest==7.2.2',
        'pytest-cov==4.0.0',
        'pytz==2024.1',
        'mongomock==4.1.2',
        'fakeredis==2.20.0',
    ],
)