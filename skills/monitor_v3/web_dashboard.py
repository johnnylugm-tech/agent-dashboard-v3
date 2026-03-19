#!/usr/bin/env python3
"""
Agent Monitor Web Dashboard v2.1

Enhanced with:
- Working chart switching (daily/weekly/monthly)
- API documentation section
- Agent operations (restart, pause)
"""

from flask import Flask, render_template_string, jsonify, request
from datetime import datetime, timedelta
import os

app = Flask(__name__, template_folder='templates')

DEFAULT_PORT = 8080

# ============================================================================
# Mock Data Functions
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

def get_cost_trend_data(period='daily'):
    """Cost trend data by period"""
    if period == 'daily':
        days = 14
        label = '14 Days'
        costs = [round(8 + (i % 5) * 2 + (i * 0.3), 2) for i in range(days)]
        dates = [(datetime.now() - timedelta(days=days - i - 1)).strftime("%m-%d") for i in range(days)]
    elif period == 'weekly':
        weeks = 8
        label = '8 Weeks'
        costs = [round(50 + i * 5 + (i % 3) * 10, 2) for i in range(weeks)]
        dates = [f"W{i+1}" for i in range(weeks)]
    else:  # monthly
        months = 6
        label = '6 Months'
        costs = [round(200 + i * 30 + (i % 2) * 50, 2) for i in range(months)]
        dates = [(datetime.now() - timedelta(days=30 * (months - i - 1))).strftime("%Y-%m") for i in range(months)]
    
    return {
        "period": period,
        "label": label,
        "dates": dates,
        "costs": costs
    }

def get_mock_alerts():
    return [
        {"id": 1, "level": "critical", "title": "Deployer Failed", "message": "Agent Deployer failed", "time": "10 min ago"},
        {"id": 2, "level": "warning", "title": "High Latency", "message": "P95 latency > 5s", "time": "30 min ago"},
        {"id": 3, "level": "info", "title": "Cache Hit Rate", "message": "Cache hit rate dropped to 45%", "time": "1 hour ago"},
    ]

# ============================================================================
# API Documentation
# ============================================================================

API_DOCS = """
## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/agents | List all agents |
| GET | /api/agents/&lt;id&gt; | Get agent details |
| GET | /api/metrics | Get metrics summary |
| GET | /api/cost-trend | Get cost trend (daily) |
| GET | /api/cost-trend?period=weekly | Get weekly trend |
| GET | /api/alerts | Get alerts |
| POST | /api/agents/&lt;id&gt;/restart | Restart agent |
| POST | /api/agents/&lt;id&gt;/pause | Pause agent |
| POST | /api/agents/&lt;id&gt;/resume | Resume agent |
| DELETE | /api/alerts/&lt;id&gt; | Dismiss alert |

## Example Response

```json
{
  "agents": [
    {
      "id": "agent-001",
      "name": "Code Generator",
      "status": "running",
      "health_score": 92
    }
  ]
}
```
"""

