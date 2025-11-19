export default function ClientDashboard() {
  return (
    <div className="p-6">
      <h2 className="text-xl font-bold mb-4">Agendamentos</h2>
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-gray-200 p-4 rounded-lg">Sessão 1</div>
        <div className="bg-gray-200 p-4 rounded-lg">Sessão 2</div>
      </div>

      <h2 className="text-xl font-bold mt-8 mb-4">Conheça nossos artistas</h2>
      <div className="flex gap-4">
        <div className="bg-red-500 p-6 rounded-full">Artist 1</div>
        <div className="bg-red-500 p-6 rounded-full">Artist 2</div>
      </div>
    </div>
  )
}
