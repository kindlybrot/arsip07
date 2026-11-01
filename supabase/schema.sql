-- ARSIP 07 — optional persistence foundation.
-- The current playable prototype synchronizes through Supabase Realtime Broadcast.
-- This table is the next step for durable sessions / reconnect recovery.
create table if not exists public.arsip_rooms (
  code text primary key check (code ~ '^[A-Z0-9]{6}$'),
  state jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

alter table public.arsip_rooms enable row level security;

-- Prototype policy: anyone with the room code can read/write room state.
-- For a public production release, replace this with authenticated membership,
-- server-side validation, and rate limits. Do not store sensitive personal data.
create policy "prototype room read" on public.arsip_rooms
  for select to anon, authenticated using (true);

create policy "prototype room insert" on public.arsip_rooms
  for insert to anon, authenticated with check (true);

create policy "prototype room update" on public.arsip_rooms
  for update to anon, authenticated using (true) with check (true);

-- Enable Realtime for this table only if you later implement postgres_changes.
-- Current app uses Broadcast channels and does not require this table.