# ============================================================================
# HTML Template
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
        
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
        
        .health-bar { width: 120px; height: 8px; background: #0f0f23; border-radius: 4px; overflow: hidden; }
        .health-fill { height: 100%; border-radius: 4px; transition: width 0.5s ease; }
        
        .alert-list { display: flex; flex-direction: column; gap: 10px; max-height: 320px; overflow-y: auto; }
        .alert-item { padding: 15px; border-radius: 12px; border-left: 4px solid; animation: slideIn 0.3s ease; position: relative; }
        .alert-item.critical { background: linear-gradient(90deg, rgba(255,71,87,0.2), transparent); border-color: #ff4757; }
        .alert-item.warning { background: linear-gradient(90deg, rgba(255,193,7,0.2), transparent); border-color: #ffc107; }
        .alert-item.info { background: linear-gradient(90deg, rgba(0,212,255,0.2), transparent); border-color: #00d4ff; }
        
        @keyframes slideIn { from { opacity: 0; transform: translateX(-20px); } to { opacity: 1; transform: translateX(0); } }
        
        .tab-bar { display: flex; gap: 10px; margin-bottom: 15px; }
        .tab { padding: 8px 16px; background: #16213e; border: none; border-radius: 8px; color: #888; cursor: pointer; transition: all 0.3s; }
        .tab.active { background: #00d4ff; color: #0f0f23; }
        .tab:hover:not(.active) { background: #1e1e4e; }
        
        .btn { padding: 6px 12px; border: none; border-radius: 6px; cursor: pointer; font-size: 12px; transition: all 0.2s; }
        .btn-restart { background: #00d4ff; color: #0f0f23; }
        .btn-pause { background: #ffc107; color: #0f0f23; }
        .btn-dismiss { background: transparent; color: #666; border: 1px solid #333; }
        .btn:hover { transform: scale(1.05); }
        
        .agent-actions { display: flex; gap: 8px; }
        
        .api-doc { background: #0f0f23; padding: 20px; border-radius: 12px; font-family: monospace; font-size: 13px; line-height: 1.6; }
        .api-doc table { width: 100%; border-collapse: collapse; margin: 15px 0; }
        .api-doc td, .api-doc th { padding: 8px; border: 1px solid #333; text-align: left; }
        .api-doc th { background: #1a1a3e; }
        
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
                <div class="alert-list" id="alertList">
                    {% for alert in alerts %}
                    <div class="alert-item {{ alert.level }}" data-id="{{ alert.id }}">
                        <div style="font-weight: 600;">{{ alert.title }}</div>
                        <div style="font-size: 12px; opacity: 0.8; margin-top: 5px;">{{ alert.message }}</div>
                        <div style="font-size: 11px; opacity: 0.5; margin-top: 5px;">{{ alert.time }}</div>
                        <button class="btn btn-dismiss" style="position: absolute; top: 10px; right: 10px;" onclick="dismissAlert({{ alert.id }})">✕</button>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>
        
        <div class="main-grid">
            <div class="card">
                <h2>🤖 Agent Status</h2>
                <div class="agents-list" id="agentsList">
                    {% for agent in agents %}
                    <div class="agent-item">
                        <div class="agent-info">
                            <div class="status-dot {{ agent.status }}"></div>
                            <div>
                                <div style="font-weight: 600;">{{ agent.name }}</div>
                                <div style="font-size: 12px; color: #666;">{{ agent.id }}</div>
                            </div>
                        </div>
                        <div style="display: flex; align-items: center; gap: 20px;">
                            <div style="text-align: right;">
                                <div class="health-bar">
                                    <div class="health-fill" style="width: {{ agent.health_score }}%; background: {% if agent.health_score >= 80 %}#00ff88{% elif agent.health_score >= 50 %}#ffc107{% else %}#ff4757{% endif %};"></div>
                                </div>
                                <div style="font-size: 12px; color: #888; margin-top: 5px;">{{ agent.health_score }}/100</div>
                            </div>
                            <div class="agent-actions">
                                <button class="btn btn-restart" onclick="restartAgent('{{ agent.id }}')">Restart</button>
                                <button class="btn btn-pause" onclick="pauseAgent('{{ agent.id }}')">Pause</button>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
            
            <div class="card">
                <h2>📚 API Documentation</h2>
                <div class="api-doc">
                    <table>
                        <tr><th>Method</th><th>Endpoint</th><th>Description</th></tr>
                        <tr><td>GET</td><td>/api/agents</td><td>List all agents</td></tr>
                        <tr><td>GET</td><td>/api/metrics</td><td>Get metrics</td></tr>
                        <tr><td>GET</td><td>/api/cost-trend?period=weekly</td><td>Cost trend</td></tr>
                        <tr><td>POST</td><td>/api/agents/&lt;id&gt;/restart</td><td>Restart agent</td></tr>
                        <tr><td>POST</td><td>/api/agents/&lt;id&gt;/pause</td><td>Pause agent</td></tr>
                        <tr><td>DELETE</td><td>/api/alerts/&lt;id&gt;</td><td>Dismiss alert</td></tr>
                    </table>
                    <div style="margin-top: 10px; color: #666;">
                        <a href="/api/agents" target="_blank" style="color: #00d4ff;">Try /api/agents</a> |
                        <a href="/api/metrics" target="_blank" style="color: #00d4ff;">Try /api/metrics</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        var costChart = echarts.init(document.getElementById('costChart'));
        var currentPeriod = 'daily';
        
        function getChartData(period) {
            var data = {{ cost_trend | tojson }};
            return data;
        }
        
        function updateChart(period) {
            fetch('/api/cost-trend?period=' + period)
                .then(response => response.json())
                .then(data => {
                    costChart.setOption({
                        xAxis: { data: data.dates },
                        series: [{ data: data.costs }]
                    });
                });
        }
        
        function switchChart(period) {
            currentPeriod = period;
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            event.target.classList.add('active');
            updateChart(period);
        }
        
        // Initial chart
        updateChart('daily');
        
        window.addEventListener('resize', function() {
            costChart.resize();
        });
        
        // Agent operations
        function restartAgent(agentId) {
            if (confirm('Restart ' + agentId + '?')) {
                fetch('/api/agents/' + agentId + '/restart', { method: 'POST' })
                    .then(r => r.json())
                    .then(d => alert(d.message || 'Restarted!'))
                    .catch(e => alert('Error: ' + e));
            }
        }
        
        function pauseAgent(agentId) {
            if (confirm('Pause ' + agentId + '?')) {
                fetch('/api/agents/' + agentId + '/pause', { method: 'POST' })
                    .then(r => r.json())
                    .then(d => alert(d.message || 'Paused!'))
                    .catch(e => alert('Error: ' + e));
            }
        }
        
        function dismissAlert(alertId) {
            fetch('/api/alerts/' + alertId, { method: 'DELETE' })
                .then(r => r.json())
                .then(d => {
                    document.querySelector('[data-id="' + alertId + '"]').remove();
                })
                .catch(e => alert('Error: ' + e));
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
        cost_trend=get_cost_trend_data('daily'),
        time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

@app.route('/api/agents')
def api_agents():
    return jsonify(get_mock_agents())

@app.route('/api/agents/<agent_id>')
def api_agent(agent_id):
    agents = get_mock_agents()
    for a in agents:
        if a['id'] == agent_id:
            return jsonify(a)
    return jsonify({'error': 'Not found'}), 404

@app.route('/api/metrics')
def api_metrics():
    return jsonify(get_mock_metrics())

@app.route('/api/cost-trend')
def api_cost_trend():
    period = request.args.get('period', 'daily')
    return jsonify(get_cost_trend_data(period))

@app.route('/api/alerts')
def api_alerts():
    return jsonify(get_mock_alerts())

@app.route('/api/agents/<agent_id>/restart', methods=['POST'])
def api_restart(agent_id):
    return jsonify({'status': 'success', 'message': f'Agent {agent_id} restarted'})

@app.route('/api/agents/<agent_id>/pause', methods=['POST'])
def api_pause(agent_id):
    return jsonify({'status': 'success', 'message': f'Agent {agent_id} paused'})

@app.route('/api/agents/<agent_id>/resume', methods=['POST'])
def api_resume(agent_id):
    return jsonify({'status': 'success', 'message': f'Agent {agent_id} resumed'})

@app.route('/api/alerts/<alert_id>', methods=['DELETE'])
def api_dismiss_alert(alert_id):
    return jsonify({'status': 'success', 'message': f'Alert {alert_id} dismissed'})

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

# ============================================================================
# Main
# ============================================================================

if __name__ == '__main__':
    port = int(os.getenv('PORT', DEFAULT_PORT))
    print(f"\n🚀 Agent Monitor Dashboard v2.1")
    print(f"   URL: http://localhost:{port}")
    print(f"   API: http://localhost:{port}/api/agents\n")
    
    app.run(host='0.0.0.0', port=port, debug=True)
