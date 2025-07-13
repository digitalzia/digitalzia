# 🎯 Resume Ranker AI - HR Recruitment Tool

An AI-powered resume ranking system that evaluates candidates using 5 key factors to help HR professionals make data-driven hiring decisions.

## 🌟 Features

### 5-Factor Analysis System
1. **Skills Match (30% weight)** - How well candidate skills align with job requirements
2. **Experience Relevance (25% weight)** - Relevance and depth of work experience  
3. **Education Background (20% weight)** - Educational qualifications and certifications
4. **Achievements/Certifications (15% weight)** - Notable accomplishments and certifications
5. **Communication Quality (10% weight)** - Language quality and professional presentation

### Classification Labels
- **Perfect Candidate (91-100 points)** 🌟 - Exceptional match for the position
- **Outstanding (76-90 points)** ⭐ - Excellent candidate with strong qualifications
- **Up to the Mark (61-75 points)** 👍 - Good candidate meeting requirements
- **Good Candidate (0-60 points)** 👌 - Basic qualifications, may need development

## 🚀 Quick Start

### Command Line Demo
```bash
# Run interactive demo
python3 demo.py

# Run with sample data
python3 demo.py --sample
```

### Web Application
```bash
# Start the web server
python3 app.py

# Open browser and go to:
# http://localhost:8000
```

### API Usage
```python
from models.resume_ranker import ResumeRanker

# Initialize ranker
ranker = ResumeRanker()

# Define job requirements
job_requirements = {
    'skills': ['Python', 'Machine Learning', 'SQL'],
    'keywords': ['data science', 'analytics', 'programming']
}

# Rank a resume
result = ranker.rank_resume(resume_text, job_requirements)
print(f"Score: {result['final_score']}/100")
print(f"Classification: {result['classification']}")
```

## 📁 Project Structure

```
digitalzia/
├── app.py                 # Web application server
├── demo.py               # Command line demo
├── requirements.txt      # Dependencies
├── models/
│   └── resume_ranker.py  # Core ranking algorithm
├── uploads/              # Resume file storage
└── README.md            # This file
```

## 🔧 Technical Details

### Ranking Algorithm

The system uses a weighted scoring approach:

```python
final_score = (
    skills_score * 0.30 +
    experience_score * 0.25 +
    education_score * 0.20 +
    achievements_score * 0.15 +
    communication_score * 0.10
)
```

### Skills Matching
- Exact keyword matching in resume text
- Case-insensitive comparison
- Percentage of required skills found

### Experience Analysis
- Years of experience extraction using regex patterns
- Job-related keyword relevance scoring
- Combined experience depth and relevance metrics

### Education Scoring
- Hierarchical qualification scoring (PhD > Master > Bachelor)
- Multiple qualification bonuses
- Certification recognition

### Achievements Detection
- Achievement keyword identification
- Certification pattern matching
- Leadership and project accomplishment scoring

### Communication Quality
- Text structure analysis
- Professional vocabulary assessment
- Readability and coherence metrics

## 🎯 Use Cases

### HR Departments
- Screen large volumes of resumes efficiently
- Standardize candidate evaluation process
- Reduce unconscious bias in initial screening
- Generate consistent ranking reports

### Recruitment Agencies
- Quickly identify top candidates for clients
- Provide data-driven candidate recommendations
- Streamline the candidate shortlisting process

### Hiring Managers
- Get objective candidate assessments
- Focus interview time on highest-ranked candidates
- Make evidence-based hiring decisions

## 📊 Sample Output

```
🎯 RESUME RANKING RESULTS
============================================================
Job Position: Senior Data Scientist

🎯 FINAL SCORE: 96.5/100
📈 CLASSIFICATION: Perfect candidate
🌟 Status: PERFECT

📋 DETAILED FACTOR ANALYSIS
----------------------------------------
Skills Match               100.0/100 [████████████████████] (30%)
Experience Relevance        98.0/100 [███████████████████░] (25%)
Education Background       100.0/100 [████████████████████] (20%)
Achievements & Certifications  100.0/100 [████████████████████] (15%)
Communication Quality       70.0/100 [██████████████░░░░░░] (10%)
```

## 🛠️ Customization

### Adjusting Weights
Modify the weights in `models/resume_ranker.py`:

```python
self.weights = {
    'skills': 0.35,        # Increase skills importance
    'experience': 0.25,
    'education': 0.15,     # Decrease education weight
    'achievements': 0.15,
    'communication': 0.10
}
```

### Adding New Factors
Extend the `ResumeRanker` class to include additional factors:

```python
def calculate_custom_factor(self, resume_text: str) -> float:
    # Your custom scoring logic
    return score

def rank_resume(self, resume_text: str, job_requirements: Dict) -> Dict:
    # Include your custom factor in the calculation
    custom_score = self.calculate_custom_factor(resume_text)
    # Update weights and calculation accordingly
```

## 🔍 Algorithm Transparency

The system provides full transparency in its scoring:
- Individual factor scores are shown
- Weights used are displayed
- Contribution of each factor to final score is calculated
- Classification thresholds are clearly defined

## 🎓 Educational Value

This project demonstrates:
- Text processing and analysis techniques
- Weighted scoring algorithms
- Web application development
- Command-line interface design
- Modular code architecture
- Documentation best practices

## 📝 Contributing

To improve the ranking algorithm:
1. Analyze the factor calculation methods
2. Test with diverse resume samples
3. Adjust weights based on hiring success correlations
4. Add new factors relevant to specific industries

## 🔮 Future Enhancements

- PDF resume parsing
- Machine learning-based improvements
- Industry-specific ranking models
- Batch processing capabilities
- Integration with ATS systems
- Multi-language support
- Resume formatting analysis

---

*Built with ❤️ for HR professionals to make better hiring decisions*