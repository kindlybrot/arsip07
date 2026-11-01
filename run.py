import os, textwrap, zipfile, json

base = os.path.dirname(os.path.abspath(__file__))
os.makedirs(base, exist_ok=True)
files = {}

files["package.json"] = r'''
{
  "name": "arsip-07-online",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "@supabase/supabase-js": "^2.57.0",
    "lucide-react": "^0.468.0",
    "motion": "^12.23.12",
    "react": "^19.1.1",
    "react-dom": "^19.1.1",
    "zustand": "^5.0.8"
  },
  "devDependencies": {
    "@types/react": "^19.1.10",
    "@types/react-dom": "^19.1.7",
    "@vitejs/plugin-react": "^5.0.2",
    "typescript": "~5.9.2",
    "vite": "^7.1.4"
  }
}
'''

files["index.html"] = r'''<!doctype html>
<html lang="id">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="theme-color" content="#0b0c10" />
    <meta name="description" content="ARSIP 07 — sebuah psychological mystery untuk dua orang." />
    <title>ARSIP 07 — The Missing Memory</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@400;500;600&display=swap" rel="stylesheet">
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
'''

files["vite.config.ts"] = r'''import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
export default defineConfig({ plugins: [react()] })
'''

files["tsconfig.json"] = r'''{
  "files": [],
  "references": [{ "path": "./tsconfig.app.json" }, { "path": "./tsconfig.node.json" }]
}'''
files["tsconfig.app.json"] = r'''{
  "compilerOptions": {
    "tsBuildInfoFile": "./node_modules/.tmp/tsconfig.app.tsbuildinfo",
    "target": "ES2022", "useDefineForClassFields": true, "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "module": "ESNext", "skipLibCheck": true, "moduleResolution": "bundler",
    "allowImportingTsExtensions": true, "verbatimModuleSyntax": true, "moduleDetection": "force",
    "noEmit": true, "jsx": "react-jsx", "strict": true, "noUnusedLocals": false,
    "noUnusedParameters": false, "noFallthroughCasesInSwitch": true
  },
  "include": ["src"]
}'''
files["tsconfig.node.json"] = r'''{
  "compilerOptions": {
    "tsBuildInfoFile": "./node_modules/.tmp/tsconfig.node.tsbuildinfo",
    "target": "ES2023", "lib": ["ES2023"], "module": "ESNext",
    "skipLibCheck": true, "moduleResolution": "bundler", "allowImportingTsExtensions": true,
    "verbatimModuleSyntax": true, "moduleDetection": "force", "noEmit": true, "strict": true
  },
  "include": ["vite.config.ts"]
}'''

files[".env.example"] = r'''VITE_SUPABASE_URL=https://YOUR_PROJECT.supabase.co
VITE_SUPABASE_ANON_KEY=YOUR_SUPABASE_ANON_KEY
'''
files[".gitignore"] = r'''node_modules
dist
.env
.env.local
.DS_Store
'''

files["netlify.toml"] = r'''[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
'''

files["supabase/schema.sql"] = r'''-- ARSIP 07 — optional persistence foundation.
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
'''

files["README.md"] = r'''# ARSIP 07 — The Missing Memory

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
'''

files["src/main.tsx"] = r'''import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './styles.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode><App /></React.StrictMode>,
)
'''

files["src/lib/supabase.ts"] = r'''import { createClient } from '@supabase/supabase-js'

const url = import.meta.env.VITE_SUPABASE_URL as string | undefined
const key = import.meta.env.VITE_SUPABASE_ANON_KEY as string | undefined

export const isOnlineConfigured = Boolean(url && key && !url.includes('YOUR_PROJECT'))
export const supabase = isOnlineConfigured ? createClient(url!, key!) : null
'''

files["src/data/story.ts"] = r'''export type Evidence = {
  id: string
  title: string
  type: string
  date: string
  body: string
  stamp: string
  privateTo?: 'analyst' | 'witness'
}

export const evidence: Evidence[] = [
  { id: 'letter', title: 'Surat yang Tidak Dikirim', type: 'SURAT / BUKTI 01', date: '14 OKTOBER 1998', stamp: 'DITEMUKAN', body: '“Jika suatu hari mereka bertanya, katakan bahwa malam itu hujan. Jangan katakan siapa yang datang lebih dulu.” Tulisan tangan di bagian bawah berbeda dari isi surat.', },
  { id: 'photo', title: 'Foto Ruang Tunggu', type: 'FOTOGRAFI / BUKTI 02', date: '14 OKTOBER 1998 · 21:16', stamp: 'ASLI', body: 'Dua siluet terlihat di pantulan kaca. Jam dinding menunjukkan 21:16, tetapi bayangan seseorang jatuh ke arah yang salah.', },
  { id: 'receipt', title: 'Kuitansi Telepon', type: 'DOKUMEN / BUKTI 03', date: '14 OKTOBER 1998', stamp: 'TERLIPAT', body: 'Panggilan keluar berlangsung selama 04 menit 12 detik. Nomor tujuan telah dihapus, tetapi tiga digit terakhir masih terbaca: 0–7–2.', },
  { id: 'tape', title: 'Rekaman Kaset B', type: 'AUDIO / BUKTI 04', date: '15 OKTOBER 1998 · 00:03', stamp: 'DIPULIHKAN', body: 'Suara perempuan: “Kamu berjanji tidak akan mengingat bagian itu.” Suara lain menjawab: “Aku tidak lupa. Aku hanya memilih versi yang bisa kita jalani.”', },
  { id: 'report', title: 'Laporan Klinik', type: 'ARSIP MEDIS / BUKTI 05', date: '16 OKTOBER 1998', stamp: 'SALINAN', body: 'Pasien datang tanpa identitas. Catatan menyebut disorientasi waktu dan memori episodik yang terfragmentasi. Kolom pendamping sengaja dikosongkan.', privateTo: 'analyst' },
  { id: 'postcard', title: 'Kartu Pos Tanpa Perangko', type: 'KORESPONDENSI / BUKTI 06', date: 'TANGGAL TIDAK DIKETAHUI', stamp: 'TANPA ALAMAT', body: '“Aku ingat lampu lorong. Aku ingat suara langkah. Tapi aku tidak ingat wajahku sendiri ketika kamu memanggil namaku.”', privateTo: 'witness' },
]

export const timeline = [
  { id: 'call', label: 'Panggilan telepon selama 4 menit 12 detik', date: '14 Okt · 20:42' },
  { id: 'arrival', label: 'Seseorang tiba di ruang tunggu', date: '14 Okt · 21:16' },
  { id: 'rain', label: 'Hujan mulai turun di sekitar gedung', date: '14 Okt · 21:30' },
  { id: 'tape', label: 'Rekaman kaset dibuat', date: '15 Okt · 00:03' },
]

export const correctTimeline = ['call', 'arrival', 'rain', 'tape']

export const theories = [
  { id: 'accident', title: 'Sebuah kecelakaan', description: 'Malam itu adalah kecelakaan. Ingatan yang hilang hanyalah akibat trauma.', result: 'Kalian memilih penjelasan yang paling mudah diterima. Namun, kuitansi telepon dan surat itu menunjukkan ada seseorang yang mengatur cerita sejak awal.' },
  { id: 'conspiracy', title: 'Seseorang menyusun kebohongan', description: 'Dua orang membuat kesepakatan untuk menghapus satu kejadian dari ingatan bersama.', result: 'Kalian menemukan pola kebohongan. Bukan untuk menutupi kejahatan, melainkan untuk melindungi seseorang dari kebenaran yang belum sanggup ia hadapi.' },
  { id: 'memory', title: 'Ingatan itu milik kalian', description: 'Kasus ini bukan tentang orang asing. Dua penyelidik adalah bagian dari ingatan yang sedang mereka selidiki.', result: 'Semua potongan akhirnya menyatu. Kalian bukan sekadar menemukan arsip. Kalian sedang membaca dua versi dari satu malam yang sama.' },
]
'''

