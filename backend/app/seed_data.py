import json
from app.database import engine, Base, SessionLocal
from app.models import Helpline, Resource, Question

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Seed Helplines if empty
    if db.query(Helpline).count() == 0:
        helplines = [
            Helpline(
                name="Tele-MANAS (Govt. of India)",
                number="14416 / 1800-891-4416",
                category="24/7 Crisis Helpline",
                description="National tele-mental health helpline providing 24/7 confidential psychological support across all Indian states.",
                hours="24/7",
                is_toll_free=True,
                languages="English, Hindi, Regional Languages",
                website="https://telemanas.mohfw.gov.in"
            ),
            Helpline(
                name="KIRAN Mental Health Helpline",
                number="1800-599-0019",
                category="24/7 Crisis Helpline",
                description="Toll-free mental health rehabilitation helpline by the Ministry of Social Justice & Empowerment.",
                hours="24/7",
                is_toll_free=True,
                languages="English, Hindi, 13 Regional Languages",
                website="https://depwd.gov.in"
            ),
            Helpline(
                name="Vandrevala Foundation",
                number="+91 9999 666 555",
                category="Tele-Therapy & Counseling",
                description="Free 24x7 emotional support and mental health counseling by trained mental health professionals.",
                hours="24/7",
                is_toll_free=False,
                languages="English, Hindi, Gujarati, Marathi",
                website="https://www.vandrevalafoundation.com"
            ),
            Helpline(
                name="AASRA Crisis Center",
                number="+91 98204 66726",
                category="24/7 Crisis Helpline",
                description="A voluntary, non-professional and confidential crisis intervention service for individuals in distress.",
                hours="24/7",
                is_toll_free=False,
                languages="English, Hindi",
                website="http://www.aasra.info"
            ),
            Helpline(
                name="Student Wellness & Peer Support Line",
                number="1800-200-CAMPUS",
                category="Student Counseling",
                description="Dedicated academic & campus stress helpline offering empathetic peer listener support for university students.",
                hours="8:00 AM - 10:00 PM",
                is_toll_free=True,
                languages="English, Hindi",
                website="https://amicare.org/campus-support"
            )
        ]
        db.add_all(helplines)

    # Seed Questions if empty
    if db.query(Question).count() == 0:
        questions = [
            Question(
                order_num=1,
                prompt="In the last month, how often have you felt overwhelmed by academic deadlines or personal commitments?",
                is_reverse_scored=False,
                options_json=json.dumps([
                    {"label": "Never", "value": 0},
                    {"label": "Almost Never", "value": 1},
                    {"label": "Sometimes", "value": 2},
                    {"label": "Fairly Often", "value": 3},
                    {"label": "Very Often", "value": 4}
                ])
            ),
            Question(
                order_num=2,
                prompt="In the last month, how often have you felt unable to control the important things in your student life?",
                is_reverse_scored=False,
                options_json=json.dumps([
                    {"label": "Never", "value": 0},
                    {"label": "Almost Never", "value": 1},
                    {"label": "Sometimes", "value": 2},
                    {"label": "Fairly Often", "value": 3},
                    {"label": "Very Often", "value": 4}
                ])
            ),
            Question(
                order_num=3,
                prompt="In the last month, how often have you felt confident in your ability to handle personal or study problems?",
                is_reverse_scored=True,
                options_json=json.dumps([
                    {"label": "Very Often", "value": 0},
                    {"label": "Fairly Often", "value": 1},
                    {"label": "Sometimes", "value": 2},
                    {"label": "Almost Never", "value": 3},
                    {"label": "Never", "value": 4}
                ])
            ),
            Question(
                order_num=4,
                prompt="In the last month, how often have you felt that difficulties were piling up so high that you could not overcome them?",
                is_reverse_scored=False,
                options_json=json.dumps([
                    {"label": "Never", "value": 0},
                    {"label": "Almost Never", "value": 1},
                    {"label": "Sometimes", "value": 2},
                    {"label": "Fairly Often", "value": 3},
                    {"label": "Very Often", "value": 4}
                ])
            )
        ]
        db.add_all(questions)

    # Seed Resources if empty
    if db.query(Resource).count() == 0:
        resources = [
            Resource(
                title="Box Breathing (4-4-4-4 Technique)",
                category="Breathing",
                description="A simple 2-minute rhythmic breathing exercise used to calm the autonomic nervous system during acute exam stress.",
                action_type="interactive",
                read_time="2 min exercise",
                content="Inhale deeply for 4 seconds, hold your breath for 4 seconds, exhale slowly for 4 seconds, and hold empty for 4 seconds. Repeat 4 cycles."
            ),
            Resource(
                title="Managing Academic Burnout & Procrastination",
                category="Exam Stress",
                description="Practical strategies to dismantle overwhelming study loads using the Pomodoro technique and micro-tasking.",
                action_type="article",
                read_time="4 min read",
                content="When faced with a massive study syllabus, break tasks down into micro-sessions of 25 minutes focused work followed by 5 minutes of physical stretch."
            ),
            Resource(
                title="Sleep Hygiene for University Students",
                category="Sleep",
                description="Simple adjustments to your evening routine to improve sleep quality and reduce nighttime racing thoughts.",
                action_type="article",
                read_time="3 min read",
                content="Avoid bright screen exposure 30 minutes before bed. Keep your study area separated from your resting space where possible."
            ),
            Resource(
                title="Grounding Yourself: 5-4-3-2-1 Technique",
                category="Mindfulness",
                description="A proven sensory grounding technique to anchor your mind when experiencing anxiety or panic.",
                action_type="exercise",
                read_time="3 min exercise",
                content="Acknowledge 5 things you can see around you, 4 things you can touch, 3 things you can hear, 2 things you can smell, and 1 thing you can taste."
            )
        ]
        db.add_all(resources)

    db.commit()
    db.close()
    print("Database seeded successfully with helplines, resources, and assessment questions.")

if __name__ == "__main__":
    seed_database()
