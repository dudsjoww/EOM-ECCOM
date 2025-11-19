export default function ArtistDashboard() {
  return (
    <main className="min-h-screen bg-neutral-900 text-white p-10 space-y-8">
      <h1 className="text-2xl font-bold">Painel do Tatuador</h1>

      <section>
        <h2 className="text-lg font-semibold mb-2">Clientes Atuais</h2>
        <div className="grid grid-cols-3 gap-4">
          {["João", "Maria", "Lucas"].map((c) => (
            <div key={c} className="bg-zinc-800 p-4 rounded-lg">
              <p>{c}</p>
              <button className="mt-2 text-sm text-red-400">Ver Detalhes</button>
            </div>
          ))}
        </div>
      </section>
    </main>
  )
}
