/*
  Warnings:

  - You are about to drop the `ToiletGuild` table. If the table is not empty, all the data it contains will be lost.

*/
-- CreateEnum
CREATE TYPE "word_filter_action" AS ENUM ('MUTE', 'KICK', 'BAN');

-- DropTable
DROP TABLE "ToiletGuild";

-- CreateTable
CREATE TABLE "word_filter" (
    "id" TEXT NOT NULL,
    "guild_id" BIGINT NOT NULL,
    "word" TEXT NOT NULL,
    "action" "word_filter_action" NOT NULL DEFAULT E'MUTE',

    CONSTRAINT "word_filter_pkey" PRIMARY KEY ("id")
);
