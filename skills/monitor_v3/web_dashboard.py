#!/usr/bin/env python3
"""
Agent Monitor Web Dashboard

Flask-based web dashboard for monitoring AI agents
"""

from flask import Flask, render_template_string, jsonify, request
from datetime import datetime
import os

app = Flask(__name__)

# ============================================================================
# Mock Data (Replace with real data in production)
# ============================================================================

def get_mock_agents():
    return [
        {"id": "agent-001", "name": "Code Generator", "status": "running", "health_score": 92},
        {"id": "agent-002", "name": "Code Reviewer", "status": "running", "health_score": 88},
        {"id": "agent-003", "name": "Tester", "status": "idle", "health_score": 95},
        {"id": "agent-004", "name": "Deployer", "status": "failed", "health_score": 45},
    ]

def get_mock_metrics():
    return {
        "total_requests": 1250,
        "success_rate": 94.5,
        "avg_latency": 1.2,
        "cost_daily": 12.50,
        "cost_weekly": 87.50,
        "cost_monthly": 350.00
    }

def get_mock_cost_trend():
    return {
        "daily": {
            "2026-03-14": 10.0,
            "2026-03-15": 12.5,
            "2026-03-16": 8.0,
            "2026-03-17": 15.0,
            "2026-03-18": 11.0,
            "2026-03-19": 12.5,
            "2026-03-20": 5.0,
        }
    }

def get_mock_alerts():
    return [
        {"id": 1, "level": "critical", "title": "Deployer Failed", "message": "Agent Deployer failed", "time": "10 min ago"},
        {"id": 2, "level": "warning", "title": "High Latency", "message": "P95 latency > 5s", "time": "30 min ago"},
    ]

# ============================================================================
# HTML Templates
# ============================================================================

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agent Monitor Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #1a1a2e; color: #fff; }
        
        .header { background: #16213e; padding: 20px; display: flex; justify-content: space-between; align-items: center; }
        .header h1 { font-size: 24px; }
        .header .time { color: #888; }
        
        .container { padding: 20px; }
        
        .stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 20px; }
        .stat-card { background: #16213e; padding: 20px; border-radius: 12px; }
        .stat-card .label { color: #888; font-size: 14px; }
        .stat-card .value { font-size: 32px; font-weight: bold; margin: 10px 0; }
        .stat-card .trend { font-size: 14px; }
        .trend.up { color: #4ade80; }
        .trend.down { color: #f87171; }
        
        .main-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 20px; }
        
        .card { background: #16213e; border-radius: 12px; padding: 20px; }
        .card h2 { font-size: 18px; margin-bottom: 20px; color: #888; }
        
        .agents-list { display: flex; flex-direction: column; gap: 10px; }
        .agent-item { background: #1a1a2e; padding: 15px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; }
        .agent-info { display: flex; align-items: center; gap: 15px; }
        .status-dot { width: 12px; height: 12px; border-radius: 50%; }
        .status-dot.running { background: #4ade80; }
        .status-dot.idle { background: #fbbf24; }
        .status-dot.failed { background: #f87171; }
        
        .health-bar { width: 100px; height: 8px; background: #333; border-radius: 4px; overflow: hidden; }
        .health-fill { height: 100%; border-radius: 4px; }
        
        .alert-list { display: flex; flex-direction: column; gap: 10px; }
        .alert-item { padding: 15px; border-radius: 8px; border-left: 4px solid; }
        .alert-item.critical { background: #2d1f1f; border-color: #f87171; }
        .alert-item.warning { background: #2d2a1f; border-color: #fbbf24; }
        .alert-item.info { background: #1f2d2d; border-color: #4ade80; }
        
        .chart-placeholder { height: 200px; background: #1a1a2e; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #666; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 Agent Monitor</h1>
        <span class="time">{{ time }}</span>
    </div>
    
    <div class="container">
        <div class="stats-grid">
            <div class="stat-card">
                <div class="label">Total Requests</div>
                <div class="value">{{ metrics.total_requests }}</div>
                <div class="trend up">↑ 12% from yesterday</div>
            </div>
            <div class="stat-card">
                <div class="label">Success Rate</div>
                <div class="value">{{ metrics.success_rate }}%</div>
                <div class="trend up">↑ 2% from yesterday</div>
            </div>
            <div class="stat-card">
                <div class="label">Avg Latency</div>
                <div class="value">{{ metrics.avg_latency }}s</div>
                <div class="trend down">↓ 0.3s from yesterday</div>
            </div>
            <div class="stat-card">
                <div class="label">Daily Cost</div>
                <div class="value">${{ metrics.cost_daily }}</div>
                <div class="trend up">↑ $2 from yesterday</div>
            </div>
        </div>
        
        <div class="main-grid">
            <div class="card">
                <h2>🤖 Agent Status</h2>
                <div class="agents-list">
                    {% for agent in agents %}
                    <div class="agent-item">
                        <div class="agent-info">
                            <div class="status-dot {{ agent.status }}"></div>
                            <div>
                                <div>{{ agent.name }}</div>
                                <div style="color: #666; font-size: 12px;">{{ agent.id }}</div>
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div class="health-bar">
                                <div class="health-fill" style="width: {{ agent.health_score }}%; background: {% if agent.health_score >= 80 %}#4ade80{% elif agent.health_score >= 50 %}#fbbf24{% else %}#f87171{% endif %};"></div>
                            </div>
                            <div style="font-size: 12px; color: #888; margin-top: 5px;">{{ agent.health_score }}/100</div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
            
            <div class="card">
                <h2>⚠️ Recent Alerts</h2>
                <div class="alert-list">
                    {% for alert in alerts %}
                    <div class="alert-item {{ alert.level }}">
                        <div style="font-weight: bold;">{{ alert.title }}</div>
                        <div style="font-size: 12px; opacity: 0.8;">{{ alert.message }}</div>
                        <div style="font-size: 11px; opacity: 0.6; margin-top: 5px;">{{ alert.time }}</div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

# ============================================================================
# Routes
# ============================================================================

@app.route('/')
def index():
    return render_template_string(DASHBOARD_HTML,
        agents=get_mock_agents(),
        metrics=get_mock_metrics(),
        alerts=get_mock_alerts(),
        time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

@app.route('/api/agents')
def api_agents():
    return jsonify(get_mock_agents())

@app.route('/api/metrics')
def api_metrics():
    return jsonify(get_mock_metrics())

@app.route('/api/cost-trend')
def api_cost_trend():
    return jsonify(get_mock_cost_trend())

@app.route('/api/alerts')
def api_alerts():
    return jsonify(get_mock_alerts())

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

# ============================================================================
# Main
# ============================================================================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print(f"\n🚀 Agent Monitor Dashboard")
    print(f"   URL: http://localhost:{port}")
    print(f"   API: http://localhost:{port}/api/agents\n")
    
    app.run(host='0.0.0.0', port=port, debug=True)
