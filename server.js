// server.js
const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");

const app = express();
const PORT = 3000;

// Store messages in memory (can be changed to DB)
let messages = [];

app.use(cors());
app.use(bodyParser.json());
app.use(express.static("public")); // For serving HTML files

// Handle contact form submission
app.post("/api/contact", (req, res) => {
  const { name, email, message } = req.body;
  if (name && email && message) {
    messages.push({ name, email, message, date: new Date() });
    return res.status(200).json({ success: true });
  }
  res.status(400).json({ success: false, error: "Invalid input" });
});

// Get all messages
app.get("/api/messages", (req, res) => {
  res.json(messages);
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
