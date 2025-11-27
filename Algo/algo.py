import sys, json, random, datetime, openai
import mysql.connector
import pygame
from pygame.locals import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

# -------- GPT-4 API Key --------
openai.api_key = "your_openai_api_key"  # Replace with your GPT-4 key

# -------- Database Connection --------
def db_conn():
    return mysql.connector.connect(
        host="localhost", user="root", password="your_password", database="algoforge"
    )

# -------- AI GPT Correction --------
def ai_correct_code_gpt(code):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You're a Python code reviewer."},
                {"role": "user", "content": f"Please review and suggest improvements:\n{code}"}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"GPT-4 error: {e}"

# -------- Save Code Version --------
def save_code_version(user, code):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO versions (username, code, saved_at) VALUES (%s, %s, %s)",
                (user, code, datetime.datetime.now()))
    conn.commit()
    conn.close()

# -------- Load Version History --------
def get_code_versions(user):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("SELECT saved_at, code FROM versions WHERE username=%s ORDER BY saved_at DESC", (user,))
    versions = cur.fetchall()
    conn.close()
    return versions

# -------- Leaderboard --------
def fetch_leaderboard():
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("SELECT username, score FROM users ORDER BY score DESC LIMIT 5")
    data = cur.fetchall()
    conn.close()
    return "\n".join([f"{u}: {s} points" for u, s in data])

# -------- Problem of the Day --------
PROBLEMS = [
    ("Reverse Array", "Reverse an array without using built-in reverse."),
    ("Binary Tree Height", "Compute the height of a binary tree."),
    ("Check Prime", "Write a function to check if a number is prime.")
]
CURRENT_PROBLEM = random.choice(PROBLEMS)

# -------- AI Hint --------
def get_problem_hint(desc):
    try:
        res = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You're a DSA tutor."},
                {"role": "user", "content": f"Give hint only for: {desc}"}
            ]
        )
        return res.choices[0].message.content.strip()
    except:
        return "Hint not available."

# -------- 3D Tree Visualizer --------
def draw_3d_tree_custom():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Dynamic 3D Tree")
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.SysFont(None, 24)

    nodes = [(300, 100, "A"), (200, 200, "B"), (400, 200, "C"),
             (150, 300, "D"), (250, 300, "E")]

    while running:
        screen.fill((255, 255, 255))
        for i, (x, y, val) in enumerate(nodes):
            pygame.draw.circle(screen, (0, 100, 200), (x, y), 30)
            img = font.render(val, True, (255, 255, 255))
            screen.blit(img, (x - 10, y - 10))
            if i == 0:
                pygame.draw.line(screen, (0, 0, 0), (x, y+30), (200, 200-30), 2)
                pygame.draw.line(screen, (0, 0, 0), (x, y+30), (400, 200-30), 2)
            elif i in [1, 2]:
                pygame.draw.line(screen, (0, 0, 0), (x, y+30), (x-50, y+70), 2)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()

# -------- Main App --------
class AlgoForge(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AlgoForge - AI + DSA + 3D")
        self.setGeometry(100, 100, 1000, 750)
        self.user = None

        self.login_input = QLineEdit()
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.editor = QTextEdit()
        self.output = QLabel("Output")
        self.lang_switch = QComboBox()
        self.lang_switch.addItems(["Python", "Java", "C++"])

        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.login_user)
        run_btn = QPushButton("Run")
        run_btn.clicked.connect(self.run_code)
        ai_btn = QPushButton("AI Review")
        ai_btn.clicked.connect(self.use_ai)
        save_btn = QPushButton("Save Version")
        save_btn.clicked.connect(self.save_version)
        view_versions = QPushButton("View Versions")
        view_versions.clicked.connect(self.show_versions)
        draw_btn = QPushButton("3D Tree")
        draw_btn.clicked.connect(draw_3d_tree_custom)
        leader_btn = QPushButton("Leaderboard")
        leader_btn.clicked.connect(self.show_leaderboard)
        problem_btn = QPushButton("Problem of the Day")
        problem_btn.clicked.connect(self.show_problem)
        submit_btn = QPushButton("Submit Solution")
        submit_btn.clicked.connect(self.submit_solution)
        hint_btn = QPushButton("Get Hint")
        hint_btn.clicked.connect(self.show_hint)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.login_input)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.pass_input)
        layout.addWidget(login_btn)
        layout.addWidget(QLabel("Language:"))
        layout.addWidget(self.lang_switch)
        layout.addWidget(QLabel("Editor:"))
        layout.addWidget(self.editor)
        layout.addWidget(run_btn)
        layout.addWidget(ai_btn)
        layout.addWidget(save_btn)
        layout.addWidget(view_versions)
        layout.addWidget(draw_btn)
        layout.addWidget(problem_btn)
        layout.addWidget(hint_btn)
        layout.addWidget(submit_btn)
        layout.addWidget(leader_btn)
        layout.addWidget(QLabel("Output:"))
        layout.addWidget(self.output)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def login_user(self):
        u, p = self.login_input.text(), self.pass_input.text()
        conn = db_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (u, p))
        if cur.fetchone():
            self.user = u
            self.output.setText(f"Welcome, {u}!")
        else:
            self.output.setText("Invalid credentials.")
        conn.close()

    def run_code(self):
        if self.lang_switch.currentText() != "Python":
            self.output.setText("Only Python code can be run.")
            return
        try:
            exec(self.editor.toPlainText(), {})
            self.output.setText("Code executed successfully.")
        except Exception as e:
            self.output.setText(str(e))

    def use_ai(self):
        result = ai_correct_code_gpt(self.editor.toPlainText())
        QMessageBox.information(self, "AI Feedback", result)

    def save_version(self):
        if not self.user:
            self.output.setText("Login first.")
            return
        save_code_version(self.user, self.editor.toPlainText())
        self.output.setText("Code version saved.")

    def show_versions(self):
        if not self.user:
            self.output.setText("Login first.")
            return
        versions = get_code_versions(self.user)
        msg = "\n\n".join([f"{dt}\n{code[:100]}..." for dt, code in versions])
        QMessageBox.information(self, "Versions", msg)

    def show_leaderboard(self):
        board = fetch_leaderboard()
        QMessageBox.information(self, "Leaderboard", board)

    def show_problem(self):
        title, desc = CURRENT_PROBLEM
        QMessageBox.information(self, title, desc)

    def submit_solution(self):
        if self.user:
            conn = db_conn()
            cur = conn.cursor()
            cur.execute("UPDATE users SET score = score + 10 WHERE username=%s", (self.user,))
            conn.commit()
            conn.close()
            self.output.setText("✅ Solution submitted. +10 XP")
        else:
            self.output.setText("Login to submit solution.")

    def show_hint(self):
        title, desc = CURRENT_PROBLEM
        hint = get_problem_hint(desc)
        QMessageBox.information(self, "Hint", hint)

# -------- Run App --------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = AlgoForge()
    win.show()
    sys.exit(app.exec_())
