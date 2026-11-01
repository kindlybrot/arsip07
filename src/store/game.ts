import { create } from 'zustand'
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

function playerId() {
  if (typeof globalThis.crypto?.randomUUID === "function") {
    return globalThis.crypto.randomUUID()
  }

  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, (c) => {
    const r = Math.random() * 16 | 0
    const v = c === "x" ? r : (r & 0x3 | 0x8)
    return v.toString(16)
  })
}

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
      const state = channel.presenceState<Player>()
      const peers = Object.values(state).flat()
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
