import tkinter as tk
from tkinter import messagebox, scrolledtext
import random
import textwrap
import sys

# ---------- Data generation ----------
senders_safe = [
    ("Nidhi Patel", "nidhi.p@company.com"),
    ("Amazon", "order-update@amazon.com"),
    ("HR Team", "hr@yourcompany.com"),
    ("Your Bank", "support@mybank.com"),
    ("LinkedIn", "messages@linkedin.com"),
    ("Saad Ashraf", "saad.ashraf.825@gmail.com"),
]

# Templates for phishing and safe emails
phish_templates = [
    {
        "subject": "Urgent: Confirm your account now",
        "body": "Dear {name},\n\nWe detected suspicious activity on your account. Please verify immediately by clicking the link below:\n\n{link}\n\nFailure to verify will lead to suspension.\n\nRegards,\nSecurity Team",
        "reason": "Urgent language + link to an external site (likely a spoofed URL)."
    },
    {
        "subject": "Invoice Attached - Overdue Payment",
        "body": "Hello {name},\n\nPlease find the attached invoice for the recent order. Pay now to avoid penalties.\n\nAttachment: invoice_{num}.zip\n\nThanks,\nAccounts",
        "reason": "Unexpected attachment (.zip) and pressure to pay — common phishing tactic."
    },
    {
        "subject": "Password Reset Request",
        "body": "Hi {name},\n\nWe received a password reset request. If this was not you, please reset your password here:\n\n{link}\n\nIf you ignore this email, your account may be compromised.",
        "reason": "Password reset links from unknown requests; phishing pages mimic real sites."
    },
    {
        "subject": "CEO: Transfer funds immediately",
        "body": "Hi {name},\n\nThis is urgent. Transfer $15,000 to the following vendor account now. Do not mention this to anyone.\n\nAccount: 123456789\n\nThanks,\n{ceo_name}",
        "reason": "CEO fraud / Business Email Compromise (urgent money transfer request)."
    },
    {
        "subject": "Unusual login from NEW device",
        "body": "Dear {name},\n\nWe noticed a login from a new device located in {city}. If this wasn't you, click here:\n\n{link}\n\nRegards,\nSecurity Team",
        "reason": "Suspicious location + link to verify; social engineering to create fear."
    },
    {
        "subject": "HR: Update your bank details for payroll",
        "body": "Hello {name},\n\nPlease update your bank details in the attached form so we can process your salary.\n\nAttachment: payroll_form.xls\n\nRegards,\nHR Team",
        "reason": "Unexpected attachment requesting sensitive data; HR-themed phishing."
    },
]

safe_templates = [
    {
        "subject": "Team Lunch Tomorrow - RSVP",
        "body": "Hey {name},\n\nWe're planning a team lunch tomorrow at 1pm. Please RSVP if you can join.\n\nThanks,\nOffice Admin",
        "reason": "Casual internal event invitation; no suspicious links or requests."
    },
    {
        "subject": "Monthly Newsletter - October",
        "body": "Dear {name},\n\nWelcome to our October newsletter. Read about recent updates and events.\n\nBest,\nCommunications",
        "reason": "Newsletter from a known sender; informational content."
    },
    {
        "subject": "Your order has shipped",
        "body": "Hi {name},\n\nGreat news — your order # {num} has been shipped. Track your package here: {link}\n\nRegards,\nE-commerce Team",
        "reason": "Shipping notification; often safe but check the domain of links. In this simulation it's safe."
    },
    {
        "subject": "Meeting Minutes from Yesterday",
        "body": "Hi {name},\n\nAttached are the minutes from yesterday's meeting. Let me know if you have edits.\n\nAttachment: minutes.pdf\n\nThanks,\nTeam Member",
        "reason": "Routine attachment (PDF) from colleague; typically safe in corporate context."
    },
]

cities = ["Berlin", "Mumbai", "New York", "Lagos", "Singapore", "Istanbul"]
ceo_names = ["Rahul Mehta", "Aisha Khan", "Liam O'Connor", "Chen Wei", "Fatima Alvi"]

def make_email(template, recipient_name):
    is_phish = template in phish_templates
    # pick variations
    link = "http://verify-secure.example.com/login" if is_phish else "https://www.example.com/track/{}".format(random.randint(1000,9999))
    num = random.randint(100,9999)
    city = random.choice(cities)
    ceo_name = random.choice(ceo_names)
    sender_name, sender_email = random.choice(senders_safe) if not is_phish else ("Support Team", "support@security-update.com")
    body = template["body"].format(name=recipient_name, link=link, num=num, city=city, ceo_name=ceo_name)
    return {
        "sender_name": sender_name,
        "sender_email": sender_email,
        "subject": template["subject"],
        "body": body,
        "is_phish": is_phish,
        "explanation": template["reason"]
    }

