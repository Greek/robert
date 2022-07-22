import express, { Request, Response } from 'express';

const teapot = express.Router();

// GET /v1/teapot
teapot.get('/', (req: Request, res: Response) => {
  return res.status(418).json({ hello: 'world', test: req.body.hi });
});

export default teapot;
