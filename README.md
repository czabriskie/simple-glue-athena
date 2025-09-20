# AWS Athena Query Project

This project contains a Python script for querying flight data using AWS Athena. The script demonstrates how to execute SQL queries against cloud-stored data and export results.

## 📁 Project Structure

```
.
├── simple_athena_query.py       # Athena query script with examples
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🚀 Features

### AWS Athena Integration
- **Execute SQL queries** against cloud-stored data
- **Built-in query examples** for data analysis
- **Automatic result handling** with pandas DataFrames
- **CSV export** functionality for results

## 📋 Prerequisites

### Software Requirements
- Python 3.7+
- AWS CLI configured with appropriate credentials
- Virtual environment (recommended)

### AWS Requirements
- AWS Account with Athena access
- S3 bucket for query results storage
- IAM permissions for:
  - Amazon Athena (query execution)
  - Amazon S3 (read/write access)

### Python Dependencies
```bash
# Install using uv (recommended)
uv pip install -r requirements.txt

# Or using pip
pip install -r requirements.txt

# Or install individually
pip install pandas pyarrow boto3
```

## 🛠️ Setup

### 1. Configure AWS Credentials
```bash
aws configure
```
Enter your:
- AWS Access Key ID
- AWS Secret Access Key
- Default region
- Default output format

### 2. Update Configuration
Edit the configuration variables in the Python scripts:

**For Athena queries** (`simple_athena_query.py`):
```python
DATABASE = "your_database_name"              # Your Athena database
S3_BUCKET = "s3://your-bucket/results/"      # Your S3 bucket for results
REGION = "us-west-2"                         # Your AWS region
```

### 3. Verify Setup
```bash
# Test AWS connectivity
aws sts get-caller-identity

# Test S3 access
aws s3 ls s3://your-bucket/
```

## 📊 Usage

### Querying with Athena

Run the Athena query script to execute predefined queries:

```bash
# Run Athena queries
/path/to/.venv/bin/python simple_athena_query.py
```

**Built-in queries:**
1. **Table Schema** - `DESCRIBE flights`
2. **Sample Data** - `SELECT * FROM flights LIMIT 5`
3. **Row Count** - `SELECT COUNT(*) FROM flights`
4. **Flight Statistics** - Daily aggregated flight data with delays

## 📈 Sample Queries

### Basic Data Exploration
```sql
-- Get table structure
DESCRIBE flights;

-- Sample records
SELECT * FROM flights LIMIT 10;

-- Total record count
SELECT COUNT(*) as total_flights FROM flights;
```

### Flight Analysis
```sql
-- Daily flight statistics
SELECT 
    fl_date, 
    COUNT(*) as flight_count,
    AVG(dep_delay) as avg_departure_delay,
    AVG(arr_delay) as avg_arrival_delay
FROM flights 
GROUP BY fl_date 
ORDER BY fl_date;

-- Delayed flights analysis
SELECT 
    COUNT(*) as total_flights,
    SUM(CASE WHEN dep_delay > 15 THEN 1 ELSE 0 END) as delayed_flights,
    AVG(dep_delay) as avg_delay
FROM flights;

-- Distance vs. Air Time correlation
SELECT 
    distance,
    AVG(air_time) as avg_air_time,
    COUNT(*) as flight_count
FROM flights 
GROUP BY distance
ORDER BY distance;
```

## 📝 Data Schema

The flights table contains the following columns:

| Column | Type | Description |
|--------|------|-------------|
| `fl_date` | date | Flight date |
| `dep_delay` | smallint | Departure delay in minutes |
| `arr_delay` | smallint | Arrival delay in minutes |
| `air_time` | smallint | Flight duration in minutes |
| `distance` | smallint | Flight distance in miles |
| `dep_time` | float | Departure time (decimal hours) |
| `arr_time` | float | Arrival time (decimal hours) |

## 🔧 Troubleshooting

### Common Issues

#### Python Syntax Errors
**Problem**: `SyntaxError: invalid syntax` with f-strings
**Solution**: Use the virtual environment Python that supports Python 3.6+
```bash
# Instead of 'python script.py', use:
/path/to/.venv/bin/python script.py
```

#### AWS Authentication Errors
**Problem**: `NoCredentialsError` or `AccessDenied`
**Solution**: 
1. Run `aws configure` to set up credentials
2. Verify IAM permissions for Athena and S3
3. Check AWS region configuration

#### Athena Query Failures
**Problem**: `COLUMN_NOT_FOUND` errors
**Solution**: 
1. Run `DESCRIBE table_name` to see available columns
2. Verify table exists in the specified database
3. Check column name spelling and case sensitivity

#### Large File Processing
**Problem**: Memory errors when processing large files
**Solution**:
1. Use chunked processing for very large files
2. Increase available system memory
3. Consider splitting into smaller batches

## 📚 Additional Resources

- [AWS Athena Documentation](https://docs.aws.amazon.com/athena/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [PyArrow Documentation](https://arrow.apache.org/docs/python/)
- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚡ Quick Start

```bash
# 1. Clone and setup
git clone <repository-url>
cd glue_parquet

# 2. Install dependencies
uv pip install -r requirements.txt
# or: pip install -r requirements.txt

# 3. Configure AWS
aws configure

# 4. Update script configuration
# Edit DATABASE and S3_BUCKET in simple_athena_query.py

# 5. Run Athena queries
/path/to/.venv/bin/python simple_athena_query.py
```

---

**Note**: This project was designed for educational purposes in cloud computing coursework. Ensure you have proper AWS cost controls in place when running queries against large datasets.
