import express, { Request, Response } from 'express';
import config from './config';

const guild = express.Router();

guild.use('/', config);

// GET /v1/guild/:id
guild.get('/:id', (req: Request, res: Response) => {
  const { id } = req.params;

  return res.status(200).end(id);
});

export default guild;
