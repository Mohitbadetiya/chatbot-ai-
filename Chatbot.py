# 💬 ChatBot with Memory
# Author: Rintaro 💫
# Description: A Python AI chatbot with memory and a simple GUI.

import tkinter as tk
from tkinter import scrolledtext
import json
import openai
import os

# ---------------------------
# ⚙️ Configuration
# ---------------------------
openai.api_key = "YOUR_OPENAI_API_KEY"  # Replace this with your API key

MEMORY_FILE = "chat_memory.json"

# ---------------------------
# 💾 Memory Functions
# ---------------------------
def load_memory():
    """Load previous chat history from memory file."""
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    else:
        return [{"role": "system", "content": "You are a friendly AI chatbot named Noelle created by Rintaro."}]


def save_memory(history):
    """Save current chat history to memory file."""
    with open(MEMORY_FILE, "w") as f:
        json.dump(history, f, indent=4)


# ---------------------------
# 🧠 AI Reply
# ---------------------------
def get_ai_reply(prompt):
    """Generate AI response using OpenAI API."""
    history.append({"role": "user", "content": prompt})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=history
        )
        reply = response.choices[0].message.content
        history.append({"role": "assistant", "content": reply})
        save_memory(history)
        return reply
    except Exception as e:
        print(e)
        return "⚠️ Sorry, I'm having trouble connecting to my brain right now."


# ---------------------------
# 💬 GUI Functions
# ---------------------------
def send_message():
    """Handle sending a user message."""
    user_input = entry.get()
    if user_input.strip() == "":
        return

    chat_window.config(state=tk.NORMAL)
    chat_window.insert(tk.END, f"You 🧍: {user_input}\n", "user")

    entry.delete(0, tk.END)

    reply = get_ai_reply(user_input)
    chat_window.insert(tk.END, f"Noelle 🩵: {reply}\n\n", "bot")

    chat_window.config(state=tk.DISABLED)
    chat_window.yview(tk.END)


def clear_memory():
    """Clear memory file and reset chat."""
    global history
    history = [{"role": "system", "content": "You are a friendly AI chatbot named Noelle created by Rintaro."}]
    save_memory(history)
    chat_window.config(state=tk.NORMAL)
    chat_window.delete(1.0, tk.END)
    chat_window.insert(tk.END, "🩵 Chat history cleared. Starting fresh!\n\n")
    chat_window.config(state=tk.DISABLED)


# ---------------------------
# 🖼️ GUI Design
# ---------------------------

# Create main window
root = tk.Tk()
root.title("Noelle ChatBot 💬")
root.geometry("500x600")
root.configure(bg="#E6E6FA")

# Title
title_label = tk.Label(root, text="Noelle ChatBot 💬", font=("Arial", 18, "bold"), bg="#E6E6FA", fg="#4B0082")
title_label.pack(pady=10)

# Chat window
chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=25, font=("Arial", 12))
chat_window.pack(padx=10, pady=10)
chat_window.config(state=tk.DISABLED)

# Input field
entry = tk.Entry(root, font=("Arial", 12))
entry.pack(padx=10, pady=10, fill=tk.X)

# Buttons
button_frame = tk.Frame(root, bg="#E6E6FA")
button_frame.pack(pady=5)

send_button = tk.Button(button_frame, text="Send", command=send_message, bg="#4B0082", fg="white", font=("Arial", 12, "bold"))
send_button.grid(row=0, column=0, padx=10)

clear_button = tk.Button(button_frame, text="Clear Memory", command=clear_memory, bg="#800080", fg="white", font=("Arial", 12, "bold"))
clear_button.grid(row=0, column=1, padx=10)

# Tag styles
chat_window.tag_config("user", foreground="#1E90FF")
chat_window.tag_config("bot", foreground="#800080")

# Load memory
history = load_memory()

# Welcome message
chat_window.config(state=tk.NORMAL)
chat_window.insert(tk.END, "🩵 Noelle: Hello! I’m Noelle, your AI friend. How are you feeling today?\n\n")
chat_window.config(state=tk.DISABLED)

# Run GUI
root.mainloop()
