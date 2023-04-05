-- Table: public.t_traintype_delay

-- DROP TABLE IF EXISTS public.t_traintype_delay;

CREATE TABLE IF NOT EXISTS public.t_traintype_delay
(
    id oid NOT NULL,
    date date NOT NULL,
    data jsonb NOT NULL,
    CONSTRAINT t_traintype_delay_pkey PRIMARY KEY (id)
    )

    TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.t_traintype_delay
    OWNER to edmgvaichktckx;

-- SEQUENCE: public.t_traintype_delay_id_seq

-- DROP SEQUENCE IF EXISTS public."t_traintype_delay_id_seq";

CREATE SEQUENCE IF NOT EXISTS public."t_traintype_delay_id_seq"
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1
    OWNED BY t_traintype_delay.id;

ALTER SEQUENCE public."t_traintype_delay_id_seq"
    OWNER TO edmgvaichktckx;

ALTER TABLE public.t_traintype_delay
    ALTER COLUMN id SET DEFAULT nextval('public.t_traintype_delay_id_seq');