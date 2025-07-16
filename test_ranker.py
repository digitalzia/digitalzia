#!/usr/bin/env python3
"""
Test script for Resume Ranker AI System By Zia
Validates all 5 factors and classification labels
"""
import sys
sys.path.append('/home/runner/work/digitalzia/digitalzia')

from models.resume_ranker import ResumeRanker


def test_classification_labels():
    """Test all classification label ranges"""
    ranker = ResumeRanker()
    
    test_scores = [45, 68, 82, 95]
    expected_labels = ["Good candidate", "Up to the mark", "Outstanding", "Perfect candidate"]
    
    print("🧪 Testing Classification Labels")
    print("-" * 40)
    
    for score, expected in zip(test_scores, expected_labels):
        actual = ranker.get_classification(score)
        status = "✅ PASS" if actual == expected else "❌ FAIL"
        print(f"Score {score:2d}: {actual:<20} {status}")
    print()


def test_skills_matching():
    """Test skills matching functionality"""
    ranker = ResumeRanker()
    
    print("🛠️ Testing Skills Matching")
    print("-" * 30)
    
    resume_text = "I have experience with Python, JavaScript, and SQL databases."
    required_skills = ["Python", "SQL", "Machine Learning", "Docker"]
    
    score = ranker.calculate_skills_match(resume_text, required_skills)
    expected = 50.0  # 2 out of 4 skills matched
    
    print(f"Resume: {resume_text}")
    print(f"Required: {required_skills}")
    print(f"Score: {score}% (Expected: {expected}%)")
    print(f"Status: {'✅ PASS' if abs(score - expected) < 0.1 else '❌ FAIL'}")
    print()


def test_experience_analysis():
    """Test experience relevance calculation"""
    ranker = ResumeRanker()
    
    print("💼 Testing Experience Analysis")
    print("-" * 35)
    
    resume_text = "Software engineer with 5 years of experience in web development and programming."
    keywords = ["programming", "software", "development"]
    
    score = ranker.calculate_experience_relevance(resume_text, keywords)
    
    print(f"Resume: {resume_text}")
    print(f"Keywords: {keywords}")
    print(f"Score: {score}%")
    print(f"Status: {'✅ PASS' if score > 50 else '❌ FAIL'}")
    print()


def test_education_scoring():
    """Test education background evaluation"""
    ranker = ResumeRanker()
    
    print("🎓 Testing Education Scoring")
    print("-" * 32)
    
    test_cases = [
        ("High school diploma", 20),
        ("Bachelor of Science degree", 60),
        ("Master of Engineering", 80),
        ("PhD in Computer Science", 100)
    ]
    
    for resume_text, min_expected in test_cases:
        score = ranker.calculate_education_score(resume_text)
        status = "✅ PASS" if score >= min_expected else "❌ FAIL"
        print(f"{resume_text:<25} Score: {score:5.1f}% {status}")
    print()


def test_achievements_detection():
    """Test achievements and certifications scoring"""
    ranker = ResumeRanker()
    
    print("🏆 Testing Achievements Detection")
    print("-" * 38)
    
    resume_text = """
    Certified AWS Solutions Architect with multiple achievements.
    Led successful project implementation that improved efficiency.
    Published research papers and received excellence award.
    """
    
    score = ranker.calculate_achievements_score(resume_text)
    
    print(f"Resume: {resume_text.strip()}")
    print(f"Score: {score}%")
    print(f"Status: {'✅ PASS' if score > 30 else '❌ FAIL'}")
    print()


def test_communication_quality():
    """Test communication and language quality assessment"""
    ranker = ResumeRanker()
    
    print("💬 Testing Communication Quality")
    print("-" * 36)
    
    test_cases = [
        ("Very short", 10),
        ("This is a well-structured professional resume with appropriate length and good vocabulary. The candidate demonstrates excellent communication skills through clear and concise presentation of their experience and qualifications.", 70)
    ]
    
    for resume_text, min_expected in test_cases:
        score = ranker.calculate_communication_score(resume_text)
        status = "✅ PASS" if score >= min_expected else "❌ FAIL"
        print(f"Text length: {len(resume_text):3d} chars, Score: {score:5.1f}% {status}")
    print()


def test_full_ranking():
    """Test complete resume ranking with all factors"""
    ranker = ResumeRanker()
    
    print("🎯 Testing Complete Resume Ranking")
    print("-" * 42)
    
    # Test data for different candidate types
    test_cases = [
        {
            'name': 'Junior Developer',
            'resume': """
            John Smith
            Junior Software Developer
            
            Education: Bachelor of Computer Science
            Skills: Python, HTML, CSS
            Experience: 1 year internship in web development
            """,
            'requirements': {
                'skills': ['Python', 'JavaScript', 'HTML', 'CSS'],
                'keywords': ['software development', 'programming']
            },
            'expected_range': (40, 70)
        },
        {
            'name': 'Senior Expert',
            'resume': """
            Dr. Jane Wilson
            Senior Data Scientist with PhD in Statistics
            
            Education: PhD Statistics, Master Computer Science
            Skills: Python, Machine Learning, Deep Learning, SQL, R
            Experience: 8 years leading data science teams
            Achievements: Published 15 papers, AWS certified, led award-winning projects
            """,
            'requirements': {
                'skills': ['Python', 'Machine Learning', 'SQL', 'Statistics'],
                'keywords': ['data science', 'analytics', 'research']
            },
            'expected_range': (85, 100)
        }
    ]
    
    for case in test_cases:
        result = ranker.rank_resume(case['resume'], case['requirements'])
        score = result['final_score']
        classification = result['classification']
        
        min_score, max_score = case['expected_range']
        status = "✅ PASS" if min_score <= score <= max_score else "❌ FAIL"
        
        print(f"{case['name']:<15} Score: {score:5.1f}% | {classification:<20} {status}")
    print()


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("🧪 RESUME RANKER AI - COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    print()
    
    test_classification_labels()
    test_skills_matching()
    test_experience_analysis()
    test_education_scoring()
    test_achievements_detection()
    test_communication_quality()
    test_full_ranking()
    
    print("=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
