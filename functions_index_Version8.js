const functions = require("firebase-functions");
const { onRequest } = require("firebase-functions/v2/https");
const fetch = require("node-fetch");

const CLOUD_RUN_URL = process.env.CLOUD_RUN_URL || "https://omniscope-xxxx.a.run.app";

exports.api = onRequest(async (req, res) => {
  const url = `${CLOUD_RUN_URL}${req.url}`;
  const response = await fetch(url, {
    method: req.method,
    headers: req.headers,
    body: req.method !== "GET" ? req.body : undefined,
  });
  const data = await response.text();
  res.status(response.status).send(data);
});