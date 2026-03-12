# 💰 Personal Finance Management System

## Local Development
```bash
# 1. Import database
mysql -u root -p < database/schema.sql

# 2. Set env vars
cp backend/.env.example backend/.env
# Edit backend/.env with your MySQL password

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
python backend/app.py
# Open http://localhost:5000  |  Password: admin123
```

## Railway Deployment
1. Push this repo to GitHub
2. Connect repo to Railway
3. Add MySQL plugin on Railway canvas
4. Set Variables in Railway (web service → Variables tab):
   ```
   DB_HOST=${{MySQL.MYSQLHOST}}
   DB_PORT=${{MySQL.MYSQLPORT}}
   DB_USER=${{MySQL.MYSQLUSER}}
   DB_PASSWORD=${{MySQL.MYSQLPASSWORD}}
   DB_NAME=${{MySQL.MYSQLDATABASE}}
   SECRET_KEY=any_long_random_string_here
   DEBUG=False
   ```
5. Railway auto-deploys using Procfile
6. Import schema: MySQL service → Data → Query → paste schema.sql → Run

## Default Login Password
`admin123`
