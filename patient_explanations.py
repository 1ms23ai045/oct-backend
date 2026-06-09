# patient_explanations.py
# Patient-friendly explanations for common people

PATIENT_EXPLANATIONS = {
    'CNV': {
        'what_is_it': 'Your eye scan shows abnormal blood vessels growing beneath your retina. This is like having extra, leaky pipes under the light-sensitive layer of your eye.',
        'meaning_for_you': 'This can cause your central vision to become blurry or distorted. Straight lines may appear wavy, and you might see dark spots.',
        'urgency': 'HIGH - Needs immediate medical attention',
        'action_steps': [
            '📅 Schedule an appointment with an eye specialist TODAY',
            '📞 Call your eye doctor immediately',
            '📋 Keep a record of any vision changes',
            '🚗 Do not drive if vision is significantly affected'
        ],
        'treatments': [
            '💉 Anti-VEGF injections (most common)',
            '🔬 Photodynamic therapy',
            '👁️ Laser surgery (in some cases)'
        ],
        'lifestyle_tips': [
            '🥗 Eat leafy greens and colorful vegetables',
            '🚭 Quit smoking',
            '🩸 Control blood pressure',
            '👓 Use magnifying devices for reading'
        ],
        'dietary_recommendations': [
            '🥬 Kale, spinach, collard greens',
            '🐟 Fish high in omega-3 (salmon, tuna)',
            '🍊 Citrus fruits (oranges, grapefruits)',
            '🥚 Eggs (especially the yolk)'
        ],
        'follow_up': 'Your doctor will likely want to see you every 4-6 weeks initially',
        'questions_for_doctor': [
            'What stage of AMD do I have?',
            'How often will I need injections?',
            'Are there any side effects of the medication?',
            'Can I continue driving?'
        ]
    },
    
    'DME': {
        'what_is_it': 'Your eye scan shows fluid buildup in the macula, the central part of your retina that helps you see fine details. This is caused by diabetes affecting your eye blood vessels.',
        'meaning_for_you': 'Your central vision may become blurry, making it hard to read, recognize faces, or drive. Colors might look faded.',
        'urgency': 'HIGH - Needs attention within 2 weeks',
        'action_steps': [
            '🩸 Check your blood sugar levels immediately',
            '👨‍⚕️ Schedule an appointment with your eye doctor',
            '💊 Review your diabetes medications with your primary care doctor',
            '📋 Track any vision changes daily'
        ],
        'treatments': [
            '💉 Anti-VEGF injections (first line treatment)',
            '💊 Steroid implants',
            '🔬 Laser therapy (focal/grid laser)',
            '🩸 Better blood sugar control'
        ],
        'lifestyle_tips': [
            '🍬 Strictly control blood sugar levels',
            '🏃 Exercise regularly (30 minutes daily)',
            '🍎 Follow a diabetes-friendly diet',
            '💧 Stay hydrated'
        ],
        'dietary_recommendations': [
            '🥦 Low glycemic index foods',
            '🍠 Whole grains instead of refined carbs',
            '🥩 Lean proteins',
            '🥑 Healthy fats (avocado, nuts)'
        ],
        'follow_up': 'Your eye doctor will want to see you every 4-8 weeks during active treatment',
        'questions_for_doctor': [
            'Is my current diabetes treatment working?',
            'How many treatments will I need?',
            'Will my vision return to normal?',
            'Should I see a diabetes specialist?'
        ]
    },
    
    'DRUSEN': {
        'what_is_it': 'Your eye scan shows small yellow deposits under your retina. Think of them like age spots on your skin, but inside your eye. They are early warning signs.',
        'meaning_for_you': 'You have early signs of age-related eye changes. Your vision is likely normal now, but you need regular monitoring.',
        'urgency': 'MEDIUM - Schedule appointment within 1-3 months',
        'action_steps': [
            '📅 Schedule annual comprehensive eye exams',
            '👓 Use an Amsler grid to monitor vision at home',
            '📋 Note any vision changes in a diary',
            '🥗 Start taking eye-healthy supplements'
        ],
        'treatments': [
            '💊 AREDS2 supplements (vitamins for eye health)',
            '👁️ No treatment needed for early drusen',
            '🔬 Monitoring only'
        ],
        'lifestyle_tips': [
            '🥬 Eat dark leafy greens daily',
            '😎 Wear sunglasses outdoors',
            '🚭 Quit smoking (very important!)',
            '💪 Maintain healthy blood pressure'
        ],
        'dietary_recommendations': [
            '🥬 Kale, spinach, collard greens',
            '🌽 Corn and yellow vegetables',
            '🍊 Orange fruits (oranges, mangoes, papaya)',
            '🐟 Fish twice a week'
        ],
        'follow_up': 'Your eye doctor will want to see you once a year, or more often if drusen increase',
        'questions_for_doctor': [
            'Should I take AREDS2 supplements?',
            'How often should I come for check-ups?',
            'What changes should I watch for?',
            'Is there anything that can reverse drusen?'
        ]
    },
    
    'NORMAL': {
        'what_is_it': 'Your eye scan shows a healthy retina with no signs of disease. The layers of your retina are normal and there is no fluid or abnormal deposits.',
        'meaning_for_you': 'Your eyes are healthy! Keep up with regular check-ups to maintain good vision.',
        'urgency': 'LOW - Routine follow-up only',
        'action_steps': [
            '📅 Schedule next annual eye exam',
            '👓 Get regular vision check-ups',
            '🥗 Maintain healthy lifestyle',
            '😎 Protect eyes from UV light'
        ],
        'treatments': [
            '✅ No treatment needed - Prevention is key!'
        ],
        'lifestyle_tips': [
            '🥬 Eat eye-healthy foods',
            '🕶️ Wear sunglasses outdoors',
            '📱 Take breaks from screens (20-20-20 rule)',
            '💪 Exercise regularly'
        ],
        'dietary_recommendations': [
            '🥕 Carrots, sweet potatoes (Vitamin A)',
            '🍊 Citrus fruits (Vitamin C)',
            '🥜 Nuts and seeds (Vitamin E)',
            '🐟 Fish (Omega-3 fatty acids)'
        ],
        'follow_up': 'Annual eye exams are recommended for everyone over 40',
        'questions_for_doctor': [
            'How often should I get my eyes checked?',
            'What vitamins are good for eye health?',
            'Does my family history put me at risk?'
        ]
    }
}

