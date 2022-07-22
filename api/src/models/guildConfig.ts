import mongoose, { model } from 'mongoose';

const guildConfig = new mongoose.Schema({
  _id: { type: Number, required: true },
  messageLog: { type: Number },
  colorsRole: { type: Number },
test: {type: String},
  snipeConfig: { type: Boolean },
});

export default model<Object>('guildconfig', guildConfig);
