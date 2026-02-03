def calculate_match_percentage(user_profile, target_profile):
    score = 0
    max_score = 100
    
    if not user_profile or not target_profile:
        return 0

    # 1. Interest Matching (40%)
    user_interests = set(i.lower() for i in user_profile.interests)
    target_interests = set(i.lower() for i in target_profile.interests)
    
    if user_interests:
        common_interests = user_interests & target_interests
        interest_score = (len(common_interests) / len(user_interests)) * 40
        score += interest_score

    # 2. College Matching (20%)
    if user_profile.college and target_profile.college:
        if user_profile.college.lower() == target_profile.college.lower():
            score += 20
        # Check preferences if relevant
        # if user_profile.preferences.get('same_college') and ...

    # 3. Department Compatibility (15%) - Placeholder for now, simplistic check
    user_pref_depts = user_profile.preferences.get('departments', [])
    if target_profile.department in user_pref_depts:
        score += 15
    elif user_profile.department == target_profile.department:
        score += 15 # Boost for same dept if not specified

    # 4. Age Compatibility (15%)
    min_age = user_profile.preferences.get('min_age', 18)
    max_age = user_profile.preferences.get('max_age', 100)
    
    if min_age <= target_profile.age <= max_age:
        score += 15

    # 5. Activity/Completeness (10%)
    score += (target_profile.profile_completeness / 100) * 10
    
    return min(round(score, 2), 100)
