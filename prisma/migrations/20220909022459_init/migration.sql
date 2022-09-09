-- CreateTable
CREATE TABLE "GuildConfiguration" (
    "id" BIGINT NOT NULL,
    "message_log_channel_id" BIGINT,
    "welcome_channel" BIGINT,
    "welcome_greeting" TEXT,
    "giveaway_channel" BIGINT,

    CONSTRAINT "GuildConfiguration_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "ToiletGuild" (
    "id" BIGINT NOT NULL,

    CONSTRAINT "ToiletGuild_pkey" PRIMARY KEY ("id")
);
