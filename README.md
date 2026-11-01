# ARSIP 07 — The Missing Memory

A cinematic, two-player psychological mystery built with React, Vite, TypeScript and Supabase Realtime.

## What is included

- Create / join a six-character room code.
- Two-player presence and live synchronization through Supabase Broadcast.
- Asymmetric private evidence: Analyst and Witness receive different information.
- Five investigation chapters: package, evidence room, witnesses, timeline, final theory.
- Shared evidence board, timeline ordering, accusation, hint counter and multiple endings.
- Responsive dark cinematic interface.
- Netlify build configuration.

## Requirements

- Node.js 20.19+ (or Node 22.12+)
- npm
- A Supabase project for online multiplayer.

## Run locally

```bash
npm install
cp .env.example .env
```

Fill `.env` with your Supabase Project URL and anon/public key:

```env
VITE_SUPABASE_URL=https://YOUR_PROJECT.supabase.co
VITE_SUPABASE_ANON_KEY=YOUR_SUPABASE_ANON_KEY
```

Then:

```bash
npm run dev
```

Open the local URL printed by Vite. Open it in two separate browsers/devices, create a room in one and join with the code in the other.

### Offline preview

If Supabase environment variables are absent, the app opens in preview mode. It can be explored on one device, but room synchronization is disabled.

## Supabase setup

1. Create a project at https://supabase.com.
2. Open Project Settings → API.
3. Copy Project URL and anon/public key into `.env`.
4. Realtime is enabled by default for Broadcast channels. No SQL is required for the current prototype.
5. `supabase/schema.sql` is an optional starting point for durable room persistence. It is not used by the current runtime.

### Multiplayer behavior

The app uses a private Supabase Realtime channel named `arsip-room:<ROOMCODE>`. Both players join the channel, track presence, and broadcast the shared game state. The first player is the host; the second player is the witness. A late joiner receives the host's current state.

This is a playable prototype architecture, not a hardened public multiplayer service. Before public launch, add:
- authenticated room membership and server-side room authorization;
- server-side validation of puzzle answers and state transitions;
- durable room snapshots and reconnect recovery;
- rate limiting, room expiration, moderation/reporting, and analytics;
- automated tests for concurrent updates and disconnect/reconnect.

## Deploy to Netlify

### Git-based deploy (recommended)

1. Push this folder to a GitHub repository.
2. In Netlify, choose **Add new site → Import an existing project**.
3. Select the repository.
4. Build command: `npm run build`
5. Publish directory: `dist`
6. Add environment variables in Site configuration → Environment variables:
   - `VITE_SUPABASE_URL`
   - `VITE_SUPABASE_ANON_KEY`
7. Deploy.

`netlify.toml` already contains the build and SPA redirect configuration.

### Netlify CLI

```bash
npm install
npm install -g netlify-cli
netlify login
netlify init
netlify deploy --build --prod
```

Set the two environment variables in Netlify before the production deploy.

## Story note

The current case is designed for an approximately 45–60 minute first playthrough, depending on discussion. It includes a complete narrative arc and multiple endings, but the writing, puzzle depth, and asset library should be playtested and expanded before commercial release.

## Project structure

```text
src/
  components/
  data/
  lib/
  store/
  App.tsx
  main.tsx
  styles.css
supabase/
  schema.sql
```
