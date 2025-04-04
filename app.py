from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import os
import json
from datetime import datetime
import platform
import sys
import subprocess
import time
import psutil

app = Flask(__name__)
CORS(app)

def get_cpu_usage_windows():
    """Get CPU usage on Windows using psutil"""
    try:
        # Get CPU usage percentage
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Get CPU information
        cpu_info = {
            'physical_cores': psutil.cpu_count(logical=False),
            'total_cores': psutil.cpu_count(logical=True),
            'max_frequency': psutil.cpu_freq().max if psutil.cpu_freq() else 'N/A',
            'current_frequency': psutil.cpu_freq().current if psutil.cpu_freq() else 'N/A',
            'name': platform.processor()
        }
        
        return {
            'usage_percent': cpu_percent,
            'cores': cpu_info['physical_cores'],
            'logical_processors': cpu_info['total_cores'],
            'name': cpu_info['name'],
            'frequency': {
                'current': cpu_info['current_frequency'],
                'max': cpu_info['max_frequency']
            }
        }
    except Exception as e:
        print(f"Error getting CPU usage: {str(e)}")
        return {
            'usage_percent': 0.0,
            'cores': 0,
            'logical_processors': 0,
            'name': 'Unknown',
            'frequency': {'current': 0, 'max': 0}
        }

def get_memory_usage_windows():
    """Get memory usage using psutil"""
    try:
        memory = psutil.virtual_memory()
        return {
            'total_gb': round(memory.total / (1024**3), 2),
            'available_gb': round(memory.available / (1024**3), 2),
            'used_gb': round(memory.used / (1024**3), 2),
            'used_percent': memory.percent
        }
    except Exception as e:
        print(f"Error getting memory usage: {str(e)}")
        return {
            'total_gb': 0,
            'available_gb': 0,
            'used_gb': 0,
            'used_percent': 0
        }

def get_disk_usage():
    """Get disk usage using psutil"""
    try:
        disk = psutil.disk_usage('/')
        io_counters = psutil.disk_io_counters()
        
        return {
            'total_gb': round(disk.total / (1024**3), 2),
            'used_gb': round(disk.used / (1024**3), 2),
            'free_gb': round(disk.free / (1024**3), 2),
            'used_percent': disk.percent,
            'io_stats': {
                'read_mb': round(io_counters.read_bytes / (1024**2), 2),
                'write_mb': round(io_counters.write_bytes / (1024**2), 2)
            }
        }
    except Exception as e:
        print(f"Error getting disk usage: {str(e)}")
        return {
            'total_gb': 0,
            'used_gb': 0,
            'free_gb': 0,
            'used_percent': 0,
            'io_stats': {'read_mb': 0, 'write_mb': 0}
        }

def get_running_processes():
    """Get list of running processes with their CPU and Memory usage"""
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'create_time']):
            try:
                pinfo = proc.info
                memory_mb = pinfo['memory_info'].rss / (1024 * 1024) if pinfo['memory_info'] else 0
                
                process = {
                    'name': pinfo['name'],
                    'pid': pinfo['pid'],
                    'cpu_usage': pinfo['cpu_percent'],
                    'memory_mb': round(memory_mb, 1),
                    'start_time': datetime.fromtimestamp(pinfo['create_time']).strftime('%Y-%m-%d %H:%M:%S')
                }
                processes.append(process)
                
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        # Sort processes
        cpu_intensive = sorted(
            [p for p in processes if p['cpu_usage'] is not None],
            key=lambda x: x['cpu_usage'],
            reverse=True
        )[:10]
        
        memory_intensive = sorted(
            [p for p in processes if p['memory_mb'] > 0],
            key=lambda x: x['memory_mb'],
            reverse=True
        )[:10]
        
        return {
            'cpu_intensive': cpu_intensive,
            'memory_intensive': memory_intensive
        }
    except Exception as e:
        print(f"Error getting processes: {str(e)}")
        return {
            'cpu_intensive': [],
            'memory_intensive': []
        }

def get_system_metrics():
    """Get all system metrics including CPU, memory, disk usage and processes"""
    try:
        # Get CPU information
        cpu_info = get_cpu_usage_windows()
        
        # Get memory information
        memory_info = get_memory_usage_windows()
        
        # Get disk information
        disk_info = get_disk_usage()
        
        # Get process information
        process_info = get_running_processes()
        
        return {
            'cpu': {
                'usage_percent': cpu_info['usage_percent'],
                'cores': cpu_info['cores'],
                'logical_processors': cpu_info['logical_processors'],
                'name': cpu_info['name'],
                'frequency': cpu_info['frequency']
            },
            'memory': memory_info,
            'disk': disk_info,
            'processes': process_info,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    except Exception as e:
        print(f"Error getting system metrics: {str(e)}")
        return {
            'error': str(e),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

@app.route('/api/metrics')
def metrics():
    """Get all system metrics"""
    return jsonify(get_system_metrics())

@app.route('/')
def index():
    """Display system monitor dashboard"""
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True) 