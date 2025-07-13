#!/usr/bin/env python3
"""
Multiple Resume Ranking Demo
Demonstrates ranking multiple candidates for the same position
"""
import sys
sys.path.append('/home/runner/work/digitalzia/digitalzia')

from models.resume_ranker import ResumeRanker


def main():
    print("=" * 70)
    print("🎯 MULTIPLE RESUME RANKING DEMO")
    print("=" * 70)
    print("Ranking 4 candidates for Senior Data Scientist position\n")
    
    ranker = ResumeRanker()
    
    # Job requirements
    job_requirements = {
        'skills': ['Python', 'Machine Learning', 'SQL', 'Data Analysis', 'Statistics'],
        'keywords': ['data science', 'analytics', 'machine learning', 'research', 'modeling']
    }
    
    # Sample resumes
    resumes = [
        {
            'filename': 'sarah_johnson.txt',
            'text': '''
            Sarah Johnson - Senior Data Scientist with 6 years of experience
            
            EDUCATION: PhD in Statistics from Stanford University, Master of Science in Computer Science from MIT
            
            SKILLS: Advanced Python programming, Machine Learning algorithms, SQL database management, 
            Statistical modeling, Deep learning frameworks (TensorFlow, PyTorch)
            
            EXPERIENCE: Data Scientist at Google (2020-Present) - Led machine learning initiatives, 
            improved ad targeting by 25%. Senior Data Analyst at Facebook (2018-2020) - Implemented 
            statistical models, designed A/B tests.
            
            ACHIEVEMENTS: Certified Professional in Data Science (Google Cloud), AWS Certified ML Specialist,
            Published 8 peer-reviewed papers, Winner of Innovation Excellence Award at Google (2022)
            '''
        },
        {
            'filename': 'mike_chen.txt', 
            'text': '''
            Mike Chen - Data Analyst with 3 years experience
            
            EDUCATION: Bachelor of Science in Mathematics from UC Berkeley
            
            SKILLS: Python programming, SQL queries, Data analysis, Basic machine learning, Excel
            
            EXPERIENCE: Data Analyst at startup (2021-Present) - Created reports and dashboards.
            Junior Analyst at consulting firm (2020-2021) - Performed data cleaning and analysis.
            
            ACHIEVEMENTS: Completed online machine learning course, Created automated reporting system
            '''
        },
        {
            'filename': 'dr_patel.txt',
            'text': '''
            Dr. Raj Patel - Research Scientist with 10 years experience
            
            EDUCATION: PhD in Computer Science from MIT, Master in Applied Mathematics from Caltech
            
            SKILLS: Python, R, Machine Learning, Deep Learning, Statistical Analysis, Research, 
            Data Science, Neural Networks, Natural Language Processing
            
            EXPERIENCE: Senior Research Scientist at Microsoft Research (2018-Present) - Led AI research team,
            published 20+ papers. Research Scientist at IBM Watson (2015-2018) - Developed ML algorithms.
            Postdoc at Stanford AI Lab (2013-2015) - Advanced machine learning research.
            
            ACHIEVEMENTS: 25 published papers in top AI conferences, 3 patents in machine learning,
            IEEE Fellow, Winner of Best Paper Award at NIPS, Keynote speaker at 10+ conferences
            '''
        },
        {
            'filename': 'lisa_wang.txt',
            'text': '''
            Lisa Wang - Junior Data Scientist
            
            EDUCATION: Bachelor in Computer Science from State University
            
            SKILLS: Python basics, SQL, Some machine learning knowledge
            
            EXPERIENCE: Intern at tech company (6 months) - Helped with data analysis projects
            
            ACHIEVEMENTS: Graduated with honors, Completed data science bootcamp
            '''
        }
    ]
    
    # Rank all resumes
    results = ranker.rank_multiple_resumes(resumes, job_requirements)
    
    # Display rankings
    print("📊 RANKING RESULTS (Highest to Lowest)")
    print("-" * 70)
    print(f"{'RANK':<5} {'CANDIDATE':<20} {'SCORE':<8} {'CLASSIFICATION':<20}")
    print("-" * 70)
    
    for i, result in enumerate(results, 1):
        filename = result['filename'].replace('.txt', '').replace('_', ' ').title()
        score = result['final_score']
        classification = result['classification']
        
        # Emoji based on classification
        if "Perfect" in classification:
            emoji = "🌟"
        elif "Outstanding" in classification:
            emoji = "⭐"
        elif "Up to the mark" in classification:
            emoji = "👍"
        else:
            emoji = "👌"
        
        print(f"{i:<5} {filename:<20} {score:<8.1f} {emoji} {classification}")
    
    print("-" * 70)
    
    # Detailed breakdown for top candidate
    if results:
        top_candidate = results[0]
        print(f"\n🏆 TOP CANDIDATE DETAILS: {top_candidate['filename'].replace('_', ' ').title()}")
        print("-" * 50)
        
        factors = top_candidate['factor_scores']
        for factor, score in factors.items():
            factor_name = factor.replace('_', ' ').title()
            print(f"{factor_name:<25} {score:>6.1f}/100")
    
    print("\n" + "=" * 70)
    print("✅ Multiple resume ranking complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()