#!/usr/bin/env python3
"""
Agent Monitor Web Dashboard v2

Enhanced with ECharts for real-time charts
"""

from flask import Flask, render_template_string, jsonify, request
from datetime import datetime, timedelta
import os

app = Flask(__name__, template_folder='templates')

# Default port
DEFAULT_PORT = 8080

# ============================================================================
# Mock Data Functions (Replace with real data in production)
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

def get_cost_trend_data():
    """Cost trend data for ECharts"""
    days = 14
    dates = []
    costs = []
    
    for i in range(days):
        date = datetime.now() - timedelta(days=days - i - 1)
        dates.append(date.strftime("%m-%d"))
        costs.append(round(8 + (i % 5) * 2 + (i * 0.3), 2))
    
    return {
        "dates": dates,
        "costs": costs
    }

def get_request_trend_data():
    """Request trend data for ECharts"""
    hours = 24
    times = []
    requests = []
    
    for i in range(hours):
        hour = datetime.now() - timedelta(hours=hours - i - 1)
        times.append(hour.strftime("%H:00"))
        requests.append(50 + (i % 10) * 5 + (i * 2))
    
    return {
        "times": times,
        "requests": requests
    }

def get_mock_alerts():
    return [
        {"id": 1, "level": "critical", "title": "Deployer Failed", "message": "Agent Deployer failed", "time": "10 min ago"},
        {"id": 2, "level": "warning", "title": "High Latency", "message": "P95 latency > 5s", "time": "30 min ago"},
        {"id": 3, "level": "info", "title": "Cache Hit Rate", "message": "Cache hit rate dropped to 45%", "time": "1 hour ago"},
    ]

