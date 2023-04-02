-- Table: public.t_unprocessed

-- DROP TABLE IF EXISTS public.t_unprocessed;

CREATE TABLE IF NOT EXISTS public.t_unprocessed
(
    id integer NOT NULL DEFAULT 'nextval('"t_unprocessed_id_seq"'::regclass)',
    date date NOT NULL,
    data jsonb NOT NULL,
    CONSTRAINT "t_unprocessed _pkey" PRIMARY KEY (id)
    )

    TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.t_unprocessed
    OWNER to edmgvaichktckx;

-- SEQUENCE: public.t_unprocessed _id_seq

-- DROP SEQUENCE IF EXISTS public."t_unprocessed _id_seq";

CREATE SEQUENCE IF NOT EXISTS public."t_unprocessed _id_seq"
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1
    OWNED BY t_unprocessed.id;

ALTER SEQUENCE public."t_unprocessed _id_seq"
    OWNER TO edmgvaichktckx;