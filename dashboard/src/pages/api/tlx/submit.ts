import { NextApiRequest, NextApiResponse } from 'next';
import prisma from '../../../lib/prisma';

export default async function submit(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const { method } = req;

  switch (method) {
    case 'GET':
      return handleGET(req, res);
    default:
      return res.status(405).json({ error: 'Only GET methods are allowed.' });
  }
}

async function handleGET(req: NextApiRequest, res: NextApiResponse) {
  return res.json({ status: 'Balls' });
}
