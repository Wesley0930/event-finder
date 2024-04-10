CREATE TABLE "Users" (
    "id" SERIAL PRIMARY KEY,
    "email" text NOT NULL,
    "username" text NOT NULL,
    "password" text NOT NULL,
    "image_url" text,
    "first_name" text NOT NULL,
    "last_name" text NOT NULL,
    "location" text NOT NULL,
    CONSTRAINT "pk_User" PRIMARY KEY (
        "id"
     ),
    CONSTRAINT "uc_User_email" UNIQUE (
        "email"
    )
);

CREATE TABLE "Events" (
    "id" int   NOT NULL,
    "event_name" text NOT NULL,
    "event_url" text NOT NULL,
    "info" text,
    "venue_name" text,
    "address" text,
    "city" text,
    "start_time" text NOT NULL,
    "end_time" text NOT NULL,

    CONSTRAINT "pk_Event" PRIMARY KEY (
        "id"
     )
);

CREATE TABLE "RSVPs" (
    "id" int   NOT NULL,
    "user_id" int   NOT NULL,
    "event_id" int   NOT NULL,
    CONSTRAINT "pk_RSVP" PRIMARY KEY (
        "id"
     )
);

CREATE TABLE "Likes" (
    "id" int   NOT NULL,
    "user_id" int   NOT NULL,
    "event_id" int   NOT NULL,
    CONSTRAINT "pk_Likes" PRIMARY KEY (
        "id"
     )
);

ALTER TABLE "RSVP" ADD CONSTRAINT "fk_RSVP_user_id" FOREIGN KEY("user_id")
REFERENCES "User" ("id");

ALTER TABLE "RSVP" ADD CONSTRAINT "fk_RSVP_event_id" FOREIGN KEY("event_id")
REFERENCES "Event" ("id");

ALTER TABLE "Likes" ADD CONSTRAINT "fk_Likes_user_id" FOREIGN KEY("user_id")
REFERENCES "User" ("id");

ALTER TABLE "Likes" ADD CONSTRAINT "fk_Likes_event_id" FOREIGN KEY("event_id")
REFERENCES "Event" ("id");

