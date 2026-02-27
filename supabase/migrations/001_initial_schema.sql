-- LaunchPulse Initial Schema
-- Run this migration in your Supabase SQL editor

-- Enable UUID extension
create extension if not exists "uuid-ossp";

-- Idea status enum
create type idea_status as enum ('draft', 'generating', 'live', 'completed', 'archived');

-- Ideas table
create table ideas (
    id uuid primary key default uuid_generate_v4(),
    idea_card jsonb not null,
    status idea_status not null default 'draft',
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create index idx_ideas_status on ideas(status);
create index idx_ideas_created_at on ideas(created_at desc);

-- PRDs table (one per idea)
create table prds (
    id uuid primary key default uuid_generate_v4(),
    idea_id uuid not null references ideas(id) on delete cascade,
    content jsonb not null,
    tokens_used integer not null default 0,
    created_at timestamptz not null default now(),
    unique(idea_id)
);

-- Landing pages table
create table landing_pages (
    id uuid primary key default uuid_generate_v4(),
    idea_id uuid not null references ideas(id) on delete cascade,
    content jsonb not null,
    html text not null,
    variant varchar(1) not null default 'A',
    created_at timestamptz not null default now(),
    unique(idea_id, variant)
);

-- Deployments table
create table deployments (
    id uuid primary key default uuid_generate_v4(),
    idea_id uuid not null references ideas(id) on delete cascade,
    landing_page_id uuid references landing_pages(id) on delete set null,
    url text not null,
    vercel_deployment_id text not null default '',
    variant varchar(1) not null default 'A',
    created_at timestamptz not null default now()
);

create index idx_deployments_idea on deployments(idea_id);

-- Leads table (email signups from landing pages)
create table leads (
    id uuid primary key default uuid_generate_v4(),
    idea_id uuid not null references ideas(id) on delete cascade,
    email text not null,
    utm_source text not null default '',
    utm_medium text not null default '',
    utm_campaign text not null default '',
    referrer text not null default '',
    variant varchar(1) not null default 'A',
    created_at timestamptz not null default now()
);

create index idx_leads_idea on leads(idea_id);
create index idx_leads_created_at on leads(created_at desc);

-- Pipeline runs table (tracks each pipeline execution)
create table pipeline_runs (
    id uuid primary key default uuid_generate_v4(),
    idea_id uuid not null references ideas(id) on delete cascade,
    config jsonb not null default '{}',
    steps jsonb not null default '[]',
    status varchar(20) not null default 'running',
    started_at timestamptz not null default now(),
    completed_at timestamptz
);

create index idx_pipeline_runs_idea on pipeline_runs(idea_id);

-- Auto-update updated_at trigger
create or replace function update_updated_at()
returns trigger as $$
begin
    new.updated_at = now();
    return new;
end;
$$ language plpgsql;

create trigger ideas_updated_at
    before update on ideas
    for each row
    execute function update_updated_at();

-- Row Level Security: allow anonymous inserts to leads (for landing pages)
alter table leads enable row level security;

create policy "Allow anonymous lead inserts"
    on leads for insert
    with check (true);

create policy "Allow authenticated read on leads"
    on leads for select
    using (true);
