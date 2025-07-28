"""
Health Check Utilities for CivicMind Services
=============================================

Common health check functionality for microservices.
"""

import time
import psutil
from typing import Dict, Any
from datetime import datetime, timedelta


class HealthChecker:
    """Health check utility for microservices"""
    
    def __init__(self, service_name: str, start_time: float = None):
        self.service_name = service_name
        self.start_time = start_time or time.time()
        self.checks = {}
    
    def get_uptime(self) -> float:
        """Get service uptime in seconds"""
        return time.time() - self.start_time
    
    def check_memory_usage(self, threshold_mb: int = 512) -> Dict[str, Any]:
        """Check memory usage"""
        try:
            process = psutil.Process()
            memory_mb = process.memory_info().rss / 1024 / 1024
            
            return {
                "status": "healthy" if memory_mb < threshold_mb else "warning",
                "memory_mb": round(memory_mb, 2),
                "threshold_mb": threshold_mb,
                "details": f"Memory usage: {memory_mb:.1f}MB"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "details": "Could not check memory usage"
            }
    
    def check_disk_space(self, threshold_gb: int = 1) -> Dict[str, Any]:
        """Check available disk space"""
        try:
            disk_usage = psutil.disk_usage('/')
            free_gb = disk_usage.free / 1024 / 1024 / 1024
            
            return {
                "status": "healthy" if free_gb > threshold_gb else "warning",
                "free_gb": round(free_gb, 2),
                "threshold_gb": threshold_gb,
                "details": f"Free disk space: {free_gb:.1f}GB"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "details": "Could not check disk space"
            }
    
    def check_external_dependency(self, name: str, url: str, 
                                  timeout: int = 5) -> Dict[str, Any]:
        """Check external dependency health"""
        import httpx
        
        try:
            start = time.time()
            with httpx.Client(timeout=timeout) as client:
                response = client.get(url)
            
            response_time = (time.time() - start) * 1000
            
            return {
                "status": "healthy" if response.status_code == 200 else "error",
                "response_code": response.status_code,
                "response_time_ms": round(response_time, 2),
                "details": f"{name} responded in {response_time:.0f}ms"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "details": f"Could not reach {name}"
            }
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get overall health status"""
        # Run all registered checks
        all_checks = {
            "memory": self.check_memory_usage(),
            "disk": self.check_disk_space(),
        }
        all_checks.update(self.checks)
        
        # Determine overall status
        statuses = [check["status"] for check in all_checks.values()]
        if "error" in statuses:
            overall_status = "unhealthy"
        elif "warning" in statuses:
            overall_status = "degraded"
        else:
            overall_status = "healthy"
        
        return {
            "service": self.service_name,
            "status": overall_status,
            "uptime_seconds": round(self.get_uptime(), 2),
            "checks": all_checks,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    
    def add_custom_check(self, name: str, check_func) -> None:
        """Add a custom health check"""
        try:
            result = check_func()
            self.checks[name] = result
        except Exception as e:
            self.checks[name] = {
                "status": "error",
                "error": str(e),
                "details": f"Custom check '{name}' failed"
            }