def generate_inbox(recipient_name="User", n=10):
    # mix safe and phishing: ensure a variety (approx 40-60 split randomized)
    emails = []
    templates_pool = phish_templates + safe_templates
    # Ensure at least 3 phishing and at least 3 safe to keep variety
    chosen = random.sample(phish_templates, k=3) + random.sample(safe_templates, k=3)
    # fill the rest randomly
    while len(chosen) < n:
        chosen.append(random.choice(templates_pool))
    random.shuffle(chosen)
    for t in chosen[:n]:
        emails.append(make_email(t, recipient_name))
    return emails

# ---------- GUI ----------
class SimulatorApp:
    def __init__(self, master):
        self.master = master
        master.title("Cybersecurity Awareness Simulator")
        master.geometry("900x600")

        self.player_name = "Player"
        self.total_questions = 10
        self.emails = generate_inbox(self.player_name, self.total_questions)
        self.current_index = 0
        self.answers = [None] * len(self.emails)  # True=Phish, False=Safe, None=unanswered

        # Left: Inbox list
        left_frame = tk.Frame(master)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=8, pady=8)

        tk.Label(left_frame, text="Inbox (Click to open)").pack(anchor="w")
        self.listbox = tk.Listbox(left_frame, width=40, height=25)
        self.listbox.pack(side=tk.TOP, fill=tk.Y)
        for i, e in enumerate(self.emails):
            preview = (e["subject"][:50] + ("..." if len(e["subject"])>50 else ""))
            tag = "[?]"  # unknown
            self.listbox.insert(tk.END, f"{i+1}. {preview} {tag}")
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        # Buttons to randomize / restart
        tk.Button(left_frame, text="New Inbox", command=self.new_inbox).pack(fill=tk.X, pady=(6,0))
        tk.Button(left_frame, text="Restart Game", command=self.restart).pack(fill=tk.X, pady=(6,0))

        # Right: Email view and actions
        right_frame = tk.Frame(master)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=8, pady=8)

        header_frame = tk.Frame(right_frame)
        header_frame.pack(fill=tk.X)
        self.subject_var = tk.StringVar()
        tk.Label(header_frame, textvariable=self.subject_var, font=("Helvetica", 14, "bold")).pack(anchor="w")
        self.sender_var = tk.StringVar()
        tk.Label(header_frame, textvariable=self.sender_var, font=("Helvetica", 10)).pack(anchor="w")

        self.body_text = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, height=18)
        self.body_text.pack(fill=tk.BOTH, expand=True)
        self.body_text.configure(state=tk.DISABLED)

        action_frame = tk.Frame(right_frame)
        action_frame.pack(fill=tk.X, pady=6)
        tk.Button(action_frame, text="Mark as PHISHING", command=lambda: self.mark(True)).pack(side=tk.LEFT, padx=6)
        tk.Button(action_frame, text="Mark as SAFE", command=lambda: self.mark(False)).pack(side=tk.LEFT, padx=6)
        tk.Button(action_frame, text="Skip", command=lambda: self.mark(None)).pack(side=tk.LEFT, padx=6)
        tk.Button(action_frame, text="Show Score", command=self.show_score).pack(side=tk.RIGHT, padx=6)

        # Footer: progress
        self.progress_var = tk.StringVar()
        tk.Label(master, textvariable=self.progress_var).pack(side=tk.BOTTOM, fill=tk.X)
        self.update_view(0)

    def update_listbox_tag(self, index):
        tag = "[?]"
        ans = self.answers[index]
        if ans is True:
            tag = "[P]"  # marked phishing
        elif ans is False:
            tag = "[S]"  # marked safe
        else:
            tag = "[?]"
        # update item
        preview = (self.emails[index]["subject"][:50] + ("..." if len(self.emails[index]["subject"])>50 else ""))
        self.listbox.delete(index)
        self.listbox.insert(index, f"{index+1}. {preview} {tag}")

    def on_select(self, event):
        if not self.listbox.curselection():
            return
        idx = self.listbox.curselection()[0]
        self.current_index = idx
        self.update_view(idx)

    def update_view(self, idx):
        e = self.emails[idx]
        self.subject_var.set(e["subject"])
        self.sender_var.set(f"From: {e['sender_name']} <{e['sender_email']}>")
        self.body_text.configure(state=tk.NORMAL)
        self.body_text.delete("1.0", tk.END)
        wrapped = textwrap.fill(e["body"], width=80)
        self.body_text.insert(tk.END, wrapped)
        # small tip: do not reveal if phishing
        self.body_text.configure(state=tk.DISABLED)
        self.progress_var.set(f"Email {idx+1} of {len(self.emails)} — Mark it Phishing or Safe.")

        # highlight list selection
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(idx)
        self.listbox.activate(idx)

    def mark(self, as_phish):
        # Record answer (True/False/None). None means skipped/unanswered for now.
        self.answers[self.current_index] = as_phish
        self.update_listbox_tag(self.current_index)
        # move to next unanswered email if available
        next_idx = None
        for i, a in enumerate(self.answers):
            if a is None:
                next_idx = i
                break
        if next_idx is None:
            # all answered (or skipped). Offer to show score
            self.show_score()
        else:
            self.current_index = next_idx
            self.update_view(next_idx)

    def score_and_report(self):
        correct = 0
        report = []
        for i, e in enumerate(self.emails):
            user_ans = self.answers[i]
            # interpret None as False (safe) only for scoring? Better to treat None as unanswered = incorrect
            if user_ans is None:
                is_correct = False
            else:
                is_correct = (user_ans == e["is_phish"])
            if is_correct:
                correct += 1
            report.append({
                "index": i+1,
                "subject": e["subject"],
                "sender": f"{e['sender_name']} <{e['sender_email']}>",
                "user_marked": "Phishing" if user_ans else ("Safe" if user_ans is False else "Unanswered"),
                "actual": "Phishing" if e["is_phish"] else "Safe",
                "correct": is_correct,
                "explanation": e["explanation"]
            })
        return correct, report

    def show_score(self):
        correct, report = self.score_and_report()
        total = len(self.emails)
        pct = int(correct/total * 100)
        msg = f"You scored {correct} / {total} ({pct}%)"
        # Show summary in new window with details
        detail_win = tk.Toplevel(self.master)
        detail_win.title("Results and Explanations")
        detail_win.geometry("800x500")
        tk.Label(detail_win, text=msg, font=("Helvetica", 14, "bold")).pack(anchor="w", padx=8, pady=8)
        # Explain common tips
        tips = (
            "Quick Tips:\n"
            "- Check sender address (spoofed domains often look similar).\n"
            "- Hover (or inspect) links before clicking — mismatched URLs are red flags.\n"
            "- Unexpected attachments (especially .zip, .exe) may contain malware.\n"
            "- Urgent threats, pressure to act quickly, or requests for money are common scams.\n"
            "- If in doubt, contact the sender via a known channel (not by replying to the email).\n"
        )
        tk.Label(detail_win, text=tips, justify=tk.LEFT).pack(anchor="w", padx=8)

        # Scrolling frame with per-email results
        container = scrolledtext.ScrolledText(detail_win, wrap=tk.WORD)
        container.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        for r in report:
            container.insert(tk.END, f"Email {r['index']}: {r['subject']}\n")
            container.insert(tk.END, f"  Sender: {r['sender']}\n")
            container.insert(tk.END, f"  You marked: {r['user_marked']}\n")
            container.insert(tk.END, f"  Actual: {r['actual']}\n")
            container.insert(tk.END, f"  Correct: {'Yes' if r['correct'] else 'No'}\n")
            container.insert(tk.END, f"  Why: {r['explanation']}\n\n")
        container.configure(state=tk.DISABLED)
        # Offer to restart
        tk.Button(detail_win, text="Play Again (New Inbox)", command=lambda: [detail_win.destroy(), self.new_inbox()]).pack(side=tk.LEFT, padx=8, pady=6)
        tk.Button(detail_win, text="Close", command=detail_win.destroy).pack(side=tk.RIGHT, padx=8, pady=6)

    def new_inbox(self):
        self.emails = generate_inbox(self.player_name, self.total_questions)
        self.answers = [None] * len(self.emails)
        self.listbox.delete(0, tk.END)
        for i, e in enumerate(self.emails):
            preview = (e["subject"][:50] + ("..." if len(e["subject"])>50 else ""))
            tag = "[?]"
            self.listbox.insert(tk.END, f"{i+1}. {preview} {tag}")
        self.current_index = 0
        self.update_view(0)

    def restart(self):
        if messagebox.askyesno("Restart", "Restart the simulator? Your current progress will be lost."):
            self.new_inbox()

def main():
    root = tk.Tk()
    app = SimulatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
