import * as functions from "firebase-functions";
import fetch from "cross-fetch";
export const solve = functions.https.onRequest(async (req, res) => {
    res.set("Access-Control-Allow-Origin", "*");
    res.set("Access-Control-Allow-Headers", "Content-Type");
    if (req.method === "OPTIONS") {
        res.status(204).send("");
        return;
    }
    try {
        const body = typeof req.body === "string" ? JSON.parse(req.body) : req.body;
        const { bot, task } = body || {};
        if (!bot || !task) {
            res.status(400).json({ error: "bot and task required" });
            return;
        }
        const runUrl = functions.config()?.run?.url || process.env.RUN_URL || "http://localhost:8080";
        const r = await fetch(`${runUrl}/solve`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ bot, task })
        });
        if (!r.ok)
            throw new Error(`HTTP ${r.status}`);
        const result = await r.json();
        res.json(result);
    }
    catch (err) {
        console.error("solve error:", err);
        res.status(500).json({ error: err.message || "internal error" });
    }
});
