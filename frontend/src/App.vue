<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue'
const bukuHighlight = {
  judul: 'Re:ZERO -Starting Life in Another World-, Vol. 1',
  penulis: 'Tappei Nagatsuki',
  ilustrator: 'Shinichirou Otsuka',
  kategori: 'Light Novel',
  stok: 2,
  cover: '/images/rezero-vol1.jpg'
}

const daftarBuku = ref([])
const loading = ref(false)
const error = ref('')
const queryPencarian = ref('')
const daftarSection = ref(null)
const arahUrutan = ref('asc')
const formTerbuka = ref(false)
const formBuku = ref({
  judul: '',
  penulis: '',
  kategori: '',
  stok: 0
})
const bukuTersaring = computed(() => {
  const keyword = queryPencarian.value.toLowerCase()

  return daftarBuku.value.filter((buku) => {
    return (
      buku.judul.toLowerCase().includes(keyword) ||
      buku.penulis.toLowerCase().includes(keyword)
    )
  })
})
const bukuDiurutkan = computed(() => {
  const hasil = [...bukuTersaring.value]

  return hasil.sort((a, b) => {
    if (arahUrutan.value === 'asc') {
      return a.judul.localeCompare(b.judul)
    }

    return b.judul.localeCompare(a.judul)
  })
})
const totalBuku = computed(() => {
  return daftarBuku.value.length
})
const stokPerluPerhatian = computed(() => {
  return daftarBuku.value.filter((buku) => {
    return buku.stok <= 3
  }).length
})
const jumlahKategori = computed(() => {
  const kategori = daftarBuku.value.reduce((hasil, buku) => {
    if (!hasil.includes(buku.kategori)) {
      hasil.push(buku.kategori)
    }

    return hasil
  }, [])

  return kategori.length
})
const totalEksemplar = computed(() => {
  return daftarBuku.value.reduce((total, buku) => {
    return total + buku.stok
  }, 0)
})

function statusStok(stok) {
  if (stok === 0) {
    return 'Stok Habis'
  }

  if (stok <= 3) {
    return 'Menipis'
  }

  return 'Tersedia'
}
function classStatus(stok) {
  if (stok === 0) {
    return 'habis'
  }

  if (stok <= 3) {
    return 'menipis'
  }

  return 'tersedia'
}
function gambarBuku(id) {
  return `/images/books/${id}.jpg`
}
function gambarError(event) {
  event.target.style.display = 'none'

  const fallback = event.target.nextElementSibling

  if (fallback) {
    fallback.style.display = 'flex'
  }
}

watch(queryPencarian, async (keyword) => {
  if (keyword.trim() === '') {
    return
  }

  await nextTick()

  daftarSection.value?.scrollIntoView({
    behavior: 'smooth',
    block: 'start'
  })
})

