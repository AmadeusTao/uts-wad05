# UTS Web Application Development

## Mini Dashboard Perpustakaan

**Nama:** Muhammad Miftahhul Fauzi  
**NIM:** 25120300009  

Project ini merupakan mini dashboard perpustakaan menggunakan Vue 3 sebagai frontend dan FastAPI sebagai backend.

## Fitur

- Menampilkan daftar buku
- Pencarian berdasarkan judul atau penulis
- Sorting buku A-Z dan Z-A berdasarkan judul
- Status stok buku
- Ringkasan statistik perpustakaan
- Tambah buku
- Hapus buku
- Tampilan responsive untuk desktop, tablet, dan mobile
- Highlight buku pilihan

## Status Stok

Threshold status stok yang digunakan:

- Stok 0: **Stok Habis**
- Stok 1 sampai 3: **Menipis**
- Stok 4 atau lebih: **Tersedia**

## Menjalankan Backend

Masuk ke folder backend:

```bash
cd backend
```

Aktifkan virtual environment:

```bash
venv\Scripts\activate
```

Jalankan FastAPI:

```bash
uvicorn main:app --reload
```

Backend berjalan di:

```text
http://127.0.0.1:8000
```

Dokumentasi API tersedia di:

```text
http://127.0.0.1:8000/docs
```

## Menjalankan Frontend

Masuk ke folder frontend:

```bash
cd frontend
```

Install dependency:

```bash
npm install
```

Jalankan Vue:

```bash
npm run dev
```

Frontend berjalan di:

```text
http://localhost:5173
```

## Struktur Data Buku

Setiap buku mempunyai field:

- `id`
- `judul`
- `penulis`
- `kategori`
- `stok`

Data awal buku disimpan pada:

```text
backend/data/books.json
```

Data tersebut dibaca oleh FastAPI dan disimpan sebagai list Python in-memory ketika server dijalankan.

## API

Endpoint yang digunakan:

```text
GET    /buku
POST   /buku
DELETE /buku/{id}
```

## Teknologi

- Vue 3
- Composition API
- JavaScript ES6+
- Fetch API
- FastAPI
- Pydantic
- CSS Flexbox dan Grid
