StudyFlowX 

StudyFlowX is an AI-powered Telegram bot developed in Python to assist students with studying and academic management.
The bot provides multiple educational tools including quiz generation, GPA calculation, note management, reminders, translation, and OCR-based text extraction from images.
This project was created as a final Python course project and demonstrates the use of Object-Oriented Programming (OOP), APIs, file handling, databases, exception handling, and modular programming.

Main Features
 🧠 AI Quiz Generator
1.	Automatically generates quizzes from study materials
2.	Supports both text input and image-based notes
3.	Uses OCR to extract text from screenshots and study images
4.	Multiple-choice questions with automatic scoring
5.	Final feedback and quiz performance review

 📝 Notes System
1.	Save personal notes
2.	View stored notes
3.	Delete unnecessary notes

Reminder System
1.	Create study reminders
2.	Helps students manage schedules and deadlines

📊 GPA Calculator
1.	Calculate GPA quickly
2.	Simple and interactive calculator

🌐 Translation System
1.	Translate text into different languages
2.	Useful for multilingual students

🖼️ OCR Image Processing
1.	Extracts text from lecture screenshots and textbook images
2.	Built using Tesseract OCR


 Technologies Used

a.	Python
b.	PyTelegramBotAPI (Telebot)
c.	SQLite
d.	JSON
e.	Tesseract OCR
f.	Groq AI API
g.	PIL (Python Imaging Library)


OOP Concepts Used

1.	This project demonstrates several Object-Oriented Programming concepts:

a.	Classes and objects
b.	Modular programming
c.	Functions and reusable modules
d.	Exception handling
e.	File handling using JSON
f.	External API integration


Project Structure

1.	main.py                  Main Telegram bot
2.	quiz_system.py           Quiz generation system
3.	database.py              Database management
4.	gpa_system.py           GPA calculator
5.	translation_system.py    Translation feature
6.	image_system.py          OCR image processing
7.	admin_system.py         Admin controls
8.	memory.json                JSON storage


How The System Works

1. User starts the Telegram bot
2. User selects a feature from the menu
3. For quizzes:
a.	User sends study material
b.	OCR extracts text from images if needed
c.	AI generates quiz questions
d.	User answers questions directly inside Telegram
e.	Bot calculates score and displays final feedback

 Installation Guide

 Clone Repository

```bash
git clone https://github.com/hamidniazi1513-lang/StudyFlowX.git
```

Install Required Libraries

```bash
pip install -r requirements.txt
```

 Install Tesseract OCR

Download and install Tesseract OCR for your operating system.

Windows example path:

```bash
C:\Program Files\Tesseract-OCR\tesseract.exe
```

---

Running The Project

Run the bot using:

```bash
python main.py 

After running the program, open Telegram and interact with the bot.



Screenshots

1.	Main menu
2.	Quiz generation
3.	GPA calculator
4.	Notes system
5.	Reminder feature

         


Challenges Faced

a.	Integrating OCR with Telegram bot workflow
b.	Handling quiz generation formatting
c.	Managing multiple bot handlers correctly
d.	Improving quiz feedback system
e.	Organizing the project into separate modules


 Future Improvements

o	Voice-to-text support
o	PDF quiz generation
o	Better UI design
o	Cloud deployment
o	Web dashboard version


Team Member 

 Hamid Niazi SE-2519
Mehdi Rezaie SE-2520


 Conclusion

StudyFlowX is a student-focused Telegram assistant that combines AI tools and automation to improve learning and productivity. The project demonstrates practical Python development skills including APIs, databases, OCR, modular programming, and Telegram bot development.