def get_patient_report(diagnosis, confidence):
    """Generate patient-friendly report"""
    info = PATIENT_EXPLANATIONS.get(diagnosis, PATIENT_EXPLANATIONS['NORMAL'])
    
    report = f"""
╔══════════════════════════════════════════════════════════════════╗
║                    YOUR EYE HEALTH REPORT                        ║
║                         (Easy-to-Understand)                      ║
╚══════════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 WHAT THE SCAN SHOWS:
{info['what_is_it']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 DIAGNOSIS SUMMARY:
   Condition: {diagnosis}
   Confidence: {confidence}%
   Urgency: {info['urgency']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 WHAT THIS MEANS FOR YOU:
{info['meaning_for_you']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ WHAT YOU SHOULD DO NEXT:

"""
    for i, step in enumerate(info['action_steps'], 1):
        report += f"   {i}. {step}\n"
    
    report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💊 TREATMENT OPTIONS:
"""
    for treatment in info['treatments']:
        report += f"   • {treatment}\n"
    
    report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🥗 LIFESTYLE & DIETARY RECOMMENDATIONS:

   EAT MORE:
   {', '.join(info['dietary_recommendations'])}

   HEALTHY HABITS:
"""
    for tip in info['lifestyle_tips']:
        report += f"   • {tip}\n"
    
    report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 FOLLOW-UP SCHEDULE:
   {info['follow_up']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❓ QUESTIONS TO ASK YOUR DOCTOR:
"""
    for question in info['questions_for_doctor']:
        report += f"   • {question}\n"
    
    report += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ IMPORTANT REMINDER:
This is an AI-assisted screening tool. Always consult with a qualified
ophthalmologist for proper diagnosis and treatment decisions.

📱 Need help? Call your eye doctor's office.

                  👁️ Take care of your vision! 👁️
"""
    
    return report