files["src/store/game.ts"] = r'''import { create } from 'zustand'
import { supabase } from '../lib/supabase'

export type PlayerRole = 'analyst' | 'witness'
export type GameState = {
  stage: number
  evidenceOpened: string[]
  timelineOrder: string[]
  timelineSolved: boolean
  witnessChoice: string
  theory: string
  hints: number
  started: boolean
  ended: boolean
}
const initial: GameState = {
  stage: 0, evidenceOpened: [], timelineOrder: [], timelineSolved: false,
  witnessChoice: '', theory: '', hints: 0, started: false, ended: false,
}
type Player = { id: string; name: string; role: PlayerRole }
type Store = {
  game: GameState
  room: string
  player: Player | null
  players: Player[]
  online: boolean
  connected: boolean
  channel: ReturnType<NonNullable<typeof supabase>['channel']> | null
  error: string
  setError: (s: string) => void
  connectRoom: (room: string, name: string, create: boolean) => Promise<void>
  updateGame: (patch: Partial<GameState>) => void
  leave: () => void
}

const playerId = () => crypto.randomUUID()
const roomCode = () => Math.random().toString(36).slice(2, 8).toUpperCase()

export const useGame = create<Store>((set, get) => ({
  game: initial, room: '', player: null, players: [], online: Boolean(supabase), connected: false, channel: null, error: '',
  setError: (error) => set({ error }),
  connectRoom: async (requestedRoom, name, createRoom) => {
    if (!supabase) {
      const code = createRoom ? roomCode() : requestedRoom.trim().toUpperCase()
      set({ room: code, player: { id: playerId(), name, role: 'analyst' }, players: [{ id: 'local', name, role: 'analyst' }], connected: true, error: 'Mode preview aktif: isi Supabase URL dan anon key untuk multiplayer online.' })
      return
    }
    const code = createRoom ? roomCode() : requestedRoom.trim().toUpperCase()
    const id = playerId()
    const channel = supabase.channel(`arsip-room:${code}`, {
      config: { broadcast: { self: false }, presence: { key: id } },
    })
    const player: Player = { id, name, role: 'analyst' }
    set({ room: code, player, channel, connected: false, error: '' })

    channel.on('presence', { event: 'sync' }, () => {
      const state = channel.presenceState<Record<string, Player>>()
      const peers = Object.values(state).flat().map(p => p as Player)
      const unique = [...new Map(peers.map(p => [p.id, p])).values()]
      const ordered = unique.sort((a, b) => a.id.localeCompare(b.id))
      const me = ordered.findIndex(p => p.id === id)
      const assigned = ordered.map((p, i) => ({ ...p, role: (i === 0 ? 'analyst' : 'witness') as PlayerRole }))
      set({ players: assigned, player: assigned.find(p => p.id === id) ?? { ...player, role: me === 0 ? 'analyst' : 'witness' } })
      if (assigned.length > 1) {
        const host = assigned[0]
        if (host.id !== id) channel.send({ type: 'broadcast', event: 'request_state', payload: { from: id } })
      }
    })
    channel.on('broadcast', { event: 'game_state' }, ({ payload }) => {
      if (payload?.state) set({ game: payload.state as GameState })
    })
    channel.on('broadcast', { event: 'request_state' }, () => {
      if (get().player?.role === 'analyst') channel.send({ type: 'broadcast', event: 'game_state', payload: { state: get().game } })
    })
    channel.subscribe(async (status) => {
      if (status === 'SUBSCRIBED') {
        await channel.track({ id, name, role: 'analyst', joinedAt: new Date().toISOString() })
        set({ connected: true })
      } else if (status === 'CHANNEL_ERROR' || status === 'TIMED_OUT') {
        set({ error: 'Koneksi room gagal. Periksa Supabase URL, anon key, dan koneksi internet.' })
      }
    })
  },
  updateGame: (patch) => {
    const next = { ...get().game, ...patch }
    set({ game: next })
    const { channel, connected } = get()
    if (channel && connected) channel.send({ type: 'broadcast', event: 'game_state', payload: { state: next } })
  },
  leave: () => {
    const { channel } = get()
    if (channel && supabase) supabase.removeChannel(channel)
    set({ game: initial, room: '', player: null, players: [], connected: false, channel: null, error: '' })
  },
}))
'''

