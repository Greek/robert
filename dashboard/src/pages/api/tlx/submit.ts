import { NextApiRequest, NextApiResponse } from 'next';
import { getToken } from 'next-auth/jwt';
import prisma from '../../../lib/prisma';

export default async function submit(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const { method } = req;

  const secret = process.env.NEXTAUTH_SECRET;
  const token = await getToken({ req, secret });

  if (!token)
    return res.status(401).json({ error: 'Please provide a valid token.' });

  // eslint-disable-next-line @typescript-eslint/ban-ts-comment
  // @ts-ignore
  if (!token.email?.valueOf == 'apapuig+discord@gmail.com')
    return res
      .status(403)
      .json({ error: 'You do not have access to this resource.' });

  switch (method) {
    case 'GET':
      return handleGET(req, res);
    case 'POST':
      return handlePOST(req, res);
    default:
      return res.status(405).json({ error: 'Only GET methods are allowed.' });
  }
}

async function handlePOST(req: NextApiRequest, res: NextApiResponse) {
  const result = await prisma.tLXReport.create({
    data: {
      name: req.body.name,
      icon: req.body.icon,
      owner: Number(req.body.owner),
      approximate_member_count: Number(req.body.member_count),
    },
  });

  return res.status(200).json({
    id: `${result.id}`,
  });
}

async function handleGET(req: NextApiRequest, res: NextApiResponse) {
  return res.json({
    status: 'lil bro is really handling a submit request as a get request',
  });
}
