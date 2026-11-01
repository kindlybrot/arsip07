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
  isHost: boolean
  revision: number
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

function mergeGame(current: GameState, patch: Partial<GameState>): GameState {
  return {
    ...current,
    ...patch,
    stage: Math.max(current.stage, patch.stage ?? current.stage),
    evidenceOpened: [...new Set([...current.evidenceOpened, ...(patch.evidenceOpened ?? [])])],
    timelineSolved: current.timelineSolved || Boolean(patch.timelineSolved),
    hints: Math.max(current.hints, patch.hints ?? current.hints),
    started: current.started || Boolean(patch.started),
    ended: current.ended || Boolean(patch.ended),
    witnessChoice: current.witnessChoice || patch.witnessChoice || '',
  }
}

export const useGame = create<Store>((set, get) => ({
  game: initial, room: '', player: null, players: [], online: Boolean(supabase), connected: false, isHost: false, revision: 0, channel: null, error: '',
  setError: (error) => set({ error }),
  connectRoom: async (requestedRoom, name, createRoom) => {
    if (!supabase) {
      const code = createRoom ? roomCode() : requestedRoom.trim().toUpperCase()
      const localPlayer = { id: playerId(), name, role: 'analyst' as const }
      set({ room: code, player: localPlayer, players: [{ ...localPlayer, id: 'local' }], connected: true, isHost: true, revision: 0, game: initial, error: 'Mode preview aktif: isi Supabase URL dan publishable key untuk multiplayer online.' })
      return
    }
    const code = createRoom ? roomCode() : requestedRoom.trim().toUpperCase()
    const id = playerId()
    const role: PlayerRole = createRoom ? 'analyst' : 'witness'
    const channel = supabase.channel(`arsip-room:${code}`, {
      config: { broadcast: { self: false }, presence: { key: id } },
    })
    const player: Player = { id, name, role }
    let requestedState = false
    set({ room: code, player, players: [], channel, connected: false, isHost: createRoom, revision: 0, game: initial, error: '' })

    channel.on('presence', { event: 'sync' }, () => {
      if (get().channel !== channel) return
      const state = channel.presenceState<Player>()
      const peers = Object.values(state).flat()
      const unique = [...new Map(peers.map(p => [p.id, p])).values()]
      const assigned = unique.sort((a, b) => a.role === b.role ? a.id.localeCompare(b.id) : a.role === 'analyst' ? -1 : 1)
      if (assigned.length > 2 && !createRoom) {
        if (supabase) supabase.removeChannel(channel)
        set({ game: initial, room: '', player: null, players: [], connected: false, isHost: false, revision: 0, channel: null, error: 'Room sudah penuh. Satu room hanya dapat diisi dua pemain.' })
        return
      }
      set({ players: assigned.slice(0, 2), player: assigned.find(p => p.id === id) ?? player, error: assigned.length > 2 ? 'Room penuh. Pemain ketiga tidak dapat bergabung.' : '' })
      if (!createRoom && assigned.some(p => p.role === 'analyst') && !requestedState) {
        requestedState = true
        channel.send({ type: 'broadcast', event: 'request_state', payload: { from: id } })
      }
    })
    channel.on('broadcast', { event: 'game_state' }, ({ payload }) => {
      if (get().channel !== channel || createRoom || !payload?.state) return
      const incomingRevision = Number(payload.revision) || 0
      if (incomingRevision >= get().revision) set({ game: payload.state as GameState, revision: incomingRevision })
    })
    channel.on('broadcast', { event: 'request_state' }, () => {
      if (get().channel === channel && createRoom) {
        channel.send({ type: 'broadcast', event: 'game_state', payload: { state: get().game, revision: get().revision } })
      }
    })
    channel.on('broadcast', { event: 'game_action' }, ({ payload }) => {
      if (get().channel !== channel || !createRoom || !payload?.patch) return
      const next = mergeGame(get().game, payload.patch as Partial<GameState>)
      const revision = get().revision + 1
      set({ game: next, revision })
      channel.send({ type: 'broadcast', event: 'game_state', payload: { state: next, revision } })
    })
    channel.subscribe(async (status) => {
      if (status === 'SUBSCRIBED') {
        try {
          await channel.track({ ...player, joinedAt: new Date().toISOString() })
          if (get().channel === channel) set({ connected: true })
        } catch {
          if (get().channel === channel) set({ error: 'Gagal mendaftarkan pemain ke room. Coba muat ulang halaman.' })
        }
      } else if (status === 'CHANNEL_ERROR' || status === 'TIMED_OUT') {
        if (get().channel === channel) set({ connected: false, error: 'Koneksi room gagal. Periksa URL dan key Supabase, lalu coba gabung lagi.' })
      }
    })
  },
  updateGame: (patch) => {
    const { channel, connected, isHost } = get()
    if (!channel || !connected) {
        set({ game: mergeGame(get().game, patch) })
      return
    }
    if (!isHost) {
      channel.send({ type: 'broadcast', event: 'game_action', payload: { patch } })
      return
    }
    const next = mergeGame(get().game, patch)
    const revision = get().revision + 1
    set({ game: next, revision })
    channel.send({ type: 'broadcast', event: 'game_state', payload: { state: next, revision } })
  },
  leave: () => {
    const { channel } = get()
    if (channel && supabase) supabase.removeChannel(channel)
    set({ game: initial, room: '', player: null, players: [], connected: false, isHost: false, revision: 0, channel: null, error: '' })
  },
}))