async function ambilBuku() {
  loading.value = true
  error.value = ''

  try {
    const response = await fetch('http://127.0.0.1:8000/buku')

    if (!response.ok) {
      throw new Error('Gagal mengambil data buku')
    }

    daftarBuku.value = await response.json()
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

async function tambahBuku() {
  try {
    const response = await fetch('http://127.0.0.1:8000/buku', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(formBuku.value)
    })

    if (!response.ok) {
      throw new Error('Gagal menambahkan buku')
    }

    formBuku.value = {
      judul: '',
      penulis: '',
      kategori: '',
      stok: 0
    }

    formTerbuka.value = false

    await ambilBuku()
  } catch (err) {
    error.value = err.message
  }
}

async function hapusBuku(id) {
  const konfirmasi = confirm('Yakin ingin menghapus buku ini?')

  if (!konfirmasi) {
    return
  }

  try {
    const response = await fetch(`http://127.0.0.1:8000/buku/${id}`, {
      method: 'DELETE'
    })

    if (!response.ok) {
      throw new Error('Gagal menghapus buku')
    }

    await ambilBuku()
  } catch (err) {
    error.value = err.message
  }
}

onMounted(() => {
  ambilBuku()
})
</script>

<template>
  <div class="page">
    <header class="topbar">
      <div class="brand">
        <div class="brand-icon">P</div>

        <div>
          <h1>Pustaka Amadeus</h1>
          <span>Dashboard Perpustakaan</span>
        </div>
      </div>

      <div class="top-menu">
        <a href="#">Dashboard</a>
        <a href="#">Koleksi</a>
        <a href="#">Tentang</a>
      </div>
    </header>

    <nav class="navbar">
      <button class="category-button">
        ☰ Kategori
      </button>

      <div class="search-box">
        <span class="search-icon">⌕</span>

        <input
          v-model="queryPencarian"
          type="text"
          placeholder="Cari judul buku atau penulis..."
        >
      </div>

      <button
        class="outline-button"
        :class="{ aktif: arahUrutan === 'asc' }"
        @click="arahUrutan = 'asc'"
      >
        Urutkan A-Z
      </button>

      <button
        class="outline-button"
        :class="{ aktif: arahUrutan === 'desc' }"
        @click="arahUrutan = 'desc'"
      >
        Urutkan Z-A
      </button>

      <button
        class="primary-button"
        @click="formTerbuka = !formTerbuka"
      >
        + Tambah Buku
      </button>
    </nav>

      <section v-if="formTerbuka" class="form-wrapper">
        <form class="book-form" @submit.prevent="tambahBuku">
          <div class="form-header">
            <div>
              <h3>Tambah Buku Baru</h3>
              <p>Masukkan informasi buku yang ingin ditambahkan.</p>
            </div>

            <button
              type="button"
              class="close-button"
              @click="formTerbuka = false"
            >
              ✕
            </button>
          </div>

          <div class="form-grid">
            <div class="form-group">
              <label>Judul Buku</label>

              <input
                v-model="formBuku.judul"
                type="text"
                placeholder="Masukkan judul buku"
                required
              >
            </div>

            <div class="form-group">
              <label>Penulis</label>

              <input
                v-model="formBuku.penulis"
                type="text"
                placeholder="Masukkan nama penulis"
                required
              >
            </div>

            <div class="form-group">
              <label>Kategori</label>

              <input
                v-model="formBuku.kategori"
                type="text"
                placeholder="Contoh: Light Novel"
                required
              >
            </div>

            <div class="form-group">
              <label>Stok</label>

              <input
                v-model.number="formBuku.stok"
                type="number"
                min="0"
                required
              >
            </div>
          </div>

          <div class="form-actions">
            <button
              type="button"
              class="outline-button"
              @click="formTerbuka = false"
            >
              Batal
            </button>

            <button
              type="submit"
              class="primary-button"
            >
              Simpan Buku
            </button>
          </div>
        </form>
      </section>

    <main class="container">
<section class="highlight-book">
  <div class="highlight-content">
    <span class="highlight-label">Pilihan Minggu Ini</span>

    <h2>{{ bukuHighlight.judul }}</h2>

    <p class="highlight-author">
      Karya {{ bukuHighlight.penulis }}
    </p>

    <p class="highlight-description">
      Light novel fantasy yang kami jadikan buku unggulan
      di dashboard. Section ini dipakai untuk menampilkan
      satu buku yang ingin lebih ditonjolkan dari koleksi lain.
    </p>

    <div class="highlight-meta">
      <span>{{ bukuHighlight.kategori }}</span>
      <span>Ilustrator: {{ bukuHighlight.ilustrator }}</span>
      <span>Stok: {{ bukuHighlight.stok }}</span>
    </div>

    <div class="highlight-actions">
      <button class="primary-button">Lihat Koleksi</button>
      <button class="outline-button">Cek Detail</button>
    </div>
  </div>

  <div class="highlight-cover">
    <img
      :src="bukuHighlight.cover"
      :alt="bukuHighlight.judul"
    >
  </div>
</section>
      <section class="welcome">
        <div>
          <span class="breadcrumb">Home / Perpustakaan</span>

          <h2>Koleksi Buku</h2>

          <p>
            Kelola koleksi dan pantau ketersediaan buku
            perpustakaan.
          </p>
        </div>
      </section>

      <section class="category-list">
        <button>Semua Buku</button>
        <button>Teknologi</button>
        <button>Light Novel</button>
        <button>Sains</button>
        <button>Psikologi</button>
        <button>Sejarah</button>
        <button>Novel</button>
      </section>

      <section class="summary">
        <div class="summary-card">
          <div class="summary-icon">📚</div>

          <div>
            <span>Total Buku</span>
            <strong>{{ totalBuku }}</strong>
            <small>koleksi buku</small>
          </div>
        </div>

        <div class="summary-card">
          <div class="summary-icon">⚠</div>

          <div>
            <span>Stok Menipis + Habis</span>
            <strong>{{ stokPerluPerhatian }}</strong>
            <small>perlu diperhatikan</small>
          </div>
        </div>

        <div class="summary-card">
          <div class="summary-icon">▦</div>

          <div>
            <span>Jumlah Kategori</span>
            <strong>{{ jumlahKategori }}</strong>
            <small>kategori tersedia</small>
          </div>
        </div>

        <div class="summary-card">
          <div class="summary-icon">▤</div>

          <div>
            <span>Total Eksemplar</span>
            <strong>{{ totalEksemplar }}</strong>
            <small>seluruh stok buku</small>
          </div>
        </div>
      </section>

      <section
        ref="daftarSection"
        class="section-header daftar-section"
      >
        <div>
          <h2>Daftar Buku</h2>
          <p>Semua koleksi yang tersedia di perpustakaan</p>
        </div>

       <span class="book-count">
        {{ bukuDiurutkan.length }} buku
      </span>
      </section>

      <section class="book-grid">
        <p v-if="loading" class="status-message">
        Sedang mengambil data buku...
        </p>

        <p v-else-if="error" class="status-message error-message">
          {{ error }}
        </p>

        <p
          v-else-if="bukuDiurutkan.length === 0"
          class="status-message"
        >
          Data buku belum tersedia.
        </p>

        <article
          v-else
          v-for="buku in bukuDiurutkan"
          :key="buku.id"
          class="book-card"
        >
          <div class="book-cover">
            <span class="category-label">
              {{ buku.kategori }}
            </span>

            <div class="book-visual">
          <img
            :src="gambarBuku(buku.id)"
            :alt="buku.judul"
            class="book-image"
            @error="gambarError"
          >

          <div class="book-fallback">
            <span class="fallback-icon">📖</span>

            <span class="fallback-title">
              {{ buku.judul }}
            </span>
          </div>
        </div>

            <span
              class="stock-badge"
              :class="classStatus(buku.stok)"
            >
              {{ statusStok(buku.stok) }}
            </span>
          </div>

          <div class="book-info">
            <span class="book-category">
              {{ buku.kategori }}
            </span>

            <h3>{{ buku.judul }}</h3>

            <p>{{ buku.penulis }}</p>

            <div class="book-footer">
              <span>Stok: {{ buku.stok }}</span>

              <button @click="hapusBuku(buku.id)">
                Hapus
              </button>
            </div>
          </div>
        </article>
      </section>
    </main>
  </div>
</template>

<style scoped>
* {
  box-sizing: border-box;
}

.page {
  min-height: 100vh;
  background: #f7f8fa;
  color: #24272b;
  font-family: Arial, sans-serif;
}

.book-visual {
  width: 150px;
  height: 190px;
  position: relative;
}

.book-image {
  width: 150px;
  height: 190px;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.18);
}

