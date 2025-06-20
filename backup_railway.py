import os
import pymysql
from datetime import datetime

# REPLACE THESE WITH YOUR RAILWAY MYSQL CREDENTIALS
MYSQL_HOST = "mysql.railway.internal"  # e.g., "containers-us-west-123.railway.app"
MYSQL_PORT = 3306  # Replace with your actual port (e.g., 7815)
MYSQL_USER = "root"
MYSQL_PASSWORD = "nzJFHHPkIxVCsHbCGsXehvmCfSbwJTdb"  # Replace with your actual password
MYSQL_DATABASE = "railway"

def create_backup():
    """Create a SQL backup of the Railway MySQL database"""
    
    backup_filename = f"railway_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
    
    try:
        # Connect to the database
        print(f"Connecting to MySQL at {MYSQL_HOST}:{MYSQL_PORT}...")
        connection = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        print("Connected successfully!")
        
        with open(backup_filename, 'w', encoding='utf8') as backup_file:
            # Write header
            backup_file.write(f"-- Railway MySQL Backup\n")
            backup_file.write(f"-- Generated on: {datetime.now()}\n")
            backup_file.write(f"-- Database: {MYSQL_DATABASE}\n\n")
            
            backup_file.write("SET FOREIGN_KEY_CHECKS=0;\n")
            backup_file.write("SET SQL_MODE='NO_AUTO_VALUE_ON_ZERO';\n\n")
            
            with connection.cursor() as cursor:
                # Get all tables
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                
                print(f"Found {len(tables)} tables to backup...")
                
                for table_dict in tables:
                    table_name = list(table_dict.values())[0]
                    print(f"Backing up table: {table_name}")
                    
                    # Get table structure
                    cursor.execute(f"SHOW CREATE TABLE `{table_name}`")
                    create_table = cursor.fetchone()
                    create_statement = list(create_table.values())[1]
                    
                    # Write DROP and CREATE statements
                    backup_file.write(f"\n-- Table structure for table `{table_name}`\n")
                    backup_file.write(f"DROP TABLE IF EXISTS `{table_name}`;\n")
                    backup_file.write(f"{create_statement};\n\n")
                    
                    # Get table data
                    cursor.execute(f"SELECT * FROM `{table_name}`")
                    rows = cursor.fetchall()
                    
                    if rows:
                        backup_file.write(f"-- Dumping data for table `{table_name}`\n")
                        
                        # Get column names
                        columns = list(rows[0].keys())
                        columns_str = ', '.join([f"`{col}`" for col in columns])
                        
                        # Write INSERT statements
                        for row in rows:
                            values = []
                            for col in columns:
                                value = row[col]
                                if value is None:
                                    values.append('NULL')
                                elif isinstance(value, (int, float)):
                                    values.append(str(value))
                                elif isinstance(value, bytes):
                                    # Handle binary data
                                    values.append("0x" + value.hex())
                                else:
                                    # Escape single quotes and backslashes
                                    value = str(value).replace('\\', '\\\\').replace("'", "\\'")
                                    values.append(f"'{value}'")
                            
                            values_str = ', '.join(values)
                            backup_file.write(f"INSERT INTO `{table_name}` ({columns_str}) VALUES ({values_str});\n")
                        
                        backup_file.write("\n")
                
                # Count records for summary
                cursor.execute("SELECT COUNT(*) as count FROM users")
                users_count = cursor.fetchone()['count']
                
                print(f"\n✅ Backup completed successfully!")
                print(f"📁 File: {backup_filename}")
                print(f"👥 Users backed up: {users_count}")
            
            backup_file.write("\nSET FOREIGN_KEY_CHECKS=1;\n")
        
        connection.close()
        
        # Check file size
        file_size = os.path.getsize(backup_filename) / 1024  # KB
        print(f"📊 Backup size: {file_size:.2f} KB")
        
        return backup_filename
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Check your MySQL credentials")
        print("2. Make sure your Railway MySQL is accessible")
        print("3. Check if your IP is allowed in Railway settings")
        return None

if __name__ == "__main__":
    print("🚀 Starting Railway MySQL Backup...\n")
    
    # Show current settings (without password)
    print(f"Host: {MYSQL_HOST}")
    print(f"Port: {MYSQL_PORT}")
    print(f"User: {MYSQL_USER}")
    print(f"Database: {MYSQL_DATABASE}")
    print("-" * 50)
    
    backup_file = create_backup()
    
    if backup_file:
        print(f"\n✨ Next steps:")
        print(f"1. Check the backup file: {backup_file}")
        print(f"2. Keep this file safe for importing to PythonAnywhere")
        print(f"3. You can open it in a text editor to verify the SQL content")