import { useEffect, useMemo, useState } from 'react'
import './gameplay.css'
import { AnimatePresence, motion } from 'motion/react'
import { Archive, ArrowDown, ArrowLeft, ArrowRight, AudioLines, BookOpen, Check, ChevronRight, CircleHelp, Clipboard, Clock3, Copy, Eye, Fingerprint, FileText, LockKeyhole, Menu, MessageSquare, Radio, RotateCcw, Shield, Sparkles, Users, X } from 'lucide-react'
import { evidence, timeline, correctTimeline, theories } from './data/story'
import { useGame, type GameState } from './store/game'
import { isOnlineConfigured } from './lib/supabase'

const slide = { initial: { opacity: 0, y: 14 }, animate: { opacity: 1, y: 0 }, exit: { opacity: 0, y: -10 } }

function App() {
  const { game, room, player, players, connected, error, connectRoom, updateGame, leave, setError } = useGame()
  const [name, setName] = useState('')
  const [roomInput, setRoomInput] = useState('')
  const [tab, setTab] = useState<'case'|'evidence'|'journal'>('case')
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [selectedEvidence, setSelectedEvidence] = useState<string | null>(null)
  const [timelineFeedback, setTimelineFeedback] = useState('')
  const [theory, setTheory] = useState('')
  const [copied, setCopied] = useState(false)

  const opened = evidence.filter(e => game.evidenceOpened.includes(e.id))
  const selectedOrder = game.timelineOrder
  const currentEvidence = evidence.find(e => e.id === selectedEvidence)
  const visibleEvidence = useMemo(() => evidence.filter(e => !e.privateTo || e.privateTo === player?.role), [player?.role])
  const progress = Math.min(100, Math.round((game.evidenceOpened.length / evidence.length) * 55 + (game.timelineSolved ? 20 : 0) + (game.witnessChoice ? 10 : 0) + (game.ended ? 15 : 0)))

  useEffect(() => { setSelectedEvidence(null) }, [game.stage])

  const create = async () => {
    if (!name.trim()) return setError('Masukkan nama panggilan terlebih dahulu.')
    await connectRoom('', name.trim(), true)
  }
  const join = async () => {
    if (!name.trim() || roomInput.trim().length !== 6) return setError('Masukkan nama dan kode room 6 karakter.')
    await connectRoom(roomInput, name.trim(), false)
  }
  const begin = () => updateGame({ started: true, stage: 2 })
  const openEvidence = (id: string) => {
    const next = [...new Set([...game.evidenceOpened, id])]
    updateGame({ evidenceOpened: next })
    setSelectedEvidence(id)
  }
  const addTimeline = (id: string) => {
    if (selectedOrder.includes(id)) return
    const next = [...selectedOrder, id]
    if (next.length === 4) {
      const correct = next.every((v, i) => v === correctTimeline[i])
      if (correct) updateGame({ timelineOrder: next, timelineSolved: true, stage: 4 })
      else { updateGame({ timelineOrder: [] }); setTimelineFeedback('Urutannya belum cocok. Baca lagi jam pada bukti dan coba susun ulang.') }
    } else { updateGame({ timelineOrder: next }); setTimelineFeedback('') }
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
  const reset = () => { leave(); setTheory(''); setTimelineFeedback(''); setTab('case'); setMobileMenuOpen(false) }

  if (!room || !player) {
    return <Landing name={name} setName={setName} roomInput={roomInput} setRoomInput={setRoomInput} create={create} join={join} error={error} online={isOnlineConfigured} />
  }

  const isSecond = player.role === 'witness'
  return (
    <div className="game-shell">
      <header className="topbar">
        <button className="icon-button mobile-menu-button" onClick={()=>setMobileMenuOpen(true)} aria-label="Buka menu navigasi" aria-expanded={mobileMenuOpen} title="Buka menu"><Menu size={19}/></button>
        <div className="brand"><span className="brand-mark"><Archive size={16}/></span><span>DEPARTEMEN ARSIP <b>/</b> 07</span></div>
        <div className="top-center"><span className={`live-dot ${connected ? '' : 'offline'}`}/>{error ? 'CONNECTION ISSUE' : connected ? 'ROOM ONLINE' : 'CONNECTING'} <span className="top-divider"/> ROOM {room}</div>
        <button className="icon-button" onClick={reset} title="Keluar dari room"><X size={17}/></button>
      </header>
      <div className="progress-track"><div className="progress-fill" style={{ width: `${progress}%` }}/></div>
      <div className="game-layout">
        {mobileMenuOpen&&<button className="sidebar-backdrop" onClick={()=>setMobileMenuOpen(false)} aria-label="Tutup menu navigasi"/>}
        <aside className={`sidebar ${mobileMenuOpen?'mobile-open':''}`}>
          <div className="mobile-sidebar-header"><span>ARSIP 07 / MENU</span><button className="icon-button" onClick={()=>setMobileMenuOpen(false)} aria-label="Tutup menu"><X size={17}/></button></div>
          <div className="case-label">CURRENT CASE</div>
          <div className="case-title">THE MISSING<br/><em>MEMORY</em></div>
          <div className="case-meta"><span>CASE NO. 07-1998</span><span>CLASSIFIED</span></div>
          <div className="side-rule"/>
          <div className="players-title"><Users size={13}/> INVESTIGATORS</div>
          {players.map((p, i) => <div className="player-line" key={p.id}><span className={`avatar ${p.role}`}>{p.role === 'analyst' ? 'A' : 'W'}</span><span><b>{p.name}</b><small>{p.role === 'analyst' ? 'THE ANALYST' : 'THE WITNESS'}</small></span><span className="online-dot"/></div>)}
          {players.length < 2 && <div className="waiting-player"><span className="pulse"/> Menunggu pemain kedua…</div>}
          <div className="side-rule"/>
          <div className="nav-list">
            <button className={tab==='case'?'active':''} onClick={()=>{setTab('case');setMobileMenuOpen(false)}}><Archive size={15}/> Case file <ChevronRight size={14}/></button>
            <button className={tab==='evidence'?'active':''} onClick={()=>{setTab('evidence');setMobileMenuOpen(false)}}><Fingerprint size={15}/> Evidence board <span className="nav-count">{opened.length}</span></button>
            <button className={tab==='journal'?'active':''} onClick={()=>{setTab('journal');setMobileMenuOpen(false)}}><BookOpen size={15}/> Field journal</button>
          </div>
          <div className="sidebar-bottom"><Shield size={14}/> PRIVATE INVESTIGATION SESSION<br/><small>Do not distribute case materials.</small></div>
        </aside>

        <main className="main-content">
          <div className="mobile-room"><span>ROOM {room}</span><span>{players.length}/2 INVESTIGATORS</span></div>
          <RoomStatus players={players} connected={connected} error={error}/>
          <ObjectiveBar game={game}/>
          {tab === 'evidence' ? <motion.div key="evidence" {...slide}><EvidenceBoard items={visibleEvidence} opened={game.evidenceOpened} open={openEvidence}/></motion.div>
              : tab === 'journal' ? <motion.div key="journal" {...slide}><Journal game={game} role={player.role} /></motion.div>
              : <motion.div key={`stage-${game.stage}-${game.ended}`} {...slide}>
                {!game.started ? <Briefing begin={begin} players={players.length} role={player.role} online={Boolean(isOnlineConfigured)} connected={connected} />
                  : game.ended ? <Ending theory={game.theory} hints={game.hints} artifacts={game.evidenceOpened.length} reset={reset}/>
                  : game.stage <= 2 ? <EvidenceChapter items={visibleEvidence} opened={game.evidenceOpened} open={openEvidence} role={player.role} next={() => updateGame({stage:3})}/>
                  : game.stage === 3 ? <WitnessChapter choice={game.witnessChoice} choose={(v)=>updateGame({witnessChoice:v,stage:4})} role={player.role}/>
                  : game.stage === 4 ? <TimelineChapter selected={selectedOrder} add={addTimeline} solved={game.timelineSolved} theory={theory} setTheory={setTheory} submit={submitTheory} hint={()=>updateGame({hints:game.hints+1})} hintUsed={game.hints > 0} feedback={timelineFeedback}/>
                  : null}
                </motion.div>}
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

function RoomStatus({players,connected,error}:{players:{id:string;name:string;role:string}[];connected:boolean;error:string}) {
  return <section className={`room-status-strip ${error?'has-error':''}`} aria-live="polite">
    <div className="room-status-heading"><span className={`live-dot ${connected?'':'offline'}`}/><b>{error?'KONEKSI BERMASALAH':connected?'ROOM TERHUBUNG':'MENGHUBUNGKAN KE ROOM'}</b><span>{players.length}/2 PEMAIN</span></div>
    <div className="room-status-players">
      {players.map(p=><span className="room-player-chip" key={p.id}><i className={`avatar ${p.role}`}>{p.role==='analyst'?'A':'W'}</i><span><b>{p.name}</b><small>{p.role==='analyst'?'ANALYST':'WITNESS'}</small></span></span>)}
      {players.length<2&&<span className="room-waiting">{connected?'Bagikan kode room agar pasanganmu bisa bergabung.':'Status pemain akan muncul setelah koneksi tersambung.'}</span>}
    </div>
    {error&&<p>{error}</p>}
  </section>
}

function ObjectiveBar({game}:{game:GameState}) {
  const objective = !game.started ? ['SEBELUM MULAI','Baca tutorial, lalu pastikan dua pemain sudah terhubung.']
    : game.ended ? ['KASUS SELESAI','Baca kesimpulan akhir dan bandingkan teori kalian.']
      : game.stage <= 2 ? ['OBJEKTIF 1/3',`Buka minimal 4 dari 6 bukti bersama (${game.evidenceOpened.length}/6). Bukti privat perlu dibagikan lewat diskusi.`]
        : game.stage === 3 ? ['OBJEKTIF 2/3','Diskusikan rekaman saksi, pilih satu interpretasi, lalu rekam jawaban.']
          : game.timelineSolved ? ['OBJEKTIF 3/3','Pilih teori yang paling cocok dengan bukti, lalu kirim deduksi akhir.']
            : ['OBJEKTIF 3/3','Susun empat kejadian dari waktu paling awal ke paling akhir.']
  return <section className="objective-bar"><div><span>{objective[0]}</span><b>{objective[1]}</b></div><div className="objective-mark"><Check size={15}/></div></section>
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

function Briefing({begin,players,role,online,connected}:{begin:()=>void;players:number;role:string;online:boolean;connected:boolean}) {
  const canBegin = !online || (connected && players === 2 && role === 'analyst')
  return <section className="chapter">
    <div className="chapter-kicker">01 / CASE OPENING <span>14 OCTOBER 1998</span></div>
    <h1>The room remembers<br/><em>what you forgot.</em></h1>
    <p className="chapter-lead">Pukul 02:17 dini hari, sebuah amplop tiba di kantor arsip. Tidak ada pengirim. Hanya dua nama penyelidik yang tertulis di bagian depan—nama kalian.</p>
    <div className="cinema-image"><div className="image-caption">FIG. 01 — THE ARCHIVE ROOM, 1998</div><div className="image-overlay-text">SOMEONE WAS HERE.</div></div>
    <div className="document-quote"><span>TRANSCRIPT / ENVELOPE CONTENT</span><p>“Kalian pernah berada di ruangan itu. Kalian berdua. Tetapi hanya satu dari kalian yang mengingat malam tersebut dengan benar.”</p><small>— UNKNOWN AUTHOR</small></div>
    <div className="briefing-grid"><div><span>TUJUAN KASUS</span><b>Rekonstruksi malam yang hilang.</b><p>Buka bukti, bandingkan dua versi ingatan, susun kronologi, lalu pilih teori akhir.</p></div><div><span>STATUS PARTNER</span><b>{players}/2 penyelidik terhubung</b><p>{players < 2 ? 'Bagikan kode room dari panel kanan. Tunggu nama partner muncul sebelum host memulai.' : 'Kalian berdua siap. Analyst memulai kasus; Witness bergabung sebagai partner.'}</p></div></div>
    <div className="tutorial-panel"><div className="tutorial-title"><BookOpen size={16}/><span><small>PANDUAN PEMAIN</small><b>Cara bermain sampai kasus selesai</b></span></div>
      <ol><li><b>Masuk berdua.</b> Analyst membuat room dan membagikan kode; Witness membuka game di perangkat lain lalu memasukkan kode yang sama.</li>
        <li><b>Bandingkan bukti.</b> Buka bukti di papan. Minimal 4 dari 6 harus dibuka untuk lanjut. Laporan klinik hanya milik Analyst, kartu pos hanya milik Witness; ceritakan isinya satu sama lain.</li>
        <li><b>Sepakati kesaksian.</b> Baca transkrip, diskusikan maknanya, lalu salah satu pemain merekam satu interpretasi.</li>
        <li><b>Susun kronologi.</b> Urutkan empat peristiwa dari yang paling awal. Kalau salah, urutannya dikosongkan dan bisa dicoba lagi. Satu petunjuk tersedia.</li>
        <li><b>Tutup kasus.</b> Pilih teori akhir dan kirim deduksi. Teori “Ingatan itu milik kalian” membuka kesimpulan paling lengkap.</li></ol>
      <div className="tutorial-note"><MessageSquare size={14}/> Game ini kooperatif: bicarakan bukti privat lewat panggilan atau tatap muka, jangan berharap dokumen privat muncul di layar partner.</div>
    </div>
    <button className="primary-button wide" disabled={!canBegin} onClick={begin}>{role==='witness'&&online?'MENUNGGU HOST MEMULAI':players<2&&online?'MENUNGGU PEMAIN KEDUA':'MULAI INVESTIGASI'} <ArrowRight size={16}/></button>
    {!canBegin&&<p className="muted-note">{connected?'Host Analyst akan bisa memulai setelah kedua nama muncul.':'Sedang menghubungkan ke Supabase. Tunggu status room berubah menjadi terhubung.'}</p>}
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
    <p className="chapter-lead">Buka minimal empat bukti untuk melanjutkan. Baca detailnya, lalu bandingkan dengan partner karena setiap peran memiliki satu dokumen privat.</p>
    <EvidenceBoard items={items} opened={opened} open={open}/>
    <div className="chapter-footer"><span>{count} / 6 PIECES RECOVERED BY THE TEAM</span><button className="primary-button" disabled={count<4} onClick={next}>CONTINUE TO WITNESSES <ArrowRight size={15}/></button></div>
    <p className="muted-note">Setidaknya empat bukti harus dibuka. Untuk mengakses semua detail, minta pasanganmu membacakan bukti privat mereka.</p>
  </section>
}

function EvidenceBoard({items,opened,open}:{items:typeof evidence;opened:string[];open:(id:string)=>void}) {
  return <div className="evidence-grid">{items.map(item=><button className={`evidence-card ${opened.includes(item.id)?'found':''}`} key={item.id} onClick={()=>open(item.id)}>
    <div className="evidence-thumb">{item.type.startsWith('AUDIO')?<AudioLines size={28}/>:item.type.startsWith('FOTOGRAFI')?<Eye size={28}/>:<FileText size={28}/>}<span>{String(evidence.findIndex(e=>e.id===item.id)+1).padStart(2,'0')}</span></div>
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

function TimelineChapter({selected,add,solved,theory,setTheory,submit,hint,hintUsed,feedback}:{selected:string[];add:(id:string)=>void;solved:boolean;theory:string;setTheory:(v:string)=>void;submit:()=>void;hint:()=>void;hintUsed:boolean;feedback:string}) {
  return <section className="chapter">
    <div className="chapter-kicker">05 / RECONSTRUCT THE NIGHT <span>CHRONOLOGY</span></div>
    <h1>Put the night<br/><em>back together.</em></h1>
    <p className="chapter-lead">Susun kejadian berdasarkan bukti yang kalian temukan. Pilih urutan dari kejadian paling awal hingga paling akhir.</p>
    <div className="timeline-puzzle">
      <div className="timeline-progress"><span>SEQUENCE BUILDER</span><span>{solved?'SEQUENCE VERIFIED':`${selected.length}/4 EVENTS PLACED`}</span></div>
      {selected.map((id,i)=><div className="timeline-picked" key={id}><span>{String(i+1).padStart(2,'0')}</span>{timeline.find(t=>t.id===id)?.label}<Check size={14}/></div>)}
      {!solved&&<div className="timeline-options">{timeline.filter(t=>!selected.includes(t.id)).map(t=><button key={t.id} onClick={()=>add(t.id)}><span>+</span><b>{t.label}</b><small>{t.date}</small></button>)}</div>}
      {solved&&<div className="success-note"><Check size={14}/> Timeline reconstructed. The missing sequence is now visible.</div>}
      {feedback&&<div className="form-error timeline-error">{feedback}</div>}
    </div>
    {hintUsed&&<div className="hint-card"><Sparkles size={15}/> Petunjuk: kuitansi mencatat panggilan sebelum foto ruang tunggu. Rekaman kaset dibuat setelah tengah malam.</div>}
    <button className="text-button hint-button" disabled={hintUsed} onClick={hint}><CircleHelp size={14}/> {hintUsed?'PETUNJUK SUDAH DIGUNAKAN':'MINTA SATU PETUNJUK'} <span>{hintUsed?'1/1':'TERSEDIA'}</span></button>
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

function Ending({theory,hints,artifacts,reset}:{theory:string;hints:number;artifacts:number;reset:()=>void}) {
  const found = theories.find(t=>t.id===theory) ?? theories[0]
  const isTrue = theory==='memory'
  return <section className="ending-screen"><div className="ending-symbol"><Fingerprint size={35}/></div><div className="chapter-kicker">CASE CLOSED / 07-1998 <span>{isTrue?'TRUTH RECOVERED':'PARTIAL CONCLUSION'}</span></div><h1>{isTrue?<>The memory<br/>was never lost.</>:<>A version of<br/>the truth.</>}</h1><div className="ending-line"/><h2>{found.title}</h2><p>{found.result}</p><div className="ending-stats"><div><b>{String(artifacts).padStart(2,'0')}</b><span>ARTIFACTS</span></div><div><b>{hints}</b><span>HINTS USED</span></div><div><b>{isTrue?'TRUE':'PARTIAL'}</b><span>CASE STATUS</span></div></div><blockquote>“Ada hal-hal yang kita lupakan untuk bertahan hidup. Dan ada hal-hal yang kita ingat karena akhirnya kita siap menghadapinya.”</blockquote><button className="primary-button" onClick={reset}><RotateCcw size={15}/> RETURN TO ARCHIVE</button></section>
}

export default App
