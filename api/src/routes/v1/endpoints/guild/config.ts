import express, { Request, Response } from 'express';
import guildconfig from '../../../../models/guildconfig';
import consola from 'consola';

const config = express.Router();

// GET /v1/guild/:id/config
config.get('/:id/config', async (req: Request, res: Response) => {
  console.log(req.params.id);
  try {
    return res.status(501).send('Not implemented');
    const result = await guildconfig.findById({ id: '953134018071769169' });

    return res.status(200).json(result);
  } catch (e) {
    consola.error(e);
    return res.status(500).send('500 Internal Server Error');
  }
});

export default config;
