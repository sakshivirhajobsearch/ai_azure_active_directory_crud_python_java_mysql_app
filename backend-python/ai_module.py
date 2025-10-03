def predict_role_risk(user):
    job = user.get('jobTitle', '') or ''
    if 'Admin' in job or 'Administrator' in job:
        return "High Risk"
    return "Low Risk"

if __name__ == "__main__":
    print(predict_role_risk({'jobTitle': 'Security Admin'}))