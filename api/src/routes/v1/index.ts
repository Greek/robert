import express from 'express';

import ping from './endpoints/ping';
import teapot from './endpoints/teapot';
import guild from './endpoints/guild/index';

const v1route = express.Router();

v1route.use('/ping', ping);
v1route.use('/teapot', teapot);
v1route.use('/guild', guild);

export default v1route;