# ============================================================================
# HTML Template with ECharts
# ============================================================================

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agent Monitor Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f0f23; color: #fff; }
        
        .header { background: #1a1a3e; padding: 20px 30px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #333; }
        .header h1 { font-size: 24px; font-weight: 600; }
        .header h1 span { color: #00d4ff; }
        .header .time { color: #888; font-size: 14px; }
        
        .container { padding: 20px 30px; }
        
        .stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 20px; }
        .stat-card { background: linear-gradient(135deg, #1a1a3e 0%, #16213e 100%); padding: 20px; border-radius: 16px; border: 1px solid #2a2a5e; }
        .stat-card .label { color: #888; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; }
        .stat-card .value { font-size: 36px; font-weight: bold; margin: 10px 0; background: linear-gradient(90deg, #fff, #00d4ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .stat-card .trend { font-size: 13px; display: flex; align-items: center; gap: 5px; }
        .trend.up { color: #00ff88; }
        .trend.down { color: #ff4757; }
        
        .main-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 20px; margin-bottom: 20px; }
        
        .card { background: #1a1a3e; border-radius: 16px; padding: 20px; border: 1px solid #2a2a5e; }
        .card h2 { font-size: 16px; color: #888; margin-bottom: 20px; display: flex; align-items: center; gap: 10px; }
        
        .chart-container { height: 280px; width: 100%; }
        
        .agents-list { display: flex; flex-direction: column; gap: 12px; }
        .agent-item { background: #16213e; padding: 15px 20px; border-radius: 12px; display: flex; justify-content: space-between; align-items: center; transition: all 0.3s; }
        .agent-item:hover { background: #1e1e4e; transform: translateX(5px); }
        .agent-info { display: flex; align-items: center; gap: 15px; }
        .status-dot { width: 12px; height: 12px; border-radius: 50%; animation: pulse 2s infinite; }
        .status-dot.running { background: #00ff88; box-shadow: 0 0 10px #00ff88; }
        .status-dot.idle { background: #ffc107; }
        .status-dot.failed { background: #ff4757; box-shadow: 0 0 10px #ff4757; }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .health-bar { width: 120px; height: 8px; background: #0f0f23; border-radius: 4px; overflow: hidden; }
        .health-fill { height: 100%; border-radius: 4px; transition: width 0.5s ease; }
        
        .alert-list { display: flex; flex-direction: column; gap: 10px; max-height: 320px; overflow-y: auto; }
        .alert-item { padding: 15px; border-radius: 12px; border-left: 4px solid; animation: slideIn 0.3s ease; }
        .alert-item.critical { background: linear-gradient(90deg, rgba(255,71,87,0.2), transparent); border-color: #ff4757; }
        .alert-item.warning { background: linear-gradient(90deg, rgba(255,193,7,0.2), transparent); border-color: #ffc107; }
        .alert-item.info { background: linear-gradient(90deg, rgba(0,212,255,0.2), transparent); border-color: #00d4ff; }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        }
        
        .tab-bar { display: flex; gap: 10px; margin-bottom: 15px; }
        .tab { padding: 8px 16px; background: #16213e; border: none; border-radius: 8px; color: #888; cursor: pointer; transition: all 0.3s; }
        .tab.active { background: #00d4ff; color: #0f0f23; }
        .tab:hover:not(.active) { background: #1e1e4e; }
        
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: #0f0f23; }
        ::-webkit-scrollbar-thumb { background: #333; border-radius: 3px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 Agent <span>Monitor</span></h1>
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
                <h2>📈 Cost Trend</h2>
                <div class="tab-bar">
                    <button class="tab active" onclick="switchChart('daily')">Daily</button>
                    <button class="tab" onclick="switchChart('weekly')">Weekly</button>
                    <button class="tab" onclick="switchChart('monthly')">Monthly</button>
                </div>
                <div id="costChart" class="chart-container"></div>
            </div>
            
            <div class="card">
                <h2>⚠️ Recent Alerts</h2>
                <div class="alert-list">
                    {% for alert in alerts %}
                    <div class="alert-item {{ alert.level }}">
                        <div style="font-weight: 600;">{{ alert.title }}</div>
                        <div style="font-size: 12px; opacity: 0.8; margin-top: 5px;">{{ alert.message }}</div>
                        <div style="font-size: 11px; opacity: 0.5; margin-top: 5px;">{{ alert.time }}</div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>
        
        <div class="card">
            <h2>🤖 Agent Status</h2>
            <div class="agents-list">
                {% for agent in agents %}
                <div class="agent-item">
                    <div class="agent-info">
                        <div class="status-dot {{ agent.status }}"></div>
                        <div>
                            <div style="font-weight: 600;">{{ agent.name }}</div>
                            <div style="font-size: 12px; color: #666;">{{ agent.id }}</div>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div class="health-bar">
                            <div class="health-fill" style="width: {{ agent.health_score }}%; background: {% if agent.health_score >= 80 %}#00ff88{% elif agent.health_score >= 50 %}#ffc107{% else %}#ff4757{% endif %};"></div>
                        </div>
                        <div style="font-size: 12px; color: #888; margin-top: 5px;">{{ agent.health_score }}/100</div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
    
    <script>
        // Initialize ECharts
        var costChart = echarts.init(document.getElementById('costChart'));
        
        var option = {
            backgroundColor: 'transparent',
            grid: { top: 20, right: 20, bottom: 30, left: 50 },
            xAxis: {
                type: 'category',
                data: {{ cost_trend.dates | safe }},
                axisLine: { lineStyle: { color: '#333' } },
                axisLabel: { color: '#888' }
            },
            yAxis: {
                type: 'value',
                axisLine: { lineStyle: { color: '#333' } },
                axisLabel: { color: '#888', formatter: '$' + '{value}' },
                splitLine: { lineStyle: { color: '#222' } }
            },
            series: [{
                data: {{ cost_trend.costs | safe }},
                type: 'line',
                smooth: true,
                symbol: 'circle',
                symbolSize: 8,
                lineStyle: { color: '#00d4ff', width: 3 },
                itemStyle: { color: '#00d4ff' },
                areaStyle: {
                    color: {
                        type: 'linear',
                        x: 0, y: 0, x2: 0, y2: 1,
                        colorStops: [
                            { offset: 0, color: 'rgba(0,212,255,0.3)' },
                            { offset: 1, color: 'rgba(0,212,255,0)' }
                        ]
                    }
                }
            }],
            tooltip: {
                trigger: 'axis',
                backgroundColor: '#1a1a3e',
                borderColor: '#333',
                textStyle: { color: '#fff' }
            }
        };
        
        costChart.setOption(option);
        
        // Responsive
        window.addEventListener('resize', function() {
            costChart.resize();
        });
        
        function switchChart(period) {
            // Update chart based on period
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            event.target.classList.add('active');
        }
    </script>
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
        cost_trend=get_cost_trend_data(),
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
    return jsonify(get_cost_trend_data())

@app.route('/api/request-trend')
def api_request_trend():
    return jsonify(get_request_trend_data())

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
    port = int(os.getenv('PORT', DEFAULT_PORT))
    print(f"\n🚀 Agent Monitor Dashboard v2")
    print(f"   URL: http://localhost:{port}")
    print(f"   API: http://localhost:{port}/api/agents\n")
    
    app.run(host='0.0.0.0', port=port, debug=True)
