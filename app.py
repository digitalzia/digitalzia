"""
Resume Ranker Web Application
A simple web interface for the AI Resume Ranking System
"""
import os
import json
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import sys
sys.path.append('/home/runner/work/digitalzia/digitalzia')

from models.resume_ranker import ResumeRanker


class ResumeRankerHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler for the Resume Ranker application"""
    
    def __init__(self, *args, **kwargs):
        self.ranker = ResumeRanker()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/' or parsed_path.path == '/index.html':
            self.serve_main_page()
        elif parsed_path.path == '/style.css':
            self.serve_css()
        elif parsed_path.path == '/script.js':
            self.serve_js()
        else:
            self.send_error(404)
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/rank':
            self.handle_ranking_request()
        else:
            self.send_error(404)
    
    def serve_main_page(self):
        """Serve the main HTML page"""
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resume Ranker AI - HR Recruitment Tool</title>
    <link rel="stylesheet" href="/style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>🎯 Resume Ranker AI</h1>
            <p>AI-Powered HR Recruitment Tool with 5-Factor Analysis</p>
        </header>
        
        <div class="main-content">
            <div class="job-requirements">
                <h2>📋 Job Requirements</h2>
                <form id="rankingForm">
                    <div class="form-group">
                        <label for="jobTitle">Job Title:</label>
                        <input type="text" id="jobTitle" name="jobTitle" placeholder="e.g., Senior Data Scientist" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="requiredSkills">Required Skills (comma-separated):</label>
                        <textarea id="requiredSkills" name="requiredSkills" 
                                placeholder="e.g., Python, Machine Learning, SQL, Data Analysis, Statistics" required></textarea>
                    </div>
                    
                    <div class="form-group">
                        <label for="jobKeywords">Job Keywords (comma-separated):</label>
                        <textarea id="jobKeywords" name="jobKeywords" 
                                placeholder="e.g., software development, data science, analytics, programming, research"></textarea>
                    </div>
                    
                    <div class="form-group">
                        <label for="resumeText">Resume Text:</label>
                        <textarea id="resumeText" name="resumeText" 
                                placeholder="Paste the candidate's resume text here..." required></textarea>
                    </div>
                    
                    <button type="submit">🔍 Analyze Resume</button>
                </form>
            </div>
            
            <div id="results" class="results-section" style="display: none;">
                <h2>📊 Ranking Results</h2>
                <div id="resultsContent"></div>
            </div>
        </div>
        
        <footer>
            <div class="ranking-factors">
                <h3>📈 Our 5-Factor Ranking System</h3>
                <div class="factors-grid">
                    <div class="factor">
                        <h4>🛠️ Skills Match (30%)</h4>
                        <p>How well the candidate's skills align with job requirements</p>
                    </div>
                    <div class="factor">
                        <h4>💼 Experience Relevance (25%)</h4>
                        <p>Relevance and depth of work experience</p>
                    </div>
                    <div class="factor">
                        <h4>🎓 Education Background (20%)</h4>
                        <p>Educational qualifications and certifications</p>
                    </div>
                    <div class="factor">
                        <h4>🏆 Achievements (15%)</h4>
                        <p>Certifications, awards, and notable accomplishments</p>
                    </div>
                    <div class="factor">
                        <h4>💬 Communication Quality (10%)</h4>
                        <p>Language quality and professional presentation</p>
                    </div>
                </div>
                
                <div class="classification-guide">
                    <h3>🎯 Classification Labels</h3>
                    <div class="labels-grid">
                        <div class="label perfect">Perfect Candidate (91-100)</div>
                        <div class="label outstanding">Outstanding (76-90)</div>
                        <div class="label adequate">Up to the Mark (61-75)</div>
                        <div class="label good">Good Candidate (0-60)</div>
                    </div>
                </div>
            </div>
        </footer>
    </div>
    
    <script src="/script.js"></script>
</body>
</html>
"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode())
    
    def serve_css(self):
        """Serve CSS styles"""
        css_content = """
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

header {
    text-align: center;
    margin-bottom: 30px;
    background: rgba(255, 255, 255, 0.95);
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

header h1 {
    font-size: 2.5em;
    color: #4a5568;
    margin-bottom: 10px;
}

header p {
    font-size: 1.2em;
    color: #718096;
}

.main-content {
    display: grid;
    gap: 30px;
    margin-bottom: 40px;
}

.job-requirements {
    background: rgba(255, 255, 255, 0.95);
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.job-requirements h2 {
    color: #4a5568;
    margin-bottom: 20px;
    font-size: 1.8em;
}

.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    font-weight: bold;
    color: #4a5568;
}

.form-group input,
.form-group textarea {
    width: 100%;
    padding: 12px;
    border: 2px solid #e2e8f0;
    border-radius: 8px;
    font-size: 16px;
    transition: border-color 0.3s ease;
}

.form-group input:focus,
.form-group textarea:focus {
    outline: none;
    border-color: #667eea;
}

.form-group textarea {
    min-height: 100px;
    resize: vertical;
}

#resumeText {
    min-height: 200px;
}

button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 15px 30px;
    border: none;
    border-radius: 8px;
    font-size: 18px;
    font-weight: bold;
    cursor: pointer;
    transition: transform 0.3s ease;
    width: 100%;
}

button:hover {
    transform: translateY(-2px);
}

