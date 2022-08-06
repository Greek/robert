import { NextApiRequest, NextApiResponse } from 'next';
import { getToken } from 'next-auth/jwt';
import { getSession } from 'next-auth/react';
import prisma from '../../../../lib/prisma';

export default async function submit(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const { method } = req;

  const secret = process.env.NEXTAUTH_SECRET;
  const token = await getToken({ req, secret });

  if (!token)
    return res.status(401).json({ error: 'Please provide a valid token.' });

  switch (method) {
    case 'GET':
      return handleGET(req, res);
    default:
      return res.status(405).json({ error: 'Only GET methods are allowed.' });
  }
}

async function handleGET(req: NextApiRequest, res: NextApiResponse) {
  const result = await prisma.tLXReport.findUnique({
    where: {
      id: `${req.query.id}`,
    },
  });

  if (!result)
    return res.status(404).json({ error: 'This report could not be found.' });

  return res.status(200).json({
    result,
  });
}