files["src/App.tsx"] = r'''import { useMemo, useState } from 'react'
import { AnimatePresence, motion } from 'motion/react'
import { Archive, ArrowDown, ArrowLeft, ArrowRight, AudioLines, BookOpen, Check, ChevronRight, CircleHelp, Clipboard, Clock3, Copy, Eye, Fingerprint, FileText, LockKeyhole, MessageSquare, Radio, RotateCcw, Shield, Sparkles, Users, X } from 'lucide-react'
import { evidence, timeline, correctTimeline, theories } from './data/story'
import { useGame, type GameState } from './store/game'
import { isOnlineConfigured } from './lib/supabase'

const slide = { initial: { opacity: 0, y: 14 }, animate: { opacity: 1, y: 0 }, exit: { opacity: 0, y: -10 } }

function App() {
  const { game, room, player, players, connected, error, connectRoom, updateGame, leave, setError } = useGame()
  const [name, setName] = useState('')
  const [roomInput, setRoomInput] = useState('')
  const [tab, setTab] = useState<'case'|'evidence'|'journal'>('case')
  const [selectedEvidence, setSelectedEvidence] = useState<string | null>(null)
  const [selectedOrder, setSelectedOrder] = useState<string[]>([])
  const [theory, setTheory] = useState('')
  const [showHint, setShowHint] = useState(false)
  const [copied, setCopied] = useState(false)

  const opened = evidence.filter(e => game.evidenceOpened.includes(e.id))
  const currentEvidence = evidence.find(e => e.id === selectedEvidence)
  const visibleEvidence = useMemo(() => evidence.filter(e => !e.privateTo || e.privateTo === player?.role), [player?.role])
  const progress = Math.min(100, Math.round((game.evidenceOpened.length / evidence.length) * 55 + (game.timelineSolved ? 20 : 0) + (game.witnessChoice ? 10 : 0) + (game.ended ? 15 : 0)))

  const create = async () => {
    if (!name.trim()) return setError('Masukkan nama panggilan terlebih dahulu.')
    await connectRoom('', name.trim(), true)
  }
  const join = async () => {
    if (!name.trim() || roomInput.trim().length !== 6) return setError('Masukkan nama dan kode room 6 karakter.')
    await connectRoom(roomInput, name.trim(), false)
  }
  const begin = () => updateGame({ started: true, stage: 1 })
  const openEvidence = (id: string) => {
    const next = [...new Set([...game.evidenceOpened, id])]
    updateGame({ evidenceOpened: next })
    setSelectedEvidence(id)
  }
  const addTimeline = (id: string) => {
    if (selectedOrder.includes(id)) return
    const next = [...selectedOrder, id]
    setSelectedOrder(next)
    if (next.length === 4) {
      const correct = next.every((v, i) => v === correctTimeline[i])
      if (correct) updateGame({ timelineOrder: next, timelineSolved: true, stage: 4 })
      else setSelectedOrder([])
    }
  }
  const submitTheory = () => {
    if (!theory) return
    updateGame({ theory, ended: true, stage: 5 })
  }
  const copyRoom = async () => {
    await navigator.clipboard?.writeText(room)
    setCopied(true)
    window.setTimeout(() => setCopied(false), 1600)
  }
  const reset = () => { leave(); setSelectedOrder([]); setTheory(''); setTab('case') }

  if (!room || !player) {
    return <Landing name={name} setName={setName} roomInput={roomInput} setRoomInput={setRoomInput} create={create} join={join} error={error} online={isOnlineConfigured} />
  }

  const isSecond = player.role === 'witness'
  return (
    <div className="game-shell">
      <header className="topbar">
        <div className="brand"><span className="brand-mark"><Archive size={16}/></span><span>DEPARTEMEN ARSIP <b>/</b> 07</span></div>
        <div className="top-center"><span className="live-dot"/>{connected ? 'CHANNEL SECURE' : 'CONNECTING'} <span className="top-divider"/> ROOM {room}</div>
        <button className="icon-button" onClick={reset} title="Keluar dari room"><X size={17}/></button>
      </header>
      <div className="progress-track"><div className="progress-fill" style={{ width: `${progress}%` }}/></div>
      <div className="game-layout">
        <aside className="sidebar">
          <div className="case-label">CURRENT CASE</div>
          <div className="case-title">THE MISSING<br/><em>MEMORY</em></div>
          <div className="case-meta"><span>CASE NO. 07-1998</span><span>CLASSIFIED</span></div>
          <div className="side-rule"/>
          <div className="players-title"><Users size={13}/> INVESTIGATORS</div>
          {players.map((p, i) => <div className="player-line" key={p.id}><span className={`avatar ${p.role}`}>{p.role === 'analyst' ? 'A' : 'W'}</span><span><b>{p.name}</b><small>{p.role === 'analyst' ? 'THE ANALYST' : 'THE WITNESS'}</small></span><span className="online-dot"/></div>)}
          {players.length < 2 && <div className="waiting-player"><span className="pulse"/> Menunggu pemain kedua…</div>}
          <div className="side-rule"/>
          <div className="nav-list">
            <button className={tab==='case'?'active':''} onClick={()=>setTab('case')}><Archive size={15}/> Case file <ChevronRight size={14}/></button>
            <button className={tab==='evidence'?'active':''} onClick={()=>setTab('evidence')}><Fingerprint size={15}/> Evidence board <span className="nav-count">{opened.length}</span></button>
            <button className={tab==='journal'?'active':''} onClick={()=>setTab('journal')}><BookOpen size={15}/> Field journal</button>
          </div>
          <div className="sidebar-bottom"><Shield size={14}/> PRIVATE INVESTIGATION SESSION<br/><small>Do not distribute case materials.</small></div>
        </aside>

        <main className="main-content">
          <div className="mobile-room"><span>ROOM {room}</span><span>{players.length}/2 INVESTIGATORS</span></div>
          <AnimatePresence mode="wait">
            {tab === 'evidence' ? <motion.div key="evidence" {...slide}><EvidenceBoard items={visibleEvidence} opened={game.evidenceOpened} open={openEvidence}/></motion.div>
              : tab === 'journal' ? <motion.div key="journal" {...slide}><Journal game={game} role={player.role} /></motion.div>
              : <motion.div key={`stage-${game.stage}-${game.ended}`} {...slide}>
                {!game.started ? <Briefing begin={begin} players={players.length} role={player.role} />
                  : game.ended ? <Ending theory={game.theory} hints={game.hints} reset={reset}/>
                  : game.stage <= 1 ? <ChapterOne open={() => setTab('evidence')} role={player.role} players={players.length}/>
                  : game.stage === 2 ? <EvidenceChapter items={visibleEvidence} opened={game.evidenceOpened} open={openEvidence} role={player.role} next={() => updateGame({stage:3})}/>
                  : game.stage === 3 ? <WitnessChapter choice={game.witnessChoice} choose={(v)=>updateGame({witnessChoice:v,stage:4})} role={player.role}/>
                  : game.stage === 4 ? <TimelineChapter selected={selectedOrder} add={addTimeline} solved={game.timelineSolved} theory={theory} setTheory={setTheory} submit={submitTheory} hint={()=>{setShowHint(!showHint);if(!showHint)updateGame({hints:game.hints+1})}} showHint={showHint}/>
                  : null}
              </motion.div>}
          </AnimatePresence>
        </main>
        <aside className="right-rail">
          <div className="rail-heading">CASE STATUS <span className="live-dot"/></div>
          <div className="status-card"><div className="status-number">{String(opened.length).padStart(2,'0')}<small>/ 06</small></div><span>PIECES RECOVERED</span><div className="mini-track"><div style={{width:`${opened.length/6*100}%`}}/></div></div>
          <div className="rail-heading spaced">ROOM ACCESS</div>
          <div className="room-card"><span>INVITATION CODE</span><strong>{room}</strong><button onClick={copyRoom}><Copy size={13}/>{copied?'COPIED':'COPY CODE'}</button></div>
          <div className="rail-heading spaced">YOUR IDENTITY</div>
          <div className="identity-card"><div className={`avatar large ${player.role}`}>{isSecond?'W':'A'}</div><div><b>{player.name}</b><small>{isSecond?'THE WITNESS':'THE ANALYST'}</small></div></div>
          <div className="private-note"><LockKeyhole size={14}/><span>{isSecond ? 'You hold a private memory fragment. Share only what you choose.' : 'You have access to the clinical record. Compare it with your partner’s evidence.'}</span></div>
          {error && <div className="small-error">{error}</div>}
        </aside>
      </div>
      <AnimatePresence>{currentEvidence && <EvidenceModal item={currentEvidence} close={()=>setSelectedEvidence(null)}/>}</AnimatePresence>
    </div>
  )
}

function Landing({name,setName,roomInput,setRoomInput,create,join,error,online}:{name:string;setName:(v:string)=>void;roomInput:string;setRoomInput:(v:string)=>void;create:()=>void;join:()=>void;error:string;online:boolean}) {
  return <div className="landing">
    <div className="landing-noise"/>
    <header className="landing-top"><div className="brand"><span className="brand-mark"><Archive size={16}/></span> DEPARTEMEN ARSIP <b>/</b> 07</div><div className="classified">CLASSIFIED INVESTIGATION <span>●</span></div></header>
    <main className="landing-content">
      <div className="eyebrow"><span/> AN INTERACTIVE PSYCHOLOGICAL MYSTERY <span/></div>
      <div className="hero-title">SOME MEMORIES<br/>WERE NEVER <em>YOURS.</em></div>
      <p className="hero-copy">Sebuah kasus lama. Dua versi kebenaran. Satu ingatan yang sengaja dikubur. Kalian hanya bisa menemukannya bersama.</p>
      <div className="hero-stamp"><span>CASE FILE</span><b>07</b><span>OCT 1998 · REOPENED</span></div>
      <div className="access-panel">
        <div className="panel-top"><span>SECURE ACCESS TERMINAL</span><span><LockKeyhole size={12}/> ENCRYPTED SESSION</span></div>
        <label>INVESTIGATOR CALLSIGN</label>
        <input value={name} onChange={e=>setName(e.target.value)} placeholder="Masukkan nama panggilan" maxLength={20}/>
        <button className="primary-button" onClick={create}>CREATE NEW INVESTIGATION <ArrowRight size={16}/></button>
        <div className="or"><span/> OR JOIN AN EXISTING CASE <span/></div>
        <div className="join-row"><input value={roomInput} onChange={e=>setRoomInput(e.target.value.toUpperCase().slice(0,6))} placeholder="6-DIGIT CODE" maxLength={6}/><button onClick={join}>JOIN <ArrowRight size={15}/></button></div>
        {error && <div className="form-error">{error}</div>}
        {!online && <div className="preview-warning"><CircleHelp size={14}/> Preview mode — configure Supabase to enable online rooms.</div>}
      </div>
      <div className="landing-foot"><span><Clock3 size={13}/> APPROX. 60 MINUTES</span><span><Users size={13}/> TWO INVESTIGATORS</span><span><Radio size={13}/> REAL-TIME CO-OP</span></div>
    </main>
    <div className="landing-watermark">07</div>
    <div className="landing-bottom"><span>ARSIP 07 — THE MISSING MEMORY</span><span>ALL MEMORIES SUBJECT TO REVISION</span></div>
  </div>
}

function Briefing({begin,players,role}:{begin:()=>void;players:number;role:string}) {
  return <section className="chapter">
    <div className="chapter-kicker">01 / CASE OPENING <span>14 OCTOBER 1998</span></div>
    <h1>The room remembers<br/><em>what you forgot.</em></h1>
    <p className="chapter-lead">Pukul 02:17 dini hari, sebuah amplop tiba di kantor arsip. Tidak ada pengirim. Hanya dua nama penyelidik yang tertulis di bagian depan—nama kalian.</p>
    <div className="cinema-image"><div className="image-caption">FIG. 01 — THE ARCHIVE ROOM, 1998</div><div className="image-overlay-text">SOMEONE WAS HERE.</div></div>
    <div className="document-quote"><span>TRANSCRIPT / ENVELOPE CONTENT</span><p>“Kalian pernah berada di ruangan itu. Kalian berdua. Tetapi hanya satu dari kalian yang mengingat malam tersebut dengan benar.”</p><small>— UNKNOWN AUTHOR</small></div>
    <div className="briefing-grid"><div><span>YOUR ASSIGNMENT</span><b>Reconstruct the missing night.</b><p>Periksa bukti, dengarkan saksi, dan temukan bagian ingatan yang sengaja dihapus.</p></div><div><span>PARTNER STATUS</span><b>{players}/2 investigators connected</b><p>{players < 2 ? 'Kalian bisa mulai sendiri, tetapi pengalaman terbaik membutuhkan dua pemain.' : 'Kedua penyelidik sudah terhubung. Informasi kalian tidak sepenuhnya sama.'}</p></div></div>
    <button className="primary-button wide" onClick={begin}>OPEN CASE FILE <ArrowRight size={16}/></button>
  </section>
}

function ChapterOne({open,role,players}:{open:()=>void;role:string;players:number}) {
  return <section className="chapter">
    <div className="chapter-kicker">02 / THE FIRST TRACE <span>FILE 01—06</span></div>
    <h1>Evidence is never<br/><em>the whole truth.</em></h1>
    <p className="chapter-lead">Kalian menemukan enam artefak dari malam yang sama. Namun beberapa dokumen hanya terlihat oleh satu penyelidik.</p>
    <div className="alert-strip"><LockKeyhole size={15}/><span><b>ASYMMETRIC EVIDENCE</b> — {role === 'analyst' ? 'Laporan klinik hanya tersedia di berkasmu.' : 'Kartu pos tanpa perangko hanya tersedia di berkasmu.'} Kalian harus saling bertukar informasi.</span></div>
    <EvidenceBoard items={evidence.filter(e=>!e.privateTo||e.privateTo===role)} opened={[]} open={open}/>
    <button className="primary-button wide" onClick={open}>OPEN EVIDENCE BOARD <ArrowRight size={16}/></button>
  </section>
}

function EvidenceChapter({items,opened,open,role,next}:{items:typeof evidence;opened:string[];open:(id:string)=>void;role:string;next:()=>void}) {
  const count = opened.length
  return <section className="chapter">
    <div className="chapter-kicker">03 / THE EVIDENCE ROOM <span>{count} RECOVERED</span></div>
    <h1>Fragments of<br/><em>a broken night.</em></h1>
    <p className="chapter-lead">Buka seluruh bukti yang bisa kalian akses. Jangan simpulkan terlalu cepat—beberapa detail baru masuk akal setelah kalian berbagi informasi.</p>
    <EvidenceBoard items={items} opened={opened} open={open}/>
    <div className="chapter-footer"><span>{count} / 6 PIECES RECOVERED BY THE TEAM</span><button className="primary-button" disabled={count<4} onClick={next}>CONTINUE TO WITNESSES <ArrowRight size={15}/></button></div>
    <p className="muted-note">Setidaknya empat bukti harus dibuka. Untuk mengakses semua detail, minta pasanganmu membacakan bukti privat mereka.</p>
  </section>
}

function EvidenceBoard({items,opened,open}:{items:typeof evidence;opened:string[];open:(id:string)=>void}) {
  return <div className="evidence-grid">{items.map((item,i)=><button className={`evidence-card ${opened.includes(item.id)?'found':''}`} key={item.id} onClick={()=>open(item.id)}>
    <div className="evidence-thumb">{item.type.startsWith('AUDIO')?<AudioLines size={28}/>:item.type.startsWith('FOTOGRAFI')?<Eye size={28}/>:<FileText size={28}/>}<span>{String(i+1).padStart(2,'0')}</span></div>
    <div className="evidence-info"><small>{item.type}</small><b>{item.title}</b><span>{item.date}</span></div>
    <div className="evidence-status">{opened.includes(item.id)?<><Check size={12}/> REVIEWED</>:item.privateTo?<><LockKeyhole size={12}/> PRIVATE</>:<><ArrowRight size={12}/> OPEN FILE</>}</div>
  </button>)}</div>
}

function EvidenceModal({item,close}:{item:typeof evidence[number];close:()=>void}) {
  return <motion.div className="modal-backdrop" initial={{opacity:0}} animate={{opacity:1}} exit={{opacity:0}} onClick={close}><motion.div className="evidence-modal" initial={{y:20,opacity:0}} animate={{y:0,opacity:1}} exit={{y:20,opacity:0}} onClick={e=>e.stopPropagation()}>
    <button className="modal-close" onClick={close}><X size={18}/></button><div className="modal-type">{item.type} <span>{item.stamp}</span></div><h2>{item.title}</h2><div className="modal-date">{item.date}</div><div className="document-body">{item.body}</div><div className="modal-foot"><span>ARSIP 07 / EVIDENCE CONTROL</span><button className="text-button" onClick={close}>CLOSE DOCUMENT <X size={13}/></button></div>
  </motion.div></motion.div>
}

function WitnessChapter({choice,choose,role}:{choice:string;choose:(v:string)=>void;role:string}) {
  const [answer,setAnswer] = useState('')
  return <section className="chapter">
    <div className="chapter-kicker">04 / WITNESS INTERROGATION <span>TRANSCRIPT 02:17</span></div>
    <h1>One of you is<br/><em>remembering wrong.</em></h1>
    <p className="chapter-lead">Rekaman wawancara terakhir berisi satu pertanyaan. Jawaban kalian akan menentukan bagaimana investigasi bergerak.</p>
    <div className="transcript">
      <div className="transcript-head"><span><AudioLines size={14}/> AUDIO TRANSCRIPT / RESTORED</span><span>00:03:41</span></div>
      <div className="speaker"><span className="speaker-tag">INTERVIEWER</span><p>“Apakah kamu ingat siapa yang pertama kali tiba di ruang tunggu malam itu?”</p></div>
      <div className="speaker reply"><span className="speaker-tag">UNKNOWN VOICE</span><p>“Aku ingat suara hujan. Aku ingat seseorang memanggil namaku. Tapi aku tidak yakin nama siapa yang disebut.”</p></div>
      <div className="waveform">{Array.from({length:70},(_,i)=><i key={i} style={{height:`${12+((i*17+7)%38)}px`}}/>)}</div>
    </div>
    <div className="question-block"><span>YOUR INTERPRETATION</span><h3>Apa yang paling mungkin disembunyikan oleh saksi?</h3>
      {[
        ['identity','Identitas orang yang tiba lebih dulu.'],
        ['memory','Fakta bahwa saksi memiliki ingatan yang berbeda.'],
        ['promise','Janji yang dibuat sebelum malam itu terjadi.'],
      ].map(([v,label])=><button key={v} className={`choice-row ${answer===v?'selected':''}`} onClick={()=>setAnswer(v)}><span className="choice-radio"/>{label}</button>)}
      <button className="primary-button wide" disabled={!answer||Boolean(choice)} onClick={()=>choose(answer)}>{choice?'INTERPRETATION RECORDED':'RECORD INTERPRETATION'} <ArrowRight size={15}/></button>
      {choice&&<div className="success-note"><Check size={14}/> Your interpretation has been recorded. Both investigators can continue.</div>}
      <p className="muted-note">Peran kamu: {role==='analyst'?'THE ANALYST — kamu melihat pola pada dokumen.':'THE WITNESS — kamu menerima fragmen ingatan personal.'} Diskusikan pilihan dengan pasangan sebelum mengunci jawaban.</p>
    </div>
  </section>
}

function TimelineChapter({selected,add,solved,theory,setTheory,submit,hint,showHint}:{selected:string[];add:(id:string)=>void;solved:boolean;theory:string;setTheory:(v:string)=>void;submit:()=>void;hint:()=>void;showHint:boolean}) {
  return <section className="chapter">
    <div className="chapter-kicker">05 / RECONSTRUCT THE NIGHT <span>CHRONOLOGY</span></div>
    <h1>Put the night<br/><em>back together.</em></h1>
    <p className="chapter-lead">Susun kejadian berdasarkan bukti yang kalian temukan. Pilih urutan dari kejadian paling awal hingga paling akhir.</p>
    <div className="timeline-puzzle">
      <div className="timeline-progress"><span>SEQUENCE BUILDER</span><span>{solved?'SEQUENCE VERIFIED':`${selected.length}/4 EVENTS PLACED`}</span></div>
      {selected.map((id,i)=><div className="timeline-picked" key={id}><span>{String(i+1).padStart(2,'0')}</span>{timeline.find(t=>t.id===id)?.label}<Check size={14}/></div>)}
      {!solved&&<div className="timeline-options">{timeline.filter(t=>!selected.includes(t.id)).map(t=><button key={t.id} onClick={()=>add(t.id)}><span>+</span><b>{t.label}</b><small>{t.date}</small></button>)}</div>}
      {solved&&<div className="success-note"><Check size={14}/> Timeline reconstructed. The missing sequence is now visible.</div>}
    </div>
    {showHint&&<div className="hint-card"><Sparkles size={15}/> Petunjuk: kuitansi telepon mencatat panggilan sebelum foto ruang tunggu. Rekaman kaset dibuat setelah tengah malam.</div>}
    <button className="text-button hint-button" onClick={hint}><CircleHelp size={14}/> REQUEST A HINT <span>+1 HINT USED</span></button>
    {solved&&<div className="theory-block"><div className="chapter-kicker">FINAL DEDUCTION <span>CHOOSE YOUR THEORY</span></div><h2>What really happened?</h2><p className="muted-note">Pilih teori yang paling sesuai dengan bukti. Tidak semua jawaban akan membuka akhir yang sama.</p>
      {theories.map(t=><button key={t.id} className={`theory-card ${theory===t.id?'selected':''}`} onClick={()=>setTheory(t.id)}><span className="choice-radio"/><div><b>{t.title}</b><p>{t.description}</p></div></button>)}
      <button className="primary-button wide" disabled={!theory} onClick={submit}>SUBMIT FINAL DEDUCTION <ArrowRight size={15}/></button>
    </div>}
  </section>
}

function Journal({game,role}:{game:GameState;role:string}) {
  return <section className="chapter"><div className="chapter-kicker">FIELD NOTES <span>LIVE SESSION</span></div><h1>Investigator’s<br/><em>journal.</em></h1><p className="chapter-lead">Catatan progres investigasi bersama. Gunakan ruang ini untuk membandingkan temuan dan teori.</p>
    <div className="journal-stat-grid"><div><b>{game.evidenceOpened.length}</b><span>EVIDENCE REVIEWED</span></div><div><b>{game.hints}</b><span>HINTS USED</span></div><div><b>{game.timelineSolved?'✓':'—'}</b><span>TIMELINE STATUS</span></div></div>
    <div className="journal-entry"><span>PERSONAL ACCESS / {role.toUpperCase()}</span><h3>Your private fragment</h3><p>{role==='analyst'?'Laporan klinik menyebut pasien mengalami fragmentasi memori episodik. Ada kemungkinan ingatan yang hilang bukan terhapus secara alami.':'Kartu pos itu terasa seperti ditulis oleh seseorang yang mengenalmu. Kamu ingat lampu lorong, tetapi tidak ingat wajah yang berdiri di sana.'}</p></div>
    <div className="journal-entry"><span>SHARED OBJECTIVE</span><h3>Reconstruct October 14, 1998</h3><p>Enam bukti, dua versi ingatan, dan satu malam yang tidak pernah selesai diceritakan.</p></div>
  </section>
}

function Ending({theory,hints,reset}:{theory:string;hints:number;reset:()=>void}) {
  const found = theories.find(t=>t.id===theory) ?? theories[0]
  const isTrue = theory==='memory'
  return <section className="ending-screen"><div className="ending-symbol"><Fingerprint size={35}/></div><div className="chapter-kicker">CASE CLOSED / 07-1998 <span>{isTrue?'TRUTH RECOVERED':'PARTIAL CONCLUSION'}</span></div><h1>{isTrue?'The memory\\nwas never lost.':'A version of\\nthe truth.'}</h1><div className="ending-line"/><h2>{found.title}</h2><p>{found.result}</p><div className="ending-stats"><div><b>06</b><span>ARTIFACTS</span></div><div><b>{hints}</b><span>HINTS USED</span></div><div><b>{isTrue?'TRUE':'PARTIAL'}</b><span>CASE STATUS</span></div></div><blockquote>“Ada hal-hal yang kita lupakan untuk bertahan hidup. Dan ada hal-hal yang kita ingat karena akhirnya kita siap menghadapinya.”</blockquote><button className="primary-button" onClick={reset}><RotateCcw size={15}/> RETURN TO ARCHIVE</button></section>
}

export default App
'''