.book-fallback {
  width: 150px;
  height: 190px;
  padding: 16px;
  display: none;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 12px;
  text-align: center;
  border-radius: 8px;
  background: linear-gradient(
    145deg,
    #e8f2fa,
    #d9e9f5
  );
  border: 1px solid #d2e1ec;
}

.fallback-icon {
  font-size: 42px;
}

.fallback-title {
  font-size: 12px;
  font-weight: 600;
  line-height: 1.4;
  color: #38546b;
}

.book-image {
  width: 140px;
  height: 190px;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.18);
}

.form-wrapper {
  padding: 20px 32px;
  background: white;
  border-bottom: 1px solid #e2e5e9;
}

.book-form {
  max-width: 1000px;
  margin: 0 auto;
  padding: 24px;
  border: 1px solid #dfe3e8;
  border-radius: 14px;
  background: #f9fafb;
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 20px;
}

.form-header h3 {
  margin: 0 0 5px;
}

.form-header p {
  margin: 0;
  color: #747980;
  font-size: 13px;
}

.close-button {
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 16px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 7px;
}

.form-group label {
  font-size: 13px;
  font-weight: 600;
}

.form-group input {
  padding: 11px 12px;
  border: 1px solid #d4d9df;
  border-radius: 8px;
  outline: none;
}

