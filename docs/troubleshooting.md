# 🛠️ CivicMind AI Troubleshooting Guide

Comprehensive troubleshooting guide for common issues, debugging techniques, and system maintenance.

## 📋 Quick Reference

- [🚨 Common Issues](#-common-issues)
- [🔧 Installation Problems](#-installation-problems)
- [⚙️ Configuration Issues](#️-configuration-issues)
- [🤖 Agent Problems](#-agent-problems)
- [🗄️ Database Issues](#️-database-issues)
- [🌐 API and Integration Problems](#-api-and-integration-problems)
- [🐳 Docker and Deployment Issues](#-docker-and-deployment-issues)
- [📊 Performance Troubleshooting](#-performance-troubleshooting)
- [🔒 Security Issues](#-security-issues)
- [📝 Logging and Debugging](#-logging-and-debugging)

---

## 🚨 **Common Issues**

### **Problem: "Module not found" errors**

```bash
ModuleNotFoundError: No module named 'civicmind'
```

**Solutions:**
1. **Check virtual environment**
   ```bash
   # Ensure virtual environment is activated
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   
   # Verify Python path
   python -c "import sys; print(sys.path)"
   ```

2. **Reinstall dependencies**
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```

3. **Check PYTHONPATH**
   ```bash
   export PYTHONPATH="${PYTHONPATH}:/path/to/civicmind-ai"
   ```

### **Problem: OpenAI API errors**

```bash
AuthenticationError: Incorrect API key provided
```

**Solutions:**
1. **Verify API key**
   ```bash
   # Check if API key is set
   echo $OPENAI_API_KEY
   
   # Test API key directly
   curl https://api.openai.com/v1/models \
     -H "Authorization: Bearer $OPENAI_API_KEY"
   ```

2. **Check billing and usage**
   - Visit [OpenAI Platform](https://platform.openai.com/usage)
   - Ensure you have available credits
   - Check rate limits

3. **Update API key format**
   ```bash
   # New format starts with sk-proj-
   export OPENAI_API_KEY="sk-proj-your-new-api-key"
   ```

### **Problem: Server won't start**

```bash
ERROR: Address already in use
```

**Solutions:**
1. **Check port usage**
   ```bash
   # Find what's using port 8000
   lsof -i :8000        # Linux/Mac
   netstat -ano | findstr :8000  # Windows
   ```

2. **Kill existing processes**
   ```bash
   # Kill process using port
   kill -9 $(lsof -t -i:8000)  # Linux/Mac
   taskkill /PID <PID> /F       # Windows
   ```

3. **Use different port**
   ```bash
   export CIVICMIND_PORT=8001
   python server.py
   ```

---

## 🔧 **Installation Problems**

### **Python Version Issues**

**Problem:** Python version too old
```bash
ERROR: Python 3.11 or higher is required
```

**Solutions:**
1. **Install Python 3.11+**
   ```bash
   # Using pyenv (recommended)
   pyenv install 3.11.7
   pyenv local 3.11.7
   
   # Or download from python.org
   # https://www.python.org/downloads/
   ```

2. **Update virtual environment**
   ```bash
   # Remove old venv
   rm -rf venv
   
   # Create new with correct Python
   python3.11 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### **Dependency Conflicts**

**Problem:** Package version conflicts
```bash
ERROR: Could not find a version that satisfies the requirement
```

**Solutions:**
1. **Clean install**
   ```bash
   # Remove existing packages
   pip freeze | xargs pip uninstall -y
   
   # Fresh install
   pip install -r requirements.txt
   ```

2. **Use conda environment**
   ```bash
   conda create -n civicmind python=3.11
   conda activate civicmind
   pip install -r requirements.txt
   ```

3. **Check for platform-specific packages**
   ```bash
   # For Mac M1/M2
   pip install --no-binary=:all: package_name
   
   # For specific architecture
   pip install --only-binary=all package_name
   ```

### **Permissions Issues**

**Problem:** Permission denied during installation
```bash
PermissionError: [Errno 13] Permission denied
```

**Solutions:**
1. **Use virtual environment (preferred)**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Use user installation**
   ```bash
   pip install --user -r requirements.txt
   ```

3. **Fix permissions (Linux/Mac)**
   ```bash
   sudo chown -R $USER:$USER /path/to/civicmind-ai
   chmod -R 755 /path/to/civicmind-ai
   ```

---

## ⚙️ **Configuration Issues**

### **Environment Variables**

**Problem:** Configuration not loading
```bash
KeyError: 'OPENAI_API_KEY'
```

**Debug steps:**
1. **Check .env file**
   ```bash
   # Verify .env exists and has correct format
   cat .env
   
   # Check for common issues:
   # - No spaces around = sign
   # - No quotes unless needed
   # - No trailing spaces
   ```

2. **Load environment manually**
   ```bash
   # Test loading
   python -c "
   from dotenv import load_dotenv
   import os
   load_dotenv()
   print(os.getenv('OPENAI_API_KEY'))
   "
   ```

3. **Set environment variables directly**
   ```bash
   export OPENAI_API_KEY="your-api-key"
   export DATABASE_URL="postgresql://user:pass@localhost/db"
   python server.py
   ```

### **Database Configuration**

**Problem:** Database connection fails
```bash
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solutions:**
1. **Check database service**
   ```bash
   # PostgreSQL status
   sudo systemctl status postgresql  # Linux
   brew services list | grep postgres  # Mac
   
   # Start if needed
   sudo systemctl start postgresql
   brew services start postgresql
   ```

2. **Verify connection details**
   ```bash
   # Test connection
   psql -h localhost -U civicmind -d civicmind
   
   # Check if database exists
   psql -l
   ```

3. **Create database if missing**
   ```sql
   CREATE DATABASE civicmind;
   CREATE USER civicmind WITH PASSWORD 'password';
   GRANT ALL PRIVILEGES ON DATABASE civicmind TO civicmind;
   ```

### **Vector Store Issues**

**Problem:** ChromaDB initialization fails
```bash
ValueError: Could not load vector store
```

**Solutions:**
1. **Create data directory**
   ```bash
   mkdir -p data/vectorstore
   chmod 755 data/vectorstore
   ```

2. **Reset vector store**
   ```bash
   # Remove and recreate
   rm -rf data/vectorstore
   python -c "
   from civicmind.core.civic_orchestrator import CivicOrchestrator
   CivicOrchestrator.initialize_vector_store()
   "
   ```

3. **Check permissions**
   ```bash
   ls -la data/
   # Ensure civicmind user can read/write
   ```

---

## 🤖 **Agent Problems**

### **Agent Not Responding**

**Problem:** Agent returns empty or error responses
```bash
AgentException: Agent failed to process request
```

**Debug steps:**
1. **Test individual agent**
   ```python
   from civicmind.agents.parking_agent import ParkingAgent
   from langchain_openai import ChatOpenAI
   
   llm = ChatOpenAI(api_key="your-key")
   agent = ParkingAgent(llm)
   
   response = agent.analyze_issue(
       "Test parking issue",
       "Test City, CA",
       {}
   )
   print(response)
   ```

2. **Check system prompt**
   ```python
   agent = ParkingAgent(llm)
   print(agent.get_system_prompt())
   # Verify prompt is loaded correctly
   ```

3. **Verify LLM connection**
   ```python
   from langchain_openai import ChatOpenAI
   
   llm = ChatOpenAI(api_key="your-key")
   response = llm.invoke([{"role": "user", "content": "Hello"}])
   print(response.content)
   ```

### **Agent Registration Issues**

**Problem:** Agent not found in factory
```bash
KeyError: 'parking' agent not found
```

**Solutions:**
1. **Check agent registration**
   ```python
   from civicmind.core.agent_factory import AgentFactory
   
   factory = AgentFactory("api-key")
   print(factory.list_agents())
   ```

2. **Manual registration**
   ```python
   from civicmind.agents.parking_agent import ParkingAgent
   
   factory.register_agent("parking", ParkingAgent)
   ```

3. **Check imports**
   ```python
   # Verify agent can be imported
   try:
       from civicmind.agents.parking_agent import ParkingAgent
       print("Import successful")
   except ImportError as e:
       print(f"Import failed: {e}")
   ```

### **Prompt Engineering Issues**

**Problem:** Poor agent responses
```bash
Agent provides irrelevant or incorrect advice
```

**Solutions:**
1. **Review system prompt**
   ```python
   # Add more specific instructions
   def get_system_prompt(self):
       return """
       You are a parking specialist. ALWAYS:
       1. Suggest community-first solutions
       2. Provide specific contact information
       3. Include relevant municipal codes
       4. Respect cultural differences
       """
   ```

2. **Add examples in prompt**
   ```python
   prompt += """
   Example:
   Issue: "Neighbor blocks driveway"
   Response: "1. Talk to neighbor first..."
   """
   ```

3. **Test with different prompts**
   ```python
   # A/B test different prompt versions
   prompts = [prompt_v1, prompt_v2, prompt_v3]
   for i, prompt in enumerate(prompts):
       # Test and compare responses
   ```

---

## 🗄️ **Database Issues**

### **Migration Problems**

**Problem:** Database schema out of sync
```bash
sqlalchemy.exc.ProgrammingError: relation does not exist
```

**Solutions:**
1. **Run migrations**
   ```bash
   # If using Alembic
   alembic upgrade head
   
   # Or recreate tables
   python -c "
   from civicmind.core.database import create_tables
   create_tables()
   "
   ```

2. **Reset database**
   ```sql
   -- Backup first!
   pg_dump civicmind > backup.sql
   
   -- Drop and recreate
   DROP DATABASE civicmind;
   CREATE DATABASE civicmind;
   ```

3. **Check table structure**
   ```sql
   -- List tables
   \dt
   
   -- Describe table
   \d table_name
   ```

### **Performance Issues**

**Problem:** Slow database queries
```bash
Query takes >5 seconds to complete
```

**Solutions:**
1. **Add indexes**
   ```sql
   -- Common indexes for CivicMind
   CREATE INDEX idx_issues_location ON issues(location);
   CREATE INDEX idx_issues_created_at ON issues(created_at);
   CREATE INDEX idx_issues_status ON issues(status);
   ```

2. **Analyze query performance**
   ```sql
   EXPLAIN ANALYZE SELECT * FROM issues WHERE location = 'Sacramento, CA';
   ```

3. **Database maintenance**
   ```sql
   -- Update statistics
   ANALYZE;
   
   -- Clean up
   VACUUM;
   
   -- Reindex
   REINDEX DATABASE civicmind;
   ```

### **Connection Pool Issues**

**Problem:** Database connection exhausted
```bash
sqlalchemy.exc.TimeoutError: QueuePool limit exceeded
```

**Solutions:**
1. **Increase pool size**
   ```python
   engine = create_engine(
       DATABASE_URL,
       pool_size=20,
       max_overflow=30,
       pool_timeout=30
   )
   ```

2. **Check for connection leaks**
   ```python
   # Always close connections
   with engine.begin() as conn:
       result = conn.execute(query)
   # Connection automatically closed
   ```

3. **Monitor connections**
   ```sql
   -- Check active connections
   SELECT count(*) FROM pg_stat_activity WHERE datname = 'civicmind';
   ```

---

## 🌐 **API and Integration Problems**

### **External API Failures**

**Problem:** Third-party API not responding
```bash
requests.exceptions.ConnectionError: Failed to establish connection
```

**Solutions:**
1. **Implement retry logic**
   ```python
   import time
   from requests.adapters import HTTPAdapter
   from urllib3.util.retry import Retry
   
   session = requests.Session()
   retry_strategy = Retry(
       total=3,
       backoff_factor=1,
       status_forcelist=[429, 500, 502, 503, 504]
   )
   adapter = HTTPAdapter(max_retries=retry_strategy)
   session.mount("http://", adapter)
   session.mount("https://", adapter)
   ```

2. **Add circuit breaker**
   ```python
   from pybreaker import CircuitBreaker
   
   api_breaker = CircuitBreaker(fail_max=5, reset_timeout=60)
   
   @api_breaker
   def call_external_api():
       return requests.get("https://api.example.com/data")
   ```

3. **Implement fallback data**
   ```python
   try:
       response = call_external_api()
   except Exception:
       # Use cached or default data
       response = get_fallback_data()
   ```

### **Rate Limiting Issues**

**Problem:** API rate limits exceeded
```bash
HTTPError: 429 Too Many Requests
```

**Solutions:**
1. **Implement rate limiting**
   ```python
   from ratelimit import limits, sleep_and_retry
   import time
   
   @sleep_and_retry
   @limits(calls=100, period=3600)  # 100 calls per hour
   def call_api():
       return requests.get("https://api.example.com/data")
   ```

2. **Use queue system**
   ```python
   import redis
   from celery import Celery
   
   app = Celery('civicmind', broker='redis://localhost:6379')
   
   @app.task
   def process_api_request(data):
       # Process API requests in background
       pass
   ```

3. **Cache responses**
   ```python
   import redis
   import json
   
   cache = redis.Redis(host='localhost', port=6379, db=0)
   
   def cached_api_call(url, cache_time=3600):
       cached = cache.get(url)
       if cached:
           return json.loads(cached)
       
       response = requests.get(url)
       cache.setex(url, cache_time, json.dumps(response.json()))
       return response.json()
   ```

---

## 🐳 **Docker and Deployment Issues**

### **Container Startup Problems**

**Problem:** Container exits immediately
```bash
docker: Error response from daemon: container exited with code 1
```

**Solutions:**
1. **Check container logs**
   ```bash
   docker logs container_name
   docker logs --follow container_name
   ```

2. **Debug interactively**
   ```bash
   # Start container with bash
   docker run -it civicmind-ai /bin/bash
   
   # Check what's failing
   python server.py
   ```

3. **Verify Dockerfile**
   ```dockerfile
   # Common issues:
   # - Missing WORKDIR
   # - Wrong COPY paths
   # - Missing dependencies
   # - Incorrect CMD/ENTRYPOINT
   ```

### **Docker Compose Issues**

**Problem:** Services can't communicate
```bash
django.db.utils.OperationalError: could not translate host name "postgres" to address
```

**Solutions:**
1. **Check network configuration**
   ```bash
   docker network ls
   docker network inspect civicmind-ai_default
   ```

2. **Verify service names**
   ```yaml
   # Use service names as hostnames
   DATABASE_URL=postgresql://user:pass@postgres:5432/db
   REDIS_URL=redis://redis:6379
   ```

3. **Check startup order**
   ```yaml
   services:
     civicmind-api:
       depends_on:
         - postgres
         - redis
       restart: unless-stopped
   ```

### **Volume and Persistence Issues**

**Problem:** Data not persisting between restarts
```bash
Data lost when container restarts
```

**Solutions:**
1. **Verify volume mounts**
   ```yaml
   volumes:
     - ./data:/app/data
     - postgres_data:/var/lib/postgresql/data
   ```

2. **Check permissions**
   ```bash
   # Host permissions
   sudo chown -R 1000:1000 ./data
   chmod -R 755 ./data
   ```

3. **Named volumes for persistence**
   ```yaml
   volumes:
     postgres_data:
     redis_data:
   ```

---

## 📊 **Performance Troubleshooting**

### **Slow Response Times**

**Problem:** API responses take >5 seconds
```bash
Request timeout after 30 seconds
```

**Solutions:**
1. **Profile the application**
   ```python
   import cProfile
   import pstats
   
   profiler = cProfile.Profile()
   profiler.enable()
   
   # Your code here
   
   profiler.disable()
   stats = pstats.Stats(profiler)
   stats.sort_stats('cumulative')
   stats.print_stats()
   ```

2. **Optimize database queries**
   ```python
   # Use eager loading
   query = session.query(Issue).options(
       joinedload(Issue.citizen),
       joinedload(Issue.responses)
   )
   
   # Add pagination
   issues = query.offset(skip).limit(limit).all()
   ```

3. **Implement caching**
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=1000)
   def get_agent_response(issue_type, description):
       # Expensive operation
       return agent.analyze_issue(description)
   ```

### **Memory Issues**

**Problem:** High memory usage or memory leaks
```bash
MemoryError: Unable to allocate array
```

**Solutions:**
1. **Monitor memory usage**
   ```python
   import psutil
   import os
   
   process = psutil.Process(os.getpid())
   print(f"Memory usage: {process.memory_info().rss / 1024 / 1024:.2f} MB")
   ```

2. **Optimize vector operations**
   ```python
   # Process in batches
   def process_large_dataset(data, batch_size=1000):
       for i in range(0, len(data), batch_size):
           batch = data[i:i+batch_size]
           yield process_batch(batch)
   ```

3. **Use generators for large datasets**
   ```python
   def get_issues():
       # Instead of loading all at once
       for issue in session.query(Issue).yield_per(100):
           yield issue
   ```

### **High CPU Usage**

**Problem:** CPU usage consistently >80%
```bash
System becomes unresponsive under load
```

**Solutions:**
1. **Use async operations**
   ```python
   import asyncio
   import aiohttp
   
   async def call_multiple_apis():
       async with aiohttp.ClientSession() as session:
           tasks = [
               session.get(url) for url in urls
           ]
           responses = await asyncio.gather(*tasks)
           return responses
   ```

2. **Implement background processing**
   ```python
   from celery import Celery
   
   app = Celery('civicmind')
   
   @app.task
   def heavy_computation(data):
       # Move CPU-intensive tasks to background
       return process_data(data)
   ```

3. **Optimize AI model calls**
   ```python
   # Batch similar requests
   def batch_analyze_issues(issues):
       grouped = group_by_type(issues)
       results = {}
       for issue_type, issue_list in grouped.items():
           # Process similar issues together
           results[issue_type] = agent.batch_analyze(issue_list)
       return results
   ```

---

## 🔒 **Security Issues**

### **Authentication Problems**

**Problem:** JWT token validation fails
```bash
jose.exceptions.JWTError: Invalid token
```

**Solutions:**
1. **Check token format**
   ```python
   import jwt
   
   try:
       payload = jwt.decode(token, secret_key, algorithms=["HS256"])
       print(payload)
   except jwt.InvalidTokenError as e:
       print(f"Token error: {e}")
   ```

2. **Verify secret key**
   ```python
   # Ensure same secret used for encoding/decoding
   import os
   secret = os.getenv("SECRET_KEY")
   if not secret or len(secret) < 32:
       raise ValueError("SECRET_KEY must be at least 32 characters")
   ```

3. **Check token expiration**
   ```python
   from datetime import datetime, timedelta
   
   # Set appropriate expiration
   exp = datetime.utcnow() + timedelta(hours=24)
   payload = {"exp": exp, "user_id": user_id}
   ```

### **API Security Issues**

**Problem:** Unauthorized access to endpoints
```bash
403 Forbidden: Insufficient permissions
```

**Solutions:**
1. **Implement proper authentication**
   ```python
   from fastapi import Depends, HTTPException, status
   from fastapi.security import HTTPBearer
   
   security = HTTPBearer()
   
   async def verify_token(token: str = Depends(security)):
       try:
           payload = jwt.decode(token.credentials, SECRET_KEY)
           return payload
       except jwt.InvalidTokenError:
           raise HTTPException(
               status_code=status.HTTP_401_UNAUTHORIZED,
               detail="Invalid token"
           )
   ```

2. **Add rate limiting**
   ```python
   from slowapi import Limiter, _rate_limit_exceeded_handler
   from slowapi.util import get_remote_address
   
   limiter = Limiter(key_func=get_remote_address)
   
   @app.get("/api/v1/issues")
   @limiter.limit("10/minute")
   async def get_issues(request: Request):
       return issues
   ```

3. **Input validation**
   ```python
   from pydantic import BaseModel, validator
   
   class IssueRequest(BaseModel):
       description: str
       location: str
       
       @validator('description')
       def validate_description(cls, v):
           if len(v) < 10:
               raise ValueError('Description too short')
           return v
   ```

---

## 📝 **Logging and Debugging**

### **Enable Debug Logging**

```python
# logging_config.py
import logging
import sys

def setup_debug_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('debug.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Set specific loggers
    logging.getLogger("civicmind").setLevel(logging.DEBUG)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
    logging.getLogger("httpx").setLevel(logging.DEBUG)
```

### **Debug Agent Interactions**

```python
import logging
from civicmind.agents.base_agent import BaseCivicAgent

class DebugAgent(BaseCivicAgent):
    def analyze_issue(self, description, location, context):
        logger = logging.getLogger(__name__)
        
        logger.debug(f"Input: {description}")
        logger.debug(f"Location: {location}")
        logger.debug(f"Context: {context}")
        
        try:
            response = super().analyze_issue(description, location, context)
            logger.debug(f"Response: {response}")
            return response
        except Exception as e:
            logger.error(f"Agent error: {e}", exc_info=True)
            raise
```

### **API Request Debugging**

```python
import logging
import requests

# Enable HTTP debugging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("requests.packages.urllib3").setLevel(logging.DEBUG)
logging.getLogger("httpx").setLevel(logging.DEBUG)

# Or use httpx with detailed logging
import httpx

async with httpx.AsyncClient() as client:
    response = await client.get("https://api.example.com")
    print(f"Status: {response.status_code}")
    print(f"Headers: {response.headers}")
    print(f"Content: {response.text}")
```

### **Performance Debugging**

```python
import time
from functools import wraps

def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.2f} seconds")
        return result
    return wrapper

@timing_decorator
def slow_function():
    # Your code here
    pass
```

---

## 🆘 **Getting Help**

When you can't resolve an issue:

1. **Check the logs first**
   ```bash
   tail -f logs/civicmind.log
   journalctl -f -u civicmind  # If using systemd
   ```

2. **Gather system information**
   ```bash
   # System info
   uname -a
   python --version
   pip list
   
   # Application info
   curl http://localhost:8000/health
   ```

3. **Create minimal reproduction**
   ```python
   # Simplest possible code that shows the issue
   from civicmind.agents.parking_agent import ParkingAgent
   agent = ParkingAgent(llm)
   response = agent.analyze_issue("test", "test", {})
   print(response)
   ```

4. **Community support**
   - GitHub Issues: Report bugs with logs and reproduction steps
   - Discussions: Ask questions and share solutions
   - Email: support@civicmind.ai for urgent issues

Remember: Always include relevant logs, error messages, and system information when seeking help!
