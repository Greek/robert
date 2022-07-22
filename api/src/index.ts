// eslint-disable-next-line @typescript-eslint/no-var-requires
require('dotenv').config();

import { createServer } from 'http';
import { exit } from 'process';
import { app } from './server';

import consola from 'consola';
import mongoose from 'mongoose';

export const server = createServer();

async function initServer() {
  consola.info('Connecting to MongoDB');
  await mongoose
    .connect(`${process.env.MONGO_URL}`)
    .then(() => {
      consola.info('Connection successful.');
    })
    .catch((error) => {
      consola.fatal(error);
      consola.fatal('Could not connect to MongoDB, See error above.');
      exit(1);
    });

  server.on('request', app);
  server.listen(process.env.PORT ?? 3000, () => {
    consola.info(`Listening on port ${process.env.PORT ?? 3000}`);
  });
}

initServer();
