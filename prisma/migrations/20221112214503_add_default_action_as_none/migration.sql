/*
  Warnings:

  - Made the column `action` on table `word_filter` required. This step will fail if there are existing NULL values in that column.

*/
-- AlterTable
ALTER TABLE "word_filter" ALTER COLUMN "action" SET NOT NULL,
ALTER COLUMN "action" SET DEFAULT E'NONE';
