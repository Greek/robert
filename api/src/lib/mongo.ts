// eslint-disable-next-line @typescript-eslint/no-var-requires
require('dotenv').config();

import mongoose from 'mongoose';

export default async () => {
  await mongoose.connect(`${process.env.MONGO_URL}`);
  return mongoose;
};