.results-section {
    background: rgba(255, 255, 255, 0.95);
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.results-section h2 {
    color: #4a5568;
    margin-bottom: 20px;
    font-size: 1.8em;
}

.result-card {
    background: #f7fafc;
    padding: 25px;
    border-radius: 12px;
    margin-bottom: 20px;
    border-left: 5px solid #667eea;
}

.score-summary {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    flex-wrap: wrap;
    gap: 15px;
}

.final-score {
    font-size: 3em;
    font-weight: bold;
    color: #667eea;
}

.classification {
    padding: 10px 20px;
    border-radius: 25px;
    font-weight: bold;
    font-size: 1.2em;
    text-align: center;
}

.classification.perfect { background: #c6f6d5; color: #22543d; }
.classification.outstanding { background: #bee3f8; color: #2a69ac; }
.classification.adequate { background: #fef5e7; color: #c05621; }
.classification.good { background: #fed7d7; color: #c53030; }

.factors-breakdown {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 15px;
    margin-top: 20px;
}

.factor-score {
    background: white;
    padding: 15px;
    border-radius: 8px;
    text-align: center;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.factor-score h4 {
    color: #4a5568;
    margin-bottom: 10px;
}

.score-bar {
    background: #e2e8f0;
    height: 20px;
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 5px;
}

.score-fill {
    height: 100%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    transition: width 0.5s ease;
}

.ranking-factors {
    background: rgba(255, 255, 255, 0.95);
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.ranking-factors h3 {
    color: #4a5568;
    margin-bottom: 20px;
    font-size: 1.5em;
    text-align: center;
}

.factors-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.factor {
    background: #f7fafc;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    border-top: 4px solid #667eea;
}

.factor h4 {
    color: #4a5568;
    margin-bottom: 10px;
}

.classification-guide {
    text-align: center;
}

.labels-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
    margin-top: 15px;
}

.label {
    padding: 15px;
    border-radius: 10px;
    font-weight: bold;
    color: white;
}

.label.perfect { background: #48bb78; }
.label.outstanding { background: #4299e1; }
.label.adequate { background: #ed8936; }
.label.good { background: #e53e3e; }

@media (max-width: 768px) {
    .container {
        padding: 10px;
    }
    
    header h1 {
        font-size: 2em;
    }
    
    .score-summary {
        flex-direction: column;
        text-align: center;
    }
    
    .factors-grid,
    .labels-grid {
        grid-template-columns: 1fr;
    }
}
"""
        self.send_response(200)
        self.send_header('Content-type', 'text/css')
        self.end_headers()
        self.wfile.write(css_content.encode())
    
    def serve_js(self):
        """Serve JavaScript functionality"""
        js_content = """
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('rankingForm');
    const resultsSection = document.getElementById('results');
    const resultsContent = document.getElementById('resultsContent');
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(form);
        const data = {
            jobTitle: formData.get('jobTitle'),
            requiredSkills: formData.get('requiredSkills'),
            jobKeywords: formData.get('jobKeywords'),
            resumeText: formData.get('resumeText')
        };
        
        try {
            const response = await fetch('/rank', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            
            const result = await response.json();
            displayResults(result);
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while processing your request.');
        }
    });
    
    function displayResults(result) {
        const classificationClass = getClassificationClass(result.classification);
        
        resultsContent.innerHTML = `
            <div class="result-card">
                <div class="score-summary">
                    <div>
                        <div class="final-score">${result.final_score}</div>
                        <div style="text-align: center; color: #718096;">Final Score</div>
                    </div>
                    <div class="classification ${classificationClass}">
                        ${result.classification}
                    </div>
                </div>
                
                <h3 style="color: #4a5568; margin-bottom: 15px;">Factor Breakdown:</h3>
                <div class="factors-breakdown">
                    ${Object.entries(result.factor_scores).map(([factor, score]) => `
                        <div class="factor-score">
                            <h4>${formatFactorName(factor)}</h4>
                            <div class="score-bar">
                                <div class="score-fill" style="width: ${score}%"></div>
                            </div>
                            <div>${score}/100</div>
                        </div>
                    `).join('')}
                </div>
                
                <div style="margin-top: 20px; padding: 15px; background: #edf2f7; border-radius: 8px;">
                    <h4 style="color: #4a5568; margin-bottom: 10px;">Scoring Weights Used:</h4>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; font-size: 0.9em;">
                        ${Object.entries(result.weights_used).map(([factor, weight]) => `
                            <div>• ${formatFactorName(factor)}: ${(weight * 100).toFixed(0)}%</div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
        
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }
    
    function getClassificationClass(classification) {
        if (classification.includes('Perfect')) return 'perfect';
        if (classification.includes('Outstanding')) return 'outstanding';
        if (classification.includes('Up to the mark')) return 'adequate';
        return 'good';
    }
    
    function formatFactorName(factor) {
        return factor.replace(/_/g, ' ')
                    .split(' ')
                    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                    .join(' ');
    }
});
"""
        self.send_response(200)
        self.send_header('Content-type', 'application/javascript')
        self.end_headers()
        self.wfile.write(js_content.encode())
    
    def handle_ranking_request(self):
        """Handle resume ranking POST request"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Parse job requirements
            job_requirements = {
                'skills': [skill.strip() for skill in data.get('requiredSkills', '').split(',') if skill.strip()],
                'keywords': [keyword.strip() for keyword in data.get('jobKeywords', '').split(',') if keyword.strip()]
            }
            
            # Rank the resume
            resume_text = data.get('resumeText', '')
            result = self.ranker.rank_resume(resume_text, job_requirements)
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
            
        except Exception as e:
            print(f"Error processing ranking request: {e}")
            self.send_error(500, str(e))


def run_server(port=8000):
    """Run the web server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, ResumeRankerHandler)
    print(f"🚀 Resume Ranker AI Server running on http://localhost:{port}")
    print("📝 Open your browser and navigate to the URL above")
    print("🛑 Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        httpd.server_close()


if __name__ == "__main__":
    run_server()