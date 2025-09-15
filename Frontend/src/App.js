import React, { useState, useEffect } from "react";
import axios from "axios";
import "./index.css";

const BACKEND =
    process.env.NODE_ENV === "production"
        ? "https://aimockinterviwer-excelrelated.onrender.com"
        : "http://127.0.0.1:8000";

function App() {
    const [sessionId, setSessionId] = useState(null);
    const [messages, setMessages] = useState([]);
    const [answer, setAnswer] = useState("");
    const [loading, setLoading] = useState(false);

    // Typing effect
    const addMessageWithTyping = (from, text, isSummary = false) => {
        if (isSummary) {
            setMessages((prev) => [...prev, { from, isSummary: true, summary: text }]);
            return;
        }

        let i = 0;
        let currentText = "";
        setMessages((prev) => [...prev, { from, text: "" }]);

        const interval = setInterval(() => {
            currentText += text.charAt(i);
            setMessages((prev) => {
                const updated = [...prev];
                updated[updated.length - 1].text = currentText;
                return updated;
            });
            i++;
            if (i >= text.length) clearInterval(interval);
        }, 30);
    };

    // Start interview
    useEffect(() => {
        const fetchStart = async () => {
            setLoading(true);
            const res = await axios.post(`${BACKEND}/start`);
            const sid = res.data.session_id;
            setSessionId(sid);

            addMessageWithTyping("AI", res.data.question);
            setLoading(false);
        };
        fetchStart();
    }, []);

    const handleSubmit = async () => {
        if (!answer.trim()) return;

        setMessages((prev) => [...prev, { from: "You", text: answer }]);
        setAnswer("");
        setLoading(true);

        const res = await axios.post(`${BACKEND}/answer`, {
            session_id: sessionId,
            answer,
        });
        setLoading(false);

        if (res.data.next_question) {
            addMessageWithTyping("AI", res.data.next_question);
        } else if (res.data.message) {
            addMessageWithTyping("AI", res.data.message);
        }
    };

    const fetchSummary = async () => {
        if (!sessionId) return;
        setLoading(true);
        const res = await axios.get(`${BACKEND}/summary`, {
            params: { session_id: sessionId },
        });
        setLoading(false);

        addMessageWithTyping("AI", res.data.summary, true);
    };

    return (
        <div className="chat">
            <h1>AI Excel Mock Interviewer</h1>

            <div className="messages">
                {messages.map((msg, i) =>
                    msg.isSummary ? (
                        <div key={i} className="message-bot summary-box">
                            <b>?? Performance Summary</b>
                            <p>{msg.summary}</p>
                        </div>
                    ) : (
                        <div
                            key={i}
                            className={msg.from === "AI" ? "message-bot" : "message-user"}
                        >
                            <b>{msg.from}:</b>
                            <div className="msg-text">{msg.text}</div>
                        </div>
                    )
                )}
                {loading && (
                    <div className="message-bot typing-indicator">
                        <b>AI:</b>
                        <span className="dot"></span>
                        <span className="dot"></span>
                        <span className="dot"></span>
                    </div>
                )}
            </div>

            {/* ? Controls always visible */}
            <div className="controls">
                <textarea
                    value={answer}
                    onChange={(e) => setAnswer(e.target.value)}
                    placeholder="Type your answer..."
                />
                <button onClick={handleSubmit}>Send</button>
            </div>

            <button onClick={fetchSummary} style={{ marginTop: "12px" }}>
                Get Performance Summary
            </button>
        </div>
    );
}

export default App;
