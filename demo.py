#!/usr/bin/env python3
"""
Resume Ranker AI - Command Line Demo
Interactive demo of the 5-factor resume ranking system
"""
import sys
import os
sys.path.append('/home/runner/work/digitalzia/digitalzia')

from models.resume_ranker import ResumeRanker


def print_banner():
    """Print application banner"""
    print("=" * 60)
    print("🎯 RESUME RANKER AI - HR RECRUITMENT TOOL")
    print("=" * 60)
    print("AI-Powered 5-Factor Resume Analysis System")
    print()


def get_job_requirements():
    """Get job requirements from user input"""
    print("📋 JOB REQUIREMENTS SETUP")
    print("-" * 30)
    
    job_title = input("Enter Job Title: ").strip()
    print()
    
    print("Enter Required Skills (comma-separated):")
    print("Example: Python, Machine Learning, SQL, Data Analysis")
    skills_input = input("Skills: ").strip()
    skills = [skill.strip() for skill in skills_input.split(',') if skill.strip()]
    print()
    
    print("Enter Job Keywords (comma-separated):")
    print("Example: software development, programming, analytics")
    keywords_input = input("Keywords: ").strip()
    keywords = [keyword.strip() for keyword in keywords_input.split(',') if keyword.strip()]
    
    return {
        'title': job_title,
        'skills': skills,
        'keywords': keywords
    }


def get_resume_text():
    """Get resume text from user input"""
    print("\n📄 RESUME INPUT")
    print("-" * 20)
    print("Enter the candidate's resume text (press Enter twice when done):")
    print()
    
    lines = []
    while True:
        line = input()
        if line.strip() == "" and len(lines) > 0 and lines[-1].strip() == "":
            break
        lines.append(line)
    
    return '\n'.join(lines)


def display_results(result, job_info):
    """Display ranking results in a formatted way"""
    print("\n" + "=" * 60)
    print("📊 RESUME RANKING RESULTS")
    print("=" * 60)
    
    print(f"Job Position: {job_info['title']}")
    print()
    
    # Final Score and Classification
    score = result['final_score']
    classification = result['classification']
    
    print(f"🎯 FINAL SCORE: {score}/100")
    print(f"📈 CLASSIFICATION: {classification}")
    
    # Determine classification emoji
    if "Perfect" in classification:
        emoji = "🌟"
        color = "PERFECT"
    elif "Outstanding" in classification:
        emoji = "⭐"
        color = "OUTSTANDING"
    elif "Up to the mark" in classification:
        emoji = "👍"
        color = "ADEQUATE"
    else:
        emoji = "👌"
        color = "GOOD"
    
    print(f"{emoji} Status: {color}")
    print()
    
    # Factor Breakdown
    print("📋 DETAILED FACTOR ANALYSIS")
    print("-" * 40)
    
    factors = result['factor_scores']
    weights = result['weights_used']
    
    factor_names = {
        'skills_match': 'Skills Match',
        'experience_relevance': 'Experience Relevance',
        'education_background': 'Education Background',
        'achievements_certifications': 'Achievements & Certifications',
        'communication_quality': 'Communication Quality'
    }
    
    for factor_key, score in factors.items():
        factor_name = factor_names.get(factor_key, factor_key)
        weight_key = factor_key.split('_')[0] if '_' in factor_key else factor_key
        weight = weights.get(weight_key, 0) * 100
        
        # Create a simple progress bar
        bar_length = 20
        filled_length = int(bar_length * score / 100)
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        
        print(f"{factor_name:<25} {score:>6.1f}/100 [{bar}] ({weight:>2.0f}%)")
    
    print()
    
    # Scoring breakdown
    print("💡 SCORING BREAKDOWN")
    print("-" * 25)
    for factor_key, score in factors.items():
        factor_name = factor_names.get(factor_key, factor_key)
        weight_key = factor_key.split('_')[0] if '_' in factor_key else factor_key
        if weight_key == 'achievements':
            weight_key = 'achievements'
        elif weight_key == 'communication':
            weight_key = 'communication'
        weight = weights.get(weight_key, 0)
        contribution = score * weight
        print(f"{factor_name:<25} {score:>6.1f} × {weight:>4.1f} = {contribution:>6.2f}")
    
    print("-" * 50)
    print(f"{'TOTAL WEIGHTED SCORE':<25} {'':>15} = {score:>6.2f}")


