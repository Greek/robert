import express from 'express';
const ping = express.Router();

// GET /v1/ping
ping.get('/', (req, res) => {
  res.send({
    message: 'Pong!',
  });
});

export default ping;
