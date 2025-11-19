import Header from "@/components/layout/header"
import Artists from "@/components/artists"

export default function ClientPage() {
  return (
    <main className="min-h-screen bg-white text-black space-y-8">
      <Header />
      <section className="p-8">
        <h2 className="text-xl font-semibold">Pendente</h2>
        <div className="flex gap-4 mt-2">
          <button className="w-20 h-20 border border-black rounded-md flex items-center justify-center">
            +
          </button>
        </div>
      </section>

      <section>
        <h2 className="text-xl font-semibold">Agendamentos</h2>
        <div className="flex gap-4 mt-2">
          <div className="bg-gray-300 p-4 rounded-lg">
            <p>Sessão 1</p>
            <p>Data: 02/02/2026</p>
            <p>Horário: 14:00</p>
            <p>Artista: Soyve</p>
          </div>
          <button className="w-20 h-20 border border-black rounded-md flex items-center justify-center">
            +
          </button>
        </div>
      </section>

      <section>
        <h2 className="text-xl font-semibold">Solicitações</h2>
        <div className="flex gap-2 mt-2">
          {Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="bg-gray-400 w-16 h-16 rounded-md flex items-center justify-center">
              Tattoo
            </div>
          ))}
          <button className="w-16 h-16 border border-black rounded-md flex items-center justify-center">
            +
          </button>
        </div>
      </section>

      <section>
        <h2 className="text-2xl font-bold text-center mt-8">
          Conheça melhor os nossos profissionais
        </h2>
        <Artists />
      </section>
    </main>
  )
}