.form-group input:focus {
  border-color: #0067b9;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.daftar-section {
  scroll-margin-top: 130px;
}

.outline-button.aktif {
  background: #0067b9;
  color: white;
  border-color: #0067b9;
}

.topbar {
  height: 46px;
  padding: 0 32px;
  background: #f1f1f1;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
}

.brand-icon {
  width: 30px;
  height: 30px;
  background: #0067b9;
  color: white;
  border-radius: 50%;
  display: grid;
  place-items: center;
  font-weight: bold;
}

.brand h1 {
  margin: 0;
  font-size: 16px;
  color: #005aa3;
}

.brand span {
  display: none;
}

.top-menu {
  display: flex;
  gap: 26px;
}

.top-menu a {
  color: #333;
  font-size: 13px;
  text-decoration: none;
}

.navbar {
  min-height: 100px;
  padding: 20px 32px;
  background: white;
  border-bottom: 1px solid #e2e5e9;
  display: flex;
  align-items: center;
  gap: 14px;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
}

.status-message {
  grid-column: 1 / -1;
  padding: 30px;
  text-align: center;
  background: white;
  border: 1px solid #e0e4e8;
  border-radius: 12px;
  color: #73787e;
}

.error-message {
  color: #c53a3a;
  background: #fff4f4;
}

.category-button,
.outline-button,
.primary-button {
  height: 46px;
  padding: 0 18px;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
}

.category-button,
.outline-button {
  border: 1px solid #d6dbe1;
  background: white;
  color: #30343a;
}

.primary-button {
  border: none;
  background: #0067b9;
  color: white;
}

.search-box {
  flex: 1;
  position: relative;
  max-width: 570px;
}

.search-box input {
  width: 100%;
  height: 48px;
  padding: 0 18px 0 44px;
  border: 1px solid #ccd2d9;
  border-radius: 24px;
  outline: none;
  font-size: 14px;
}

.search-box input:focus {
  border-color: #0067b9;
}

.search-icon {
  position: absolute;
  left: 18px;
  top: 13px;
  color: #777;
  font-size: 20px;
}

.container {
  max-width: 1320px;
  margin: 0 auto;
  padding: 32px;
}

.highlight-book {
  margin-bottom: 28px;
  padding: 28px;
  border-radius: 18px;
  background: linear-gradient(135deg, #0f3d6e, #1f6fb2);
  color: white;
  display: grid;
  grid-template-columns: 1.4fr 340px;
  gap: 24px;
  align-items: center;
  overflow: hidden;
}

.highlight-label {
  display: inline-block;
  margin-bottom: 12px;
  padding: 6px 12px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.15);
  font-size: 12px;
  font-weight: 600;
}

.highlight-book h2 {
  margin: 0 0 10px;
  font-size: 32px;
  line-height: 1.2;
}

.highlight-author {
  margin: 0 0 12px;
  font-size: 16px;
  font-weight: 600;
  color: #dcecff;
}

.highlight-description {
  max-width: 650px;
  margin: 0 0 18px;
  color: #e7f1fb;
  line-height: 1.6;
}

.highlight-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
}

.highlight-meta span {
  padding: 8px 12px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.14);
  font-size: 13px;
}

.highlight-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.highlight-actions .outline-button {
  background: rgba(255, 255, 255, 0.08);
  color: white;
  border-color: rgba(255, 255, 255, 0.25);
}

.highlight-actions .primary-button {
  background: white;
  color: #0f4f8f;
}

.highlight-cover {
  display: flex;
  justify-content: center;
}

.highlight-cover img {
  width: 100%;
  max-width: 240px;
  border-radius: 14px;
  box-shadow: 0 18px 36px rgba(0, 0, 0, 0.28);
  object-fit: cover;
}

.welcome {
  margin-bottom: 24px;
}

.breadcrumb {
  color: #72777f;
  font-size: 13px;
}

.welcome h2 {
  margin: 18px 0 6px;
  font-size: 28px;
}

.welcome p {
  margin: 0;
  color: #72777f;
}

.category-list {
  display: flex;
  gap: 12px;
  overflow-x: auto;
  padding-bottom: 12px;
  margin-bottom: 24px;
}