def run_demo():
    """Run the interactive demo"""
    print_banner()
    
    ranker = ResumeRanker()
    
    # Get job requirements
    job_info = get_job_requirements()
    job_requirements = {
        'skills': job_info['skills'],
        'keywords': job_info['keywords']
    }
    
    # Get resume text
    resume_text = get_resume_text()
    
    if not resume_text.strip():
        print("❌ No resume text provided. Exiting.")
        return
    
    # Perform ranking
    print("\n🔄 Analyzing resume...")
    result = ranker.rank_resume(resume_text, job_requirements)
    
    # Display results
    display_results(result, job_info)
    
    print("\n" + "=" * 60)
    print("✅ Analysis Complete!")
    print("Thank you for using Resume Ranker AI! 🎯")
    print("=" * 60)


def run_sample_demo():
    """Run a demo with sample data"""
    print_banner()
    print("🔬 SAMPLE DEMO MODE")
    print("Running analysis with sample data...\n")
    
    ranker = ResumeRanker()
    
    # Sample job requirements
    job_info = {
        'title': 'Senior Data Scientist',
        'skills': ['Python', 'Machine Learning', 'SQL', 'Data Analysis', 'Statistics'],
        'keywords': ['data science', 'analytics', 'machine learning', 'research', 'modeling']
    }
    
    job_requirements = {
        'skills': job_info['skills'],
        'keywords': job_info['keywords']
    }
    
    # Sample resume
    sample_resume = """
    Sarah Johnson
    Senior Data Scientist with 6 years of experience
    
    EDUCATION:
    - PhD in Statistics from Stanford University (2018)
    - Master of Science in Computer Science from MIT (2015)
    - Bachelor of Mathematics from UC Berkeley (2013)
    
    TECHNICAL SKILLS:
    - Advanced Python programming and data analysis
    - Machine Learning: supervised and unsupervised learning
    - SQL database management and optimization
    - Statistical modeling and hypothesis testing
    - Deep learning frameworks: TensorFlow, PyTorch
    - Data visualization: matplotlib, seaborn, plotly
    - Big data technologies: Spark, Hadoop
    
    PROFESSIONAL EXPERIENCE:
    Data Scientist at Google (2020-Present)
    - Led machine learning initiatives that improved ad targeting by 25%
    - Developed predictive models for user behavior analysis
    - Collaborated with cross-functional teams on data-driven product decisions
    - Mentored junior data scientists and conducted technical interviews
    
    Senior Data Analyst at Facebook (2018-2020)
    - Implemented statistical models for user engagement optimization
    - Designed and executed A/B tests for product features
    - Created automated reporting dashboards using Python and SQL
    - Published research findings in internal technical conferences
    
    ACHIEVEMENTS & CERTIFICATIONS:
    - Certified Professional in Data Science (Google Cloud)
    - AWS Certified Machine Learning Specialist
    - Published 8 peer-reviewed papers in machine learning journals
    - Winner of "Innovation Excellence Award" at Google (2022)
    - Speaker at 5 international data science conferences
    - Led successful implementation of recommendation engine serving 100M+ users
    - Achieved 40% improvement in model accuracy through novel ensemble methods
    
    PROJECTS:
    - Developed fraud detection system reducing false positives by 60%
    - Created customer lifetime value prediction model with 95% accuracy
    - Built real-time analytics pipeline processing 1TB+ daily data
    """
    
    # Perform ranking
    result = ranker.rank_resume(sample_resume, job_requirements)
    
    # Display results
    display_results(result, job_info)
    
    print("\n" + "=" * 60)
    print("✅ Sample Demo Complete!")
    print("This demonstrates a high-scoring candidate profile. 🌟")
    print("=" * 60)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--sample":
        run_sample_demo()
    else:
        print("Choose demo mode:")
        print("1. Interactive Demo (enter your own data)")
        print("2. Sample Demo (pre-loaded example)")
        print()
        
        choice = input("Enter choice (1 or 2): ").strip()
        
        if choice == "2":
            run_sample_demo()
        else:
            run_demo()