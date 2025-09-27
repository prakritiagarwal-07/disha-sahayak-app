import pandas as pd
import random

def generate_mock_data():
    """Generates mock internship data, now including education and stipend, and saves to CSV."""
    internship_data = {
        'internship_id': range(1, 51),
        'title': [
            "Data Entry Operator", "Social Media Marketing Intern", "Graphic Design Intern", "Content Writing Intern",
            "Web Development Intern (Frontend)", "HR Assistant Intern", "Market Research Analyst", "Agriculture Field Assistant",
            "Rural Development Project Intern", "Government Scheme Promoter", "IT Helpdesk Support", "Accounts Assistant",
            "Videography Intern", "Community Mobilizer", "Public Health Intern", "E-commerce Operations Intern",
            "Digital Marketing Intern", "Mobile App Development Intern", "Customer Service Intern", "Supply Chain Intern",
            "Data Analyst Intern", "Graphic Designer (UI/UX)", "Journalism Intern", "Renewable Energy Intern",
            "Teaching Assistant Intern", "Legal Research Intern", "Event Management Intern", "Photography Intern",
            "Mechanical Engineering Intern", "Civil Engineering Site Intern", "Financial Literacy Campaigner",
            "Content Creator (Video)", "Public Relations Intern", "Animal Husbandry Intern", "Lab Assistant (Science)",
            "Library Management Intern", "Tourism and Hospitality Intern", "Logistics Coordinator Intern",
            "Local Governance Intern", "CAD Designer Intern", "Nutrition and Dietetics Intern", "Social Work Intern",
            "Digital Illustrator", "Software Testing Intern", "SEO Analyst Intern", "Urban Planning Assistant",
            "AI/ML Project Intern", "Cybersecurity Intern", "Robotics Intern", "Content Translation Intern"
        ],
        'description': [ "Description for internship " + str(i) for i in range(1, 51) ], # Simplified for brevity
        'education_required': [
            "12th Pass", "Graduate", "Graduate", "Graduate", "Graduate", "Graduate", "Post Graduate", "12th Pass",
            "Graduate", "12th Pass", "Graduate", "Graduate", "12th Pass", "12th Pass", "Graduate", "Graduate",
            "Graduate", "Graduate", "12th Pass", "Graduate", "Post Graduate", "Graduate", "Graduate", "Graduate",
            "Graduate", "Graduate", "12th Pass", "12th Pass", "Graduate", "Graduate", "12th Pass", "Graduate",
            "Graduate", "12th Pass", "Graduate", "12th Pass", "12th Pass", "Graduate", "Graduate", "Graduate",
            "Graduate", "Graduate", "Graduate", "Graduate", "Graduate", "Graduate", "Post Graduate", "Post Graduate",
            "Graduate", "Graduate"
        ],
        'skills_required': [
            "MS Excel, Typing Speed, Attention to Detail", "Social Media Management, Content Creation, Communication",
            "Adobe Photoshop, Canva, Creativity", "Creative Writing, SEO, Research", "HTML, CSS, JavaScript",
            "MS Office, Communication, Organization", "Data Analysis, Research, MS Excel", "Agriculture, Communication",
            "Project Management, Community Engagement", "Public Speaking, Communication", "Troubleshooting, Customer Service",
            "Tally, Bookkeeping, MS Excel", "Video Editing, Adobe Premiere Pro", "Communication, Public Speaking",
            "Data Collection, MS Office", "MS Excel, E-commerce Platforms", "SEO, Google Ads, Social Media Marketing",
            "Java, Android Studio, XML", "Communication, Problem Solving", "Logistics, MS Excel",
            "Python, SQL, Data Visualization", "Figma, Adobe XD, UI/UX Design", "Writing, Research",
            "MS Office, Research", "Communication, Patience", "Legal Research, MS Word",
            "Organization, Communication", "Adobe Lightroom, Photography", "AutoCAD, SolidWorks",
            "Site Supervision, AutoCAD", "Communication, Finance", "Video Editing, Creativity",
            "Writing, Communication", "Veterinary Science, Animal Care", "MS Office, Attention to Detail",
            "Organization, MS Office", "Customer Service, Communication", "MS Excel, Organization",
            "Research, MS Office", "AutoCAD, Design", "Nutrition, Communication", "Empathy, Communication",
            "Adobe Illustrator, Digital Art", "Manual Testing, Bug Reporting", "SEO, Google Analytics",
            "AutoCAD, Research", "Python, TensorFlow, Scikit-learn", "Networking, Cybersecurity Basics",
            "C++, Arduino, Problem Solving", "Bilingual, Translation, Writing"
        ],
        'location_city': [
            "Jaipur", "Pune", "Bangalore", "Delhi", "Lucknow", "Bhopal", "Patna", "Udaipur", "Ranchi", "Bhubaneswar",
            "Hyderabad", "Mumbai", "Chennai", "Kolkata", "Ahmedabad", "Surat", "Nagpur", "Indore", "Thane", "Ghaziabad",
            "Ludhiana", "Agra", "Nashik", "Faridabad", "Meerut", "Rajkot", "Varanasi", "Srinagar", "Aurangabad", "Dhanbad",
            "Amritsar", "Allahabad", "Jodhpur", "Raipur", "Coimbatore", "Guwahati", "Chandigarh", "Mysore", "Gurgaon",
            "Noida", "Shimla", "Dehradun", "Visakhapatnam", "Kochi", "Thiruvananthapuram", "Kota", "Bhilwara", "Ajmer",
            "Alwar", "Sikar"
        ],
        'latitude': [26.9124, 18.5204, 12.9716, 28.7041, 26.8467, 23.2599, 25.5941, 24.5854, 23.3441, 20.2961, 17.3850, 19.0760, 13.0827, 22.5726, 23.0225, 21.1702, 21.1458, 22.7196, 19.2183, 28.6692, 30.9010, 27.1767, 20.0112, 28.4089, 28.9845, 22.3039, 25.3176, 34.0837, 19.8762, 23.7957, 31.6340, 25.4358, 26.2389, 21.2514, 11.0168, 26.1445, 30.7333, 12.2958, 28.4595, 28.5355, 31.1048, 30.3165, 17.6868, 9.9312, 8.5241, 25.18, 25.33, 26.44, 27.55, 27.53],
        'longitude': [75.7873, 73.8567, 77.5946, 77.1025, 80.9462, 77.4126, 85.1376, 73.7125, 85.3096, 85.8245, 78.4867, 72.8777, 80.2707, 88.3639, 72.5714, 72.8311, 79.0882, 75.8577, 72.9781, 77.4538, 75.8573, 78.0081, 73.7898, 77.3178, 77.6793, 70.7915, 82.9739, 74.7973, 75.3433, 86.4304, 74.8723, 81.8463, 73.0243, 81.6296, 76.9558, 91.7362, 76.7794, 76.6394, 77.0266, 77.3910, 77.1734, 78.0322, 83.2185, 76.2711, 76.9366, 75.83, 74.63, 75.08, 76.63, 75.13],
        'stipend': [ random.randint(50, 200) * 100 for _ in range(50) ]
    }
    internships_df = pd.DataFrame(internship_data)
    internships_df.to_csv('internships.csv', index=False)
    print("Successfully created internships.csv with 50 mock internships.")

if __name__ == '__main__':
    generate_mock_data()