.category-list button {
  min-width: 130px;
  padding: 11px 20px;
  background: white;
  border: 1px solid #d7dce2;
  border-radius: 24px;
  cursor: pointer;
  white-space: nowrap;
}

.category-list button:first-child {
  background: #0067b9;
  color: white;
  border-color: #0067b9;
}

.summary {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 38px;
}

.summary-card {
  display: flex;
  gap: 14px;
  padding: 20px;
  background: white;
  border: 1px solid #e0e4e8;
  border-radius: 12px;
}

.summary-icon {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  background: #eef6fc;
  display: grid;
  place-items: center;
  font-size: 20px;
}

.summary-card span {
  display: block;
  color: #71767d;
  font-size: 13px;
}

.summary-card strong {
  display: block;
  margin: 5px 0;
  font-size: 26px;
}

.summary-card small {
  color: #94989e;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: end;
  margin-bottom: 20px;
}

.section-header h2 {
  margin: 0 0 5px;
}

.section-header p {
  margin: 0;
  color: #777c83;
}

.book-count {
  color: #777c83;
  font-size: 14px;
}

.book-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.book-card {
  background: white;
  border: 1px solid #e0e4e8;
  border-radius: 12px;
  overflow: hidden;
}

.book-cover {
  height: 220px;
  position: relative;
  padding: 18px;
  background: #f1f5f8;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cover-placeholder {
  font-size: 72px;
}

.category-label {
  position: absolute;
  top: 14px;
  left: 14px;
  padding: 5px 9px;
  border-radius: 6px;
  background: #e6f3fc;
  color: #0067b9;
  font-size: 11px;
}

.stock-badge {
  position: absolute;
  right: 14px;
  bottom: 14px;
  padding: 6px 10px;
  border-radius: 15px;
  font-size: 12px;
}

.stock-badge.tersedia {
  background: #e8f7ee;
  color: #18864b;
}

.stock-badge.menipis {
  background: #fff4d8;
  color: #b77900;
}

.stock-badge.habis {
  background: #ffe9e9;
  color: #c53a3a;
}

.book-info {
  padding: 18px;
}

.book-category {
  color: #0067b9;
  font-size: 12px;
}

.book-info h3 {
  margin: 7px 0;
  font-size: 16px;
}

.book-info p {
  margin: 0;
  color: #747980;
  font-size: 13px;
}

.book-footer {
  margin-top: 18px;
  padding-top: 14px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.book-footer span {
  font-size: 13px;
  font-weight: 600;
}

.book-footer button {
  border: none;
  background: #fff0f0;
  color: #c53a3a;
  padding: 7px 10px;
  border-radius: 6px;
  cursor: pointer;
}

.empty-card {
  min-height: 335px;
  padding: 30px;
  border: 1px dashed #bbc3cb;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: #73787e;
}

.empty-card strong {
  color: #32363a;
}

.empty-card p {
  max-width: 210px;
  font-size: 13px;
}

.empty-icon {
  width: 52px;
  height: 52px;
  margin-bottom: 15px;
  border-radius: 50%;
  background: #edf5fb;
  color: #0067b9;
  display: grid;
  place-items: center;
  font-size: 28px;
}

@media (max-width: 1023px) {
  .navbar {
    flex-wrap: wrap;
  }

  .search-box {
    order: 3;
    max-width: none;
    flex-basis: 100%;
  }

  .highlight-book {
  grid-template-columns: 1fr;
  }

  .highlight-cover {
  justify-content: flex-start;
  }

  .summary {
    grid-template-columns: repeat(2, 1fr);
  }

  .book-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 767px) {
  .topbar {
    padding: 0 16px;
  }

  .top-menu {
    display: none;
  }

  .navbar {
    padding: 16px;
  }

  .category-button {
    display: none;
  }

  .outline-button,
  .primary-button {
    flex: 1;
  }

  .container {
    padding: 20px 16px;
  }

  .highlight-book {
  padding: 22px 18px;
  }

  .highlight-book h2 {
  font-size: 24px;
  }

  .highlight-cover img {
  max-width: 180px;
  }

  .summary {
    grid-template-columns: 1fr;
  }

  .book-grid {
    grid-template-columns: 1fr;
  }

  .section-header {
    align-items: start;
    gap: 12px;
    flex-direction: column;
  }

  .form-wrapper {
    padding: 16px;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }
}
</style>