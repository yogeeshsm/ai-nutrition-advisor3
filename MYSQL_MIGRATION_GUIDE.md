# SQLite to MySQL Migration Guide

This guide will help you migrate your AI Nutrition Advisor database from SQLite to MySQL.

## Prerequisites

### 1. Install MySQL Server

**Windows:**
- Download MySQL Community Server from: https://dev.mysql.com/downloads/mysql/
- Run the installer and follow the setup wizard
- Set a root password (remember this!)
- Default port: 3306

**Alternative - Using XAMPP:**
- Download XAMPP from: https://www.apachefriends.org/
- Install and start MySQL from XAMPP Control Panel
- Default user: `root`, password: (empty)

### 2. Verify MySQL Installation

Open Command Prompt and run:
```bash
mysql --version
```

You should see output like: `mysql Ver 8.0.x`

## Migration Steps

### Step 1: Configure MySQL Connection

Edit `db_config.py` and update the MySQL configuration:

```python
MYSQL_CONFIG = {
    'host': 'localhost',        # Your MySQL host
    'port': 3306,               # Your MySQL port
    'user': 'root',             # Your MySQL username
    'password': 'your_password', # Your MySQL password
    'database': 'nutrition_advisor',
    'charset': 'utf8mb4',
    'use_unicode': True,
    'autocommit': False
}
```

### Step 2: Create MySQL User (Optional but Recommended)

For security, create a dedicated user instead of using root:

```sql
-- Connect to MySQL as root
mysql -u root -p

-- Create database and user
CREATE DATABASE nutrition_advisor CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'nutrition_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON nutrition_advisor.* TO 'nutrition_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

Then update `db_config.py`:
```python
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'nutrition_user',
    'password': 'secure_password',
    'database': 'nutrition_advisor',
    ...
}
```

### Step 3: Backup SQLite Database

**IMPORTANT:** Always backup before migration!

```bash
# Create backup folder
mkdir backups

# Copy SQLite database
copy nutrition_advisor.db backups\nutrition_advisor_backup_%date:~-4,4%%date:~-7,2%%date:~-10,2%.db
```

### Step 4: Run Migration Script

Activate your virtual environment and run:

```bash
# Activate virtual environment
.venv\Scripts\Activate.ps1

# Install MySQL connector (already done)
pip install mysql-connector-python

# Run migration
python migrate_to_mysql.py
```

The script will:
1. Create MySQL database
2. Create all tables
3. Migrate all data from SQLite
4. Verify row counts

### Step 5: Switch Application to MySQL

Set environment variable to use MySQL:

**Option A - Temporary (current session):**
```powershell
$env:DB_TYPE='mysql'
python start_server.py
```

**Option B - Permanent (recommended):**

Create/update `.env` file:
```
DB_TYPE=mysql
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=nutrition_user
MYSQL_PASSWORD=secure_password
MYSQL_DATABASE=nutrition_advisor
```

Then install python-dotenv:
```bash
pip install python-dotenv
```

Update `db_config.py` to load from .env:
```python
from dotenv import load_dotenv
load_dotenv()

DB_TYPE = os.environ.get('DB_TYPE', 'sqlite')
```

### Step 6: Test MySQL Connection

```bash
python -c "from database import get_connection; conn = get_connection(); print('✓ MySQL connected!'); conn.close()"
```

### Step 7: Verify Application

```bash
# Start server
python start_server.py

# Test in browser
# Visit: http://127.0.0.1:5000
```

## Rollback to SQLite

If you need to switch back to SQLite:

**Temporary:**
```powershell
$env:DB_TYPE='sqlite'
python start_server.py
```

**Permanent:**
Update `.env`:
```
DB_TYPE=sqlite
```

## Performance Comparison

### SQLite Advantages:
- No server setup required
- Single file database
- Perfect for development
- Lower overhead

### MySQL Advantages:
- Better concurrent access
- Scales to larger datasets
- Network access (remote connections)
- Better for production deployment
- Advanced features (replication, clustering)

## Troubleshooting

### Error: "Access denied for user"
- Check username/password in `db_config.py`
- Verify user has permissions: `SHOW GRANTS FOR 'nutrition_user'@'localhost';`

### Error: "Can't connect to MySQL server"
- Ensure MySQL service is running
- Check port 3306 is not blocked by firewall
- Verify host address (use `127.0.0.1` instead of `localhost` if needed)

### Error: "Unknown database"
- The migration script creates it automatically
- Or manually: `CREATE DATABASE nutrition_advisor;`

### Data mismatch after migration
- Re-run verification: `python migrate_to_mysql.py` (choose verify only)
- Check for special characters in text fields
- Ensure charset is utf8mb4

## MySQL Management Tools

### Command Line:
```bash
# Connect to MySQL
mysql -u nutrition_user -p nutrition_advisor

# Show tables
SHOW TABLES;

# Count rows
SELECT COUNT(*) FROM children;

# View data
SELECT * FROM children LIMIT 10;
```

### GUI Tools:
- **MySQL Workbench** (Official): https://dev.mysql.com/downloads/workbench/
- **phpMyAdmin** (Web-based): Included with XAMPP
- **DBeaver** (Multi-database): https://dbeaver.io/

## Environment Variables Reference

```bash
# Database configuration
DB_TYPE=mysql                    # 'sqlite' or 'mysql'

# MySQL specific
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=nutrition_user
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=nutrition_advisor
```

## Production Deployment Tips

1. **Use connection pooling** for better performance
2. **Enable SSL** for secure connections
3. **Regular backups** with mysqldump:
   ```bash
   mysqldump -u nutrition_user -p nutrition_advisor > backup.sql
   ```
4. **Monitor performance** with MySQL slow query log
5. **Optimize tables** regularly: `OPTIMIZE TABLE table_name;`

## Need Help?

- MySQL Documentation: https://dev.mysql.com/doc/
- Check application logs for detailed error messages
- Verify both SQLite and MySQL have same data structure
