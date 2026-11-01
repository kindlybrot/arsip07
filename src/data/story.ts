export type Evidence = {
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