files["src/styles.css"] = r'''@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,500;0,600;1,400;1,500&display=swap');
:root{font-family:'DM Sans',sans-serif;color:#e9e5dc;background:#0b0c10;font-synthesis:none;text-rendering:optimizeLegibility;--bg:#0b0c10;--panel:#12141a;--panel2:#191b22;--line:#2c2d33;--muted:#8b8b91;--gold:#c9a66b;--gold2:#e3c28a;--red:#b56e69;--green:#86ad91;--mono:'DM Mono',monospace;--serif:'Playfair Display',serif}
*{box-sizing:border-box}body{margin:0;min-width:320px;background:var(--bg)}button,input{font:inherit}button{cursor:pointer}button:disabled{opacity:.35;cursor:not-allowed}.landing{min-height:100vh;position:relative;overflow:hidden;background:radial-gradient(ellipse at 50% 38%,#28231f 0,#151419 38%,#0b0c10 75%)}.landing:before,.landing-noise{content:"";position:absolute;inset:0;pointer-events:none;background:linear-gradient(90deg,#0b0c10 0%,transparent 24%,transparent 76%,#0b0c10 100%),repeating-linear-gradient(0deg,transparent,transparent 3px,#ffffff03 4px)}.landing:after{content:"";position:absolute;inset:0;pointer-events:none;opacity:.13;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 180 180' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='.24'/%3E%3C/svg%3E")}.landing-top,.landing-bottom{position:relative;z-index:2;display:flex;justify-content:space-between;align-items:center;padding:25px 5vw;color:#aaa;font:10px var(--mono);letter-spacing:.13em}.brand{display:flex;align-items:center;gap:10px;font:11px var(--mono);letter-spacing:.14em}.brand b{color:var(--gold)}.brand-mark{display:grid;place-items:center;width:27px;height:27px;border:1px solid #8e7049;color:var(--gold)}.classified{color:#777}.classified span{color:var(--red);margin-left:8px}.landing-content{position:relative;z-index:2;width:min(660px,90vw);margin:7vh auto 55px;text-align:center}.eyebrow,.chapter-kicker{font:10px var(--mono);letter-spacing:.16em;color:var(--gold);display:flex;align-items:center;gap:12px}.eyebrow{justify-content:center}.eyebrow span{width:25px;height:1px;background:#8c704d}.hero-title{font:clamp(43px,8vw,82px)/1.05 var(--serif);letter-spacing:-.04em;margin:30px 0 17px;color:#f1ece2}.hero-title em,.case-title em,.chapter h1 em{color:var(--gold2);font-weight:400}.hero-copy{max-width:490px;margin:0 auto;color:#a8a4a0;font-size:14px;line-height:1.8}.hero-stamp{margin:30px auto 25px;display:flex;align-items:center;justify-content:center;gap:14px;color:#857d72;font:9px var(--mono);letter-spacing:.12em}.hero-stamp b{font:32px var(--serif);color:var(--gold);border:1px solid #5a4a37;padding:5px 13px}.access-panel{max-width:410px;margin:auto;text-align:left;padding:23px 25px 21px;background:#111218e8;border:1px solid #37343a;box-shadow:0 18px 70px #0008;position:relative}.access-panel:before{content:"";position:absolute;top:-1px;left:25px;width:55px;height:1px;background:var(--gold)}.panel-top{display:flex;justify-content:space-between;gap:8px;font:9px var(--mono);letter-spacing:.08em;color:#999;margin-bottom:25px}.panel-top span:last-child{display:flex;align-items:center;gap:5px;color:#777}.access-panel label{display:block;font:9px var(--mono);letter-spacing:.12em;color:#aaa;margin-bottom:9px}.access-panel input,.join-row input{width:100%;background:#090a0e;border:1px solid #35353b;color:#eee;padding:13px 12px;outline:none;font:12px var(--mono);letter-spacing:.06em}.access-panel input:focus,.join-row input:focus{border-color:var(--gold)}.primary-button{display:flex;align-items:center;justify-content:center;gap:12px;background:var(--gold);border:1px solid var(--gold);color:#17130e;padding:13px 17px;font:10px var(--mono);letter-spacing:.1em;transition:.2s}.primary-button:hover:not(:disabled){background:var(--gold2);transform:translateY(-1px)}.access-panel>.primary-button{width:100%;margin-top:12px}.or{display:flex;align-items:center;gap:10px;justify-content:center;margin:22px 0 14px;color:#777;font:9px var(--mono);letter-spacing:.1em}.or span{height:1px;flex:1;background:#34343a}.join-row{display:flex;gap:8px}.join-row input{min-width:0;text-align:center;letter-spacing:.22em}.join-row button{display:flex;align-items:center;gap:10px;padding:0 15px;background:transparent;border:1px solid #65543c;color:var(--gold);font:10px var(--mono)}.preview-warning,.form-error{display:flex;gap:8px;align-items:center;margin-top:14px;font-size:11px;color:#c29a6a;line-height:1.5}.form-error{color:#d18c84}.landing-foot{display:flex;justify-content:center;gap:26px;margin-top:25px;color:#777;font:9px var(--mono);letter-spacing:.08em}.landing-foot span{display:flex;align-items:center;gap:7px}.landing-watermark{position:absolute;right:-25px;bottom:-110px;font:340px/.8 var(--serif);color:#ffffff05;pointer-events:none}.landing-bottom{position:absolute;bottom:0;left:0;right:0;border-top:1px solid #ffffff12;color:#626168;font-size:9px}.game-shell{min-height:100vh;background:#0d0e12}.topbar{height:61px;border-bottom:1px solid var(--line);display:flex;align-items:center;justify-content:space-between;padding:0 27px;background:#101116}.top-center{display:flex;align-items:center;gap:9px;font:9px var(--mono);letter-spacing:.1em;color:#999}.live-dot,.online-dot{width:6px;height:6px;border-radius:50%;background:#82a987;box-shadow:0 0 9px #82a98788}.top-divider{height:12px;width:1px;background:#444}.icon-button{background:transparent;border:1px solid #383840;color:#aaa;width:31px;height:31px;display:grid;place-items:center}.progress-track{height:2px;background:#25252b}.progress-fill{height:100%;background:var(--gold);transition:width .5s}.game-layout{display:grid;grid-template-columns:230px minmax(0,1fr) 235px;max-width:1500px;margin:auto;min-height:calc(100vh - 63px)}.sidebar,.right-rail{padding:30px 22px;border-right:1px solid var(--line);position:relative;background:#101116}.right-rail{border-right:0;border-left:1px solid var(--line)}.case-label,.rail-heading,.players-title,.sidebar-bottom,.case-meta,.status-card>span,.room-card>span,.identity-card small,.player-line small{font:9px var(--mono);letter-spacing:.12em;color:#777}.case-title{font:28px/1.05 var(--serif);margin:14px 0 13px}.case-meta{display:flex;flex-direction:column;gap:5px;font-size:8px}.side-rule{height:1px;background:var(--line);margin:24px 0}.players-title{display:flex;align-items:center;gap:8px;margin-bottom:14px}.player-line{display:flex;align-items:center;gap:10px;margin:12px 0}.avatar{width:29px;height:29px;display:grid;place-items:center;border:1px solid #776143;color:var(--gold);font:11px var(--mono);background:#30281d}.avatar.witness{border-color:#667b85;color:#9db8c2;background:#1d292e}.player-line b,.identity-card b{display:block;font-size:11px;font-weight:500}.player-line small,.identity-card small{display:block;font-size:8px;margin-top:4px}.online-dot{margin-left:auto}.waiting-player{font-size:10px;color:#8d8985;display:flex;align-items:center;gap:8px;margin-top:18px}.pulse{width:6px;height:6px;border-radius:50%;background:var(--gold);animation:pulse 1.4s infinite}@keyframes pulse{50%{opacity:.25;box-shadow:0 0 0 5px #c9a66b22}}.nav-list{display:grid;gap:5px}.nav-list button{display:flex;align-items:center;gap:10px;text-align:left;padding:11px 9px;background:transparent;border:0;color:#85858b;font-size:11px}.nav-list button.active{background:#222027;color:var(--gold);border-left:2px solid var(--gold)}.nav-list button svg:last-child,.nav-count{margin-left:auto}.nav-count{font:9px var(--mono);color:#888}.sidebar-bottom{position:absolute;bottom:25px;line-height:2;color:#9b8c72}.sidebar-bottom small{color:#666}.main-content{padding:42px clamp(24px,5vw,75px) 70px;min-width:0}.chapter{max-width:780px;margin:auto}.chapter-kicker{justify-content:space-between;border-bottom:1px solid var(--line);padding-bottom:14px;font-size:9px}.chapter-kicker span{color:#777}.chapter h1{font:clamp(39px,5vw,61px)/1.08 var(--serif);letter-spacing:-.035em;margin:27px 0 17px;font-weight:400}.chapter-lead{max-width:650px;color:#aaa8a5;font-size:13px;line-height:1.9;margin-bottom:28px}.cinema-image{height:210px;position:relative;overflow:hidden;background:linear-gradient(90deg,#141314aa,#14131422),linear-gradient(0deg,#0a0a0d 0%,transparent 60%),url("https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=1400&q=80") center 52%/cover;border:1px solid #39343a;filter:saturate(.55)}.cinema-image:after{content:"";position:absolute;inset:0;background:repeating-linear-gradient(0deg,transparent,transparent 3px,#0002 4px)}.image-caption{position:absolute;top:14px;left:15px;z-index:1;font:9px var(--mono);letter-spacing:.1em;color:#c7b89e}.image-overlay-text{position:absolute;bottom:18px;left:20px;z-index:1;font:clamp(18px,3vw,27px) var(--serif);letter-spacing:.15em;color:#e6d9c5}.document-quote{margin:23px 0;padding:18px 22px;border-left:2px solid var(--gold);background:#c9a66b0b}.document-quote>span,.document-quote small{font:9px var(--mono);letter-spacing:.1em;color:#a28a65}.document-quote p{font:19px/1.55 var(--serif);color:#d8d0c3;margin:12px 0}.briefing-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:22px 0}.briefing-grid>div,.status-card,.room-card,.identity-card{padding:15px;background:#14151b;border:1px solid #2e2e35}.briefing-grid span{display:block;font:9px var(--mono);color:var(--gold);letter-spacing:.1em;margin-bottom:9px}.briefing-grid b{font:16px var(--serif);font-weight:400}.briefing-grid p{font-size:11px;line-height:1.7;color:#888;margin:8px 0 0}.wide{width:100%}.rail-heading{display:flex;justify-content:space-between;align-items:center}.status-card{margin-top:13px}.status-number{font:34px var(--serif);color:var(--gold);margin-bottom:3px}.status-number small{font-size:14px;color:#777}.status-card>span{font-size:8px}.mini-track{height:2px;background:#303037;margin-top:13px}.mini-track div{height:100%;background:var(--gold)}.spaced{margin-top:27px;margin-bottom:12px}.room-card{display:grid;gap:9px}.room-card strong{font:25px var(--mono);letter-spacing:.18em;color:var(--gold2)}.room-card button{display:flex;align-items:center;gap:7px;background:transparent;border:0;color:#999;padding:0;font:9px var(--mono)}.identity-card{display:flex;align-items:center;gap:11px}.avatar.large{width:35px;height:35px}.private-note{display:flex;gap:9px;margin-top:18px;color:#9a8d79;font-size:10px;line-height:1.6}.private-note svg{flex:none}.small-error{color:#d28d85;font-size:10px;margin-top:15px}.evidence-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin:20px 0}.evidence-card{display:flex;flex-direction:column;text-align:left;background:#15161c;border:1px solid #34343b;padding:0;color:#ddd;min-width:0;transition:.2s}.evidence-card:hover{border-color:#98794f;transform:translateY(-2px)}.evidence-card.found{border-color:#6d765e}.evidence-thumb{height:95px;display:flex;align-items:center;justify-content:center;position:relative;color:#9e8b6c;background:linear-gradient(135deg,#28251f,#15161b);border-bottom:1px solid #333}.evidence-thumb:after{content:"";position:absolute;inset:0;background:repeating-linear-gradient(0deg,transparent,transparent 4px,#0002 5px)}.evidence-thumb span{position:absolute;top:9px;left:10px;font:9px var(--mono);color:#aaa}.evidence-info{display:grid;gap:6px;padding:12px}.evidence-info small{font:8px var(--mono);letter-spacing:.08em;color:var(--gold)}.evidence-info b{font:15px var(--serif);font-weight:400}.evidence-info span{font:8px var(--mono);color:#777}.evidence-status{display:flex;align-items:center;gap:6px;padding:9px 12px;border-top:1px solid #2c2d32;color:#8c8a85;font:8px var(--mono);letter-spacing:.08em}.alert-strip{display:flex;gap:10px;padding:13px 14px;background:#c9a66b0d;border:1px solid #5a4934;color:#b7a68b;font-size:10px;line-height:1.6}.alert-strip svg{flex:none;color:var(--gold)}.chapter-footer{display:flex;justify-content:space-between;align-items:center;gap:15px;margin-top:18px;font:9px var(--mono);color:#777}.muted-note{font-size:10px;color:#777;line-height:1.7;margin-top:14px}.modal-backdrop{position:fixed;inset:0;z-index:10;background:#050609d9;display:grid;place-items:center;padding:20px}.evidence-modal{position:relative;width:min(560px,100%);padding:30px;background:#e6dfcf;color:#29251e;box-shadow:0 20px 80px #000b}.modal-close{position:absolute;right:16px;top:16px;background:transparent;border:0;color:#51493e}.modal-type,.modal-date,.modal-foot{font:9px var(--mono);letter-spacing:.1em;color:#75664f}.modal-type{display:flex;justify-content:space-between;gap:10px}.modal-type span{color:#9c564c}.evidence-modal h2{font:32px var(--serif);font-weight:400;margin:25px 0 7px}.document-body{margin:30px 0;padding:22px 17px;border:1px solid #bdb29c;background:#f1ebdc;font:20px/1.8 var(--serif);min-height:130px}.modal-foot{display:flex;justify-content:space-between;align-items:center;border-top:1px solid #bdb29c;padding-top:15px;font-size:8px}.text-button{display:flex;align-items:center;gap:8px;background:transparent;border:0;color:#b89a6c;font:9px var(--mono);letter-spacing:.08em}.transcript{border:1px solid #36353b;background:#13141a;margin:25px 0}.transcript-head{display:flex;justify-content:space-between;padding:13px 16px;border-bottom:1px solid #333;font:9px var(--mono);color:#8d8b88}.transcript-head span:first-child{display:flex;align-items:center;gap:8px;color:var(--gold)}.speaker{padding:15px 18px 4px}.speaker.reply{padding-top:8px}.speaker-tag{font:8px var(--mono);letter-spacing:.12em;color:var(--gold)}.speaker p{font:17px/1.6 var(--serif);color:#d2ccc1;margin:8px 0}.speaker.reply p{color:#aaa}.waveform{height:55px;display:flex;align-items:center;justify-content:center;gap:3px;padding:0 18px 12px}.waveform i{width:2px;background:#92764e;opacity:.65}.question-block{margin-top:25px}.question-block>span{font:9px var(--mono);color:var(--gold);letter-spacing:.12em}.question-block h3{font:23px var(--serif);font-weight:400}.choice-row,.theory-card{width:100%;display:flex;align-items:center;gap:12px;text-align:left;padding:13px 14px;background:#15161c;border:1px solid #33343a;color:#c7c3bc;margin:8px 0;font-size:11px}.choice-row.selected,.theory-card.selected{border-color:var(--gold);background:#c9a66b10}.choice-radio{width:13px;height:13px;border:1px solid #777;border-radius:50%;flex:none}.selected .choice-radio{border:4px solid var(--gold)}.success-note{display:flex;gap:8px;align-items:center;margin:13px 0;padding:11px;background:#86ad9110;border:1px solid #536d55;color:#9db89e;font-size:10px}.timeline-puzzle{border:1px solid #36353b;background:#13141a;padding:17px}.timeline-progress{display:flex;justify-content:space-between;gap:10px;padding-bottom:13px;border-bottom:1px solid #333;font:9px var(--mono);color:var(--gold)}.timeline-picked{display:flex;align-items:center;gap:12px;padding:13px 9px;border-bottom:1px solid #292a30;font-size:11px;color:#c8c3b8}.timeline-picked span{font:10px var(--mono);color:var(--gold)}.timeline-picked svg{margin-left:auto;color:var(--green)}.timeline-options{display:grid;gap:8px;margin-top:14px}.timeline-options button{display:grid;grid-template-columns:18px 1fr auto;align-items:center;gap:9px;text-align:left;background:#1a1b22;border:1px solid #33343a;color:#bbb;padding:12px;font-size:10px}.timeline-options button:hover{border-color:#8b7049}.timeline-options button>span{font:16px var(--mono);color:var(--gold)}.timeline-options small{font:8px var(--mono);color:#777}.hint-button{margin:15px 0}.hint-button span{color:#777;margin-left:8px}.hint-card{display:flex;gap:9px;padding:12px;background:#c9a66b10;color:#c5ad84;font-size:11px;line-height:1.6}.theory-block{margin-top:35px;padding-top:25px;border-top:1px solid #39383e}.theory-block h2{font:30px var(--serif);font-weight:400;margin:20px 0 5px}.theory-card{align-items:flex-start}.theory-card>div b{font:16px var(--serif);font-weight:400}.theory-card p{font-size:10px;line-height:1.6;color:#89878a;margin:6px 0 0}.journal-stat-grid,.ending-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:25px 0}.journal-stat-grid>div,.ending-stats>div{padding:15px;background:#15161c;border:1px solid #333}.journal-stat-grid b,.ending-stats b{display:block;font:30px var(--serif);color:var(--gold)}.journal-stat-grid span,.ending-stats span{font:8px var(--mono);color:#888;letter-spacing:.08em}.journal-entry{padding:19px;margin:12px 0;background:#15161c;border-left:2px solid #8c704d}.journal-entry>span{font:8px var(--mono);color:var(--gold);letter-spacing:.1em}.journal-entry h3{font:20px var(--serif);font-weight:400;margin:11px 0}.journal-entry p{font-size:12px;color:#aaa;line-height:1.8;margin:0}.ending-screen{max-width:680px;margin:30px auto;text-align:center}.ending-symbol{width:76px;height:76px;border:1px solid #7d6748;color:var(--gold);display:grid;place-items:center;border-radius:50%;margin:0 auto 25px}.ending-screen .chapter-kicker{justify-content:center}.ending-screen h1{white-space:pre-line;font:clamp(42px,6vw,65px)/1.08 var(--serif);font-weight:400;margin:30px 0 20px}.ending-line{width:60px;height:1px;background:var(--gold);margin:0 auto 25px}.ending-screen h2{font:24px var(--serif);font-weight:400;color:var(--gold2)}.ending-screen>p{max-width:500px;margin:0 auto;color:#aaa;line-height:1.9;font-size:13px}.ending-screen blockquote{font:20px/1.6 var(--serif);color:#d0c5b2;border-top:1px solid #39383e;border-bottom:1px solid #39383e;padding:23px;margin:25px 0}.ending-screen>.primary-button{margin:auto}.mobile-room{display:none}
@media(max-width:1050px){.game-layout{grid-template-columns:190px minmax(0,1fr)}.right-rail{display:none}.main-content{padding:35px 35px 60px}}
@media(max-width:700px){.landing-top,.landing-bottom{padding:18px 17px}.classified{display:none}.landing-content{margin:7vh auto 70px}.landing-foot{gap:10px;flex-wrap:wrap;font-size:8px}.landing-bottom{font-size:7px}.game-layout{display:block}.sidebar{display:none}.main-content{padding:25px 18px 55px}.topbar{padding:0 16px}.top-center{font-size:8px}.mobile-room{display:flex;justify-content:space-between;color:#888;font:9px var(--mono);margin-bottom:20px}.chapter h1{font-size:43px}.briefing-grid,.evidence-grid{grid-template-columns:1fr 1fr}.evidence-thumb{height:75px}.evidence-info{padding:10px}.evidence-info b{font-size:13px}.chapter-footer{align-items:flex-start;flex-direction:column}.chapter-footer .primary-button{width:100%}.panel-top{font-size:8px}.document-body{font-size:17px}.modal-foot{gap:10px}.modal-foot span{font-size:7px}.modal-foot button{font-size:7px}.timeline-options button{grid-template-columns:18px 1fr}.timeline-options small{grid-column:2}.ending-stats b{font-size:24px}}
@media(max-width:390px){.briefing-grid,.evidence-grid{grid-template-columns:1fr}.hero-title{font-size:42px}.access-panel{padding:19px}.landing-foot{font-size:7px}}
'''

for rel, content in files.items():
    path = os.path.join(base, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(textwrap.dedent(content).lstrip())

zip_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "arsip-07-online.zip")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    for root, dirs, names in os.walk(base):
        for name in names:
            p = os.path.join(root, name)
            z.write(p, os.path.relpath(p, os.path.dirname(base)))

print(f"Created {len(files)} project files")
print(zip_path)
