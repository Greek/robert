-- AlterTable
ALTER TABLE "GuildConfiguration" ADD COLUMN     "color_enabled" BOOLEAN NOT NULL DEFAULT false,
ADD COLUMN     "mute_role" BIGINT;
