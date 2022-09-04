import express from 'express';

const v2route = express.Router();

v2route.use('/', (res, req) => {
  return req.status(501).send('There is no v2?');
});

export default v2route;
